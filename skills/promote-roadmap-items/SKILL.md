---
name: promote-roadmap-items
description: Promote prioritized backlog items into the roadmap's Now/Next/Later tiers based on strategic_goal capacity allocation and priority scores. Event-driven (not calendar-driven).
description_zh: 把已评分的 backlog 条目按 strategic_goal 容量分配晋升进 roadmap 的 Now/Next/Later 槽位；事件驱动，不绑定固定周期。
tags: [workflow, automation, meta-skill]
version: 1.2.1
license: MIT
recommended_scope: project
cognitive_mode: interpretive
metadata:
  author: ai-cortex
triggers: [promote roadmap, roadmap planning, pull items, release planning]
input_schema:
  type: free-form
  description: Priority-scored backlog items, current roadmap, strategic_goal capacity allocation
output_schema:
  type: chat
  description: Promotion/demotion decisions for Now/Next/Later tiers + capacity usage report + updated roadmap.md
---

# Skill: Promote Roadmap Items

## Purpose

Promote scored backlog items into the roadmap's Now / Next / Later slots according to the strategic-goal capacity allocation. This is the supporting skill for the **roadmap planning ceremony**, and it is event-driven.

---

## Core Objective

**Primary goal**: decide which items are promoted / demoted / held, based on the current strategic-goal capacity allocation and the backlog priorities, and update roadmap.md.

**Success criteria** (all of them must hold):

1. ✅ Backlog items with a priority set were read (unset ones skipped)
2. ✅ The capacity used and remaining in each roadmap tier (Now/Next/Later) was computed
3. ✅ Promotion candidates were presented against the strategic_goal capacity allocation (from roadmap.md or the strategy setup)
4. ✅ The user confirmed every promotion / demotion decision
5. ✅ roadmap.md and the status field of each promoted item were updated
6. ✅ A capacity usage report was emitted (used / total / remaining per goal)

**Acceptance test**: after promotion, can a reader see straight from roadmap.md which strategic_goal each Now item came from and what its priority is?

---

## Scope Boundaries

**This skill owns**:

- Backlog → Roadmap promotion / demotion decisions
- Holding to the strategic_goal capacity guardrail
- Updating roadmap.md and the status of the promoted items

**This skill does not own**:

- Creating new backlog items (`capture-work-items`)
- Scoring backlog items (`prioritize-backlog`)
- Defining the roadmap's base structure / milestones (`define-roadmap`)
- Task breakdown (the AgentFabric runtime takes it)
- Requirement capture (`capture-work-items`)

**Handoff point**: promoted Now-tier items go into `capture-work-items` as needed, and the AgentFabric runtime then carries out design / task breakdown / execution.

---

## Use Cases

- **Capacity freed**: the previous batch of Now-tier items finished, capacity came free, and new items need pulling in
- **Strategy refresh**: after the strategic goals shift, re-assess whether the Now-tier items still fit
- **Filling a large gap**: a large gap reported by `plan-next` reaches the promotion decision after capture + prioritize
- **Planning on demand**: the user starts roadmap planning themselves, tied to no fixed cycle

---

## Behavior

### Stage 0: read the inputs

1. Read `docs/process-management/roadmap.md` (the current Now / Next / Later state)
2. Read the backlog directory and select the items whose `priority` is set (not unset) **and whose `status` is not `declined`** — `declined` is the terminal state for never doing it, written by `prioritize-backlog`, and it takes no part in promotion
3. Read `docs/project-overview/strategic-goals.md` (the list of strategic goals)
4. Read the strategic-goal capacity allocation declared in roadmap.md (see Stage 1)

**halt conditions**:
- roadmap.md does not exist → suggest running `define-roadmap` first
- strategic-goals.md does not exist → suggest running `design-strategic-goals` first
- every backlog item is `priority: unset` → suggest running `prioritize-backlog` first
- roadmap.md carries no capacity allocation, or no total capacity baseline → halt, and prompt for a `define-roadmap` run to settle the capacity

### Stage 1: compute the current capacity state

The **total capacity baseline** comes from the header of the "Capacity allocation" section in roadmap.md, gathered and written by step 8 of `define-roadmap` (headcount × cycle − overhead, converted into effective working hours). When the baseline is missing, halt and prompt for a rerun of `define-roadmap` — with no denominator, no goal's allocated capacity can be worked out.

For each strategic_goal:

| Field | Meaning |
|---|---|
| Allocated capacity | that goal's percentage in roadmap.md × the **total capacity baseline** |
| Used capacity | the sum of effort across the current Now-tier items belonging to that goal |
| Remaining capacity | allocated - used |

Emit the capacity table:

```markdown
## Current capacity usage

| Strategic Goal | Allocated | Used | Remaining | Share |
| Goal 1 (user value) | 6 person-weeks | 4 person-weeks | 2 person-weeks | 67% |
| Goal 2 (market expansion) | 2 person-weeks | 1 person-week | 1 person-week | 50% |
| Goal 3 (engineering health) | 2 person-weeks | 0 person-weeks | 2 person-weeks | 0% |
```

### Stage 2: generate promotion candidates

**Now-tier admission rule**: the 3–5 top-ranked items that carry no unresolved prerequisite. Both conditions hold.

The dependency check reads each item's frontmatter `depends_on` (registered by `map-item-dependencies`):

| `depends_on` state | Handling |
|---|---|
| `—` (checked, no dependency) | may enter Now |
| has dependencies, and every prerequisite is already in Now or finished | may enter Now |
| has dependencies with an unresolved prerequisite | **must not enter Now**; Next is as far as it goes, and the candidate table names which one blocks it |
| field missing (never checked) | do not wave it through silently. Prompt for a `map-item-dependencies` run first; when the user insists on continuing, mark it "dependencies unchecked" in the candidate table and leave the risk with the user |

For each strategic_goal:

1. Select the backlog items belonging to that goal
2. Sort by `priority` (P0 > P1 > P2 > P3)
3. Pull from the highest priority downward against the remaining capacity, until that goal's capacity is full or no items are left

Emit the promotion candidate table:

```markdown
## Promotion candidates (Now tier)

| Goal | Item | Priority | Effort | Action |
| Goal 1 | #42 payment optimization | P0 | 2w | promote Later → Now |
| Goal 3 | #17 tech debt: auth refactor | P1 | 2w | promote Backlog → Now |
```

### Stage 3: demotion / deferral decisions

Check the current Now-tier items:

- if the priority has dropped (a re-score after a strategy change, say) → suggest demoting it to Next or Later
- if a strategic_goal is over its capacity → suggest demoting the lowest-priority item

Emit the demotion suggestions.

### Stage 4: the user confirms each decision

Present the merged list (promotions + demotions) and have the user confirm item by item:

```markdown
## Confirmation list

[ ] #42 promote Later → Now?
[ ] #17 promote Backlog → Now?
[ ] #8 demote Now → Next? (over capacity + low priority)
[ ] ...
```

### Stage 5: persist

For each confirmed decision:

1. Update the item's frontmatter `status` (`captured` → `active` on entering Now; `active` → `deferred` on demotion)
2. Update roadmap.md, adding / removing the matching item reference
3. Write the `promoted_at` / `demoted_at` timestamp into the item's frontmatter

### Stage 6: emit the final report

- Counts promoted / demoted / held
- Capacity usage after the update
- The suggested next step (`capture-work-items` for the newly promoted Now items, for example)

---

## Input and Output

**Input**: roadmap.md + the backlog (priority set) + strategic-goals.md + the capacity allocation.

**Output**: the decision table in chat + the roadmap.md update + the item frontmatter update (status + promoted_at / demoted_at).

---

## Restrictions

### Hard Boundaries

- Do not promote a `priority: unset` item (go through `prioritize-backlog` first)
- Do not promote a `status: declined` item — that terminal state means never doing it, and taking it back in needs the user to lift the terminal state explicitly
- Do not exceed a strategic_goal's capacity allocation (when it is over capacity, something must be demoted before anything is promoted)
- Do not promote a P3 item into Now automatically (P3 goes to Later by default)
- Do not promote an item with an unresolved prerequisite into Now (clear the prerequisite first, or promote only as far as Next)
- Do not change the roadmap's strategic_goal capacity allocation automatically (that is `define-roadmap`'s job)

### Skill boundaries

**Not done here (other skills own it)**:

| Action | Owner |
|---|---|
| Creating backlog items | `capture-work-items` |
| Scoring the backlog | `prioritize-backlog` |
| Defining roadmap structure and capacity | `define-roadmap` |
| Breaking a Now item into tasks | AgentFabric runtime (outside AI Cortex) |
| Detailed requirement capture | `capture-work-items` |

---

## Anti-Patterns

- ❌ **Do not tie it to a fixed cycle** ("run it every Monday") — this skill is **event-driven** (capacity freed / strategy change / on demand)
- ❌ **Do not ignore the capacity guardrail** — one goal holding a high-priority item is no licence to overrun and take another goal's capacity
- ❌ **Do not promote too much at once** — the Now tier caps at **3–5 items** by default (a project can override it in roadmap.md), and stacking past that cap breaks the pull-based flow
- ❌ **Do not act on priority-unset items** — score them first
- ❌ **Do not skip the dependency check** — high priority does not mean it can be pulled now; a blocked item in Now just holds capacity and produces nothing
- ❌ **Do not change the roadmap structure** (adding a milestone, say) — that is `define-roadmap`'s business

---

## Self-Check

- [ ] roadmap.md, the backlog and strategic-goals.md were read successfully
- [ ] The capacity allocation exists; where it does not, the run halted and suggested `define-roadmap`
- [ ] Only backlog items with `priority` set and `status` other than `declined` were handled
- [ ] Capacity usage was computed for every strategic_goal
- [ ] Promotion candidates were generated by priority order plus the capacity constraint
- [ ] Now-tier candidates passed the dependency check; items missing `depends_on` were told to run `map-item-dependencies` first, not waved through silently
- [ ] The Now-tier item count stays within the WIP cap (3–5 by default)
- [ ] The demotion suggestions weigh priority and over-capacity
- [ ] The user confirmed item by item; nothing was auto-approved
- [ ] roadmap.md was updated and the item frontmatter was updated
- [ ] The final capacity usage report was emitted

---

## Examples

### Example 1: freed capacity triggers a promotion (the mainstream case)

**Context**: 3 Now items finished during the cycle, freeing 4 person-weeks of capacity. Strategic goals: Goal 1 (60%), Goal 2 (20%), Goal 3 engineering health (20%).

**Flow**:

1. Compute capacity — Goal 3 has 2 weeks free, Goal 1 has 2 weeks free
2. Generate candidates:
   - Goal 1: #42 payment optimization (P0, 2w) → promote Later → Now
   - Goal 3: #17 auth refactor (P1, 2w) → promote Backlog → Now
3. The user confirms item by item (all yes)
4. Update roadmap.md and set the item status to active
5. Capacity report: Goal 1 6/6, Goal 2 1/2, Goal 3 2/2

**Result**: 2 items promoted into Now; the handoff suggests running `capture-work-items` for the new Now items.

### Example 2: a strategy refresh forces a broad re-assessment (edge case)

**Context**: after the quarterly strategy refresh, a new strategic goal 4 joins and Goal 3's capacity moves from 20% to 10%.

**Flow**:

1. halt and check — the capacity allocation in roadmap.md does not reflect the new strategy
2. Prompt: "the strategic goals or the capacity have changed, and this skill cannot handle a structural change. Run `define-roadmap` first to settle the capacity allocation again."
3. The user runs `define-roadmap`, then starts over
4. Re-enter promote-roadmap-items: Goal 3 turns out to be over capacity (2w in Now, new capacity 1w), so suggest demoting #17 to Next
5. The user confirms → update

**Result**: the roadmap lines up with the strategy again; #17 is demoted but not lost.

---
