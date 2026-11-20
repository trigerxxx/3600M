"""Аватар канала The Sheep Standard: Волк в костюме крупным планом. 800x800 (YouTube/TikTok показывают кругом)."""
from PIL import Image, ImageDraw

from wolf import sheep, wolf

S = 800


def avatar(bg, name, gary=False):
    im = Image.new("RGB", (S, S), bg)
    d = ImageDraw.Draw(im)
    # рисуем сразу в 800x800: голова крупно по центру, внизу воротник и галстук
    wolf(d, 298, 1248, 1.7, "stand")
    if gary:
        sheep(d, 150, 790, 0.75, 0.0, "shock", seed=9)
    # предпросмотр кругом
    m = Image.new("L", (S, S), 0)
    ImageDraw.Draw(m).ellipse((0, 0, S - 1, S - 1), fill=255)
    circ = Image.new("RGB", (S, S), (24, 24, 28))
    circ.paste(im, (0, 0), m)
    im.save(f"avatar-{name}.png")
    return circ


prev = Image.new("RGB", (S * 3 + 80, S + 40), (24, 24, 28))
for i, (bg, name, g) in enumerate([((255, 255, 255), "white", False), ((79, 179, 240), "blue", False), ((246, 214, 92), "gold", True)]):
    prev.paste(avatar(bg, name, g), (20 + i * (S + 20), 20))
prev.save("avatar-preview.png")
