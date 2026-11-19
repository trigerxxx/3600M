"""Сцены для сериала GHOST (хакер, ФБР). Тёмные, плоские, один холодный акцент (циан) и красный для опасности.
Импорт этого модуля регистрирует сцены в scenes.SCENES, после чего их можно звать через kit.scene("..."). """
import math
import random

from PIL import Image, ImageDraw, ImageFilter

import scenes as S
from scenes import BH, BW, F_BLACK, F_BOLD, F_SEMI, font, glow, grad, text_c

CYAN = (80, 220, 255)
RED = (232, 48, 42)
INK = (8, 10, 16)


def human(d, x, y, s, col, liz=False, back=False):
    """Силуэт по пояс: голова, плечи. liz — хвост волос; back — со спины в капюшоне."""
    d.ellipse((x - 48 * s, y - 230 * s, x + 48 * s, y - 128 * s), fill=col)
    if liz:
        d.ellipse((x + 30 * s, y - 210 * s, x + 80 * s, y - 120 * s), fill=col)
    if back:
        d.polygon([(x - 62 * s, y - 150 * s), (x, y - 250 * s), (x + 62 * s, y - 150 * s)], fill=col)
    d.polygon([(x - 150 * s, y + 60 * s), (x - 130 * s, y - 70 * s), (x - 60 * s, y - 120 * s), (x + 60 * s, y - 120 * s),
               (x + 130 * s, y - 70 * s), (x + 150 * s, y + 60 * s)], fill=col)


def cat(d, x, y, s, col, eyes=(255, 214, 80)):
    d.ellipse((x - 70 * s, y - 60 * s, x + 70 * s, y + 40 * s), fill=col)
    d.ellipse((x - 45 * s, y - 130 * s, x + 45 * s, y - 50 * s), fill=col)
    d.polygon([(x - 42 * s, y - 110 * s), (x - 36 * s, y - 160 * s), (x - 10 * s, y - 125 * s)], fill=col)
    d.polygon([(x + 42 * s, y - 110 * s), (x + 36 * s, y - 160 * s), (x + 10 * s, y - 125 * s)], fill=col)
    d.line((x + 60 * s, y + 20 * s, x + 130 * s, y - 30 * s, x + 120 * s, y - 90 * s), fill=col, width=int(16 * s), joint="curve")
    for ex in (-1, 1):
        d.ellipse((x + ex * 20 * s - 9 * s, y - 100 * s, x + ex * 20 * s + 9 * s, y - 84 * s), fill=eyes)


def code_lines(d, box, rng, col=CYAN, n=14):
    x0, y0, x1, y1 = box
    for i in range(n):
        y = y0 + 20 + i * (y1 - y0 - 40) / n
        x = x0 + 30 + rng.choice([0, 0, 40, 80])
        w = rng.uniform(0.2, 0.75) * (x1 - x0 - 120)
        d.rectangle((x, y, x + w, y + 10), fill=tuple(int(c * rng.uniform(0.5, 1)) for c in col))


def sc_apartment(rng, p):
    im = grad((10, 14, 30), (4, 5, 12))
    d = ImageDraw.Draw(im)
    # окно с городом
    d.rectangle((1500, 180, 2150, 760), fill=(14, 22, 48))
    for _ in range(140):
        x, y = rng.uniform(1520, 2130), rng.uniform(380, 740)
        d.rectangle((x, y, x + 10, y + 14), fill=rng.choice([(255, 214, 120), (255, 190, 90), (120, 160, 220)]))
    for k in range(9):
        x = 1520 + k * 70
        h = rng.uniform(150, 360)
        d.rectangle((x, 760 - h, x + 60, 760), fill=(8, 12, 26))
    d.rectangle((1500, 180, 2150, 760), outline=(30, 34, 50), width=18)
    d.line((1825, 180, 1825, 760), fill=(30, 34, 50), width=12)
    # стол и монитор
    d.rectangle((0, 980, BW, BH), fill=(16, 14, 20))
    d.rectangle((0, 960, BW, 985), fill=(36, 30, 40))
    mon = (520, 400, 1260, 860)
    d.rectangle((mon[0] - 16, mon[1] - 16, mon[2] + 16, mon[3] + 16), fill=(20, 22, 28))
    d.rectangle(mon, fill=(6, 20, 30))
    code_lines(d, mon, rng)
    d.rectangle((860, 876, 920, 960), fill=(20, 22, 28))
    im = glow(im, 890, 630, 520, (40, 140, 190), 0.55)
    d = ImageDraw.Draw(im)
    human(d, 860, 1280, 1.5, INK, back=True)
    cat(d, 1420, 950, 1.0, (14, 12, 18))
    d.rounded_rectangle((300, 880, 380, 960), 10, fill=(60, 50, 60))   # кружка
    return im


def sc_pizza(rng, p):
    im = grad((8, 10, 18), (2, 3, 6))
    im = glow(im, 1152, 640, 700, (40, 60, 90), 0.5)
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = 340, 160, 1964, 1140
    d.rounded_rectangle((x0 - 24, y0 - 24, x1 + 24, y1 + 24), 30, fill=(20, 22, 28))
    d.rectangle((x0, y0, x1, y1), fill=(250, 246, 240))
    d.rectangle((x0, y0, x1, y0 + 70), fill=(220, 222, 228))
    for k, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse((x0 + 30 + k * 40, y0 + 22, x0 + 56 + k * 40, y0 + 48), fill=c)
    d.rectangle((x0, y0 + 70, x1, y0 + 200), fill=(200, 40, 34))
    d.text((x0 + 60, y0 + 95), "PIZZA PALACE", font=font(F_BLACK, 80), fill=(255, 255, 255))
    # пицца
    cx, cy, r = x0 + 420, y0 + 560, 250
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(230, 160, 70))
    d.ellipse((cx - r + 30, cy - r + 30, cx + r - 30, cy + r - 30), fill=(220, 60, 40))
    for _ in range(14):
        a, rr = rng.uniform(0, 6.28), rng.uniform(0, r - 70)
        px, py = cx + math.cos(a) * rr, cy + math.sin(a) * rr
        d.ellipse((px - 26, py - 26, px + 26, py + 26), fill=(150, 30, 30))
    # корзина
    bx = x0 + 820
    d.text((bx, y0 + 270), "YOUR ORDER", font=font(F_BOLD, 50), fill=(40, 40, 46))
    for i, (item, price) in enumerate([("XXL Pepperoni", "$0.00"), ("Garlic bread", "$0.00"), ("Cola x2", "$0.00")]):
        y = y0 + 360 + i * 80
        d.text((bx, y), item, font=font(F_SEMI, 46), fill=(60, 60, 66))
        d.text((x1 - 260, y), price, font=font(F_BOLD, 46), fill=(60, 60, 66))
    d.line((bx, y0 + 620, x1 - 60, y0 + 620), fill=(200, 200, 206), width=4)
    d.text((bx, y0 + 650), "TOTAL", font=font(F_BLACK, 70), fill=(20, 20, 24))
    d.text((x1 - 380, y0 + 650), "$0.00", font=font(F_BLACK, 80), fill=(30, 170, 70))
    d.rounded_rectangle((bx, y0 + 800, x1 - 60, y0 + 900), 20, fill=(30, 170, 70))
    text_c(d, (bx + x1 - 60) / 2, y0 + 818, "ORDER PLACED", font(F_BLACK, 56), (255, 255, 255))
    return im


def sc_door(rng, p):
    im = grad((6, 6, 10), (2, 2, 4))
    d = ImageDraw.Draw(im)
    dx0, dy0, dx1, dy1 = 820, 120, 1484, 1296
    # свет из щелей: красный и синий
    im = glow(im, dx0 - 10, 700, 260, (40, 70, 255), 0.9)
    im = glow(im, dx1 + 10, 700, 260, (255, 40, 40), 0.9)
    im = glow(im, 1152, dy0 - 10, 220, (230, 230, 255), 0.5)
    d = ImageDraw.Draw(im)
    d.rectangle((dx0 - 40, dy0 - 40, dx1 + 40, dy1), fill=(26, 22, 22))
    d.rectangle((dx0, dy0, dx1, dy1), fill=(58, 40, 30))
    for (a, b) in [((dx0 + 60, dy0 + 80), (dx1 - 60, dy0 + 520)), ((dx0 + 60, dy0 + 620), (dx1 - 60, dy1 - 80))]:
        d.rectangle((a[0], a[1], b[0], b[1]), outline=(44, 30, 22), width=14)
    d.ellipse((dx1 - 110, 700, dx1 - 60, 750), fill=(190, 160, 90))
    # трещины
    for _ in range(3):
        x, y = rng.uniform(dx0 + 100, dx1 - 100), rng.uniform(300, 900)
        pts = [(x, y)]
        for _ in range(5):
            x, y = x + rng.uniform(-60, 60), y + rng.uniform(30, 90)
            pts.append((x, y))
        d.line(pts, fill=(14, 10, 8), width=6)
    # часы на стене
    d.ellipse((260, 260, 520, 520), fill=(230, 230, 236), outline=(40, 40, 46), width=12)
    d.line((390, 390, 390, 290), fill=INK, width=12)
    d.line((390, 390, 390, 480), fill=INK, width=8)
    return im


def sc_wall(rng, p):
    im = grad((26, 20, 16), (12, 9, 8))
    d = ImageDraw.Draw(im)
    d.rectangle((120, 90, 2184, 1210), fill=(120, 86, 56))
    for _ in range(1600):
        x, y = rng.uniform(120, 2184), rng.uniform(90, 1210)
        d.point((x, y), fill=(100, 70, 44))
    pins = []
    for _ in range(26):
        w, h = rng.uniform(150, 260), rng.uniform(110, 200)
        x, y = rng.uniform(180, 2120 - w), rng.uniform(130, 1150 - h)
        if 820 < x + w / 2 < 1480 and 360 < y + h / 2 < 940:
            continue
        photo = rng.random() < 0.4
        d.rectangle((x, y, x + w, y + h), fill=(70, 74, 82) if photo else (238, 234, 222))
        if photo:
            S.person(d, x + w / 2, y + h - 6, h / 300, (30, 32, 38))
        else:
            for k in range(4):
                d.rectangle((x + 16, y + 24 + k * 28, x + 16 + rng.uniform(0.4, 0.9) * (w - 32), y + 34 + k * 28), fill=(160, 156, 146))
        pins.append((x + w / 2, y + 10))
    # центр: силуэт со знаком вопроса
    cx, cy = 1152, 650
    d.rectangle((cx - 300, cy - 300, cx + 300, cy + 300), fill=(238, 234, 222))
    human(d, cx, cy + 290, 1.55, (20, 20, 24))
    text_c(d, cx, cy - 150, "?", font(F_BLACK, 170), (255, 255, 255))
    # красные нитки
    for (x, y) in pins:
        d.line((x, y, cx + rng.uniform(-200, 200), cy - 290), fill=(200, 30, 30), width=5)
        d.ellipse((x - 12, y - 12, x + 12, y + 12), fill=(220, 40, 40))
    im = glow(im, cx, cy, 600, (255, 220, 160), 0.25)
    return im


def sc_office(rng, p):
    im = grad((18, 22, 32), (6, 8, 12))
    d = ImageDraw.Draw(im)
    for k in range(6):   # лампы
        x = 200 + k * 380
        d.rectangle((x, 60, x + 220, 80), fill=(220, 230, 255))
    im = glow(im, 1152, 0, 900, (120, 140, 200), 0.3)
    d = ImageDraw.Draw(im)
    for row, (y, s) in enumerate([(560, 0.5), (700, 0.7)]):
        for k in range(7 - row * 2):
            x = 150 + k * (320 + row * 130) + row * 60
            d.rectangle((x, y, x + 260 * s * 1.6, y + 20), fill=(40, 44, 56))
            d.rectangle((x + 60 * s, y - 150 * s, x + 260 * s, y - 10), fill=(30, 50, 70))
            S.person(d, x + 100 * s * 1.6, y + 10, s * 0.9, (14, 16, 24))
    # передний стол: кофе и пропуск
    d.rectangle((0, 1000, BW, BH), fill=(30, 26, 26))
    d.rounded_rectangle((700, 860, 860, 1060), 16, fill=(236, 236, 236))
    d.ellipse((700, 840, 860, 890), fill=(80, 50, 30))
    for k in range(3):
        d.line((740 + k * 40, 820, 750 + k * 40, 700), fill=(200, 200, 210), width=5)
    bx, by = 1200, 860
    d.rounded_rectangle((bx, by, bx + 480, by + 300), 24, fill=(240, 240, 244))
    d.rectangle((bx, by, bx + 480, by + 70), fill=(30, 50, 110))
    d.text((bx + 30, by + 12), "FEDERAL BUREAU", font=font(F_BOLD, 40), fill=(255, 255, 255))
    d.rectangle((bx + 30, by + 100, bx + 170, by + 260), fill=(160, 166, 176))
    d.text((bx + 200, by + 110), "CONSULTANT", font=font(F_BLACK, 36), fill=(30, 50, 110))
    d.text((bx + 200, by + 180), "ACCESS: 2", font=font(F_BOLD, 36), fill=(90, 96, 110))
    return im


def sc_liz(rng, p):
    im = grad((30, 26, 22), (8, 7, 6))
    d = ImageDraw.Draw(im)
    for k in range(14):   # жалюзи
        y = 120 + k * 60
        d.rectangle((1250, y, 2150, y + 34), fill=(230, 190, 120))
    im = glow(im, 1700, 520, 600, (255, 180, 90), 0.4)
    d = ImageDraw.Draw(im)
    human(d, 1150, 1300, 3.2, (14, 12, 12), liz=True)
    d.polygon([(1240, 1050), (1290, 1030), (1300, 1090), (1250, 1110)], fill=(230, 190, 90))   # значок
    return im


def sc_mask(rng, p):
    im = Image.new("RGB", (BW, BH), (2, 3, 6))
    im = glow(im, 1152, 620, 500, (30, 120, 160), 0.6)
    d = ImageDraw.Draw(im)
    d.ellipse((900, 240, 1404, 1000), fill=(236, 240, 244))
    d.polygon([(960, 520), (1110, 560), (1100, 600), (970, 580)], fill=INK)
    d.polygon([(1344, 520), (1194, 560), (1204, 600), (1334, 580)], fill=INK)
    d.line((1060, 820, 1152, 840, 1244, 820), fill=(60, 64, 70), width=10, joint="curve")
    if p.get("title", True):
        text_c(d, 1152, 1060, "GHOST", font(F_BLACK, 140), CYAN, spacing=30)
    return im


def sc_choice(rng, p):
    im = Image.new("RGB", (BW, BH), (6, 6, 10))
    d = ImageDraw.Draw(im)
    # слева решётка
    d.rectangle((150, 200, 1000, 1100), fill=(30, 32, 38))
    for k in range(9):
        x = 190 + k * 95
        d.rectangle((x, 200, x + 26, 1100), fill=(120, 126, 136))
    d.rectangle((150, 200, 1000, 236), fill=(120, 126, 136))
    d.rectangle((150, 1064, 1000, 1100), fill=(120, 126, 136))
    text_c(d, 575, 1130, "10 YEARS", font(F_BLACK, 90), (220, 220, 226))
    # справа значок
    cx, cy = 1730, 620
    pts = [(cx, cy - 330), (cx + 260, cy - 200), (cx + 230, cy + 160), (cx, cy + 340), (cx - 230, cy + 160), (cx - 260, cy - 200)]
    d.polygon(pts, fill=(220, 180, 70))
    d.polygon([(x * 0.8 + cx * 0.2, y * 0.8 + cy * 0.2) for x, y in pts], fill=(240, 205, 100))
    text_c(d, cx, cy - 60, "FBI", font(F_BLACK, 130), (90, 60, 10))
    text_c(d, cx, 1130, "WORK FOR US", font(F_BLACK, 90), (240, 205, 100))
    text_c(d, 1152, 560, "OR", font(F_BLACK, 110), (255, 255, 255))
    return im


for _k, _v in list(globals().items()):
    if _k.startswith("sc_"):
        S.SCENES[_k[3:]] = _v
