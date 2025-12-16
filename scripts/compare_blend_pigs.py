"""
Compare Downloaded Pig Models (BLEND files) Side-by-Side
Imports blend files, normalizes size, adds labels, renders comparison

Run with: ./blender.sh scripts/compare_blend_pigs.py
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
OUTPUT_FILE = os.path.join(PREVIEW_DIR, "pig_comparison_blends.png")

# Pig model paths (relative to MODELS_DIR)
PIG_MODELS = [
    ("lowpoly_pig.blend", "Lowpoly Pig"),
    ("porco.blend", "Porco"),
    ("Farm Animals by @Quaternius/Blends/Pig.blend", "Quaternius Pig"),
]

# Grid layout
SPACING = 3.5
TARGET_SIZE = 2.0

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def clear_scene():
    """Remove all objects from scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Clear orphan data
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)

def get_combined_bounds(objects):
    """Get combined bounding box for all mesh objects"""
    all_coords = []
    for obj in objects:
        if obj.type == 'MESH':
            for corner in obj.bound_box:
                world_corner = obj.matrix_world @ Vector(corner)
                all_coords.append(world_corner)

    if not all_coords:
        return None

    xs = [v.x for v in all_coords]
    ys = [v.y for v in all_coords]
    zs = [v.z for v in all_coords]

    return {
        'min': Vector((min(xs), min(ys), min(zs))),
        'max': Vector((max(xs), max(ys), max(zs))),
        'size': Vector((max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))),
        'center': Vector(((max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2, (max(zs) + min(zs)) / 2))
    }

def normalize_model(objects, target_size=2.0):
    """Scale objects to target size and center at origin"""
    bounds = get_combined_bounds(objects)
    if not bounds:
        return 1.0

    max_dim = max(bounds['size'].x, bounds['size'].y, bounds['size'].z)
    scale_factor = target_size / max_dim if max_dim > 0 else 1.0

    # Center and scale
    offset = -bounds['center']
    for obj in objects:
        obj.location += offset
        obj.scale *= scale_factor

    return scale_factor

def create_label(text, location):
    """Create 3D text label"""
    bpy.ops.object.text_add(location=location)
    label = bpy.context.active_object
    label.data.body = text
    label.data.size = 0.3
    label.data.align_x = 'CENTER'
    label.rotation_euler = (math.radians(90), 0, 0)

    # Add white material
    mat = bpy.data.materials.new(name=f"Label_{text}")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (1, 1, 1, 1)
    label.data.materials.append(mat)

    return label

# =============================================================================
# IMPORT FUNCTIONS
# =============================================================================

def import_blend(filepath, collection_name):
    """Import objects from a blend file"""
    # Track existing objects
    existing = set(bpy.data.objects)

    # Link all objects from the blend file
    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        data_to.objects = data_from.objects

    # Link imported objects to scene
    imported = []
    for obj in data_to.objects:
        if obj is not None:
            bpy.context.collection.objects.link(obj)
            imported.append(obj)

    return imported

def import_and_arrange_models():
    """Import all blend files and arrange in a row"""
    models = []

    for i, (rel_path, name) in enumerate(PIG_MODELS):
        filepath = os.path.join(MODELS_DIR, rel_path)

        if not os.path.exists(filepath):
            print(f"WARNING: File not found: {filepath}")
            continue

        print(f"Importing {i+1}/{len(PIG_MODELS)}: {name}")

        # Calculate position (horizontal row)
        x_pos = i * SPACING
        y_pos = 0

        # Import
        imported = import_blend(filepath, f"Pig_{i}")

        if not imported:
            print(f"  WARNING: No objects imported from {rel_path}")
            continue

        # Filter to mesh objects only
        mesh_objects = [obj for obj in imported if obj.type == 'MESH']

        if not mesh_objects:
            print(f"  WARNING: No mesh objects in {rel_path}")
            continue

        # Create parent empty
        parent = bpy.data.objects.new(f"Model_{i}_{name}", None)
        bpy.context.collection.objects.link(parent)

        for obj in mesh_objects:
            obj.parent = parent

        # Normalize size
        normalize_model(mesh_objects, TARGET_SIZE)

        # Update transforms
        bpy.context.view_layer.update()

        # Get new bounds after normalization
        bounds = get_combined_bounds(mesh_objects)
        if bounds:
            # Lift model so bottom is at z=0
            lift = -bounds['min'].z
            for obj in mesh_objects:
                obj.location.z += lift

        # Position
        parent.location = (x_pos, y_pos, 0)

        # Create label below
        create_label(name, (x_pos, y_pos - 1.8, -0.3))

        models.append({
            'name': name,
            'parent': parent,
            'objects': mesh_objects,
            'position': (x_pos, y_pos)
        })

        print(f"  Positioned at ({x_pos}, {y_pos}) with {len(mesh_objects)} meshes")

    return models

# =============================================================================
# SCENE SETUP
# =============================================================================

def setup_camera(num_models):
    """Setup camera to view all models"""
    # Center of row
    center_x = (num_models - 1) * SPACING / 2

    # Camera distance based on number of models
    distance = max(num_models * SPACING * 0.8, 6)

    bpy.ops.object.camera_add(location=(center_x, -distance, distance * 0.5))
    camera = bpy.context.active_object
    camera.name = "ComparisonCamera"
    camera.rotation_euler = (math.radians(65), 0, 0)
    bpy.context.scene.camera = camera

    # Adjust FOV
    camera.data.lens = 35

    return camera

def setup_lighting():
    """Setup lighting for comparison"""
    # Key light (sun)
    bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
    sun = bpy.context.active_object
    sun.name = "Sun"
    sun.data.energy = 3.0
    sun.rotation_euler = (math.radians(45), 0, math.radians(30))

    # Fill light
    bpy.ops.object.light_add(type='AREA', location=(-5, -3, 8))
    fill = bpy.context.active_object
    fill.name = "Fill"
    fill.data.energy = 300
    fill.data.size = 8

    return sun, fill

def setup_render(num_models):
    """Setup render settings"""
    scene = bpy.context.scene

    # Resolution - wider for more models
    scene.render.resolution_x = 600 * num_models
    scene.render.resolution_y = 600
    scene.render.resolution_percentage = 100

    # Use Cycles
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 64
    scene.cycles.use_denoising = True

    # Background - dark gray
    scene.world.use_nodes = True
    bg = scene.world.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (0.12, 0.12, 0.15, 1)

    # Output
    scene.render.filepath = OUTPUT_FILE
    scene.render.image_settings.file_format = 'PNG'

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("PIG COMPARISON - Importing BLEND files")
    print("=" * 70)

    # Clear scene
    clear_scene()

    # Import and arrange models
    models = import_and_arrange_models()
    num_models = len(models)

    if num_models == 0:
        print("ERROR: No models imported!")
        return

    print(f"\nSuccessfully imported {num_models} models")

    # Setup scene
    print("\nSetting up camera and lighting...")
    setup_camera(num_models)
    setup_lighting()
    setup_render(num_models)

    # Create output directory if needed
    os.makedirs(PREVIEW_DIR, exist_ok=True)

    # Render
    print(f"\nRendering comparison to {OUTPUT_FILE}...")
    bpy.ops.render.render(write_still=True)

    print("=" * 70)
    print(f"DONE! Comparison saved to:")
    print(f"  {OUTPUT_FILE}")
    print("=" * 70)

    # Print model list
    print("\nModels in comparison (left to right):")
    for i, m in enumerate(models):
        print(f"  {i+1}. {m['name']}")

if __name__ == "__main__":
    main()
