"""Сборка длинного ролика: таймлайн → кадры (4 процесса) → звук → субтитры → MP4.
Запуск: python3 render.py [--preview]   (нужны piper, ffmpeg, Pillow, numpy, scipy)"""
import math
import os
import re
import subprocess
import sys
import wave
from multiprocessing import Pool

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import scenes
import sound
from script import SEGMENTS, TITLE

HERE = os.path.dirname(os.path.abspath(__file__))
SC = os.path.dirname(HERE)
B = os.path.join(HERE, "build")
os.makedirs(B, exist_ok=True)
W, H, FPS = 1920, 1080, 24
PREVIEW = "--preview" in sys.argv
LEAD, TAIL = 0.5, 1.3
PIPER = [f"{SC}/tts/bin/piper", "-m", f"{SC}/voices/en_US-ryan-high.onnx"]

INTERIOR = {"tent_int", "flask", "tracker", "radio", "rule", "news", "hands", "tent_door"}
SNOW = {"storm": (520, -1300, 320, True), "wind": (260, -420, 160, False), "wind_soft": (160, -110, 90, False),
        "camp": (120, -80, 70, False), "silence": (90, -20, 50, False), "tent": (120, -80, 70, False)}


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def wav_read(path):
    with wave.open(path) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        return x, w.getframerate()


def sentence_times(path, n):
    """Время начала/конца каждого предложения по паузам в озвучке."""
    x, sr = wav_read(path)
    hop = int(sr * 0.02)
    rms = np.array([np.sqrt((x[i:i + hop] ** 2).mean()) for i in range(0, len(x) - hop, hop)])
    voiced = rms > 0.012
    gaps, i = [], 0
    while i < len(voiced):
        if not voiced[i]:
            j = i
            while j < len(voiced) and not voiced[j]:
                j += 1
            if i > 0 and j < len(voiced):
                gaps.append((j - i, i * 0.02, j * 0.02))
            i = j
        else:
            i += 1
    dur = len(x) / sr
    gaps = sorted(sorted(gaps, reverse=True)[: n - 1], key=lambda g: g[1])
    if len(gaps) != n - 1:
        return [(dur * k / n, dur * (k + 1) / n) for k in range(n)]
    edges = [0.0] + [g[1] for g in gaps] + [dur]
    starts = [0.0] + [g[2] for g in gaps]
    return [(starts[k], edges[k + 1]) for k in range(n)]


def timeline():
    tl, clock = [], 0.0
    for s in SEGMENTS:
        e = dict(s)
        if s["text"]:
            wav = f"{B}/{s['id']}.wav"
            if not os.path.exists(wav):
                subprocess.run(PIPER + ["--length-scale", "1.3", "--sentence-silence", "0.75", "-f", wav],
                               input=s["text"].encode(), check=True, stderr=subprocess.DEVNULL)
            x, sr = wav_read(wav)
            vd = len(x) / sr
            e["dur"] = LEAD + vd + TAIL
            sents = sentences(s["text"])
            e["subs"] = [(LEAD + a, LEAD + b, txt) for (a, b), txt in zip(sentence_times(wav, len(sents)), sents)]
            e["wav"] = wav
        else:
            e["subs"] = []
        e["start"] = clock
        clock += e["dur"]
        tl.append(e)
    return tl, clock


# ---------------- камера ----------------
def ease(u):
    return u * u * (3 - 2 * u)


def camera(mode, u, t, seed):
    z, cx, cy, sx, sy = 1.04, 0.5, 0.5, 0.0, 0.0
    e = ease(u)
    if mode == "push":
        z = 1.02 + 0.08 * u
    elif mode == "push_slow":
        z = 1.02 + 0.05 * u
    elif mode == "push_fast":
        z = 1.02 + 0.2 * e
    elif mode == "pull":
        z = 1.16 - 0.14 * e
    elif mode == "pan_right":
        z, cx = 1.14, 0.44 + 0.12 * e
    elif mode == "pan_left":
        z, cx = 1.14, 0.56 - 0.12 * e
    elif mode == "tilt_up":
        z, cy = 1.16, 0.6 - 0.18 * e
    elif mode == "tilt_down":
        z, cy = 1.16, 0.42 + 0.16 * e
    elif mode == "shake":
        z = 1.1 + 0.03 * u
        sx = (math.sin(t * 13.1 + seed) + math.sin(t * 7.3)) * 6
        sy = (math.sin(t * 11.7 + seed * 2) + math.sin(t * 5.1)) * 5
    elif mode == "still":
        z = 1.0 + 0.03 * u
    # лёгкое «дыхание» ручной камеры
    sx += math.sin(t * 0.7 + seed) * 2.5
    sy += math.sin(t * 0.53 + seed * 1.7) * 2.0
    return z, cx, cy, sx, sy


def frame_from(still, z, cx, cy, sx, sy):
    vw, vh = scenes.BW / z, scenes.BH / z
    left = min(max(cx * scenes.BW - vw / 2, 0), scenes.BW - vw) + sx
    top = min(max(cy * scenes.BH - vh / 2, 0), scenes.BH - vh) + sy
    k = vw / W
    return still.transform((W, H), Image.AFFINE, (k, 0, left, 0, k, top), resample=Image.BILINEAR)


# ---------------- снег ----------------
class Snow:
    def __init__(self, n, vx, vy, streak, seed):
        r = np.random.default_rng(seed)
        self.p = r.uniform(0, 1, (n, 2)) * [W + 400, H + 200]
        self.depth = r.uniform(0.3, 1.0, n)
        self.wob = r.uniform(0, 6.28, n)
        self.vx, self.vy, self.streak = vx, vy, streak

    def draw(self, d, t):
        for (x0, y0), dp, wb in zip(self.p, self.depth, self.wob):
            x = (x0 + self.vx * dp * t + math.sin(t * 1.3 + wb) * 20) % (W + 400) - 200
            y = (y0 + self.vy * dp * t) % (H + 200) - 100
            r = 1.0 + dp * 3.2
            c = int(150 + 105 * dp)
            col = (c, c, min(255, c + 12))
            if self.streak:
                d.line((x, y, x - self.vx * dp * 0.03, y - self.vy * dp * 0.03), fill=col, width=max(1, int(r * 0.8)))
            else:
                d.ellipse((x - r, y - r, x + r, y + r), fill=col)


# ---------------- субтитры ----------------
SUBF = ImageFont.truetype(scenes.F_BOLD, 46)


def sub_overlay(text):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if SUBF.getlength(cur + " " + w) > 1400 and cur:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    lh = 60
    im = Image.new("RGBA", (W, lh * len(lines) + 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, ln in enumerate(lines):
        x = (W - SUBF.getlength(ln)) / 2
        d.text((x, 10 + i * lh), ln, font=SUBF, fill=(255, 255, 255, 255), stroke_width=5, stroke_fill=(0, 0, 0, 235))
    return im


VIG = None
GRAIN = None


def post_init():
    global VIG, GRAIN
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    VIG = (1 - 0.42 * np.clip(r - 0.35, 0, 1) ** 1.6)[..., None].astype(np.float32)
    g = np.random.default_rng(1)
    GRAIN = [g.normal(0, 5, (H, W, 1)).astype(np.float32) for _ in range(6)]


def render_segment(args):
    idx, e, total = args
    out = f"{B}/v_{e['id']}.mp4"
    if os.path.exists(out) and not PREVIEW:
        return out
    post_init()
    p = dict(e["p"])
    sc = e["scene"]
    stills = {}

    def still(key, pp):
        if key not in stills:
            stills[key] = scenes.render_still(sc, pp, seed=idx * 7 + 3)
        return stills[key]

    n = int(round(e["dur"] * FPS))
    interior = sc in INTERIOR
    amb = e["amb"]
    snow = None
    if sc == "tear":
        snow = Snow(260, 700, 380, True, idx)
    elif not interior:
        nn, vx, vy, streak = SNOW[amb]
        snow = Snow(nn, vx, vy, streak, idx)
    subs = [(a, b, sub_overlay(t)) for a, b, t in e["subs"]]
    frames = range(0, n, 12) if PREVIEW else range(n)
    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", out]
    ff = None if PREVIEW else subprocess.Popen(cmd, stdin=subprocess.PIPE)
    grow = [1, 2, 7, 12]
    for i in frames:
        t = i / FPS
        u = i / max(1, n - 1)
        pp = p
        key = "base"
        if p.get("grow"):
            k = sum(1 for a, b, _ in e["subs"] if t >= a - 0.1)
            pp = dict(p, count=grow[max(0, min(3, k - 1))])
            key = pp["count"]
        if p.get("alarm"):
            on = int(t * 2.2) % 2 == 0 and t > 0.25
            pp = dict(p, alarm_on=on)
            key = on
        im = frame_from(still(key, pp), *camera(e["cam"], u, t, idx))
        if snow:
            snow.draw(ImageDraw.Draw(im), t + idx * 3)
        a = np.asarray(im, dtype=np.float32)
        flick = 1.0
        if sc in ("tent_int", "hands", "tear"):
            flick = 1 + 0.025 * math.sin(t * 9.1) * math.sin(t * 3.7 + idx)
        fade = 1.0
        if e["text"] is None:
            fade = min(1, t / 0.4, (e["dur"] - t) / 0.4)
        if idx == 0:
            fade = min(fade, t / 1.5)
        if idx == total - 1:
            fade = min(fade, (e["dur"] - t) / 2.5)
        a = a * VIG * (flick * max(0.0, fade)) + GRAIN[i % 6]
        im = Image.fromarray(a.clip(0, 255).astype(np.uint8))
        for s0, s1, ov in subs:
            if s0 <= t < s1 + 0.15:
                im.paste(ov, (0, H - 70 - ov.height), ov)
        if PREVIEW:
            im.resize((480, 270)).save(f"{B}/pv_{e['id']}_{i:05d}.png")
        else:
            ff.stdin.write(im.tobytes())
    if ff:
        ff.stdin.close()
        ff.wait()
    return out


# ---------------- звук ----------------
def special_voice(kind, path_cache={}):
    txt = {"radio": "Ilyas, this is base camp. Do you copy? Ilyas, come in.", "whisper": "Ilyas. Ilyas."}[kind]
    wav = f"{B}/sp_{kind}.wav"
    if not os.path.exists(wav):
        subprocess.run(PIPER + ["--length-scale", "1.0" if kind == "radio" else "1.5", "-f", wav],
                       input=txt.encode(), check=True, stderr=subprocess.DEVNULL)
    x, sr = wav_read(wav)
    x = np.interp(np.arange(0, len(x), sr / sound.SR), np.arange(len(x)), x)
    return x


def voice_fx(kind, rng):
    x = special_voice(kind)
    if kind == "radio":
        y = np.tanh(sound.bp(x, 500, 2800, 4) * 6) * 0.5
        y += sound.bp(rng.standard_normal(len(y)), 400, 4000) * 0.06
        sq = sound.fx("static")[: int(0.25 * sound.SR)]
        out = np.concatenate([sq[:, 0], y, sq[:, 0]])
        return sound.reverb(sound.st(out, -0.2), 1.0, 0.2) * 0.5
    y = sound.hp(x, 900) * 0.6
    return sound.reverb(sound.st(y, rng.choice([-0.8, 0.8])), 2.8, 0.7) * 0.6


def place(buf, x, at):
    s = int(at * sound.SR)
    if s < 0:
        x, s = x[-s:], 0
    e = min(len(buf), s + len(x))
    if e > s:
        buf[s:e] += x[: e - s]


def runs(tl, key):
    out = []
    for e in tl:
        if out and out[-1][0] == e[key]:
            out[-1][2] = e["start"] + e["dur"]
        else:
            out.append([e[key], e["start"], e["start"] + e["dur"]])
    return out


def fade_edges(x, f):
    n = min(int(f * sound.SR), len(x) // 2)
    w = np.sin(np.linspace(0, np.pi / 2, n))[:, None]
    x[:n] *= w
    x[-n:] *= w[::-1]
    return x


def build_audio(tl, total):
    N = int((total + 1) * sound.SR)
    voice, ambb, mus, sfx = (np.zeros((N, 2)) for _ in range(4))
    for k, (kind, a, b) in enumerate(runs(tl, "amb")):
        x = fade_edges(sound.amb(kind, b - a + 2, k), 1.0)
        place(ambb, x, a - 1)
    for k, (mood, a, b) in enumerate(runs(tl, "mood")):
        x = fade_edges(sound.pad(mood, b - a + 3, k), 1.5)
        place(mus, x, a - 1.5)
    for k, e in enumerate(tl):
        if e.get("wav"):
            x, sr = wav_read(e["wav"])
            x = np.interp(np.arange(0, len(x), sr / sound.SR), np.arange(len(x)), x)
            x = sound.hp(x, 90)
            v = sound.reverb(sound.st(x), 0.8, 0.1)
            place(voice, v / np.abs(v).max() * 0.85, e["start"] + LEAD)
        for name, at in e["sfx"]:
            tt = e["start"] + (at if at >= 0 else e["dur"] - TAIL + at if e.get("wav") else e["dur"] + at)
            place(sfx, sound.fx(name, k, voice_fx), tt)
    env = np.abs(voice).max(1)
    win = int(0.25 * sound.SR)
    c = np.concatenate([[0], np.cumsum(env)])
    env = (c[np.minimum(np.arange(len(env)) + win // 2, len(env))] - c[np.maximum(np.arange(len(env)) - win // 2, 0)]) / win
    duck = (1 - 0.55 * np.clip(env / 0.08, 0, 1))[:, None]
    mix = voice + (ambb * 0.9 + mus * 0.85) * duck + sfx
    fo = int(2.5 * sound.SR)
    end = int(total * sound.SR)
    mix[end - fo:end] *= np.linspace(1, 0, fo)[:, None]
    mix[end:] = 0
    mix = mix / np.abs(mix).max() * 0.9
    path = f"{B}/mix.wav"
    with wave.open(path, "w") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sound.SR)
        w.writeframes((mix[:end] * 32767).astype(np.int16).tobytes())
    return path


def srt(tl):
    def ts(x):
        h, m, s = int(x // 3600), int(x % 3600 // 60), x % 60
        return f"{h:02d}:{m:02d}:{int(s):02d},{int((s % 1) * 1000):03d}"
    out, k = [], 1
    for e in tl:
        for a, b, t in e["subs"]:
            out.append(f"{k}\n{ts(e['start'] + a)} --> {ts(e['start'] + b + 0.15)}\n{t}\n")
            k += 1
    open(f"{HERE}/everest.srt", "w").write("\n".join(out))


def main():
    tl, total = timeline()
    print(f"{len(tl)} частей, {total / 60:.2f} мин")
    srt(tl)
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    jobs = [(i, e, len(tl)) for i, e in enumerate(tl) if not only or e["id"] in only]
    with Pool(4) as pool:
        for v in pool.imap_unordered(render_segment, jobs):
            print("готово", os.path.basename(v), flush=True)
    if PREVIEW or only:
        return
    mix = build_audio(tl, total)
    lst = f"{B}/list.txt"
    open(lst, "w").write("".join(f"file 'v_{e['id']}.mp4'\n" for e in tl))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", f"{B}/video.mp4"], check=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"{B}/video.mp4", "-i", mix, "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest",
                    f"{HERE}/everest-44-days.mp4"], check=True)
    print("ГОТОВО", f"{HERE}/everest-44-days.mp4")


if __name__ == "__main__":
    main()
