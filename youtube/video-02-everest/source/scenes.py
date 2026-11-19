"""Сцены ролика: каждая функция рисует один большой кадр (2304x1296) в стиле low-poly.
Холодный синий снаружи, тёплый оранжевый внутри, красный только для опасности."""
import math
import random

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

BW, BH = 2304, 1296
F_BLACK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
F_BOLD = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
F_SEMI = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
_f = {}


def font(p, s):
    if (p, s) not in _f:
        _f[(p, s)] = ImageFont.truetype(p, s)
    return _f[(p, s)]


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def grad(top, bot, w=BW, h=BH, mid=None, midpos=0.5):
    y = np.linspace(0, 1, h)[:, None]
    top, bot = np.array(top, float), np.array(bot, float)
    if mid is None:
        col = top + (bot - top) * y[..., None]
    else:
        mid = np.array(mid, float)
        a = np.clip(y / midpos, 0, 1)[..., None]
        b = np.clip((y - midpos) / (1 - midpos), 0, 1)[..., None]
        col = np.where(y[..., None] < midpos, top + (mid - top) * a, mid + (bot - mid) * b)
    col = np.broadcast_to(col, (h, w, 3))
    return Image.fromarray(col.astype(np.uint8), "RGB")


def glow(im, x, y, r, color, strength=1.0):
    """Мягкое свечение (добавляется к картинке)."""
    layer = Image.new("RGB", im.size)
    d = ImageDraw.Draw(layer)
    d.ellipse((x - r, y - r, x + r, y + r), fill=tuple(int(c * strength) for c in color))
    layer = layer.filter(ImageFilter.GaussianBlur(r * 0.6))
    return ImageChops.add(im, layer)


def add_glow_layer(im, draw_fn, blur, strength=1.0):
    layer = Image.new("RGB", im.size)
    draw_fn(ImageDraw.Draw(layer))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    if strength != 1.0:
        layer = Image.fromarray((np.asarray(layer, float) * strength).clip(0, 255).astype(np.uint8))
    return ImageChops.add(im, layer)


def stars(d, rng, n=500, ymax=0.6, bright=255):
    for _ in range(n):
        x, y = rng.random() * BW, (rng.random() ** 1.6) * BH * ymax
        r = rng.choice([1, 1, 1, 2, 2, 3])
        b = int(bright * rng.uniform(0.35, 1))
        d.ellipse((x - r / 2, y - r / 2, x + r / 2, y + r / 2), fill=(b, b, min(255, b + 20)))


def peak(d, x, top, base, hw, lit, shade, snow=0.38, slit=(240, 246, 255), sshade=(150, 170, 205), skew=0.12, rng=None):
    """Одна low-poly вершина: освещённая левая грань, тёмная правая, снежная шапка."""
    rng = rng or random
    mx = x + hw * skew
    d.polygon([(x, top), (x - hw, base), (mx, base)], fill=lit)
    d.polygon([(x, top), (mx, base), (x + hw, base)], fill=shade)
    if snow > 0:
        sy = top + (base - top) * snow
        k = (sy - top) / (base - top)
        lx, rx, cx = x - hw * k, x + hw * k, x + (mx - x) * k
        zz_l = [(lx + (cx - lx) * i / 4, sy + (rng.uniform(-1, 1) * 22 if 0 < i < 4 else 0)) for i in range(5)]
        zz_r = [(cx + (rx - cx) * i / 4, sy + (rng.uniform(-1, 1) * 22 if 0 < i < 4 else 0)) for i in range(5)]
        d.polygon([(x, top)] + zz_l, fill=slit)
        d.polygon([(x, top)] + zz_r, fill=sshade)


def mrange(d, rng, base, n, hmin, hmax, lit, shade, slit, sshade, snow=0.4, x0=-200, x1=BW + 200, wmul=1.0):
    pts = sorted([rng.uniform(x0, x1) for _ in range(n)])
    order = list(range(n))
    rng.shuffle(order)
    for i in order:
        h = rng.uniform(hmin, hmax)
        peak(d, pts[i], base - h, base + 4, h * rng.uniform(0.9, 1.5) * wmul, lit, shade, snow, slit, sshade,
             skew=rng.uniform(-0.25, 0.3), rng=rng)


def fog(im, y, h, color, alpha=0.6, blur=60):
    layer = Image.new("L", im.size, 0)
    ImageDraw.Draw(layer).rectangle((0, y, BW, y + h), fill=int(255 * alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    return Image.composite(Image.new("RGB", im.size, color), im, layer)


def clouds(im, rng, y, n, color, alpha=0.7, rmin=80, rmax=220, blur=40, spread=None):
    layer = Image.new("L", im.size, 0)
    d = ImageDraw.Draw(layer)
    x0, x1 = spread or (-100, BW + 100)
    for _ in range(n):
        x, r = rng.uniform(x0, x1), rng.uniform(rmin, rmax)
        yy = y + rng.uniform(-r * 0.3, r * 0.3)
        d.ellipse((x - r * 1.6, yy - r * 0.6, x + r * 1.6, yy + r * 0.6), fill=int(255 * alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    return Image.composite(Image.new("RGB", im.size, color), im, layer)


def person(d, x, y, s, col, sitting=True):
    """Силуэт сидящего, сгорбленного человека в пуховке (s = масштаб)."""
    d.ellipse((x - 26 * s, y - 120 * s, x + 26 * s, y - 68 * s), fill=col)      # капюшон
    d.polygon([(x - 50 * s, y), (x - 44 * s, y - 70 * s), (x - 10 * s, y - 92 * s), (x + 34 * s, y - 80 * s),
               (x + 58 * s, y - 30 * s), (x + 62 * s, y)], fill=col)
    if not sitting:
        d.rectangle((x - 30 * s, y, x - 8 * s, y + 70 * s), fill=col)
        d.rectangle((x + 10 * s, y, x + 32 * s, y + 70 * s), fill=col)


def tent(d, x, y, s, front=(255, 122, 26), side=(190, 70, 20), door=(70, 22, 8), glowing=False):
    d.polygon([(x - 150 * s, y), (x - 20 * s, y - 150 * s), (x + 110 * s, y)], fill=front)
    d.polygon([(x - 20 * s, y - 150 * s), (x + 230 * s, y - 120 * s), (x + 290 * s, y - 6 * s), (x + 110 * s, y)], fill=side)
    d.polygon([(x - 60 * s, y), (x - 20 * s, y - 92 * s), (x + 30 * s, y)], fill=(255, 196, 110) if glowing else door)
    # оттяжки
    d.line((x - 20 * s, y - 150 * s, x - 230 * s, y + 10 * s), fill=(40, 40, 50), width=max(1, int(3 * s)))
    d.line((x + 230 * s, y - 120 * s, x + 380 * s, y + 4 * s), fill=(40, 40, 50), width=max(1, int(3 * s)))


def text_c(d, cx, y, txt, f, fill, spacing=0, stroke=0, stroke_fill=None):
    if spacing:
        w = sum(f.getlength(ch) for ch in txt) + spacing * (len(txt) - 1)
        x = cx - w / 2
        for ch in txt:
            d.text((x, y), ch, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
            x += f.getlength(ch) + spacing
    else:
        w = f.getlength(txt)
        d.text((cx - w / 2, y), txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)


# ===================== сцены =====================

def sc_storm(rng, p):
    im = grad((26, 36, 58), (70, 86, 110), mid=(48, 62, 86), midpos=0.55)
    d = ImageDraw.Draw(im)
    mrange(d, rng, 980, 7, 380, 620, (92, 106, 130), (60, 72, 96), (150, 162, 182), (104, 118, 142), snow=0.5)
    im = fog(im, 520, 380, (78, 94, 118), 0.65, 90)
    d = ImageDraw.Draw(im)
    # гребень на переднем плане
    d.polygon([(-50, 1300), (-50, 900), (500, 760), (1150, 840), (1700, 700), (2400, 860), (2400, 1300)], fill=(36, 46, 66))
    d.polygon([(-50, 900), (500, 760), (1150, 840), (1150, 870), (500, 800), (-50, 940)], fill=(180, 192, 210))
    d.polygon([(1150, 840), (1700, 700), (2400, 860), (2400, 900), (1700, 740), (1150, 870)], fill=(120, 134, 158))
    if p.get("climber"):
        person(d, 1240, 840, 0.55, (14, 18, 28), sitting=False)
        im = glow(im, 1252, 785, 26, (255, 230, 170), 1.0)
        d = ImageDraw.Draw(im)
        d.line((1240, 830, 1700, 712), fill=(255, 90, 40), width=3)   # верёвка уходит в белое
    im = clouds(im, rng, 300, 14, (120, 134, 156), 0.55, 120, 300, 70)
    im = fog(im, 0, 1296, (140, 152, 172), 0.18, 10)
    return im


def sc_summit_clear(rng, p):
    im = grad((12, 46, 120), (110, 170, 230), mid=(40, 100, 190), midpos=0.6)
    im = glow(im, 420, 260, 160, (255, 250, 220), 0.9)
    d = ImageDraw.Draw(im)
    mrange(d, rng, 1120, 9, 200, 380, (150, 180, 220), (96, 124, 170), (236, 244, 255), (170, 192, 226), snow=0.45)
    peak(d, 1080, 210, 1120, 760, (230, 238, 250), (120, 146, 190), snow=0.55, slit=(255, 255, 255), sshade=(176, 196, 230), skew=0.1, rng=rng)
    d.rectangle((0, 1110, BW, BH), fill=(200, 214, 236))
    im = clouds(im, rng, 1150, 22, (236, 242, 252), 0.9, 120, 260, 40)
    # стена облаков справа
    im = clouds(im, rng, 600, 18, (96, 104, 124), 0.9, 160, 340, 50, spread=(1700, 2700))
    im = clouds(im, rng, 360, 10, (120, 128, 146), 0.8, 140, 280, 60, spread=(1900, 2700))
    d = ImageDraw.Draw(im)
    person(d, 980, 470, 0.32, (10, 16, 34), sitting=False)
    d.line((990, 460, 1240, 560), fill=(255, 90, 40), width=2)
    return im


def sc_news(rng, p):
    im = grad((18, 22, 32), (8, 10, 16))
    d = ImageDraw.Draw(im)
    # лист бумаги чуть повёрнут
    paper = Image.new("RGB", (1500, 980), (236, 230, 216))
    pd = ImageDraw.Draw(paper)
    pd.rectangle((0, 0, 1500, 980), outline=(200, 192, 176), width=6)
    pd.rectangle((70, 70, 330, 128), fill=(232, 48, 42))
    pd.text((92, 76), "BREAKING", font=font(F_BLACK, 44), fill=(255, 255, 255))
    pd.text((70, 170), "CLIMBER MISSING", font=font(F_BLACK, 132), fill=(22, 22, 26))
    pd.text((70, 310), "IN THE DEATH ZONE", font=font(F_BLACK, 132), fill=(22, 22, 26))
    pd.text((72, 480), "Search called off after two weeks. \"Nobody survives up there.\"", font=font(F_SEMI, 44), fill=(70, 66, 60))
    r = random.Random(3)
    for i in range(7):
        y = 600 + i * 46
        pd.rectangle((72, y, 72 + r.randint(900, 1340), y + 16), fill=(188, 182, 168))
    paper = paper.filter(ImageFilter.GaussianBlur(0.6)).rotate(-3, expand=True, fillcolor=(0, 0, 0))
    mask = Image.new("L", (1500, 980), 255).rotate(-3, expand=True, fillcolor=0)
    shadow = Image.new("L", im.size, 0)
    shadow.paste(mask, (430, 190))
    shadow = shadow.filter(ImageFilter.GaussianBlur(40))
    im = Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, shadow)
    im.paste(paper, (400, 160), mask)
    im = glow(im, 1150, 600, 700, (60, 40, 20), 0.5)
    return im


def sc_tent_ledge(rng, p):
    night = p.get("night", True)
    im = grad((6, 10, 26), (34, 52, 92), mid=(14, 24, 52), midpos=0.55)
    d = ImageDraw.Draw(im)
    stars(d, rng, 600)
    mrange(d, rng, 900, 8, 260, 480, (60, 80, 124), (34, 46, 80), (150, 170, 210), (80, 98, 140), snow=0.45)
    im = fog(im, 760, 200, (30, 44, 80), 0.5, 60)
    d = ImageDraw.Draw(im)
    # скала-уступ
    d.polygon([(-50, 1300), (-50, 980), (300, 900), (900, 950), (1500, 920), (1900, 980), (2400, 1050), (2400, 1300)], fill=(20, 26, 40))
    d.polygon([(300, 900), (900, 950), (1500, 920), (1500, 950), (900, 980), (300, 930)], fill=(170, 186, 214))
    d.polygon([(900, 980), (1500, 950), (1900, 1010), (1400, 1300), (800, 1300)], fill=(28, 34, 52))
    tent(d, 1050, 945, 1.4, glowing=True)
    im = glow(im, 1030, 880, 260, (255, 140, 40), 0.55)
    im = clouds(im, rng, 1180, 8, (40, 52, 80), 0.6, 120, 240, 50)
    return im


def sc_tracker(rng, p):
    alarm = p.get("alarm_on", False)
    im = grad((10, 14, 24), (2, 4, 8))
    im = glow(im, 1150, 640, 600, (40, 60, 90), 0.5)
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = 640, 230, 1660, 1120
    d.rounded_rectangle((x0 + 20, y0 + 30, x1 + 20, y1 + 30), 90, fill=(0, 0, 0))
    d.rounded_rectangle((x0, y0, x1, y1), 90, fill=(52, 56, 64))
    d.rounded_rectangle((x0 + 12, y0 + 12, x1 - 12, y1 - 12), 80, fill=(38, 42, 50))
    d.rectangle((x1 - 220, y0 - 170, x1 - 160, y0 + 20), fill=(44, 48, 56))       # антенна
    d.rounded_rectangle((x1 - 230, y0 - 200, x1 - 150, y0 - 150), 20, fill=(232, 48, 42) if alarm else (60, 64, 72))
    scr = (x0 + 110, y0 + 120, x1 - 110, y0 + 640)
    bg = (120, 20, 16) if alarm else (34, 64, 46)
    fg = (255, 220, 210) if alarm else (170, 255, 190)
    d.rounded_rectangle(scr, 30, fill=bg)
    day = p.get("day", "44")
    if "?" in day:
        day = "--"
    text_c(d, (scr[0] + scr[2]) / 2, scr[1] + 40, p.get("label", "DAY"), font(F_BOLD, 54), fg, spacing=10)
    text_c(d, (scr[0] + scr[2]) / 2, scr[1] + 120, day, font(F_BLACK, 300), fg)
    for i, lab in enumerate(["SOS", "OK", "GPS"]):
        cx = x0 + 250 + i * 260
        d.ellipse((cx - 70, y1 - 270, cx + 70, y1 - 130), fill=(28, 30, 36))
        text_c(d, cx, y1 - 228, lab, font(F_BOLD, 40), (130, 136, 146))
    im = glow(im, (scr[0] + scr[2]) // 2, (scr[1] + scr[3]) // 2, 420, (232, 48, 42) if alarm else (60, 200, 110), 0.35)
    # иней по краям
    d = ImageDraw.Draw(im)
    for _ in range(450):
        a = rng.random() * math.tau
        rr = rng.uniform(0.9, 1.05)
        x = 1150 + math.cos(a) * 560 * rr
        y = 675 + math.sin(a) * 500 * rr
        r = rng.choice([2, 3, 4, 6])
        c = rng.randint(170, 240)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(c, c + 8 if c < 247 else c, 255))
    return im


def flask_img(rng, count, dark=False):
    im = grad((40, 30, 26), (14, 10, 10)) if not dark else grad((10, 14, 24), (2, 3, 6))
    im = glow(im, 1150, 640, 700, (255, 140, 60) if not dark else (60, 90, 140), 0.35)
    d = ImageDraw.Draw(im)
    # фляга
    x0, y0, x1, y1 = 760, 260, 1540, 1180
    d.rounded_rectangle((x0 + 30, y0 + 40, x1 + 30, y1 + 40), 140, fill=(0, 0, 0))
    body = (78, 132, 170) if not dark else (40, 70, 100)
    d.rounded_rectangle((x0, y0, x1, y1), 140, fill=body)
    d.rounded_rectangle((x0 + 40, y0 + 40, x0 + 170, y1 - 60), 60, fill=mix(body, (255, 255, 255), 0.25))
    d.rounded_rectangle((1060, 130, 1240, 280), 30, fill=(30, 34, 40))
    # зарубки группами по пять
    sc = (236, 244, 250) if not dark else (190, 210, 230)
    gx, gy, col = x0 + 230, y0 + 120, 0
    for i in range(count):
        g, k = divmod(i, 5)
        row, cg = divmod(g, 3)
        bx = gx + cg * 170
        by = gy + row * 150
        if k < 4:
            xx = bx + k * 30 + rng.uniform(-3, 3)
            d.line((xx, by, xx + rng.uniform(-6, 6), by + 110), fill=sc, width=9)
        else:
            d.line((bx - 18, by + 90, bx + 110, by + 18), fill=sc, width=9)
    return im


def sc_flask(rng, p):
    return flask_img(rng, p.get("count", 1), p.get("dark", False))


def sc_deathzone(rng, p):
    im = grad((8, 12, 30), (40, 62, 110), mid=(18, 30, 66), midpos=0.5)
    d = ImageDraw.Draw(im)
    stars(d, rng, 450, 0.4)
    mrange(d, rng, 1300, 6, 300, 520, (54, 74, 120), (30, 42, 76), (130, 150, 196), (70, 88, 130), snow=0.4)
    peak(d, 1152, 120, 1300, 900, (110, 136, 186), (52, 70, 116), snow=0.48, slit=(230, 238, 255), sshade=(130, 150, 196), skew=0.1, rng=rng)
    y = 560
    for x in range(0, BW, 60):
        d.line((x, y, x + 34, y), fill=(232, 48, 42), width=6)
    d.text((90, y - 104), "DEATH ZONE", font=font(F_BLACK, 84), fill=(255, 70, 60))
    d.text((90, y + 22), "8,000 m", font=font(F_BOLD, 56), fill=(255, 190, 180))
    d.text((1700, y + 22), "-40 °C", font=font(F_BOLD, 56), fill=(200, 220, 255))
    tent(d, 1250, 470, 0.32, glowing=True)
    im = glow(im, 1250, 440, 60, (255, 140, 40), 0.8)
    im = add_glow_layer(im, lambda g: g.line((0, y, BW, y), fill=(232, 48, 42), width=10), 18, 0.8)
    return im


def sc_basecamp(rng, p):
    im = grad((40, 34, 80), (232, 120, 70), mid=(150, 70, 100), midpos=0.55)
    d = ImageDraw.Draw(im)
    peak(d, 1300, 80, 900, 1100, (170, 110, 140), (80, 50, 90), snow=0.45, slit=(255, 210, 190), sshade=(150, 120, 170), rng=rng)
    mrange(d, rng, 950, 7, 180, 320, (90, 60, 96), (56, 38, 70), (200, 160, 180), (110, 90, 130), snow=0.3)
    d.rectangle((0, 940, BW, BH), fill=(36, 30, 52))
    d.polygon([(0, 940), (BW, 900), (BW, 960), (0, 990)], fill=(120, 110, 150))
    # палатки лагеря
    cols = [(255, 184, 77), (255, 122, 26), (232, 200, 60), (255, 150, 60)]
    for i in range(16):
        x = rng.uniform(150, 2150)
        y = rng.uniform(1010, 1220)
        s = 0.28 + (y - 1000) / 900
        tent(d, x, y, s, front=rng.choice(cols), side=(150, 70, 30), glowing=rng.random() < 0.5)
    # флажки
    flag = [(30, 90, 200), (240, 240, 240), (220, 40, 40), (40, 160, 70), (250, 200, 40)]
    for line in range(2):
        x0, y0, x1, y1 = 100 + line * 900, 860 + line * 40, 1100 + line * 1000, 980 + line * 30
        for k in range(24):
            t = k / 24
            x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t + math.sin(t * math.pi) * 60
            d.polygon([(x, y), (x + 34, y + 2), (x + 16, y + 40)], fill=flag[k % 5])
        d.line((x0, y0, x1, y1), fill=(30, 26, 40), width=2)
    # радист
    person(d, 1700, 1150, 0.9, (16, 12, 26))
    d.line((1716, 1050, 1760, 960), fill=(16, 12, 26), width=8)
    im = glow(im, 1760, 960, 40, (255, 80, 60), 0.9)
    return im


def sc_radio(rng, p):
    im = grad((14, 20, 34), (4, 6, 12))
    im = glow(im, 1150, 650, 500, (50, 70, 110), 0.6)
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = 860, 300, 1440, 1150
    d.rounded_rectangle((x0 + 26, y0 + 36, x1 + 26, y1 + 36), 60, fill=(0, 0, 0))
    d.rounded_rectangle((x0, y0, x1, y1), 60, fill=(36, 38, 44))
    d.rounded_rectangle((x0 + 150, y0 - 340, x0 + 220, y0 + 10), 30, fill=(28, 30, 34))
    d.rounded_rectangle((x0 + 70, y0 + 80, x1 - 70, y0 + 330), 24, fill=(20, 26, 22))
    text_c(d, (x0 + x1) / 2, y0 + 160, "NO BATTERY", font(F_BOLD, 48), (60, 80, 66))
    for r_ in range(6):
        for c_ in range(6):
            cx, cy = x0 + 120 + c_ * 68, y0 + 440 + r_ * 66
            d.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), fill=(22, 24, 28))
    d.rounded_rectangle((x0 - 30, y0 + 360, x0 + 10, y0 + 560), 14, fill=(232, 48, 42))
    for _ in range(1600):
        x, y = rng.uniform(x0 - 40, x1 + 40), rng.uniform(y0 - 40, y1 + 40)
        if (x0 + 40 < x < x1 - 40 and y0 + 40 < y < y1 - 40) or rng.random() < 0.6:
            continue
        r = rng.choice([2, 3, 4])
        c = rng.randint(180, 240)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(c, c + 10 if c < 245 else c, 255))
    return im


def sc_tent_int(rng, p):
    dim, warm, shadow = p.get("dim"), p.get("warm"), p.get("shadow")
    wall_l = (210, 92, 26) if not dim else (110, 46, 20)
    wall_r = (150, 58, 18) if not dim else (74, 30, 14)
    if warm:
        wall_l, wall_r = (236, 120, 40), (176, 74, 24)
    im = Image.new("RGB", (BW, BH), (20, 10, 6))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 1152, BH), fill=mix(wall_l, (0, 0, 0), 0.15))
    d.rectangle((1152, 0, BW, BH), fill=mix(wall_r, (0, 0, 0), 0.15))
    d.polygon([(-100, BH), (1152, -60), (1152, BH)], fill=wall_l)
    d.polygon([(1152, -60), (BW + 100, BH), (1152, BH)], fill=wall_r)
    d.polygon([(-100, 1080), (BW + 100, 1080), (BW + 100, BH), (-100, BH)], fill=(60, 40, 40) if not dim else (34, 24, 26))
    d.line((1152, -60, 1152, BH), fill=mix(wall_r, (0, 0, 0), 0.4), width=10)
    # швы ткани
    for k in range(1, 6):
        t = k / 6
        d.line((1152 - 1252 * t, -60 + (BH + 60) * t, 1152 + 1252 * t, -60 + (BH + 60) * t), fill=mix(wall_l, (0, 0, 0), 0.25), width=4)
    if shadow:
        sh = Image.new("L", im.size, 0)
        sd = ImageDraw.Draw(sh)
        sd.ellipse((560, 330, 700, 470), fill=200)
        sd.polygon([(500, 1080), (520, 560), (630, 450), (740, 560), (760, 1080)], fill=200)
        sh = sh.filter(ImageFilter.GaussianBlur(28))
        im = Image.composite(Image.new("RGB", im.size, (40, 14, 8)), im, sh)
        d = ImageDraw.Draw(im)
    # иней
    for _ in range(500):
        x, y = rng.uniform(0, BW), rng.uniform(0, 1080) * rng.random()
        r = rng.choice([1, 2, 2, 3])
        c = rng.randint(200, 250)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(c, c, 255))
    # спальник и Ильяс
    d.rounded_rectangle((1260, 860, 2000, 1200), 160, fill=(30, 64, 110) if not dim else (18, 36, 64))
    person(d, 1500, 1000, 2.2, (24, 14, 14))
    # вещи на полу
    d.rounded_rectangle((420, 980, 560, 1120), 20, fill=(70, 80, 90))          # горелка
    d.rectangle((440, 960, 540, 985), fill=(40, 44, 50))
    d.rounded_rectangle((640, 900, 760, 1150), 50, fill=(78, 132, 170))         # фляга
    d.polygon([(820, 1130), (1060, 1080), (1070, 1100), (830, 1150)], fill=(200, 210, 220))  # нож
    d.rounded_rectangle((180, 1000, 360, 1160), 30, fill=(160, 140, 90))        # еда
    # налобный фонарь
    lamp = (255, 214, 150) if not dim else (200, 160, 110)
    im = add_glow_layer(im, lambda g: g.polygon([(1490, 790), (900, 1150), (1300, 1250)], fill=(110, 80, 40)), 60, 0.9 if not dim else 0.5)
    im = glow(im, 1490, 790, 30, lamp, 1.0)
    if warm:
        im = glow(im, 490, 950, 140, (255, 150, 60), 0.6)
    return im


def sc_tear(rng, p):
    im = sc_tent_int(rng, dict(dim=True))
    d = ImageDraw.Draw(im)
    pts_top, pts_bot = [], []
    for i in range(9):
        t = i / 8
        x = 360 + 560 * t
        y = 260 + 520 * t
        w = math.sin(t * math.pi) * 110
        pts_top.append((x + rng.uniform(-14, 14) - w * 0.5, y + rng.uniform(-14, 14) - w))
        pts_bot.append((x + rng.uniform(-14, 14) + w * 0.5, y + rng.uniform(-14, 14) + w))
    poly = pts_top + pts_bot[::-1]
    d.polygon(poly, fill=(14, 22, 44))
    d.line(pts_top + [pts_bot[-1]] + pts_bot[::-1], fill=(80, 30, 10), width=6)
    for _ in range(140):
        t = rng.random()
        x, y = 360 + 560 * t, 260 + 520 * t
        r = rng.choice([3, 4, 6])
        d.ellipse((x - r, y - r, x + r, y + r), fill=(230, 240, 255))
    red = Image.new("RGB", im.size, (120, 10, 10))
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rectangle((0, 0, BW, BH), outline=255, width=260)
    m = m.filter(ImageFilter.GaussianBlur(160)).point(lambda v: int(v * 0.5))
    return Image.composite(red, im, m)


def sc_hands(rng, p):
    warm = p.get("warm")
    base = (150, 60, 20) if warm else (90, 36, 14)
    im = Image.new("RGB", (BW, BH), base)
    d = ImageDraw.Draw(im)
    for y in range(0, BH, 18):
        d.line((0, y, BW, y + 40), fill=mix(base, (0, 0, 0), 0.12), width=6)
    # шов поперёк ткани
    pts = [(300 + i * 120, 640 + math.sin(i * 0.9) * 40) for i in range(16)]
    d.line(pts, fill=(30, 10, 4), width=18)
    for i, (x, y) in enumerate(pts[:10]):
        d.line((x - 30, y - 50, x + 30, y + 50), fill=(232, 230, 220), width=8)
    # рукавицы
    for (cx, cy, ang) in [(1180, 760, -20), (1620, 700, 25)]:
        mit = Image.new("RGBA", (520, 420), (0, 0, 0, 0))
        md = ImageDraw.Draw(mit)
        md.rounded_rectangle((40, 80, 480, 360), 140, fill=(26, 40, 70, 255))
        md.ellipse((20, 40, 200, 220), fill=(26, 40, 70, 255))
        md.rounded_rectangle((330, 120, 520, 330), 40, fill=(18, 26, 46, 255))
        for _ in range(14):
            x, y = rng.uniform(60, 460), rng.uniform(90, 350)
            md.ellipse((x - 3, y - 3, x + 3, y + 3), fill=(220, 230, 255, 255))
        mit = mit.rotate(ang, expand=True, resample=Image.BICUBIC)
        im.paste(mit, (int(cx - mit.width / 2), int(cy - mit.height / 2)), mit)
    d = ImageDraw.Draw(im)
    d.line((1290, 650, 1430, 560), fill=(230, 232, 240), width=6)       # игла
    d.line((1430, 560, 1620, 420, 1900, 380), fill=(240, 236, 220), width=3)
    lamp = (255, 200, 120) if warm else (180, 200, 255)
    im = glow(im, 1400, 640, 520, lamp, 0.35)
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).ellipse((500, 100, 2300, 1300), fill=255)
    m = ImageChops.invert(m.filter(ImageFilter.GaussianBlur(220)))
    return Image.composite(Image.new("RGB", im.size, (6, 4, 4)), im, m)


def dawn_img(rng, wall=0.0):
    im = grad((40, 18, 70), (255, 140, 60), mid=(196, 60, 80), midpos=0.5)
    im = glow(im, 1500, 700, 320, (255, 230, 160), 1.0)
    im = glow(im, 1500, 700, 90, (255, 255, 230), 1.0)
    if wall:
        im = clouds(im, rng, 640, 26, (70, 64, 84), 0.95 * wall, 160, 320, 40, spread=(-200, 900))
        im = clouds(im, rng, 460, 14, (90, 80, 100), 0.85 * wall, 120, 260, 50, spread=(-200, 700))
    d = ImageDraw.Draw(im)
    mrange(d, rng, 860, 12, 140, 300, (190, 90, 110), (110, 50, 90), (255, 190, 170), (170, 110, 150), snow=0.4)
    im = clouds(im, rng, 900, 30, (255, 180, 170), 0.8, 120, 240, 40)
    d = ImageDraw.Draw(im)
    mrange(d, rng, 1060, 7, 220, 380, (230, 100, 90), (90, 40, 80), (255, 210, 190), (160, 110, 160), snow=0.45)
    im = clouds(im, rng, 1110, 20, (240, 170, 180), 0.7, 120, 260, 50)
    d = ImageDraw.Draw(im)
    d.polygon([(1500, BH), (1800, 1050), (2050, 1080), (2400, 1000), (2400, BH)], fill=(40, 18, 30))
    d.polygon([(1800, 1050), (2050, 1080), (2400, 1000), (2400, 1020), (2050, 1100), (1800, 1070)], fill=(255, 190, 170))
    tent(d, 2080, 1080, 0.5)
    person(d, 1900, 1080, 0.55, (20, 8, 16))
    return im


def sc_dawn(rng, p):
    return dawn_img(rng)


def sc_storm_coming(rng, p):
    return dawn_img(rng, wall=p.get("wall", 0.7))


def sc_tent_door(rng, p):
    inner = dawn_img(random.Random(7))
    im = Image.new("RGB", (BW, BH), (70, 26, 8))
    d = ImageDraw.Draw(im)
    d.polygon([(0, 0), (BW, 0), (BW, BH), (0, BH)], fill=(110, 40, 12))
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).polygon([(1152, 120), (520, BH), (1784, BH)], fill=255)
    im = Image.composite(inner, im, m)
    d = ImageDraw.Draw(im)
    for side in (-1, 1):
        x0, x1 = 1152, 1152 + side * 632
        for k in range(60):
            t = k / 60
            x = x0 + (x1 - x0) * t
            y = 120 + (BH - 120) * t
            d.rectangle((x - 8, y - 4, x + 8, y + 4), fill=(200, 200, 210))
    im = add_glow_layer(im, lambda g: g.polygon([(1152, 120), (520, BH), (1784, BH)], fill=(140, 60, 30)), 80, 0.6)
    return im


def sc_night_ext(rng, p):
    im = grad((4, 8, 24), (30, 50, 96), mid=(10, 20, 50), midpos=0.6)
    d = ImageDraw.Draw(im)
    stars(d, rng, 1100, 0.75)
    im = glow(im, 1800, 240, 70, (230, 236, 255), 1.0)
    im = glow(im, 1800, 240, 260, (90, 110, 170), 0.6)
    d = ImageDraw.Draw(im)
    mrange(d, rng, 1000, 9, 300, 560, (80, 100, 150), (36, 50, 90), (190, 206, 240), (96, 112, 160), snow=0.45)
    im = fog(im, 860, 200, (30, 44, 84), 0.5, 60)
    d = ImageDraw.Draw(im)
    d.polygon([(-50, BH), (-50, 1060), (900, 1000), (1800, 1100), (2400, 1040), (2400, BH)], fill=(16, 22, 38))
    tent(d, 820, 1010, 0.45, glowing=True)
    im = glow(im, 810, 990, 90, (255, 140, 40), 0.6)
    return im


def sc_descent(rng, p):
    im = grad((60, 80, 130), (190, 200, 220), mid=(120, 140, 180), midpos=0.4)
    d = ImageDraw.Draw(im)
    for i, base in enumerate([520, 700, 900]):
        mrange(d, rng, base, 8, 120 + i * 40, 220 + i * 60, mix((120, 140, 180), (60, 70, 100), i / 3),
               mix((90, 100, 140), (40, 46, 70), i / 3), (230, 236, 250), (160, 176, 210), snow=0.5)
        im = fog(im, base - 40, 80, (170, 182, 210), 0.4, 40)
        d = ImageDraw.Draw(im)
    d.polygon([(-50, BH), (-50, 900), (700, 1000), (1400, 940), (2400, 1060), (2400, BH)], fill=(220, 228, 242))
    d.polygon([(700, 1000), (1400, 940), (2400, 1060), (2400, BH), (900, BH)], fill=(170, 182, 210))
    # трещины
    for _ in range(6):
        x, y = rng.uniform(200, 2100), rng.uniform(1050, 1250)
        d.polygon([(x - 120, y), (x - 40, y - 12), (x + 60, y + 4), (x + 140, y - 6), (x + 60, y + 18), (x - 40, y + 14)], fill=(30, 50, 90))
    # маршрут вниз
    route = [(1900, 1180), (1500, 1060), (1250, 930), (1100, 800), (900, 700), (760, 560), (640, 470)]
    for a, b in zip(route, route[1:]):
        n = int(math.dist(a, b) / 40)
        for k in range(n):
            if k % 2 == 0:
                t0, t1 = k / n, (k + 1) / n
                d.line((a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0,
                        a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1), fill=(255, 122, 26), width=10)
    for (x, y), lab in zip([route[0], route[3], route[-1]], ["8,400 m", "7,100 m", "5,364 m  BASE CAMP"]):
        d.ellipse((x - 16, y - 16, x + 16, y + 16), fill=(255, 184, 77), outline=(40, 20, 0), width=4)
        d.text((x + 30, y - 34), lab, font=font(F_BLACK, 48), fill=(255, 255, 255), stroke_width=6, stroke_fill=(20, 30, 50))
    person(d, 1760, 1215, 0.8, (16, 20, 34))
    return im


def sc_end(rng, p):
    im = grad((4, 6, 16), (20, 30, 60))
    d = ImageDraw.Draw(im)
    stars(d, rng, 700, 0.6)
    peak(d, 1152, 260, 1300, 1000, (40, 56, 96), (20, 28, 54), snow=0.45, slit=(130, 150, 196), sshade=(60, 74, 116), rng=rng)
    im = fog(im, 700, 600, (6, 8, 20), 0.75, 80)
    d = ImageDraw.Draw(im)
    text_c(d, 1152, 330, "EVEREST", font(F_BOLD, 64), (180, 200, 240), spacing=24)
    im = add_glow_layer(im, lambda g: text_c(g, 1152, 410, "GET DOWN ALIVE", font(F_BLACK, 190), (255, 120, 30)), 30, 0.9)
    d = ImageDraw.Draw(im)
    text_c(d, 1152, 410, "GET DOWN ALIVE", font(F_BLACK, 190), (255, 214, 150))
    if p.get("cta"):
        text_c(d, 1152, 700, "HOW MANY DAYS WOULD YOU LAST?", font(F_BOLD, 60), (235, 240, 255))
        d.rounded_rectangle((852, 820, 1452, 930), 55, fill=(232, 48, 42))
        text_c(d, 1152, 842, "SUBSCRIBE", font(F_BLACK, 62), (255, 255, 255), spacing=6)
    return im


def sc_card(rng, p):
    im = grad((6, 8, 16), (14, 20, 36))
    d = ImageDraw.Draw(im)
    mrange(d, rng, 1296, 6, 260, 460, (22, 30, 50), (14, 18, 34), (44, 56, 84), (26, 32, 52), snow=0.4)
    im = fog(im, 900, 400, (6, 8, 16), 0.6, 80)
    d = ImageDraw.Draw(im)
    big = p["big"]
    small = p["small"]
    if big == "EVEREST":
        im = add_glow_layer(im, lambda g: text_c(g, 1152, 430, "EVEREST", font(F_BLACK, 260), (90, 140, 255)), 40, 0.9)
        d = ImageDraw.Draw(im)
        text_c(d, 1152, 430, "EVEREST", font(F_BLACK, 260), (236, 242, 255))
        text_c(d, 1152, 760, small, font(F_BOLD, 64), (255, 184, 77), spacing=14)
    else:
        text_c(d, 1152, 440, big, font(F_BOLD, 56), (255, 184, 77), spacing=22)
        im = add_glow_layer(im, lambda g: text_c(g, 1152, 540, small, font(F_BLACK, 170), (80, 120, 220)), 36, 0.8)
        d = ImageDraw.Draw(im)
        text_c(d, 1152, 540, small, font(F_BLACK, 170), (240, 244, 255))
    return im


def sc_rule(rng, p):
    im = grad((26, 12, 6), (8, 4, 2))
    im = glow(im, 1152, 648, 600, (255, 120, 40), 0.35)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((460, 300, 1844, 1000), 60, fill=(244, 227, 193))
    d.rounded_rectangle((460, 300, 1844, 1000), 60, outline=(42, 18, 0), width=10)
    d.ellipse((560, 420, 860, 720), fill=(255, 122, 26), outline=(42, 18, 0), width=8)
    text_c(d, 710, 470, p["n"], font(F_BLACK, 190), (42, 18, 0))
    d.text((940, 420), "RULE " + p["n"], font=font(F_BOLD, 54), fill=(150, 80, 30))
    hf = font(F_BLACK, 88)
    words, lines, cur = p["head"].split(), [], ""
    for w in words:
        if hf.getlength(cur + " " + w) > 820 and cur:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    for i, ln in enumerate(lines):
        d.text((940, 500 + i * 100), ln, font=hf, fill=(42, 18, 0))
    d.text((560, 860), p["sub"], font=font(F_SEMI, 50), fill=(110, 70, 40))
    return im


SCENES = {k[3:]: v for k, v in globals().items() if k.startswith("sc_")}


def render_still(scene, p, seed=1):
    rng = random.Random(seed)
    return SCENES[scene](rng, p)
