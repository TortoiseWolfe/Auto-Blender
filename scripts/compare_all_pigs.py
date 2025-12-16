"""
Compare All Downloaded Pig Models Side-by-Side
Imports all GLB files from models/polypizza, normalizes size, adds labels, renders comparison

Run with: ./blender.sh scripts/compare_all_pigs.py
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
MODELS_DIR = os.path.join(REPO_ROOT, "models/polypizza")
PREVIEW_DIR = os.path.join(REPO_ROOT, "previews")
OUTPUT_FILE = os.path.join(PREVIEW_DIR, "all_pigs_comparison.png")

# Grid layout
MODELS_PER_ROW = 5
SPACING = 3.0
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
    """Scale objects to target size and center at origin, return scale factor"""
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
    label.data.size = 0.25
    label.data.align_x = 'CENTER'
    label.rotation_euler = (math.radians(90), 0, 0)

    # Add material
    mat = bpy.data.materials.new(name=f"Label_{text}")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (1, 1, 1, 1)
    label.data.materials.append(mat)

    return label

# =============================================================================
# IMPORT AND ARRANGE
# =============================================================================

def import_glb(filepath):
    """Import GLB file and return imported objects"""
    # Track existing objects
    existing = set(bpy.data.objects)

    # Import
    bpy.ops.import_scene.gltf(filepath=filepath)

    # Find new objects
    new_objects = [obj for obj in bpy.data.objects if obj not in existing]
    return new_objects

def import_and_arrange_models():
    """Import all GLB files and arrange in grid"""
    # Get list of GLB files
    glb_files = sorted([f for f in os.listdir(MODELS_DIR) if f.endswith('.glb')])

    print(f"Found {len(glb_files)} GLB files to import")

    models = []

    for i, filename in enumerate(glb_files):
        filepath = os.path.join(MODELS_DIR, filename)
        name = filename.replace('.glb', '').replace('_', ' ').title()

        print(f"Importing {i+1}/{len(glb_files)}: {name}")

        # Calculate grid position
        row = i // MODELS_PER_ROW
        col = i % MODELS_PER_ROW
        x_pos = col * SPACING
        y_pos = -row * SPACING

        # Import
        imported = import_glb(filepath)

        if not imported:
            print(f"  WARNING: No objects imported from {filename}")
            continue

        # Create parent empty
        parent = bpy.data.objects.new(f"Model_{i}", None)
        bpy.context.collection.objects.link(parent)

        for obj in imported:
            obj.parent = parent

        # Normalize size
        normalize_model(imported, TARGET_SIZE)

        # Update transforms
        bpy.context.view_layer.update()

        # Position
        parent.location = (x_pos, y_pos, 0)

        # Create label
        label_text = name[:20]  # Truncate long names
        create_label(label_text, (x_pos, y_pos - 1.8, -1.2))

        models.append({
            'name': name,
            'parent': parent,
            'objects': imported,
            'position': (x_pos, y_pos)
        })

        print(f"  Positioned at ({x_pos}, {y_pos})")

    return models

# =============================================================================
# SCENE SETUP
# =============================================================================

def setup_camera(num_models):
    """Setup camera to view all models"""
    rows = (num_models + MODELS_PER_ROW - 1) // MODELS_PER_ROW
    cols = min(num_models, MODELS_PER_ROW)

    # Center of grid
    center_x = (cols - 1) * SPACING / 2
    center_y = -(rows - 1) * SPACING / 2

    # Camera distance based on grid size
    distance = max(cols, rows) * SPACING * 1.2

    bpy.ops.object.camera_add(location=(center_x, center_y - distance, distance * 0.6))
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
    bpy.ops.object.light_add(type='SUN', location=(10, -10, 15))
    sun = bpy.context.active_object
    sun.name = "Sun"
    sun.data.energy = 3.0
    sun.rotation_euler = (math.radians(45), 0, math.radians(30))

    # Fill light
    bpy.ops.object.light_add(type='AREA', location=(-10, -5, 10))
    fill = bpy.context.active_object
    fill.name = "Fill"
    fill.data.energy = 500
    fill.data.size = 10

    return sun, fill

def setup_render(num_models):
    """Setup render settings"""
    scene = bpy.context.scene

    # Resolution - wider for more models
    rows = (num_models + MODELS_PER_ROW - 1) // MODELS_PER_ROW
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 400 * rows
    scene.render.resolution_percentage = 100

    # Use Cycles
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 64
    scene.cycles.use_denoising = True

    # Background
    scene.world.use_nodes = True
    bg = scene.world.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (0.15, 0.15, 0.18, 1)

    # Output
    scene.render.filepath = OUTPUT_FILE
    scene.render.image_settings.file_format = 'PNG'

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("ALL PIGS COMPARISON - Importing and Arranging")
    print("=" * 70)

    # Clear scene
    clear_scene()

    # Import and arrange models
    models = import_and_arrange_models()
    num_models = len(models)

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
    print("\nModels in comparison (left to right, top to bottom):")
    for i, m in enumerate(models):
        print(f"  {i+1}. {m['name']}")

if __name__ == "__main__":
    main()
