import random
from PIL import Image, ImageDraw, ImageFilter
import scenes as S
bg = S.render_still("storm_coming", dict(wall=1.0), seed=4).resize((1280, 720))
trk = S.render_still("tracker", dict(day="52", label="DAY", alarm_on=True), seed=2).crop((560, 120, 1740, 1200)).resize((560, 512))
m = Image.new("L", trk.size, 0); ImageDraw.Draw(m).rounded_rectangle((20, 40, 540, 500), 50, fill=255)
trk = trk.rotate(-7, expand=True, resample=Image.BICUBIC); m = m.rotate(-7, expand=True)
sh = Image.new("L", bg.size, 0); sh.paste(m, (700, 150)); sh = sh.filter(ImageFilter.GaussianBlur(30))
bg = Image.composite(Image.new("RGB", bg.size, (0, 0, 0)), bg, sh)
bg.paste(trk, (690, 120), m)
d = ImageDraw.Draw(bg)
f = S.font(S.F_BLACK, 150)
for i, (t, c) in enumerate([("44 DAYS", (255, 255, 255)), ("ALONE", (255, 214, 150))]):
    d.text((50, 120 + i * 155), t, font=f, fill=c, stroke_width=10, stroke_fill=(10, 8, 20))
d.rounded_rectangle((52, 470, 560, 560), 18, fill=(232, 48, 42))
d.text((78, 478), "...OR WAS IT?", font=S.font(S.F_BLACK, 66), fill=(255, 255, 255))
bg.save("thumbnail.png")
