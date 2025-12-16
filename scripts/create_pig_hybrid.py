"""
Create Pig Hybrid - Football-shaped pig character
Uses Quaternius pig as base, rotates forward, applies pink materials, adds football lacing

Run with: ./blender.sh scripts/create_pig_hybrid.py
"""

import bpy
import os
import math
from mathutils import Vector

# =============================================================================
# CONFIGURATION
# =============================================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
MODELS_DIR = os.path.join(REPO_ROOT, "models")
PREVIEW_DIR = os.path.join(REPO_ROOT, "previews")
OUTPUT_FILE = os.path.join(PREVIEW_DIR, "pig_hybrid_v005.png")
BLEND_OUTPUT = os.path.join(MODELS_DIR, "pig_hybrid.blend")

# Source model
SOURCE_MODEL = os.path.join(MODELS_DIR, "Farm Animals by @Quaternius/Blends/Pig.blend")

# Colors
PINK_BODY = (0.95, 0.6, 0.65, 1.0)  # Bright pink
PINK_SNOUT = (0.98, 0.7, 0.72, 1.0)  # Lighter pink for snout/belly
LACING_WHITE = (1.0, 1.0, 1.0, 1.0)  # White lacing
EYE_BLACK = (0.05, 0.05, 0.05, 1.0)
CHEEK_BLUSH = (0.95, 0.45, 0.5, 1.0)  # Rosy cheeks

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def clear_scene():
    """Remove all objects from scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)

def get_bounds(obj):
    """Get bounding box for an object"""
    coords = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    xs = [v.x for v in coords]
    ys = [v.y for v in coords]
    zs = [v.z for v in coords]
    return {
        'min': Vector((min(xs), min(ys), min(zs))),
        'max': Vector((max(xs), max(ys), max(zs))),
        'center': Vector(((max(xs)+min(xs))/2, (max(ys)+min(ys))/2, (max(zs)+min(zs))/2)),
        'size': Vector((max(xs)-min(xs), max(ys)-min(ys), max(zs)-min(zs)))
    }

def create_material(name, color, roughness=0.5, metallic=0.0):
    """Create a simple material with given color"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    return mat

# =============================================================================
# IMPORT AND TRANSFORM
# =============================================================================

def import_pig():
    """Import the Quaternius pig"""
    print(f"Importing pig from: {SOURCE_MODEL}")

    with bpy.data.libraries.load(SOURCE_MODEL, link=False) as (data_from, data_to):
        data_to.objects = data_from.objects

    pig_objects = []
    for obj in data_to.objects:
        if obj is not None:
            bpy.context.collection.objects.link(obj)
            pig_objects.append(obj)

    return pig_objects

def orient_pig_forward(objects):
    """Rotate pig for 3/4 front view showing face"""
    for obj in objects:
        if obj.type == 'MESH':
            # Rotate so snout faces toward camera (front-right diagonal)
            obj.rotation_euler.z += math.radians(225)  # 3/4 turn to face camera

    bpy.context.view_layer.update()

def center_pig(objects):
    """Center pig at origin with feet on ground"""
    mesh_objects = [o for o in objects if o.type == 'MESH']
    if not mesh_objects:
        return

    # Get combined bounds
    all_coords = []
    for obj in mesh_objects:
        for corner in obj.bound_box:
            all_coords.append(obj.matrix_world @ Vector(corner))

    xs = [v.x for v in all_coords]
    ys = [v.y for v in all_coords]
    zs = [v.z for v in all_coords]

    center_x = (max(xs) + min(xs)) / 2
    center_y = (max(ys) + min(ys)) / 2
    min_z = min(zs)

    # Move to center XY and lift to ground
    for obj in mesh_objects:
        obj.location.x -= center_x
        obj.location.y -= center_y
        obj.location.z -= min_z

def apply_pink_material(objects):
    """Apply bright pink material to pig"""
    pink_mat = create_material("Pig_Pink", PINK_BODY, roughness=0.6)

    for obj in objects:
        if obj.type == 'MESH':
            # Clear existing materials
            obj.data.materials.clear()
            obj.data.materials.append(pink_mat)

# =============================================================================
# ADD FOOTBALL LACING
# =============================================================================

def add_football_lacing(pig_objects):
    """Add white football lacing on the pig's back"""
    # Find the main pig body
    main_body = None
    for obj in pig_objects:
        if obj.type == 'MESH':
            bounds = get_bounds(obj)
            if bounds['size'].x > 0.3:  # Assume body is the largest mesh
                main_body = obj
                break

    if not main_body:
        print("WARNING: Could not find main body for lacing")
        return []

    bounds = get_bounds(main_body)
    center = bounds['center']
    top_z = bounds['max'].z

    # Create lacing material
    lacing_mat = create_material("Lacing_White", LACING_WHITE, roughness=0.3)

    lacing_objects = []

    # Main center seam (along the back)
    bpy.ops.mesh.primitive_cube_add(size=1)
    seam = bpy.context.active_object
    seam.name = "Lacing_Seam"
    seam.scale = (0.02, bounds['size'].y * 0.5, 0.015)
    seam.location = (center.x, center.y, top_z + 0.01)
    seam.data.materials.append(lacing_mat)
    lacing_objects.append(seam)

    # Cross stitches
    num_stitches = 5
    stitch_spacing = bounds['size'].y * 0.4 / num_stitches
    start_y = center.y - (num_stitches - 1) * stitch_spacing / 2

    for i in range(num_stitches):
        bpy.ops.mesh.primitive_cube_add(size=1)
        stitch = bpy.context.active_object
        stitch.name = f"Lacing_Stitch_{i}"
        stitch.scale = (0.08, 0.015, 0.012)
        stitch.location = (center.x, start_y + i * stitch_spacing, top_z + 0.015)
        stitch.data.materials.append(lacing_mat)
        lacing_objects.append(stitch)

    return lacing_objects

# =============================================================================
# ADD EXPRESSION ELEMENTS
# =============================================================================

def add_cheek_blush(pig_objects):
    """Add rosy cheek circles"""
    # Find head position (front part of pig)
    main_body = None
    for obj in pig_objects:
        if obj.type == 'MESH':
            main_body = obj
            break

    if not main_body:
        return []

    bounds = get_bounds(main_body)

    blush_mat = create_material("Cheek_Blush", CHEEK_BLUSH, roughness=0.8)

    cheeks = []
    # Approximate cheek positions (front of pig, sides)
    cheek_y = bounds['min'].y + bounds['size'].y * 0.2  # Front area
    cheek_z = bounds['center'].z + bounds['size'].z * 0.1
    cheek_offset_x = bounds['size'].x * 0.25

    for side in [-1, 1]:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.08, segments=16, ring_count=8)
        cheek = bpy.context.active_object
        cheek.name = f"Cheek_{'L' if side < 0 else 'R'}"
        cheek.location = (bounds['center'].x + side * cheek_offset_x, cheek_y - 0.05, cheek_z)
        cheek.scale = (1.0, 0.3, 0.8)  # Flatten against face
        cheek.data.materials.append(blush_mat)
        cheeks.append(cheek)

    return cheeks

def add_eyebrows(pig_objects):
    """Add expressive eyebrows"""
    main_body = None
    for obj in pig_objects:
        if obj.type == 'MESH':
            main_body = obj
            break

    if not main_body:
        return []

    bounds = get_bounds(main_body)

    brow_mat = create_material("Eyebrow_Dark", (0.15, 0.1, 0.1, 1.0), roughness=0.7)

    brows = []
    # Approximate eye/brow positions
    brow_y = bounds['min'].y + bounds['size'].y * 0.15
    brow_z = bounds['center'].z + bounds['size'].z * 0.25
    brow_offset_x = bounds['size'].x * 0.18

    for side in [-1, 1]:
        bpy.ops.mesh.primitive_cube_add(size=1)
        brow = bpy.context.active_object
        brow.name = f"Eyebrow_{'L' if side < 0 else 'R'}"
        brow.scale = (0.12, 0.02, 0.025)
        brow.location = (bounds['center'].x + side * brow_offset_x, brow_y - 0.02, brow_z)
        # Angle eyebrows for determined expression
        brow.rotation_euler = (0, 0, side * math.radians(15))
        brow.data.materials.append(brow_mat)
        brows.append(brow)

    return brows

# =============================================================================
# SCENE SETUP
# =============================================================================

def setup_camera():
    """Setup camera for hero shot"""
    # Position camera much further back for full pig view
    bpy.ops.object.camera_add(location=(8.0, -12.0, 6.0))
    camera = bpy.context.active_object
    camera.name = "MainCamera"

    # Point at pig center
    bpy.ops.object.empty_add(location=(0, 0, 1.5))
    target = bpy.context.active_object
    target.name = "CameraTarget"

    constraint = camera.constraints.new(type='TRACK_TO')
    constraint.target = target
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'

    bpy.context.scene.camera = camera
    camera.data.lens = 50

    return camera

def setup_lighting():
    """Setup 3-point lighting"""
    # Key light - sun for consistent lighting
    bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
    key = bpy.context.active_object
    key.name = "Key"
    key.data.energy = 3.0
    key.rotation_euler = (math.radians(50), 0, math.radians(30))

    # Fill light
    bpy.ops.object.light_add(type='AREA', location=(-5, -5, 5))
    fill = bpy.context.active_object
    fill.name = "Fill"
    fill.data.energy = 300
    fill.data.size = 5

    # Rim light
    bpy.ops.object.light_add(type='AREA', location=(0, 8, 5))
    rim = bpy.context.active_object
    rim.name = "Rim"
    rim.data.energy = 400
    rim.data.size = 4

    return key, fill, rim

def setup_render():
    """Setup render settings"""
    scene = bpy.context.scene

    scene.render.resolution_x = 1080
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100

    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 128
    scene.cycles.use_denoising = True

    # Light background
    scene.world.use_nodes = True
    bg = scene.world.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (0.85, 0.88, 0.92, 1)  # Light blue-gray

    scene.render.filepath = OUTPUT_FILE
    scene.render.image_settings.file_format = 'PNG'

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("PIG HYBRID - Creating Football Pig Character")
    print("=" * 70)

    # Clear scene
    clear_scene()

    # Import base pig
    print("\n1. Importing Quaternius pig...")
    pig_objects = import_pig()
    print(f"   Imported {len(pig_objects)} objects")

    # Orient and center
    print("\n2. Orienting pig to face forward...")
    orient_pig_forward(pig_objects)
    center_pig(pig_objects)

    # Apply pink material
    print("\n3. Applying pink material...")
    apply_pink_material(pig_objects)

    # Add football lacing
    print("\n4. Adding football lacing...")
    lacing = add_football_lacing(pig_objects)
    print(f"   Added {len(lacing)} lacing elements")

    # Add expression
    print("\n5. Adding expression elements...")
    cheeks = add_cheek_blush(pig_objects)
    brows = add_eyebrows(pig_objects)
    print(f"   Added {len(cheeks)} cheeks, {len(brows)} eyebrows")

    # Setup scene
    print("\n6. Setting up camera and lighting...")
    setup_camera()
    setup_lighting()
    setup_render()

    # Create output directory
    os.makedirs(PREVIEW_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(BLEND_OUTPUT), exist_ok=True)

    # Save blend file
    print(f"\n7. Saving blend file to {BLEND_OUTPUT}...")
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUTPUT)

    # Render
    print(f"\n8. Rendering to {OUTPUT_FILE}...")
    bpy.ops.render.render(write_still=True)

    print("\n" + "=" * 70)
    print("DONE! Pig hybrid created:")
    print(f"  Preview: {OUTPUT_FILE}")
    print(f"  Blend:   {BLEND_OUTPUT}")
    print("=" * 70)

if __name__ == "__main__":
    main()
