# Data Model: Scrum Level 1 Geometry Parameters

**Feature**: 001-scrum-level1-refinement
**Date**: 2025-12-15

## Overview

This document defines the geometry and material parameters for the Scrum Level 1 3D model. All values are used in `scripts/create_scrum_level1.py`.

## Geometry Parameters

### Body

| Parameter | v002 Value | v003 Target | Unit |
|-----------|------------|-------------|------|
| Primitive | UV Sphere | UV Sphere | - |
| Segments | 16 | 16 | count |
| Ring Count | 12 | 12 | count |
| Radius | 1.0 | 1.0 | Blender units |
| Scale X | 1.4 | **1.6** | multiplier |
| Scale Y | 0.9 | **0.85** | multiplier |
| Scale Z | 0.85 | **0.8** | multiplier |

### Eyes (Left - Near Camera)

| Parameter | Value | Unit |
|-----------|-------|------|
| Eye White Location | (0.6, 0.55, 0.25) | XYZ |
| Eye White Radius | 0.22 | BU |
| Iris Location | (0.72, 0.6325, 0.28) | XYZ |
| Iris Radius | 0.14 | BU |
| Pupil Location | (0.8, 0.671, 0.30) | XYZ |
| Pupil Radius | 0.08 | BU |

### Eyes (Right - Far from Camera)

| Parameter | v002 Value | v003 Target | Unit |
|-----------|------------|-------------|------|
| Eye White Location | (0.6, -0.55, 0.25) | **(0.65, -0.50, 0.25)** | XYZ |
| Eye White Radius | 0.22 | 0.22 | BU |
| Iris Location | (0.72, -0.6325, 0.28) | **(0.78, -0.575, 0.28)** | XYZ |
| Iris Radius | 0.14 | 0.14 | BU |
| Pupil Location | (0.8, -0.671, 0.30) | **(0.86, -0.61, 0.30)** | XYZ |
| Pupil Radius | 0.08 | 0.08 | BU |

### Lacing Stripes

| Parameter | v002 Value | v003 Target | Unit |
|-----------|------------|-------------|------|
| Major Radius | 0.82 | 0.82 | BU |
| Minor Radius | 0.025 | **0.04** | BU |
| Major Segments | 32 | 32 | count |
| Minor Segments | 8 | 8 | count |
| Stripe X Positions | [0.3, -0.4] | [0.3, -0.4] | BU |

### Cross-Stitch

| Parameter | v002 Value | v003 Target | Unit |
|-----------|------------|-------------|------|
| Location | (-0.05, 0, 0.85) | (-0.05, 0, 0.85) | XYZ |
| Scale X | 0.5 | **0.6** | multiplier |
| Scale Y | 0.03 | **0.05** | multiplier |
| Scale Z | 0.03 | **0.05** | multiplier |

## Material Parameters

### Baby Pink (Body, Ears, Tail)

| Parameter | v002 Value | v003 Target |
|-----------|------------|-------------|
| Hex Color | #FFB6C1 | #FFB6C1 |
| Roughness | 0.7 | **0.5** |

### Eye Gold (Iris)

| Parameter | Value |
|-----------|-------|
| Hex Color | #D4A017 |
| Roughness | 0.3 |

### Lacing White

| Parameter | Value |
|-----------|-------|
| Hex Color | #FFFFFF |
| Roughness | 0.7 |

## Render Settings

| Parameter | v002 Value | v003 Target |
|-----------|------------|-------------|
| Engine | BLENDER_EEVEE | BLENDER_EEVEE (try CYCLES if color still washed) |
| Resolution | 1024x1024 | 1024x1024 |
| Transparent BG | True | True |

## Validation

All parameters must result in a model that passes:
- [ ] Football-shaped body silhouette
- [ ] Both eyes visible from 3/4 view
- [ ] Golden amber iris color (#D4A017)
- [ ] White lacing prominently visible
- [ ] Saturated bubblegum pink appearance
