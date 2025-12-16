# Quickstart: Scrum Level 1 Model Refinement

**Feature**: 001-scrum-level1-refinement

## Prerequisites

- Blender 5.0+ installed on Windows
- WSL2 with access to Windows filesystem
- `blender.sh` wrapper script in repo root

## Generate New Iteration

```bash
# From repo root
./blender.sh scripts/create_scrum_level1.py
```

## Output Locations

| Artifact | Path |
|----------|------|
| Blend file | `blend/scrum_level1_v{NNN}.blend` |
| Preview image | `previews/scrum_level1_v{NNN}.png` |
| Reference image | `reference/scrum_level1_target.png` |

## Visual Validation Workflow

1. Run script to generate new version
2. Open `previews/scrum_level1_v{NNN}.png`
3. Compare side-by-side with `reference/scrum_level1_target.png`
4. Check immutable traits:
   - [ ] Football-shaped body
   - [ ] White lacing visible
   - [ ] Golden eyes (#D4A017)
   - [ ] Large snout with nostrils
   - [ ] Curly tail
   - [ ] Four hooves

## Code Locations

| Change | File | Function |
|--------|------|----------|
| Body shape | `scripts/create_scrum_level1.py` | `create_body()` |
| Eye positions | `scripts/create_scrum_level1.py` | `create_eyes()` |
| Lacing thickness | `scripts/create_scrum_level1.py` | `create_lacing()` |
| Material settings | `scripts/create_scrum_level1.py` | `create_material()` |

## Rollback

Previous versions are preserved. To compare:

```bash
# List all versions
ls -la previews/scrum_level1_v*.png

# View specific version in image viewer
xdg-open previews/scrum_level1_v002.png
```
