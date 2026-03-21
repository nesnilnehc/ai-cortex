---
name: define-strategic-pillars
description: Derive 3–5 strategic pillars (high-level themes) from vision and North Star that structure and guide strategic goals and roadmap. Produces a strategic pillars document; persisted to docs.
tags: [documentation, workflow]
version: 1.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [strategic pillars, define pillars, strategy pillars]
input_schema:
  type: free-form
  description: Vision; North Star (or paths); project context; optional mission; existing goals or pillars
output_schema:
  type: document-artifact
  description: Strategic pillars document with 3–5 pillars; written to docs/project-overview/strategic-pillars.md (or project norms)
  artifact_type: strategic-pillars
  path_pattern: docs/project-overview/strategic-pillars.md
  lifecycle: living
---

# Skill: Define Strategic Pillars

## Purpose

Derive **3–5 strategic pillars** (high-level themes) from **vision** and **North Star** that structure and guide strategic goals and roadmap. Produce a pillars document so goals and roadmap can be grouped under pillars. Does not define mission, vision, North Star, goals, milestones, or roadmap.

---

## Core Objective

**Primary Goal**: Produce a user-confirmed strategic pillars document containing exactly 3–5 pillars (themes) aligned with vision and North Star, persisted to the project-agreed path.

**Success Criteria** (ALL must be met):

1. ✅ **3–5 pillars documented**: Exactly 3–5 strategic pillars, each with a clear name and short description (what this pillar represents).
2. ✅ **Theme-level**: Each pillar is a high-level theme or strategic direction, not a goal or initiative.
3. ✅ **Aligned with vision**: Each pillar supports the vision; alignment is stated or evident.
4. ✅ **North Star connection**: At least one pillar clearly supports or frames the North Star; optional: brief "how this supports vision/NSM" per pillar.
5. ✅ **User confirmed**: User explicitly approved (e.g. "approved", "looks good", "proceed", or equivalent).
6. ✅ **Document persisted**: Written to agreed path (default `docs/project-overview/strategic-pillars.md` or per project norms).

**Acceptance Test**: Can a reader see how each pillar frames the strategy and how goals or roadmap themes can be grouped under them?

**Handoff Point**: When pillars are approved and persisted, hand off to `design-strategic-goals` (goals can map to pillars) or `define-roadmap` (roadmap themes can align to pillars); this skill does not define goals or roadmap.

---

## Scope Boundaries

**This skill handles**:

- Eliciting and documenting 3–5 strategic pillars (high-level themes).
- Ensuring alignment with vision and North Star (read from `define-vision` / `define-north-star` outputs or existing docs).
- Persisting to project-agreed path (default `docs/project-overview/strategic-pillars.md`).
- Optional: per-pillar note on how it supports vision or North Star.

**This skill does NOT handle**:

- Defining mission, vision, or North Star (use `define-mission`, `define-vision`, `define-north-star`).
- Defining strategic goals or milestones (use `design-strategic-goals`, `define-milestones`).
- Defining roadmap (use `define-roadmap`).

---

## Use Cases

- **After vision and North Star**: Establish 3–5 pillars that structure how goals and roadmap are organized.
- **Strategy structure**: Provide a stable set of themes so goals and initiatives can be grouped (e.g. "Product Excellence", "Customer Success", "Operational Efficiency").
- **Before or with goals**: Run before or in parallel with `design-strategic-goals` so goals can map to pillars.
- **Fourth layer in strategy chain**: Run after mission, vision, and north star when building the full hierarchy (Mission → Vision → North Star → Pillars → Goals → Milestones → Roadmap).

---

## Behavior

### Interaction Policy

- **Defaults**: Output path from project norms if present; otherwise `docs/project-overview/strategic-pillars.md`. Read vision and North Star from `docs/project-overview/` when available.
- **Choice options**: If user has more than 5 candidate pillars, offer to prioritize or merge into 3–5; ask user to confirm the final set.
- **Confirm**: Before overwriting an existing strategic-pillars file; before final persist.

### Execution Process

1. **Load vision and North Star**: Read from `docs/project-overview/vision.md` and `docs/project-overview/north-star.md` or user-provided summary.
2. **Elicit**: What 3–5 high-level themes or pillars would structure the strategy and guide goals/roadmap?
3. **Draft pillars**: Theme-level (e.g. "Customer First", "Operational Excellence"); not goals or initiatives.
4. **Check alignment**: Each pillar supports the vision; at least one clearly supports or frames the North Star.
5. **Persist**: Write to project-agreed path; create `docs/project-overview/` if missing. Optional: add "How this supports vision/NSM" per pillar.

---

## Input & Output

**Input**:

- **Required**: Vision; North Star (or paths); project context.
- **Optional**: Mission; existing goals or pillars; constraints (e.g. org structure).

**Output**:

- **Artifact**: Strategic pillars document.
- **Location**: `docs/project-overview/strategic-pillars.md` (or per project norms).
- **Content**: List of 3–5 pillars (name, short description); optional mapping to vision/NSM.
- **Lifecycle**: Living (updated when vision or strategy direction changes).

---

## Restrictions

### Hard Boundaries

- Do NOT define mission, vision, North Star, goals, milestones, or roadmap in this skill.
- Do NOT overwrite an existing strategic-pillars file without explicit user confirmation.

### Skill Boundaries (Avoid Overlap)

**Do NOT do these (other skills handle them)**:

- **Mission / vision / North Star**: Use `define-mission`, `define-vision`, `define-north-star`.
- **Strategic goals**: Use `design-strategic-goals`; goals can map to pillars.
- **Milestones / roadmap**: Use `define-milestones`, `define-roadmap`.

**When to stop and hand off**:

- User says "approved" or equivalent → Pillars complete; offer handoff to `design-strategic-goals` or `define-roadmap`.
- User asks for goals or roadmap → Hand off to `design-strategic-goals` or `define-roadmap`.

---

## Self-Check

### Core Success Criteria (ALL must be met)

- [ ] **3–5 pillars documented**: Each with name and short description.
- [ ] **Theme-level**: Pillars are themes/directions, not goals or initiatives.
- [ ] **Aligned with vision**: Each pillar supports the vision; alignment stated or evident.
- [ ] **North Star connection**: At least one pillar supports or frames the North Star.
- [ ] **User confirmed**: User said "approved", "looks good", "proceed", or equivalent.
- [ ] **Document persisted**: Written to agreed path.

### Process Quality Checks

- [ ] **Vision/NSM used**: Did I read or request vision and North Star before drafting pillars?
- [ ] **No goals in pillars**: Did I avoid writing outcome goals (those belong in design-strategic-goals)?

### Acceptance Test

**Can a reader see how each pillar frames the strategy and how goals or roadmap themes can be grouped under them?**

If NO: Clarify pillar descriptions and alignment.
If YES: Pillars are complete. Proceed to handoff or stop.

---

## Examples

### Example 1: Vision and North Star exist, define pillars

**Context**: Vision and North Star documents exist. User wants strategic pillars to structure goals and roadmap.

**Process**: Read vision and north-star. Propose 3–5 pillars (e.g. "Discoverability", "Reusability", "Governance", "Ecosystem"). Add short description per pillar and how it supports vision/NSM. User confirms. Write to `docs/project-overview/strategic-pillars.md`.

**Outcome**: Pillars persisted; handoff to `design-strategic-goals` or `define-roadmap`.

### Example 2: Goals already exist

**Context**: Strategic goals document exists; user wants to add a pillars layer for structure.

**Process**: Read vision, North Star, and existing goals. Propose pillars that group or frame the existing goals (e.g. cluster goals under 3–5 themes). User confirms. Write to `docs/project-overview/strategic-pillars.md`. Suggest updating goals doc to reference pillars if desired.

**Outcome**: Pillars persisted; goals can be explicitly mapped to pillars in a later pass.
