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
import glob
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)  # Go up from scripts/ to repo root

# Output directories (relative to repo root)
BLEND_DIR = os.path.join(REPO_ROOT, "blend")
PREVIEW_DIR = os.path.join(REPO_ROOT, "previews")
REFERENCE_DIR = os.path.join(REPO_ROOT, "reference")

# Reference image for photo-matching
REFERENCE_IMAGE = os.path.join(REFERENCE_DIR, "scrum_level1_target.png")

PREVIEW_RENDER = True
SAVE_BLEND = True
USE_REFERENCE_BG = True  # Load reference image as camera background

def get_next_version():
    """Find next version number for preview files"""
    existing = glob.glob(os.path.join(PREVIEW_DIR, "scrum_level1_v*.png"))
    if not existing:
        return 1
    versions = []
    for f in existing:
        try:
            v = int(os.path.basename(f).replace("scrum_level1_v", "").replace(".png", ""))
            versions.append(v)
        except:
            pass
    return max(versions) + 1 if versions else 1

# Colors (hex) - v007: VIBRANT pink like reference
COLORS = {
    "baby_pink": "#FF6B8A",  # Strong saturated pink
    "snout_pink": "#FF5577",
    "eye_white": "#FFFFFF",
    "pupil_black": "#1A1A1A",
    "eye_gold": "#D4A017",
    "nostril_dark": "#993344",  # Dark contrast
    "hoof_pink": "#FF7799",
    "lacing_white": "#FFFFFF",
    "cheek_blush": "#FF5566",  # Visible coral blush
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
    
    # Scale to football/egg shape (v004: balanced - not so long it hides snout)
    body.scale = (1.3, 0.95, 0.9)
    bpy.ops.object.transform_apply(scale=True)
    
    # Apply material (v007: lower roughness 0.3 for more vibrant pink)
    mat = create_material("BabyPink", COLORS["baby_pink"], roughness=0.3)
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
    """Create eyes on FRONT of face - both visible from 3/4 view like reference"""
    eyes = []

    # v005: Eyes on FRONT of face - LARGER like reference with visible white
    eye_configs = [
        # Left eye (near camera) - on front-left of face
        {"side": "L", "white": (0.85, 0.28, 0.25), "iris": (0.98, 0.32, 0.27), "pupil": (1.06, 0.34, 0.28)},
        # Right eye (far camera) - on front-right of face
        {"side": "R", "white": (0.85, -0.28, 0.25), "iris": (0.98, -0.32, 0.27), "pupil": (1.06, -0.34, 0.28)},
    ]

    for i, config in enumerate(eye_configs):
        # Eye white - LARGER for cartoon look
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=14,
            ring_count=10,
            radius=0.28,  # v005: bigger eyes
            location=config["white"]
        )
        eye = bpy.context.active_object
        eye.name = f"Eye_{config['side']}"

        mat = create_material(f"EyeWhite_{i}", COLORS["eye_white"], roughness=0.2)
        apply_material(eye, mat)
        bpy.ops.object.shade_smooth()
        eyes.append(eye)

        # Iris (gold) - facing outward/forward - LARGER
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=12,
            ring_count=8,
            radius=0.18,  # v005: bigger iris
            location=config["iris"]
        )
        iris = bpy.context.active_object
        iris.name = f"Iris_{config['side']}"

        mat = create_material(f"IrisGold_{i}", COLORS["eye_gold"], roughness=0.3)
        apply_material(iris, mat)
        bpy.ops.object.shade_smooth()
        eyes.append(iris)

        # Pupil (black) - centered on iris, facing outward - LARGER
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=10,
            ring_count=8,
            radius=0.10,  # v005: bigger pupil
            location=config["pupil"]
        )
        pupil = bpy.context.active_object
        pupil.name = f"Pupil_{config['side']}"

        mat = create_material(f"PupilBlack_{i}", COLORS["pupil_black"], roughness=0.5)
        apply_material(pupil, mat)
        bpy.ops.object.shade_smooth()
        eyes.append(pupil)

    return eyes


def create_eyebrows():
    """v005: Create eyebrows for worried/concerned expression per FR-011"""
    eyebrows = []
    # Use darker pink for eyebrows to stand out
    mat = create_material("EyebrowPink", "#E896A8", roughness=0.5)

    # Two eyebrows above eyes - WORRIED look means inner edges UP
    # (opposite of angry which has inner edges down)
    eyebrow_configs = [
        # Left eyebrow - inner edge (toward center) tilts UP for worried
        {"side": "L", "loc": (1.0, 0.18, 0.52), "rot": (math.radians(10), math.radians(-15), math.radians(25))},
        # Right eyebrow - mirror of left
        {"side": "R", "loc": (1.0, -0.18, 0.52), "rot": (math.radians(10), math.radians(15), math.radians(-25))},
    ]

    for config in eyebrow_configs:
        # Use flattened sphere for eyebrow shape - BIGGER
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=8,
            ring_count=6,
            radius=0.10,  # v005: bigger
            location=config["loc"]
        )
        eyebrow = bpy.context.active_object
        eyebrow.name = f"Eyebrow_{config['side']}"

        # Flatten and elongate for eyebrow shape - more prominent
        eyebrow.scale = (2.0, 0.5, 0.4)
        eyebrow.rotation_euler = config["rot"]
        bpy.ops.object.transform_apply(scale=True, rotation=True)

        apply_material(eyebrow, mat)
        bpy.ops.object.shade_smooth()
        eyebrows.append(eyebrow)

    return eyebrows


def create_cheek_blush():
    """v005: Create pink cheek blush marks for cuteness per FR-012"""
    blushes = []
    # Use a more visible coral/orange-pink for blush
    mat = create_material("CheekBlush", "#FF9999", roughness=0.6)

    # Two oval blush marks below eyes - pushed FORWARD
    blush_configs = [
        # Left cheek - below left eye
        {"side": "L", "loc": (1.05, 0.40, 0.05)},
        # Right cheek - below right eye
        {"side": "R", "loc": (1.05, -0.40, 0.05)},
    ]

    for config in blush_configs:
        # Flattened sphere for blush - slightly larger
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=10,
            ring_count=8,
            radius=0.10,
            location=config["loc"]
        )
        blush = bpy.context.active_object
        blush.name = f"CheekBlush_{config['side']}"

        # Flatten to sit on face surface, make oval
        blush.scale = (0.3, 0.6, 0.25)
        bpy.ops.object.transform_apply(scale=True)

        apply_material(blush, mat)
        bpy.ops.object.shade_smooth()
        blushes.append(blush)

    return blushes


def create_ears():
    """Create ears pointing UP and BACK like reference image"""
    ears = []

    for i, y_offset in enumerate([0.65, -0.65]):
        # Cone shape for pointy pig ears
        bpy.ops.mesh.primitive_cone_add(
            vertices=12,
            radius1=0.18,
            radius2=0.02,
            depth=0.35,
            location=(-0.2, y_offset, 0.55)
        )
        ear = bpy.context.active_object
        ear.name = f"Ear_{'L' if i == 0 else 'R'}"

        # Rotate to point UP and slightly BACK
        ear.rotation_euler = (
            math.radians(-30),     # Tilt back
            math.radians(25 * (1 if i == 0 else -1)),  # Angle outward
            math.radians(10 * (1 if i == 0 else -1))   # Slight twist
        )

        bpy.ops.object.transform_apply(rotation=True)

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
    """Create HORIZONTAL white football lacing stripes across body like reference"""
    mat = create_material("LacingWhite", COLORS["lacing_white"])
    laces = []

    # Two main horizontal stripes wrapping around the body
    stripe_positions = [0.3, -0.4]  # X positions along the body

    for i, x_pos in enumerate(stripe_positions):
        # Create a torus for a stripe that wraps around
        # v003: Increased minor_radius from 0.025 to 0.04 per T003/FR-005
        bpy.ops.mesh.primitive_torus_add(
            major_radius=0.82,  # Radius around body
            minor_radius=0.04,  # Thickness of stripe (v003: increased)
            major_segments=32,
            minor_segments=8,
            location=(x_pos, 0, 0)
        )
        stripe = bpy.context.active_object
        stripe.name = f"Lacing_Stripe_{i}"

        # Rotate to wrap around body (Y-axis ring)
        stripe.rotation_euler = (0, math.radians(90), 0)
        bpy.ops.object.transform_apply(rotation=True)

        apply_material(stripe, mat)
        laces.append(stripe)

    # Add small cross-stitches between the stripes (on top)
    # v003: Increased scale from (0.5, 0.03, 0.03) to (0.6, 0.05, 0.05) per T004
    for i, x_pos in enumerate([-0.05]):
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(x_pos, 0, 0.85)
        )
        stitch = bpy.context.active_object
        stitch.name = f"Lacing_Stitch_{i}"
        stitch.scale = (0.6, 0.05, 0.05)  # v003: increased visibility
        bpy.ops.object.transform_apply(scale=True)
        apply_material(stitch, mat)
        laces.append(stitch)

    return laces


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
    """Set up camera for preview render - 3/4 front-right view to match reference"""
    # Position camera for 3/4 front-right view (matching HogBall logo reference)
    bpy.ops.object.camera_add(
        location=(3.5, -2.5, 1.0)  # Front-right, slightly above
    )
    camera = bpy.context.active_object
    camera.name = "PreviewCamera"

    # Point at pig's face area (slightly forward of origin)
    target = Vector((0.3, 0, 0.1))
    direction = target - camera.location
    camera.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    # Set as active camera
    bpy.context.scene.camera = camera

    # Load reference image as background if enabled
    if USE_REFERENCE_BG and os.path.exists(REFERENCE_IMAGE):
        camera.data.show_background_images = True
        bg = camera.data.background_images.new()
        bg.image = bpy.data.images.load(REFERENCE_IMAGE)
        bg.alpha = 0.5  # Semi-transparent for comparison
        bg.display_depth = 'BACK'
        print(f"Loaded reference background: {REFERENCE_IMAGE}")

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
    
    # Use Cycles for better color reproduction (v005: EEVEE washes out pink)
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 64  # Lower samples for faster preview
    
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

    print("Creating eyebrows...")  # v003: FR-011
    eyebrows = create_eyebrows()

    print("Creating cheek blush...")  # v003: FR-012
    cheek_blush = create_cheek_blush()

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

    # Get version number for this iteration
    version = get_next_version()
    version_str = f"v{version:03d}"
    print(f"Iteration: {version_str}")

    # Save blend file (versioned)
    if SAVE_BLEND:
        blend_path = os.path.join(BLEND_DIR, f"scrum_level1_{version_str}.blend")
        bpy.ops.wm.save_as_mainfile(filepath=blend_path)
        print(f"Saved: {blend_path}")

    # Render preview (versioned)
    if PREVIEW_RENDER:
        preview_path = os.path.join(PREVIEW_DIR, f"scrum_level1_{version_str}.png")
        scene.render.filepath = preview_path
        bpy.ops.render.render(write_still=True)
        print(f"Preview rendered: {preview_path}")

    print("=" * 50)
    print(f"DONE! Version: {version_str}")
    print(f"Blend: {BLEND_DIR}/scrum_level1_{version_str}.blend")
    print(f"Preview: {PREVIEW_DIR}/scrum_level1_{version_str}.png")
    print("=" * 50)


if __name__ == "__main__":
    main()
