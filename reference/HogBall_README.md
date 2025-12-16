# HogBall 3D Assets

3D models for **Scrum**, the sentient pig mascot from HogBall.

## Quick Start

### Test Blender is working:
```bash
blender --version
```

### Generate Level 1 Baby Pig:
```bash
cd HogBall_3D
blender --background --python scripts/create_scrum_level1.py
```

### Open result in Blender GUI:
```bash
blender /tmp/hogball/scrum_level1.blend
```

## Folder Structure

```
HogBall_3D/
├── scripts/           # Blender Python scripts
├── blend/             # Final .blend files
├── exports/           # Game-ready .glb/.fbx files
├── previews/          # Rendered preview images
├── reference/         # Character bible and docs
├── CLAUDE_CODE_INSTRUCTIONS.md  # Detailed guide for AI
└── README.md          # This file
```

## Character Evolution

| Level | Name | Description |
|-------|------|-------------|
| 1 | Baby Pig | Pink, round, innocent |
| 2 | Adolescent | Spotted, mischievous |
| 3 | Young Hog | Reddish-brown, determined |
| 4 | Wild Boar | Dark, scarred, aggressive |

## For Claude Code

See `CLAUDE_CODE_INSTRUCTIONS.md` for:
- Blender Python API basics
- Color specifications
- Model structure requirements
- Rendering workflow

See `reference/HogBall_Character_Bible.md` for:
- Complete character specifications
- AI image generation prompts
- Evolution trait tables
