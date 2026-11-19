"""Эскизы героини криминального канала: немецкая овчарка-криминалист (агент Лиз).
Стиль как у Волка: белый фон, толстый контур, «кривые» линии. Ориентир для рисунка автора, не финальная графика."""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "sheep-standard", "sketches"))
from wolf import INK, line, shape, wob  # noqa: E402  общие «кривые» кисти

F = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
TAN, TAN_L, BLACK = (196, 132, 64), (226, 176, 112), (36, 30, 28)
COAT, COAT_D, BELT = (200, 168, 118), (168, 136, 90), (90, 64, 40)
GOLD, MUG = (236, 190, 70), (230, 230, 236)


def shepherd(d, cx, base, s=1.0, pose="stand"):
    jt = base - 470 * s                     # верх плаща
    # хвост
    shape(d, wob(cx - 120 * s, base - 200 * s, 85 * s, 30 * s, seed=3, rot=1.1), BLACK, 8)
    shape(d, wob(cx - 150 * s, base - 130 * s, 30 * s, 22 * s, seed=4), TAN, 6)
    # лапы
    for lx in (-1, 1):
        shape(d, [(cx + lx * 22 * s, base - 150 * s), (cx + lx * 58 * s, base - 150 * s), (cx + lx * 56 * s, base - 22 * s), (cx + lx * 24 * s, base - 22 * s)], TAN, 8, seed=5 + lx)
        shape(d, wob(cx + lx * 48 * s, base - 14 * s, 36 * s, 16 * s, seed=7 + lx), TAN_L, 6)
    # плащ
    shape(d, [(cx - 100 * s, jt + 40 * s), (cx + 100 * s, jt + 40 * s), (cx + 135 * s, base - 130 * s), (cx - 135 * s, base - 130 * s)], COAT, 9, seed=10)
    d.line((cx, jt + 80 * s, cx + 4 * s, base - 135 * s), fill=COAT_D, width=int(6 * s))
    shape(d, [(cx - 118 * s, jt + 230 * s), (cx + 118 * s, jt + 230 * s), (cx + 120 * s, jt + 262 * s), (cx - 120 * s, jt + 262 * s)], BELT, 6, seed=11)
    for lx in (-1, 1):   # лацканы и поднятый воротник
        shape(d, [(cx + lx * 20 * s, jt + 40 * s), (cx + lx * 100 * s, jt + 30 * s), (cx + lx * 80 * s, jt + 120 * s)], COAT_D, 7, seed=12 + lx)
    # значок на поясе
    shape(d, [(cx + 50 * s, jt + 220 * s), (cx + 82 * s, jt + 230 * s), (cx + 78 * s, jt + 275 * s), (cx + 60 * s, jt + 285 * s), (cx + 44 * s, jt + 270 * s)], GOLD, 6, seed=14)

    # руки и предметы
    def arm_down(lx):
        shape(d, [(cx + lx * 95 * s, jt + 50 * s), (cx + lx * 132 * s, jt + 70 * s), (cx + lx * 125 * s, jt + 240 * s), (cx + lx * 95 * s, jt + 236 * s)], COAT, 8, seed=20 + lx)
        shape(d, wob(cx + lx * 112 * s, jt + 256 * s, 22 * s, 20 * s, seed=22 + lx), TAN, 7)

    if pose == "stand":                       # кофе в лапе
        arm_down(-1)
        shape(d, [(cx + 95 * s, jt + 50 * s), (cx + 132 * s, jt + 60 * s), (cx + 190 * s, jt + 150 * s), (cx + 160 * s, jt + 170 * s)], COAT, 8, seed=24)
        shape(d, [(cx + 160 * s, jt + 90 * s), (cx + 220 * s, jt + 90 * s), (cx + 214 * s, jt + 170 * s), (cx + 166 * s, jt + 170 * s)], MUG, 7, seed=25)
        d.arc((cx + 205 * s, jt + 105 * s, cx + 245 * s, jt + 150 * s), 270, 90, fill=INK, width=int(7 * s))
        for k in range(3):
            line(d, (cx + 175 * s + k * 18 * s, jt + 80 * s), (cx + 182 * s + k * 18 * s, jt + 30 * s), 4, seed=26 + k)
        shape(d, wob(cx + 175 * s, jt + 160 * s, 22 * s, 20 * s, seed=27), TAN, 7)
    elif pose == "trail":                     # с лупой — «взяла след»
        arm_down(-1)
        shape(d, [(cx + 95 * s, jt + 50 * s), (cx + 290 * s, jt + 120 * s), (cx + 282 * s, jt + 160 * s), (cx + 90 * s, jt + 110 * s)], COAT, 8, seed=28)
        hx, hy = cx + 305 * s, jt + 140 * s
        shape(d, wob(hx, hy, 22 * s, 20 * s, seed=29), TAN, 7)
        line(d, (hx + 10 * s, hy - 10 * s), (hx + 70 * s, hy - 70 * s), int(14 * s), seed=30)
        d.ellipse((hx + 50 * s, hy - 170 * s, hx + 170 * s, hy - 50 * s), outline=INK, width=int(12 * s), fill=(220, 238, 250))
    elif pose == "weakness":                  # слабость: мячик
        arm_down(-1)
        arm_down(1)
        bx, by_ = cx + 330 * s, base - 60 * s
        d.ellipse((bx - 50 * s, by_ - 50 * s, bx + 50 * s, by_ + 50 * s), fill=(200, 230, 60), outline=INK, width=int(8 * s))
        d.arc((bx - 50 * s, by_ - 80 * s, bx + 20 * s, by_ + 40 * s), 300, 60, fill=(255, 255, 255), width=int(6 * s))

    # голова (в профиль вправо)
    hx, hy = cx + 10 * s, jt - 80 * s
    if pose == "trail":
        hx, hy = hx + 20 * s, hy + 20 * s
    for ex in (-1, 1):                        # большие стоячие уши
        ear = [(hx + ex * 45 * s - 34 * s, hy - 40 * s), (hx + ex * 45 * s - 4 * s, hy - 175 * s), (hx + ex * 45 * s + 34 * s, hy - 45 * s)]
        shape(d, ear, BLACK, 8, seed=40 + ex)
        inner = [(hx + ex * 45 * s - 16 * s, hy - 50 * s), (hx + ex * 45 * s - 4 * s, hy - 130 * s), (hx + ex * 45 * s + 14 * s, hy - 52 * s)]
        d.polygon(inner, fill=TAN_L)
    shape(d, wob(hx, hy, 92 * s, 86 * s, seed=44), TAN, 9)
    shape(d, wob(hx - 45 * s, hy - 35 * s, 46 * s, 40 * s, seed=45), BLACK, 0)   # тёмный окрас на затылке
    snout = [(hx + 30 * s, hy - 25 * s), (hx + 185 * s, hy + 5 * s), (hx + 190 * s, hy + 45 * s), (hx + 35 * s, hy + 62 * s)]
    shape(d, snout, TAN_L, 9, seed=46)
    d.polygon([(hx + 90 * s, hy - 15 * s), (hx + 185 * s, hy + 5 * s), (hx + 188 * s, hy + 25 * s), (hx + 95 * s, hy + 10 * s)], fill=BLACK)  # чёрная маска на морде
    shape(d, wob(hx + 188 * s, hy + 15 * s, 18 * s, 14 * s, seed=47), INK, 4)   # нос
    line(d, (hx + 90 * s, hy + 46 * s), (hx + 170 * s, hy + 40 * s), 6, seed=48)  # рот: никогда не улыбается
    ex_, ey_ = hx + 30 * s, hy - 15 * s
    big = pose == "weakness"
    er = (20 if big else 13) * s
    d.ellipse((ex_ - er, ey_ - er, ex_ + er, ey_ + er), fill=(255, 255, 255) if big else (120, 74, 34), outline=INK, width=5)
    pr = (10 if big else 5) * s
    off = (8 * s if big else 0)
    d.ellipse((ex_ - pr + off, ey_ - pr + off, ex_ + pr + off, ey_ + pr + off), fill=INK)
    if big:
        line(d, (ex_ - 22 * s, ey_ - 40 * s), (ex_ + 24 * s, ey_ - 46 * s), 6, seed=49)   # брови вверх
    else:
        line(d, (ex_ - 24 * s, ey_ - 24 * s), (ex_ + 24 * s, ey_ - 14 * s), 7, seed=50)   # нахмуренная бровь


def label(d, x, y, t, size=34, fill=INK):
    f = ImageFont.truetype(F, size)
    d.text((x - f.getlength(t) / 2, y), t, font=f, fill=fill)


def sheet():
    W, H = 2000, 1450
    im = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(im)
    label(d, W / 2, 40, "AGENT LIZ — GERMAN SHEPHERD, CRIMINALIST", 54)
    label(d, W / 2, 110, "sketches for the author's own drawing · not final art", 30, (120, 120, 120))
    for i, (p, name) in enumerate([("stand", "ON DUTY (coffee, never smiles)"), ("trail", "ON THE TRAIL"), ("weakness", "HER ONE WEAKNESS")]):
        cx = 300 + i * 640
        shepherd(d, cx, 1000, 0.95, p)
        label(d, cx + 60, 1040, name, 34)
    line(d, (80, 1120), (1920, 1120), 4, seed=1)
    label(d, W / 2, 1150, "TRENCH COAT · GOLD BADGE · BLACK SADDLE & TAN · HUGE EARS · SERIOUS BROW", 34)
    label(d, W / 2, 1210, "8 years on Ghost's trail. Smells lies. Can't ignore a tennis ball.", 34, (120, 120, 120))
    im.save("shepherd-sheet.png")


if __name__ == "__main__":
    sheet()
