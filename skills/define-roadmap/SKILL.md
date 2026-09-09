---
name: define-roadmap
description: Derive a strategic roadmap from goals using milestone checkpoints, strategic bets, success metrics, and promotion criteria. Produces a decision-grade roadmap document.
description_zh: 从战略目标推导路线图，包含里程碑、关键举措、成功指标与推进条件，产出可用于决策的路线图文档。
tags: [documentation, strategy, workflow]
version: 4.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [define roadmap, roadmap, milestones, strategic roadmap, phase planning]
input_schema:
  type: free-form
  description: Strategic goals (document or path); project context; optional vision/NSM; time horizon or phase preference
output_schema:
  type: document-artifact
  description: Decision-grade roadmap document with milestones, strategic bets, success metrics, and promotion criteria
  artifact_type: roadmap
  path_pattern: docs/process-management/roadmap.md
  path_alt: docs/process-management/milestones.md
  lifecycle: living
---

# Skill: Define Roadmap

## Purpose

Derive a "decision-driving roadmap" from the strategic goals, not a task list. A roadmap is not a set of milestones; it is an **expression of the path**.

---

## Core Objective

**Primary goal**: produce a user-confirmed, decision-driving roadmap document in which every stage explicitly carries a milestone, strategic bets, success metrics, and promotion criteria.

**Success criteria** (all must be met):

1. ✅ **Core model complete**: every stage must carry a Milestone, Strategic Bets, Metrics, and Promotion Criteria.
2. ✅ **Ordered structure, visible path**: stages are split by **Now / Next / Later**, showing the evolution path.
3. ✅ **Outcome- and metric-driven**: success metrics must be written as a triplet (current value / target value / frame of reference); milestones are outcome-driven, never a feature list or mixed-in TODOs. Criteria in [rules/roadmap-quality.md](../../rules/roadmap-quality.md).
4. ✅ **No false precision**: the Later stage states direction only and **carries no specific dates**.
5. ✅ **Goal traceability and constraint**: a goal mapping exists, and the constraint is stated explicitly: "the backlog must map to the roadmap; a requirement outside the roadmap is not done by default".
6. ✅ **User confirmation and persistence**: the user explicitly approves, and the document is written to the agreed path (default `docs/process-management/roadmap.md`, or `milestones.md` per project norms).
7. ✅ **Capacity allocated by strategic_goal**: the roadmap must declare the **total capacity baseline** for the current cycle, plus each strategic_goal's percentage of that baseline; the percentages must sum to 100%. The percentages are settled by the user and must not be inferred by this skill — for the capacity guardrail to control by strategic goal, there has to be a denominator that is attributable and that the user owns.

**Acceptance test**: can a reader see the evolution path at a glance, promotion criteria included? Can the stage outcome be verified through the success metrics rather than by checking a task list?

**Handoff point**: once the roadmap is approved and persisted, hand off to backlog planning (`capture-work-items`) or routing diagnosis (`plan-next`).

---

## Scope Boundaries

**This skill does**:

- Derive the stages from the strategic goals and split them (Now / Next / Later).
- Define the milestone, strategic bets (2–5), success metrics, and promotion criteria for each stage.
- Organise and generate the structured roadmap document.
- Persist to the path agreed for the project.

**This skill does not do**:

- Define the mission, vision, North Star, or strategic goals (use `define-mission`, `define-vision`, `define-north-star`, `design-strategic-goals`).
- Write concrete requirements (use `capture-work-items`); task breakdown is taken on by a runtime platform such as AgentFabric.
- Create concrete backlog items (use `capture-work-items`).

---

## Use Cases

- **After the strategic goals are set**: high-level strategic goals need turning into concrete stages, strategic bets, and metrics.
- **Stage transition assessment**: the "promotion criteria" (Next → Now) decide whether the team can enter the next stage.
- **Planning and alignment meetings**: give the team and stakeholders a clear expression of the path and a basis for decisions, and weed out scattered requirements that do not fit the current path.

---

## Behavior

### Interaction Policy

- **Default**: output to `docs/process-management/roadmap.md`, or follow the project's existing norms. Read `docs/project-overview/strategic-goals.md` automatically as the input basis.
- **Inference and confirmation**: distil the strategic bets and metrics from the current project state or context; before a core decision, and before overwriting an existing document, ask the user for explicit confirmation.

### Execution Process

1. **Load the strategic goals**: read the existing strategic goals and the project context.
2. **Split the stages**: structure them into a Now / Next / Later view.
3. **Define the milestone**: write it as an outcome sentence — `let [segment] be able to [achieve something], so that [business impact]` — keeping it driven by outcome rather than by deliverable.
4. **Distil the strategic bets**: distil 2–5 Strategic Bets per stage, each written as a falsifiable hypothesis — `we believe [doing X] brings [result] for [audience], because [assumption]`. A bet must be falsifiable, or it degenerates into a noun phrase.
5. **Define the success metrics**: set the verification standard for the stage outcome, each written as a triplet — current value / target value / frame of reference. The frame of reference is an industry benchmark, a project historical value, or an empirical threshold; where there is none, write "project-defined (no external benchmark)". This format shares one set of criteria with the `plan-next` diagnostic self-check; see [rules/roadmap-quality.md](../../rules/roadmap-quality.md).
6. **Define the promotion criteria**: state the precondition for entering the next stage (such as the switch condition for Next → Now).
7. **Build the goal mapping**: make sure the stage goals and the backlog can map to the strategy.
8. **Settle the total capacity baseline**: ask for the capacity available in the current cycle. It is the denominator of the downstream `promote-roadmap-items` capacity formula, and without it the whole guardrail computes nothing.
   - Collection basis: engineer headcount × cycle length − known overheads (meetings, oncall, interviews, holidays)
   - Discount to 60–70% effective working hours; prefer the user's measured value where one exists
   - Write the result, in person-weeks, into the header of the "Capacity Allocation" section
   - **The buffer is deducted here**: the percentages that follow are relative to this effective capacity, not to calendar capacity. Room for unplanned work (urgent issues, quick wins, requests from other teams) was already given up in the discount, and gets no separate slot
9. **Settle the capacity allocation**: ask the user for each strategic_goal's percentage of the total capacity baseline for the current cycle.
   - Present the strategic-goals list and ask item by item, or ask the user for the whole allocation in one go
   - Check that the percentages sum to 100%; where they do not, halt and prompt for a correction
   - A default split is suggested (example: user value 60% / market expansion 20% / engineering health 20%), but the user settles it
   - The ratio can be tuned to the project stage: a new product leans to features, a mature product to tech debt, the aftermath of an incident to reliability, a fast-growth period to scalability
   - **The engineering-health goal must not be 0%** — with no capacity, governance / tech-debt / documentation work never gets in during the competition for value
10. **Generate the roadmap document**: draft the document from the output structure template (including the "Capacity Allocation" section).
11. **Confirm and persist**: once the user confirms, write it out and note the last-updated date.

### Output Structure Template (embedded contract)

```markdown
# Roadmap

## Route Overview

Now / Next / Later (with a brief note on promotion criteria)

## Capacity Allocation (current cycle)

**Total capacity baseline**: <N> person-weeks (<headcount> people × <cycle> − overheads, discounted to <60–70>% effective working hours; the buffer for unplanned work is already deducted in the discount)

| Strategic Goal | Percentage | Capacity | Note |
| Goal 1 (user value) | 60% | 6 person-weeks | Core delivery |
| Goal 2 (market expansion) | 20% | 2 person-weeks | Adjacent expansion |
| Goal 3 (engineering health) | 20% | 2 person-weeks | Governance and tech debt, must not be 0 |

> This allocation is consumed by the `promote-roadmap-items` skill inside its capacity guardrail: allocated capacity = percentage × total capacity baseline.
> The percentages must sum to 100%; the engineering-health goal must not be 0%.
> A strategy refresh or a capacity change must rerun this skill.

---

## Now

### Milestone
- Let [segment] be able to [achieve something], so that [business impact]

### Strategic Bets
- We believe [doing X] brings [result] for [audience], because [assumption]

### Success Metrics
- <metric name>: current <value> / target <value> / frame of reference <industry benchmark | project historical value | empirical threshold | project-defined (no external benchmark)>

---

## Next

### Promotion Criteria
- ...

### Milestone
- ...

### Strategic Bets
- ...

---

## Later

Direction only, no dates

---

## Explicitly Not Doing This Round (optional)

| Excluded item | Reason | When to re-evaluate |

> "A requirement outside the roadmap is not done by default" is an implicit rule, and the reader cannot see what was excluded.
> Listing a stakeholder request that was kept out saves explaining it one person at a time.

---

## Milestone Detail (appendix)

| Milestone | Scope | Metrics | Goals |
```

---

## Input & Output

**Input**:
- **Required**: the strategic goals (document or path); the project context.
- **Optional**: vision / North Star metric; time horizon or stage preference.

**Output**:
- **Artifact**: a decision-grade roadmap document.
- **Location**: `docs/process-management/roadmap.md` or `milestones.md` (per project norms).
- **Content**: the route overview plus the Now/Next/Later detail (milestone, strategic bets, metrics, promotion criteria).
- **Lifecycle**: living (updated continuously as the stages advance).

---

## Restrictions

### Hard Boundaries

- **Roadmap mapping constraint**: state explicitly that "the backlog must map to the roadmap; a requirement outside the roadmap is not done by default".
- **Structure enforced**: every stage must carry the core model (milestone, strategic bets, success metrics, promotion criteria); not one of them may be missing.
- **The total capacity baseline must not be omitted**: with no baseline the downstream capacity formula has no denominator, and the guardrail is decorative.
- **The capacity allocation must not be omitted**: every strategic_goal must have a percentage, summing to 100%; the engineering-health goal must not be 0%.
- **The capacity allocation must not be inferred by this skill**: the user must settle it; a suggestion can be offered, but nothing is written automatically.
- **No overwrite**: do not overwrite an existing roadmap file without the user's explicit confirmation.

### Anti-Patterns (avoid)

- **Feature list**: degrading the roadmap into a pile of features.
- **Mixed-in TODOs**: blending in execution-level tasks.
- **No metrics**: no way to verify whether a milestone was reached.
- **No strategic bets**: goals with no matching strategic action.
- **False precision**: writing specific dates or times into the Later stage.

### Skill Boundaries (avoid overlap)

**Do not do these (other skills own them)**:
- **Define the strategic goals**: use `design-strategic-goals`.
- **Break down concrete requirements**: use `capture-work-items`; task breakdown is taken on by a runtime such as AgentFabric.
- **Write the backlog**: use `capture-work-items`.

**When to stop and hand off**:
- The user replies "approved / confirmed" or similar → the roadmap is done; persist the document and hand off to `plan-next` or to backlog planning.

---

## Self-Check

### Core Success Criteria (all must be met)

- [ ] **Core model complete**: the document carries the milestone, strategic bets, success metrics, and promotion criteria.
- [ ] **Ordered structure, visible path**: the roadmap shows the evolution path through Now / Next / Later.
- [ ] **Outcome- and metric-driven**: the content is outcome-driven, with no feature or TODO list; milestones use the outcome sentence, strategic bets the hypothesis sentence.
- [ ] **Metric triplet**: every success metric carries current value / target value / frame of reference; where there is no frame of reference, "project-defined (no external benchmark)" is marked.
- [ ] **No false precision**: the Later stage carries no specific dates, only direction.
- [ ] **Goal traceability and constraint**: the mapping from roadmap to strategic goals is shown, and the backlog is constrained.
- [ ] **Total capacity baseline declared**: with the person-week count and the discount basis.
- [ ] **Capacity allocation complete**: every strategic_goal has a percentage, they sum to 100%, and engineering health is ≠ 0%.
- [ ] **User confirmation and persistence**: the user approved it, and it is written to the agreed path.

### Acceptance Test

Can a reader see the evolution path at a glance, promotion criteria included? Can the stage outcome be verified through the success metrics rather than by checking a task list?

- If no: add the success metrics or the promotion criteria, and strip out the feature TODO list.
- If yes: the roadmap meets the production bar; move on to the handoff.

---

## Examples

### Example 1: Generate a production-grade roadmap from the strategic goals

**Context**: strategic goals carrying 3 metrics already exist; an evolution path is needed.
**Process**:
1. Read the goals and split them into the Now / Next / Later view.
2. Define 3 explicit strategic bets and quantified success metrics for Now.
3. Define the "promotion criteria" for the Next stage (e.g. "start the Next stage when core architecture validation reaches 10k QPS").
4. List the long-range exploration themes in Later (no dates).
5. Present the draft, and write to `docs/process-management/roadmap.md` once it is approved.
**Result**: the roadmap is persisted and drives the next round of resource allocation and decisions.

### Example 2: Correcting the task-list anti-pattern

**Context**: the user asks "turn these backlog tasks into a scheduled roadmap for me".
**Process**:
1. State this skill's principle to the user: a roadmap is an expression of the path and a decision model, not a task list.
2. Abstract the concrete backlog into matching strategic bets and stage milestones.
3. Add the success metrics and promotion criteria for each stage, and remove the fine-grained TODOs.
4. Offer the draft and confirm it with the user.
**Result**: the requirement list is converted into a production-grade decision roadmap.

### Example 3: Capacity allocation is required (edge case)

**Context**: the user drafts a roadmap but skips the capacity allocation section and asks to persist it as is.
**Process**:
1. Detect that the roadmap has no "capacity allocation".
2. halt and explain: "capacity allocation is what promote-roadmap-items uses as its guardrail; without it, promotion cannot be controlled by strategic goal."
3. Present the strategic-goals list:
   - Goal 1 (user value): ? %
   - Goal 2 (market expansion): ? %
   - Goal 3 (engineering health): ? %
4. Fill in the total capacity baseline first: 4 people × 6 weeks × 65% ≈ 10 person-weeks.
5. The user gives 70/20/10.
6. Check the sum = 100 ✓; engineering health at 10% is not 0 ✓; that converts to 7 / 2 / 1 person-weeks.
7. Write the "Capacity Allocation" section and persist.
**Result**: the roadmap carries a capacity allocation that promote-roadmap-items can consume, and the loop closes.
