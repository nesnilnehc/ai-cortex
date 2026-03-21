---
name: design-strategic-goals
description: Define 3–5 long-term strategic goals that move the project toward the vision and North Star. Produces a goals document aligned with mission, vision, and NSM; persisted to docs.
tags: [documentation, workflow]
version: 1.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [strategic goals, design goals, define goals]
input_schema:
  type: free-form
  description: Vision; North Star (or paths); project context; optional mission; existing goals or priorities
output_schema:
  type: document-artifact
  description: Strategic goals document with 3–5 goals; written to docs/project-overview/strategic-goals.md (or project norms)
  artifact_type: strategic-goals
  path_pattern: docs/project-overview/strategic-goals.md
  lifecycle: living
---

# Skill: Design Strategic Goals

## Purpose

Define **3–5 long-term strategic goals** that move the project toward the vision and North Star. Produce a goals document with outcome-focused goals (not task lists or roadmap). Does not define mission, vision, North Star, or milestones.

---

## Core Objective

**Primary Goal**: Produce a user-confirmed strategic goals document containing exactly 3–5 outcome-focused goals aligned with vision and North Star, persisted to the project-agreed path.

**Success Criteria** (ALL must be met):

1. ✅ **3–5 goals documented**: Exactly 3–5 strategic goals, each with a clear title and short description.
2. ✅ **Outcome-focused**: Each goal describes an outcome or result, not a task list or feature list.
3. ✅ **Aligned with vision**: Each goal supports the vision; alignment is stated or evident.
4. ✅ **North Star connection**: At least one goal clearly supports or moves the North Star metric; optional: brief "how this supports vision/NSM" per goal.
5. ✅ **User confirmed**: User explicitly approved (e.g. "approved", "looks good", "proceed", or equivalent).
6. ✅ **Document persisted**: Written to agreed path (default `docs/project-overview/strategic-goals.md` or per project norms).

**Acceptance Test**: Can a reader see how each of the 3–5 goals advances the vision and North Star, without needing dates or phases (those belong in milestones)?

**Handoff Point**: When goals are approved and persisted, hand off to `define-milestones` to break goals into phase checkpoints, or stop.

---

## Scope Boundaries

**This skill handles**:

- Eliciting and documenting 3–5 long-term strategic goals.
- Ensuring alignment with vision and North Star (read from `define-vision` / `define-north-star` outputs or existing docs).
- Persisting to project-agreed path (default `docs/project-overview/strategic-goals.md`).
- Optional: per-goal note on how it supports vision or North Star.

**This skill does NOT handle**:

- Defining mission, vision, or North Star (use `define-mission`, `define-vision`, `define-north-star`).
- Breaking goals into phases or dates (use `define-milestones`).
- Writing requirements, roadmap, or backlog (use `analyze-requirements`, project planning, `capture-work-items`).

---

## Use Cases

- **After vision and North Star**: Set 3–5 strategic outcomes that advance the vision and move the NSM.
- **Annual or quarterly strategy**: Define or refresh strategic priorities.
- **When backlog lacks goal alignment**: Create explicit goals so roadmap and backlog can trace to them.
- **Fourth layer in strategy chain**: Run after mission, vision, and north star when building the full hierarchy.

---

## Behavior

### Interaction Policy

- **Defaults**: Output path from project norms if present; otherwise `docs/project-overview/strategic-goals.md`. Read vision and North Star from `docs/project-overview/` when available.
- **Choice options**: If user has more than 5 candidate goals, offer to prioritize or cluster into 3–5; ask user to confirm the final set.
- **Confirm**: Before overwriting an existing strategic-goals file; before final persist.

### Execution Process

1. **Load vision and North Star**: Read from `docs/project-overview/vision.md` and `docs/project-overview/north-star.md` or user-provided summary.
2. **Elicit**: What 3–5 outcomes would materially advance the vision and move the North Star?
3. **Draft goals**: Outcome-focused (e.g. "Reduce time-to-deploy for 80% of teams to under 5 min"); not task lists or feature lists.
4. **Check alignment**: Each goal supports the vision; at least one clearly supports the North Star.
5. **Persist**: Write to project-agreed path; create `docs/project-overview/` if missing. Optional: add "How this supports vision/NSM" per goal.

---

## Input & Output

**Input**:

- **Required**: Vision; North Star (or paths to vision/north-star docs); project context.
- **Optional**: Mission; time horizon; existing goals or priorities.

**Output**:

- **Artifact**: Strategic goals document.
- **Location**: `docs/project-overview/strategic-goals.md` (or per project norms).
- **Content**: 3–5 strategic goals (title + short description); optional: link to vision/NSM; "How this supports vision/NSM" per goal.
- **Lifecycle**: Living (reviewed at strategy cycles).

---

## Restrictions

### Hard Boundaries

- Do NOT define mission, vision, North Star, or milestones in this skill.
- Do NOT include dates or phases in the goals document (those belong in `define-milestones`).
- Do NOT produce fewer than 3 or more than 5 strategic goals in the document.

### Skill Boundaries (Avoid Overlap)

**Do NOT do these (other skills handle them)**:

- **Mission**: Why we exist → Use `define-mission`.
- **Vision**: What future we build → Use `define-vision`.
- **North Star**: Single metric → Use `define-north-star`.
- **Milestones**: Phase checkpoints → Use `define-milestones`.
- **Requirements or backlog**: Use `analyze-requirements`, `capture-work-items`, project planning.

**When to stop and hand off**:

- User says "approved" or equivalent → Goals complete; offer handoff to `define-milestones`.
- User asks for phases or milestones → Hand off to `define-milestones`.

---

## Self-Check

### Core Success Criteria (ALL must be met)

- [ ] **3–5 goals documented**: Exactly 3–5 strategic goals with title and description.
- [ ] **Outcome-focused**: Each goal is an outcome or result, not a task list.
- [ ] **Aligned with vision**: Each goal supports the vision.
- [ ] **North Star connection**: At least one goal clearly supports or moves the North Star.
- [ ] **User confirmed**: User said "approved", "looks good", "proceed", or equivalent.
- [ ] **Document persisted**: Written to agreed path (default `docs/project-overview/strategic-goals.md` or project norms).

### Process Quality Checks

- [ ] **Vision/NSM used**: Did I read or request vision and North Star before drafting goals?
- [ ] **No dates/phases**: Did I avoid putting milestones or timelines in the goals document?

### Acceptance Test

**Can a reader see how each goal advances the vision and North Star without needing dates or phases?**

If NO: Goals may be too tactical or missing alignment. Refine to outcomes and state alignment.
If YES: Strategic goals are complete. Proceed to handoff or stop.

---

## Examples

### Example 1: Full hierarchy in place

**Context**: Vision and North Star exist. User wants 3–5 strategic goals.

**Process**: Read vision and north-star docs. Elicit outcomes (e.g. "80% of teams deploy in under 5 min", "Zero manual steps for standard deploys", "Full audit trail for every deployment"). Draft 3–5 goals; state how each supports vision/NSM. User confirms. Write to `docs/project-overview/strategic-goals.md`.

**Outcome**: Goals persisted; handoff to `define-milestones` offered.

### Example 2: User proposes six goals

**Context**: User lists six candidate goals; plan allows only 3–5.

**Process**: Cluster or prioritize into 3–5 (e.g. merge two related goals, or drop lowest priority). Present the 3–5 set with rationale; ask user to confirm or adjust. Ensure each is outcome-focused and aligned with vision/NSM. Persist once confirmed.

**Outcome**: Document contains exactly 3–5 goals; user has explicitly approved the set.
