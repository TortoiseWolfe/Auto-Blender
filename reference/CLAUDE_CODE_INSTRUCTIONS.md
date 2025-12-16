# HogBall 3D Modeling Project - Claude Code Instructions

## Project Overview

You are creating 3D models for **HogBall**, a fantasy football game where a sentient pig named **Scrum** IS the ball. Scrum evolves through 4 stages as players level up.

**Your task:** Create low-poly stylized 3D models of Scrum at each evolution stage using Blender's Python API.

---

## Environment Setup

Blender is installed and accessible via command line:

```bash
# Run a Python script in Blender (headless)
blender --background --python script.py

# Run with a specific blend file
blender myfile.blend --background --python script.py

# Run and keep Blender open to see results (GUI)
blender --python script.py
```

---

## Workflow

### Step 1: Create the model via Python script
```bash
blender --background --python create_scrum_level1.py
```

### Step 2: Render a preview to verify
The script should save a preview render as PNG so you can view it and iterate.

### Step 3: Iterate
View the preview image, identify issues, modify the script, re-run.

### Step 4: Export
Save final `.blend` file and optionally export to `.glb`/`.fbx` for game engine use.

---

## Model Structure

Each Scrum model should be organized as:

```
Scrum_Level1 (Empty - parent)
├── Body (Mesh - football-shaped)
├── Snout (Mesh)
├── Eye_L (Mesh)
├── Eye_R (Mesh)
├── Pupil_L (Mesh)
├── Pupil_R (Mesh)
├── Ear_L (Mesh)
├── Ear_R (Mesh)
├── Tail (Mesh or Curve)
├── Hoof_FL (Mesh)
├── Hoof_FR (Mesh)
├── Hoof_BL (Mesh)
├── Hoof_BR (Mesh)
└── Lacing (Mesh or Curve - white football stitching)
```

Use an Empty as the parent so the whole character can be moved/rotated as one unit.

---

## Art Style Guidelines

**Target aesthetic:** Low-poly stylized (think Crossy Road, Katamari, Pikuniku)

- **Polygon count:** ~500-2000 tris per model (game-ready)
- **No subdivision surface** for final export (keep it chunky)
- **Flat shading or slight smooth** depending on look
- **Solid colors** - use simple materials, no complex textures yet
- **Exaggerated proportions** - big snout, small body reads well at game scale

---

## Blender Python Basics

### Starting fresh
```python
import bpy
import math

# Clear the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
```

### Creating primitives
```python
# UV Sphere (good for body, snout)
bpy.ops.mesh.primitive_uv_sphere_add(
    segments=16, 
    ring_count=8, 
    radius=1.0, 
    location=(0, 0, 0)
)
obj = bpy.context.active_object
obj.name = "Body"

# Scale to football shape
obj.scale = (1.5, 1.0, 1.0)  # elongated X axis
bpy.ops.object.transform_apply(scale=True)
```

### Creating materials
```python
def create_material(name, hex_color):
    """Create a simple material from hex color"""
    # Convert hex to RGB
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16) / 255
    g = int(hex_color[2:4], 16) / 255
    b = int(hex_color[4:6], 16) / 255
    
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (r, g, b, 1)
    bsdf.inputs["Roughness"].default_value = 0.7
    return mat

# Apply to object
pink_mat = create_material("BabyPink", "#FFB6C1")
obj.data.materials.append(pink_mat)
```

### Parenting objects
```python
# Create parent empty
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
parent = bpy.context.active_object
parent.name = "Scrum_Level1"

# Parent all parts to it
for obj_name in ["Body", "Snout", "Eye_L", "Eye_R"]:
    obj = bpy.data.objects.get(obj_name)
    if obj:
        obj.parent = parent
```

### Rendering a preview
```python
# Set up camera
bpy.ops.object.camera_add(location=(5, -5, 3))
camera = bpy.context.active_object
camera.name = "PreviewCam"

# Point camera at origin
from mathutils import Vector
direction = Vector((0, 0, 0)) - camera.location
camera.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

bpy.context.scene.camera = camera

# Render settings
scene = bpy.context.scene
scene.render.resolution_x = 800
scene.render.resolution_y = 800
scene.render.film_transparent = True  # Transparent background

# Render
scene.render.filepath = "//scrum_level1_preview.png"
bpy.ops.render.render(write_still=True)
print(f"Preview saved to: {scene.render.filepath}")
```

### Saving the file
```python
bpy.ops.wm.save_as_mainfile(filepath="//scrum_level1.blend")
```

---

## Color Reference

| Element | Hex Code | RGB (0-1) |
|---------|----------|-----------|
| Baby pink (L1) | #FFB6C1 | (1.0, 0.71, 0.76) |
| Dusty pink (L2) | #D4A5A5 | (0.83, 0.65, 0.65) |
| Reddish brown (L3) | #A0522D | (0.63, 0.32, 0.18) |
| Leather brown (L4) | #8B4513 | (0.55, 0.27, 0.07) |
| Eye gold | #D4A017 | (0.83, 0.63, 0.09) |
| White (lacing) | #FFFFFF | (1.0, 1.0, 1.0) |
| Black (pupils) | #1A1A1A | (0.1, 0.1, 0.1) |

---

## Level-Specific Notes

### Level 1: Baby Pig
- Roundest, softest shapes
- Use more sphere-based geometry
- Ears point DOWN (floppy)
- No tusks
- Smallest scale

### Level 2: Adolescent  
- Slightly more angular
- Add subtle brown spots (could be separate mesh pieces or texture later)
- Ears point slightly UP
- Tiny tusk nubs (small cones at mouth corners)
- Slight eyebrow ridge forming

### Level 3: Young Hog
- More defined muscles (can add edge loops to suggest bulk)
- Bristle texture (could be simple planes or spikes on back)
- Pointed alert ears
- Visible small tusks (curved cones)
- Eyebrow furrow (brow ridge mesh)

### Level 4: Wild Boar
- Most angular, aggressive shapes
- Heavy brow ridge
- Full curved tusks
- One ear with notch (battle scar)
- Optional: scar lines as separate edge geometry
- Largest scale

---

## Suggested File Structure

```
HogBall_3D/
├── scripts/
│   ├── create_scrum_level1.py
│   ├── create_scrum_level2.py
│   ├── create_scrum_level3.py
│   ├── create_scrum_level4.py
│   └── utils.py (shared functions)
├── blend/
│   ├── scrum_level1.blend
│   ├── scrum_level2.blend
│   ├── scrum_level3.blend
│   └── scrum_level4.blend
├── exports/
│   ├── scrum_level1.glb
│   ├── scrum_level2.glb
│   └── ...
├── previews/
│   ├── scrum_level1_preview.png
│   └── ...
└── reference/
    ├── HogBall_Character_Bible.md
    └── CLAUDE_CODE_INSTRUCTIONS.md
```

---

## Troubleshooting

### "bpy module not found"
You're running Python outside of Blender. Use:
```bash
blender --background --python yourscript.py
```

### Can't see the render
Make sure you're saving to an accessible path. Use `//` prefix for paths relative to the blend file, or use absolute paths.

### Objects not appearing
Check location values—they might be spawning far from origin. Also check if they're on a hidden collection.

### Script errors with no details
Run Blender with console output:
```bash
blender --background --python script.py 2>&1
```

---

## Getting Started

Begin with Level 1 (Baby Pig). Create a script that:

1. Clears the scene
2. Creates a football-shaped body (elongated sphere)
3. Adds a large snout (sphere, positioned at front)
4. Adds nostrils (two small indented cylinders or scaled spheres)
5. Adds eyes (spheres with pupil spheres inside)
6. Adds floppy ears (flattened/bent cones or sculpted shapes)
7. Adds curly tail (bezier curve with bevel, or spiral mesh)
8. Adds 4 small hooves (cylinders or rounded cubes)
9. Adds white lacing stripe along the top (curve with bevel, or thin box)
10. Applies materials with correct colors
11. Parents everything to an empty
12. Sets up camera and lighting
13. Renders a preview image
14. Saves the .blend file

Iterate on proportions until it looks like a cute baby pig shaped like a football!

---

*Reference the HogBall_Character_Bible.md for complete character specifications.*
