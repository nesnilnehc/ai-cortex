---
name: update-roadmap
description: Day-to-day roadmap maintenance — change item status, shift dates with downstream impact analysis, and produce a what-changed summary. Does not move items between Now/Next/Later tiers.
description_zh: 路线图日常运维——改条目状态、挪期并计算下游影响、产出本次变更摘要；不改变条目所在的 Now/Next/Later 层级。
tags: [workflow, planning, maintenance]
version: 1.0.1
license: MIT
recommended_scope: project
cognitive_mode: interpretive
metadata:
  author: ai-cortex
triggers: [update roadmap, change status, at risk, blocked, shift dates, roadmap maintenance]
input_schema:
  type: free-form
  description: Current roadmap plus the intended status change or date shift; optional blocker details
output_schema:
  type: chat
  description: Updated roadmap.md and item frontmatter, downstream impact list, and a what-changed summary
---

# Skill: Update Roadmap

## Purpose

The entry point for day-to-day maintenance once the roadmap is in place: change status, shift dates, say plainly what this round changed.

`define-roadmap` covers building from scratch, `promote-roadmap-items` covers promotion and demotion across tiers, and between them sits a large block of day-to-day movement — an item started, an item got stuck, an item slips by two weeks — which is what this skill covers.

---

## Core Objective

**Primary goal**: land one roadmap change completely, and let a reader see what changed, why it changed, and who it affects.

**Success criteria** (all must hold):

1. ✅ A status change lands in both roadmap.md and the item frontmatter, leaving no one-sided update
2. ✅ A change to `at risk` or `blocked` must record the blocking reason and the mitigation; with either one missing, nothing is written
3. ✅ A date shift must compute the downstream impact: list the items this shift affects
4. ✅ Items that cross a hard deadline after the shift are flagged explicitly
5. ✅ A "what changed this round" summary is output, covering the changed items, the reasons, and the blast radius
6. ✅ The Now / Next / Later tier each item sits in stays unchanged

**Acceptance test**: after the change, can someone who took no part in the discussion read the summary alone and state "what changed, why, and who is affected"?

**Handoff point**: if the change really calls for a cross-tier adjustment (an item that no longer belongs in Now, say), stop and hand off to `promote-roadmap-items`.

---

## Scope Boundaries

**This skill owns**:

- Item status changes (not started / in progress / at risk / blocked / done)
- Date and timing adjustments, and the downstream impact analysis that goes with them
- The what-changed summary for this round

**This skill does not own**:

- Cross-tier promotion / demotion (`promote-roadmap-items`)
- Structural roadmap changes: new milestones, capacity allocation edits, strategic bet edits (`define-roadmap`)
- Creating items (`capture-work-items`)
- Re-scoring (`prioritize-backlog`)
- Dependency identification (`map-item-dependencies`)

**The line against `promote-roadmap-items`**: **changing the tier belongs to promote, leaving the tier alone belongs here.** Pushing a Now item back two weeks is this skill; moving it to Next is promote. The test is whether the tier changed, not whether the date changed.

---

## Use Cases

- **Progress sync**: an item started / finished and the status has to keep up
- **Risk escalation**: an item is stuck, and the blocking reason and mitigation need recording
- **Timing adjustment**: a dependency slipped or the scope changed, so the date moves back and the blast radius has to be visible
- **Before communicating a change**: a "what changed this round" note is needed to share with stakeholders

---

## Behavior

### Interaction policy

- **Default**: read roadmap.md and the related item files from the paths the project norms define
- **Must ask**: on a change to `at risk` / `blocked`, the blocking reason and the mitigation are both indispensable; if either is missing, nothing is written
- **Write after confirmation**: present the change list and the downstream impact first, and persist only after the user confirms

### Execution

1. **Read the current state**: load roadmap.md and the frontmatter of the items involved.
2. **Identify the change type**: status change / date shift / both.
   - If what the user actually wants is a move across tiers → **stop**, explain that this falls to `promote-roadmap-items`, and hand off.
3. **Handling a status change**:
   - The target status comes from: not started / in progress / at risk / blocked / done
   - On a change to **at risk** or **blocked**, ask two things: what it is stuck on (the blocking reason) and what the plan is (the mitigation). Write only once both are in hand
   - On a change to **done**, check whether the item's success metric was met; when it was not and the item is marked done anyway, ask the user to explain
4. **Handling a date shift**:
   - Ask for the reason for the shift (scope change / dependency slip / resource change / other)
   - **Compute the downstream impact**: read each item's `depends_on`, find the items that carry this one as a prerequisite, and list their affected dates one by one
   - **Flag hard-deadline breaches**: items that cross a compliance, commitment, external-constraint or similar hard deadline after the shift are marked in red on their own
   - With the dependency data missing (`map-item-dependencies` was never run), state outright "downstream impact not computed, dependency data missing"; do not pretend the analysis happened
5. **Present the change list**: changed items + reasons + downstream impact + deadline breaches, then ask the user to confirm.
6. **Persist to both places**: roadmap.md and the item frontmatter are updated together, leaving nothing one-sided.
7. **Output the change summary**: see the template below.

### Change summary template

```markdown
## Roadmap changes this round

**Changed at**: <ISO date>

| Item | Change | Reason |
| #42 payment optimization | in progress → blocked | waiting on the third-party sandbox |
| #63 mobile workflow | date +2 weeks | design delivery slipped |

**Blocked items and mitigations**
- #42: ticket filed, 3 working days expected; a local stand-in is being prepared so development can go on in parallel

**Downstream impact**
- #51 advanced reporting: prerequisite #42 slipped, so this item's real start date moves out 2 weeks

**Hard-deadline breaches**
- None

**Unchanged**: the tiers stay as they are (this skill makes no cross-tier adjustment)
```

---

## Input & Output

**Input**: the current roadmap.md, the intended change, and optional blocker details.

**Output**: updated roadmap.md and item frontmatter + the downstream impact list + the what-changed summary.

---

## Restrictions

### Hard Boundaries

- **Do not change the tier**: an item must not be moved between Now / Next / Later; that is `promote-roadmap-items`'s job
- **Do not change the structure**: no new milestones, no touching the capacity allocation, no editing the strategic bets
- **A blocker must have a follow-up**: `at risk` / `blocked` is not written while the blocking reason or the mitigation is missing
- **No one-sided update**: roadmap.md and the item frontmatter must stay in sync
- **With the dependency data missing, must not pretend the downstream impact was analyzed** — the fact that it was not computed, and why, must be stated explicitly

### Anti-patterns (avoid)

- ❌ **Changing status silently**: change it without saying why, and next time nobody remembers what happened
- ❌ **Shifting a date without looking downstream**: pushing one item back looks harmless and drags a whole chain with it
- ❌ **Using a date shift in place of demotion**: an item shifted over and over does not belong in Now; the route is demotion via `promote-roadmap-items`, not one more push
- ❌ **Marking done without checking the metric**: marking an item done while its success metric is unmet makes the metric decorative
- ❌ **Changing a pile of things with no summary**: the change summary is what stakeholders read, and a batch of changes needs it more, not less

### Skill Boundaries (avoid overlap)

| Action | Owner |
|---|---|
| Cross-tier promotion / demotion | `promote-roadmap-items` |
| New milestone / capacity edit | `define-roadmap` |
| Creating items | `capture-work-items` |
| Re-scoring | `prioritize-backlog` |
| Dependency identification | `map-item-dependencies` |
| Roadmap health check | `review-roadmap` |

---

## Self-Check

- [ ] The change type was identified; anything that is a cross-tier move went to `promote-roadmap-items`
- [ ] Every `at risk` / `blocked` change recorded the blocking reason and the mitigation
- [ ] Items marked done had their success metric checked
- [ ] Date shifts had their downstream impact computed; where dependency data was missing, the omission was stated explicitly
- [ ] Hard-deadline breaches were flagged on their own
- [ ] The change list was persisted only after the user confirmed it
- [ ] roadmap.md and the item frontmatter were both written
- [ ] The what-changed summary was output
- [ ] No item's tier was touched

---

## Examples

### Example 1: an item gets stuck (mainstream case)

**Background**: #42 payment optimization sits in the Now tier, in progress, and is suddenly stuck on a third-party sandbox.

**Flow**:

1. Identified as a status change: in progress → blocked.
2. Ask the two questions: what it is stuck on (the third-party sandbox is not open yet) and what the plan is (ticket filed, 3 working days expected; a local stand-in is being prepared for parallel development).
3. Read `depends_on` and find that #51 advanced reporting carries #42 as a prerequisite → downstream impact: #51's start date moves out.
4. No hard-deadline breach.
5. The user confirms → roadmap.md and #42's frontmatter are both written.
6. Output the change summary.

**Result**: the blocker is on record with a mitigation, and #51's slip surfaces early rather than at the moment it was due to start.

### Example 2: repeated shifts that call for demotion (edge case)

**Background**: #63 mobile workflow is being pushed back for the third time.

**Flow**:

1. Identified as a date shift; the reason asked for → "design never gets scheduled".
2. Check the history: this item has already shifted twice within this cycle.
3. **Tell the user**: an item that shifts over and over in the Now tier does not currently meet the conditions for being pulled into Now — shifting it again only leaves the Now tier looking full while nothing moves.
4. Suggest switching to `promote-roadmap-items` and demoting it to Next, freeing capacity for items that can move.
5. The user agrees → **this skill stops** and hands off to promote.

**Result**: a third shift did not paper over the problem; the tier adjustment went back to the skill it belongs to.

### Example 3: dependency data missing (edge case)

**Background**: the user wants to push #38 data pipeline upgrade back by 3 weeks, but the project has never run `map-item-dependencies` and the items carry no `depends_on`.

**Flow**:

1. Identified as a date shift; the reason is that resources were pulled away.
2. Attempt to compute the downstream impact → every item's `depends_on` is empty rather than `—`, so "no dependency" cannot be told apart from "not checked".
3. **No pretending the analysis happened**. The change summary says outright: "downstream impact not computed — the project has not registered dependency data yet".
4. Suggest running `map-item-dependencies` first and then deciding how far the shift goes, along with a pointer the user can judge from: pipeline items usually have downstream consumers.
5. The user chooses to shift now and fill in the dependencies later → persist as decided, keeping the not-computed statement in the summary.

**Result**: the change goes ahead, but "downstream was not computed this time" is written out in the open rather than leaving a reader to assume it was assessed.
