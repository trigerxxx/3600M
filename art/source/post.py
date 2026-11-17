"""Обработка ключевого арта: свечение, цвет, виньетка, заголовок."""
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageChops, ImageFont

src, out = sys.argv[1], sys.argv[2]
img = Image.open(src).convert("RGB")
W, H = img.size

# свечение: яркие места размыть и добавить сверху
bright = img.point(lambda v: max(0, v - 170) * 3)
glow = bright.filter(ImageFilter.GaussianBlur(W * 0.02))
img = ImageChops.add(img, glow)
glow2 = bright.filter(ImageFilter.GaussianBlur(W * 0.06))
img = ImageChops.add(img, glow2.point(lambda v: v // 2))

# цвет
img = ImageEnhance.Color(img).enhance(1.25)
img = ImageEnhance.Contrast(img).enhance(1.08)

# виньетка
vig = Image.new("L", (W, H), 0)
d = ImageDraw.Draw(vig)
for i in range(60):
    t = i / 60
    pad = int(t * W * 0.45)
    d.ellipse((-W * 0.25 + pad, -H * 0.15 + pad, W * 1.25 - pad, H * 1.15 - pad), fill=int(255 * t))
vig = vig.filter(ImageFilter.GaussianBlur(W * 0.06))
dark = Image.new("RGB", (W, H), (4, 6, 14))
img = Image.composite(img, dark, vig.point(lambda v: min(255, int(v * 1.4 + 40))))

# затемнение снизу под заголовок
grad = Image.new("L", (W, H), 0)
gd = ImageDraw.Draw(grad)
for y in range(int(H * 0.72), H):
    gd.line([(0, y), (W, y)], fill=int(235 * (y - H * 0.72) / (H * 0.28)))
img = Image.composite(dark, img, grad)

# заголовок
font = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
draw = ImageDraw.Draw(img)


def title(text, size, y, fill, stroke, sw):
    f = ImageFont.truetype(font, size)
    tw = draw.textlength(text, font=f)
    x = (W - tw) / 2
    # тень
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.text((x + size * 0.04, y + size * 0.06), text, font=f, fill=(0, 0, 0, 200), stroke_width=sw, stroke_fill=(0, 0, 0, 200))
    shadow = shadow.filter(ImageFilter.GaussianBlur(size * 0.05))
    img.paste(shadow, (0, 0), shadow)
    draw.text((x, y), text, font=f, fill=fill, stroke_width=sw, stroke_fill=stroke)


s = W / 1080
title("3600", int(300 * s), int(H * 0.755), (255, 184, 102), (60, 20, 5), int(10 * s))
title("DON'T OPEN THE DOOR", int(92 * s), int(H * 0.905), (255, 72, 52), (40, 6, 4), int(7 * s))

img.save(out, quality=95)
print("ok", img.size)
