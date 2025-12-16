import bpy
import math
from mathutils import Vector

# =========================================================
# CONFIGURATION
# =========================================================

OUTPUT_PATH = "/tmp/pig_detailed.png"
RESOLUTION = 2048
CLEAR_SCENE = True

# =========================================================
# SCENE UTILITIES
# =========================================================

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def setup_scene():
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 300
    scene.render.resolution_x = RESOLUTION
    scene.render.resolution_y = RESOLUTION
    scene.render.film_transparent = True
    scene.view_settings.view_transform = 'Filmic'
    scene.view_settings.look = 'Medium High Contrast'

# =========================================================
# MATERIALS
# =========================================================

def pig_skin_material():
    mat = bpy.data.materials.new("PigSkin")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new("ShaderNodeOutputMaterial")
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    noise = nodes.new("ShaderNodeTexNoise")
    bump = nodes.new("ShaderNodeBump")

    noise.inputs["Scale"].default_value = 25
    noise.inputs["Detail"].default_value = 6
    bump.inputs["Strength"].default_value = 0.15

    bsdf.inputs["Base Color"].default_value = (0.84, 0.55, 0.55, 1)
    bsdf.inputs["Roughness"].default_value = 0.48
    # Blender 5.0 uses "Subsurface Weight" instead of "Subsurface"
    if "Subsurface Weight" in bsdf.inputs:
        bsdf.inputs["Subsurface Weight"].default_value = 0.28
    elif "Subsurface" in bsdf.inputs:
        bsdf.inputs["Subsurface"].default_value = 0.28
    # Subsurface color/radius also changed in Blender 4.0+
    if "Subsurface Radius" in bsdf.inputs:
        bsdf.inputs["Subsurface Radius"].default_value = (0.9, 0.6, 0.6)

    links.new(noise.outputs["Fac"], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])

    return mat

def simple_material(name, color, roughness=0.6):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Roughness"].default_value = roughness
    return mat

# =========================================================
# GEOMETRY HELPERS
# =========================================================

def sphere(name, scale, location):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(scale=True)
    return obj

def cylinder(name, radius, depth, location):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=location)
    obj = bpy.context.active_object
    obj.name = name
    return obj

# =========================================================
# CHARACTER BUILD
# =========================================================

def build_body(mat):
    body = sphere("Body", (1.45, 1.0, 0.95), (0, 0, 0))
    body.data.materials.append(mat)
    return body

def build_snout(mat):
    snout = sphere("Snout", (0.4, 0.35, 0.3), (1.35, 0, -0.15))
    snout.data.materials.append(mat)

    for y in (-0.08, 0.08):
        nostril = cylinder(
            "Nostril",
            radius=0.04,
            depth=0.05,
            location=(1.55, y, -0.15)
        )
        nostril.rotation_euler[1] = math.radians(90)
        nostril.data.materials.append(
            simple_material("NostrilDark", (0.25, 0.1, 0.1))
        )

    return snout

def build_eyes():
    eye_white = simple_material("EyeWhite", (1, 1, 1), 0.3)
    iris_mat = simple_material("Iris", (0.8, 0.55, 0.1), 0.4)
    cornea_mat = simple_material("Cornea", (1, 1, 1), 0.05)

    for side in (-1, 1):
        sclera = sphere("Eye", (0.12, 0.12, 0.12), (0.9, side * 0.25, 0.15))
        sclera.data.materials.append(eye_white)

        iris = sphere("Iris", (0.07, 0.07, 0.07), (0.97, side * 0.25, 0.15))
        iris.data.materials.append(iris_mat)

        cornea = sphere("Cornea", (0.125, 0.125, 0.125), (0.9, side * 0.25, 0.15))
        cornea.data.materials.append(cornea_mat)

def build_ears(mat):
    for side in (-1, 1):
        ear = sphere(
            "Ear",
            (0.28, 0.12, 0.4),
            (0.35, side * 0.6, 0.55)
        )
        ear.rotation_euler = (
            math.radians(25),
            math.radians(-15),
            math.radians(side * 10)
        )
        ear.data.materials.append(mat)

def build_legs(body_mat, hoof_mat):
    for x in (-0.65, 0.65):
        for y in (-0.4, 0.4):
            leg = cylinder("Leg", 0.13, 0.45, (x, y, -0.7))
            leg.data.materials.append(body_mat)

            hoof = cylinder("Hoof", 0.14, 0.12, (x, y, -0.95))
            hoof.data.materials.append(hoof_mat)

def build_laces(mat):
    bpy.ops.curve.primitive_bezier_curve_add(location=(0.15, 0, 0.55))
    lace = bpy.context.active_object
    lace.rotation_euler[1] = math.radians(90)
    lace.data.bevel_depth = 0.03
    lace.data.bevel_resolution = 6
    lace.data.materials.append(mat)

# =========================================================
# LIGHTING & CAMERA
# =========================================================

def setup_lighting():
    lights = [
        ("Key", (5, -4, 4), 1400),
        ("Fill", (-3, -3, 2.5), 500),
        ("Rim", (-5, 4, 5), 1200)
    ]

    for name, loc, power in lights:
        light = bpy.data.lights.new(name, type='AREA')
        light.energy = power
        obj = bpy.data.objects.new(name, light)
        bpy.context.collection.objects.link(obj)
        obj.location = loc

def setup_camera():
    bpy.ops.object.camera_add(location=(4.5, -4.5, 2.8))
    cam = bpy.context.active_object
    cam.data.lens = 50
    cam.rotation_euler = (
        math.radians(62),
        0,
        math.radians(45)
    )
    bpy.context.scene.camera = cam

# =========================================================
# RENDER
# =========================================================

def render():
    bpy.context.scene.render.filepath = OUTPUT_PATH
    bpy.ops.render.render(write_still=True)

# =========================================================
# MAIN
# =========================================================

def main():
    if CLEAR_SCENE:
        clear_scene()

    setup_scene()

    body_mat = pig_skin_material()
    hoof_mat = simple_material("Hoof", (0.2, 0.1, 0.1))
    lace_mat = simple_material("Laces", (0.95, 0.95, 0.95), 0.35)

    build_body(body_mat)
    build_snout(body_mat)
    build_eyes()
    build_ears(body_mat)
    build_legs(body_mat, hoof_mat)
    build_laces(lace_mat)

    setup_lighting()
    setup_camera()
    render()

if __name__ == "__main__":
    main()
