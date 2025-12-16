# Feature Specification: Scrum Level 1 Model Refinement

**Feature Branch**: `001-scrum-level1-refinement`
**Created**: 2025-12-15
**Status**: Draft
**Input**: Iterate on 3D pig mascot model to match HogBall reference image with accurate eye placement, ear orientation, lacing pattern, body shape, and color saturation

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Visual Accuracy Validation (Priority: P1)

As a game artist reviewing the 3D Scrum model, I can compare the rendered preview against the 2D reference image and confirm visual alignment of key character traits.

**Why this priority**: Visual accuracy to the reference image is the primary goal of this feature. Without accurate rendering of the character's defining features, the model cannot be approved for the game.

**Independent Test**: Can be tested by rendering v003+ and performing side-by-side comparison with `reference/scrum_level1_target.png`. Visual checklist verification delivers confidence that the model matches the approved design.

**Acceptance Scenarios**:

1. **Given** a completed model iteration, **When** rendered at the same angle as the reference, **Then** the football-shaped body silhouette matches the reference proportions (pointed at both ends, widest in middle)
2. **Given** a rendered preview, **When** compared to the reference, **Then** both eyes (near AND far) are clearly visible with golden amber iris color (#D4A017) matching the Character Bible
3. **Given** a rendered preview, **When** compared to the reference, **Then** the white football lacing is prominently visible as horizontal stripes with cross-stitch detail across the body
4. **Given** a rendered preview, **When** compared to the reference, **Then** eyebrows create a worried/concerned expression matching the reference
5. **Given** a rendered preview, **When** compared to the reference, **Then** pink cheek blush marks are visible adding cuteness to the face

---

### User Story 2 - Color Consistency with Character Bible (Priority: P2)

As a game artist, I can verify that all color values in the rendered model match the hex specifications defined in the Character Bible.

**Why this priority**: Consistent color values ensure brand identity across all game assets. Colors are defined in the Character Bible and must be accurate for Level 1's bubblegum pink appearance.

**Independent Test**: Can be tested by sampling colors from the rendered preview using an image editor and comparing hex values against the Character Bible specifications.

**Acceptance Scenarios**:

1. **Given** the rendered body material, **When** color sampled, **Then** the base pink is saturated bubblegum pink (#FFB6C1) matching the Character Bible, not washed out
2. **Given** the rendered eye iris, **When** color sampled, **Then** the golden amber matches #D4A017
3. **Given** the rendered lacing, **When** color sampled, **Then** the white lacing is pure white (#FFFFFF)

---

### User Story 3 - Iterative Version Tracking (Priority: P3)

As a game artist iterating on the model, I can preserve all previous iterations while generating new versions, enabling progress tracking and easy rollback.

**Why this priority**: The constitution mandates version tracking (v001, v002, etc.) to enable visual progress tracking and rollback capability. This is foundational to the iterative workflow.

**Independent Test**: Can be tested by running the generation script multiple times and verifying each produces a uniquely numbered output file without overwriting previous versions.

**Acceptance Scenarios**:

1. **Given** existing previews v001 and v002, **When** the script runs, **Then** output is named v003 (or next sequential number)
2. **Given** any iteration, **When** a rollback is needed, **Then** previous versions remain available in the previews directory
3. **Given** a new render, **When** output is saved, **Then** corresponding .blend file is also saved with matching version number

---

### Edge Cases

- What happens when the reference image file is missing? Script continues to render without background overlay, logging a message
- What happens if the previews directory doesn't exist? Script creates it automatically via `os.makedirs()`
- How does the system handle very high version numbers? 3-digit zero-padding (v001-v999) is supported

## Requirements *(mandatory)*

### Functional Requirements

#### Geometry & Shape
- **FR-001**: Model MUST display body shape with football silhouette (scale ratio 1.6:0.85:0.8 X:Y:Z, pointed at both ends, widest in middle)
- **FR-002**: Model MUST position eyes on SIDE of head (Y-offset ±0.50 to ±0.55) so BOTH near and far eyes are visible from 3/4 view angle
- **FR-003**: Model MUST render eyes with golden amber iris color (#D4A017) per Character Bible
- **FR-004**: Model MUST display ears pointing UP and BACK, not floppy/downward
- **FR-005**: Model MUST show white football lacing as horizontal stripes (stripe thickness 0.04 BU) with cross-stitch detail between stripes
- **FR-006**: Model MUST use saturated bubblegum pink (#FFB6C1, material roughness ≤0.5) for body, not washed-out pink
- **FR-007**: Model MUST include curly tail, large snout with oval nostrils, and small hooves

#### Expression (Reference Image Match)
- **FR-011**: Model MUST include eyebrow geometry positioned above eyes to create worried/concerned expression (tilted inward)
- **FR-012**: Model MUST include pink cheek blush marks (oval shapes, lighter pink #FFC0CB) positioned below/beside eyes for cuteness

#### Version Tracking & Workflow
- **FR-008**: Script MUST auto-increment version numbers for each render (v001, v002, v003...)
- **FR-009**: Script MUST save both .blend and .png files with matching version numbers
- **FR-010**: Camera angle MUST match reference image perspective (3/4 front-right view, position 3.5, -2.5, 1.0)

### Key Entities

- **Scrum Model**: The 3D pig mascot composed of body, snout, nostrils, eyes (white, iris, pupil), eyebrows, cheek blush, ears, tail, hooves, and lacing geometry
- **Reference Image**: 2D target design (`reference/scrum_level1_target.png`) serving as ground truth for visual accuracy
- **Character Bible**: Source document defining immutable traits and color specifications
- **Version Artifacts**: Each iteration produces a versioned .blend file and .png preview

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Model silhouette matches reference image football shape when overlaid at same scale/angle (visual approval by reviewer)
- **SC-002**: Both eyes are clearly visible in rendered 3/4 view preview, with golden iris distinguishable
- **SC-003**: White lacing stripes are prominently visible as distinct horizontal bands across the body
- **SC-004**: Pink body color reads as saturated "bubblegum pink" to reviewer, not pale/washed-out
- **SC-005**: Ears visibly point upward/backward, not drooping or horizontal
- **SC-006**: Each script execution produces unique versioned output files without overwriting previous iterations
- **SC-007**: Model passes all immutable traits checklist from Character Bible (football body, white lacing, golden eyes, large snout, curly tail, consistent hooves)
- **SC-008**: Eyebrows are visible and create worried/concerned expression matching reference image
- **SC-009**: Cheek blush marks are visible as pink oval accents adding cuteness to the face

## Assumptions

- Blender is available via WSL2 → Windows execution path using `blender.sh` wrapper
- Reference image exists at `reference/scrum_level1_target.png`
- Current model version is v002 with eyes on sides, upward ears, horizontal lacing (baseline for refinement)
- All color values are converted from hex to Blender's 0-1 RGB range programmatically
- Visual validation is subjective and requires human reviewer comparison against reference
