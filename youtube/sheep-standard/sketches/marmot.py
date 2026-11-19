"""Образцы сурка для The Sheep Standard: «кривой» стиль от руки, толстый контур, каменное лицо."""
import math
import random

from PIL import Image, ImageDraw, ImageFont

INK = (17, 17, 17)
BG = (255, 246, 227)
F = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
FB = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
R = random.Random(4)


def wob(cx, cy, rx, ry, n=48, amp=0.035, seed=None, squash=0.0, rot=0.0):
    r = random.Random(seed if seed is not None else R.random())
    ph = [r.uniform(0, 6.28) for _ in range(3)]
    pts = []
    for i in range(n):
        a = i / n * math.tau
        k = 1 + amp * (math.sin(3 * a + ph[0]) + 0.6 * math.sin(5 * a + ph[1]) + 0.4 * math.sin(9 * a + ph[2]))
        x, y = math.cos(a) * rx * k, math.sin(a) * ry * k
        if squash and y > 0:          # шире книзу (груша)
            x *= 1 + squash * (y / ry)
        xr = x * math.cos(rot) - y * math.sin(rot)
        yr = x * math.sin(rot) + y * math.cos(rot)
        pts.append((cx + xr, cy + yr))
    return pts


def shape(d, pts, fill, w=9):
    d.polygon(pts, fill=fill)
    d.line(pts + [pts[0]], fill=INK, width=w, joint="curve")


def wline(d, a, b, w=9, seed=None):
    r = random.Random(seed)
    pts = []
    for i in range(9):
        t = i / 8
        x = a[0] + (b[0] - a[0]) * t + (r.uniform(-3, 3) if 0 < i < 8 else 0)
        y = a[1] + (b[1] - a[1]) * t + (r.uniform(-3, 3) if 0 < i < 8 else 0)
        pts.append((x, y))
    d.line(pts, fill=INK, width=w, joint="curve")


def sheep(d, cx, cy, s=1.0):
    for k, (dx, dy) in enumerate([(-30, -10), (0, -22), (30, -10), (-20, 12), (20, 12), (0, 0)]):
        shape(d, wob(cx + dx * s, cy + dy * s, 30 * s, 24 * s, seed=50 + k), (255, 255, 255), max(4, int(6 * s)))
    shape(d, wob(cx + 48 * s, cy - 4 * s, 18 * s, 15 * s, seed=60), (60, 50, 50), max(4, int(6 * s)))
    d.ellipse((cx + 50 * s, cy - 10 * s, cx + 56 * s, cy - 4 * s), fill=(255, 255, 255))
    for lx in (-22, 18):
        wline(d, (cx + lx * s, cy + 26 * s), (cx + lx * s, cy + 50 * s), max(4, int(7 * s)), seed=lx)


def marmot(im, cx, base, s=1.0, pose="stand", variant="A", costume=None, seed=1):
    d = ImageDraw.Draw(im)
    fur = {"A": (138, 90, 51), "B": (150, 104, 60), "C": (120, 82, 50)}[variant]
    belly = {"A": (201, 150, 95), "B": (214, 168, 112), "C": (190, 140, 92)}[variant]
    tall = pose == "shock" or variant == "C"
    bw, bh = (150, 210) if not tall else (118, 260)
    if variant == "B":
        bw, bh = 175, 185
    by = base - bh * s
    hx, hy = cx, by - bh * 0.55 * s - (10 * s if tall else 0)
    hw, hh = (120 if variant != "B" else 130) * s, 95 * s
    if costume == "crown":
        cape = [(cx - bw * 0.55 * s, by - 20 * s), (cx + bw * 0.55 * s, by - 20 * s), (cx + bw * 1.25 * s, base), (cx - bw * 1.25 * s, base)]
        shape(d, cape, (200, 40, 50), 9)
        for k in range(7):
            x = cx - bw * 1.2 * s + k * bw * 0.4 * s
            d.ellipse((x - 9 * s, base - 22 * s, x + 9 * s, base - 4 * s), fill=(255, 255, 255), outline=INK, width=3)
    # хвост
    shape(d, wob(cx + bw * 0.85 * s, base - 40 * s, 40 * s, 22 * s, seed=seed + 9, rot=-0.6), fur)
    # ступни
    for fx in (-0.45, 0.45):
        shape(d, wob(cx + fx * bw * s, base - 6 * s, 48 * s, 22 * s, seed=seed + int(fx * 10)), fur)
    # тело
    body = wob(cx, by + 10 * s, bw * s, bh * s, seed=seed, squash=0.0 if tall else 0.22)
    shape(d, body, fur)
    shape(d, wob(cx, by + 40 * s, bw * 0.62 * s, bh * 0.72 * s, seed=seed + 3, squash=0.15), belly, 6)
    # уши
    for ex in (-1, 1):
        shape(d, wob(hx + ex * hw * 0.78, hy - hh * 0.62, 26 * s, 22 * s, seed=seed + 20 + ex), fur)
        d.ellipse((hx + ex * hw * 0.78 - 10 * s, hy - hh * 0.62 - 6 * s, hx + ex * hw * 0.78 + 10 * s, hy - hh * 0.62 + 10 * s), fill=(90, 56, 34))
    # голова
    shape(d, wob(hx, hy, hw, hh, seed=seed + 5), fur)
    shape(d, wob(hx, hy + hh * 0.35, hw * 0.62, hh * 0.5, seed=seed + 6), belly, 6)   # морда
    # лицо: каменное
    ey = hy - hh * 0.12
    er = 9 * s if pose != "shock" else 11 * s
    for ex in (-1, 1):
        d.ellipse((hx + ex * hw * 0.42 - er, ey - er, hx + ex * hw * 0.42 + er, ey + er), fill=INK)
        if pose == "shock":
            wline(d, (hx + ex * hw * 0.42 - 18 * s, ey - 34 * s), (hx + ex * hw * 0.42 + 18 * s, ey - 40 * s), int(7 * s), seed=seed + ex)
    shape(d, wob(hx, hy + hh * 0.18, 20 * s, 13 * s, seed=seed + 7), (60, 36, 28), 5)       # нос
    wline(d, (hx - 26 * s, hy + hh * 0.48), (hx + 26 * s, hy + hh * 0.48), int(8 * s), seed=seed + 8)  # рот-линия
    # зубы — фирменная деталь
    for tx in (-1, 1):
        x0 = hx + tx * 9 * s - 8 * s
        d.rectangle((x0, hy + hh * 0.52, x0 + 16 * s, hy + hh * 0.52 + 22 * s), fill=(255, 255, 255), outline=INK, width=max(3, int(4 * s)))
    # лапы
    if pose == "stand":
        for ax in (-1, 1):
            shape(d, wob(cx + ax * 40 * s, by + 30 * s, 26 * s, 40 * s, seed=seed + 30 + ax, rot=ax * 0.5), fur)
    elif pose == "present":
        shape(d, wob(cx - 50 * s, by + 40 * s, 26 * s, 40 * s, seed=seed + 31, rot=-0.4), fur)
        arm = [(cx + 40 * s, by + 10 * s), (cx + 210 * s, by + 30 * s)]
        d.line(arm, fill=INK, width=int(64 * s))
        d.line(arm, fill=fur, width=int(48 * s))
        shape(d, wob(cx + 225 * s, by + 34 * s, 40 * s, 20 * s, seed=seed + 33), fur)
        sheep(d, cx + 236 * s, by - 44 * s, 1.35 * s)
    elif pose == "shock":
        for ax in (-1, 1):
            shape(d, wob(cx + ax * (bw * 0.72) * s, by + 70 * s, 20 * s, 56 * s, seed=seed + 35 + ax), fur)
    # костюмы
    if costume == "crown":
        cw = hw * 1.15
        top = hy - hh - 40 * s
        pts = [(hx - cw / 2, hy - hh * 0.75), (hx - cw / 2, top + 10 * s), (hx - cw / 4, top + 40 * s), (hx, top - 6 * s),
               (hx + cw / 4, top + 40 * s), (hx + cw / 2, top + 10 * s), (hx + cw / 2, hy - hh * 0.75)]
        shape(d, pts, (242, 182, 48), 8)
        d.ellipse((hx - 9 * s, top + 30 * s, hx + 9 * s, top + 48 * s), fill=(232, 48, 42), outline=INK, width=4)

    elif costume == "suit":
        for sx in (-1, 1):
            jk = [(cx + sx * 20 * s, by + 10 * s), (cx + sx * bw * 1.02 * s, by + 20 * s), (cx + sx * bw * 1.08 * s, base - 40 * s), (cx + sx * 40 * s, base - 30 * s)]
            shape(d, jk, (30, 50, 110), 8)
        d.polygon([(cx - 60 * s, by + 10 * s), (cx, by + 120 * s), (cx + 60 * s, by + 10 * s)], fill=(255, 255, 255), outline=INK)
        d.polygon([(cx - 12 * s, by + 20 * s), (cx + 12 * s, by + 20 * s), (cx + 8 * s, by + 110 * s), (cx, by + 125 * s), (cx - 8 * s, by + 110 * s)], fill=(232, 48, 42), outline=INK)
        for gx in (-1, 1):
            d.ellipse((hx + gx * hw * 0.42 - 26 * s, ey - 22 * s, hx + gx * hw * 0.42 + 26 * s, ey + 22 * s), outline=INK, width=int(6 * s))
        wline(d, (hx - hw * 0.42 + 26 * s, ey), (hx + hw * 0.42 - 26 * s, ey), int(6 * s), seed=3)
    elif costume == "apron":
        ap = wob(cx, by + 110 * s, bw * 0.6 * s, bh * 0.55 * s, seed=seed + 40)
        shape(d, ap, (90, 160, 210), 7)
        wline(d, (cx - 50 * s, by + 10 * s), (cx + 50 * s, by + 10 * s), int(7 * s), seed=4)


def label(d, x, y, t, size=34, fill=INK):
    f = ImageFont.truetype(F, size)
    d.text((x - f.getlength(t) / 2, y), t, font=f, fill=fill)


def sheet():
    W, H = 2000, 2350
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    label(d, W / 2, 40, "THE SHEEP STANDARD — MARMOT SKETCHES", 56)
    label(d, W / 2, 112, "reference for the author's own drawing · not final art", 30, (120, 100, 80))
    # ряд 1: три варианта формы
    for i, (v, name) in enumerate([("A", "A · CLASSIC PEAR"), ("B", "B · ROUND POTATO"), ("C", "C · TALL & SKINNY")]):
        cx = 360 + i * 640
        marmot(im, cx, 760, 1.0, "stand", v, seed=10 + i)
        label(d, cx, 800, name, 40)
    d = ImageDraw.Draw(im)
    wline(d, (80, 880), (1920, 880), 4, seed=1)
    # ряд 2: позы варианта A
    label(d, W / 2, 900, "POSES (variant A)", 44)
    for i, (p, name) in enumerate([("stand", "STAND"), ("present", "PRESENT (holds the money)"), ("shock", "SHOCK — STANDS UP STRAIGHT")]):
        cx = 330 + i * 660 - (60 if p == "present" else 0)
        marmot(im, cx, 1500, 0.95, p, "A", seed=20)
        label(d, 330 + i * 660, 1540, name, 34)
    d = ImageDraw.Draw(im)
    wline(d, (80, 1620), (1920, 1620), 4, seed=2)
    # ряд 3: костюмы
    label(d, W / 2, 1640, "SAME MARMOT, DIFFERENT COSTUMES", 44)
    for i, (c, name) in enumerate([("crown", "THE KING (government)"), ("suit", "THE BANKER"), ("apron", "THE SHOPKEEPER")]):
        cx = 360 + i * 640
        marmot(im, cx, 2230, 0.92, "stand", "A", costume=c, seed=30)
        label(d, cx, 2270, name, 34)
    im.save("marmot-sheet.png")

    # обложка-пример
    t = Image.new("RGB", (1280, 720), BG)
    td = ImageDraw.Draw(t)
    sheep(td, 330, 400, 3.2)
    marmot(t, 950, 820, 1.25, "stand", "A", seed=20)
    td = ImageDraw.Draw(t)
    f = ImageFont.truetype(F, 120)
    td.text((70, 60), "INFLATION", font=f, fill=INK)
    t.save("thumb-example.png")


if __name__ == "__main__":
    sheet()
