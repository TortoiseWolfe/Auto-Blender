# Implementation Plan: Scrum Level 1 Model Refinement

**Branch**: `001-scrum-level1-refinement` | **Date**: 2025-12-15 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-scrum-level1-refinement/spec.md`

## Summary

Refine the Scrum Level 1 3D pig mascot model to better match the HogBall reference image. Key improvements: increase pink color saturation, enhance far eye visibility, make lacing more prominent, and adjust body shape to be more football-pointed. All changes via Blender Python script modifications.

## Technical Context

**Language/Version**: Python 3.x (Blender embedded Python)
**Primary Dependencies**: bpy (Blender Python API), mathutils
**Storage**: File-based (.blend, .png outputs)
**Testing**: Visual comparison against reference image
**Target Platform**: Windows Blender 5.0 via WSL2 wrapper
**Project Type**: Single script (procedural 3D model generation)
**Performance Goals**: N/A (offline asset generation)
**Constraints**: Script must run headless via `blender --background --python`
**Scale/Scope**: Single character model, 4 geometry adjustments

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Reference-Driven Design | ✅ PASS | Reference image at `reference/scrum_level1_target.png`, all changes derived from comparison |
| II. Character Consistency | ✅ PASS | All immutable traits preserved (football body, white lacing, golden eyes, snout, curly tail, hooves) |
| III. Iterative Development | ✅ PASS | Version tracking implemented (v001, v002, v003...), no overwrites |
| IV. Procedural Generation | ✅ PASS | All model changes via `create_scrum_level1.py` script |
| V. Visual Validation | ✅ PASS | Each iteration renders preview for comparison |

**Quality Gates**:
- [x] Script runs without errors (baseline v002 functional)
- [x] Preview renders successfully
- [ ] Visual comparison with reference completed (pending v003)
- [ ] Immutable traits checklist verified (pending v003)
- [x] Version number incremented

## Project Structure

### Documentation (this feature)

```text
specs/001-scrum-level1-refinement/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output (geometry parameters)
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (via /speckit.tasks)
```

### Source Code (repository root)

```text
Auto-Blender/
├── scripts/
│   └── create_scrum_level1.py    # Main generation script (MODIFY)
├── blend/                         # Generated .blend files (gitignored)
├── previews/                      # Versioned render outputs
├── exports/                       # Game-ready exports
├── reference/
│   ├── HogBall_Character_Bible.md
│   └── scrum_level1_target.png   # Reference image
└── specs/                         # SpecKit specifications
```

**Structure Decision**: Single script project. All changes to `scripts/create_scrum_level1.py`.

## Complexity Tracking

No constitution violations. All changes are incremental parameter adjustments to existing procedural code.

---

## Phase 0: Research

No external research required. All information available from:
- Character Bible (color hex values)
- Reference image (visual proportions)
- Current script (baseline parameters)

### Known Issues from v002

Based on visual comparison with reference image:

1. **Pink color appears washed out** - EEVEE rendering may be desaturating; need to verify material settings or try Cycles
2. **Far eye not visible enough** - Y-offset may need adjustment, or eye needs to be pushed forward more on far side
3. **Lacing not prominent** - Torus stripes too thin, cross-stitch too small
4. **Body not football-pointed enough** - X-scale 1.4 may need increase, or use lattice deformation for pointed ends

### Research Findings

| Decision | Rationale | Alternatives Rejected |
|----------|-----------|----------------------|
| Increase body X-scale to 1.6 | More pointed football shape | Lattice deformation (too complex for incremental change) |
| Increase lacing minor_radius to 0.04 | Thicker, more visible stripes | Adding more stripes (cluttered) |
| Adjust far eye forward X position | Better visibility from 3/4 view | Moving camera (breaks reference angle match) |
| Try Cycles renderer | Better color accuracy | Keep EEVEE (faster but washed colors) |

---

## Phase 1: Design

### Geometry Parameters (data-model.md equivalent)

| Component | Current Value | Proposed Value | Change |
|-----------|---------------|----------------|--------|
| **Body** | scale=(1.4, 0.9, 0.85) | scale=(1.6, 0.85, 0.8) | More elongated, pointed |
| **Lacing stripes** | minor_radius=0.025 | minor_radius=0.04 | 60% thicker |
| **Cross-stitch** | scale=(0.5, 0.03, 0.03) | scale=(0.6, 0.05, 0.05) | 67% thicker |
| **Far eye (R)** | location=(0.6, -0.55, 0.25) | location=(0.65, -0.50, 0.25) | Forward + inward |
| **Far iris (R)** | location=(0.72, iris_y, 0.28) | location=(0.78, iris_y, 0.28) | Forward |
| **Far pupil (R)** | location=(0.8, pupil_y, 0.30) | location=(0.86, pupil_y, 0.30) | Forward |

### Material Parameters

| Component | Current | Proposed | Change |
|-----------|---------|----------|--------|
| **Render engine** | BLENDER_EEVEE | BLENDER_EEVEE_NEXT or CYCLES | Better color reproduction |
| **Pink roughness** | 0.7 | 0.5 | Shinier, more saturated appearance |
| **Pink saturation** | Unchanged | Add +10% saturation boost | Via node if needed |

### Implementation Approach

1. **Body shape**: Modify `create_body()` scale parameters
2. **Eye positions**: Modify `create_eyes()` to handle left/right asymmetrically for camera angle
3. **Lacing thickness**: Modify `create_lacing()` torus and cube dimensions
4. **Material tweaks**: Modify `create_material()` roughness, optionally add color boost node

### Quickstart

```bash
# Generate next iteration (v003)
./blender.sh scripts/create_scrum_level1.py

# Output locations:
# - blend/scrum_level1_v003.blend
# - previews/scrum_level1_v003.png
```

---

## Next Steps

Run `/speckit.tasks` to generate actionable task list from this plan.
