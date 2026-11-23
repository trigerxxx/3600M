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


def hero(im, fn, rim, volume=True):
    """Герой со светящимся контуром и тенью. volume=True — объём: свет сверху-слева, затемнение к краям."""
    big = Image.new("RGBA", (Wd * 2, Hd * 2), (0, 0, 0, 0)); fn(ImageDraw.Draw(big), 2)
    lay = big.resize((Wd, Hd), Image.LANCZOS); a = lay.getchannel("A")
    rgb = np.asarray(lay.convert("RGB"), np.float32)
    if volume:
        bb = a.getbbox() or (0, 0, Wd, Hd)
        y, x = np.mgrid[0:Hd, 0:Wd].astype(np.float32)
        lx, ly = bb[0] + (bb[2] - bb[0]) * 0.3, bb[1] + (bb[3] - bb[1]) * 0.15           # «лампа» сверху-слева
        r = np.sqrt(((x - lx) / (bb[2] - bb[0] + 1)) ** 2 + ((y - ly) / (bb[3] - bb[1] + 1)) ** 2)
        light = np.clip(1.28 - r * 0.75, 0.68, 1.28)
        inner = np.asarray(a.filter(ImageFilter.GaussianBlur(22)), np.float32) / 255     # к краям темнее
        edge = 0.72 + 0.28 * np.clip((inner - 0.35) / 0.5, 0, 1)
        rgb = rgb * (light * edge)[..., None]
    else:
        rgb = rgb * np.linspace(1.1, 0.82, Hd)[:, None, None]
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


def wolf_portrait(d, cx, cy, s=1.0, lens=True, mood="smirk", glasses="on", hat=None, monocle=False, chain=False, outfit="suit"):
    """glasses: on / down / none. hat: None / top (цилиндр). monocle, chain — реквизит «богача»."""
    """Волк анфас для обложек: голова и плечи, тёмные очки с отражением графиков, хитрая ухмылка.
    cx, cy — центр головы. Никаких вытянутых рук — только портрет."""
    sh, wob, INK = W.shape, W.wob, (17, 17, 17)
    GREY, GREY_L, GREY_D, SUIT, TIE = (128, 132, 140), (198, 201, 206), (92, 96, 106), (34, 44, 74), (214, 40, 40)
    P = lambda x, y: (cx + x * s, cy + y * s)
    lw = max(4, int(9 * s))
    if outfit == "leather":                      # чёрная кожаная куртка поверх чёрной футболки
        LEATHER, TEE = (30, 30, 34), (48, 48, 54)
        sh(d, [P(-440, 1000), P(-360, 330), P(-260, 250), P(-90, 225), P(90, 225), P(260, 250), P(360, 330), P(440, 1000)], LEATHER, lw, seed=201)
        sh(d, [P(-115, 228), P(115, 228), P(70, 1000), P(-70, 1000)], TEE, lw, seed=260)                    # футболка
        d.arc([P(-90, 190), P(90, 290)], 20, 160, fill=INK, width=lw)                                       # круглый ворот
        for k in (-1, 1):                                                                                   # широкий кожаный воротник
            sh(d, [P(k * 95, 228), P(k * 250, 255), P(k * 210, 420), P(k * 120, 470)], (42, 42, 48), lw, seed=261 + k)
            d.line([P(k * 125, 480), P(k * 160, 1000)], fill=(150, 150, 160), width=max(3, int(7 * s)))     # молния
            d.line([P(k * 300, 330), P(k * 360, 560)], fill=(95, 95, 108), width=max(4, int(14 * s)))      # блики кожи
            d.line([P(k * 215, 290), P(k * 230, 380)], fill=(85, 85, 98), width=max(3, int(9 * s)))
    else:
        # плечи и пиджак
        sh(d, [P(-440, 1000), P(-360, 330), P(-260, 250), P(-90, 225), P(90, 225), P(260, 250), P(360, 330), P(440, 1000)], SUIT, lw, seed=201)   # пиджак уходит за низ кадра
        d.polygon([P(-95, 228), P(95, 228), P(0, 470)], fill=(250, 250, 250), outline=INK)
        sh(d, [P(-30, 250), P(30, 250), P(42, 430), P(0, 480), P(-42, 430)], TIE, lw, seed=202)
        sh(d, [P(-34, 232), P(34, 232), P(26, 268), P(-26, 268)], TIE, lw, seed=203)
        for k in (-1, 1):
            W.line(d, P(k * 95, 228), P(k * 30, 470), lw, seed=204 + k)
            d.polygon([P(k * 95, 228), P(k * 150, 235), P(k * 60, 330)], fill=(250, 250, 250), outline=INK)   # воротник рубашки
        sh(d, [P(-250, 380), P(-180, 372), P(-185, 400), P(-245, 405)], (250, 250, 250), max(3, int(5 * s)), seed=230)   # нагрудный платок
        d.polygon([P(-240, 378), P(-215, 350), P(-200, 376)], fill=TIE, outline=INK)
        d.line([P(200, 300), P(290, 360)], fill=(70, 84, 120), width=max(3, int(10 * s)))          # блик на плече
    # шея-мех
    sh(d, [P(-150, 120), P(150, 120), P(120, 250), P(-120, 250)], GREY_D, lw, seed=205)
    # уши
    for k in (-1, 1):
        sh(d, [P(k * 95, -120), P(k * 185, -370), P(k * 225, -95)], GREY_D, lw, seed=206 + k)
        sh(d, [P(k * 125, -135), P(k * 182, -300), P(k * 198, -125)], (70, 62, 70), max(3, int(6 * s)), seed=208 + k)
    # голова: широкие скулы с клочками меха, сужается к морде
    sh(d, [P(-150, -200), P(0, -225), P(150, -200), P(215, -110), P(275, 10), P(225, 40), P(270, 95), P(185, 120),
           P(120, 190), P(0, 215), P(-120, 190), P(-185, 120), P(-270, 95), P(-225, 40), P(-275, 10), P(-215, -110)], GREY, lw, seed=210)
    sh(d, [P(-70, -215), P(0, -228), P(70, -215), P(30, -60), P(0, -40), P(-30, -60)], GREY_D, max(3, int(5 * s)), seed=211)   # тёмная полоса на лбу
    # морда: вытянутая, светлая, сужается к подбородку
    sh(d, [P(-70, -20), P(70, -20), P(118, 95), P(98, 175), P(0, 212), P(-98, 175), P(-118, 95)], GREY_L, lw, seed=213)
    for k in (-1, 1):                         # пряди меха и тени
        for j in range(3):
            d.line([P(k * (175 + j * 22), -40 + j * 40), P(k * (205 + j * 22), -10 + j * 40)], fill=GREY_D, width=max(2, int(6 * s)))
        d.line([P(k * 80, 60), P(k * 104, 120)], fill=(170, 174, 182), width=max(3, int(10 * s)))
        for j in range(3):                    # точки усов
            d.ellipse([P(k * (52 + j * 16) - 4, 122 + (j % 2) * 10 - 4), P(k * (52 + j * 16) + 4, 122 + (j % 2) * 10 + 4)], fill=GREY_D)
    sh(d, [P(-50, 40), P(50, 40), P(38, 90), P(0, 104), P(-38, 90)], INK, max(3, int(5 * s)), seed=215)   # нос
    d.ellipse([P(-24, 50), P(-6, 62)], fill=(95, 98, 108))                                           # блик на носу
    # рот
    d.line([P(0, 104), P(0, 136)], fill=INK, width=lw)
    if mood == "smirk":
        d.line([P(-70, 150), P(-30, 146), P(0, 138)], fill=INK, width=lw, joint="curve")
        d.line([P(0, 138), P(45, 142), P(85, 126), P(108, 98)], fill=INK, width=lw, joint="curve")
        d.polygon([P(60, 138), P(72, 172), P(84, 132)], fill=(255, 255, 255), outline=INK)     # клык в ухмылке
    elif mood == "laugh":
        d.chord([P(-82, 108), P(82, 200)], 0, 180, fill=(90, 26, 32), outline=INK, width=lw)
        for x in (-52, 34):
            d.polygon([P(x, 154), P(x + 10, 178), P(x + 20, 154)], fill=(255, 255, 255), outline=INK)
    elif mood == "shock":
        sh(d, wob(cx, cy + 165 * s, 30 * s, 28 * s, seed=218), (90, 26, 32), lw)
    # глаза (видны, если очки приспущены): жёлтые, хитрые, с полуприкрытым веком
    if glasses in ("down", "none"):
        for k, open_ in ((-1, 0.55), (1, 0.8)):
            ex, ey = k * 98, (-88 if glasses == "down" else -45)
            d.ellipse([P(ex - 50, ey - 30), P(ex + 50, ey + 30)], fill=(255, 205, 60), outline=INK, width=lw)
            d.ellipse([P(ex - 9, ey - 24), P(ex + 9, ey + 24)], fill=INK)                       # вертикальный зрачок
            d.ellipse([P(ex - 18, ey - 18), P(ex - 8, ey - 8)], fill=(255, 255, 255))           # блик
            lid = ey - 30 + 60 * (1 - open_)                                                   # тяжёлое верхнее веко
            d.chord([P(ex - 54, ey - 40), P(ex + 54, lid * 2 - (ey - 40))], 180, 360, fill=GREY, outline=INK, width=lw)
        lens_box = [(-172, -28, -30, 30), (30, -28, 172, 30)] if glasses == "down" else []
        bridge_y, arm_y = 0, -10
    else:
        lens_box = [(-185, -78, -22, 18), (22, -78, 185, 18)]
        bridge_y, arm_y = -45, -55
    for i, (x0, y0, x1, y1) in enumerate(lens_box):
        d.rounded_rectangle([P(x0, y0), P(x1, y1)], radius=int(22 * s), fill=(18, 20, 30), outline=INK, width=lw)
        if lens:                                  # в стёклах отражается график: слева рост, справа обвал
            col = (40, 235, 120) if i == 0 else (255, 45, 70)
            pts = [(0.1, 0.8), (0.3, 0.65), (0.45, 0.72), (0.65, 0.4), (0.9, 0.2)] if i == 0 else [(0.1, 0.25), (0.3, 0.4), (0.5, 0.32), (0.7, 0.62), (0.9, 0.82)]
            pp = [P(x0 + (x1 - x0) * u, y0 + (y1 - y0) * v) for u, v in pts]
            d.line(pp, fill=col, width=max(3, int(8 * s)), joint="curve")
        d.line([P(x0 + 18, y0 + 14), P(x0 + 50, y0 + 8)], fill=(150, 160, 180), width=max(2, int(5 * s)))   # блик
    if lens_box:
        d.line([P(lens_box[0][2], bridge_y), P(lens_box[1][0], bridge_y)], fill=INK, width=lw)   # перемычка
        for k in (-1, 1):
            d.line([P(k * lens_box[1][2], arm_y), P(k * 222, arm_y - 30)], fill=INK, width=lw)    # дужки
    # брови: левая ровная, правая поднята — «самодовольный» взгляд
    by = -40 if glasses == "down" else (5 if glasses == "none" else 0)
    W.line(d, P(-165, -102 + by), P(-40, -92 + by), max(5, int(12 * s)), seed=219)
    d.line([P(40, -112 + by), P(110, -158 + by), P(175, -132 + by)], fill=INK, width=max(5, int(12 * s)), joint="curve")

    GOLD_ = (242, 182, 48)
    if monocle:                                  # монокль на правом глазу + цепочка к лацкану
        ex, ey = 98, (-88 if glasses == "down" else -45)
        d.ellipse([P(ex - 62, ey - 62), P(ex + 62, ey + 62)], outline=GOLD_, width=max(4, int(12 * s)))
        d.ellipse([P(ex - 70, ey - 70), P(ex + 70, ey + 70)], outline=INK, width=max(2, int(5 * s)))
        d.line([P(ex + 50, ey + 50), P(150, 120), P(175, 200), P(120, 300)], fill=GOLD_, width=max(3, int(7 * s)), joint="curve")
    if chain:                                    # золотая цепь на груди
        pts = [P(x, 255 + 0.0016 * x * x) for x in range(-260, 261, 20)]
        d.line(pts, fill=INK, width=max(6, int(18 * s)), joint="curve")
        d.line(pts, fill=GOLD_, width=max(4, int(11 * s)), joint="curve")
        d.ellipse([P(-42, 300), P(42, 384)], fill=GOLD_, outline=INK, width=lw)
        d.text(P(0, 342), "$", font=F(int(60 * s)), fill=INK, anchor="mm")
    if hat == "top":                             # цилиндр, чуть набок
        sh(d, [P(-260, -175), P(250, -205), P(256, -160), P(-254, -130)], (24, 24, 30), lw, seed=250)   # поля
        sh(d, [P(-170, -170), P(160, -196), P(150, -390), P(-160, -372)], (24, 24, 30), lw, seed=251)   # тулья
        sh(d, [P(-166, -235), P(156, -258), P(158, -210), P(-168, -186)], (180, 30, 40), max(3, int(6 * s)), seed=252)  # лента
        d.line([P(-120, -360), P(-110, -260)], fill=(70, 70, 82), width=max(3, int(12 * s)))   # блик



def ai_bubble(d, cx, cy, r, s=1.0):
    """Мыльный пузырь «AI» с иглой."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 200, 255), outline=(230, 245, 255), width=max(4, int(10 * s)))
    d.ellipse([cx - r * 0.82, cy - r * 0.82, cx + r * 0.82, cy + r * 0.82], outline=(200, 160, 255), width=max(3, int(6 * s)))
    d.arc([cx - r * 0.7, cy - r * 0.75, cx + r * 0.2, cy + r * 0.1], 190, 260, fill=(255, 255, 255), width=max(4, int(14 * s)))
    d.text((cx, cy + r * 0.05), "AI", font=F(int(r * 0.8)), fill=(255, 255, 255), anchor="mm", stroke_width=max(3, int(8 * s)), stroke_fill=(40, 60, 140))
    tx, ty = cx + r * 0.72, cy - r * 0.72                                       # кончик иглы касается пузыря сверху-справа
    ex, ey = cx + r * 1.55, cy - r * 1.45
    d.line([(ex, ey), (tx, ty)], fill=(215, 220, 230), width=max(5, int(12 * s)))
    d.ellipse([ex - r * 0.1, ey - r * 0.1, ex + r * 0.1, ey + r * 0.1], fill=(214, 40, 40), outline=(17, 17, 17), width=max(2, int(4 * s)))
    for k in range(5):                                                          # «искры» в точке прокола
        import math
        a_ = -2.4 + k * 0.5
        d.line([(tx + math.cos(a_) * r * 0.12, ty + math.sin(a_) * r * 0.12), (tx + math.cos(a_) * r * 0.28, ty + math.sin(a_) * r * 0.28)], fill=(255, 230, 90), width=max(3, int(7 * s)))

def wolf_holds_bill(d, cx, cy, s=1.0, text="$100", mood="smirk", glasses="down"):
    """Волк анфас держит купюру двумя лапами перед собой (отсылка к «показывает купюру в камеру»)."""
    import doodle as D
    wolf_portrait(d, cx, cy, s, mood=mood, glasses=glasses)
    INK, GREY, SUIT = (17, 17, 17), (128, 132, 140), (34, 44, 74)
    P = lambda x, y: (cx + x * s, cy + y * s)
    lw = max(4, int(9 * s))
    bw, bh = 470, 210
    x0, y0 = cx - bw / 2 * s, cy + 290 * s
    SLEEVE, CUFF = (62, 76, 124), (245, 245, 245)
    for k in (-1, 1):                                   # рукава (под купюрой): от низа кадра к лапам, светлее пиджака
        px = k * (bw / 2 + 8)
        W.shape(d, [P(k * 470, 1000), P(k * 200, 1000), P(px - k * 62, 470), P(px + k * 70, 470)], SLEEVE, lw, seed=240 + k)
        d.line([P(k * 340, 1000), P(px + k * 10, 490)], fill=(88, 104, 160), width=max(3, int(10 * s)))   # блик на рукаве
        W.shape(d, [P(px - k * 66, 445), P(px + k * 72, 445), P(px + k * 74, 492), P(px - k * 66, 492)], CUFF, lw, seed=246 + k)
    W.shape(d, [(x0, y0), (x0 + bw * s, y0), (x0 + bw * s, y0 + bh * s), (x0, y0 + bh * s)], (196, 222, 176), lw, seed=245)   # купюра
    d.rectangle([x0 + 18 * s, y0 + 16 * s, x0 + (bw - 18) * s, y0 + (bh - 16) * s], outline=(70, 120, 70), width=max(2, int(4 * s)))
    d.ellipse([cx - 52 * s, y0 + 40 * s, cx + 52 * s, y0 + (bh - 40) * s], fill=(160, 196, 140), outline=(70, 120, 70), width=max(2, int(4 * s)))
    W.sheep(d, cx - 38 * s, y0 + 158 * s, 0.28 * s, 1.0, "calm", seed=5)                                                   # «портрет» на купюре — овца
    f = F(int(62 * s))
    for xx in (x0 + 118 * s, x0 + (bw - 118) * s):
        d.text((xx, y0 + bh / 2 * s), text, font=F(int(56 * s)), fill=(40, 90, 50), anchor="mm")
    for k in (-1, 1):                                   # лапы держат края (поверх купюры, не закрывая цифры)
        W.shape(d, W.wob(cx + k * (bw / 2 + 8) * s, cy + 400 * s, 40 * s, 58 * s, seed=243 + k), GREY, lw)
        for j in range(3):
            d.line([P(k * (bw / 2 - 18), 368 + j * 28), P(k * (bw / 2 + 14), 368 + j * 28)], fill=INK, width=max(2, int(5 * s)))
