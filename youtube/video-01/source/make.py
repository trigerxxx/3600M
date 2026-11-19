"""Сборка ролика: озвучка → кадры анимаций → субтитры → музыка → MP4.
Запуск: tts/bin/python make.py  (нужны piper, ffmpeg, Pillow, numpy)
"""
import math
import os
import random
import subprocess
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from script import SEGMENTS, TITLE

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.path.dirname(HERE)
PIPER = os.path.join(SCRATCH, "tts", "bin", "piper")
VOICE = os.path.join(SCRATCH, "voices", "en_US-ryan-high.onnx")
OUT = os.path.join(HERE, "build")
os.makedirs(OUT, exist_ok=True)

W, H, FPS = 1280, 720, 24
BLACK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
BODY = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
BODY_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
C = dict(bg=(9, 26, 17), bg2=(18, 58, 37), gold=(255, 200, 106), orange=(255, 122, 26), green=(79, 208, 106),
         red=(232, 48, 42), ice=(185, 205, 190), white=(244, 241, 230), dark=(4, 14, 9))
_fonts = {}


def font(path, size):
    k = (path, size)
    if k not in _fonts:
        _fonts[k] = ImageFont.truetype(path, size)
    return _fonts[k]


def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


# ---------- фон: тёмные джунгли со светлячками ----------
random.seed(5)
FLIES = [(random.uniform(0, W), random.uniform(0, H), random.uniform(0.2, 1.0), random.uniform(0, 6.28)) for _ in range(40)]
BASE = Image.new("RGB", (W, H), C["bg"])
_d = ImageDraw.Draw(BASE)
for y in range(H):
    k = y / H
    _d.line([(0, y), (W, y)], fill=(int(9 + 10 * k), int(26 + 20 * k), int(17 + 10 * k)))
glow = Image.new("RGB", (W, H), (0, 0, 0))
ImageDraw.Draw(glow).ellipse((W * 0.2, H * 0.1, W * 0.8, H * 0.9), fill=(30, 70, 40))
BASE = Image.blend(BASE, glow.filter(ImageFilter.GaussianBlur(120)), 0.5)


def background(t):
    im = BASE.copy()
    d = ImageDraw.Draw(im)
    for x, y, s, ph in FLIES:
        yy = (y - t * 12 * s) % H
        xx = x + 8 * math.sin(t * s + ph)
        a = 0.5 + 0.5 * math.sin(t * 2 * s + ph)
        r = 1.5 + 2 * s
        col = (int(150 + 80 * a), int(200 + 50 * a), int(90 + 40 * a))
        d.ellipse((xx - r, yy - r, xx + r, yy + r), fill=col)
    return im


def text_center(d, text, f, y, fill, shadow=None):
    w = d.textlength(text, font=f)
    x = (W - w) / 2
    if shadow:
        d.text((x, y + max(3, f.size // 18)), text, font=f, fill=shadow)
    d.text((x, y), text, font=f, fill=fill)
    return w


def fmt(n):
    return f"{int(n):,}"


# ---------- визуальные типы ----------
def v_lines(d, t, dur, p):
    n = len(p["lines"])
    fs = 92 if n <= 2 else 80
    total = n * (fs + 18)
    y0 = H * 0.42 - total / 2
    for i, line in enumerate(p["lines"]):
        k = ease((t - i * 0.45) / 0.4)
        if k <= 0:
            continue
        col = C["gold"] if i == n - 1 else C["white"]
        y = y0 + i * (fs + 18) + (1 - k) * 30
        text_center(d, line, font(BLACK, fs), y, col, (60, 28, 0) if col == C["gold"] else C["dark"])


def v_counter(d, t, dur, p):
    k = ease(t / max(1.2, dur * 0.55))
    val = p["value"] * k
    text_center(d, fmt(val), font(BLACK, 120 if p["value"] < 1e10 else 96), H * 0.3, C["gold"], (60, 28, 0))
    text_center(d, p["label"].upper(), font(BLACK, 38), H * 0.3 + 150, C["green"], C["dark"])
    text_center(d, p["note"], font(BODY_R, 18), H * 0.3 + 205, C["ice"])


def v_title(d, t, dur, p):
    k = ease(t / 0.6)
    fs = 150
    text_center(d, p["big"], font(BLACK, fs), H * 0.3 + (1 - k) * 40, C["gold"], (60, 28, 0))
    if t > 0.4:
        text_center(d, p["small"].upper(), font(BLACK, 36), H * 0.3 + 175, C["green"], C["dark"])


def v_cards(d, t, dur, p):
    n = len(p["items"])
    cw, ch, gap = 330, 200, 36
    x0 = (W - (n * cw + (n - 1) * gap)) / 2
    for i, (a, b) in enumerate(p["items"]):
        k = ease((t - i * 0.5) / 0.4)
        if k <= 0:
            continue
        x = x0 + i * (cw + gap)
        y = H * 0.3 + (1 - k) * 30
        d.rounded_rectangle((x, y, x + cw, y + ch), radius=24, fill=C["bg2"], outline=(46, 90, 62), width=3)
        tw = d.textlength(a, font=font(BLACK, 46))
        d.text((x + (cw - tw) / 2, y + 48), a, font=font(BLACK, 46), fill=C["gold"])
        tw = d.textlength(b, font=font(BODY, 24))
        d.text((x + (cw - tw) / 2, y + 120), b, font=font(BODY, 24), fill=C["white"])


def v_timeline(d, t, dur, p):
    n = len(p["steps"])
    y = H * 0.45
    x0, x1 = 160, W - 160
    k = ease(t / max(1.0, dur * 0.6))
    d.line((x0, y, x0 + (x1 - x0) * k, y), fill=C["green"], width=8)
    for i, (a, b) in enumerate(p["steps"]):
        x = x0 + (x1 - x0) * i / (n - 1)
        if k * (n - 1) + 0.01 < i:
            continue
        d.ellipse((x - 18, y - 18, x + 18, y + 18), fill=C["orange"], outline=C["dark"], width=4)
        tw = d.textlength(a, font=font(BLACK, 34))
        d.text((x - tw / 2, y - 90), a, font=font(BLACK, 34), fill=C["gold"])
        tw = d.textlength(b, font=font(BODY, 24))
        d.text((x - tw / 2, y + 40), b, font=font(BODY, 24), fill=C["white"])


def v_bars(d, t, dur, p):
    text_center(d, p["title"], font(BLACK, 34), 120, C["white"])
    mx = max(v for _, v in p["bars"])
    k = ease(t / max(1.2, dur * 0.5))
    bw, gap = 250, 120
    n = len(p["bars"])
    x0 = (W - (n * bw + (n - 1) * gap)) / 2
    base = 560
    for i, (name, v) in enumerate(p["bars"]):
        h = 320 * (v / mx) * k
        x = x0 + i * (bw + gap)
        col = C["orange"] if i == 0 else (90, 130, 105)
        d.rounded_rectangle((x, base - h, x + bw, base), radius=16, fill=col)
        lab = f"{v * k:.0f}{p['unit']}"
        tw = d.textlength(lab, font=font(BLACK, 54))
        d.text((x + (bw - tw) / 2, base - h - 70), lab, font=font(BLACK, 54), fill=C["gold"] if i == 0 else C["white"])
        tw = d.textlength(name, font=font(BODY, 26))
        d.text((x + (bw - tw) / 2, base + 14), name, font=font(BODY, 26), fill=C["white"])
    text_center(d, p["note"], font(BODY_R, 18), base + 58, C["ice"])


def v_money(d, t, dur, p):
    k = ease(t / 0.8)
    text_center(d, p["value"], font(BLACK, int(140 + 20 * k)), H * 0.28, C["gold"], (60, 28, 0))
    text_center(d, "LIFETIME REVENUE", font(BLACK, 36), H * 0.28 + 190, C["green"], C["dark"])
    d.rounded_rectangle((W / 2 - 300, H * 0.28 + 250, W / 2 + 300, H * 0.28 + 300), radius=14, fill=(58, 7, 5), outline=C["red"], width=3)
    text_center(d, p["note"], font(BODY, 20), H * 0.28 + 262, C["white"])


def v_point(d, t, dur, p):
    k = ease(t / 0.5)
    cx, cy = 230, H * 0.42
    r = 90 * k
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=C["orange"], outline=C["dark"], width=6)
    if k > 0.5:
        num = str(p["n"])
        tw = d.textlength(num, font=font(BLACK, 110))
        d.text((cx - tw / 2, cy - 68), num, font=font(BLACK, 110), fill=C["dark"])
    k2 = ease((t - 0.25) / 0.5)
    if k2 > 0:
        d.text((370 + (1 - k2) * 40, cy - 70), p["head"], font=font(BLACK, 54), fill=C["white"])
        d.text((370 + (1 - k2) * 40, cy + 10), p["sub"], font=font(BODY, 30), fill=C["green"])


def v_quote(d, t, dur, p):
    k = ease(t / 0.6)
    d.text((140, 150), "“", font=font(BLACK, 200), fill=C["orange"])
    words = p["text"].split()
    lines, cur = [], ""
    f = font(BLACK, 52)
    for w_ in words:
        test = (cur + " " + w_).strip()
        if d.textlength(test, font=f) > 960:
            lines.append(cur)
            cur = w_
        else:
            cur = test
    lines.append(cur)
    for i, line in enumerate(lines):
        if k * len(lines) + 0.3 < i:
            continue
        d.text((180, 260 + i * 68), line, font=f, fill=C["white"])
    d.text((180, 270 + len(lines) * 68), "— " + p["who"], font=font(BODY_R, 22), fill=C["ice"])


VIS = dict(lines=v_lines, counter=v_counter, title=v_title, cards=v_cards, timeline=v_timeline,
           bars=v_bars, money=v_money, point=v_point, quote=v_quote)


def caption(d, words, t, dur):
    """Субтитры по 6 слов, текущий кусок внизу экрана."""
    chunks = [words[i:i + 6] for i in range(0, len(words), 6)]
    if not chunks:
        return
    i = min(len(chunks) - 1, int(t / dur * len(chunks)))
    text = " ".join(chunks[i])
    f = font(BODY, 30)
    tw = d.textlength(text, font=f)
    x, y = (W - tw) / 2, H - 92
    d.rounded_rectangle((x - 18, y - 10, x + tw + 18, y + 46), radius=12, fill=(0, 0, 0))
    d.text((x, y), text, font=f, fill=(255, 255, 255))


# ---------- озвучка ----------
def tts(seg):
    wav = os.path.join(OUT, seg["id"] + ".wav")
    if not os.path.exists(wav):
        subprocess.run([PIPER, "-m", VOICE, "--length-scale", "1.05", "--sentence-silence", "0.3", "-f", wav],
                       input=seg["text"].encode(), check=True, stderr=subprocess.DEVNULL)
    with wave.open(wav) as w_:
        return wav, w_.getnframes() / w_.getframerate()


def main():
    srt, clock = [], 0.0
    seg_videos, seg_audio = [], []
    for n, seg in enumerate(SEGMENTS):
        wav, dur = tts(seg)
        dur += 0.35
        frames = int(dur * FPS)
        fdir = os.path.join(OUT, "f_" + seg["id"])
        os.makedirs(fdir, exist_ok=True)
        words = seg["text"].split()
        for i in range(frames):
            t = i / FPS
            im = background(clock + t)
            d = ImageDraw.Draw(im)
            VIS[seg["visual"]["kind"]](d, t, dur, seg["visual"])
            caption(d, words, t, dur)
            im.save(os.path.join(fdir, f"{i:05d}.png"), compress_level=1)
        mp4 = os.path.join(OUT, seg["id"] + ".mp4")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(FPS), "-i", os.path.join(fdir, "%05d.png"),
                        "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", mp4], check=True)
        seg_videos.append(mp4)
        padded = os.path.join(OUT, seg["id"] + "_p.wav")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wav, "-af", f"aresample=48000,apad=whole_dur={dur}",
                        "-ac", "2", padded], check=True)
        seg_audio.append(padded)
        def ts(x):
            return f"{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int((x % 1) * 1000):03d}"
        srt.append(f"{n + 1}\n{ts(clock)} --> {ts(clock + dur - 0.35)}\n{seg['text']}\n")
        clock += dur
        print(seg["id"], round(dur, 1), flush=True)

    with open(os.path.join(OUT, "list.txt"), "w") as f:
        for v in seg_videos:
            f.write(f"file '{v}'\n")
    with open(os.path.join(OUT, "alist.txt"), "w") as f:
        for a in seg_audio:
            f.write(f"file '{a}'\n")
    with open(os.path.join(HERE, "video1.srt"), "w") as f:
        f.write("\n".join(srt))

    # музыка: тихий тёплый эмбиент
    sr, total = 48000, clock
    tt = np.arange(int(sr * total)) / sr
    chord = sum(np.sin(2 * np.pi * f0 * tt) * a for f0, a in [(110, 0.5), (164.8, 0.35), (220, 0.25), (277.2, 0.15)])
    chord *= 0.5 + 0.5 * np.sin(2 * np.pi * tt / 8)
    pulse = np.sin(2 * np.pi * 55 * tt) * (np.sin(2 * np.pi * tt * 1.0) > 0.95) * 0.6
    music = (chord + pulse) / 3
    music = music / np.abs(music).max() * 0.6
    st = np.stack([music, np.roll(music, 300)], 1)
    with wave.open(os.path.join(OUT, "music.wav"), "wb") as w_:
        w_.setnchannels(2); w_.setsampwidth(2); w_.setframerate(sr)
        w_.writeframes((st * 32767).astype(np.int16).tobytes())

    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(OUT, "list.txt"),
                    "-c", "copy", os.path.join(OUT, "video.mp4")], check=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(OUT, "alist.txt"),
                    os.path.join(OUT, "voice.wav")], check=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", os.path.join(OUT, "video.mp4"), "-i", os.path.join(OUT, "voice.wav"),
                    "-i", os.path.join(OUT, "music.wav"), "-filter_complex",
                    "[1]volume=1.6,asplit=2[v1][v2];[2]volume=0.12[m];[m][v1]sidechaincompress=threshold=0.05:ratio=4[md];[v2][md]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5",
                    "-map", "0:v", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
                    os.path.join(HERE, "video1-99nights.mp4")], check=True)
    print("TOTAL", round(clock, 1), "s")


if __name__ == "__main__":
    main()
