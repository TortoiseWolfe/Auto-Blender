# Tasks: Scrum Level 1 Model Refinement

**Feature Branch**: `001-scrum-level1-refinement`
**Generated**: 2025-12-15
**Source**: [plan.md](plan.md), [spec.md](spec.md), [data-model.md](data-model.md)

---

## Phase 1: Setup

No setup tasks required - baseline v002 script is already functional.

---

## Phase 2: Foundational

No foundational blocking tasks - all changes are incremental to existing script.

---

## Phase 3: User Story 1 - Visual Accuracy (P1)

**Goal**: Model geometry matches reference image proportions for body, eyes, ears, and lacing.

**Independent Test**: Render v003 and visually compare against `reference/scrum_level1_target.png`.

### Tasks

- [ ] T001 [P] [US1] Modify body scale to (1.6, 0.85, 0.8) for football shape in `scripts/create_scrum_level1.py:create_body()`
- [ ] T002 [P] [US1] Modify far eye (R) positions for better visibility in `scripts/create_scrum_level1.py:create_eyes()`
  - Eye white: (0.6, -0.55, 0.25) → (0.65, -0.50, 0.25)
  - Iris: Push forward X by 0.06
  - Pupil: Push forward X by 0.06
- [ ] T003 [P] [US1] Increase lacing stripe thickness (minor_radius 0.025 → 0.04) in `scripts/create_scrum_level1.py:create_lacing()`
- [ ] T004 [P] [US1] Increase cross-stitch scale (0.5, 0.03, 0.03) → (0.6, 0.05, 0.05) in `scripts/create_scrum_level1.py:create_lacing()`
- [ ] T016 [P] [US1] Add `create_eyebrows()` function for worried expression in `scripts/create_scrum_level1.py`
  - Two small curved/angled shapes above eyes
  - Tilted inward to create concerned look
  - Same pink color as body (#FFB6C1)
- [ ] T017 [P] [US1] Add `create_cheek_blush()` function for cuteness in `scripts/create_scrum_level1.py`
  - Two oval shapes positioned below/beside eyes
  - Lighter pink color (#FFC0CB)
  - Subtle, not overpowering
- [ ] T005 [US1] Run script to generate v003 via `./blender.sh scripts/create_scrum_level1.py`
- [ ] T006 [US1] Visually validate v003 against reference image for geometry AND expression match

---

## Phase 4: User Story 2 - Color Consistency (P2)

**Goal**: Pink body color renders as saturated bubblegum pink, not washed out.

**Independent Test**: Sample colors from rendered preview and compare hex values to Character Bible.

### Tasks

- [ ] T007 [US2] Reduce pink material roughness (0.7 → 0.5) in `scripts/create_scrum_level1.py:create_material()`
- [ ] T008 [US2] Run script to generate v004 via `./blender.sh scripts/create_scrum_level1.py`
- [ ] T009 [US2] Visually validate v004 pink saturation against Character Bible #FFB6C1
- [ ] T010 [US2] If pink still washed out: Try CYCLES renderer in `scripts/create_scrum_level1.py:setup_render_settings()`

---

## Phase 5: User Story 3 - Version Tracking (P3)

**Goal**: Each iteration produces uniquely versioned files without overwriting.

**Independent Test**: Run script multiple times, verify sequential versioning.

### Tasks

- [ ] T011 [US3] Verify version tracking works (already implemented in v002 baseline)
- [ ] T012 [US3] Confirm v003/v004 files exist in `previews/` without overwriting v001/v002

---

## Phase 6: Polish & Validation

- [ ] T013 Run final validation against immutable traits checklist (Character Bible)
- [ ] T014 Document v003/v004 comparison notes in commit message
- [ ] T015 Update quality gates in `specs/001-scrum-level1-refinement/plan.md`

---

## Dependencies

```
Phase 3 (US1: Geometry) → Phase 4 (US2: Color) → Phase 5 (US3: Verify)
                                                        ↓
                                                 Phase 6 (Polish)
```

User stories are **mostly independent** - geometry and color can be done in either order, but US3 verification depends on having multiple iterations.

---

## Parallel Execution

**Within Phase 3 (US1)**:
- T001, T002, T003, T004, T016, T017 can be done in any order before T005 (render)

**Within Phase 4 (US2)**:
- T007 completes before T008 (render)

---

## Implementation Strategy

**MVP Scope**: Complete Phase 3 (US1) only → delivers visual accuracy improvement

**Incremental Delivery**:
1. v003: Geometry fixes (body, eyes, lacing)
2. v004: Color saturation fix (if needed after v003)

---

## Summary

| Phase | Story | Tasks | Key File |
|-------|-------|-------|----------|
| 3 | US1 (P1) | T001-T006, T016-T017 | `scripts/create_scrum_level1.py` |
| 4 | US2 (P2) | T007-T010 | `scripts/create_scrum_level1.py` |
| 5 | US3 (P3) | T011-T012 | `previews/` |
| 6 | Polish | T013-T015 | `plan.md` |

**Total Tasks**: 17
**Parallel Opportunities**: T001-T004, T016-T017 (Phase 3)
**MVP**: Phase 3 only (8 tasks)

---

## Baseline Coverage (No Tasks Needed)

The following requirements are already satisfied by the v002 baseline and require no changes:

| Requirement | Status | Evidence |
|-------------|--------|----------|
| FR-004 (ears UP/BACK) | ✅ Complete | Cone ears with correct rotation in `create_ears()` |
| FR-007 (tail/snout/hooves) | ✅ Complete | All components present in v002 |
| FR-010 (camera angle) | ✅ Complete | 3/4 front-right view in `setup_camera()` |
