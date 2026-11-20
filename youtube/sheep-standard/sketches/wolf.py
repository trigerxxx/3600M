"""Эскизы для The Sheep Standard: Волк в костюме и овцы (пушистая = богатая, остриженная = бедная).
Это ориентир для рисунков автора, не финальная графика."""
import math
import random

from PIL import Image, ImageDraw, ImageFont

INK = (17, 17, 17)
BG = (255, 255, 255)
F = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
GREY, GREY_D, GREY_L = (128, 132, 140), (92, 96, 104), (196, 199, 204)
SUIT, SHIRT, TIE = (34, 44, 74), (255, 255, 255), (214, 40, 40)
WOOL, FACE, SKIN = (255, 255, 255), (52, 46, 46), (246, 196, 186)
BOIL = 0   # анимация: меняется каждые несколько кадров → линии «дрожат», как у рисованного мультика


def wob(cx, cy, rx, ry, n=44, amp=0.035, seed=1, rot=0.0):
    r = random.Random(seed + BOIL * 97)
    ph = [r.uniform(0, 6.28) for _ in range(3)]
    pts = []
    for i in range(n):
        a = i / n * math.tau
        k = 1 + amp * (math.sin(3 * a + ph[0]) + 0.6 * math.sin(5 * a + ph[1]) + 0.4 * math.sin(9 * a + ph[2]))
        x, y = math.cos(a) * rx * k, math.sin(a) * ry * k
        pts.append((cx + x * math.cos(rot) - y * math.sin(rot), cy + x * math.sin(rot) + y * math.cos(rot)))
    return pts


def jag(pts, seed=1, amp=3):
    r = random.Random(seed + BOIL * 131)
    out = []
    for (a, b) in zip(pts, pts[1:] + pts[:1]):
        for i in range(4):
            t = i / 4
            out.append((a[0] + (b[0] - a[0]) * t + r.uniform(-amp, amp), a[1] + (b[1] - a[1]) * t + r.uniform(-amp, amp)))
    return out


def shape(d, pts, fill, w=9, seed=1):
    pts = jag(pts, seed) if len(pts) < 20 else pts
    d.polygon(pts, fill=fill)
    d.line(pts + [pts[0]], fill=INK, width=w, joint="curve")


def line(d, a, b, w=8, seed=1):
    r = random.Random(seed + BOIL * 173)
    pts = [(a[0] + (b[0] - a[0]) * i / 8 + (r.uniform(-2.5, 2.5) if 0 < i < 8 else 0),
            a[1] + (b[1] - a[1]) * i / 8 + (r.uniform(-2.5, 2.5) if 0 < i < 8 else 0)) for i in range(9)]
    d.line(pts, fill=INK, width=w, joint="curve")


# ---------------- овца ----------------
def sheep(d, cx, base, s=1.0, fleece=1.0, mood="calm", seed=3):
    """fleece: 1.0 — пушистая (богатая), 0.5 — подстрижена, 0 — острижена (бедная)."""
    bw, bh = 150 * s, 95 * s
    by = base - (95 + 75 * fleece) * s
    for lx in (-0.55, -0.2, 0.25, 0.6):
        line(d, (cx + lx * bw, by + 40 * s), (cx + lx * bw, base), max(5, int(11 * s)), seed=int(lx * 10) + seed)
    if fleece > 0.05:
        k = 0.55 + 0.45 * fleece
        r = random.Random(seed)
        n = int(9 + 9 * fleece)
        for i in range(n):
            a = i / n * math.tau
            px = cx + math.cos(a) * bw * 0.78 * k
            py = by + math.sin(a) * bh * 0.72 * k
            shape(d, wob(px, py, 46 * s * k, 40 * s * k, seed=seed + i), WOOL, max(5, int(8 * s)), seed=seed + i)
        shape(d, wob(cx, by, bw * 0.85 * k, bh * 0.8 * k, seed=seed + 40), WOOL, 0)
        d.polygon(wob(cx, by, bw * 0.84 * k, bh * 0.79 * k, seed=seed + 40), fill=WOOL)
    else:
        shape(d, wob(cx, by, bw * 0.6, bh * 0.55, seed=seed + 41), SKIN, max(5, int(8 * s)))
        shape(d, wob(cx - bw * 0.1, by - bh * 0.5, 22 * s, 16 * s, seed=seed + 42), WOOL, max(4, int(6 * s)))   # клочок
        for k in range(3):
            line(d, (cx - 40 * s + k * 30 * s, by - 10 * s), (cx - 30 * s + k * 30 * s, by + 10 * s), max(3, int(4 * s)), seed=k)
    # голова
    hx, hy = cx + bw * 0.78, by - bh * 0.35
    shape(d, wob(hx, hy, 40 * s, 52 * s, seed=seed + 50, rot=0.3), FACE, max(5, int(8 * s)))
    for ex in (-1, 1):
        shape(d, wob(hx + ex * 44 * s, hy - 30 * s, 22 * s, 10 * s, seed=seed + 51 + ex, rot=ex * 0.4), FACE, max(4, int(6 * s)))
    er = 9 * s
    for ex in (-1, 1):
        ey = hy - 12 * s
        d.ellipse((hx + ex * 16 * s - er, ey - er, hx + ex * 16 * s + er, ey + er), fill=WOOL)
        pr = 4 * s if mood != "shock" else 2.5 * s
        d.ellipse((hx + ex * 16 * s - pr, ey - pr, hx + ex * 16 * s + pr, ey + pr), fill=INK)
    if mood == "sad":
        d.arc((hx - 14 * s, hy + 22 * s, hx + 14 * s, hy + 42 * s), 200, 340, fill=WOOL, width=max(3, int(4 * s)))
    elif mood == "shock":
        d.ellipse((hx - 7 * s, hy + 18 * s, hx + 7 * s, hy + 34 * s), fill=WOOL)
    else:
        d.line((hx - 12 * s, hy + 28 * s, hx + 12 * s, hy + 28 * s), fill=WOOL, width=max(3, int(4 * s)))


# ---------------- волк ----------------
def wolf(d, cx, base, s=1.0, pose="stand", seed=7, talk=0.0, blink=False):
    """talk 0..1 — насколько открыта пасть (анимация речи); blink — глаз закрыт."""
    # ноги и ботинки
    for lx in (-1, 1):
        shape(d, [(cx + lx * 18 * s, base - 200 * s), (cx + lx * 60 * s, base - 200 * s), (cx + lx * 58 * s, base - 20 * s), (cx + lx * 20 * s, base - 20 * s)], SUIT, 8, seed=lx + 3)
        shape(d, wob(cx + lx * 48 * s, base - 12 * s, 40 * s, 16 * s, seed=seed + lx), INK, 4)
    # хвост
    shape(d, wob(cx - 95 * s, base - 230 * s, 70 * s, 26 * s, seed=seed + 4, rot=0.9), GREY, 8)
    # пиджак
    jt = base - 470 * s
    shape(d, [(cx - 95 * s, jt + 30 * s), (cx + 95 * s, jt + 30 * s), (cx + 105 * s, base - 190 * s), (cx - 105 * s, base - 190 * s)], SUIT, 9, seed=11)
    d.polygon([(cx - 40 * s, jt + 30 * s), (cx + 40 * s, jt + 30 * s), (cx, jt + 170 * s)], fill=SHIRT, outline=INK)
    shape(d, [(cx - 13 * s, jt + 40 * s), (cx + 13 * s, jt + 40 * s), (cx + 9 * s, jt + 150 * s), (cx, jt + 170 * s), (cx - 9 * s, jt + 150 * s)], TIE, 5, seed=12)
    for lx in (-1, 1):   # лацканы
        line(d, (cx + lx * 40 * s, jt + 30 * s), (cx + lx * 10 * s, jt + 175 * s), 6, seed=13 + lx)
    d.ellipse((cx - 6 * s, jt + 210 * s, cx + 6 * s, jt + 222 * s), fill=INK)
    # руки
    if pose == "stand":
        for lx in (-1, 1):
            shape(d, [(cx + lx * 92 * s, jt + 40 * s), (cx + lx * 128 * s, jt + 60 * s), (cx + lx * 120 * s, jt + 230 * s), (cx + lx * 92 * s, jt + 225 * s)], SUIT, 8, seed=20 + lx)
            shape(d, wob(cx + lx * 108 * s, jt + 245 * s, 22 * s, 20 * s, seed=22 + lx), GREY, 7)
    elif pose == "present":
        shape(d, [(cx - 92 * s, jt + 40 * s), (cx - 128 * s, jt + 60 * s), (cx - 120 * s, jt + 230 * s), (cx - 92 * s, jt + 225 * s)], SUIT, 8, seed=19)
        shape(d, wob(cx - 108 * s, jt + 245 * s, 22 * s, 20 * s, seed=23), GREY, 7)
        shape(d, [(cx + 90 * s, jt + 50 * s), (cx + 290 * s, jt + 100 * s), (cx + 285 * s, jt + 140 * s), (cx + 85 * s, jt + 110 * s)], SUIT, 8, seed=24)
        shape(d, wob(cx + 310 * s, jt + 118 * s, 30 * s, 18 * s, seed=25), GREY, 7)
    elif pose == "phone":                 # левая рука опущена; правая: плечо → локоть (предплечье и лапа с телефоном — после головы)
        shape(d, [(cx - 92 * s, jt + 40 * s), (cx - 128 * s, jt + 60 * s), (cx - 120 * s, jt + 230 * s), (cx - 92 * s, jt + 225 * s)], SUIT, 8, seed=19)
        shape(d, wob(cx - 108 * s, jt + 245 * s, 22 * s, 20 * s, seed=23), GREY, 7)
        shape(d, [(cx + 88 * s, jt + 35 * s), (cx + 128 * s, jt + 55 * s), (cx + 150 * s, jt + 185 * s), (cx + 110 * s, jt + 200 * s)], SUIT, 8, seed=20)
    elif pose == "shears":
        shape(d, [(cx - 92 * s, jt + 40 * s), (cx - 128 * s, jt + 60 * s), (cx - 120 * s, jt + 230 * s), (cx - 92 * s, jt + 225 * s)], SUIT, 8, seed=19)
        shape(d, wob(cx - 108 * s, jt + 245 * s, 22 * s, 20 * s, seed=23), GREY, 7)
        shape(d, [(cx + 90 * s, jt + 50 * s), (cx + 270 * s, jt + 40 * s), (cx + 275 * s, jt + 80 * s), (cx + 95 * s, jt + 105 * s)], SUIT, 8, seed=26)
        hx2, hy2 = cx + 290 * s, jt + 58 * s
        shape(d, wob(hx2, hy2, 22 * s, 20 * s, seed=27), GREY, 7)
        for k in (-1, 1):   # ножницы для стрижки
            shape(d, [(hx2 + 10 * s, hy2 - 10 * s), (hx2 + 120 * s, hy2 - 60 * s + k * 18 * s), (hx2 + 125 * s, hy2 - 50 * s + k * 18 * s), (hx2 + 16 * s, hy2 + 4 * s)], (200, 205, 212), 6, seed=28 + k)
    # голова (в профиль вправо)
    hx, hy = cx + 10 * s, jt - 70 * s
    for ex, rot in ((-1, -0.25), (1, 0.15)):
        ear = [(hx + ex * 50 * s - 30 * s, hy - 50 * s), (hx + ex * 50 * s - 5 * s, hy - 150 * s), (hx + ex * 50 * s + 30 * s, hy - 55 * s)]
        shape(d, ear, GREY_D, 8, seed=30 + ex)
    shape(d, wob(hx, hy, 95 * s, 88 * s, seed=seed + 30), GREY, 9)
    snout = [(hx + 40 * s, hy - 30 * s), (hx + 190 * s, hy + 10 * s), (hx + 195 * s, hy + 45 * s), (hx + 40 * s, hy + 60 * s)]
    shape(d, snout, GREY_L, 9, seed=33)
    shape(d, wob(hx + 192 * s, hy + 18 * s, 18 * s, 14 * s, seed=34), INK, 4)   # нос
    if talk > 0.05:   # открытая пасть: тёмный рот и опущенная нижняя челюсть
        o = talk
        d.polygon([(hx + 60 * s, hy + 44 * s), (hx + 185 * s, hy + 38 * s), (hx + 176 * s, hy + (40 + 42 * o) * s), (hx + 70 * s, hy + (52 + 26 * o) * s)],
                  fill=(90, 26, 32), outline=INK)
        jaw = [(hx + 42 * s, hy + (52 + 26 * o) * s), (hx + 176 * s, hy + (40 + 42 * o) * s), (hx + 170 * s, hy + (58 + 42 * o) * s), (hx + 42 * s, hy + (74 + 26 * o) * s)]
        shape(d, jaw, GREY_L, 8, seed=37)
    else:
        line(d, (hx + 90 * s, hy + 45 * s), (hx + 175 * s, hy + 40 * s), 6, seed=35)  # рот
    d.polygon([(hx + 150 * s, hy + 40 * s), (hx + 158 * s, hy + 56 * s), (hx + 165 * s, hy + 40 * s)], fill=WOOL, outline=INK)  # клык
    # глаз: полузакрытый, каменный
    ex_, ey_ = hx + 40 * s, hy - 25 * s
    if blink:
        d.line((ex_ - 16 * s, ey_ + 2 * s, ex_ + 16 * s, ey_ + 2 * s), fill=INK, width=max(4, int(5 * s)))
    else:
        d.ellipse((ex_ - 14 * s, ey_ - 12 * s, ex_ + 14 * s, ey_ + 12 * s), fill=(255, 214, 80), outline=INK, width=5)
        d.ellipse((ex_ - 4 * s, ey_ - 4 * s, ex_ + 4 * s, ey_ + 4 * s), fill=INK)
        d.line((ex_ - 18 * s, ey_ - 4 * s, ex_ + 18 * s, ey_ - 4 * s), fill=GREY_D, width=int(12 * s))  # веко — скучающий взгляд
    line(d, (ex_ - 20 * s, ey_ - 22 * s), (ex_ + 22 * s, ey_ - 18 * s), 6, seed=36)  # бровь
    if pose == "phone":                   # предплечье от локтя вверх к уху, лапа держит телефон
        ex2, ey2 = cx + 130 * s, jt + 190 * s          # локоть
        px, py = hx - 5 * s, hy + 45 * s               # лапа у щеки
        shape(d, [(ex2 - 22 * s, ey2 + 8 * s), (ex2 + 24 * s, ey2 - 6 * s), (px + 28 * s, py + 8 * s), (px - 18 * s, py + 22 * s)], SUIT, 8, seed=40)
        shape(d, [(px - 38 * s, py - 115 * s), (px + 8 * s, py - 122 * s), (px + 18 * s, py + 2 * s), (px - 28 * s, py + 8 * s)], (40, 44, 52), 6, seed=38)
        d.rectangle((px - 28 * s, py - 105 * s, px + 2 * s, py - 12 * s), fill=(90, 150, 210))   # экран
        shape(d, wob(px - 4 * s, py - 10 * s, 26 * s, 22 * s, seed=39), GREY, 7)               # лапа на телефоне


def wool_note(d, x, y, s=1.0):
    shape(d, [(x, y), (x + 220 * s, y), (x + 220 * s, y + 110 * s), (x, y + 110 * s)], (233, 211, 168), 7, seed=60)
    f = ImageFont.truetype(F, int(30 * s))
    d.text((x + 22 * s, y + 18 * s), "1 WOOL", font=f, fill=INK)
    d.ellipse((x + 150 * s, y + 55 * s, x + 200 * s, y + 100 * s), outline=(214, 40, 40), width=int(6 * s))


def label(d, x, y, t, size=34, fill=INK):
    f = ImageFont.truetype(F, size)
    d.text((x - f.getlength(t) / 2, y), t, font=f, fill=fill)


def sheet():
    W, H = 2000, 2500
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    label(d, W / 2, 40, "THE SHEEP STANDARD — THE WOLF & THE SHEEP", 54)
    label(d, W / 2, 110, "sketches for the author's own drawing · not final art", 30, (120, 120, 120))
    # волк: три позы
    label(d, W / 2, 180, "THE WOLF (in a suit, bored eyes, always honest)", 40)
    for i, (p, name) in enumerate([("stand", "STAND"), ("present", "PRESENT"), ("shears", "THE SHEARS (fees)")]):
        cx = 300 + i * 620
        wolf(d, cx, 1000, 0.95, p)
        if p == "present":
            wool_note(d, cx + 200, 610, 0.9)
        label(d, cx + 60, 1040, name, 36)
    line(d, (80, 1120), (1920, 1120), 4, seed=1)
    # шерсть = богатство
    label(d, W / 2, 1150, "FLEECE = WEALTH", 48)
    for i, (fl, m, name) in enumerate([(1.0, "calm", "RICH"), (0.5, "sad", "AFTER INFLATION"), (0.0, "shock", "FLEECED")]):
        cx = 330 + i * 640
        sheep(d, cx, 1560, 1.15, fl, m, seed=5 + i)
        label(d, cx + 40, 1600, name, 38)
    line(d, (80, 1690), (1920, 1690), 4, seed=2)
    # сцена-пример
    label(d, W / 2, 1720, "EXAMPLE SCENE", 44)
    wolf(d, 620, 2420, 0.75, "shears")
    sheep(d, 1180, 2380, 1.1, 0.0, "shock", seed=9)
    for k in range(6):
        shape(d, wob(860 + k * 34, 2300 + (k % 2) * 30, 26, 22, seed=70 + k), WOOL, 6)
    im.save("wolf-sheet.png")

    t = Image.new("RGB", (1280, 720), BG)
    td = ImageDraw.Draw(t)
    sheep(td, 330, 640, 1.5, 0.0, "shock", seed=9)
    wolf(td, 980, 760, 0.95, "stand")
    f = ImageFont.truetype(F, 112)
    td.text((60, 50), "FLEECED", font=f, fill=INK)
    t.save("wolf-thumb-example.png")


if __name__ == "__main__":
    sheet()
