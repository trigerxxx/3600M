"""Ключевой арт «3600: Don't Open the Door» в сочном стиле.
blender -b --factory-startup -P keyart.py -- <out.png> <res_x> <res_y> <samples>
"""
import math
import random
import sys

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
OUT = argv[0]
RX, RY, SAMPLES = int(argv[1]), int(argv[2]), int(argv[3])
random.seed(36)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene


# ---------- материалы ----------
def mat(name, color, rough=0.45, emit=None, strength=0.0, coat=0.0, sss=0.0, metal=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    b.inputs["Coat Weight"].default_value = coat
    if sss:
        b.inputs["Subsurface Weight"].default_value = sss
        b.inputs["Subsurface Radius"].default_value = (0.6, 0.8, 1.0)
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1)
        b.inputs["Emission Strength"].default_value = strength
    return m


def hexc(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    # sRGB -> linear
    f = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return (f(r), f(g), f(b))


def wood_mat(name, base):
    m = mat(name, base, 0.6)
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    wave = nt.nodes.new("ShaderNodeTexWave")
    wave.wave_type = "BANDS"
    wave.bands_direction = "Z"
    wave.inputs["Scale"].default_value = 3.0
    wave.inputs["Distortion"].default_value = 2.0
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (*[c * 0.55 for c in base], 1)
    ramp.color_ramp.elements[1].color = (*base, 1)
    nt.links.new(wave.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    return m


M = {
    "snow": mat("snow", hexc("#c9d9f2"), 0.6, sss=0.25, coat=0.05),
    "rock": mat("rock", hexc("#2b3550"), 0.8),
    "mount_snow": mat("mount_snow", hexc("#b9cdf0"), 0.5, sss=0.1),
    "wood": wood_mat("wood", hexc("#8a4f2a")),
    "wood_dark": wood_mat("wood_dark", hexc("#4a2a18")),
    "roof": mat("roof", hexc("#6b2a22"), 0.5),
    "window": mat("window", hexc("#ffb060"), 0.2, emit=hexc("#ff9a3a"), strength=18),
    "door": mat("door", hexc("#3b4f7a"), 0.3, coat=0.6),
    "frost": mat("frost", hexc("#cfe6ff"), 0.15, emit=hexc("#9fd0ff"), strength=1.5),
    "metal": mat("metal", hexc("#c9cfd8"), 0.25, metal=1.0),
    "beacon": mat("beacon", hexc("#ff2a1a"), 0.2, emit=hexc("#ff2a1a"), strength=40),
    "lamp": mat("lamp", hexc("#ffd27a"), 0.2, emit=hexc("#ffcc66"), strength=30),
    "skin": mat("skin", hexc("#ffcf8a"), 0.35, coat=0.5),
    "parka_o": mat("parka_o", hexc("#ff6a1a"), 0.4, coat=0.4),
    "parka_b": mat("parka_b", hexc("#1f6bff"), 0.4, coat=0.4),
    "parka_g": mat("parka_g", hexc("#19c26b"), 0.4, coat=0.4),
    "pants": mat("pants", hexc("#20283c"), 0.5),
    "fur": mat("fur", hexc("#f4efe6"), 0.9, sss=0.2),
    "black": mat("black", hexc("#0b0c10"), 0.3, coat=0.8),
    "hair": mat("hair", hexc("#1c1410"), 0.4, coat=0.5),
    "guest": mat("guest", hexc("#020308"), 0.9),
    "eyes": mat("eyes", hexc("#bfe8ff"), 0.1, emit=hexc("#7fd4ff"), strength=60),
    "flash": mat("flash", hexc("#fff3c4"), 0.1, emit=hexc("#fff0b0"), strength=40),
    "red": mat("red", hexc("#d92b20"), 0.35, coat=0.6),
    "flake": mat("flake", hexc("#ffffff"), 0.2, emit=hexc("#dfefff"), strength=3),
}


# ---------- геометрия ----------
def obj_from(op, name, loc, scale=(1, 1, 1), rot=(0, 0, 0), material=None, bevel=0.0, **kw):
    op(location=loc, rotation=rot, **kw)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    if material:
        o.data.materials.append(material)
    if bevel:
        bpy.ops.object.transform_apply(scale=True)
        mod = o.modifiers.new("bevel", "BEVEL")
        mod.width = bevel
        mod.segments = 4
        mod.limit_method = "NONE"
    bpy.ops.object.shade_smooth() if bevel else None
    return o


def box(name, loc, size, material, rot=(0, 0, 0), bevel=0.0):
    return obj_from(bpy.ops.mesh.primitive_cube_add, name, loc, (size[0] / 2, size[1] / 2, size[2] / 2), rot, material, bevel)


def sphere(name, loc, r, material, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(location=loc, radius=r, segments=24, ring_count=16)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    o.data.materials.append(material)
    bpy.ops.object.shade_smooth()
    return o


def cyl(name, loc, r, h, material, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(location=loc, radius=r, depth=h, rotation=rot, vertices=24)
    o = bpy.context.object
    o.name = name
    o.data.materials.append(material)
    bpy.ops.object.shade_smooth()
    return o


# ---------- мир ----------
w = bpy.data.worlds.new("night")
w.use_nodes = True
nt = w.node_tree
bg = nt.nodes["Background"]
sky = nt.nodes.new("ShaderNodeTexGradient")
coord = nt.nodes.new("ShaderNodeTexCoord")
mapn = nt.nodes.new("ShaderNodeMapping")
mapn.inputs["Rotation"].default_value = (0, math.radians(-90), 0)
ramp = nt.nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].color = (*hexc("#2a4a9a"), 1)
ramp.color_ramp.elements[1].color = (*hexc("#070b1c"), 1)
ramp.color_ramp.elements[0].position = 0.45
nt.links.new(coord.outputs["Generated"], mapn.inputs["Vector"])
nt.links.new(mapn.outputs["Vector"], sky.inputs["Vector"])
nt.links.new(sky.outputs["Fac"], ramp.inputs["Fac"])
nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
bg.inputs["Strength"].default_value = 0.6
sc.world = w

# земля из снега с холмиками
bpy.ops.mesh.primitive_plane_add(size=160, location=(0, 20, 0))
ground = bpy.context.object
ground.data.materials.append(M["snow"])
bpy.ops.object.modifier_add(type="SUBSURF")
ground.modifiers[-1].levels = 6
ground.modifiers[-1].render_levels = 6
ground.modifiers[-1].subdivision_type = "SIMPLE"
tex = bpy.data.textures.new("bumps", "CLOUDS")
tex.noise_scale = 2.5
disp = ground.modifiers.new("disp", "DISPLACE")
disp.texture = tex
disp.strength = 0.6
bpy.ops.object.shade_smooth()

# горы
for i, (x, y, h, r) in enumerate([(-38, 70, 34, 26), (-8, 90, 46, 32), (26, 78, 38, 26), (50, 95, 30, 22), (-60, 100, 28, 24)]):
    cone = obj_from(bpy.ops.mesh.primitive_cone_add, f"mount{i}", (x, y, h / 2 - 1), material=M["rock"], vertices=7, radius1=r, depth=h)
    cap = obj_from(bpy.ops.mesh.primitive_cone_add, f"cap{i}", (x, y, h - h * 0.22 - 1), material=M["mount_snow"], vertices=7, radius1=r * 0.45, depth=h * 0.45)

# ---------- станция ----------
st = Vector((0, 6, 0))
box("cabin", st + Vector((0, 0, 3)), (12, 8, 6), M["wood"], bevel=0.12)
# двускатная крыша
for side in (-1, 1):
    box(f"roof{side}", st + Vector((side * 3.3, 0, 7.3)), (7.6, 9.4, 0.5), M["roof"], rot=(0, math.radians(side * 33), 0), bevel=0.1)
    box(f"roofsnow{side}", st + Vector((side * 3.25, 0, 7.75)), (7.4, 9.6, 0.45), M["snow"], rot=(0, math.radians(side * 33), 0), bevel=0.2)
box("gable", st + Vector((0, -3.9, 7.0)), (8, 0.3, 2.2), M["wood_dark"], bevel=0.05)
box("chimney", st + Vector((3.5, 1, 8.8)), (1.2, 1.2, 3), M["rock"], bevel=0.08)
box("chimneysnow", st + Vector((3.5, 1, 10.35)), (1.5, 1.5, 0.35), M["snow"], bevel=0.12)
# окна
for x in (-3.8, 3.8):
    box(f"winframe{x}", st + Vector((x, -4.05, 3.4)), (2.4, 0.3, 2.2), M["wood_dark"], bevel=0.06)
    box(f"win{x}", st + Vector((x, -4.15, 3.4)), (1.9, 0.2, 1.7), M["window"])
    box(f"winsill{x}", st + Vector((x, -4.35, 2.2)), (2.7, 0.6, 0.3), M["snow"], bevel=0.12)
    bpy.ops.object.light_add(type="AREA", location=st + Vector((x, -4.9, 3.4)), rotation=(math.radians(-90), 0, 0))
    l = bpy.context.object
    l.data.energy = 900
    l.data.size = 2.0
    l.data.color = hexc("#ff9a3a")
# дверь в инее
box("door", st + Vector((0, -4.1, 2.3)), (2.2, 0.3, 4.4), M["door"], bevel=0.08)
box("doorframe", st + Vector((0, -4.0, 2.4)), (2.8, 0.25, 4.9), M["wood_dark"], bevel=0.06)
for i in range(9):
    sphere(f"frost{i}", st + Vector((random.uniform(-1, 1), -4.28, random.uniform(0.3, 4.3))), random.uniform(0.08, 0.2), M["frost"], (1, 0.3, 1))
cyl("doorknob", st + Vector((0.8, -4.3, 2.2)), 0.12, 0.2, M["metal"], rot=(math.radians(90), 0, 0))
# лампа над дверью
sphere("doorlamp", st + Vector((0, -4.5, 5.3)), 0.35, M["lamp"])
bpy.ops.object.light_add(type="POINT", location=st + Vector((0, -5.2, 5.2)))
bpy.context.object.data.energy = 600
bpy.context.object.data.color = hexc("#ffc060")
bpy.context.object.data.shadow_soft_size = 0.4

# метеомачта с красным маячком
cyl("mast", st + Vector((-9, -1, 6)), 0.15, 12, M["metal"])
box("vane", st + Vector((-9, -1, 11.8)), (2.2, 0.15, 0.15), M["red"], bevel=0.04)
sphere("beacon", st + Vector((-9, -1, 12.3)), 0.3, M["beacon"])
bpy.ops.object.light_add(type="POINT", location=st + Vector((-9, -1.6, 12.3)))
bpy.context.object.data.energy = 1500
bpy.context.object.data.color = hexc("#ff2a1a")
box("instrument", st + Vector((-9, -1, 2.6)), (1.4, 1.0, 1.6), M["metal"], bevel=0.1)


# ---------- персонажи в стиле блочных аватаров ----------
def avatar(name, base, parka, pose=0.0, face="scared", rotz=0.0, flashlight=False, hood=True):
    root = bpy.data.objects.new(name, None)
    sc.collection.objects.link(root)
    parts = []
    parts.append(box(name + "_legL", base + Vector((-0.45, 0, 1.0)), (0.85, 0.9, 2.0), M["pants"], bevel=0.12))
    parts.append(box(name + "_legR", base + Vector((0.45, 0, 1.0)), (0.85, 0.9, 2.0), M["pants"], bevel=0.12))
    parts.append(box(name + "_bootL", base + Vector((-0.45, -0.1, 0.2)), (0.95, 1.1, 0.45), M["black"], bevel=0.12))
    parts.append(box(name + "_bootR", base + Vector((0.45, -0.1, 0.2)), (0.95, 1.1, 0.45), M["black"], bevel=0.12))
    parts.append(box(name + "_torso", base + Vector((0, 0, 3.0)), (2.0, 1.1, 2.0), parka, bevel=0.18))
    parts.append(box(name + "_zip", base + Vector((0, -0.57, 3.0)), (0.12, 0.05, 1.8), M["metal"]))
    aL = box(name + "_armL", base + Vector((-1.45, 0, 3.0)), (0.85, 0.95, 2.0), parka, rot=(math.radians(-pose * 0.6), 0, 0), bevel=0.16)
    aR = box(name + "_armR", base + Vector((1.45, 0, 3.0)), (0.85, 0.95, 2.0), parka, rot=(math.radians(-pose), 0, math.radians(-8)), bevel=0.16)
    parts += [aL, aR]
    head = box(name + "_head", base + Vector((0, 0, 4.75)), (1.25, 1.2, 1.2), M["skin"], bevel=0.3)
    parts.append(head)
    # лицо
    for dx in (-0.25, 0.25):
        parts.append(sphere(name + f"_eye{dx}", base + Vector((dx, -0.58, 4.9)), 0.11 if face == "scared" else 0.09, M["black"], (1, 0.5, 1.25)))
        parts.append(sphere(name + f"_hl{dx}", base + Vector((dx + 0.03, -0.64, 4.95)), 0.035, M["flake"]))
    if face == "scared":
        parts.append(sphere(name + "_mouth", base + Vector((0, -0.6, 4.45)), 0.14, M["black"], (1, 0.4, 1.3)))
    else:
        bpy.ops.mesh.primitive_torus_add(location=base + Vector((0, -0.6, 4.55)), major_radius=0.22, minor_radius=0.05, rotation=(math.radians(90), 0, 0))
        mth = bpy.context.object
        mth.data.materials.append(M["black"])
        parts.append(mth)
    if hood:
        parts.append(box(name + "_hood", base + Vector((0, 0.12, 5.0)), (1.55, 1.25, 1.55), parka, bevel=0.35))
        bpy.ops.mesh.primitive_torus_add(location=base + Vector((0, -0.55, 4.8)), major_radius=0.82, minor_radius=0.2, rotation=(math.radians(90), 0, 0))
        fur = bpy.context.object
        fur.data.materials.append(M["fur"])
        bpy.ops.object.shade_smooth()
        parts.append(fur)
    else:
        parts.append(box(name + "_hair", base + Vector((0, 0.1, 5.45)), (1.35, 1.25, 0.45), M["hair"], bevel=0.15))
        for k in range(5):
            parts.append(box(name + f"_spike{k}", base + Vector((-0.5 + k * 0.25, 0.1, 5.75)), (0.3, 0.9, 0.5), M["hair"], rot=(0, math.radians(random.uniform(-25, 25)), 0), bevel=0.08))
    if flashlight:
        parts.append(cyl(name + "_torch", base + Vector((1.5, -1.0, 3.9)), 0.18, 0.9, M["black"], rot=(math.radians(80), 0, 0)))
        parts.append(sphere(name + "_lens", base + Vector((1.5, -1.45, 3.98)), 0.17, M["flash"], (1, 0.3, 1)))
    for p in parts:
        p.parent = root
    root.rotation_euler = (0, 0, math.radians(rotz))
    return root


avatar("hero", Vector((0.2, -6.5, 0)), M["parka_o"], pose=55, face="scared", rotz=8, flashlight=True)
avatar("friendL", Vector((-3.4, -3.6, 0)), M["parka_b"], pose=20, face="scared", rotz=-20, hood=False)
avatar("friendR", Vector((3.6, -3.2, 0)), M["parka_g"], pose=-10, face="smile", rotz=25)

# фонарик: луч на дверь
bpy.ops.object.light_add(type="SPOT", location=(1.7, -7.7, 3.95))
spot = bpy.context.object
spot.data.energy = 3500
spot.data.spot_size = math.radians(22)
spot.data.spot_blend = 0.4
spot.data.color = hexc("#fff0c0")
d = (st + Vector((0, -4.2, 3.0))) - spot.location
spot.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()

# Гость в дверях: чёрный силуэт со светящимися глазами
g = st + Vector((-2.6, -4.8, 0))
for nm, loc, size in [("g_body", (0, 0, 3.6), (1.3, 0.8, 4.2)), ("g_legL", (-0.35, 0, 0.9), (0.5, 0.6, 1.9)), ("g_legR", (0.35, 0, 0.9), (0.5, 0.6, 1.9)),
                      ("g_armL", (-0.95, 0, 3.0), (0.4, 0.5, 3.6)), ("g_armR", (0.95, 0, 3.0), (0.4, 0.5, 3.6)), ("g_head", (0, 0, 6.3), (1.0, 0.9, 1.3))]:
    box(nm, g + Vector(loc), size, M["guest"], bevel=0.12)
for dx in (-0.22, 0.22):
    sphere(f"g_eye{dx}", g + Vector((dx, -0.48, 6.4)), 0.11, M["eyes"], (1.3, 0.5, 0.8))
bpy.ops.object.light_add(type="POINT", location=g + Vector((0, -1.0, 6.3)))
bpy.context.object.data.energy = 400
bpy.context.object.data.color = hexc("#7fd4ff")

# снежинки
for i in range(260):
    p = Vector((random.uniform(-14, 14), random.uniform(-6, 14), random.uniform(0.3, 18)))
    sphere(f"flake{i}", p, random.uniform(0.03, 0.09), M["flake"])

# тёплый рисующий свет спереди и холодный контровой сзади
bpy.ops.object.light_add(type="AREA", location=(-7, -15, 8))
key = bpy.context.object
key.data.energy = 1800
key.data.size = 7
key.data.color = hexc("#ffb070")
key.rotation_euler = (Vector((0, -5, 3)) - key.location).to_track_quat("-Z", "Y").to_euler()
bpy.ops.object.light_add(type="AREA", location=(0, 1, 9))
rim = bpy.context.object
rim.data.energy = 2500
rim.data.size = 12
rim.data.color = hexc("#6fa8ff")
rim.rotation_euler = (Vector((0, -6, 3)) - rim.location).to_track_quat("-Z", "Y").to_euler()
# луна-контровой свет
bpy.ops.object.light_add(type="SUN", rotation=(math.radians(60), 0, math.radians(200)))
sun = bpy.context.object
sun.data.energy = 2.2
sun.data.color = hexc("#7fa8ff")
sun.data.angle = math.radians(2)
sphere("moon", (-22, 120, 52), 6, mat("moonm", hexc("#dfe8ff"), 0.5, emit=hexc("#cfe0ff"), strength=6))

# туман для объёмного света
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 10, 10))
fog = bpy.context.object
fog.scale = (60, 60, 22)
fm = bpy.data.materials.new("fog")
fm.use_nodes = True
fnt = fm.node_tree
fnt.nodes.remove(fnt.nodes["Principled BSDF"])
vol = fnt.nodes.new("ShaderNodeVolumePrincipled")
vol.inputs["Density"].default_value = 0.006
vol.inputs["Color"].default_value = (*hexc("#9db8ff"), 1)
fnt.links.new(vol.outputs["Volume"], fnt.nodes["Material Output"].inputs["Volume"])
fog.data.materials.append(fm)

# ---------- камера ----------
cam_data = bpy.data.cameras.new("cam")
cam_data.lens = 30
cam = bpy.data.objects.new("cam", cam_data)
sc.collection.objects.link(cam)
cam.location = (0.4, -19.5, 3.6)
tgt = Vector((0, 4, 6.4))
cam.rotation_euler = (tgt - cam.location).to_track_quat("-Z", "Y").to_euler()
sc.camera = cam

# ---------- рендер ----------
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = SAMPLES
sc.cycles.use_denoising = True
sc.cycles.max_bounces = 6
sc.cycles.volume_bounces = 1
sc.cycles.volume_step_rate = 4.0
sc.render.resolution_x, sc.render.resolution_y = RX, RY
sc.render.resolution_percentage = 100
sc.render.filepath = OUT
sc.view_settings.view_transform = "AgX"
try:
    sc.view_settings.look = "AgX - Punchy"
except TypeError:
    pass
sc.view_settings.exposure = 0.3
bpy.ops.render.render(write_still=True)
