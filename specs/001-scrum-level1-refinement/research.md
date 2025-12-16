# Research: Scrum Level 1 Model Refinement

**Feature**: 001-scrum-level1-refinement
**Date**: 2025-12-15

## Research Summary

No external research required. All technical decisions derived from:
- Character Bible specifications (color hex values)
- Reference image comparison (`reference/scrum_level1_target.png`)
- Current script analysis (`scripts/create_scrum_level1.py`)

## Decisions

### 1. Body Shape - More Football-Pointed

**Decision**: Increase body X-scale from 1.4 to 1.6, reduce Y/Z slightly

**Rationale**:
- Current body is too egg-shaped, not pointy enough at ends
- Reference image shows distinct football silhouette with tapered ends
- Simple scale adjustment maintains procedural generation principle

**Alternatives Rejected**:
- Lattice deformation: Too complex for incremental change, harder to parameterize
- Custom mesh: Violates procedural generation principle

### 2. Pink Color Saturation

**Decision**: Reduce material roughness from 0.7 to 0.5, optionally switch to Cycles

**Rationale**:
- EEVEE tends to wash out colors compared to reference
- Lower roughness = shinier surface = more saturated color appearance
- Character Bible specifies #FFB6C1 (bubblegum pink) - must read as saturated

**Alternatives Rejected**:
- Adjusting hex value: Violates Character Bible spec
- Post-processing: Not part of procedural workflow

### 3. Far Eye Visibility

**Decision**: Move far eye (right side) forward in X and slightly inward in Y

**Rationale**:
- From 3/4 camera angle, far eye is partially occluded by head
- Moving it forward brings it into view
- Reference shows both eyes clearly visible

**Alternatives Rejected**:
- Moving camera: Would break reference angle match
- Making eyes larger: Would violate proportion consistency

### 4. Lacing Prominence

**Decision**: Increase torus minor_radius from 0.025 to 0.04, increase cross-stitch scale

**Rationale**:
- Current lacing stripes are too thin to be prominent
- Reference shows distinct white lacing as key character feature
- Constitution lists white lacing as immutable trait

**Alternatives Rejected**:
- Adding more stripes: Would clutter design
- Making stripes glow: Not appropriate for solid model
