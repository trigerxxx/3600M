"""Шапка канала The Sheep Standard: 2560x1440, главное — в безопасной зоне 1546x423 по центру (видно на телефоне)."""
from PIL import Image, ImageDraw, ImageFont

from wolf import INK, line, sheep, shape, wob, wolf

W, H = 2560, 1440
SAFE = (507, 508, 2053, 931)
F = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
FB = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"


def outlined(d, xy, txt, f, fill, stroke=10):
    d.text(xy, txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=INK)


def banner(bg, name, title_fill, sub_fill):
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im)
    # по краям (видно только на ПК/ТВ): облака шерсти и пасущиеся овцы
    for k, (x, y, r) in enumerate([(150, 300, 90), (320, 1150, 110), (2380, 260, 100), (2250, 1200, 120), (120, 800, 70), (2450, 760, 80)]):
        shape(d, wob(x, y, r, r * 0.7, seed=80 + k), (255, 255, 255), 8)
    for k, x in enumerate([180, 2330]):
        sheep(d, x, 1080 if k else 560, 0.7, 1.0, "calm", seed=90 + k)
    # волк слева: голова целиком в безопасной зоне, костюм уходит вниз (на ПК виден весь)
    wolf(d, 680, 1186, 0.9, "shears")
    # заголовок и подзаголовок справа от волка
    ft, fs = ImageFont.truetype(F, 96), ImageFont.truetype(FB, 40)
    t1, t2 = "THE SHEEP STANDARD", "A wolf in a suit explains how money really works."
    cx = 1490
    outlined(d, (cx - ft.getlength(t1) / 2, 545), t1, ft, title_fill)
    d.text((cx - fs.getlength(t2) / 2, 672), t2, font=fs, fill=sub_fill)
    # ряд овец: от пушистой до лысого Гэри
    xs, fls = [1250, 1400, 1550], [1.0, 0.5, 0.0]
    for i, (x, fl) in enumerate(zip(xs, fls)):
        sheep(d, x, 918, 0.45, fl, ["calm", "sad", "shock"][i], seed=5 + i)
    fg = ImageFont.truetype(F, 36)
    line(d, (1700, 850), (1635, 850), 5, seed=3)
    d.polygon([(1640, 838), (1640, 862), (1618, 850)], fill=INK)
    d.text((1715, 828), "GARY", font=fg, fill=INK)
    im.save(f"banner-{name}.png")
    # превью: что видно на телефоне (безопасная зона) и на ПК
    pv = im.copy()
    ImageDraw.Draw(pv).rectangle(SAFE, outline=(232, 48, 42), width=6)
    return pv, im.crop(SAFE)


for bg, name, tf, sf in [((79, 179, 240), "blue", (255, 255, 255), (12, 30, 60)), ((255, 255, 255), "white", (255, 255, 255), (60, 60, 66))]:
    pv, safe = banner(bg, name, tf, sf)
    pv.resize((1280, 720)).save(f"banner-{name}-preview-desktop.png")
    safe.save(f"banner-{name}-preview-phone.png")
