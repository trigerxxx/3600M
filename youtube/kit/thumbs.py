"""Обложки канала Волка: тёмный кинематографичный фон, металлическое слово, герой со светящимся контуром,
неоновые графики 📈📉. Используется для всех обложек (правила — CLAUDE.md, раздел видео)."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "sheep-standard", "sketches")); sys.path.insert(0, HERE)
import numpy as np
import wolf as W
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BLK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
Wd, Hd = 1280, 720
NEON_RED, NEON_GREEN = (255, 45, 70), (40, 235, 120)


def F(s):
    return ImageFont.truetype(BLK, s)


def background(glow, cx=640, cy=400):
    y, x = np.mgrid[0:Hd, 0:Wd]
    r = np.sqrt(((x - cx) / Wd) ** 2 + ((y - cy) / Hd) ** 2)
    a = np.array([12, 14, 24], np.float32) + np.clip(1 - r * 1.8, 0, 1)[..., None] * np.array(glow, np.float32) * 0.6
    a = a * np.clip(1 - r * 0.9, 0.35, 1)[..., None] + np.random.default_rng(1).normal(0, 4, (Hd, Wd, 1))
    im = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")
    grid = Image.new("RGBA", (Wd, Hd), (0, 0, 0, 0)); d = ImageDraw.Draw(grid)   # еле видная сетка биржевого графика
    for gx in range(0, Wd, 80):
        d.line((gx, 0, gx, Hd), fill=(255, 255, 255, 16), width=1)
    for gy in range(0, Hd, 80):
        d.line((0, gy, Wd, gy), fill=(255, 255, 255, 16), width=1)
    im.alpha_composite(grid)
    return im


def metal_word(im, text, y, size):
    f = F(size); w = f.getlength(text)
    while w > 1240:
        size -= 6; f = F(size); w = f.getlength(text)
    x = int((Wd - w) / 2)
    mask = Image.new("L", (Wd, Hd), 0); ImageDraw.Draw(mask).text((x, y), text, font=f, fill=255)
    bb = mask.getbbox(); t = np.clip((np.arange(Hd)[:, None] - bb[1]) / (bb[3] - bb[1]), 0, 1)
    g = ((1 - t) + t * 0.45) * 255
    lay = Image.fromarray(np.stack([g, g, g], -1).repeat(Wd, 1).clip(0, 255).astype(np.uint8)).convert("RGBA")
    lay.putalpha(mask.point(lambda v: int(v * 0.92)))
    sh = Image.new("RGBA", (Wd, Hd), (0, 0, 0, 0)); sh.putalpha(mask.filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.6)))
    im.alpha_composite(sh, (6, 10)); im.alpha_composite(lay)


def neon_chart(im, pts, col, width=16, fill=True, label=None, arrow=True):
    """Насыщенный неоновый график со свечением, заливкой и стрелкой."""
    lay = Image.new("RGBA", (Wd, Hd), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    if fill:
        poly = pts + [(pts[-1][0], Hd), (pts[0][0], Hd)]
        m = Image.new("L", (Wd, Hd), 0); ImageDraw.Draw(m).polygon(poly, fill=255)
        top = min(p[1] for p in pts); t = np.clip((np.arange(Hd)[:, None] - top) / (Hd - top), 0, 1)
        xr = np.clip((np.arange(Wd)[None, :] - pts[0][0]) / 260, 0, 1)      # мягкий вход слева, без резкой границы
        alpha = (np.asarray(m, np.float32) / 255) * (0.38 * (1 - t)) * xr * 255
        fl = Image.new("RGBA", (Wd, Hd), col + (0,)); fl.putalpha(Image.fromarray(alpha.astype(np.uint8)))
        im.alpha_composite(fl)
    d.line(pts, fill=col + (255,), width=width, joint="curve")
    if arrow:
        (x0, y0), (x1, y1) = pts[-2], pts[-1]
        v = np.array([x1 - x0, y1 - y0], float); v /= np.linalg.norm(v); n = np.array([-v[1], v[0]])
        tip = np.array([x1, y1]) + v * 34
        d.polygon([tuple(tip), tuple(np.array([x1, y1]) + n * 30 - v * 10), tuple(np.array([x1, y1]) - n * 30 - v * 10)], fill=col + (255,))
    a = lay.getchannel("A")
    for r, k in ((26, 1.0), (10, 1.0)):
        g = Image.new("RGBA", (Wd, Hd), col + (0,)); g.putalpha(a.filter(ImageFilter.GaussianBlur(r)).point(lambda v: min(255, int(v * k))))
        im.alpha_composite(g)
    core = Image.new("RGBA", (Wd, Hd), (255, 255, 255, 0)); core.putalpha(a.filter(ImageFilter.MinFilter(9)).point(lambda v: int(v * 0.55)))
    im.alpha_composite(lay); im.alpha_composite(core)
    if label:
        txt, (lx, ly) = label
        ImageDraw.Draw(im).text((lx, ly), txt, font=F(44), fill=col + (255,), stroke_width=6, stroke_fill=(8, 8, 12))


def hero(im, fn, rim):
    big = Image.new("RGBA", (Wd * 2, Hd * 2), (0, 0, 0, 0)); fn(ImageDraw.Draw(big), 2)
    lay = big.resize((Wd, Hd), Image.LANCZOS); a = lay.getchannel("A")
    rgb = np.asarray(lay.convert("RGB"), np.float32) * np.linspace(1.1, 0.82, Hd)[:, None, None]
    sh_ = Image.fromarray(rgb.clip(0, 255).astype(np.uint8)).convert("RGBA"); sh_.putalpha(a)
    gl = Image.new("RGBA", (Wd, Hd), rim + (0,)); gl.putalpha(a.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.9)))
    shadow = Image.new("RGBA", (Wd, Hd), (0, 0, 0, 0)); shadow.putalpha(a.filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.7)))
    im.alpha_composite(shadow, (18, 22)); im.alpha_composite(gl); im.alpha_composite(sh_)


def finish(im, path):
    a = np.asarray(im.convert("RGB"), np.float32) + np.random.default_rng(2).normal(0, 3, (Hd, Wd, 1))
    Image.fromarray(a.clip(0, 255).astype(np.uint8)).save(path)


def preview(paths, out):
    ims = [Image.open(p) for p in paths]
    o = Image.new("RGB", (660 * len(ims), 480), (40, 40, 40))
    for i, x in enumerate(ims):
        o.paste(x.resize((640, 360)), (i * 660, 0)); o.paste(x.resize((196, 110)), (i * 660, 368))
    o.save(out)
