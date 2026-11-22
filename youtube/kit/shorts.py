"""Вертикальные Shorts из горизонтального ролика Волка: крупная картинка + крупные субтитры.

Почему так: в ленте Shorts зритель решает за долю секунды. Узкая полоса 16:9 посреди белого экрана
и отсутствие текста → 90% пролистывают. Здесь: центр кадра (квадрат) на всю ширину, заголовок-крючок
в безопасной зоне (не под кнопками YouTube), субтитры по 2–4 слова, крупно, по центру.

Безопасная зона 1080×1920: сверху до ~370 закрыто вкладками, снизу от ~1330 — подпись и ник,
справа x>930 ниже середины — кнопки лайка/комментариев.

Запуск: python3 shorts.py <видео.mp4> <субтитры.srt> <начало_с> <конец_с> "<строка 1>" "<строка 2>" <выход.mp4>
"""
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
HAND = os.path.join(HERE, "fonts", "architects-daughter-latin-400-normal.woff")
BLACK = "/usr/share/fonts/opentype/inter/Inter-Black.otf"


def ts(s):
    h, m, rest = s.split(":")
    sec, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000


def read_srt(path):
    out = []
    for blk in open(path, encoding="utf-8").read().strip().split("\n\n"):
        lines = blk.strip().split("\n")
        if len(lines) >= 3 and "-->" in lines[1]:
            a, b = [ts(x.strip()) for x in lines[1].split("-->")]
            out.append((a, b, " ".join(lines[2:])))
    return out


def chunks(a, b, text, maxw=3):
    """Фраза → куски по 2–3 слова; время делим по длине куска."""
    words = text.split()
    groups, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) >= maxw or re.search(r"[.,!?…:]$", w):
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    total = sum(len(" ".join(g)) for g in groups) or 1
    t, res = a, []
    for g in groups:
        d = (b - a) * len(" ".join(g)) / total
        res.append((t, t + d, " ".join(g)))
        t += d
    return res


def ass_time(t):
    t = max(0, t)
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def make(video, srt, start, end, l1, l2, out):
    subs = [c for a, b, tx in read_srt(srt) if b > start and a < end for c in chunks(a, b, tx)]
    ass = tempfile.NamedTemporaryFile("w", suffix=".ass", delete=False, encoding="utf-8")
    ass.write(f"""[Script Info]
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Outline, Shadow, Alignment, MarginV
Style: Cap, Inter Black, 96, &H00FFFFFF, &H00111111, &H00000000, -1, 6, 0, 5, 0

[Events]
Format: Layer, Start, End, Style, Text
""")
    for a, b, tx in subs:
        if b <= start or a >= end:
            continue
        tx = tx.upper().replace("{", "(").replace("}", ")")
        ass.write(f"Dialogue: 0,{ass_time(a - start)},{ass_time(min(b, end) - start)},Cap,{{\\pos(540,1215)}}{tx}\n")
    ass.close()
    esc = lambda s: s.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace("$", "\\$")
    vf = (f"[0:v]crop=1440:1080:240:0,scale=1080:810,pad=1080:1920:0:570:white,"
          f"drawtext=fontfile={HAND}:text='{esc(l1)}':fontsize=70:fontcolor=black:x=(w-text_w)/2:y=385,"
          f"drawtext=fontfile={HAND}:text='{esc(l2)}':fontsize=70:fontcolor=0xD62828:x=(w-text_w)/2:y=470,"
          f"subtitles={ass.name}:fontsdir=/usr/share/fonts/opentype/inter[v];[0:a]loudnorm=I=-14:TP=-1.5[a]")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(start), "-to", str(end), "-i", video, "-filter_complex", vf,
                    "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                    "-movflags", "+faststart", out], check=True)
    os.unlink(ass.name)


if __name__ == "__main__":
    v, s, a, b, l1, l2, o = sys.argv[1:8]
    make(v, s, float(a), float(b), l1, l2, o)
    print("ok", o)
