---
name: define-milestones
description: Break strategic goals into concrete phase checkpoints (milestones) that represent major progress stages. Produces a milestones document with traceability to goals; persisted to docs.
tags: [documentation, workflow]
version: 1.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [define milestones, milestones, phase checkpoints]
input_schema:
  type: free-form
  description: Strategic goals (document or path); project context; optional vision/NSM; existing roadmap or phases
output_schema:
  type: document-artifact
  description: Milestones document with phase checkpoints and goal mapping; written to docs/process-management/milestones.md (or project norms)
  artifact_type: milestones
  path_pattern: docs/process-management/milestones.md
  lifecycle: living
---

# Skill: Define Milestones

## Purpose

Break **strategic goals** into **concrete phase checkpoints (milestones)** that represent major progress stages. Produce a milestones document with clear phases and traceability to strategic goals. Does not define mission, vision, North Star, or goals; does not write requirements or backlog.

---

## Core Objective

**Primary Goal**: Produce a user-confirmed milestones document that breaks strategic goals into phase checkpoints, with each milestone traceable to at least one goal, persisted to the project-agreed path.

**Success Criteria** (ALL must be met):

1. ✅ **Milestones documented**: List of milestones, each with name, short scope, and success criterion (outcome or deliverable).
2. ✅ **Traceability**: Each milestone maps to at least one strategic goal; mapping is explicit in the document.
3. ✅ **Concrete checkpoints**: Each milestone is a phase or checkpoint, not a task list or backlog.
4. ✅ **User confirmed**: User explicitly approved (e.g. "approved", "looks good", "proceed", or equivalent).
5. ✅ **Document persisted**: Written to agreed path (default `docs/process-management/milestones.md` or per project norms).
6. ✅ **Scope respected**: No requirements, backlog items, or feature specs in the milestones document.

**Acceptance Test**: Can a reader see which strategic goal each milestone advances and what "done" looks like for each phase, without needing full backlog detail?

**Handoff Point**: When milestones are approved and persisted, hand off to backlog/roadmap planning or to `align-planning` / `run-checkpoint` for governance; this skill does not create backlog items.

---

## Scope Boundaries

**This skill handles**:

- Deriving milestones from strategic goals (read from `design-strategic-goals` output or existing docs).
- Defining phases/checkpoints (e.g. by outcome or optional timeframe).
- Documenting scope and success criterion per milestone.
- Persisting to project-agreed path (default `docs/process-management/milestones.md`).
- Explicit mapping: each milestone → at least one strategic goal.

**This skill does NOT handle**:

- Defining mission, vision, North Star, or strategic goals (use `define-mission`, `define-vision`, `define-north-star`, `design-strategic-goals`).
- Writing requirements (use `analyze-requirements`).
- Creating backlog items (use `capture-work-items`, project planning).
- Building a full roadmap (project planning; this skill only produces the milestones layer).

---

## Use Cases

- **After strategic goals**: Define phases or major checkpoints that indicate progress toward each goal.
- **Release or planning cycle**: Establish "what done looks like" for the next 1–2 phases.
- **Governance gates**: Provide milestones so `run-checkpoint` or `align-planning` can assess completion and alignment.
- **Fifth layer in strategy chain**: Run after mission, vision, north star, and strategic goals when building the full hierarchy.

---

## Behavior

### Interaction Policy

- **Defaults**: Output path from project norms if present; otherwise `docs/process-management/milestones.md`. Read strategic goals from `docs/project-overview/strategic-goals.md` or user when available.
- **Choice options**: If user wants both outcome-based and time-based milestones, offer structure (e.g. "Phase 1: outcome X by date Y") and ask for confirmation.
- **Confirm**: Before overwriting an existing milestones file; before final persist.

### Execution Process

1. **Load strategic goals**: Read from `docs/project-overview/strategic-goals.md` or user-provided summary.
2. **Per goal (or subset)**: What are 1–3 major checkpoints or phases that indicate clear progress?
3. **Per milestone**: Name, short scope, success criterion (outcome or deliverable), optional timeframe.
4. **Traceability**: Ensure each milestone maps to at least one strategic goal; record mapping in the document.
5. **Persist**: Write to project-agreed path; create `docs/process-management/` if missing.

---

## Input & Output

**Input**:

- **Required**: Strategic goals (document or path); project context.
- **Optional**: Vision/NSM; existing roadmap or phases; time constraints.

**Output**:

- **Artifact**: Milestones document.
- **Location**: `docs/process-management/milestones.md` (or per project norms).
- **Content**: List of milestones (name, scope, success criterion, optional timeframe); mapping to strategic goals.
- **Lifecycle**: Living (updated as phases complete or goals change).

---

## Restrictions

### Hard Boundaries

- Do NOT define mission, vision, North Star, or strategic goals in this skill.
- Do NOT create backlog items, requirements, or feature specs; milestones are checkpoints only.
- Do NOT overwrite an existing milestones file without explicit user confirmation.

### Skill Boundaries (Avoid Overlap)

**Do NOT do these (other skills handle them)**:

- **Mission / vision / North Star / goals**: Use `define-mission`, `define-vision`, `define-north-star`, `design-strategic-goals`.
- **Requirements**: Use `analyze-requirements`.
- **Backlog items**: Use `capture-work-items`, project planning.
- **Roadmap detail**: Project planning; this skill produces the milestones layer only.

**When to stop and hand off**:

- User says "approved" or equivalent → Milestones complete; offer handoff to backlog/roadmap or governance skills.
- User asks for requirements or backlog → Hand off to `analyze-requirements` or `capture-work-items`.

---

## Self-Check

### Core Success Criteria (ALL must be met)

- [ ] **Milestones documented**: List of milestones with name, scope, success criterion (optional timeframe).
- [ ] **Traceability**: Each milestone maps to at least one strategic goal; mapping in document.
- [ ] **Concrete checkpoints**: Milestones are phases/checkpoints, not task lists.
- [ ] **User confirmed**: User said "approved", "looks good", "proceed", or equivalent.
- [ ] **Document persisted**: Written to agreed path (default `docs/process-management/milestones.md` or project norms).
- [ ] **Scope respected**: No requirements, backlog, or feature specs in the document.

### Process Quality Checks

- [ ] **Goals used**: Did I read or request strategic goals before drafting milestones?
- [ ] **No backlog**: Did I avoid writing individual backlog items or requirements?

### Acceptance Test

**Can a reader see which goal each milestone advances and what "done" looks like for each phase?**

If NO: Milestones may be too vague or missing goal mapping. Add traceability and success criteria.
If YES: Milestones are complete. Proceed to handoff or stop.

---

## Examples

### Example 1: Goals exist, define phases

**Context**: Strategic goals document exists with 4 goals. User wants milestones for the next 12 months.

**Process**: Read strategic-goals. For each goal, propose 1–2 milestones (e.g. "M1: 50% of teams can deploy in under 10 min", "M2: Rollback available for all services"). Add mapping: M1 → Goal A, M2 → Goal A, etc. Optional: add rough timeframe. User confirms. Write to `docs/process-management/milestones.md`.

**Outcome**: Milestones persisted; handoff to backlog/roadmap or `run-checkpoint` for governance.

### Example 2: No strategic goals yet

**Context**: User asks to "define milestones" but no strategic-goals document exists.

**Process**: Recommend running `design-strategic-goals` first so milestones can trace to goals. If user prefers to proceed anyway, ask for at least a short list of goals or outcomes to map to; draft milestones and document the assumed goals. Confirm with user; persist. Suggest adding strategic goals later for full traceability.

**Outcome**: Milestones persisted with explicit or assumed goal mapping; user can run `design-strategic-goals` later to complete the chain.
