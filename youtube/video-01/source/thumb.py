from PIL import Image, ImageDraw, ImageFilter, ImageFont
W, H = 1280, 720
BLACK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
im = Image.new("RGB", (W, H), (9, 26, 17))
d = ImageDraw.Draw(im)
for y in range(H):
    k = y / H
    d.line([(0, y), (W, y)], fill=(int(12 + 20 * k), int(40 + 30 * k), int(24 + 10 * k)))
# свечение за сараем
g = Image.new("RGB", (W, H), (0, 0, 0))
ImageDraw.Draw(g).ellipse((700, 140, 1240, 680), fill=(255, 150, 50))
im = Image.blend(im, g.filter(ImageFilter.GaussianBlur(90)), 0.45)
d = ImageDraw.Draw(im)
# сарай
d.polygon([(800, 380), (980, 250), (1160, 380)], fill=(110, 50, 30), outline=(30, 12, 5))
d.rectangle((830, 380, 1130, 610), fill=(150, 80, 45), outline=(30, 12, 5), width=6)
for x in range(850, 1130, 40):
    d.line((x, 390, x, 600), fill=(120, 62, 35), width=4)
d.rectangle((900, 450, 1010, 540), fill=(255, 210, 120), outline=(30, 12, 5), width=6)
d.line((955, 450, 955, 540), fill=(30, 12, 5), width=5)
d.line((900, 495, 1010, 495), fill=(30, 12, 5), width=5)
# трое блочных человечков в окне
for i, x in enumerate((918, 948, 978)):
    d.rectangle((x, 470, x + 22, 492), fill=(255, 207, 138))
    d.rectangle((x - 2, 492, x + 24, 520), fill=[(255, 106, 26), (31, 107, 255), (79, 208, 106)][i])
# деньги
for (x, y, r) in [(760, 200, 0), (1190, 230, 20), (720, 560, -15), (1210, 560, 10)]:
    note = Image.new("RGBA", (130, 64), (0, 0, 0, 0))
    nd = ImageDraw.Draw(note)
    nd.rounded_rectangle((0, 0, 129, 63), radius=8, fill=(90, 170, 90), outline=(20, 60, 25), width=5)
    nd.text((44, 4), "$", font=ImageFont.truetype(BLACK, 46), fill=(20, 60, 25))
    note = note.rotate(r, expand=True)
    im.paste(note, (x, y), note)
d = ImageDraw.Draw(im)
def t(text, size, xy, fill, stroke=10):
    d.text(xy, text, font=ImageFont.truetype(BLACK, size), fill=fill, stroke_width=stroke, stroke_fill=(20, 8, 0))
t("$240M", 210, (50, 120), (255, 205, 100), 12)
t("FROM A", 92, (60, 380), (255, 255, 255))
t("SHED?", 128, (60, 470), (255, 122, 26), 12)
im.save("thumbnail.png")
