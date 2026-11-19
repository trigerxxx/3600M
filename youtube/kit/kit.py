"""YT-KIT: вертикальные истории в формате «слово за словом» (Shorts / TikTok / Reels).
Правила формата: FORMAT.md. Пример сценария: stories/everest_vertical.py.

Запуск:  python3 kit.py stories/<история>.py            → готовый mp4
         python3 kit.py stories/<история>.py --check    → только контрольный лист кадров (быстро)
Нужно: ffmpeg, Pillow, numpy, scipy, ключ ElevenLabs в Network secrets окружения."""
import importlib.util
import math
import os
import random
import re
import subprocess
import sys
import wave
from multiprocessing import Pool

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import scenes  # noqa: E402
import sound  # noqa: E402
import voice  # noqa: E402

W, H, FPS = 1080, 1920, 30
VIS_CY = 640                 # центр зоны картинки
CAP_Y = 1110                 # линия слов (выше кнопок Shorts/TikTok)
HUD_Y = 120
F_BLACK, F_BOLD, F_SEMI = scenes.F_BLACK, scenes.F_BOLD, scenes.F_SEMI
F_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
font = scenes.font

ACCENT = (255, 122, 26)       # переопределяется в STORY
STORY = {}


def ease(u):
    u = max(0.0, min(1.0, u))
    return 1 - (1 - u) ** 3


def rr_mask(w, h, r):
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=255)
    return m


def view(still, ow, oh, z, cx, cy):
    """Кадрирование большого кадра сцены под окно ow×oh с зумом z и центром (cx, cy) 0..1."""
    BW, BH = still.size
    k = min(BW / ow, BH / oh) / z
    vw, vh = ow * k, oh * k
    left = min(max(cx * BW - vw / 2, 0), BW - vw)
    top = min(max(cy * BH - vh / 2, 0), BH - vh)
    return still.transform((ow, oh), Image.AFFINE, (k, 0, left, 0, k, top), resample=Image.BILINEAR)


_stills = {}


def still_of(name, p, seed=5):
    key = (name, tuple(sorted((k, str(v)) for k, v in p.items())), seed)
    if key not in _stills:
        _stills[key] = scenes.render_still(name, p, seed=seed)
    return _stills[key]


# =============== кадры (shots) ===============
class Shot:
    sfx_in = "tick"          # звук при появлении кадра

    def prepare(self, tl, block):
        pass

    def draw(self, im, lt, dur, T):
        raise NotImplementedError


class scene(Shot):
    """Иллюстрация из scenes.py. mode: card (карточка), circle (линза/прицел), full (на весь верх с затуханием)."""

    def __init__(self, name, mode="card", z=(1.0, 1.1), cx=0.5, cy=0.5, cross=False, **p):
        self.name, self.mode, self.z, self.cx, self.cy, self.cross, self.p = name, mode, z, cx, cy, cross, p

    def draw(self, im, lt, dur, T):
        st = getattr(self, "img", None) or still_of(self.name, self.p)
        z = self.z[0] + (self.z[1] - self.z[0]) * min(1, lt / max(dur, 0.1))
        if self.mode == "card":
            w, h = 1000, 600
            img = view(st, w, h, z, self.cx, self.cy)
            x, y = (W - w) // 2, VIS_CY - h // 2
            sh = Image.new("L", (W, H), 0)
            ImageDraw.Draw(sh).rounded_rectangle((x + 10, y + 26, x + w + 10, y + h + 26), 36, fill=200)
            im.paste((0, 0, 0), (0, 0), sh.filter(ImageFilter.GaussianBlur(24)))
            im.paste(img, (x, y), rr_mask(w, h, 36))
            ImageDraw.Draw(im).rounded_rectangle((x, y, x + w, y + h), 36, outline=(70, 76, 92), width=3)
        elif self.mode == "circle":
            d = 860
            img = view(st, d, d, z, self.cx, self.cy)
            x, y = (W - d) // 2, VIS_CY - d // 2
            m = Image.new("L", (d, d), 0)
            ImageDraw.Draw(m).ellipse((0, 0, d - 1, d - 1), fill=255)
            # тёмный край линзы
            vg = Image.new("L", (d, d), 0)
            ImageDraw.Draw(vg).ellipse((60, 60, d - 60, d - 60), fill=255)
            vg = vg.filter(ImageFilter.GaussianBlur(70))
            img = Image.composite(img, Image.new("RGB", (d, d), (0, 0, 0)), vg)
            im.paste(img, (x, y), m)
            dr = ImageDraw.Draw(im)
            dr.ellipse((x - 6, y - 6, x + d + 6, y + d + 6), outline=(28, 30, 38), width=16)
            dr.ellipse((x, y, x + d, y + d), outline=(90, 96, 110), width=3)
            if self.cross:
                c = (20, 20, 24)
                dr.line((x + 40, VIS_CY, x + d - 40, VIS_CY), fill=c, width=3)
                dr.line((W // 2, y + 40, W // 2, y + d - 40), fill=c, width=3)
        else:  # full
            h = 1350
            img = view(st, W, h, z, self.cx, self.cy)
            m = Image.new("L", (1, h), 255)
            for yy in range(h - 420, h):
                m.putpixel((0, yy), int(255 * (1 - (yy - (h - 420)) / 420) ** 1.5))
            im.paste(img, (0, 0), m.resize((W, h)))


class device(Shot):
    """Экран телефона или трекера. msgs: [(слово, текст, 'in'|'out'|'sys', 'alert'?)] — сообщение появляется на этом слове."""
    sfx_in = "tick"

    def __init__(self, kind="phone", title="Unknown", status="online", msgs=()):
        self.kind, self.title, self.status, self.msgs = kind, title, status, list(msgs)

    def prepare(self, tl, block):
        self.times = []
        for m in self.msgs:
            t = block["start"] + wtime(block, m[0])
            self.times.append(t)
            tl["sfx"].append((t, "msg" if self.kind == "phone" else "beep"))

    def draw(self, im, lt, dur, T):
        tracker = self.kind == "tracker"
        w, h = 660, 1060
        x, y = (W - w) // 2, 200
        d = ImageDraw.Draw(im)
        body = (40, 44, 52) if tracker else (14, 16, 22)
        d.rounded_rectangle((x - 14, y - 14, x + w + 14, y + h + 14), 70, fill=(6, 7, 10))
        d.rounded_rectangle((x, y, x + w, y + h), 60, fill=body, outline=(60, 64, 76), width=3)
        scr = (x + 26, y + 30, x + w - 26, y + h - 30)
        d.rounded_rectangle(scr, 44, fill=(22, 44, 32) if tracker else (18, 22, 30))
        hf = font(F_MONO if tracker else F_BOLD, 38)
        sf = font(F_MONO if tracker else F_SEMI, 26)
        d.text((scr[0] + 40, scr[1] + 34), self.title, font=hf, fill=(170, 255, 190) if tracker else (240, 242, 248))
        stc = (255, 90, 80) if "NO" in self.status.upper() else ((120, 220, 140) if tracker else (90, 200, 120))
        d.text((scr[0] + 40, scr[1] + 84), self.status, font=sf, fill=stc)
        d.line((scr[0] + 20, scr[1] + 134, scr[2] - 20, scr[1] + 134), fill=(60, 80, 70) if tracker else (40, 46, 60), width=2)
        mf = font(F_MONO if tracker else F_BOLD, 46 if tracker else 42)
        items = []
        for (m, t0) in zip(self.msgs, self.times):
            if T >= t0:
                items.append((m, min(1, (T - t0) / 0.18)))
        # раскладка сверху вниз; если не помещается над словом, старые сообщения уходят
        lim = CAP_Y - 110
        boxes = []
        for (m, a) in items:
            side = m[2] if len(m) > 2 else "in"
            alert = len(m) > 3 and m[3] == "alert"
            words, lines, cur = m[1].split(), [], ""
            for wd in words:
                if mf.getlength(cur + " " + wd) > 470 and cur:
                    lines.append(cur)
                    cur = wd
                else:
                    cur = (cur + " " + wd).strip()
            lines.append(cur)
            boxes.append([m, a, side, alert, lines, max(mf.getlength(l_) for l_ in lines) + 48, 30 + 56 * len(lines), 0])
        while boxes and scr[1] + 160 + sum(bx[6] + 18 for bx in boxes) > lim:
            boxes.pop(0)
        yy = scr[1] + 160
        for bx in boxes:
            bx[7] = yy
            yy += bx[6] + 18
        for (m, a, side, alert, lines, bw, bh, yy) in boxes:
            off = (1 - ease(a)) * 30
            if side == "out":
                bx = scr[2] - 30 - bw
                fill = ACCENT if not tracker else (60, 120, 80)
                tc = (20, 10, 4) if not tracker else (220, 255, 230)
            elif side == "sys":
                bx = (scr[0] + scr[2] - bw) / 2
                fill, tc = ((10, 26, 16), (170, 255, 190)) if tracker else ((30, 34, 44), (180, 186, 196))
            else:
                bx = scr[0] + 30
                fill = (40, 46, 60) if not tracker else (30, 70, 44)
                tc = (240, 242, 248) if not tracker else (170, 255, 190)
            if alert:
                fill, tc = (150, 20, 18), (255, 230, 225)
            yy2 = yy + off
            d.rounded_rectangle((bx, yy2, bx + bw, yy2 + bh), 26, fill=fill)
            for i, ln in enumerate(lines):
                d.text((bx + 24, yy2 + 14 + i * 56), ln, font=mf, fill=tc)


class stamp(Shot):
    """Красный штамп: «RULE #1», «MISTAKE #1». Прилетает с ударом и тряской."""
    sfx_in = "hit"
    shake = True

    def __init__(self, text, sub="", bg=None, color=(232, 48, 42), **p):
        self.text, self.sub, self.bg, self.color, self.p = text, sub, bg, color, p

    def draw(self, im, lt, dur, T):
        if self.bg:
            st = still_of(self.bg, self.p)
            img = view(st, W, 1350, 1.08, 0.5, 0.5)
            img = Image.fromarray((np.asarray(img) * 0.35).astype(np.uint8))
            im.paste(img, (0, 0))
        f = font(F_BLACK, 120)
        tw = f.getlength(self.text)
        lay = Image.new("RGBA", (int(tw) + 120, 230), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        d.rounded_rectangle((8, 8, lay.width - 8, 222), 26, outline=self.color + (255,), width=12, fill=(40, 6, 6, 200))
        d.text((60, 36), self.text, font=f, fill=self.color + (255,))
        s = 1 + 0.7 * (1 - ease(lt / 0.14))
        lay = lay.resize((int(lay.width * s), int(lay.height * s)), Image.BILINEAR).rotate(6, expand=True, resample=Image.BICUBIC)
        im.paste(lay, ((W - lay.width) // 2, VIS_CY - lay.height // 2), lay)
        if self.sub and lt > 0.25:
            scenes.text_c(ImageDraw.Draw(im), W / 2, VIS_CY + 170, self.sub, font(F_BOLD, 44), (235, 225, 220))


class counter(Shot):
    """Большое число, которое досчитывает до значения."""
    sfx_in = "tick"

    def __init__(self, to, frm=0, label="", suffix="", color=None, dur=1.0):
        self.to, self.frm, self.label, self.suffix, self.color, self.cd = to, frm, label, suffix, color, dur

    def draw(self, im, lt, dur, T):
        v = self.frm + (self.to - self.frm) * ease(lt / self.cd)
        txt = f"{int(round(v)):,}{self.suffix}"
        d = ImageDraw.Draw(im)
        if self.label:
            scenes.text_c(d, W / 2, VIS_CY - 240, self.label, font(F_BOLD, 46), (200, 206, 220), spacing=8)
        col = self.color or ACCENT
        im2 = scenes.add_glow_layer(im, lambda g: scenes.text_c(g, W / 2, VIS_CY - 150, txt, font(F_BLACK, 300), col), 40, 0.7)
        im.paste(im2)
        scenes.text_c(ImageDraw.Draw(im), W / 2, VIS_CY - 150, txt, font(F_BLACK, 300), (255, 255, 255))


class tally(Shot):
    """Фляга с зарубками: число зарубок растёт от frm до to за первые 70% кадра."""
    sfx_in = "tick"

    def __init__(self, frm, to, dark=False):
        self.frm, self.to, self.dark = frm, to, dark

    def draw(self, im, lt, dur, T):
        n = int(round(self.frm + (self.to - self.frm) * min(1, lt / max(0.1, dur * 0.7))))
        key = ("flask", n, self.dark)
        if key not in _stills:
            _stills[key] = scenes.flask_img(random.Random(3), n, self.dark)
        sc = scene("flask", mode="card", z=(1.05, 1.1))
        sc.img = _stills[key]
        sc.draw(im, lt, dur, T)


class news(Shot):
    """Телевизор с выпуском новостей: картинка сцены, плашка BREAKING, бегущая строка."""
    sfx_in = "tick"

    def __init__(self, headline, ticker="", bg="basecamp", **p):
        self.headline, self.ticker, self.bg, self.p = headline, ticker, bg, p

    def draw(self, im, lt, dur, T):
        w, h = 1000, 640
        x, y = (W - w) // 2, VIS_CY - h // 2
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((x - 22, y - 22, x + w + 22, y + h + 22), 30, fill=(10, 11, 14), outline=(50, 54, 64), width=3)
        img = view(still_of(self.bg, self.p), w, h, 1.05 + 0.05 * lt / max(dur, 0.1), 0.5, 0.45)
        im.paste(img, (x, y))
        d = ImageDraw.Draw(im)
        d.rectangle((x, y + h - 190, x + 250, y + h - 130), fill=(232, 48, 42))
        d.text((x + 22, y + h - 182), "BREAKING", font=font(F_BLACK, 40), fill=(255, 255, 255))
        d.rectangle((x, y + h - 130, x + w, y + h - 50), fill=(245, 245, 245))
        d.text((x + 22, y + h - 118), self.headline, font=font(F_BLACK, 50), fill=(20, 20, 24))
        d.rectangle((x, y + h - 50, x + w, y + h), fill=(20, 20, 26))
        tf = font(F_BOLD, 30)
        tx = x + w - (lt * 220) % (tf.getlength(self.ticker + "   •   ") + w)
        d.text((tx, y + h - 42), self.ticker + "   •   " + self.ticker, font=tf, fill=(220, 220, 230))
        d.rectangle((x + w - 90, y + 20, x + w - 20, y + 64), fill=(232, 48, 42))
        d.text((x + w - 80, y + 24), "LIVE", font=font(F_BLACK, 30), fill=(255, 255, 255))


class title(Shot):
    """Крупный текст: название главы, итог, призыв."""
    sfx_in = "hit"

    def __init__(self, big, small="", color=None):
        self.big, self.small, self.color = big, small, color

    def draw(self, im, lt, dur, T):
        col = self.color or ACCENT
        lines = self.big.split("\n")
        f = font(F_BLACK, 140 if max(len(l_) for l_ in lines) < 11 else 104)
        y0 = VIS_CY - len(lines) * 75
        if self.small:
            scenes.text_c(ImageDraw.Draw(im), W / 2, y0 - 90, self.small, font(F_BOLD, 44), (200, 206, 220), spacing=10)

        def g(dr):
            for i, ln in enumerate(lines):
                scenes.text_c(dr, W / 2, y0 + i * 150, ln, f, col)
        im.paste(scenes.add_glow_layer(im, g, 36, 0.8))
        dr = ImageDraw.Draw(im)
        for i, ln in enumerate(lines):
            scenes.text_c(dr, W / 2, y0 + i * 150, ln, f, (255, 255, 255))


# =============== сценарий → таймлайн ===============
def widx(b, key):
    """Номер слова: число, или само слово ('ripped'), или 'one#2' — второе вхождение."""
    if isinstance(key, int):
        return key
    word, _, n = key.partition("#")
    n = int(n or 1)
    toks = [re.sub(r"[^\w'-]", "", t).lower() for t in b["text"].replace("*", "").split()]
    c = 0
    for i, t in enumerate(toks):
        if t == word.lower():
            c += 1
            if c == n:
                return i
    raise ValueError(f"нет слова {key!r} в блоке: {b['text'][:50]}")


def wtime(b, key):
    """Время (от начала блока) слова key; дробное число = секунды."""
    if isinstance(key, float):
        return key
    i = widx(b, key)
    return b["words"][min(i, len(b["words"]) - 1)][0] if i else 0.0


def block(text, shots, hud=None, sfx=(), mood="dark", amb="wind_soft", pause=0.3):
    """Один кусок озвучки. В тексте *слово* = подсветка. shots: [(номер слова, кадр)] — кадр меняется на этом слове."""
    return dict(text=text, shots=list(shots), hud=hud, sfx=list(sfx), mood=mood, amb=amb, pause=pause)


def build_timeline(story_mod, bdir):
    global ACCENT
    st = story_mod.STORY
    ACCENT = tuple(st.get("accent", ACCENT))
    blocks = story_mod.BLOCKS
    tl = dict(blocks=[], shots=[], sfx=[], words=[], shakes=[])
    clock = 0.0
    clean = [re.sub(r"\*", "", b["text"]) for b in blocks]
    for i, b in enumerate(blocks):
        wav = os.path.join(bdir, f"b{i:02d}.wav")
        words = voice.say(clean[i], wav, st.get("voice", "brian"), clean[i - 1] if i else "",
                          clean[i + 1] if i + 1 < len(blocks) else "", speed=st.get("speed", 1.0))
        tokens = b["text"].split()
        if len(tokens) != len(words):
            print(f"  внимание: блок {i} — слов {len(tokens)} в тексте, {len(words)} в озвучке")
        with wave.open(wav) as w_:
            vd = w_.getnframes() / w_.getframerate()
        bl = dict(b, start=clock, words=words, wav=wav, dur=vd + b["pause"])
        for k, (t0, t1, wd) in enumerate(words):
            hl = k < len(tokens) and tokens[k].startswith("*")
            tl["words"].append((clock + t0, clock + t1, re.sub(r"[*]", "", wd), hl))
        for (wi, shot) in b["shots"]:
            tl["shots"].append([clock + wtime(bl, wi), shot, bl])
        for (wi, name) in b["sfx"]:
            tl["sfx"].append((clock + wtime(bl, wi), name))
        tl["blocks"].append(bl)
        clock += bl["dur"]
    tl["total"] = clock + st.get("end_hold", 1.2)
    tl["shots"].sort(key=lambda s: s[0])
    for k, s in enumerate(tl["shots"]):
        s.append(tl["shots"][k + 1][0] if k + 1 < len(tl["shots"]) else tl["total"])
        s[1].prepare(tl, s[2])
        if k > 0 and s[1].sfx_in:
            tl["sfx"].append((s[0], s[1].sfx_in))
        if getattr(s[1], "shake", False):
            tl["shakes"].append(s[0])
    for t, n in tl["sfx"]:
        if n in ("boom", "hit"):
            tl["shakes"].append(t)
    return tl


# =============== отрисовка кадра ===============
BG = None
GRAIN = None
DUST = None


def init_post():
    global BG, GRAIN, DUST
    yy, xx = np.mgrid[0:H, 0:W]
    g = (np.linspace(16, 4, H)[:, None] * np.ones((1, W)))
    r = np.sqrt(((xx - W / 2) / (W * 0.7)) ** 2 + ((yy - VIS_CY) / (H * 0.5)) ** 2)
    v = np.clip(1.2 - r, 0.25, 1.0)
    bg = np.stack([g * 0.8 * v, g * 0.85 * v, g * 1.15 * v], -1)
    BG = Image.fromarray(bg.clip(0, 255).astype(np.uint8))
    rng = np.random.default_rng(2)
    GRAIN = [rng.normal(0, 4.5, (H, W, 1)).astype(np.float32) for _ in range(5)]
    DUST = rng.uniform(0, 1, (70, 4))


_cap_cache = {}


def cap_img(word, hl):
    k = (word, hl)
    if k not in _cap_cache:
        f = font(F_BLACK, 100)
        txt = word.upper()
        w = int(f.getlength(txt)) + 80
        lay = Image.new("RGBA", (w, 170), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        if hl:
            gl = Image.new("RGBA", lay.size, (0, 0, 0, 0))
            ImageDraw.Draw(gl).text((40, 20), txt, font=f, fill=ACCENT + (200,))
            lay.alpha_composite(gl.filter(ImageFilter.GaussianBlur(18)))
        d.text((40, 20), txt, font=f, fill=(ACCENT if hl else (255, 255, 255)) + (255,), stroke_width=7, stroke_fill=(0, 0, 0, 255))
        _cap_cache[k] = lay
    return _cap_cache[k]


def hud_draw(im, T, tl):
    bl = None
    for b in tl["blocks"]:
        if b["start"] <= T:
            bl = b
    if not bl or not bl.get("hud"):
        return
    left, clk = bl["hud"]
    d = ImageDraw.Draw(im)
    f = font(F_BOLD, 30)
    d.ellipse((60, HUD_Y + 8, 76, HUD_Y + 24), fill=(232, 48, 42) if int(T * 1.5) % 2 == 0 else (90, 20, 18))
    d.text((92, HUD_Y), left, font=f, fill=(225, 228, 236))
    if clk:
        h_, m_, s_ = (int(x) for x in clk.split(":"))
        secs = h_ * 3600 + m_ * 60 + s_ + int(T - bl["start"])
        txt = f"{secs // 3600 % 24:02d}:{secs // 60 % 60:02d}:{secs % 60:02d}"
        fm = font(F_MONO, 34)
        d.text((W - 60 - fm.getlength(txt), HUD_Y - 3), txt, font=fm, fill=(225, 228, 236))
    d.line((60, HUD_Y + 56, W - 60, HUD_Y + 56), fill=(50, 54, 64), width=2)


def render_frame(T, tl):
    im = BG.copy()
    cur = None
    for s in tl["shots"]:
        if s[0] <= T:
            cur = s
    lt = 0.0
    if cur:
        t0, shot, bl, t1 = cur
        lt = T - t0
        shot.draw(im, lt, t1 - t0, T)
    # пылинки
    d = ImageDraw.Draw(im)
    for x0, y0, sp, sz in DUST:
        x = (x0 * W + T * 12 * sp) % W
        y = (y0 * H - T * 25 * sp) % H
        r = 1 + sz * 2
        c = int(70 + 80 * sz)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(c, c - 10, c - 25))
    # «поп» при смене кадра
    if cur and lt < 0.14:
        s = 1 + 0.05 * (1 - ease(lt / 0.14))
        k = 1 / s
        im = im.transform((W, H), Image.AFFINE, (k, 0, W / 2 * (1 - k), 0, k, VIS_CY * (1 - k)), resample=Image.BILINEAR)
    # тряска
    sh = 0.0
    for ts in tl["shakes"]:
        if 0 <= T - ts < 0.35:
            sh = max(sh, 1 - (T - ts) / 0.35)
    if sh:
        dx, dy = math.sin(T * 91) * 16 * sh, math.cos(T * 77) * 12 * sh
        im = im.transform((W, H), Image.AFFINE, (1, 0, dx, 0, 1, dy), resample=Image.BILINEAR)
    hud_draw(im, T, tl)
    # слово
    wcur = None
    for (a, b, wd, hl) in tl["words"]:
        if a <= T:
            wcur = (a, b, wd, hl)
        else:
            break
    if wcur and T - wcur[1] < 0.5:
        lay = cap_img(wcur[2], wcur[3])
        s = 1 + 0.16 * (1 - ease((T - wcur[0]) / 0.1))
        if s > 1.001:
            lay = lay.resize((int(lay.width * s), int(lay.height * s)), Image.BILINEAR)
        im.paste(lay, ((W - lay.width) // 2, CAP_Y - lay.height // 2), lay)
    a = np.asarray(im, dtype=np.float32) + GRAIN[int(T * FPS) % 5]
    fade = min(1.0, T / 0.25, (tl["total"] - T) / 0.8)
    return Image.fromarray((a * max(0.0, fade)).clip(0, 255).astype(np.uint8))


TL = None


def render_part(args):
    k, f0, f1, out = args
    init_post()
    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", out]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(f0, f1):
        ff.stdin.write(render_frame(i / FPS, TL).tobytes())
    ff.stdin.close()
    ff.wait()
    return out


# =============== звук ===============
def build_audio(tl, path):
    SR = sound.SR
    N = int((tl["total"] + 1) * SR)
    vo, amb, mus, fx = (np.zeros((N, 2)) for _ in range(4))

    def place(buf, x, at):
        s = int(at * SR)
        e = min(len(buf), s + len(x))
        if e > s:
            buf[s:e] += x[: e - s]

    def runs(key):
        out = []
        for b in tl["blocks"]:
            if out and out[-1][0] == b[key]:
                out[-1][2] = b["start"] + b["dur"]
            else:
                out.append([b[key], b["start"], b["start"] + b["dur"]])
        out[-1][2] = tl["total"]
        return out

    def fade(x, f):
        n = min(int(f * SR), len(x) // 2)
        w = np.sin(np.linspace(0, np.pi / 2, n))[:, None]
        x[:n] *= w
        x[-n:] *= w[::-1]
        return x

    for k, (kind, a, b) in enumerate(runs("amb")):
        place(amb, fade(sound.amb(kind, b - a + 1.5, k), 0.7), max(0, a - 0.5))
    for k, (mood, a, b) in enumerate(runs("mood")):
        place(mus, fade(sound.pad(mood, b - a + 2, k), 1.0), max(0, a - 0.8))
    for b in tl["blocks"]:
        with wave.open(b["wav"]) as w_:
            x = np.frombuffer(w_.readframes(w_.getnframes()), np.int16).astype(np.float32) / 32768
        v = sound.reverb(sound.st(sound.hp(x, 80)), 0.5, 0.06)
        place(vo, v / (np.abs(v).max() + 1e-9) * 0.85, b["start"])
    for k, (t, name) in enumerate(tl["sfx"]):
        place(fx, sound.fx(name, k), t)
    env = np.abs(vo).max(1)
    win = int(0.2 * SR)
    c = np.concatenate([[0], np.cumsum(env)])
    idx = np.arange(len(env))
    env = (c[np.minimum(idx + win // 2, len(env))] - c[np.maximum(idx - win // 2, 0)]) / win
    duck = (1 - 0.5 * np.clip(env / 0.08, 0, 1))[:, None]
    mix = vo + (amb * 0.8 + mus * 0.9) * duck + fx
    end = int(tl["total"] * SR)
    fo = int(0.8 * SR)
    mix[end - fo:end] *= np.linspace(1, 0, fo)[:, None]
    mix = mix[:end] / np.abs(mix[:end]).max() * 0.9
    with wave.open(path, "w") as w_:
        w_.setnchannels(2)
        w_.setsampwidth(2)
        w_.setframerate(SR)
        w_.writeframes((mix * 32767).astype(np.int16).tobytes())


def write_srt(tl, path):
    """Субтитры по фразам (для загрузки на YouTube)."""
    def ts(x):
        return f"{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(x % 1 * 1000):03d}"
    out, k = [], 1
    for b in tl["blocks"]:
        sent = [s for s in re.split(r"(?<=[.!?])\s+", re.sub(r"\*", "", b["text"])) if s]
        ws = b["words"]
        i = 0
        for s in sent:
            n = len(s.split())
            seg = ws[i:i + n]
            if seg:
                out.append(f"{k}\n{ts(b['start'] + seg[0][0])} --> {ts(b['start'] + seg[-1][1])}\n{s}\n")
                k += 1
            i += n
    open(path, "w").write("\n".join(out))


def main():
    global TL
    path = sys.argv[1]
    sys.modules["kit"] = sys.modules[__name__]   # сценарий делает `from kit import ...` — пусть это будет этот же модуль
    spec = importlib.util.spec_from_file_location("story", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    name = mod.STORY["name"]
    bdir = os.environ.get("YTKIT_BUILD", os.path.expanduser(f"~/.cache/ytkit/{name}"))
    os.makedirs(bdir, exist_ok=True)
    TL = build_timeline(mod, bdir)
    total = TL["total"]
    print(f"{name}: {total:.1f} с, кадров {len(TL['shots'])}, слов {len(TL['words'])}")
    init_post()
    if "--check" in sys.argv:
        ts = [s[0] + 0.5 for s in TL["shots"]]
        cols = 6
        rows = (len(ts) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * 270, rows * 480))
        for i, t in enumerate(ts):
            sheet.paste(render_frame(t, TL).resize((270, 480)), ((i % cols) * 270, (i // cols) * 480))
        out = os.path.join(bdir, "check.png")
        sheet.save(out)
        print("контрольный лист:", out)
        return
    n = int(total * FPS)
    parts = 4
    jobs = [(k, n * k // parts, n * (k + 1) // parts, os.path.join(bdir, f"part{k}.mp4")) for k in range(parts)]
    with Pool(parts) as pool:
        files = pool.map(render_part, jobs)
    lst = os.path.join(bdir, "parts.txt")
    open(lst, "w").write("".join(f"file '{f}'\n" for f in files))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                    os.path.join(bdir, "video.mp4")], check=True)
    wav = os.path.join(bdir, "mix.wav")
    build_audio(TL, wav)
    out = os.path.join(bdir, f"{name}.mp4")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", os.path.join(bdir, "video.mp4"), "-i", wav, "-c:v", "libx264",
                    "-crf", "21", "-maxrate", "10M", "-bufsize", "20M", "-pix_fmt", "yuv420p", "-af", "loudnorm=I=-14:TP=-1.5",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    write_srt(TL, os.path.join(bdir, f"{name}.srt"))
    print("ГОТОВО", out)


if __name__ == "__main__":
    main()
