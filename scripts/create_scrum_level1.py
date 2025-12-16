"""
HogBall - Scrum Level 1: Baby Pig
Blender Python Script

Run with: blender --background --python create_scrum_level1.py
Or with GUI: blender --python create_scrum_level1.py

This is a STARTER TEMPLATE - iterate on proportions and shapes!
"""

import bpy
import math
from mathutils import Vector

# =============================================================================
# CONFIGURATION
# =============================================================================

# Auto-detect output directory relative to script location
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)  # Go up from scripts/ to repo root

# Output directories (relative to repo root)
BLEND_DIR = os.path.join(REPO_ROOT, "blend")
PREVIEW_DIR = os.path.join(REPO_ROOT, "previews")

PREVIEW_RENDER = True
SAVE_BLEND = True

# Colors (hex)
COLORS = {
    "baby_pink": "#FFB6C1",
    "snout_pink": "#E8A0AD", 
    "eye_white": "#FFFFFF",
    "pupil_black": "#1A1A1A",
    "eye_gold": "#D4A017",
    "nostril_dark": "#C97080",
    "hoof_pink": "#F0A0B0",
    "lacing_white": "#FFFFFF",
}

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple (0-1 range)"""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16) / 255
    g = int(hex_color[2:4], 16) / 255
    b = int(hex_color[4:6], 16) / 255
    return (r, g, b, 1.0)


def create_material(name, hex_color, roughness=0.7):
    """Create a simple material from hex color"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = hex_to_rgb(hex_color)
    bsdf.inputs["Roughness"].default_value = roughness
    return mat


def apply_material(obj, material):
    """Apply material to object"""
    if obj.data.materials:
        obj.data.materials[0] = material
    else:
        obj.data.materials.append(material)


def clear_scene():
    """Remove all objects from scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Also clear orphan data
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)


# =============================================================================
# MODEL CREATION
# =============================================================================

def create_body():
    """Create football-shaped body"""
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=16,
        ring_count=12,
        radius=1.0,
        location=(0, 0, 0)
    )
    body = bpy.context.active_object
    body.name = "Body"
    
    # Scale to football/egg shape
    body.scale = (1.4, 0.9, 0.85)
    bpy.ops.object.transform_apply(scale=True)
    
    # Apply material
    mat = create_material("BabyPink", COLORS["baby_pink"])
    apply_material(body, mat)
    
    # Smooth shading
    bpy.ops.object.shade_smooth()
    
    return body


def create_snout():
    """Create the big round snout"""
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=12,
        ring_count=8,
        radius=0.45,
        location=(1.2, 0, -0.1)
    )
    snout = bpy.context.active_object
    snout.name = "Snout"
    
    # Slightly flatten
    snout.scale = (0.7, 1.0, 0.85)
    bpy.ops.object.transform_apply(scale=True)
    
    mat = create_material("SnoutPink", COLORS["snout_pink"])
    apply_material(snout, mat)
    bpy.ops.object.shade_smooth()
    
    return snout


def create_nostrils():
    """Create two oval nostrils on the snout"""
    nostrils = []
    
    for i, y_offset in enumerate([0.15, -0.15]):
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=8,
            ring_count=6,
            radius=0.1,
            location=(1.5, y_offset, -0.1)
        )
        nostril = bpy.context.active_object
        nostril.name = f"Nostril_{'L' if i == 0 else 'R'}"
        
        # Make oval shaped
        nostril.scale = (0.5, 0.7, 1.0)
        bpy.ops.object.transform_apply(scale=True)
        
        mat = create_material(f"NostrilDark_{i}", COLORS["nostril_dark"])
        apply_material(nostril, mat)
        bpy.ops.object.shade_smooth()
        
        nostrils.append(nostril)
    
    return nostrils


def create_eyes():
    """Create eyes with pupils - positioned close together near snout"""
    eyes = []
    
    for i, y_offset in enumerate([0.25, -0.25]):
        # Eye white
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=12,
            ring_count=8,
            radius=0.18,
            location=(0.9, y_offset, 0.35)
        )
        eye = bpy.context.active_object
        eye.name = f"Eye_{'L' if i == 0 else 'R'}"
        
        mat = create_material(f"EyeWhite_{i}", COLORS["eye_white"], roughness=0.3)
        apply_material(eye, mat)
        bpy.ops.object.shade_smooth()
        eyes.append(eye)
        
        # Iris (gold)
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=10,
            ring_count=6,
            radius=0.12,
            location=(1.0, y_offset * 0.9, 0.38)
        )
        iris = bpy.context.active_object
        iris.name = f"Iris_{'L' if i == 0 else 'R'}"
        
        mat = create_material(f"IrisGold_{i}", COLORS["eye_gold"], roughness=0.4)
        apply_material(iris, mat)
        bpy.ops.object.shade_smooth()
        eyes.append(iris)
        
        # Pupil (black)
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=8,
            ring_count=6,
            radius=0.07,
            location=(1.08, y_offset * 0.85, 0.40)
        )
        pupil = bpy.context.active_object
        pupil.name = f"Pupil_{'L' if i == 0 else 'R'}"
        
        mat = create_material(f"PupilBlack_{i}", COLORS["pupil_black"], roughness=0.5)
        apply_material(pupil, mat)
        bpy.ops.object.shade_smooth()
        eyes.append(pupil)
    
    return eyes


def create_ears():
    """Create small floppy ears pointing downward"""
    ears = []
    
    for i, y_offset in enumerate([0.55, -0.55]):
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=8,
            ring_count=6,
            radius=0.25,
            location=(-0.3, y_offset, 0.5)
        )
        ear = bpy.context.active_object
        ear.name = f"Ear_{'L' if i == 0 else 'R'}"
        
        # Flatten and shape
        ear.scale = (0.6, 0.3, 0.8)
        
        # Rotate to point down and out (floppy)
        ear.rotation_euler = (
            math.radians(20),      # tip forward
            math.radians(30 * (1 if i == 0 else -1)),  # out to sides
            math.radians(-40 * (1 if i == 0 else -1))  # droop down
        )
        
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        
        mat = create_material(f"EarPink_{i}", COLORS["baby_pink"])
        apply_material(ear, mat)
        bpy.ops.object.shade_smooth()
        
        ears.append(ear)
    
    return ears


def create_tail():
    """Create a curly tail"""
    # Create a bezier curve for the curl
    bpy.ops.curve.primitive_bezier_circle_add(radius=0.15, location=(-1.3, 0, 0.1))
    tail = bpy.context.active_object
    tail.name = "Tail"
    
    # Adjust curve to be a spiral
    tail.scale = (0.4, 0.4, 0.6)
    tail.rotation_euler = (math.radians(90), 0, 0)
    
    # Add bevel for thickness
    tail.data.bevel_depth = 0.05
    tail.data.bevel_resolution = 4
    
    mat = create_material("TailPink", COLORS["baby_pink"])
    apply_material(tail, mat)
    
    return tail


def create_hooves():
    """Create 4 small hooves"""
    hooves = []
    
    positions = [
        (0.5, 0.4, -0.75, "FL"),   # Front Left
        (0.5, -0.4, -0.75, "FR"),  # Front Right
        (-0.5, 0.35, -0.7, "BL"),  # Back Left
        (-0.5, -0.35, -0.7, "BR"), # Back Right
    ]
    
    for x, y, z, label in positions:
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.12,
            depth=0.15,
            location=(x, y, z)
        )
        hoof = bpy.context.active_object
        hoof.name = f"Hoof_{label}"
        
        # Round the top
        hoof.scale = (1, 1, 0.8)
        bpy.ops.object.transform_apply(scale=True)
        
        mat = create_material(f"HoofPink_{label}", COLORS["hoof_pink"])
        apply_material(hoof, mat)
        bpy.ops.object.shade_smooth()
        
        hooves.append(hoof)
    
    return hooves


def create_lacing():
    """Create white football lacing along the spine"""
    # Main vertical line
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, 0.88)
    )
    lacing_main = bpy.context.active_object
    lacing_main.name = "Lacing_Main"
    lacing_main.scale = (1.2, 0.03, 0.03)
    bpy.ops.object.transform_apply(scale=True)
    
    mat = create_material("LacingWhite", COLORS["lacing_white"])
    apply_material(lacing_main, mat)
    
    # Cross stitches
    stitches = []
    for i, x_pos in enumerate([-0.3, 0, 0.3]):
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(x_pos, 0, 0.9)
        )
        stitch = bpy.context.active_object
        stitch.name = f"Lacing_Stitch_{i}"
        stitch.scale = (0.03, 0.15, 0.02)
        bpy.ops.object.transform_apply(scale=True)
        
        apply_material(stitch, mat)
        stitches.append(stitch)
    
    return [lacing_main] + stitches


def create_parent_empty():
    """Create parent empty for all parts"""
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    parent = bpy.context.active_object
    parent.name = "Scrum_Level1"
    return parent


def parent_all_to_empty(parent):
    """Parent all mesh objects to the empty"""
    for obj in bpy.data.objects:
        if obj != parent and obj.type in ['MESH', 'CURVE']:
            obj.parent = parent


# =============================================================================
# SCENE SETUP
# =============================================================================

def setup_camera():
    """Set up camera for preview render"""
    bpy.ops.object.camera_add(
        location=(4, -4, 2.5)
    )
    camera = bpy.context.active_object
    camera.name = "PreviewCamera"
    
    # Point at origin
    direction = Vector((0, 0, 0)) - camera.location
    camera.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    
    bpy.context.scene.camera = camera
    return camera


def setup_lighting():
    """Set up basic three-point lighting"""
    # Key light
    bpy.ops.object.light_add(type='SUN', location=(5, -3, 5))
    key = bpy.context.active_object
    key.name = "KeyLight"
    key.data.energy = 3
    key.rotation_euler = (math.radians(45), math.radians(30), 0)
    
    # Fill light
    bpy.ops.object.light_add(type='SUN', location=(-3, -5, 3))
    fill = bpy.context.active_object
    fill.name = "FillLight"
    fill.data.energy = 1.5
    
    # Rim light
    bpy.ops.object.light_add(type='SUN', location=(-2, 4, 4))
    rim = bpy.context.active_object
    rim.name = "RimLight"
    rim.data.energy = 2
    
    return [key, fill, rim]


def setup_render_settings():
    """Configure render settings"""
    scene = bpy.context.scene
    
    # Resolution
    scene.render.resolution_x = 1024
    scene.render.resolution_y = 1024
    scene.render.resolution_percentage = 100
    
    # Transparent background
    scene.render.film_transparent = True
    
    # Use Cycles for better quality (or EEVEE for speed)
    scene.render.engine = 'BLENDER_EEVEE'
    
    return scene


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 50)
    print("Creating Scrum Level 1: Baby Pig")
    print("=" * 50)
    
    # Clear existing scene
    clear_scene()
    
    # Create all parts
    print("Creating body...")
    body = create_body()
    
    print("Creating snout...")
    snout = create_snout()
    
    print("Creating nostrils...")
    nostrils = create_nostrils()
    
    print("Creating eyes...")
    eyes = create_eyes()
    
    print("Creating ears...")
    ears = create_ears()
    
    print("Creating tail...")
    tail = create_tail()
    
    print("Creating hooves...")
    hooves = create_hooves()
    
    print("Creating lacing...")
    lacing = create_lacing()
    
    # Parent everything
    print("Setting up hierarchy...")
    parent = create_parent_empty()
    parent_all_to_empty(parent)
    
    # Scene setup
    print("Setting up camera and lighting...")
    camera = setup_camera()
    lights = setup_lighting()
    scene = setup_render_settings()
    
    # Ensure output directories exist
    os.makedirs(BLEND_DIR, exist_ok=True)
    os.makedirs(PREVIEW_DIR, exist_ok=True)

    # Save blend file
    if SAVE_BLEND:
        blend_path = os.path.join(BLEND_DIR, "scrum_level1.blend")
        bpy.ops.wm.save_as_mainfile(filepath=blend_path)
        print(f"Saved: {blend_path}")

    # Render preview
    if PREVIEW_RENDER:
        preview_path = os.path.join(PREVIEW_DIR, "scrum_level1_preview.png")
        scene.render.filepath = preview_path
        bpy.ops.render.render(write_still=True)
        print(f"Preview rendered: {preview_path}")

    print("=" * 50)
    print("DONE!")
    print(f"Blend file: {BLEND_DIR}")
    print(f"Preview: {PREVIEW_DIR}")
    print("=" * 50)


if __name__ == "__main__":
    main()
