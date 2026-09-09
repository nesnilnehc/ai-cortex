---
name: define-vision
description: Define the long-term future the project aims to create. Answers what future we are building; produces a vision statement aligned with mission, persisted to docs.
description_zh: 定义项目旨在创造的长远未来；回答我们在构建什么未来；产出 vision 陈述并持久化到 docs。
tags: [documentation, workflow]
version: 1.3.0
license: MIT
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

Define and record the **vision**: the long-term future the project sets out to create. A vision statement answers "what future are we building?" and stays consistent with the mission. It defines no metrics, goals or milestones.

**A vision is not**:

- **The mission**: the fundamental purpose behind the project (use `define-mission`).
- **The north star**: the single metric that stands for delivered value (use `define-north-star`).
- **Strategic goals**: the 3–5 outcomes that realize the vision (use `design-strategic-goals`).
- **Milestones**: stage checkpoints during execution (use `define-roadmap`).

---

## Core Goal

**Primary goal**: produce a user-confirmed vision statement consistent with the mission, and persist it to the path the project agreed on.

**Success criteria** (all of them must hold):

1. ✅ **A vision statement exists**: one to three sentences describing the desired future state alone (no metrics, OKRs, roadmap).
2. ✅ **Consistent with the mission**: the vision does not contradict the mission; when the mission is missing, suggest running `define-mission` first, or state the assumed purpose.
3. ✅ **User confirmation**: the user approved it explicitly ("approved", "looks good", "go ahead" or equivalent).
4. ✅ **Persisted as a document**: written to the agreed path (default `docs/project-overview/vision.md`, or the project norms).
5. ✅ **Scope respected**: the statement defines no north star metric, strategic goal or milestone.
6. ✅ **YAGNI/DRY/concision**: follow the document-artifact principles in spec §4; the vision statement is the core, avoid optional paragraphs that earn nothing (an explicit note on mission alignment or on the time horizon, say).

**Acceptance test**: can a reader tell what long-term future the project is trying to create, and see that it is consistent with the mission?

**Handoff point**: once the vision is approved and persisted, hand off to `define-north-star` or `design-strategic-goals`; stop when only the vision was asked for.

---

## Scope Boundary

### What this skill must do

- Articulate the desired long-term future state of the project or product.
- Produce the vision statement (1–3 sentences).
- Keep it consistent with the mission (read the mission from the `define-mission` output or from existing docs).
- Persist it to the path the project agreed on (default `docs/project-overview/vision.md`).

### What this skill cannot do

- Define the fundamental purpose (use `define-mission`).
- Define the north star metric or the strategic goals (use `define-north-star`, `design-strategic-goals`).
- Define milestones (use `define-roadmap`).
- Write the roadmap, requirements or backlog (use `capture-work-items` and the like).

---

## Vision Quality Guide

A strong vision statement has:

- **Concision**: 1–3 sentences, focused on the future state.
- **Consistency with the mission**: it supports the fundamental purpose in the mission and introduces no new one.
- **Imaginability**: a picture of success 2–5 years out; the reader can sketch a concrete scene.
- **No metrics**: no KPI, OKR or numeric target; metrics belong to `define-north-star` or `design-strategic-goals`.

What to avoid in a vision:

- **Implementation detail**: technology, deliverables, or "how" it gets done.
- **Buzzwords**: vague terms that clarify no future state.

---

## When to Use

- **After the mission is done**: with "why we exist" settled, establish "the future we are building".
- **A strategy or direction reset**: realign the team around the long-term aim.
- **The roadmap has no aim**: create a clear vision so the roadmap lines up with it.
- **The second layer of the strategy chain**: run it after `define-mission` when building the full hierarchy.

---

## Behavior

### Interaction strategy

- **Default**: the output path from the project norms (`docs/ARTIFACT_NORMS.md` or `.ai-cortex/artifact-norms.yaml`); otherwise `docs/project-overview/vision.md`. Infer the mission from `docs/project-overview/mission.md` or from the user.
- **Offer options**: when several futures are possible, present 1–3 candidate statements and ask the user to pick or refine one.
- **Confirm**: before overwriting an existing vision file, and before the final persist. When the mission is missing, confirm whether to assume a purpose, or suggest running `define-mission` first.

### Execution

1. **Load the mission**: read it from `docs/project-overview/mission.md` or from a summary the user provides.
2. **Elicit**: what does "success" look like 2–5 years out? What kind of world are we creating for users?
3. **Draft**: the vision statement (1–3 sentences); future state only, no metrics or KPIs.
4. **Check consistency**: make sure the vision supports the mission; refine it with the user where needed.
5. **Persist**: write to the path the project agreed on; create `docs/project-overview/` when it is missing.

---

## Input and Output

**Input**:

- **Required**: the mission (the statement itself, or the path to the mission document); project/product context.
- **Optional**: an existing vision draft, a time horizon, the audience.

**Output**:

- **Artifact**: the vision statement (1–3 sentences).
- **Location**: `docs/project-overview/vision.md` (or per the project norms).
- **Content**: the vision statement; optionally (YAGNI: only where there is a real need) a "mission alignment" or "time horizon" note.
- **Lifecycle**: living (updated when the strategic direction changes).

---

## Limits

### Hard Boundaries

- Do not put a north star metric, strategic goals, OKRs or milestones into the vision statement.
- Do not overwrite an existing vision file without explicit user confirmation.
- Do not produce more than one vision document; this skill emits the vision artifact alone.
- **YAGNI**: the vision document centres on the statement; add no optional paragraph that earns nothing.

### Skill Boundaries (avoid overlap)

**Do not do these (other skills own them)**:

- **Mission**: the fundamental purpose → Use `define-mission`
- **North star metric**: the single key metric → Use `define-north-star`
- **Strategic goals**: 3–5 outcomes → Use `design-strategic-goals`
- **Milestones**: stage checkpoints → Use `define-roadmap`
- **Roadmap, requirements or backlog** → Use `capture-work-items` and the like

**When to stop and hand off**:

- The user says "approved" or equivalent → the vision is done, hand off to `define-north-star` or `design-strategic-goals`
- The user asks for "a metric" or "a north star" → Hand off to `define-north-star`
- The user asks about goals or milestones → Hand off to `design-strategic-goals` or `define-roadmap`

---

## Self-Check

### Core success criteria (all of them must hold)

- [ ] **A vision statement exists**: one to three sentences, future state only (no metric, goal or milestone).
- [ ] **Consistent with the mission**: it does not contradict the mission, or the missing mission is noted and confirmed by the user.
- [ ] **User confirmation**: the user said "approved", "looks good", "go ahead" or similar.
- [ ] **Persisted as a document**: written to the agreed path (default `docs/project-overview/vision.md`, or the project norms).
- [ ] **Scope respected**: the statement carries no north star, goal or milestone.
- [ ] **YAGNI/DRY/concision**: follows the document-artifact principles in spec §4.

### Process quality checks

- [ ] **The mission was used**: was the mission read or asked for before the vision was drafted?
- [ ] **Future state only**: were metrics and OKRs kept out of the mix?
- [ ] **The quality guide**: was the vision quality guide applied (concision, consistency with the mission, imaginability, no buzzwords)?
- [ ] **Document-artifact principles**: were YAGNI, DRY and concision followed (spec §4)?

### Acceptance test

**Can a reader tell what long-term future the project is trying to create, and see that it supports the mission?**

If not: the vision is incomplete or misaligned. Refine it against the mission and check again.
If yes: the vision is done. Continue to the handoff, or stop.

---

## Examples

### Example 1: defining a vision when the mission already exists

**Context**: the mission reads "We exist to give engineering teams one reliable way to take a service from code to production." The user asks for a vision.

**Flow**: elicit the 2–5 year aim, such as "every team ships to production in 5 minutes with a single click, with full audit and rollback." Draft the vision; check that it supports the mission. The user confirms. Write to `docs/project-overview/vision.md`.

**Result**: the vision is persisted; hand off to `define-north-star` (for instance "successful deployments per week within 5 minutes") or `design-strategic-goals`.

### Example 2: the mission is not defined yet (edge case)

**Context**: the user asks to "define our vision", but no mission document exists.

**Flow**: ask whether to assume a purpose from the README or the surrounding context, or suggest running `define-mission` first. If the user chooses to continue, note the assumed purpose in the vision document; draft the vision and confirm it with the user. Persist it, and suggest filling in the mission later to complete the strategy chain.

**Result**: the vision is persisted with an optional "assumed purpose" note; the user can run `define-mission` later to complete the chain.
