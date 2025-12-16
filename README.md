# Auto-Blender - HogBall Mascot Generator

## Pig Model Download Links

These sources have free/CC0 pig models. Download manually since CAPTCHA blocks automated downloads:

### poly.pizza (CC-BY, requires manual download due to CAPTCHA)
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

### Quaternius (CC0, direct download)
- Farm Animals Pack: https://quaternius.com/packs/farmpack.html
- Ultimate Animated Animals: https://quaternius.com/packs/ultimateanimatedanimals.html
- All Packs: https://quaternius.com/index.html

### Other Sources
- OpenGameArt Pigs: https://opengameart.org/art-search-advanced?keys=pig&field_art_type_tid%5B%5D=10
- Sketchfab (filter CC0): https://sketchfab.com/search?features=downloadable&licenses=322a749bcfa841b29dff1571c1d5b317&licenses=b9ddc40b93e34cdca1fc152f39b9f375&q=pig&type=models
- Kenney Animal Pack: https://kenney.nl/assets/animal-pack-redux
- TurboSquid Free: https://www.turbosquid.com/Search/3D-Models/free/pig

### Currently Downloaded (in models/ folder)
1. `lowpoly_pig.blend` - Low poly pig model
2. `porco.blend` - Porco pig model
3. `Farm Animals by @Quaternius/Blends/Pig.blend` - Quaternius farm pig (also OBJ, FBX)

## Usage

Place downloaded GLB/GLTF/blend files in `models/polypizza/` or `models/downloads/`, then run:
```bash
./blender.sh scripts/compare_all_pigs.py
```

---

# SpecKit Project Template

Constitution  
Specify  
Clarify  
Plan  
Checklist  
Task  
Analyze  
Implement  

This template provides a Docker-based setup for [GitHub SpecKit](https://github.com/github/spec-kit) - a spec-driven development toolkit that helps you create, plan, and implement features using AI-assisted workflows.

## What This Template Provides

- **No local Python/UV required** - Everything runs in Docker containers
- **Auto-installation** - SpecKit installs automatically on first use
- **Claude Code integration** - Slash commands for spec-driven development
- **Project templates** - Pre-configured structure for specifications, plans, and tasks

## Requirements

- Docker
- Docker Compose

That's it! No Python, UV, or other dependencies needed on your local machine.

## Quick Start

### 1. Create a New Project

```bash
# Copy the template to your new project location
cp -r /home/turtle_wolfe/repos/speckit-template /path/to/your-new-project
cd /path/to/your-new-project

# Run any specify command - this auto-installs everything on first run
./specify --help
```

### 2. What Happens on First Run

When you run `./specify` for the first time:

1. **Installs SpecKit** - Downloads and installs SpecKit CLI in `.speckit/` directory
2. **Initializes Project** - Creates `.specify/` with templates and configuration
3. **Sets up Claude Code** - Adds slash commands to `.claude/commands/`

This takes a minute or two. Subsequent runs are instant.

## Available Slash Commands

After initialization, use these commands in Claude Code:

### Core Workflow

1. `/speckit.constitution` - Establish project principles and values
2. `/speckit.specify` - Create baseline specification for features
3. `/speckit.plan` - Create detailed implementation plan
4. `/speckit.tasks` - Generate actionable task list
5. `/speckit.implement` - Execute implementation

### Optional Enhancement Commands

- `/speckit.clarify` - Ask structured questions to clarify requirements (run before planning)
- `/speckit.analyze` - Cross-artifact consistency analysis (run after tasks, before implementation)
- `/speckit.checklist` - Generate quality checklists (run after planning)

## Using the Specify CLI

You can also use SpecKit's CLI directly:

```bash
./specify --help           # Show help
./specify init --help      # Show initialization options
./specify check            # Check required tools
```

## Updating SpecKit

To update to the latest version of SpecKit:

```bash
./specify update
```

This removes the current installation and reinstalls from the latest version on GitHub.

## File Structure

```
your-project/
├── .claude/              # Claude Code configuration and slash commands
│   └── commands/         # Auto-generated slash commands
├── .specify/             # SpecKit templates and configuration
│   ├── memory/           # Project constitution
│   ├── templates/        # Spec, plan, and task templates
│   └── scripts/          # Helper scripts
├── .speckit/             # SpecKit installation (auto-generated)
├── docker-compose.yml    # Docker configuration
├── specify*              # Main wrapper script
├── .gitignore           # Excludes .speckit/ and .specify/
└── README.md            # This file
```

### What to Commit to Git

**Commit these:**
- `docker-compose.yml`
- `specify` script
- `README.md`
- `.gitignore`

**Don't commit these** (already in .gitignore):
- `.speckit/` - Installation files, regenerated automatically
- `.specify/` - Templates and config, regenerated on init

## How It Works

The `specify` wrapper script:

1. Checks if Docker is running
2. Installs SpecKit in `.speckit/` if not present
3. Initializes project structure in `.specify/` if not present
4. Runs your command in a Docker container

All SpecKit files stay in your project directory, persisting between runs.

## Troubleshooting

### "Cannot connect to Docker daemon"
Make sure Docker is running.

### Permission errors on files
Run `./specify update` to clean and reinstall.

### Slash commands not appearing
Make sure you're using Claude Code and the `.claude/commands/` directory exists.

## Learn More

- [SpecKit Documentation](https://github.com/github/spec-kit)
- [Spec-Driven Development Guide](https://github.com/github/spec-kit/blob/main/docs/spec-driven-development.md)
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
# SpecKitTemplate
