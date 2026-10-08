---
name: promote-roadmap-items
description: Promote prioritized requirements and defects into the roadmap's Now/Next/Later tiers based on priority scores and dependency readiness. Event-driven (not calendar-driven).
version: 3.0.0
license: MIT
---

# Skill: Promote Roadmap Items

## Purpose

Promote scored backlog items into the roadmap's Now / Next / Later slots in priority order, with strategic-goal traceability and prerequisite checks. This is the supporting skill for the **roadmap planning ceremony**, and it is event-driven.

---

## Core Objective

**Primary goal**: decide which items are promoted / demoted / held, based on backlog priorities and prerequisite readiness, and update roadmap.md.

**Success criteria** (all of them must hold):

1. ✅ Backlog items with a priority set were read (unset ones skipped)
2. ✅ Current items and eligible backlog items were compared in priority order
3. ✅ Promotion candidates carry priority, strategic_goal, dependency readiness, and a reason for their proposed tier
4. ✅ The user confirmed every promotion / demotion decision
5. ✅ roadmap.md and each item's project-defined planning fields were updated without changing approval status
6. ✅ A priority-ordered tier report was emitted with reasons for held or deferred items

**Acceptance test**: after promotion, can a reader see straight from roadmap.md which strategic_goal each Now item came from and what its priority is?

---

## Scope Boundaries

**This skill owns**:

- Backlog → Roadmap promotion / demotion decisions
- Ordering candidates by priority and checking prerequisite readiness
- Updating roadmap.md and project-defined planning fields of promoted requirements and defects

**This skill does not own**:

- Creating new backlog items (`capture-work-items`)
- Scoring backlog items (`prioritize-backlog`)
- Defining the roadmap's base structure / milestones (`define-roadmap`)
- Task breakdown (the AgentFabric runtime takes it)
- Requirement capture (`capture-work-items`)

**Handoff point**: promoted Now-tier items go into `capture-work-items` as needed, and the AgentFabric runtime then carries out design / task breakdown / execution.

---

## Use Cases

- **Items completed**: previous Now-tier items finished and the next priorities need reassessing
- **Strategy refresh**: after the strategic goals shift, re-assess whether the Now-tier items still fit
- **Filling a large gap**: a large gap reported by `plan-next` reaches the promotion decision after capture + prioritize
- **Planning on demand**: the user starts roadmap planning themselves, tied to no fixed cycle

---

## Behavior

### Stage 0: read the inputs

1. Read `docs/process-management/roadmap.md` (the current Now / Next / Later state)
2. Read requirement and defect records in the backlog and select the items whose `priority` is set (not unset) **and whose `status` is not `declined`** — `declined` is the terminal state for never doing it, written by `prioritize-backlog`, and it takes no part in promotion
3. Read `docs/project-overview/strategic-goals.md` (the list of strategic goals)
4. Read each item's current tier, priority rationale, and prerequisite state

**halt conditions**:

- roadmap.md does not exist → suggest running `define-roadmap` first
- strategic-goals.md does not exist → suggest running `design-strategic-goals` first
- eligible records exist but every one is `priority: unset` → suggest running `prioritize-backlog` first
- no eligible records exist → emit an empty candidate report; do not request scoring or fabricate items

Only requirements and defects are candidates. Resolve task-only inputs to their parent
record and consolidate them; never promote task IDs or task groups as rows. Missing
parent registration is handed to `capture-work-items`. Preserve explicit project
capacity, approval and pause decisions; no default quota is introduced.

### Stage 1: compare the current priority order

Combine current roadmap items with eligible backlog items and compare them across all strategic goals by `priority` (P0 > P1 > P2 > P3). Goal mapping provides traceability, not a separate promotion queue or quota.

For equal priorities, preserve the existing order unless a documented strategic override justifies changing it. For new tied items, use their stable ID or path for a reproducible presentation order; this tie-break is not a new priority score.

### Stage 2: generate promotion candidates

**Now-tier admission rule**: propose P0/P1 items for Now, P2 for Next, and P3 for Later. These are defaults; an explicit user decision may change the proposed tier, with its reason recorded. Prerequisite checks still apply to every Now candidate. There is no default item-count limit or effort prerequisite; explicit project decisions apply.

The dependency check reads each item's frontmatter `depends_on` (registered by `map-item-dependencies`):

| `depends_on` state | Handling |
| --- | --- |
| `—` (checked, no dependency) | may enter Now |
| has dependencies, and every prerequisite is finished or its required deliverable is verified available | may enter Now |
| a prerequisite is in Now but its required deliverable is not available | **must not enter Now**; keep the dependent item in Next until the prerequisite is satisfied |
| has dependencies with an unresolved prerequisite | **must not enter Now**; Next is as far as it goes, and the candidate table names which one blocks it |
| field missing (never checked) | do not wave it through silently. Prompt for a `map-item-dependencies` run first; when the user insists on continuing, mark it "dependencies unchecked" in the candidate table and leave the risk with the user |

Generate candidates across goals in priority order. Apply the default tier mapping, prerequisite checks, and the roadmap's declared stage promotion criteria. Keep a blocked P0/P1 item in Next and explain its blocker; do not lower its priority to justify the deferral.

Emit the candidate table:

```markdown
## Promotion candidates

| Goal | Item | Priority | Dependencies | Action | Reason |
| --- | --- | --- | --- | --- | --- |
| Goal 1 | #42 payment optimization | P0 | Checked, none | Later → Now | Highest priority, ready |
| Goal 3 | #17 auth refactor | P1 | Blocked by #12 | Backlog → Next | Prerequisite unresolved |
```

### Stage 3: demotion / deferral decisions

Check the current Now-tier items:

- if the priority has dropped (a re-score after a strategy change, say) → suggest demoting it to Next or Later
- if a prerequisite is unresolved or the stage promotion criteria no longer hold → suggest deferring the item to Next and name the blocker

Emit the demotion suggestions.

### Stage 4: the user confirms each decision

Present the merged list (promotions + demotions) and have the user confirm item by item:

```markdown
## Confirmation list

[ ] #42 promote Later → Now?
[ ] #17 promote Backlog → Now?
[ ] #8 demote Now → Next? (priority dropped)
[ ] ...
```

### Stage 5: persist

For each confirmed decision:

1. Update only the project-defined planning tier or execution field when its contract permits it. Preserve approval/lifecycle `status` such as `draft` or `approved`. If the source has no planning field, roadmap placement alone records the decision; do not invent a new field or convert approval into execution.
2. Update roadmap.md with a concise requirement or defect row: source link, outcome, priority and status/key condition. Keep task progress and acceptance evidence in the source.
3. Record the update date in the roadmap; write `promoted_at` / `demoted_at` only when supported by the project source contract.

### Stage 6: emit the final report

- Counts promoted / demoted / held
- Priority-ordered items by tier, with reasons for held or deferred items
- The suggested next step (`capture-work-items` for the newly promoted Now items, for example)

---

## Input and Output

**Input**: roadmap.md + the backlog (priority set) + strategic-goals.md.

**Output**: the decision table in chat + the roadmap.md update + the item frontmatter update (project-defined planning fields, if supported; approval status preserved).

---

## Restrictions

### Hard Boundaries

- Do not promote a `priority: unset` item (go through `prioritize-backlog` first)
- Do not promote a `status: declined` item — that terminal state means never doing it, and taking it back in needs the user to lift the terminal state explicitly
- Do not promote a P3 item into Now automatically (P3 goes to Later by default)
- Do not promote an item with an unresolved prerequisite into Now (clear the prerequisite first, or promote only as far as Next)
- Do not introduce staffing, effort, quota or item-count gates; preserve explicit project constraints

### Skill boundaries

**Not done here (other skills own it)**:

| Action | Owner |
| --- | --- |
| Creating backlog items | `capture-work-items` |
| Scoring the backlog | `prioritize-backlog` |
| Defining roadmap structure | `define-roadmap` |
| Breaking a Now item into tasks | AgentFabric runtime (outside AI Cortex) |
| Detailed requirement capture | `capture-work-items` |

---

## Anti-Patterns

- ❌ **Do not tie it to a fixed cycle** ("run it every Monday") — this skill is **event-driven** (items completed / priority or strategy change / on demand)
- ❌ **Do not partition priority by goal quotas** — compare candidates across goals in priority order
- ❌ **Do not act on priority-unset items** — score them first
- ❌ **Do not skip the dependency check** — high priority does not mean it can be pulled now; a blocked item in Now cannot progress
- ❌ **Do not change the roadmap structure** (adding a milestone, say) — that is `define-roadmap`'s business

---

## Self-Check

- [ ] roadmap.md, the backlog and strategic-goals.md were read successfully
- [ ] Only backlog items with `priority` set and `status` other than `declined` were handled
- [ ] Current and candidate items were compared across goals in priority order
- [ ] Promotion candidates were generated by priority order, stage criteria, and dependency readiness
- [ ] Now-tier candidates passed the dependency check; items missing `depends_on` were told to run `map-item-dependencies` first, not waved through silently
- [ ] No default resource gate was imposed; explicit project decisions were preserved
- [ ] Only requirement and defect rows were persisted, with no task groups or copied execution detail
- [ ] The demotion suggestions weigh priority changes and prerequisite readiness
- [ ] The user confirmed item by item; nothing was auto-approved
- [ ] roadmap.md and supported planning fields agree; approval states were not changed by placement
- [ ] The final priority-ordered tier report was emitted

---

## Examples

### Example 1: priorities determine promotion (mainstream case)

**Context**: previous Now items have finished. #42 belongs to Goal 1 and is P0; #17 belongs to Goal 3 and is P1. Both have checked dependencies and are ready. Staffing and effort estimates are absent.

**Flow**:

1. Compare both items across goals in priority order: #42 before #17.
2. Propose both for Now, explaining their priorities and readiness.
3. The user confirms each decision.
4. Update roadmap.md and supported planning fields; preserve the source approval state.
5. Report the resulting priority order and confirmed changes.

**Result**: both items enter Now without resource estimates or goal quotas.

### Example 2: a priority change causes demotion (edge case)

**Context**: after a strategy refresh, `prioritize-backlog` changes #17 from P1 to P3. A new P0 item #60 depends on an unresolved prerequisite #12.

**Flow**:

1. Read the updated priorities and dependency evidence.
2. Propose demoting #17 from Now to Later because its priority dropped.
3. Propose #60 for Next until #12 is resolved; retain its P0 priority and name the blocker.
4. The user confirms the proposals and the files are updated.

**Result**: tier placement reflects priorities and readiness; neither item is lost.
