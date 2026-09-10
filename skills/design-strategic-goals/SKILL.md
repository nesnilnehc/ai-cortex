---
name: design-strategic-goals
description: Define 3–5 long-term strategic goals that move the project toward the vision and North Star. Produces a goals document aligned with mission, vision, and NSM; persisted to docs.
description_zh: 定义 3–5 个推动项目走向 vision 与 North Star 的长期战略目标；产出 goals 文档。
tags: [documentation, workflow]
version: 1.3.0
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

#Skill: Design Strategic Goals

## Purpose

Define **3-5 long-term strategic goals** that move the project toward the vision and the North Star. Produce an outcome-centred goals document (not a task list or a roadmap). Does not define mission, vision, North Star, or milestones.

---

## Core Objective

**Primary goal**: produce a user-confirmed strategic goals document holding 3-5 outcome-centred goals aligned with the vision and the North Star, persisted to the path agreed for the project.

**Success criteria** (all must be met):

1. ✅ **3-5 goals recorded**: exactly 3-5 strategic goals, each with a clear title and a short description.
2. ✅ **Outcome-centred**: each goal describes an outcome whose attainment can be judged, not a task list, a feature list, or a restatement of a pillar direction.
3. ✅ **Aligned with the vision**: every goal supports the vision; the alignment is stated or self-evident.
4. ✅ **North Star link**: at least one goal explicitly supports or moves the North Star metric; optional: a short note per goal on "how this supports the vision/NSM".
5. ✅ **User confirmation**: the user explicitly approves (e.g. "approved", "looks good", "go ahead", or equivalent).
6. ✅ **Document persisted**: written to the agreed path (default `docs/project-overview/strategic-goals.md`, or per project norms).
7. ✅ **Engineering-health goal included**: a long-term project (planning horizon > 6 months) must include a goal of the "sustainable engineering / governance health" kind; a short-term or experimental project may take an explicit exemption and record the reason in the document. Rationale: without a strategic sponsor, governance / tech-debt / documentation work never wins capacity in the competition for value.

**Acceptance test**: can a reader see how each of the 3-5 goals advances the vision and the North Star, with no dates or stages (those belong to milestones)? Does a long-term project carry one goal that speaks for governance / engineering health?

**Handoff point**: once the goals are approved and persisted, hand off to "define-roadmap" to break the goals into stage checkpoints, or stop.

---

## Scope Boundaries

**This skill does**:

- Elicit and record 3-5 long-term strategic goals.
- Ensure alignment with the vision and the North Star (read from the "define-vision" / "define-north-star" output, or from existing documents).
- Persist to the path agreed for the project (default "docs/project-overview/strategic-goals.md").
- Optional: a note per goal explaining how it supports the vision or the North Star.

**This skill does not do**:

- Define the mission, vision, or North Star (use "define-mission", "define-vision", "define-north-star").
- Break goals into stages or dates (use "define-roadmap").
- Write requirements, roadmaps, or backlog (use "analyse-requirements", "project-planning", "capture-work-items").

---

## Use Cases

- **After the vision and the North Star**: set 3-5 strategic outcomes that advance the vision and move the NSM.
- **Annual or quarterly strategy**: define or update strategic priorities.
- **When the backlog lacks goal alignment**: create explicit goals so the roadmap and the backlog can trace to them.
- **The fourth layer of the strategy chain**: follows mission, vision, and North Star when the full hierarchy is being built.

---

## Behavior

### Interaction Policy

- **Default**: the output path from project norms if one exists; otherwise "docs/project-overview/strategic-goals.md". Read the vision and the North Star from "docs/project-overview/" if they are there.
- **Cold-start fallback**: when `vision.md` and `north-star.md` are **both** missing, do not halt; switch to "Cold-Start Fallback Mode" below and infer candidate goals from repository evidence. When only one is missing, stay on the normal path and derive from the one that exists.
- **Choice of options**: if the user has more than 5 candidate goals, offer to rank or cluster them into 3-5; ask the user to confirm the final set.
- **Confirm**: before overwriting an existing strategic goals file; before the final persist.

### Execution Process

1. **Load the vision, North Star, and strategic pillars**: read `docs/project-overview/vision.md`, `docs/project-overview/north-star.md`, and `docs/project-overview/strategic-pillars.md` (where present), or a summary supplied by the user.
   - Both missing → switch to "Cold-Start Fallback Mode"; the remaining steps are unchanged.
2. **Work backwards from the North Star metric**: ask "what must be true for the North Star metric to grow?" Each "must be true" is a candidate goal. Goals climb in layers, from base capability to refinement.
3. **Draft the goals**: focus on outcomes (e.g. "cut deployment time to under 5 minutes for 80% of teams"); not a task list or a feature list.
4. **Engineering-health goal check**:
   - Ask about or judge the project's planning horizon (> 6 months counts as a long-term project).
   - Long-term project whose draft has no engineering / governance health goal → ask the user whether to bring in the default template (see "Engineering-Health Goal Template" below); the user can adjust the key results to fit the project.
   - Short-term or experimental project where the user takes the exemption → record the "exemption rationale" at the end of the document.
5. **Check alignment**: every goal supports the vision; at least one explicitly supports the North Star.
6. **Persist**: write to the path agreed for the project; create "docs/project-overview/" if it is missing. Optional: add "how this supports the vision/NSM" to each goal.

### Cold-Start Fallback Mode

**Trigger**: `vision.md` and `north-star.md` are both missing. Working backwards from the North Star then has no basis, but the repository itself is an extractable evidence source — this must not degrade into interrogating the user from scratch, item by item.

**Extraction sources** (ordered by intent density; work down the list and stop once you have enough):

1. `README.md` / `AGENTS.md` / `CLAUDE.md` — the intent the project states about itself
2. `CHANGELOG.md` — where effort actually went; the highest intent density
3. Recent git log — same as above; **the two are independent, and git log on its own is enough when CHANGELOG is missing** — do not skip this level because one of the two is absent
4. Code directory structure and dependency manifest — the capability boundary
5. Existing backlog / issues — unmet needs
6. The rest of `docs/`

**Safety constraints (not omissible)**: a goal inferred from evidence reads as coherent and fluent — which is exactly why it is most likely to be invention filling a blank. So:

- Every candidate goal must carry an "inference basis" pointing at a specific file and location. **A goal whose basis cannot be derived must not be written**
- Mark everything as inferred rather than confirmed. **Must not persist automatically**; the user must confirm or correct each item
- Leave a marker at the top of the persisted document: `> This batch of goals lacks vision / North Star backing and is a temporary anchor; once the upstream is in place this skill must be rerun`
- Tell the user plainly: this is fallback output, and the normal path is to run `define-vision` and `define-north-star` first

**Output shape**:

```markdown
## Candidate Goal N: <goal title>

**Description**: <one outcome-centred sentence>

**Inference basis**:
- The last 5 `CHANGELOG.md` entries cluster on direction X
- `README.md` line 12 states the goal as Y

**To confirm**: this goal was inferred from evidence — confirm it, correct it, or delete it
```

### Engineering-Health Goal Template (Default)

A long-term project must hold a goal of this kind (tune the specific key results per project):

```markdown
## Goal N: Sustainable Engineering and Governance Health

**Description**: keep the project's code quality, documentation consistency, and
governance mechanisms evolving, so the other strategic goals stay achievable long-term.

**Key results** (illustrative; tune per project):
- Core documentation norms (ARTIFACT_NORMS) 100% compliant
- ADR coverage ≥ 90% (every architecture decision is documented)
- Tech-debt backlog item count ≤ X (set by team size)
- Governance health matrix pass rate ≥ 95% (plan-next output)
- Production incident MTTR ≤ Y hours
```

This goal **supports the long-term achievability of all the other strategic goals**; it is not a standalone product goal. Its existence guarantees that governance / tech-debt / documentation groundwork holds a legitimate strategic position in the competition for value — the capacity guardrail allocates by strategic_goal, and without this goal such work has no capacity to belong to.

---

## Input & Output

**Input**:

- **Required**: project context.
- **Required on the normal path**: the vision; the North Star (or paths to the vision/North Star documents). When both are missing, switch to cold-start fallback mode and infer from repository evidence.
- **Optional**: mission; time horizon; existing goals or priorities.

**Output**:

- **Artifact**: the strategic goals document.
- **Location**: `docs/project-overview/strategic-goals.md` (or per project norms).
- **Content**: 3-5 strategic goals (title + short description); optional: links to the vision/NSM, and a "how this supports the vision/NSM" note per goal.
- **Lifecycle**: living (reviewed on the strategy cycle).

---

## Restrictions

### Hard Boundaries

- Do not define the mission, vision, North Star, or milestones in this skill.
- Do not put dates or stages in the goals document (those belong to "define-roadmap").
- The document must not carry fewer than 3 or more than 5 strategic goals.
- A long-term project (planning horizon > 6 months) must not drop the engineering / governance health goal entirely; an exemption must record its reason in the document.
- **Must not persist automatically in fallback mode**: an evidence-inferred candidate goal is written only after the user confirms or corrects each item.
- **Must not write an unsupported goal in fallback mode**: every candidate goal must point at a specific extraction-source file and location; where no basis can be derived, leave it out.

### Skill Boundaries (no overlap)

**Do not do these (other skills handle them)**:

- **Mission**: why we exist → use `define-mission`.
- **Vision**: what future we are building → use "define-vision".
- **North Star**: the single metric → use `define-north-star`.
- **Milestones**: stage checkpoints → use `define-roadmap`.
- **Requirements or backlog**: use "analyse-requirements", "capture-work-items", project planning.

**When to stop and hand off**:

- The user says "approved" or equivalent → the goals are done; offer the handoff to "define-roadmap".
- The user asks for stages or milestones → hand off to "define-roadmap".

---

## Self-Check

### Core Success Criteria (all must be met)

- [ ] **3–5 goals recorded**: exactly 3–5 strategic goals, with titles and descriptions.
- [ ] **Outcome-focused**: every goal is an outcome or a result, not a task list.
- [ ] **Aligned with the vision**: every goal supports the vision.
- [ ] **North Star link**: at least one goal explicitly supports or moves the North Star (not applicable in fallback mode; the next item replaces it).
- [ ] **Fallback-mode compliance** (fallback path only): every goal carries an inference basis pointing at a specific file; each has been confirmed by the user; the document header carries the "no upstream backing, temporary anchor" marker.
- [ ] **Engineering-health goal**: a long-term project holds an engineering / governance health goal; an exemption has its reason recorded.
- [ ] **User confirmation**: the user said "approved", "looks good", "go ahead", or similar.
- [ ] **Document persisted**: written to the agreed path (default `docs/project-overview/strategic-goals.md`, or project norms).

### Process Quality Checks

- [ ] **Vision/NSM used**: did I read or request the vision and the North Star before drafting goals?
- [ ] **No dates or stages**: did I avoid putting milestones or timelines into the goals document?
- [ ] **Goals are not restated pillars**: each goal describes an outcome whose attainment can be judged, not an ongoing direction.
- [ ] **Goals may span pillars**: one goal can touch several pillars; goals and pillars need not map one to one.
- [ ] **Layered progression**: the goals hold a clear layering from base capability to refinement.

### Acceptance Test

**Can a reader see how each goal advances the vision and the North Star with no dates or stages?**

If no: the goals are probably too tactical, or the alignment is missing. Sharpen the outcomes and state the alignment.
If yes: the strategic goals are done. Move to the handoff or stop.

---

## Examples

### Example 1: Full hierarchy in place

**Context**: the vision and the North Star exist. The user wants 3-5 strategic goals.

**Process**: read the vision and North Star documents. Derive outcomes (e.g. "80% of teams deploy within 5 minutes", "zero manual steps in a standard deployment", "a complete audit trail for every deployment"). Draft 3-5 goals; state how each supports the vision/NSM. The user confirms. Write to "docs/project-overview/strategic-goals.md".

**Result**: the goals are persisted; offer the handoff to "define-roadmap".

### Example 2: The user proposes six goals

**Context**: the user lists six candidate goals; the plan allows only 3-5.

**Process**: cluster or rank them down to 3-5 (e.g. merge two related goals, or drop the lowest-ranked one). Present the set of 3-5 with the rationale; ask the user to confirm or adjust. Make sure each one is outcome-centred and aligned with the vision/NSM. Persist once confirmed.

**Result**: the document holds exactly 3-5 goals; the user explicitly approved the set.

### Example 4: Cold-start fallback (edge case)

**Context**: a newly inherited repository holds only a README and source code; `docs/project-overview/` is empty. The user wants the strategic goals stood up first.

**Process**:

1. Detect that `vision.md` and `north-star.md` are both missing → switch to fallback mode, and tell the user this is fallback output.
2. Scan in extraction-source order: the README states "let small and mid-sized teams run a private deployment with no ops work"; the last 8 CHANGELOG entries cluster on the install script and cross-platform compatibility; 5 backlog items are complaints about missing documentation.
3. Infer 3 candidate goals, each with its basis:
   - Candidate 1 "install and it runs" ← the README:3 statement + the direction of the last 8 CHANGELOG entries
   - Candidate 2 "documentation is self-service" ← 5 backlog complaints
   - Candidate 3 "sustainable engineering and governance health" ← required for a long-term project
4. Present the candidate list, marked "inferred from evidence — confirm, correct, or delete", and **write nothing to disk**.
5. The user rewords candidate 2 and confirms the other two.
6. Write the document with a marker at the top: `> This batch of goals lacks vision / North Star backing and is a temporary anchor; once the upstream is in place this skill must be rerun`.
7. Tell the user: the normal path is to run `define-vision` and `define-north-star` first, then rerun this skill once they are in place.

**Result**: the chain does not spin at its starting point; the output is usable but explicitly marked as temporary, and every item's source can be looked up.

### Example 3: Long-term project with no engineering-health goal (edge case)

**Context**: the user drafted 4 strategic goals, all user- or market-oriented; the planning horizon is 12 months (a long-term project).

**Process**:
1. Detect that none of the 4 goals touches engineering / governance health.
2. Tell the user: "This is a long-term project; an engineering-health goal is recommended here, otherwise tech-debt and governance work has no strategic sponsor over the long run and the capacity guardrail has nothing to attach to."
3. Show the default template; the user tunes the key results (e.g. "tech-debt backlog item count ≤ 20" becomes "≤ 30", based on team size).
4. The user confirms it as goal 5.
5. Persist the 5 goals.

**Result**: the document holds 5 strategic goals, goal 5 being "sustainable engineering and governance health". The capacity guardrail then has a legitimate slot when it allocates by strategic_goal_id.
