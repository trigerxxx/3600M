"""Shorts 9:16 из длинного ролика: те же сцены, озвучка и звук, вертикальный кадр, крючок сверху, концовка «полная история»."""
import os
import subprocess
import sys
from multiprocessing import Pool

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import render
import scenes

render.W, render.H = 1080, 1920
W, H = render.W, render.H
SB = os.path.join(render.HERE, "build_shorts")
os.makedirs(SB, exist_ok=True)

SHORTS = {
    "short1-day52": (["c3", "c4", "f1", "f3", "m1", "m2", "m3", "m5"], "HE COUNTED 44 DAYS\nON EVEREST"),
    "short2-tear": (["t1", "t2", "t3", "t4", "t5", "t6"], "DAY 41. MINUS 40.\nTHE TENT RIPS."),
    "short3-shadow": (["d3", "d3b"], "SOMEONE WAS OUTSIDE\nHIS TENT. AT 8,000 M."),
}
# широкие сцены (текст/предметы во всю ширину) — показываем целиком поверх размытого фона
FIT = {"tracker", "rule", "news", "card", "deathzone", "descent", "end"}
# куда смотреть в вертикальном кадре (0..1 по ширине)
CX = {"tent_int": 0.62, "hands": 0.6, "tent_ledge": 0.47, "dawn": 0.84, "storm_coming": 0.6, "storm": 0.54,
      "flask": 0.5, "tear": 0.4, "night_ext": 0.36, "summit_clear": 0.45, "basecamp": 0.6, "tent_door": 0.5}

_bg_cache = {}


def frame_from(still, z, cx, cy, sx, sy, scene=None):
    if scene in FIT:
        key = id(still)
        if key not in _bg_cache:
            k = H / scenes.BH
            bg = still.resize((int(scenes.BW * k), H)).crop((int((scenes.BW * k - W) / 2), 0, int((scenes.BW * k - W) / 2) + W, H))
            bg = bg.filter(ImageFilter.GaussianBlur(40))
            _bg_cache[key] = Image.fromarray((np.asarray(bg) * 0.45).astype(np.uint8))
        out = _bg_cache[key].copy()
        fw, fh = W, int(W * scenes.BH / scenes.BW)
        vw, vh = scenes.BW / z, scenes.BH / z
        left = (scenes.BW - vw) / 2 + sx
        top = (scenes.BH - vh) / 2 + sy
        k = vw / fw
        fg = still.transform((fw, fh), Image.AFFINE, (k, 0, left, 0, k, top), resample=Image.BILINEAR)
        out.paste(fg, (0, (H - fh) // 2))
        return out
    cx = (0.27 if CURRENT.get("shadow") else CX.get(scene, cx)) + (cx - 0.5) * 0.5
    vh = scenes.BH / z
    vw = vh * W / H
    left = min(max(cx * scenes.BW - vw / 2, 0), scenes.BW - vw) + sx
    top = min(max(cy * scenes.BH - vh / 2, 0), scenes.BH - vh) + sy
    k = vw / W
    return still.transform((W, H), Image.AFFINE, (k, 0, left, 0, k, top), resample=Image.BILINEAR)


SUBF = ImageFont.truetype(scenes.F_BLACK, 64)


def sub_overlay(text):
    words, lines, cur = text.upper().split(), [], ""
    for w in words:
        if SUBF.getlength(cur + " " + w) > 900 and cur:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    lh = 80
    im = Image.new("RGBA", (W, lh * len(lines) + 30 + 480), (0, 0, 0, 0))   # +480: поднимаем над кнопками Shorts
    d = ImageDraw.Draw(im)
    for i, ln in enumerate(lines):
        d.text(((W - SUBF.getlength(ln)) / 2, 10 + i * lh), ln, font=SUBF, fill=(255, 255, 255, 255),
               stroke_width=8, stroke_fill=(0, 0, 0, 255))
    return im


HOOKF = ImageFont.truetype(scenes.F_BLACK, 76)


def hook_overlay(text, color=(255, 214, 150)):
    lines = text.split("\n")
    im = Image.new("RGBA", (W, 100 * len(lines) + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, ln in enumerate(lines):
        d.text(((W - HOOKF.getlength(ln)) / 2, 20 + i * 100), ln, font=HOOKF, fill=color + (255,),
               stroke_width=9, stroke_fill=(0, 0, 0, 255))
    return im


# подменяем функции длинного ролика на вертикальные
_orig_render_segment = render.render_segment


def patched_frame_from(still, z, cx, cy, sx, sy):
    return frame_from(still, z, cx, cy, sx, sy, scene=CURRENT["scene"])


CURRENT = {"scene": None}
render.frame_from = patched_frame_from
render.sub_overlay = sub_overlay

# крючок и концовка рисуются поверх через подмену Image.paste-точки субтитров: проще — дорисовать в отдельном проходе
_orig_fromarray = Image.fromarray
OVER = {"items": []}


def render_seg(args):
    idx, e, total, hook, last = args
    CURRENT["scene"] = e["scene"]
    CURRENT["shadow"] = e["p"].get("shadow")
    render.B = SB
    e = dict(e)
    if hook:
        e["subs"] = list(e["subs"])
    out = _orig_render_segment((idx, e, total))
    # поверх: крючок в первой части, «полная история» в последней
    if hook or last:
        ov = hook_overlay(hook) if hook else hook_overlay("FULL STORY\nON MY CHANNEL", (255, 255, 255))
        tmp = out[:-4] + "_ov.png"
        ov.save(tmp)
        y = 190 if hook else 300
        dst = out[:-4] + "_o.mp4"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", out, "-i", tmp, "-filter_complex",
                        f"[0][1]overlay=0:{y}", "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", dst], check=True)
        os.replace(dst, out)
    return out


def build(name, ids, hook):
    render.B = os.path.join(render.HERE, "build")
    tl_all, _ = render.timeline()
    by = {e["id"]: e for e in tl_all}
    tl, clock = [], 0.0
    for k, i in enumerate(ids):
        e = dict(by[i])
        e["dur"] = e["dur"] - 0.9
        e["start"] = clock
        e["id"] = f"{name}_{i}"
        if e["cam"] == "still":
            e["cam"] = "push"
        clock += e["dur"]
        tl.append(e)
    end = dict(by["e2"], id=f"{name}_end", text=None, subs=[], dur=3.2, start=clock, sfx=[("boom", 0.1)], cam="push_slow")
    end.pop("wav", None)
    tl.append(end)
    clock += end["dur"]
    jobs = [(k + 1, e, len(tl) + 1, hook if k == 0 else None, k == len(tl) - 1) for k, e in enumerate(tl)]
    with Pool(4) as pool:
        for v in pool.imap_unordered(render_seg, jobs):
            print("  ", os.path.basename(v), flush=True)
    render.B = os.path.join(render.HERE, "build")
    mix = render.build_audio(tl, clock)
    lst = f"{SB}/{name}.txt"
    open(lst, "w").write("".join(f"file 'v_{e['id']}.mp4'\n" for e in tl))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", f"{SB}/{name}_v.mp4"], check=True)
    out = f"{render.HERE}/{name}.mp4"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"{SB}/{name}_v.mp4", "-i", mix, "-c:v", "libx264", "-crf", "21",
                    "-maxrate", "10M", "-bufsize", "20M", "-pix_fmt", "yuv420p", "-af", "loudnorm=I=-14:TP=-1.5", "-c:a", "aac",
                    "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    print(name, f"{clock:.1f}s", out, flush=True)


if __name__ == "__main__":
    only = sys.argv[1:] or list(SHORTS)
    for n in only:
        build(n, *SHORTS[n])
