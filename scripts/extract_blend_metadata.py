"""
Extract metadata from blend files to help identify source/author
"""
import bpy
import os
import json

MODELS_DIR = "/home/turtle_wolfe/repos/Auto-Blender/models/unverified"

def get_blend_info(filepath):
    """Extract any identifying info from a blend file"""
    bpy.ops.wm.open_mainfile(filepath=filepath)

    info = {
        "file": os.path.basename(filepath),
        "blend_file_version": f"{bpy.data.version[0]}.{bpy.data.version[1]}.{bpy.data.version[2]}",
        "objects": [],
        "materials": [],
        "textures": [],
        "texts": [],
    }

    # Get object names
    for obj in bpy.data.objects:
        info["objects"].append(obj.name)

    # Get material names
    for mat in bpy.data.materials:
        info["materials"].append(mat.name)

    # Get image/texture names (might have source paths)
    for img in bpy.data.images:
        info["textures"].append({
            "name": img.name,
            "filepath": img.filepath if img.filepath else "embedded"
        })

    # Get any text blocks (might have license info)
    for txt in bpy.data.texts:
        info["texts"].append({
            "name": txt.name,
            "content": txt.as_string()[:500]  # First 500 chars
        })

    # Scene info
    scene = bpy.context.scene
    info["scene_name"] = scene.name

    return info

def main():
    results = []

    for filename in os.listdir(MODELS_DIR):
        if filename.endswith(".blend"):
            filepath = os.path.join(MODELS_DIR, filename)
            print(f"\n{'='*60}")
            print(f"Analyzing: {filename}")
            print('='*60)

            try:
                info = get_blend_info(filepath)
                results.append(info)

                print(f"Blender version: {info['blend_file_version']}")
                print(f"Scene: {info['scene_name']}")
                print(f"Objects: {info['objects']}")
                print(f"Materials: {info['materials']}")
                if info['textures']:
                    print(f"Textures: {info['textures']}")
                if info['texts']:
                    print(f"Text blocks: {info['texts']}")
            except Exception as e:
                print(f"Error: {e}")

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
