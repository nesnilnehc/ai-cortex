---
name: define-roadmap
description: Translate strategic goals and milestones into a time-bound roadmap of initiatives or themes. Produces a roadmap document that bridges strategy and delivery planning; persisted to docs.
tags: [documentation, workflow]
version: 1.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [define roadmap, roadmap, strategic roadmap]
input_schema:
  type: free-form
  description: Strategic goals and milestones (documents or paths); optional initiatives; project context; time horizon
output_schema:
  type: document-artifact
  description: Roadmap document with initiatives/themes and optional timeframes; written to docs/process-management/roadmap.md (or project norms)
  artifact_type: roadmap
  path_pattern: docs/process-management/roadmap.md
  lifecycle: living
---

# Skill: Define Roadmap

## Purpose

Translate **strategic goals** and **milestones** into a **time-bound roadmap** of initiatives or themes (with optional timeframes). Produce a single roadmap document that bridges strategy and delivery planning. Does not define mission, vision, North Star, goals, or milestones; does not create backlog items.

---

## Core Objective

**Primary Goal**: Produce a user-confirmed roadmap document that maps goals and milestones to initiatives or themes with optional timeframes, persisted to the project-agreed path.

**Success Criteria** (ALL must be met):

1. ✅ **Roadmap documented**: Initiatives or themes listed, each with name and short scope; optional quarters or phases.
2. ✅ **Traceability**: Each roadmap item maps to at least one milestone or strategic goal; mapping is explicit in the document.
3. ✅ **Time-bound (optional)**: If time horizon is provided, roadmap reflects it; otherwise outcome-ordered is acceptable.
4. ✅ **User confirmed**: User explicitly approved (e.g. "approved", "looks good", "proceed", or equivalent).
5. ✅ **Document persisted**: Written to agreed path (default `docs/process-management/roadmap.md` or per project norms).
6. ✅ **Scope respected**: No backlog items, requirements, or task lists in the roadmap document.

**Acceptance Test**: Can a reader see how each roadmap item advances milestones and goals, and in what order or timeframe (if specified)?

**Handoff Point**: When roadmap is approved and persisted, hand off to backlog planning; this skill does not create backlog items.

---

## Scope Boundaries

**This skill handles**:

- Deriving roadmap structure from strategic goals and milestones (read from existing docs or user input).
- Defining initiatives or themes with optional timeframes (e.g. by quarter or phase).
- Documenting traceability: roadmap item → milestone(s) and goal(s).
- Persisting to project-agreed path (default `docs/process-management/roadmap.md`).

**This skill does NOT handle**:

- Defining mission, vision, North Star, goals, or milestones (use `define-mission`, `define-vision`, `define-north-star`, `design-strategic-goals`, `define-milestones`).
- Creating backlog items (use `capture-work-items`, project planning).

---

## Use Cases

- **After milestones**: Build a visible plan that connects strategy to release or sprint planning.
- **Planning cycle**: Establish initiative/theme sequence or time-bound view for the next 1–2 periods.
- **Before backlog**: Provide roadmap so backlog items can be grouped under initiatives or themes.
- **Strategy-to-execution bridge**: Run after goals and milestones when building the full hierarchy.

---

## Behavior

### Interaction Policy

- **Defaults**: Output path from project norms if present; otherwise `docs/process-management/roadmap.md`. Read goals and milestones from `docs/project-overview/strategic-goals.md` and `docs/process-management/milestones.md` when available.
- **Choice options**: If user wants both outcome-ordered and time-bound views, offer structure (e.g. phases with optional quarters) and ask for confirmation.
- **Confirm**: Before overwriting an existing roadmap file; before final persist.

### Execution Process

1. **Load strategy**: Read strategic goals and milestones from docs or user-provided summary; optionally read strategic pillars.
2. **Derive structure**: For each milestone (or goal), what initiatives or themes represent the next level of planning?
3. **Per roadmap item**: Name, short scope, optional timeframe; explicit mapping to milestone(s) and goal(s).
4. **Persist**: Write to project-agreed path; create `docs/process-management/` if missing.

---

## Input & Output

**Input**:

- **Required**: Strategic goals and milestones (documents or paths); project context.
- **Optional**: Initiatives document; time horizon (e.g. next 4 quarters); existing roadmap.

**Output**:

- **Artifact**: Roadmap document.
- **Location**: `docs/process-management/roadmap.md` (or per project norms).
- **Content**: Initiatives/themes with scope, optional timeframes; mapping to milestones and goals.
- **Lifecycle**: Living (updated as execution progresses or strategy changes).

---

## Restrictions

### Hard Boundaries

- Do NOT define mission, vision, North Star, goals, or milestones in this skill.
- Do NOT create backlog items, requirements, or task lists; roadmap is initiatives/themes only.
- Do NOT overwrite an existing roadmap file without explicit user confirmation.

### Skill Boundaries (Avoid Overlap)

**Do NOT do these (other skills handle them)**:

- **Mission / vision / North Star / goals / milestones**: Use `define-mission`, `define-vision`, `define-north-star`, `design-strategic-goals`, `define-milestones`.
- **Strategic pillars**: Use `define-strategic-pillars`; this skill may consume pillars as input.
- **Backlog items**: Use `capture-work-items`, project planning.

**When to stop and hand off**:

- User says "approved" or equivalent → Roadmap complete; offer handoff to backlog planning.
- User asks for backlog or requirements → Hand off to `capture-work-items` or `analyze-requirements`.

---

## Self-Check

### Core Success Criteria (ALL must be met)

- [ ] **Roadmap documented**: Initiatives/themes with name, scope, optional timeframe.
- [ ] **Traceability**: Each item maps to at least one milestone or goal; mapping in document.
- [ ] **User confirmed**: User said "approved", "looks good", "proceed", or equivalent.
- [ ] **Document persisted**: Written to agreed path (default `docs/process-management/roadmap.md` or project norms).
- [ ] **Scope respected**: No backlog items, requirements, or task lists in the document.

### Process Quality Checks

- [ ] **Strategy used**: Did I read or request goals and milestones before drafting roadmap?
- [ ] **No backlog**: Did I avoid writing individual backlog items?

### Acceptance Test

**Can a reader see how each roadmap item advances milestones and goals, and in what order or timeframe?**

If NO: Add traceability and optional timeframes.
If YES: Roadmap is complete. Proceed to handoff or stop.

---

## Examples

### Example 1: Goals and milestones exist, build roadmap

**Context**: Strategic goals and milestones documents exist. User wants a roadmap for the next 4 quarters.

**Process**: Read strategic-goals and milestones. Propose initiatives or themes per milestone; add optional quarters. Map each item to milestone(s) and goal(s). User confirms. Write to `docs/process-management/roadmap.md`.

**Outcome**: Roadmap persisted; handoff to backlog planning.

### Example 2: Initiatives document exists

**Context**: User has strategic pillars or themes and now wants a time-bound roadmap.

**Process**: Read pillars (or goals) and milestones. Arrange themes into phases or quarters; add traceability to milestones and goals. User confirms. Write to `docs/process-management/roadmap.md`.

**Outcome**: Roadmap persisted with themes as building blocks.
