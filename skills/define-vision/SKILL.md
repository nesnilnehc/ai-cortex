---
name: define-vision
description: Define the long-term future the project aims to create. Answers what future we are building; produces a vision statement aligned with mission, persisted to docs.
tags: [documentation, workflow, eng-standards]
version: 1.0.0
license: MIT
related_skills: [define-mission, define-north-star, design-strategic-goals, bootstrap-docs]
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [define vision, vision, what future]
input_schema:
  type: free-form
  description: Mission (statement or path); project/product context; optional existing vision draft
output_schema:
  type: document-artifact
  description: Vision statement written to docs/project-overview/vision.md (or project norms)
  artifact_type: vision
  path_pattern: docs/project-overview/vision.md
  lifecycle: living
---

# Skill: Define Vision

## Purpose

Define and document the **vision**: the long-term future the project aims to create. Produce a concise vision statement that answers "What future are we building?" and aligns with the mission. Does not define metrics, goals, or milestones.

---

## Core Objective

**Primary Goal**: Produce a single, user-confirmed vision statement consistent with the mission and persist it to the project-agreed path.

**Success Criteria** (ALL must be met):

1. ✅ **Vision statement exists**: One to three sentences describing the desired future state only (no metrics, no OKRs, no roadmap).
2. ✅ **Aligned with mission**: Vision does not contradict the mission; if mission is missing, recommend running `define-mission` first or state assumed purpose.
3. ✅ **User confirmed**: User explicitly approved (e.g. "approved", "looks good", "proceed", or equivalent).
4. ✅ **Document persisted**: Written to agreed path (default `docs/project-overview/vision.md` or per project norms).
5. ✅ **Scope respected**: Statement does not define North Star metric, strategic goals, or milestones.

**Acceptance Test**: Can a reader understand what long-term future this project is trying to create, and see that it supports the mission?

**Handoff Point**: When vision is approved and persisted, hand off to `define-north-star` or `design-strategic-goals` as needed, or stop.

---

## Scope Boundaries

**This skill handles**:

- Articulating the desired long-term future state of the project or product.
- Producing a vision statement (1–3 sentences).
- Ensuring consistency with mission (read mission from `define-mission` output or existing docs).
- Persisting to project-agreed path (default `docs/project-overview/vision.md`).

**This skill does NOT handle**:

- Defining purpose (use `define-mission`).
- Defining North Star metric or goals (use `define-north-star`, `design-strategic-goals`).
- Defining milestones (use `define-milestones`).
- Writing roadmap, requirements, or backlog (use project planning, `analyze-requirements`, `capture-work-items`).

---

## Use Cases

- **After mission**: Establish "what future we build" once "why we exist" is clear.
- **Strategy or direction reset**: Realign the team on the long-term target.
- **When roadmap lacks a target**: Create a clear vision so roadmap and goals can align.
- **Second layer in strategy chain**: Run after `define-mission` when building the full hierarchy.

---

## Behavior

### Interaction Policy

- **Defaults**: Output path from project norms if present; otherwise `docs/project-overview/vision.md`. Read mission from `docs/project-overview/mission.md` or user when available.
- **Choice options**: If multiple plausible futures exist, offer 1–3 candidate statements and ask user to pick or refine.
- **Confirm**: Before overwriting an existing vision file; before final persist. If mission is missing, confirm whether to assume a purpose or suggest running `define-mission` first.

### Execution Process

1. **Load mission**: Read mission from `docs/project-overview/mission.md` or user-provided summary.
2. **Elicit**: What does "success" look like in 2–5 years? What world are we creating for users?
3. **Draft**: Vision statement (1–3 sentences); future state only — no metrics or KPIs.
4. **Check alignment**: Ensure vision supports mission; refine with user if needed.
5. **Persist**: Write to project-agreed path; create `docs/project-overview/` if missing.

---

## Input & Output

**Input**:

- **Required**: Mission (statement or path to mission doc); project/product context.
- **Optional**: Existing vision draft, time horizon, audience.

**Output**:

- **Artifact**: Vision statement (1–3 sentences).
- **Location**: `docs/project-overview/vision.md` (or per project norms).
- **Content**: Vision statement; optional: "Aligned with mission", "Time horizon".
- **Lifecycle**: Living (update when strategic direction changes).

---

## Restrictions

### Hard Boundaries

- Do NOT include North Star metric, strategic goals, OKRs, or milestones in the vision statement.
- Do NOT overwrite an existing vision file without explicit user confirmation.
- Do NOT produce more than one artifact; this skill produces only the vision document.

### Skill Boundaries (Avoid Overlap)

**Do NOT do these (other skills handle them)**:

- **Mission**: Why we exist → Use `define-mission`.
- **North Star metric**: Single key metric → Use `define-north-star`.
- **Strategic goals**: 3–5 outcomes → Use `design-strategic-goals`.
- **Milestones**: Phase checkpoints → Use `define-milestones`.

**When to stop and hand off**:

- User says "approved" or equivalent → Vision complete; offer handoff to `define-north-star` or `design-strategic-goals`.
- User asks for "one metric" or "North Star" → Hand off to `define-north-star`.
- User asks for goals or milestones → Hand off to `design-strategic-goals` or `define-milestones`.

---

## Self-Check

### Core Success Criteria (ALL must be met)

- [ ] **Vision statement exists**: One to three sentences, future state only (no metrics, goals, milestones).
- [ ] **Aligned with mission**: No contradiction with mission; or mission absence noted and user confirmed.
- [ ] **User confirmed**: User said "approved", "looks good", "proceed", or equivalent.
- [ ] **Document persisted**: Written to agreed path (default `docs/project-overview/vision.md` or project norms).
- [ ] **Scope respected**: No North Star, goals, or milestones in the statement.

### Process Quality Checks

- [ ] **Mission used**: Did I read or request mission before drafting vision?
- [ ] **Future only**: Did I avoid mixing in metrics or OKRs?

### Acceptance Test

**Can a reader understand what long-term future this project is trying to create and see that it supports the mission?**

If NO: Vision is incomplete or misaligned. Refine and re-check against mission.
If YES: Vision is complete. Proceed to handoff or stop.

---

## Examples

### Example 1: Vision after mission exists

**Context**: Mission is "We exist to give engineering teams a single, reliable way to deploy services from code to production." User wants a vision.

**Process**: Elicit 2–5 year target: e.g. "Every team can ship to production in under 5 minutes with one click, with full audit and rollback." Draft vision; check it supports the mission. User confirms. Write to `docs/project-overview/vision.md`.

**Outcome**: Vision persisted; handoff to `define-north-star` (e.g. "deployments per week that succeeded within 5 min") or `design-strategic-goals` offered.

### Example 2: No mission yet

**Context**: User asks to "define our vision" but no mission document exists.

**Process**: Ask whether to assume a purpose from README/context or recommend running `define-mission` first. If user prefers to proceed, state assumed purpose in vision doc and draft vision; confirm with user. Persist; suggest adding mission later for full hierarchy.

**Outcome**: Vision persisted with optional "Assumed purpose" note; user can run `define-mission` later to complete the chain.
