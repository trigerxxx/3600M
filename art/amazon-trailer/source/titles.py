from PIL import Image, ImageDraw, ImageFilter, ImageFont
W, H = 1280, 720
BLACK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def centered(d, text, font, y, fill):
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, y), text, font=font, fill=fill)

# 1. радио на чёрном (субтитр)
im = Image.new("RGB", (W, H), (0, 0, 0))
d = ImageDraw.Draw(im)
centered(d, "« …поиски будут прекращены через 33 дня… »", ImageFont.truetype(REG, 30), 560, (200, 210, 220))
im.save("radio.png")

# 2. титул
im = Image.new("RGB", (W, H), (4, 10, 6))
glow = Image.new("RGB", (W, H), (0, 0, 0))
g = ImageDraw.Draw(glow)
centered(g, "33 DAYS", ImageFont.truetype(BLACK, 190), 190, (255, 140, 40))
glow = glow.filter(ImageFilter.GaussianBlur(28))
im = Image.blend(im, glow, 0.6)
d = ImageDraw.Draw(im)
centered(d, "33 DAYS", ImageFont.truetype(BLACK, 190), 190, (255, 196, 110))
centered(d, "LOST IN THE AMAZON", ImageFont.truetype(BLACK, 46), 420, (120, 230, 170))
centered(d, "Найди их.  Подай сигнал.  Успей.", ImageFont.truetype(REG, 30), 520, (230, 236, 240))
im.save("title.png")

# 3. финальная фраза для рекламы
im = Image.new("RGB", (W, H), (0, 0, 0))
d = ImageDraw.Draw(im)
centered(d, "THEN THEY STOP SEARCHING.", ImageFont.truetype(BLACK, 64), 320, (255, 255, 255))
im.save("stop.png")
print("ok")
