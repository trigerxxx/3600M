"""Крушение самолёта над Амазонией: вид спереди, пике, удар о кроны.
blender -b --factory-startup -P crash.py -- <outdir> <res_x> <res_y> <samples> [--still N]
"""
import math
import random
import sys

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
OUT, RX, RY, SAMPLES = argv[0], int(argv[1]), int(argv[2]), int(argv[3])
STILL = int(argv[argv.index("--still") + 1]) if "--still" in argv else None
random.seed(33)
FPS, FRAMES = 24, 120
IMPACT = 92  # кадр удара о кроны

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.fps = FPS
sc.frame_start, sc.frame_end = 1, FRAMES


def hexc(h):
    h = h.lstrip("#")
    f = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return tuple(f(int(h[i:i + 2], 16) / 255) for i in (0, 2, 4))


def mat(name, color, rough=0.5, emit=None, strength=0.0, metal=0.0, coat=0.0, alpha=1.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*hexc(color), 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    b.inputs["Coat Weight"].default_value = coat
    if emit:
        b.inputs["Emission Color"].default_value = (*hexc(emit), 1)
        b.inputs["Emission Strength"].default_value = strength
    if alpha < 1:
        b.inputs["Alpha"].default_value = alpha
    return m


M = {
    "body": mat("body", "#f4f1ea", 0.25, coat=0.8),
    "stripe": mat("stripe", "#ff6a1a", 0.3, coat=0.6),
    "glass": mat("glass", "#0e1a2a", 0.05, coat=1.0),
    "metal": mat("metal", "#9aa3ad", 0.3, metal=1.0),
    "fire": mat("fire", "#ffb040", 0.2, emit="#ff7a1a", strength=35),
    "smoke": mat("smoke", "#4a4a52", 0.9, alpha=0.7),
    "smoke_l": mat("smoke_l", "#8a8a92", 0.9, alpha=0.5),
    "ground": mat("ground", "#0f3d1e", 0.9),
    "river": mat("river", "#1fb8b0", 0.05, coat=1.0, emit="#0f6f80", strength=0.3),
    "flash": mat("flash", "#ffffff", 0.5, emit="#fff3e0", strength=0.0),
    "leaf": mat("leaf", "#46d06a", 0.6),
}
CANOPY = [mat(f"can{i}", c, 0.7) for i, c in enumerate(["#1e7a34", "#2a9a3e", "#17652b", "#3fb24a", "#0f5a2a", "#5ac24e"])]


def add(op, name, loc, scale=(1, 1, 1), rot=(0, 0, 0), material=None, smooth=True, **kw):
    op(location=loc, rotation=rot, **kw)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    if material:
        o.data.materials.append(material)
    if smooth:
        bpy.ops.object.shade_smooth()
    return o


# ---------- небо ----------
w = bpy.data.worlds.new("sunset")
w.use_nodes = True
nt = w.node_tree
bg = nt.nodes["Background"]
coord = nt.nodes.new("ShaderNodeTexCoord")
sep = nt.nodes.new("ShaderNodeSeparateXYZ")
ramp = nt.nodes.new("ShaderNodeValToRGB")
cr = ramp.color_ramp
cr.elements[0].position, cr.elements[0].color = 0.0, (*hexc("#ff9a4a"), 1)
cr.elements[1].position, cr.elements[1].color = 0.55, (*hexc("#3b2a6a"), 1)
e = cr.elements.new(0.18)
e.color = (*hexc("#ff5a5a"), 1)
nt.links.new(coord.outputs["Generated"], sep.inputs["Vector"])
nt.links.new(sep.outputs["Z"], ramp.inputs["Fac"])
nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
bg.inputs["Strength"].default_value = 1.4
sc.world = w

# солнце у горизонта
bpy.ops.object.light_add(type="SUN", rotation=(math.radians(84), 0, math.radians(165)))
sun = bpy.context.object
sun.data.energy = 6
sun.data.color = hexc("#ffb070")
sun.data.angle = math.radians(3)
add(bpy.ops.mesh.primitive_uv_sphere_add, "sundisk", (-60, 420, 18), (14, 14, 14),
    material=mat("sund", "#ffd27a", emit="#ffb060", strength=12))

# мягкий заполняющий свет со стороны камеры, чтобы джунгли не были чёрными
bpy.ops.object.light_add(type="SUN", rotation=(math.radians(60), 0, math.radians(10)))
fill = bpy.context.object
fill.data.energy = 1.2
fill.data.color = hexc("#ffc8a0")

# ---------- джунгли ----------
add(bpy.ops.mesh.primitive_plane_add, "ground", (0, 150, -1), (400, 400, 1), material=M["ground"], size=1)
# река
for i in range(40):
    y = 40 + i * 12
    x = 18 * math.sin(i * 0.35) - 30
    add(bpy.ops.mesh.primitive_plane_add, f"river{i}", (x, y, -0.6), (9, 7, 1), rot=(0, 0, math.radians(20 * math.cos(i * 0.35))), material=M["river"], size=1, smooth=False)
# кроны деревьев: много сфер разного размера и оттенка
for i in range(900):
    y = random.uniform(-15, 320)
    x = random.uniform(-90, 90) * (1 + y / 260)
    rx = 18 * math.sin(((y + 20) / 12) * 0.35) - 30
    if abs(x - rx) < 7:
        continue
    # поляна вокруг камеры и полоса, куда падает самолёт
    if (x + 1.2) ** 2 + (y + 13) ** 2 < 11 ** 2:
        continue
    r = random.uniform(2.0, 4.5)
    z = random.uniform(1.5, 4.5)
    o = add(bpy.ops.mesh.primitive_ico_sphere_add, f"tree{i}", (x, y, z), (1, 1, random.uniform(0.7, 0.95)),
            material=random.choice(CANOPY), subdivisions=2, radius=r)

# ---------- самолёт (частный бизнес-джет) ----------
plane = bpy.data.objects.new("plane", None)
sc.collection.objects.link(plane)
parts = []
parts.append(add(bpy.ops.mesh.primitive_cylinder_add, "fuselage", (0, 0, 0), (0.9, 0.9, 6.0), rot=(math.radians(90), 0, 0), material=M["body"], vertices=32))
parts.append(add(bpy.ops.mesh.primitive_uv_sphere_add, "nose", (0, -6.0, 0), (0.9, 2.2, 0.9), material=M["body"]))
parts.append(add(bpy.ops.mesh.primitive_uv_sphere_add, "cockpit", (0, -6.4, 0.45), (0.7, 1.1, 0.42), material=M["glass"]))
parts.append(add(bpy.ops.mesh.primitive_uv_sphere_add, "tailcone", (0, 6.0, 0.15), (0.75, 2.0, 0.7), material=M["body"]))
parts.append(add(bpy.ops.mesh.primitive_cube_add, "stripe", (0, 0, -0.1), (0.93, 6.2, 0.12), material=M["stripe"]))
for k in range(6):
    parts.append(add(bpy.ops.mesh.primitive_uv_sphere_add, f"win{k}", (0.86, -3.4 + k * 1.1, 0.35), (0.06, 0.28, 0.2), material=M["glass"]))
    parts.append(add(bpy.ops.mesh.primitive_uv_sphere_add, f"winL{k}", (-0.86, -3.4 + k * 1.1, 0.35), (0.06, 0.28, 0.2), material=M["glass"]))
wingL = add(bpy.ops.mesh.primitive_cube_add, "wingL", (-4.6, 0.6, -0.35), (4.0, 1.3, 0.12), rot=(0, math.radians(-4), math.radians(-14)), material=M["body"])
wingR = add(bpy.ops.mesh.primitive_cube_add, "wingR", (4.6, 0.6, -0.35), (4.0, 1.3, 0.12), rot=(0, math.radians(4), math.radians(14)), material=M["body"])
parts += [wingL]
for side in (-1, 1):
    parts.append(add(bpy.ops.mesh.primitive_cylinder_add, f"engine{side}", (side * 1.45, 4.3, 0.55), (0.45, 0.45, 1.3), rot=(math.radians(90), 0, 0), material=M["metal"], vertices=24))
parts.append(add(bpy.ops.mesh.primitive_cube_add, "fin", (0, 6.6, 1.8), (0.1, 1.2, 1.6), rot=(math.radians(-25), 0, 0), material=M["body"]))
parts.append(add(bpy.ops.mesh.primitive_cube_add, "stab", (0, 7.4, 3.25), (2.4, 0.7, 0.08), material=M["stripe"]))
# огонь в правом двигателе
fire = add(bpy.ops.mesh.primitive_uv_sphere_add, "fireball", (1.45, 5.7, 0.55), (0.55, 0.9, 0.55), material=M["fire"])
parts.append(fire)
bpy.ops.object.light_add(type="POINT", location=(1.45, 6.3, 0.9))
fl = bpy.context.object
fl.data.energy = 900
fl.data.color = hexc("#ff7a1a")
parts.append(fl)
for p in parts:
    p.parent = plane
wingR.parent = plane

# ---------- движение самолёта: пике прямо на камеру ----------
start, end = Vector((10, 170, 55)), Vector((0.5, 4, 7.5))
for f in range(1, FRAMES + 1):
    t = min(1.0, (f - 1) / (IMPACT - 1))
    te = t * t
    pos = start.lerp(end, te)
    if f > IMPACT:
        pos = end + Vector((0, -0.18 * (f - IMPACT), -0.25 * (f - IMPACT)))
    plane.location = pos
    dirv = (end - start).normalized()
    pitch = math.atan2(-dirv.z, -dirv.y)
    roll = math.radians(-8 - 14 * t + 3 * math.sin(f * 0.7))
    yaw = math.radians(math.pi * 0 + 6 * math.sin(f * 0.15))
    plane.rotation_euler = (pitch * 0.85, roll, yaw)
    plane.keyframe_insert("location", frame=f)
    plane.keyframe_insert("rotation_euler", frame=f)

# правое крыло отрывается в момент удара и летит к камере
bpy.context.view_layer.update()
wingR_world = wingR.matrix_world.copy()
for f in (1, IMPACT):
    wingR.keyframe_insert("location", frame=f)
    wingR.keyframe_insert("rotation_euler", frame=f)
wingR.location = wingR.location + Vector((4, -10, -1))
wingR.rotation_euler = (math.radians(70), math.radians(140), math.radians(40))
wingR.keyframe_insert("location", frame=IMPACT + 14)
wingR.keyframe_insert("rotation_euler", frame=IMPACT + 14)

# ---------- дымный след за горящим двигателем ----------
smoke_root = bpy.data.objects.new("smoke", None)
sc.collection.objects.link(smoke_root)
for i in range(70):
    f_emit = 1 + i * (IMPACT / 70)
    t = min(1.0, (f_emit - 1) / (IMPACT - 1))
    pos = start.lerp(end, t * t) + Vector((1.4, 6 + random.uniform(-0.3, 0.3), 0.5 + random.uniform(-0.3, 0.3)))
    s = add(bpy.ops.mesh.primitive_ico_sphere_add, f"puff{i}", pos, material=random.choice([M["smoke"], M["smoke_l"]]), subdivisions=2, radius=1.0)
    s.scale = (0.01, 0.01, 0.01)
    s.keyframe_insert("scale", frame=max(1, int(f_emit) - 1))
    s.scale = (1.2, 1.2, 1.2)
    s.keyframe_insert("scale", frame=int(f_emit) + 2)
    grow = random.uniform(2.2, 3.2)
    s.scale = (grow, grow, grow)
    s.location = pos + Vector((random.uniform(-1, 1), 3, 2.5))
    s.keyframe_insert("scale", frame=int(f_emit) + 40)
    s.keyframe_insert("location", frame=int(f_emit) + 40)

# листья, взлетающие при ударе
for i in range(80):
    l = add(bpy.ops.mesh.primitive_plane_add, f"leaf{i}", (random.uniform(-3, 3), random.uniform(5, 10), random.uniform(3, 5)),
            (0.25, 0.4, 1), material=M["leaf"], size=1, smooth=False)
    l.hide_render = True
    l.keyframe_insert("hide_render", frame=IMPACT - 1)
    l.hide_render = False
    l.keyframe_insert("hide_render", frame=IMPACT)
    l.keyframe_insert("location", frame=IMPACT)
    l.location = l.location + Vector((random.uniform(-10, 10), random.uniform(-14, -4), random.uniform(3, 9)))
    l.rotation_euler = (random.uniform(0, 6), random.uniform(0, 6), random.uniform(0, 6))
    l.keyframe_insert("location", frame=FRAMES)
    l.keyframe_insert("rotation_euler", frame=FRAMES)

# ---------- камера: впереди и ниже, смотрит на самолёт ----------
cam_data = bpy.data.cameras.new("cam")
cam_data.lens = 32
cam = bpy.data.objects.new("cam", cam_data)
sc.collection.objects.link(cam)
sc.camera = cam
base = Vector((-1.2, -13, 6.0))
for f in range(1, FRAMES + 1):
    shake = 0.02 * f if f < IMPACT else 0.9 * math.exp(-(f - IMPACT) / 10)
    cam.location = base + Vector((random.uniform(-1, 1) * shake * 0.15, 0, random.uniform(-1, 1) * shake * 0.15))
    target = plane.location if False else None
    t = min(1.0, (f - 1) / (IMPACT - 1))
    tgt = start.lerp(end, t * t) if f <= IMPACT else end
    tgt = tgt.lerp(Vector((0, 60, 9)), 0.35)
    cam.rotation_euler = (tgt - cam.location).to_track_quat("-Z", "Y").to_euler()
    cam.keyframe_insert("location", frame=f)
    cam.keyframe_insert("rotation_euler", frame=f)

# вспышка удара: светящаяся плоскость перед камерой
flash = add(bpy.ops.mesh.primitive_plane_add, "flash", (0, 0, 0), material=M["flash"], size=1, smooth=False)
flash.parent = cam
flash.location = (0, 0, -1.2)
flash.scale = (3, 2, 1)
fs = M["flash"].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
fa = M["flash"].node_tree.nodes["Principled BSDF"].inputs["Alpha"]
for f, strength, a in [(1, 0, 0), (IMPACT + 7, 0, 0), (IMPACT + 10, 30, 1), (FRAMES, 30, 1)]:
    fs.default_value = strength
    fa.default_value = a
    fs.keyframe_insert("default_value", frame=f)
    fa.keyframe_insert("default_value", frame=f)

# ---------- рендер ----------
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = SAMPLES
sc.cycles.use_denoising = True
sc.cycles.max_bounces = 4
sc.render.resolution_x, sc.render.resolution_y = RX, RY
sc.render.resolution_percentage = 100
sc.render.film_transparent = False
sc.view_settings.view_transform = "AgX"
try:
    sc.view_settings.look = "AgX - Punchy"
except TypeError:
    pass
sc.render.image_settings.file_format = "PNG"
if STILL:
    sc.frame_set(STILL)
    sc.render.filepath = f"{OUT}/still_{STILL:03d}.png"
    bpy.ops.render.render(write_still=True)
else:
    if "--range" in argv:
        i = argv.index("--range")
        sc.frame_start, sc.frame_end = int(argv[i + 1]), int(argv[i + 2])
    sc.render.filepath = f"{OUT}/f_"
    bpy.ops.render.render(animation=True)
