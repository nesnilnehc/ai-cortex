---
name: update-roadmap
description: Maintain requirement-and-defect roadmap summaries — change item status, shift dates with downstream impact analysis, and retain source-backed revision history. Does not move items between Now/Next/Later tiers.
version: 3.6.0
license: MIT
---

# Skill: Update Roadmap

## Purpose

The entry point for day-to-day maintenance once the roadmap is in place: change status, shift dates, say plainly what this round changed.

`define-roadmap` covers building from scratch, `promote-roadmap-items` covers promotion and demotion across tiers, and between them sits a large block of day-to-day movement — an item started, an item got stuck, an item slips by two weeks — which is what this skill covers.

---

## Core Objective

**Primary goal**: land one roadmap change completely, and let a reader see what changed, why it changed, and who it affects.

**Success criteria** (all must hold):

1. ✅ A requirement or defect status change agrees with its source and roadmap summary; task-only changes stay in the task list unless they affect the parent outcome or key blocker
2. ✅ A risk escalation or a change to `Blocked` must record the blocking reason and the mitigation; with either one missing, nothing is written
3. ✅ A date shift must compute the downstream impact: list the items this shift affects
4. ✅ Items that cross a hard deadline after the shift are flagged explicitly
5. ✅ A "what changed this round" summary is output, covering the changed items, the reasons, and the blast radius
6. ✅ The Now / Next / Later tier each item sits in stays unchanged

**Acceptance test**: after the change, can someone who took no part in the discussion read the summary alone and state "what changed, why, and who is affected"?

**Handoff point**: if the change really calls for a cross-tier adjustment (an item that no longer belongs in Now, say), stop and hand off to `promote-roadmap-items`.

---

## Scope Boundaries

**This skill owns**:

- Execution status changes using the fixed vocabulary in [roadmap-quality](../../rules/roadmap-quality.md#execution-status-vocabulary); risk remains a separate source annotation
- Date and timing adjustments, and the downstream impact analysis that goes with them
- Moving requirements/defects into or out of existing versions, preserving tier
- The what-changed summary for this round

**This skill does not own**:

- Cross-tier promotion / demotion (`promote-roadmap-items`)
- Structural roadmap changes: new milestones, stage promotion criteria edits, strategic bet edits (`define-roadmap`)
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
- **Must ask**: on a risk escalation or a change to `Blocked`, the blocking reason and the mitigation are both indispensable; if either is missing, nothing is written
- **Write the requested change**: analyze downstream impact before persisting. Ask only when the target, intended state, or a hard-deadline decision remains unclear.

### Execution

1. **Read the current state**: load roadmap.md, [roadmap-quality](../../rules/roadmap-quality.md), project closure criteria and source requirement or defect records.
   Resolve task-level input to its parent. Update task details in their source; only
   refresh the parent roadmap summary if its outcome, status, timing or key blocker changes.
   Never add a task or task group as a roadmap row.
2. **Identify the change type**: status change / date shift / existing-version scope change / existing-iteration goal, scope or cadence change / combination.
   - If what the user actually wants is a move across tiers → **stop**, explain that this falls to `promote-roadmap-items`, and hand off.
3. **Handling a status change**:
   - Map the project's source execution evidence to exactly one label from the quality rule. Keep approval, execution and key conditions in separate columns. Risk alone does not replace an execution label.
   - For a risk escalation or Blocked change, obtain the reason and mitigation from sources first; ask only for missing facts. Preserve the existing requirement to have both before writing. Keep details in the source and only the short next-step condition and link in the roadmap.
   - Verify the source basis for every transition, including pause, resume and reopening. Development complete maps to Awaiting acceptance while required acceptance is pending; passed acceptance maps to Awaiting release only if release remains required for closure. A recorded pause or blocker takes precedence while applicable.
   - Before Completed, verify the project's declared closure criterion and linked acceptance and production-release evidence where required. Do not invent or waive gates. If closure or the mapping is undefined, or sources conflict, report the limitation outside the status cell and leave the transition unresolved.
   - Task counts, test totals, commits and approval alone never prove completion; use metrics only when source criteria define them.
4. **Handling a date shift**:
   - Ask for the reason for the shift (scope change / dependency slip / resource change / other)
   - **Compute the downstream impact**: read each item's `depends_on`, find the items that carry this one as a prerequisite, and list their affected dates one by one
   - **Flag hard-deadline breaches**: items that cross a compliance, commitment, external-constraint or similar hard deadline after the shift are marked in red on their own
   - With the dependency data missing (`map-item-dependencies` was never run), state outright "downstream impact not computed, dependency data missing"; do not pretend the analysis happened
5. **Review the change list**: changed items + reasons + downstream impact + deadline breaches. Resolve any ambiguity or hard-deadline decision with the user before applying it.
6. **Persist source and summary**: load [roadmap modeling](../../specs/roadmap-modeling.md).
   For a move between existing versions, record old/new membership and the effect on
   both delivery windows, dependencies and commitments; leave tier unchanged. New
   versions/iterations, layout changes or structural changes go to `define-roadmap`. Refresh all selected views
   in the established destination using that skill's generator procedure when useful;
   confirm only a changed destination, not the same authorized location again.
   Update the authoritative source and, when the parent planning summary changes,
   its roadmap row. Keep test counts, task IDs and detailed evidence in source records;
   link them instead. Source/summary/diagram disagreement remains unresolved until repaired.
7. **Output the change summary**: see the template below.

### Change summary template

```markdown
## Roadmap changes this round

**Changed at**: <ISO date>

| Item | Change | Reason |
| --- | --- | --- |
| #42 payment optimization | In progress → Blocked | waiting on the third-party sandbox |
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

**Output**: updated authoritative source and, where parent planning changed, its roadmap summary; downstream impact and change summary.

---

## Restrictions

### Hard Boundaries

- **Do not change the tier**: an item must not be moved between Now / Next / Later; that is `promote-roadmap-items`'s job
- **Do not change the structure**: no new milestones, no changing stage promotion criteria, no editing the strategic bets
- **A blocker must have a follow-up**: a risk escalation / `Blocked` change is not written while the blocking reason or the mitigation is missing
- **Source agreement**: requirement and defect summaries agree with their source; task-only progress need not change the roadmap
- **With the dependency data missing, must not pretend the downstream impact was analyzed** — the fact that it was not computed, and why, must be stated explicitly

### Anti-patterns (avoid)

- ❌ **Changing status silently**: change it without saying why, and next time nobody remembers what happened
- ❌ **Shifting a date without looking downstream**: pushing one item back looks harmless and drags a whole chain with it
- ❌ **Using a date shift in place of demotion**: an item shifted over and over does not belong in Now; the route is demotion via `promote-roadmap-items`, not one more push
- ❌ **Marking done without acceptance evidence**: task progress or approval does not prove the requirement or defect outcome
- ❌ **Changing a pile of things with no summary**: the change summary is what stakeholders read, and a batch of changes needs it more, not less

### Skill Boundaries (avoid overlap)

| Action | Owner |
| --- | --- |
| Cross-tier promotion / demotion | `promote-roadmap-items` |
| New milestone / stage criteria edit | `define-roadmap` |
| Creating items | `capture-work-items` |
| Re-scoring | `prioritize-backlog` |
| Dependency identification | `map-item-dependencies` |
| Roadmap health check | `review-roadmap` |

---

## Self-Check

- [ ] The change type was identified; anything that is a cross-tier move went to `promote-roadmap-items`
- [ ] Every risk escalation / `Blocked` change recorded the blocking reason and the mitigation
- [ ] Every transition has source evidence; Completed meets declared closure including acceptance/release where required; no gates were invented
- [ ] Date shifts had their downstream impact computed; where dependency data was missing, the omission was stated explicitly
- [ ] Hard-deadline breaches were flagged on their own
- [ ] The requested change and downstream impact were reviewed before persistence; any unresolved decision was clarified
- [ ] Separate approval, execution and key conditions columns follow the quality rule; each execution cell contains one fixed label, without risk labels or evidence
- [ ] Source and parent summary agree; task-only changes did not add roadmap entries or duplicate details
- [ ] The what-changed summary was output
- [ ] No item's tier was touched
- [ ] Existing-version scope changes preserve tier and report both versions' impact; all selected views agree.

---

## Examples

### Example 1: an item gets stuck (mainstream case)

**Background**: #42 payment optimization sits in the Now tier, in progress, and is suddenly stuck on a third-party sandbox.

**Flow**:

1. Identified as a status change: In progress → Blocked.
2. Ask the two questions: what it is stuck on (the third-party sandbox is not open yet) and what the plan is (ticket filed, 3 working days expected; a local stand-in is being prepared for parallel development).
3. Read `depends_on` and find that #51 advanced reporting carries #42 as a prerequisite → downstream impact: #51's start date moves out.
4. No hard-deadline breach.
5. The target and impact are clear → roadmap.md and #42's frontmatter are both written.
6. Output the change summary.

**Result**: the blocker is on record with a mitigation, and #51's slip surfaces early rather than at the moment it was due to start.

### Example 2: repeated shifts that call for demotion (edge case)

**Background**: #63 mobile workflow is being pushed back for the third time.

**Flow**:

1. Identified as a date shift; the reason asked for → "design never gets scheduled".
2. Check the history: this item has already shifted twice within this cycle.
3. **Tell the user**: an item that shifts over and over in the Now tier does not currently meet the conditions for being pulled into Now — shifting it again only leaves the Now tier looking full while nothing moves.
4. Suggest switching to `promote-roadmap-items` and demoting it to Next, keeping the Now tier focused on items that can move.
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

## Filled deliverable example

[Filled change record and adjusted views](../define-roadmap/references/service-desk/change-record.md). This is a fictional completed output, not a template
or authorization to change the adopting project.

## Phase and milestone contract

Maintain existing phase timing and milestone timing/state from linked source evidence.
Apply the [Roadmap Spec](../../specs/roadmap-modeling.md): actual event timing requires
reached state; non-planned states require evidence. Date passage, member completion
and scope changes do not automatically reach a milestone or approve related work.
Report affected version windows, phase spans and event targets separately. Route
new phase/event structure to define-roadmap; do not silently upgrade legacy inputs.

Self-check: concepts, selected views and linked evidence agree with the source records.

## Revision history maintenance

Before a material planning change, read the current roadmap and durable history.
Apply the [revision contract](../../specs/roadmap-modeling.md#54-revision-records):
append one source-backed decision with a stable ID, date, before/after, reason,
impact and details link. Refresh settled priorities from their authoritative source
without making priority decisions here. Record priority/tier handoffs, membership,
phase, timing/commitment, exclusion and milestone-state changes where applicable.
The conversational change summary is also retained in the project history source;
it is not the only copy. Keep the latest five in the roadmap and verify the full
history link before shortening it. Re-rendering or retrying the same decision
reuses its ID; a correction appends a linked revision. Formatting-only edits can
remain in Git. Missing decision evidence stays unresolved, never invented.

Self-check: material changes are traceable, retained links resolve, and repeated execution adds no duplicate revision.

## Iteration and document maintenance

Read linked delivery/history pages and declared authoritative records before edits.
Maintain existing iteration goals, scope, cadence and timeboxes only from authorized
source decisions. Analyze affected versions, dependencies and commitments; carry-over
alone changes no tier, closure state or release evidence. New iteration structure or
layout routes to define-roadmap. Keep execution-board tasks in their source.
Refresh all affected main/detail/chart summaries together, reusing the same revision
ID. Preserve source-relative links and selected single/split layout. Report any
projection that could not be updated; do not claim a consistent plan while it differs.

Self-check: iteration changes have source/revision evidence; every affected main,
detail and time view agrees, with no duplicate editable scope or dates.

## Retained scenario selection

Read the existing selection source and reuse primary perspective, views, layout and
destination. Missing new metadata in legacy plans is not a reason to re-interview or
migrate. Update flow summaries from linked policy/board evidence when applicable;
no fabricated cadence, WIP number or service target. If needs materially change,
report the difference and route a structural reconsideration to define-roadmap while
preserving current choices. Refresh every affected projection only within the settled
combination; do not apply a fresh recommendation during status/date maintenance.

Self-check: the update preserves the selection or links the authorized new decision;
changed context and unavailable evidence are explicit.
