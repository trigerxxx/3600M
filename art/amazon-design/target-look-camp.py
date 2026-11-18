"""Целевой вид игры «33 Days»: ночной лагерь у обломков самолёта в джунглях.
blender -b --factory-startup -P camp.py -- out.png res_x res_y samples
"""
import math
import random
import sys

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
OUT, RX, RY, SAMPLES = argv[0], int(argv[1]), int(argv[2]), int(argv[3])
random.seed(7)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene


def hexc(h):
    h = h.lstrip("#")
    f = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return tuple(f(int(h[i:i + 2], 16) / 255) for i in (0, 2, 4))


def mat(name, color, rough=0.55, emit=None, strength=0.0, coat=0.0, sss=0.0, metal=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*hexc(color), 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    b.inputs["Coat Weight"].default_value = coat
    if sss:
        b.inputs["Subsurface Weight"].default_value = sss
    if emit:
        b.inputs["Emission Color"].default_value = (*hexc(emit), 1)
        b.inputs["Emission Strength"].default_value = strength
    return m


M = {
    "ground": mat("ground", "#2c4a1c", 0.9),
    "dirt": mat("dirt", "#6b4a2a", 0.95),
    "trunk": mat("trunk", "#5a3a22", 0.8),
    "palm": mat("palm", "#2f9a3e", 0.55, sss=0.2),
    "leaf1": mat("leaf1", "#1f7a32", 0.6, sss=0.15),
    "leaf2": mat("leaf2", "#3fb24a", 0.6, sss=0.15),
    "leaf3": mat("leaf3", "#15602a", 0.6),
    "body": mat("body", "#efe9dd", 0.3, coat=0.7),
    "stripe": mat("stripe", "#ff6a1a", 0.35, coat=0.5),
    "glass": mat("glass", "#0e1a2a", 0.05, coat=1.0),
    "rock": mat("rock", "#5a5f66", 0.8),
    "log": mat("log", "#4a2c18", 0.8),
    "fire": mat("fire", "#ffb040", 0.3, emit="#ff7a1a", strength=40),
    "fire2": mat("fire2", "#fff0a0", 0.3, emit="#ffd060", strength=60),
    "skin": mat("skin", "#ffcf8a", 0.35, coat=0.4),
    "p_o": mat("p_o", "#ff6a1a", 0.45, coat=0.3),
    "p_b": mat("p_b", "#1f6bff", 0.45, coat=0.3),
    "p_g": mat("p_g", "#ffd23a", 0.45, coat=0.3),
    "pants": mat("pants", "#2a3346", 0.6),
    "black": mat("black", "#0b0c10", 0.3, coat=0.6),
    "hair": mat("hair", "#2a1a10", 0.5),
    "monster": mat("monster", "#071208", 0.9),
    "eyes": mat("eyes", "#bfffd0", 0.1, emit="#7fffb0", strength=80),
    "firefly": mat("firefly", "#e8ff9a", 0.2, emit="#d8ff70", strength=25),
    "flare": mat("flare", "#ff3a2a", 0.2, emit="#ff2a1a", strength=60),
    "lamp": mat("lamp", "#ffe08a", 0.2, emit="#ffd070", strength=35),
    "water": mat("water", "#0e5a5a", 0.05, coat=1.0),
    "tarp": mat("tarp", "#1fb8b0", 0.6),
}


def obj(op, name, loc, scale=(1, 1, 1), rot=(0, 0, 0), material=None, bevel=0.0, smooth=True, **kw):
    op(location=loc, rotation=rot, **kw)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    if material:
        o.data.materials.append(material)
    if bevel:
        bpy.ops.object.transform_apply(scale=True)
        m = o.modifiers.new("b", "BEVEL")
        m.width, m.segments, m.limit_method = bevel, 3, "NONE"
    if smooth:
        bpy.ops.object.shade_smooth()
    return o


def box(n, loc, size, m, rot=(0, 0, 0), bevel=0.0):
    return obj(bpy.ops.mesh.primitive_cube_add, n, loc, (size[0] / 2, size[1] / 2, size[2] / 2), rot, m, bevel)


def sph(n, loc, r, m, scale=(1, 1, 1), sub=2):
    o = obj(bpy.ops.mesh.primitive_ico_sphere_add, n, loc, scale, material=m, subdivisions=sub, radius=r)
    return o


def cyl(n, loc, r, h, m, rot=(0, 0, 0), verts=12):
    return obj(bpy.ops.mesh.primitive_cylinder_add, n, loc, rot=rot, material=m, radius=r, depth=h, vertices=verts)


# ---------- ночь ----------
w = bpy.data.worlds.new("night")
w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Color"].default_value = (*hexc("#0c1a3a"), 1)
w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.6
sc.world = w
bpy.ops.object.light_add(type="SUN", rotation=(math.radians(55), 0, math.radians(210)))
moon = bpy.context.object
moon.data.energy = 1.6
moon.data.color = hexc("#7fa8ff")

# ---------- земля, поляна, река ----------
obj(bpy.ops.mesh.primitive_plane_add, "ground", (0, 0, 0), (120, 120, 1), material=M["ground"], size=1, smooth=False)
obj(bpy.ops.mesh.primitive_cylinder_add, "clearing", (0, 2, 0.01), (1, 1, 1), material=M["dirt"], radius=9, depth=0.02, vertices=48)
obj(bpy.ops.mesh.primitive_plane_add, "river", (16, 14, 0.02), (6, 40, 1), rot=(0, 0, math.radians(18)), material=M["water"], size=1, smooth=False)

# ---------- деревья джунглей ----------
def palm(x, y, h):
    seg = 6
    for i in range(seg):
        t = i / seg
        cyl(f"pt{x}{y}{i}", (x + 0.25 * math.sin(t * 2), y, h * (i + 0.5) / seg), 0.35 - 0.12 * t, h / seg + 0.1, M["trunk"])
    top = Vector((x + 0.25 * math.sin(2), y, h))
    for k in range(7):
        a = k / 7 * math.tau
        leaf = obj(bpy.ops.mesh.primitive_cube_add, f"pl{x}{y}{k}", top + Vector((math.cos(a) * 1.6, math.sin(a) * 1.6, -0.5)),
                   (1.9, 0.45, 0.06), rot=(0, math.radians(28), a), material=M["palm"])


def bush_tree(x, y, h, r):
    cyl(f"bt{x}{y}", (x, y, h / 2), 0.4, h, M["trunk"])
    for k in range(4):
        sph(f"bc{x}{y}{k}", (x + random.uniform(-1, 1), y + random.uniform(-1, 1), h + random.uniform(-0.5, 1.2)),
            r * random.uniform(0.7, 1.0), random.choice([M["leaf1"], M["leaf2"], M["leaf3"]]))


for i in range(70):
    a = random.uniform(0, math.tau)
    d = random.uniform(11, 34)
    x, y = math.cos(a) * d, math.sin(a) * d + 4
    if y < -6 and abs(x) < 8:
        continue
    if random.random() < 0.45:
        palm(x, y, random.uniform(6, 10))
    else:
        bush_tree(x, y, random.uniform(3, 6), random.uniform(2.2, 3.5))
for i in range(60):
    a = random.uniform(0, math.tau)
    d = random.uniform(8.5, 14)
    x, y = math.cos(a) * d, math.sin(a) * d + 2
    if y < -5:
        continue
    sph(f"bush{i}", (x, y, 0.5), random.uniform(0.8, 1.5), random.choice([M["leaf1"], M["leaf2"], M["leaf3"]]), (1, 1, 0.7))

# ---------- обломки самолёта ----------
pl = Vector((4.5, 6, 0))
obj(bpy.ops.mesh.primitive_cylinder_add, "fus", pl + Vector((0, 0, 1.4)), (1.4, 1.4, 5.5), rot=(math.radians(90), math.radians(8), math.radians(-30)), material=M["body"], vertices=24)
box("stripe", pl + Vector((0.3, 0.1, 1.15)), (1.0, 10.6, 0.25), M["stripe"], rot=(0, 0, math.radians(-30)))
sph("nose", pl + Vector((-2.8, -4.8, 1.2)), 1.4, M["body"], (1, 1.6, 0.95))
for k in range(5):
    sph(f"win{k}", pl + Vector((-1.6 + k * 0.9, -2.5 + k * 1.55, 2.05)), 0.22, M["glass"], (1, 1, 0.8))
box("wing", pl + Vector((-3.5, 3.0, 0.35)), (7.5, 2.4, 0.22), M["body"], rot=(math.radians(-6), math.radians(12), math.radians(-30)), bevel=0.05)
# фара светит
sph("headlight", pl + Vector((-3.6, -6.0, 1.0)), 0.35, M["lamp"])
bpy.ops.object.light_add(type="SPOT", location=pl + Vector((-3.9, -6.6, 1.2)))
hl = bpy.context.object
hl.data.energy = 2500
hl.data.spot_size = math.radians(50)
hl.data.color = hexc("#ffe0a0")
hl.rotation_euler = (Vector((-6, -12, 0)) - hl.location).to_track_quat("-Z", "Y").to_euler()
# тент из брезента у самолёта
box("tarp", pl + Vector((-5.5, 1.0, 2.2)), (4.5, 3.5, 0.08), M["tarp"], rot=(math.radians(-12), 0, math.radians(-30)))
for dx, dy in ((-7.3, 0.4), (-4.0, -1.4)):
    cyl(f"pole{dx}", pl + Vector((dx, dy, 1.1)), 0.08, 2.2, M["trunk"])

# ---------- костёр ----------
fp = Vector((-1.5, -1.5, 0))
for k in range(8):
    a = k / 8 * math.tau
    sph(f"stone{k}", fp + Vector((math.cos(a) * 1.0, math.sin(a) * 1.0, 0.15)), 0.3, M["rock"], (1, 1, 0.7), sub=1)
for k in range(5):
    a = k / 5 * math.tau
    cyl(f"log{k}", fp + Vector((math.cos(a) * 0.35, math.sin(a) * 0.35, 0.35)), 0.12, 1.3, M["log"], rot=(math.radians(60), 0, a))
sph("flame", fp + Vector((0, 0, 0.75)), 0.45, M["fire"], (1, 1, 1.7))
sph("flame2", fp + Vector((0.05, 0.05, 0.85)), 0.25, M["fire2"], (1, 1, 1.8))
bpy.ops.object.light_add(type="POINT", location=fp + Vector((0, 0, 1.3)))
fl = bpy.context.object
fl.data.energy = 3200
fl.data.color = hexc("#ff8a2a")
fl.data.shadow_soft_size = 0.6
for i in range(18):
    sph(f"spark{i}", fp + Vector((random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5), random.uniform(1.6, 4.2))), 0.04, M["fire2"], sub=1)


# ---------- герои (блочные аватары) ----------
def avatar(n, base, parka, rotz, face=True, hood=False, torch=False):
    root = bpy.data.objects.new(n, None)
    sc.collection.objects.link(root)
    parts = [
        box(n + "lL", base + Vector((-0.28, 0, 0.6)), (0.5, 0.55, 1.2), M["pants"], bevel=0.08),
        box(n + "lR", base + Vector((0.28, 0, 0.6)), (0.5, 0.55, 1.2), M["pants"], bevel=0.08),
        box(n + "t", base + Vector((0, 0, 1.8)), (1.2, 0.65, 1.2), parka, bevel=0.12),
        box(n + "aL", base + Vector((-0.86, 0, 1.75)), (0.5, 0.55, 1.2), parka, bevel=0.1),
        box(n + "aR", base + Vector((0.86, -0.2, 1.95)), (0.5, 0.55, 1.2), parka, rot=(math.radians(-50), 0, 0), bevel=0.1),
        box(n + "h", base + Vector((0, 0, 2.85)), (0.78, 0.74, 0.74), M["skin"], bevel=0.18),
        box(n + "hair", base + Vector((0, 0.06, 3.27)), (0.84, 0.8, 0.22), M["hair"], bevel=0.08),
    ]
    for dx in (-0.16, 0.16):
        parts.append(sph(n + f"e{dx}", base + Vector((dx, -0.37, 2.92)), 0.065, M["black"], (1, 0.5, 1.2), sub=2))
    if torch:
        parts.append(cyl(n + "torch", base + Vector((0.9, -0.85, 2.4)), 0.07, 0.9, M["log"], rot=(math.radians(-40), 0, 0)))
        parts.append(sph(n + "tf", base + Vector((0.9, -1.15, 2.78)), 0.18, M["fire"], (1, 1, 1.5)))
        bpy.ops.object.light_add(type="POINT", location=base + Vector((0.9, -1.3, 3.0)))
        L = bpy.context.object
        L.data.energy = 300
        L.data.color = hexc("#ff9a3a")
        parts.append(L)
    for p in parts:
        p.parent = root
    root.rotation_euler = (0, 0, math.radians(rotz))
    root.location = (0, 0, 0)
    return root


avatar("hero", Vector((-4.6, -4.4, 0)), M["p_o"], -35, torch=True)
avatar("fr1", Vector((-2.4, 1.0, 0)), M["p_b"], 160)
avatar("fr2", Vector((1.8, -2.6, 0)), M["p_g"], 70)

# ---------- «Тот, что в листве» ----------
g = Vector((-9.5, 9.5, 0))
for k in range(16):
    sph(f"vine{k}", g + Vector((random.uniform(-0.8, 0.8), random.uniform(-0.4, 0.4), 0.6 + k * 0.42)), random.uniform(0.35, 0.6), M["monster"], (1, 0.7, 1.3), sub=1)
for side in (-1, 1):
    for k in range(6):
        sph(f"arm{side}{k}", g + Vector((side * (0.8 + k * 0.18), 0, 5.4 - k * 0.55)), 0.28, M["monster"], sub=1)
sph("head", g + Vector((0, 0, 7.2)), 0.85, M["monster"], (1, 0.9, 1.25), sub=2)
for dx in (-0.28, 0.28):
    sph(f"geye{dx}", g + Vector((dx, -0.72, 7.3)), 0.12, M["eyes"], (1.4, 0.5, 0.7))
bpy.ops.object.light_add(type="POINT", location=g + Vector((0, -1.3, 7.3)))
ge = bpy.context.object
ge.data.energy = 80
ge.data.color = hexc("#7fffb0")

# светлячки
for i in range(50):
    sph(f"ff{i}", (random.uniform(-14, 14), random.uniform(-4, 16), random.uniform(0.8, 6)), 0.05, M["firefly"], sub=1)

# сигнальная ракета в небе
sph("flareball", (12, 30, 22), 0.6, M["flare"])
bpy.ops.object.light_add(type="POINT", location=(12, 29, 22))
fr = bpy.context.object
fr.data.energy = 3000
fr.data.color = hexc("#ff3a2a")

# туман для глубины
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 6, 6))
fog = bpy.context.object
fog.scale = (80, 80, 14)
fm = bpy.data.materials.new("fog")
fm.use_nodes = True
nt = fm.node_tree
nt.nodes.remove(nt.nodes["Principled BSDF"])
vol = nt.nodes.new("ShaderNodeVolumePrincipled")
vol.inputs["Density"].default_value = 0.008
vol.inputs["Color"].default_value = (*hexc("#7fa8c8"), 1)
nt.links.new(vol.outputs["Volume"], nt.nodes["Material Output"].inputs["Volume"])
fog.data.materials.append(fm)

# ---------- камера: вид игрока сзади-сверху ----------
cd = bpy.data.cameras.new("cam")
cd.lens = 28
cam = bpy.data.objects.new("cam", cd)
sc.collection.objects.link(cam)
cam.location = (1.0, -15.5, 7.0)
cam.rotation_euler = (Vector((-1.5, 3.0, 2.0)) - cam.location).to_track_quat("-Z", "Y").to_euler()
sc.camera = cam

sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = SAMPLES
sc.cycles.use_denoising = True
sc.cycles.max_bounces = 5
sc.cycles.volume_bounces = 1
sc.cycles.volume_step_rate = 3.0
sc.render.resolution_x, sc.render.resolution_y = RX, RY
sc.render.resolution_percentage = 100
sc.view_settings.view_transform = "AgX"
try:
    sc.view_settings.look = "AgX - Punchy"
except TypeError:
    pass
sc.view_settings.exposure = 0.6
sc.render.filepath = OUT
bpy.ops.render.render(write_still=True)
