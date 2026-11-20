"""Мультфильм-ролик 16:9 для канала Волка (The Sheep Standard): белый фон, Волк говорит под голос,
шерсть овец тает, слова-удары. Таймлайн, голос, звук и субтитры — из kit.py.

Запуск:  python3 cartoon.py stories/<история>.py [--check]
"""
import importlib.util
import math
import os
import subprocess
import sys
import wave
from multiprocessing import Pool

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "sheep-standard", "sketches"))
import kit  # noqa: E402
import wolf as W  # noqa: E402  рисунки Волка и овец

WID, HEI, FPS = 1920, 1080, 24
INK = (17, 17, 17)
RED = (232, 48, 42)
font = kit.font
ENV = {}          # громкость голоса по кадрам: для пасти Волка


def ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def talk_at(T):
    for b in kit.TL["blocks"]:
        if b["start"] <= T < b["start"] + b["dur"]:
            e = ENV.get(b["wav"])
            if e is None:
                return 0.0
            i = int((T - b["start"]) * FPS)
            return float(e[i]) if 0 <= i < len(e) else 0.0
    return 0.0


def blink_at(T):
    return (T % 3.7) < 0.12


def pop_text(d, cx, cy, txt, size, fill, lt, stroke=12):
    """Слово-удар: влетает с увеличением за 0.15 с."""
    s = 1 + 0.5 * (1 - ease(lt / 0.15))
    f = font(kit.F_BLACK, int(size * s))
    w = f.getlength(txt)
    if fill == INK:          # чёрный текст на белом — без обводки, иначе слипается
        stroke = 0
    d.text((cx - w / 2, cy - size * s * 0.6), txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=INK)


# ================= кадры =================
class wolf_shot(kit.Shot):
    """Волк. frame: bust (крупно по пояс) или full (в рост). pose: stand / present / shears."""
    sfx_in = None

    def __init__(self, pose="stand", frame="bust", x=0.5, text=None, text_at=None, text_color=None, prop=None):
        self.pose, self.frame, self.x, self.text, self.text_at, self.text_color, self.prop = pose, frame, x, text, text_at, text_color, prop

    def prepare(self, tl, block):
        self.t_text = block["start"] + kit.wtime(block, self.text_at) if self.text_at is not None else None

    def draw(self, im, lt, dur, T):
        d = ImageDraw.Draw(im)
        bob = math.sin(T * 2.2) * 6
        if self.frame == "bust":
            W.wolf(d, int(WID * self.x) - 60, 1720 + bob, 2.4, self.pose, talk=talk_at(T), blink=blink_at(T))
        else:
            W.wolf(d, int(WID * self.x) - 20, 1040 + bob, 1.45, self.pose, talk=talk_at(T), blink=blink_at(T))
        if self.prop == "note":
            draw_note(d, int(WID * self.x) + 420, 520, 1.3)
        if self.text and self.t_text is not None and T >= self.t_text:
            pop_text(d, WID * 0.78 if self.x < 0.6 else WID * 0.25, 300, self.text, 130, self.text_color or kit.ACCENT, T - self.t_text)


class sheep_shot(kit.Shot):
    """Овца крупно; шерсть идёт от f0 к f1 за время кадра. label — подпись сверху."""
    sfx_in = "pop"

    def __init__(self, f0=1.0, f1=1.0, mood="calm", label=None, label_color=INK, wolf=False, gary=False, sub=None):
        self.f0, self.f1, self.mood, self.label, self.label_color, self.wolf, self.gary, self.sub = f0, f1, mood, label, label_color, wolf, gary, sub

    def draw(self, im, lt, dur, T):
        d = ImageDraw.Draw(im)
        f = self.f0 + (self.f1 - self.f0) * ease(lt / max(0.1, dur * 0.85))
        cx = WID * (0.6 if self.wolf else 0.5)
        W.sheep(d, cx - 60, 1030, 2.6, f, self.mood, seed=9 if self.gary else 5)
        if self.wolf:
            W.wolf(d, 330, 1060, 1.3, "stand", talk=talk_at(T), blink=blink_at(T))
        if self.label:
            pop_text(d, cx, 150, self.label, 110, self.label_color, lt)
        if self.sub:
            f2 = font(kit.F_BOLD, 54)
            d.text((cx - f2.getlength(self.sub) / 2, 230), self.sub, font=f2, fill=(90, 90, 96))


class word_shot(kit.Shot):
    """Крупное слово по центру (с ударом)."""
    sfx_in = "hit"
    shake = True

    def __init__(self, text, sub=None, color=None):
        self.text, self.sub, self.color = text, sub, color

    def draw(self, im, lt, dur, T):
        d = ImageDraw.Draw(im)
        pop_text(d, WID / 2, HEI * 0.46, self.text, 230, self.color or kit.ACCENT, lt, stroke=16)
        if self.sub and lt > 0.3:
            f = font(kit.F_BOLD, 60)
            d.text((WID / 2 - f.getlength(self.sub) / 2, HEI * 0.66), self.sub, font=f, fill=(70, 70, 76))


class title_shot(kit.Shot):
    """Заставка: название ролика + маленький Волк с ножницами."""
    sfx_in = "boom"
    shake = True

    def __init__(self, big, small=""):
        self.big, self.small = big, small

    def draw(self, im, lt, dur, T):
        d = ImageDraw.Draw(im)
        W.wolf(d, 330, 1080, 1.2, "shears", talk=talk_at(T), blink=blink_at(T))
        lines = self.big.split("\n")
        for i, ln in enumerate(lines):
            pop_text(d, WID * 0.6, 380 + i * 170, ln, 150, (255, 255, 255), lt, stroke=16)
        if self.small:
            f = font(kit.F_BOLD, 52)
            d.text((WID * 0.6 - f.getlength(self.small) / 2, 380 + len(lines) * 170), self.small, font=f, fill=(80, 80, 86))


def draw_note(d, x, y, s=1.0):
    W.shape(d, [(x, y), (x + 230 * s, y), (x + 230 * s, y + 115 * s), (x, y + 115 * s)], (233, 211, 168), 7, seed=60)
    f = font(kit.F_BLACK, int(32 * s))
    d.text((x + 22 * s, y + 18 * s), "1 WOOL", font=f, fill=INK)
    d.ellipse((x + 155 * s, y + 55 * s, x + 205 * s, y + 103 * s), outline=RED, width=int(6 * s))


# ================= отрисовка =================
def envelope(wav):
    with wave.open(wav) as w_:
        x = np.frombuffer(w_.readframes(w_.getnframes()), np.int16).astype(np.float32) / 32768
        sr = w_.getframerate()
    hop = sr // FPS
    n = len(x) // hop
    rms = np.array([np.sqrt((x[i * hop:(i + 1) * hop] ** 2).mean()) for i in range(n)])
    e = np.clip((rms - 0.015) / 0.09, 0, 1)
    e = np.convolve(e, [0.25, 0.5, 0.25], "same")
    return e


def render_frame(T):
    im = Image.new("RGB", (WID, HEI), (255, 255, 255))
    W.BOIL = int(T * 8)              # «дрожание» линий 8 раз в секунду
    cur = None
    for s in kit.TL["shots"]:
        if s[0] <= T:
            cur = s
    if cur:
        t0, shot, bl, t1 = cur
        lt = T - t0
        shot.draw(im, lt, t1 - t0, T)
        z = 1 + 0.04 * ease(lt / max(0.1, t1 - t0))          # медленный наезд камеры
        sh = 0.0
        for ts in kit.TL["shakes"]:
            if 0 <= T - ts < 0.3:
                sh = max(sh, 1 - (T - ts) / 0.3)
        dx, dy = math.sin(T * 91) * 14 * sh, math.cos(T * 77) * 10 * sh
        k = 1 / z
        im = im.transform((WID, HEI), Image.AFFINE, (k, 0, WID / 2 * (1 - k) + dx, 0, k, HEI / 2 * (1 - k) + dy),
                          resample=Image.BILINEAR, fillcolor=(255, 255, 255))
    fade = min(1.0, T / 0.3, (kit.TL["total"] - T) / 0.8)
    if fade < 1:
        im = Image.fromarray((np.asarray(im, dtype=np.float32) * max(0.0, fade)).astype(np.uint8))
    return im


def render_part(args):
    k, f0, f1, out = args
    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{WID}x{HEI}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", out]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(f0, f1):
        ff.stdin.write(render_frame(i / FPS).tobytes())
    ff.stdin.close()
    ff.wait()
    return out


def main():
    path = sys.argv[1]
    sys.modules["cartoon"] = sys.modules[__name__]
    sys.modules["kit"] = kit
    spec = importlib.util.spec_from_file_location("story", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    name = mod.STORY["name"]
    bdir = os.environ.get("YTKIT_BUILD", os.path.expanduser(f"~/.cache/ytkit/{name}"))
    os.makedirs(bdir, exist_ok=True)
    kit.TL = build = kit.build_timeline(mod, bdir)
    for b in build["blocks"]:
        ENV[b["wav"]] = envelope(b["wav"])
    total = build["total"]
    print(f"{name}: {total:.1f} с, кадров {len(build['shots'])}")
    if "--check" in sys.argv:
        ts = [s[0] + 0.6 for s in build["shots"]]
        cols = 4
        rows = (len(ts) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * 480, rows * 270), (40, 40, 40))
        for i, t in enumerate(ts):
            sheet.paste(render_frame(t).resize((480, 270)), ((i % cols) * 480, (i // cols) * 270))
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
    kit.build_audio(build, wav)
    out = os.path.join(bdir, f"{name}.mp4")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", os.path.join(bdir, "video.mp4"), "-i", wav, "-c:v", "libx264",
                    "-crf", "21", "-pix_fmt", "yuv420p", "-af", "loudnorm=I=-14:TP=-1.5", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", out], check=True)
    kit.write_srt(build, os.path.join(bdir, f"{name}.srt"))
    print("ГОТОВО", out)


if __name__ == "__main__":
    main()
