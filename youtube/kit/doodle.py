"""Doodle-explainer для канала Волка — по плагину автора doodle-explainer-edit (стиль Primate Economics).

Правила стиля: белый фон; камеры нет; только жёсткие склейки; склейка в паузе голоса (одна фраза = один план);
анимация только тремя приёмами — смена позы (пасть каждые 0.33 с), мгновенное появление на слове, накопление;
рукописные титулы со звёздочками; повторяющийся мем-панч (крупный Гэри); подписи строчными ровным гротеском;
звук — только голос. Единственный фейд — вход в финал.

Сценарий: stories/<эпизод>.py → seq([(фраза, кадр), ...]) — каждая фраза получает свой план.
Запуск: python3 doodle.py stories/<эпизод>.py [--check]
"""
import importlib.util
import os
import subprocess
import sys
import wave
from multiprocessing import Pool

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "sheep-standard", "sketches"))
import kit  # noqa: E402
import wolf as W  # noqa: E402

WID, HEI, FPS = 1920, 1080, 30
INK, RED, GOLD = (17, 17, 17), (214, 40, 40), (242, 182, 48)
HAND = os.path.join(HERE, "fonts", "architects-daughter-latin-400-normal.woff")
CAPF = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
GROUND = 1000
ENV = {}
_fc = {}


def F(path, size):
    if (path, size) not in _fc:
        _fc[(path, size)] = ImageFont.truetype(path, size)
    return _fc[(path, size)]


# ---------------- голос → пасть ----------------
def envelope(wav):
    with wave.open(wav) as w_:
        x = np.frombuffer(w_.readframes(w_.getnframes()), np.int16).astype(np.float32) / 32768
        sr = w_.getframerate()
    hop = sr // FPS
    n = len(x) // hop
    return np.array([np.sqrt((x[i * hop:(i + 1) * hop] ** 2).mean()) for i in range(n)])


def speaking(T):
    for b in kit.TL["blocks"]:
        if b["start"] <= T < b["start"] + b["dur"]:
            e = ENV.get(b["wav"])
            i = int((T - b["start"]) * FPS)
            if e is None or not (0 <= i < len(e)):
                return False
            win = e[max(0, i - 2):i + 3]
            return float(win.max()) > 0.03
    return False


def mouth(T):
    """Смена позы: пока голос звучит, пасть открыта/закрыта каждые 0.33 с."""
    return 0.85 if speaking(T) and int(T / 0.33) % 2 == 0 else 0.0


# ---------------- рисунки предметов ----------------
def sheep_head(cx, base, s, f):
    bw, bh = 150 * s, 95 * s
    by = base - (95 + 75 * f) * s
    return cx + bw * 0.78, by - bh * 0.35


def costume(d, cx, base, s, f, kind):
    hx, hy = sheep_head(cx, base, s, f)
    if kind == "crown":
        w = 70 * s
        top = hy - 120 * s
        W.shape(d, [(hx - w, hy - 45 * s), (hx - w, top + 15 * s), (hx - w / 2, top + 45 * s), (hx, top),
                    (hx + w / 2, top + 45 * s), (hx + w, top + 15 * s), (hx + w, hy - 45 * s)], GOLD, max(5, int(7 * s)), seed=70)
    elif kind == "hat":         # соломенная шляпа продавца
        d.ellipse((hx - 85 * s, hy - 62 * s, hx + 85 * s, hy - 30 * s), fill=(232, 196, 96), outline=INK, width=max(4, int(6 * s)))
        W.shape(d, W.wob(hx, hy - 62 * s, 48 * s, 30 * s, seed=71), (232, 196, 96), max(4, int(6 * s)))
    elif kind == "scarf":       # бабушка: платок и очки
        W.shape(d, W.wob(hx - 6 * s, hy - 30 * s, 58 * s, 40 * s, seed=72), (196, 70, 120), max(4, int(6 * s)))
        for ex in (-1, 1):
            d.ellipse((hx + ex * 16 * s - 15 * s, hy - 27 * s, hx + ex * 16 * s + 15 * s, hy + 3 * s), outline=INK, width=max(3, int(5 * s)))
    elif kind == "helmet":      # строитель
        W.shape(d, W.wob(hx, hy - 45 * s, 50 * s, 30 * s, seed=73), (250, 200, 30), max(4, int(6 * s)))
        d.line((hx - 62 * s, hy - 30 * s, hx + 62 * s, hy - 30 * s), fill=INK, width=max(4, int(7 * s)))
    elif kind == "shades":      # богатая овца
        for ex in (-1, 1):
            d.ellipse((hx + ex * 17 * s - 17 * s, hy - 26 * s, hx + ex * 17 * s + 17 * s, hy - 2 * s), fill=INK)
        d.line((hx - 2 * s, hy - 16 * s, hx + 2 * s, hy - 16 * s), fill=INK, width=max(3, int(4 * s)))


def note(d, x, y, s=1.0, text="1 WOOL"):
    W.shape(d, [(x, y), (x + 230 * s, y), (x + 230 * s, y + 115 * s), (x, y + 115 * s)], (233, 211, 168), max(4, int(7 * s)), seed=60)
    fs = int(38 * s)
    while F(HAND, fs).getlength(text) > 130 * s and fs > 10:   # длинная сумма — мельче, чтобы влезла
        fs -= 2
    d.text((x + 22 * s, y + 22 * s), text, font=F(HAND, fs), fill=INK)
    d.ellipse((x + 160 * s, y + 58 * s, x + 208 * s, y + 104 * s), outline=RED, width=max(3, int(6 * s)))


def grass(d, x, y, s=1.0, seed=0):
    for k in range(5):
        a = (k - 2) * 18 * s
        W.shape(d, [(x + a - 10 * s, y), (x + a * 1.6, y - (70 + 12 * (k % 2)) * s), (x + a + 10 * s, y)], (70, 170, 70), max(3, int(5 * s)), seed=seed + k)
    d.line((x - 30 * s, y - 8 * s, x + 30 * s, y - 8 * s), fill=(150, 100, 50), width=max(4, int(8 * s)))


def stall(d, x, price=None, sign="GRASS"):
    for px in (x - 230, x + 230):
        W.shape(d, [(px - 14, 300), (px + 14, 300), (px + 14, GROUND), (px - 14, GROUND)], (150, 100, 55), 7, seed=int(px))
    W.shape(d, [(x - 270, 220), (x + 270, 220), (x + 270, 360), (x - 270, 360)], (200, 150, 85), 8, seed=74)
    fs = 96
    while F(HAND, fs).getlength(sign) > 500 and fs > 30:   # длинная вывеска — мельче, чтобы влезла
        fs -= 4
    f = F(HAND, fs)
    d.text((x - f.getlength(sign) / 2, 290 - fs * 0.6), sign, font=f, fill=INK)
    W.shape(d, [(x - 260, 700), (x + 260, 700), (x + 260, 770), (x - 260, 770)], (180, 130, 70), 8, seed=75)
    for k in range(4):
        grass(d, x - 180 + k * 120, 700, 0.8, seed=k * 7)
    if price is not None:
        tag(d, x - 90, 420, str(price))


def tag(d, x, y, text, big=False):
    f = F(HAND, 170 if big else 130)
    w = f.getlength(text) + 70
    h = 200 if big else 160
    W.shape(d, [(x, y), (x + w, y), (x + w, y + h), (x, y + h)], (255, 255, 255), 8, seed=76)
    d.text((x + 35, y + 10), text, font=f, fill=RED)


def statue(d, x, headless=False):
    W.shape(d, [(x - 170, 820), (x + 170, 820), (x + 190, GROUND), (x - 190, GROUND)], (170, 170, 176), 8, seed=77)
    old = W.WOOL
    W.WOOL = GOLD
    W.sheep(d, x - 80, 830, 1.5, 1.0, "calm", seed=11)
    W.WOOL = old
    if headless:
        hx, hy = sheep_head(x - 80, 830, 1.5, 1.0)
        d.ellipse((hx - 80, hy - 100, hx + 90, hy + 90), fill=(255, 255, 255))
        d.line((hx - 70, hy, hx - 40, hy + 30), fill=INK, width=6)
    else:
        costume(d, x - 80, 830, 1.5, 1.0, "crown")


def barrow(d, x, n=6):
    for k in range(n):
        note(d, x - 180 + (k % 3) * 110, 560 - (k // 3) * 60, 0.8)
    W.shape(d, [(x - 250, 640), (x + 200, 640), (x + 140, 790), (x - 190, 790)], (110, 120, 130), 8, seed=78)
    d.ellipse((x - 40, 780, x + 60, 880), fill=(60, 60, 66), outline=INK, width=8)
    d.line((x + 200, 650, x + 360, 760), fill=INK, width=12)


def chest(d, x, n=4):
    for k in range(n):
        note(d, x - 150 + k * 40, 640 - k * 30, 0.7)
    W.shape(d, [(x - 170, 720), (x + 170, 720), (x + 170, 900), (x - 170, 900)], (140, 90, 50), 8, seed=79)


def stamp(d, x, y):
    W.shape(d, [(x - 40, y), (x + 40, y), (x + 40, y + 120), (x - 40, y + 120)], (90, 60, 40), 7, seed=80)
    W.shape(d, [(x - 90, y + 120), (x + 90, y + 120), (x + 90, y + 170), (x - 90, y + 170)], RED, 7, seed=81)


def ice(d, x, y):
    W.shape(d, [(x - 130, y - 120), (x + 130, y - 130), (x + 140, y + 110), (x - 120, y + 120)], (200, 230, 250), 8, seed=82)
    note(d, x - 100, y - 50, 0.85)
    for k in range(3):
        W.shape(d, W.wob(x - 80 + k * 80, y + 160 + k * 15, 18, 26, seed=83 + k), (200, 230, 250), 5)


def chart(d, stage="up", x0=360, y0=220, w=1200, h=640):
    """График акции: up — растёт, peak — на вершине, crash — обвал."""
    d.line((x0, y0, x0, y0 + h), fill=INK, width=8)
    d.line((x0, y0 + h, x0 + w, y0 + h), fill=INK, width=8)
    up = [(x0 + 40, y0 + h - 40), (x0 + 200, y0 + h - 70), (x0 + 330, y0 + h - 160), (x0 + 470, y0 + h - 240),
          (x0 + 600, y0 + h - 380), (x0 + 730, y0 + h - 470), (x0 + 850, y0 + 60)]
    pts = up[:4] if stage == "start" else up
    col = (40, 160, 70)
    if stage == "crash":
        pts = up + [(x0 + 930, y0 + 300), (x0 + 1010, y0 + h - 120), (x0 + 1120, y0 + h - 30)]
        d.line(up, fill=col, width=14, joint="curve")
        d.line(pts[len(up) - 1:], fill=RED, width=14, joint="curve")
    else:
        d.line(pts, fill=col, width=14, joint="curve")
    if stage in ("peak", "crash"):
        px, py = up[-1]
        d.ellipse((px - 18, py - 18, px + 18, py + 18), fill=INK)


def phone(d, x, y, s=1.0, title="", msgs=()):
    """Телефон с чатом: msgs — строки сообщений."""
    W.shape(d, [(x, y), (x + 360 * s, y), (x + 360 * s, y + 680 * s), (x, y + 680 * s)], (40, 44, 52), 8, seed=84)
    d.rectangle((x + 22 * s, y + 60 * s, x + 338 * s, y + 620 * s), fill=(245, 245, 248))
    if title:
        d.text((x + 40 * s, y + 70 * s), title, font=F(CAPF, int(30 * s)), fill=(90, 90, 96))
    for i, m in enumerate(msgs):
        yy = y + (130 + i * 115) * s
        W.shape(d, [(x + 40 * s, yy), (x + 320 * s, yy), (x + 320 * s, yy + 90 * s), (x + 40 * s, yy + 90 * s)], (210, 235, 255), 5, seed=85 + i)
        d.text((x + 58 * s, yy + 22 * s), m, font=F(HAND, int(34 * s)), fill=INK)


def gavel(d, x, y):
    W.shape(d, [(x - 40, y + 60), (x + 260, y - 120), (x + 285, y - 85), (x - 15, y + 95)], (140, 90, 50), 8, seed=86)
    W.shape(d, [(x + 200, y - 230), (x + 330, y - 150), (x + 280, y - 70), (x + 150, y - 150)], (110, 70, 40), 8, seed=87)
    W.shape(d, [(x - 150, y + 170), (x + 150, y + 170), (x + 150, y + 220), (x - 150, y + 220)], (110, 70, 40), 8, seed=88)


def coin(d, x, y, r=170, text="$GRASS"):
    d.ellipse((x - r, y - r, x + r, y + r), fill=GOLD, outline=INK, width=9)
    d.ellipse((x - r + 26, y - r + 26, x + r - 26, y + r - 26), outline=(200, 140, 30), width=6)
    f = F(HAND, int(r * 0.42))
    d.text((x - f.getlength(text) / 2, y - r * 0.28), text, font=f, fill=INK)


def boiler(d, T):
    """Комната волков с телефонами."""
    for k, x in enumerate((360, 960, 1560)):
        W.wolf(d, x, 1000, 0.82, "phone", talk=0.8 if int(T * 3 + k) % 2 == 0 else 0.0)
        W.shape(d, [(x - 230, 820), (x + 230, 820), (x + 230, 880), (x - 230, 880)], (150, 100, 55), 7, seed=89 + k)


def card(d, x, y, s=1.0, text="WOLF CARD", col=(242, 182, 48), cut=False):
    """Кредитка: x, y — центр. cut=True — разрезана пополам."""
    w, h = 430 * s, 270 * s
    halves = [(-w / 2, w / 2, 0)] if not cut else [(-w / 2, -8 * s, -30 * s), (8 * s, w / 2, 30 * s)]
    for a, b, dy in halves:
        W.shape(d, [(x + a, y - h / 2 + dy), (x + b, y - h / 2 + dy), (x + b, y + h / 2 + dy), (x + a, y + h / 2 + dy)], col, max(4, int(8 * s)), seed=91)
    W.shape(d, [(x - w / 2 + 40 * s, y - 50 * s), (x - w / 2 + 110 * s, y - 50 * s), (x - w / 2 + 110 * s, y + 5 * s), (x - w / 2 + 40 * s, y + 5 * s)], (220, 220, 225), max(3, int(5 * s)), seed=92)
    if cut:
        return
    fs = int(44 * s)
    while F(HAND, fs).getlength(text) > w - 60 * s and fs > 10:
        fs -= 2
    d.text((x - w / 2 + 40 * s, y + 40 * s), text, font=F(HAND, fs), fill=INK)
    d.text((x - w / 2 + 40 * s, y + 85 * s), "**** 4242", font=F(CAPF, int(26 * s)), fill=INK)


def bill(d, x, y, lines, s=1.0):
    """Выписка по карте: lines — [(текст, красный?)]."""
    W.shape(d, [(x, y), (x + 620 * s, y), (x + 620 * s, y + (150 + 105 * len(lines)) * s), (x, y + (150 + 105 * len(lines)) * s)], (255, 255, 255), max(4, int(8 * s)), seed=93)
    d.text((x + 40 * s, y + 35 * s), "STATEMENT", font=F(CAPF, int(40 * s)), fill=(120, 120, 126))
    for i, (t, red) in enumerate(lines):
        yy = y + (115 + i * 105) * s
        if red:
            W.shape(d, [(x + 25 * s, yy - 10 * s), (x + 595 * s, yy - 10 * s), (x + 595 * s, yy + 85 * s), (x + 25 * s, yy + 85 * s)], (255, 225, 225), 4, seed=94 + i)
        d.text((x + 45 * s, yy), t, font=F(HAND, int(58 * s)), fill=RED if red else INK)


def snowball(d, x, y, r=200, text="DEBT"):
    W.shape(d, W.wob(x, y, r, r * 0.95, seed=95), (240, 244, 250), max(5, int(r / 22)))
    ns = 0.45 * r / 300
    for k in range(max(2, int(r / 45))):
        a = 0.5 + k * 2.4
        if abs(np.sin(a)) < 0.45:     # не заходить на полосу текста
            a += 0.9
        note(d, x + np.cos(a) * r * 0.62 - 115 * ns, y + np.sin(a) * r * 0.62 - 58 * ns, ns)
    fs = int(r * 0.45)
    while F(HAND, fs).getlength(text) > r * 1.6 and fs > 10:
        fs -= 2
    f = F(HAND, fs)
    d.text((x - f.getlength(text) / 2, y - fs * 0.62), text, font=f, fill=RED)


def bag(d, x, y, s=1.0, text="SALE"):
    W.shape(d, [(x - 150 * s, y - 180 * s), (x + 150 * s, y - 180 * s), (x + 175 * s, y + 180 * s), (x - 175 * s, y + 180 * s)], (230, 90, 90), max(4, int(8 * s)), seed=96)
    d.arc((x - 80 * s, y - 280 * s, x + 80 * s, y - 100 * s), 180, 360, fill=INK, width=max(4, int(9 * s)))
    fs = int(90 * s)
    while F(HAND, fs).getlength(text) > 270 * s and fs > 10:
        fs -= 2
    f = F(HAND, fs)
    d.text((x - f.getlength(text) / 2, y - 60 * s), text, font=f, fill=(255, 255, 255))


def house(d, x, s=1.0, sign=None):
    W.shape(d, [(x - 260 * s, GROUND), (x - 260 * s, GROUND - 330 * s), (x + 260 * s, GROUND - 330 * s), (x + 260 * s, GROUND)], (235, 215, 180), max(4, int(8 * s)), seed=97)
    W.shape(d, [(x - 310 * s, GROUND - 320 * s), (x, GROUND - 560 * s), (x + 310 * s, GROUND - 320 * s)], RED, max(4, int(8 * s)), seed=98)
    W.shape(d, [(x - 50 * s, GROUND), (x - 50 * s, GROUND - 170 * s), (x + 50 * s, GROUND - 170 * s), (x + 50 * s, GROUND)], (140, 90, 50), max(3, int(6 * s)), seed=99)
    for wx in (-170, 110):
        W.shape(d, [(x + wx * s, GROUND - 260 * s), (x + (wx + 70) * s, GROUND - 260 * s), (x + (wx + 70) * s, GROUND - 190 * s), (x + wx * s, GROUND - 190 * s)], (190, 225, 250), max(3, int(6 * s)), seed=100)
    if sign:
        tag(d, x - 120 * s, GROUND - 720 * s, sign)


def car(d, x, s=1.0, rust=False):
    col = (150, 120, 100) if rust else (60, 120, 210)
    W.shape(d, [(x - 300 * s, GROUND - 60 * s), (x - 300 * s, GROUND - 170 * s), (x - 150 * s, GROUND - 180 * s), (x - 90 * s, GROUND - 290 * s),
                (x + 140 * s, GROUND - 290 * s), (x + 210 * s, GROUND - 180 * s), (x + 300 * s, GROUND - 160 * s), (x + 300 * s, GROUND - 60 * s)], col, max(4, int(8 * s)), seed=101)
    for wx in (-180, 180):
        d.ellipse((x + (wx - 60) * s, GROUND - 120 * s, x + (wx + 60) * s, GROUND), fill=(50, 50, 55), outline=INK, width=max(3, int(7 * s)))
    if rust:
        for k in range(5):
            d.ellipse((x + (-200 + k * 90) * s, GROUND - 150 * s, x + (-175 + k * 90) * s, GROUND - 125 * s), fill=(120, 70, 40))


def tree(d, x, n=6, s=1.0):
    """Шерстяное дерево: растёт само, n — сколько клочков шерсти (купюр) на ветках."""
    W.shape(d, [(x - 35 * s, GROUND), (x - 25 * s, GROUND - 330 * s), (x + 25 * s, GROUND - 330 * s), (x + 35 * s, GROUND)], (140, 90, 50), max(4, int(8 * s)), seed=102)
    W.shape(d, W.wob(x, GROUND - 470 * s, 260 * s, 200 * s, seed=103), (110, 185, 90), max(4, int(8 * s)))
    pts = [(-150, -520), (40, -600), (-40, -430), (130, -470), (-190, -420), (180, -560), (-90, -610), (60, -380), (-140, -330), (150, -380), (0, -520), (-220, -500)]
    for k in range(min(n, len(pts))):
        W.shape(d, W.wob(x + pts[k][0] * s, GROUND + pts[k][1] * s, 42 * s, 32 * s, seed=104 + k), (255, 255, 255), max(3, int(6 * s)))


def sparkle(d, x, y, r=22):
    d.polygon([(x, y - r), (x + r * 0.28, y - r * 0.28), (x + r, y), (x + r * 0.28, y + r * 0.28), (x, y + r),
               (x - r * 0.28, y + r * 0.28), (x - r, y), (x - r * 0.28, y - r * 0.28)], fill=(240, 200, 40))


# ---------------- элементы кадра ----------------
def draw_item(d, it, T):
    k = it["kind"]
    if k == "wolf":
        W.wolf(d, it.get("x", 960), it.get("base", GROUND + 30), it.get("s", 1.4), it.get("pose", "stand"), talk=mouth(T))
    elif k == "sheep":
        x, base, s, f = it.get("x", 960), it.get("base", GROUND), it.get("s", 1.3), it.get("f", 1.0)
        W.sheep(d, x, base, s, f, it.get("mood", "calm"), seed=it.get("seed", 5))
        if it.get("c"):
            costume(d, x, base, s, f, it["c"])
    elif k == "gary":
        W.sheep(d, it.get("x", 960), it.get("base", GROUND), it.get("s", 1.3), 0.0, it.get("mood", "shock"), seed=9)
    elif k == "note":
        note(d, it["x"], it["y"], it.get("s", 1.0), it.get("text", "1 WOOL"))
    elif k == "notes":   # накопление: n купюр (n растёт по словам)
        for j in range(it["_n"]):
            note(d, it["x"] + (j % it.get("cols", 4)) * 120, it["y"] - (j // it.get("cols", 4)) * 70, it.get("s", 0.8))
    elif k == "grass":
        for j in range(it.get("n", 6)):
            grass(d, it["x"] + (j % 4) * 110, it["y"] - (j // 4) * 60, it.get("s", 1.0), seed=j * 5)
    elif k == "stall":
        stall(d, it.get("x", 1300), it.get("price"), it.get("sign", "GRASS"))
    elif k == "tag":
        tag(d, it["x"], it["y"], it["text"], it.get("big", False))
    elif k == "statue":
        statue(d, it.get("x", 1350), it.get("headless", False))
    elif k == "barrow":
        barrow(d, it.get("x", 1250), it.get("n", 6))
    elif k == "chest":
        chest(d, it.get("x", 1300), it.get("n", 4))
    elif k == "stamp":
        stamp(d, it["x"], it["y"])
    elif k == "ice":
        ice(d, it.get("x", 1300), it.get("y", 560))
    elif k == "chart":
        chart(d, it.get("stage", "up"))
    elif k == "phone":
        phone(d, it.get("x", 780), it.get("y", 200), it.get("s", 1.0), it.get("title", ""), it.get("msgs", ()))
    elif k == "gavel":
        gavel(d, it.get("x", 900), it.get("y", 600))
    elif k == "coin":
        coin(d, it.get("x", 960), it.get("y", 520), it.get("r", 200), it.get("text", "$GRASS"))
    elif k == "boiler":
        boiler(d, T)
    elif k == "card":
        card(d, it.get("x", 960), it.get("y", 540), it.get("s", 1.6), it.get("text", "WOLF CARD"), it.get("col", GOLD), it.get("cut", False))
    elif k == "bill":
        bill(d, it.get("x", 650), it.get("y", 180), it["lines"], it.get("s", 1.0))
    elif k == "snowball":
        snowball(d, it.get("x", 960), it.get("y", 560), it.get("r", 200), it.get("text", "DEBT"))
    elif k == "bag":
        bag(d, it.get("x", 960), it.get("y", 620), it.get("s", 1.4), it.get("text", "SALE"))
    elif k == "house":
        house(d, it.get("x", 960), it.get("s", 1.0), it.get("sign"))
    elif k == "car":
        car(d, it.get("x", 960), it.get("s", 1.0), it.get("rust", False))
    elif k == "tree":
        tree(d, it.get("x", 960), it.get("_n", it.get("n", 6)) if "at" in it else it.get("n", 6), it.get("s", 1.0))
    elif k == "text":    # крупный рукописный текст (числа, суммы)
        f = F(HAND, it.get("size", 140))
        txt = it["text"]
        d.text((it.get("x", WID / 2) - f.getlength(txt) / 2, it.get("y", 380)), txt, font=f, fill=it.get("color", INK))


class shot(kit.Shot):
    """Один план. kind: scene / title / wolfface / sheepface / gary (мем) / outro."""
    sfx_in = None

    def __init__(self, *items, kind="scene", title=None, caption=None, cap=None, c=None, mood="calm"):
        self.items, self.kind, self.title, self.caption, self.cap, self.c, self.mood = [dict(i) for i in items], kind, title, caption, cap, c, mood

    def prepare(self, tl, block):
        self.block = block
        for it in self.items:
            if "in" in it:
                it["_in"] = block["start"] + kit.wtime(block, it["in"]) - 0.05
            if it["kind"] in ("notes", "tree"):
                it["_at"] = [block["start"] + kit.wtime(block, w) - 0.05 for w in it.get("at", [])]

    def state(self, T):
        vis = tuple(T >= it.get("_in", -1) for it in self.items)
        cnt = tuple(it.get("n0", 0) + sum(1 for t in it.get("_at", []) if T >= t) * it.get("step", 1) for it in self.items if it["kind"] in ("notes", "tree"))
        has_wolf = self.kind in ("wolfface", "outro") or any(it["kind"] == "wolf" for it in self.items)
        boil = int(T * 3) if any(it["kind"] == "boiler" for it in self.items) else 0
        return (vis, cnt, mouth(T) if has_wolf else 0, boil)

    def draw(self, im, lt, dur, T):
        d = ImageDraw.Draw(im)
        if self.kind == "title":
            lines = self.title.split("\n")
            f = F(HAND, 150)
            y0 = HEI / 2 - len(lines) * 95
            boxes = []
            for i, ln in enumerate(lines):
                x = (WID - f.getlength(ln)) / 2 + i * 60
                d.text((x, y0 + i * 185), ln, font=f, fill=(20, 20, 20))
                boxes.append((x, y0 + i * 185, x + f.getlength(ln)))
            x0, x1 = min(b[0] for b in boxes), max(b[2] for b in boxes)
            for (sx, sy, r) in [(x0 - 60, y0 + 20, 22), (x1 + 50, y0 + 60, 18), (x0 + 40, y0 + len(lines) * 185 + 10, 16), (x1 + 20, y0 + len(lines) * 185 - 10, 24)]:
                sparkle(d, sx, sy, r)
        elif self.kind == "wolfface":
            W.wolf(d, 818, 2830, 4.2, "stand", talk=mouth(T))
        elif self.kind == "sheepface":
            W.sheep(d, 375, 1290, 5.0, 1.0, self.mood, seed=5)
            if self.c:
                costume(d, 375, 1290, 5.0, 1.0, self.c)
        elif self.kind == "gary":     # мем-панч: Гэри крупно, в шоке
            W.sheep(d, 375, 1201, 5.0, 0.0, "shock", seed=9)
            for k, (x, y) in enumerate([(1550, 250), (1700, 420), (1450, 520)]):
                W.shape(d, W.wob(x, y, 50, 36, seed=90 + k), (255, 255, 255), 7)
        elif self.kind == "outro":
            sky = np.linspace([255, 196, 120], [255, 120, 140], HEI)[:, None, :].repeat(WID, 1).astype(np.uint8)
            im.paste(Image.fromarray(sky))
            d = ImageDraw.Draw(im)
            d.ellipse((1380, 380, 1620, 620), fill=(255, 240, 200))
            d.rectangle((0, 900, WID, HEI), fill=(90, 160, 80))
            W.wolf(d, 620, 960, 1.25, "stand", talk=mouth(T))
            W.sheep(d, 1180, 960, 1.4, 0.0, "shock", seed=9)
        for it in self.items:
            if T >= it.get("_in", -1):
                if it["kind"] in ("notes", "tree"):
                    it["_n"] = it.get("n0", 0) + sum(1 for t in it.get("_at", []) if T >= t) * it.get("step", 1)
                draw_item(d, it, T)
        if self.caption:
            f = F(CAPF, 64)
            x, y = self.cap or (WID * 0.3 - f.getlength(self.caption) / 2, 120)
            d.text((max(40, x), y), self.caption, font=f, fill=INK)


def seq(pairs, mood="hope", amb="silence", pause=0.35):
    """[(фраза, shot), ...] → блок озвучки, где каждая фраза начинается со своего плана (склейка в паузе)."""
    text = " ".join(p[0] for p in pairs)
    shots, idx = [], 0
    for pair in pairs:
        sent, main_shot, extra = pair[0], pair[1], pair[2:]
        toks = sent.replace("*", "").split()
        low = [t.strip(".,!?—…").lower() for t in toks]
        for sh in [main_shot] + [e[1] for e in extra]:
            for it in sh.items:      # «in»/«at» — слово внутри своей фразы
                if isinstance(it.get("in"), str):
                    it["in"] = idx + low.index(it["in"].lower())
                if "at" in it:
                    it["at"] = [idx + low.index(w.lower()) if isinstance(w, str) else w for w in it["at"]]
        shots.append((idx, main_shot))
        for word, sh in extra:       # склейка внутри длинной фразы — на ударном слове
            shots.append((idx + low.index(word.lower()), sh))
        idx += len(toks)
    return kit.block(text, shots, mood=mood, amb=amb, pause=pause)


# ---------------- рендер ----------------
_cache = {"key": None, "img": None}


def render_frame(T):
    cur = None
    for s in kit.TL["shots"]:
        if s[0] <= T:
            cur = s
    key = (id(cur[1]) if cur else None, cur[1].state(T) if cur else None)
    fade = 1.0
    if cur and cur[1].kind == "outro":
        fade = min(1.0, (T - cur[0]) / 1.2)
    fade = min(fade, (kit.TL["total"] - T) / 0.6)
    if key == _cache["key"] and fade >= 1:
        return _cache["img"]
    im = Image.new("RGB", (WID, HEI), (255, 255, 255))
    if cur:
        cur[1].draw(im, T - cur[0], cur[3] - cur[0], T)
    if fade < 1:
        im = Image.fromarray((np.asarray(im, dtype=np.float32) * max(0.0, fade)).astype(np.uint8))
    else:
        _cache.update(key=key, img=im)
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


def voice_track(tl, path):
    """Только голос (по плагину): блоки на свои места, без музыки и эффектов."""
    SR = 44100
    out = np.zeros(int((tl["total"] + 1) * SR), dtype=np.float32)
    for b in tl["blocks"]:
        with wave.open(b["wav"]) as w_:
            x = np.frombuffer(w_.readframes(w_.getnframes()), np.int16).astype(np.float32) / 32768
        s = int(b["start"] * SR)
        out[s:s + len(x)] += x[: len(out) - s]
    out = out[: int(tl["total"] * SR)]
    with wave.open(path, "w") as w_:
        w_.setnchannels(1)
        w_.setsampwidth(2)
        w_.setframerate(SR)
        w_.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())


def main():
    path = sys.argv[1]
    sys.modules["doodle"] = sys.modules[__name__]
    sys.modules["kit"] = kit
    spec = importlib.util.spec_from_file_location("story", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    name = mod.STORY["name"]
    bdir = os.environ.get("YTKIT_BUILD", os.path.expanduser(f"~/.cache/ytkit/{name}"))
    os.makedirs(bdir, exist_ok=True)
    tl = kit.build_timeline(mod, bdir)
    # склейка в паузе: план начинается чуть раньше своего слова (середина паузы)
    for k, s in enumerate(tl["shots"]):
        if k:
            s[0] = max(tl["shots"][k - 1][0] + 0.3, s[0] - 0.12)
    for k, s in enumerate(tl["shots"]):
        s[3] = tl["shots"][k + 1][0] if k + 1 < len(tl["shots"]) else tl["total"]
    tl["shakes"] = []
    kit.TL = tl
    for b in tl["blocks"]:
        ENV[b["wav"]] = envelope(b["wav"])
    durs = sorted(s[3] - s[0] for s in tl["shots"])
    print(f"{name}: {tl['total']/60:.2f} мин, планов {len(durs)}, медиана {durs[len(durs)//2]:.2f} с, макс {durs[-1]:.1f} с")
    if "--check" in sys.argv:
        ts = [s[0] + 0.5 * (s[3] - s[0]) for s in tl["shots"]]
        cols = 6
        rows = (len(ts) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * 320, rows * 180), (60, 60, 60))
        for i, t in enumerate(ts):
            sheet.paste(render_frame(t).resize((316, 176)), ((i % cols) * 320 + 2, (i // cols) * 180 + 2))
        out = os.path.join(bdir, "check.png")
        sheet.save(out)
        print("контрольный лист:", out)
        return
    n = int(tl["total"] * FPS)
    parts = 4
    jobs = [(k, n * k // parts, n * (k + 1) // parts, os.path.join(bdir, f"part{k}.mp4")) for k in range(parts)]
    with Pool(parts) as pool:
        files = pool.map(render_part, jobs)
    lst = os.path.join(bdir, "parts.txt")
    open(lst, "w").write("".join(f"file '{f}'\n" for f in files))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                    os.path.join(bdir, "video.mp4")], check=True)
    wav = os.path.join(bdir, "voice.wav")
    voice_track(tl, wav)
    out = os.path.join(bdir, f"{name}.mp4")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", os.path.join(bdir, "video.mp4"), "-i", wav, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-af", "loudnorm=I=-15:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-shortest", "-movflags", "+faststart", out], check=True)
    kit.write_srt(tl, os.path.join(bdir, f"{name}.srt"))
    print("ГОТОВО", out)


if __name__ == "__main__":
    main()
