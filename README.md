# Auto-Blender - Character Pipeline

Procedural 3D character generation using Blender's Python API. Currently focused on stylized pig characters.

## Project Structure

```
reference/           # Reference images (empty - add your own)
scripts/             # Blender Python scripts
models/              # Downloaded 3D models (CC0/CC-BY)
previews/            # Render outputs
blend/               # Exported .blend files
```

## Usage

```bash
# Generate pig character
./blender.sh scripts/create_pig_level1.py

# Compare pig models
./blender.sh scripts/compare_all_pigs.py
```

---

## Free 3D Model Sources

### CC0 (No Attribution Required)

| Site | URL | Notes |
|------|-----|-------|
| **Quaternius** | https://quaternius.com | High-quality low-poly game assets, direct downloads |
| **Kenney** | https://kenney.nl/assets/animal-pack-redux | Professional quality, completely free |
| **Poly Haven** | https://polyhaven.com | Best for materials/HDRIs, few animal models |
| **OpenGameArt** | https://opengameart.org | Game-focused, check individual licenses |

### CC-BY (Attribution Required)

| Site | URL | Notes |
|------|-----|-------|
| **Poly Pizza** | https://poly.pizza | Large library, CAPTCHA blocks automation |
| **Sketchfab** | https://sketchfab.com | Filter by downloadable + CC0/CC-BY |
| **Blend Swap** | https://blendswap.com | Blender-native files |

### Direct Links - Pig Models

**Quaternius (CC0):**
- Farm Animals: https://quaternius.com/packs/farmanimal.html
- Ultimate Animated Animals: https://quaternius.com/packs/ultimateanimatedanimals.html
- All Packs: https://quaternius.com/index.html

**Poly Pizza (CC-BY 3.0):**
- Pig by Poly by Google: https://poly.pizza/m/6XC3XssJIU_
- Pig by Poly by Google #2: https://poly.pizza/m/brcb6xLELnz
- Pig by Poly by Google #3: https://poly.pizza/m/6yc3isbjZST
- Pig by Quaternius: https://poly.pizza/m/TNvG3QUFlp
- Pig by Quaternius #2: https://poly.pizza/m/u35l6uP5vj
- Pig by jeremy: https://poly.pizza/m/bbPhEBl5Bh0
- Boar by Poly by Google: https://poly.pizza/m/57fSWum6F1P
- Hog by Aya Kawa: https://poly.pizza/m/5CHg_vV9IJH
- Voxel Pig by Mauri Helme: https://poly.pizza/m/abovMDkoWAN
- Piggy Bank by Poly by Google: https://poly.pizza/m/dpvS2kdW6I9
- Piggy Bank by Poly by Google #2: https://poly.pizza/m/d1lUL18me4S
- Piggy Bank by CreativeTrio: https://poly.pizza/m/1KAexv0Erv
- Collared Peccary by Poly by Google: https://poly.pizza/m/3eoOcw_d00X

**OpenGameArt:**
- Pig search: https://opengameart.org/art-search-advanced?keys=pig&field_art_type_tid%5B%5D=10

**Sketchfab (CC0 filter):**
- Pig search: https://sketchfab.com/search?features=downloadable&licenses=322a749bcfa841b29dff1571c1d5b317&licenses=b9ddc40b93e34cdca1fc152f39b9f375&q=pig&type=models

**TurboSquid Free:**
- Pig search: https://www.turbosquid.com/Search/3D-Models/free/pig

### Currently Downloaded

- `models/cc0/Farm Animals by @Quaternius/` - Pig, Pug, Sheep (Blends, FBX, OBJ)

---

## AI 3D Generation Tools

| Tool | Free Tier | Downloads | Notes |
|------|-----------|-----------|-------|
| **Meshy** | 100 credits/month | **NO** | Generate only; download requires paid upgrade |
| **Tripo3D** | 300 credits/month | **NO** | Generate only; no commercial use |
| **Sloyd** | Editor access | **NO** | Explore only; no usable exports |

**Verdict:** None offer free downloads. All require paid tier to export models. Use CC0 sites (Quaternius, Kenney) instead.

---

## SpecKit Workflow

This project uses [SpecKit](https://github.com/github/spec-kit) for spec-driven development.

```bash
./specify --help    # Show available commands
```

### Slash Commands (in Claude Code)

1. `/speckit.constitution` - Project principles
2. `/speckit.specify` - Create feature spec
3. `/speckit.plan` - Implementation plan
4. `/speckit.tasks` - Generate task list
5. `/speckit.implement` - Execute implementation
