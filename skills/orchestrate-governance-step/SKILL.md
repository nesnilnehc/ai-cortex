---
name: orchestrate-governance-step
description: Safely advances one governance action from plan-next, re-diagnoses stale or conflicting routes, and reports whether to continue, ask, wait, or stop.
description_zh: 根据 plan-next 安全推进一项治理工作；遇到过时或冲突路由时重新诊断，并明确报告继续、询问、等待或停止。
tags: [automation, workflow, meta-skill]
version: 3.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [auto iterate, iterate governance, autopilot, governance loop, auto-advance]
input_schema:
  type: free-form
  description: Optional governance docs root; auto-discovers defaults same as plan-next.
  defaults:
    docs_root: auto
output_schema:
  type: diagnostic-report
  description: "IterationStepReport: decision_state (actionable | needs_input | no_applicable_action | complete), evidence and blockers, optional action/skill/plan trace, outcome, continuation_signal (advance | done | blocked | stalled | error)."
---

# Skill: Auto-iterate (orchestrate-governance-step)

> **Role**: evidence-led governance driver — advances one safe, eligible action from plan-next
> **WHAT**: each invocation validates current evidence, takes at most one action, verifies the result, and reports the next safe transition
> **HOW**: diagnose → validate recommendation and dependencies → act or ask/wait → re-diagnose after changes → emit the report
> **Distinct from**: `plan-next` (diagnosis and user-directed recommendation preferences, no downstream execution); `/loop` (scheduling only, no business logic); `orchestrate-repair-loop` (repairs code defects, does not advance the governance layer)

---

## Purpose

Turn a plan-next routing suggestion into one executable governance action, which is what makes a fully automatic autopilot (`/loop /orchestrate-governance-step`) possible.

plan-next diagnoses and suggests; the user has to run each suggestion by hand. orchestrate-governance-step fills that execution gap and, together with `/loop`, gives three orthogonal layers of automation:

| Layer | Skill | Responsibility |
| --- | --- | --- |
| Scheduling | `/loop` | Fires once every N minutes |
| **Driving** | **orchestrate-governance-step** | Read the routing → run 1 step → report |
| Diagnosis | `plan-next` | Inventory + gap identification + routing suggestions; reads saved exclusions |

---

## Core Objective

**Primary goal**: each invocation either carries out at most 1 governance action or makes no change and names the exact reason it cannot safely proceed. The report copies plan-next's latest `decision_state`; executor gates affect the continuation signal, not the diagnosis.

**Success criteria** (all must be met):

1. ✅ **Bounded step**: each invocation runs at most 1 governance action; no-op outcomes are first-class
2. ✅ **Stall detection**: when the same routing-card fingerprint appears 2 times in a row within a session and the target has not advanced, the `stalled` signal fires
3. ✅ **Post-execution verification**: after a modifying action, plan-next is re-run to verify intended evidence and updated decision state
4. ✅ **Decision ownership**: human-owned strategic choices pause for the user; routine, reversible, evidence-based governance work can proceed within its skill boundary
5. ✅ **Explicit continuation signal**: every invocation must emit one of the five `continuation_signal` values in the IterationStepReport

**Acceptance test**: after execution, does the IterationStepReport state clearly what was done, how it turned out, and whether the next step is to continue or to bring in a human?

---

## Scope Boundaries

**This skill covers**:

- Calling plan-next internally to get the routing
- Validating plan-next's decision state, evidence, prerequisites, dependencies, and current target before selecting the highest-priority eligible card
- Stall detection (fingerprint comparison within the session)
- Ownership and safety checks; defer human-owned/external work without persisting a recommendation exclusion
- Choosing a proportional execution guard: direct bounded invocation for routine reversible work; a concrete plan and explicit review for high-impact, multi-artifact, irreversible, or ambiguous work
- Running 1 sub-skill (once the plan passes)
- Light post-execution verification
- Emitting the IterationStepReport

**This skill does not cover**:

- Governance diagnosis and routing generation → `plan-next`
- Loop scheduling → `/loop` (built into Claude Code)
- The code-defect repair loop → `orchestrate-repair-loop`
- The content of strategic and creative decisions (mission, vision, strategic goals) → a human is needed
- Persisting an executor deferral → per-invocation deferrals are reported, never written as plan-next preferences

**Handoff points**:

- `continuation_signal: done` → plan-next explicitly reports `complete`; stop
- `continuation_signal: blocked` → preserve plan-next's `decision_state` and explain whether the stop is due to `needs_input`, `no_applicable_action`, human ownership, or external execution
- `continuation_signal: stalled | error` → stop and explain the execution failure or repeated lack of progress

---

## Use Cases

- "Keep advancing governance until it is finished" → `/loop /orchestrate-governance-step`
- "Run the next governance action" → `/orchestrate-governance-step`
- "Fully automatic autopilot, one step every 30 minutes" → `/loop /orchestrate-governance-step 30m`
- "Just show me what the next step would be, without running it" → use `/plan-next`

---

## Behavior

### Step 0: preconditions

Read the governance documentation path (by default the same `docs_root` as plan-next, or one the caller supplies explicitly).

### Step 1: call plan-next

Call `/plan-next` internally and capture the routing output. If the caller supplied `pre_run_output`, use that and skip this step.

Do not assign a stall fingerprint yet; first determine which candidate, if any, passes the ownership and safety gate.

### Step 2: parse the routing

First validate the report's `decision_state`, evidence, candidate eligibility, prerequisites, and exact target. Do not infer a state from the presence or absence of cards alone.

If a routing claim conflicts with repository evidence, the target is stale, or its prerequisite/dependency status is unclear, do not execute it. Re-run plan-next once against current evidence. If the fresh diagnosis still needs a project fact or decision, stop and ask; do not repeatedly re-plan within the same invocation. Never use a skipped recommendation to unlock a dependent route.

**End states of the iteration**:

- `actionable` and at least one eligible, non-human-owned action exists → select the highest-priority eligible card and continue
- `needs_input` → make no change; ask the focused question named by plan-next; `continuation_signal: blocked`
- `no_applicable_action` → make no change; explain whether work is excluded, externally owned, dependency-blocked, or not yet eligible; `continuation_signal: blocked`
- `complete` → confirm the evidence in plan-next and emit `done`; an empty list alone never qualifies
- No eligible action remains after human-owned items are set aside → report those items and wait; `continuation_signal: blocked`

**Decision table** (decision state is authoritative; verify its supporting evidence):

| plan-next output | continuation_signal | Meaning |
| --- | --- | --- |
| `actionable`, with one or more currently eligible cards | Continue at step 3 | Choose by priority, then apply ownership and safety gates |
| `needs_input` | `blocked` | Diagnosis cannot safely choose without the user's fact or decision |
| `no_applicable_action` | `blocked` | No eligible governance action now; distinguish external work, dependency blockers, and exclusions |
| `complete`, with acceptance evidence and no unfinished/excluded route | `done` | Governance and acceptance are met |

**Key constraints**:

- Empty output is never enough to prove `complete`; require explicit plan-next `complete` plus evidence that every declared acceptance condition is met
- Excluded unfinished work, awaiting execution, missing KPI data, or unresolved route applicability forbids `done`
- Treat an absent or malformed decision state as an incompatible plan-next output: emit `error`, name the contract mismatch, and ask for the skill to be updated; do not guess

### Step 3: ownership and safety gate

Do not automate decisions that belong to the user. Defer the current card for this invocation and consider the next independently eligible card only when plan-next already surfaced it; do not change recommendation preferences or governance state to do so.

Consider eligible cards in priority order (`urgent` → `important` → `defer` → `minor`). If a card is human-owned or externally owned, report the deferral and continue only to the next already-surfaced candidate whose dependencies are independently satisfied. `awaiting execution` is never an executable governance action.

Human decision is required when:

- The recommended skill is a creative or strategic one: `define-mission`, `design-strategic-goals`, `define-vision`, `define-north-star`, `define-strategic-pillars`
- An action would choose among materially different business outcomes or accept an unstated trade-off
- The target, authority, or prerequisite is ambiguous after the one permitted re-diagnosis
- The card is `awaiting execution`: governance is ready and outside development has to run it
- A route's completion marker says to return to plan-next after a blocker, and that blocker has occurred

If every surfaced candidate is human-owned, externally owned, or blocked, emit `blocked` and list each item with its owner/reason. Do not manufacture more candidates or claim governance is finished.

Any per-invocation deferral is not a `plan-next` exclusion and is not persisted. Never write `.ai-cortex/plan-next.yaml` from this gate.

This gate preserves automation for independent routine actions without turning one human-owned choice into a permanent suppression or bypassing dependencies.

### Step 4: stall detection

After Step 3 selects a specific executable card, compute its fingerprint and compare it with the **fingerprint of the previous executed action** in this session:

```text
fingerprint = resolved route + "||" + exact target + "||" + relevant evidence key
```

- Same fingerprint and no evidence of target progress → `continuation_signal: stalled`, state that the action failed to advance, and stop.
- Different fingerprint, first execution, or evidence of progress → continue.
- Do not fingerprint a per-invocation deferral, an `awaiting execution` card, or a no-op outcome; those are not failed executions.

### Step 5: proportional execution

For routine, reversible, single-artifact governance work with an unambiguous target and an applicable skill, call that skill directly with the narrow focus from the card. Let the called skill's own required planning and confirmation policy govern its work.

Before execution, prepare an explicit plan and review it when the change is high-impact, irreversible, spans multiple artifacts, has material external effects, or the called skill requires plan mode. Include the intended result, exact scope, red lines, and recovery path. If evidence changes or the plan reveals a new dependency, stop and re-diagnose rather than widening scope.

When using a plan, review it once against the card's evidence, exact targets, dependencies, and scope. Correct any defect before execution; if it remains materially ambiguous, ask the user instead of looping on self-review.

Then invoke the selected skill at most once. Execution failure or a newly discovered blocker stops the action; do not widen the scope.

- The plan or action diverges from reality (target already exists, prerequisite is missing, or evidence conflicts) → stop and re-run plan-next once; if unresolved, report `needs_input` or `no_applicable_action` with `continuation_signal: blocked`
- Execution fails with no safe recovery path → `continuation_signal: error`, emit the report, stop

### Step 6: post-execution verification

**Re-running** `/plan-next` **is mandatory** after a modifying action. Compare evidence and decision state, not just whether the original card disappeared. A changed or missing card alone is not proof that the action succeeded.
The only legitimate source of `done` is an explicit `complete` state from this fresh plan-next diagnosis, supported by acceptance evidence; the executor must not infer it.

| Result | Action |
| --- | --- |
| The intended change is verified and plan-next says `actionable` | `continuation_signal: advance` |
| The intended change is verified and plan-next says `complete` with acceptance evidence | `continuation_signal: done` |
| Fresh plan-next says `needs_input` or `no_applicable_action` | `continuation_signal: blocked`; preserve that decision state and explain why |
| The card disappears only because it is excluded, renamed, or no longer visible, without evidence of resolution | `continuation_signal: blocked` or `error` according to whether the cause needs a user or indicates a contract/runtime failure; never claim progress |
| The card remains eligible and unchanged after the action | Update the stall counter; when the count reaches 2 → `continuation_signal: stalled` |

### Step 7: emit the IterationStepReport

---

## Interaction with /loop (important)

`/loop` has two modes, and they consume `continuation_signal` in completely different ways:

| /loop mode | How it fires | Signal consumption | Recommended use |
| --- | --- | --- | --- |
| **Dynamic** | No interval (self-scheduled ScheduleWakeup) | Reads `continuation_signal`: done/blocked/stalled/error stop the loop | ✅ **Recommended**: `/loop /orchestrate-governance-step` (no interval) |
| **Fixed-interval (cron)** | An interval is given (`5m`, say) | **Does not read** `continuation_signal`: cron keeps firing and the signal is ignored | ⚠️ Not recommended where automatic stopping matters; the user must CronDelete by hand |

**Mandatory behavior**:

- On detecting fixed-interval cron mode (through a CronCreate record in the session context whose prompt is `/orchestrate-governance-step`), the first IterationStepReport must warn the user: "this is cron mode and the signal is ignored; to stop the repeated firing, switch to a dynamic /loop, or CronDelete once you get stalled/blocked/done"
- On the 2nd consecutive `stalled` signal, the IterationStepReport must state "**CronDelete `<job-id>` immediately, strongly recommended**" and give the job ID

**The fix**: a user who wants it to "stop automatically once governance is ready" should use `/loop /orchestrate-governance-step` (no interval, dynamic mode), not `/loop 1m /orchestrate-governance-step`.

---

## Input & Output

### Input

| Parameter | Required | Default | Description |
| --- | --- | --- | --- |
| `docs_root` | No | auto | The governance docs root; auto means the same default path as plan-next |
| `pre_run_output` | No | — | A pre-run plan-next output; when supplied, the internal call is skipped |

### Output: IterationStepReport

```markdown
## What this automatic step did

- **What was done**: [describe the action or why no action was safe/applicable]
- **Decision state**: [copy the latest plan-next state exactly; do not rewrite it based on the human-ownership gate]
- **Evidence and blockers**: [the evidence that supports the state; name blocker scope and any independent route that remains]
- **Why it needed fixing**: [the concrete problem found; omit when creating a file for the first time]
- **What changed** (when files changed):
  - Before: ...
  - After: ...
- **Result**: Success ✅ | Your call needed ⚠️ | Error ❌
- **Next**: keep going automatically | all done, nothing left | your decision needed: [explanation] | stuck: [explanation]
- _(internal) continuation signal: advance | done | blocked | stalled | error_
```

### continuation_signal semantics

| Value | Meaning | /loop behavior |
| --- | --- | --- |
| `advance` | The action finished and governance still has work | Fire again |
| `done` | Fresh plan-next explicitly reports `complete` and supplies acceptance evidence; **emitting this value from the model's own inference is forbidden** | Stop the loop |
| `blocked` | No safe action can proceed now; report `needs_input` (user fact/decision needed) or `no_applicable_action` (waiting, excluded, or dependency-protected) distinctly | Stop the loop and ask or wait |
| `stalled` | The same routing card made no progress for 2 rounds in a row | Stop the loop and report the stall |
| `error` | The sub-skill failed with no recovery path | Stop the loop and report the error |

---

## Restrictions

### Hard Boundaries

**Rule 1**: an invocation MUST run at most 1 action and MUST represent no-op outcomes explicitly

- Verification: the IterationStepReport names zero or one invoked skill and gives a supported decision state
- Consequence: REJECT (it breaks the single-step semantics of the three-layer model)

**Rule 2**: a material strategic or creative decision MUST remain with the user

- Verification: when a card requires user-owned judgment, no skill is run for that decision; independent eligible routine work may proceed and deferred items are reported without persistent suppression
- Consequence: REJECT (strategic decisions are not there to be automated)

**Rule 3**: every invocation MUST emit a valid `continuation_signal`

- Verification: the IterationStepReport carries the `continuation signal` field and its value is one of the five in the enum
- Consequence: REJECT (/loop depends on this signal to decide whether to continue)

**Rule 4**: the `done` signal MUST come from a fresh plan-next `complete` result, and MUST NOT come from the model's own inference

- Verification: the IterationStepReport quotes or summarizes explicit completion and acceptance evidence from the fresh diagnosis; an empty list alone never qualifies
- Consequence: REJECT (the model took the routing judgment away from plan-next, breaking the responsibility boundaries of the three-layer model)

**Rule 5**: `done` MUST satisfy all at once — plan-next declares `complete`, every declared acceptance condition is met, and there is no unfinished, excluded, awaiting-execution, or evidence-limited route

- Verification: when emitting `done`, the IterationStepReport gives the relevant acceptance evidence and confirms no excluded unfinished route remains; an unmet or unmeasured KPI, an "awaiting execution" card, or a suppressed unfinished route forbids `done`
- Consequence: REJECT (mistaking "strategic goal status=approved" for acceptance being met makes /loop stop at the wrong time)

**Rule 6**: an `awaiting execution` card MUST NOT be executed by this governance executor or treated as `complete`

- Verification: selected_skill is absent for that card; preserve plan-next's decision state and have `next_step` name the external owner or wait condition when no independent action remains
- Consequence: REJECT

**Rule 7**: execution safeguards MUST be proportional to impact and ambiguity; the selected skill's contract MUST be followed

- Verification: routine reversible work has a bounded focus; high-impact, irreversible, multi-artifact or ambiguous work has an explicit reviewed plan; evidence divergence stops execution and returns to diagnosis
- Consequence: REJECT (both unbounded planning overhead and under-planning material changes undermine safe execution)

**Rule 8**: a stale or contradictory route MUST trigger at most one fresh plan-next diagnosis per invocation; unresolved conflicts MUST stop for input, not execution

- Verification: `replan_count ≤ 1`; any remaining route ambiguity yields `decision_state: needs_input` and `continuation_signal: blocked`
- Consequence: REJECT (blind execution and repeated re-planning both hide the actual decision needed)

### Skill Boundaries

**Do not do the following** (other skills own them):

- **Governance diagnosis and routing** → `plan-next`
- **Loop scheduling** → `/loop`
- **The code repair loop** → `orchestrate-repair-loop`
- **Document health checks** → the AgentFabric runtime + linter / CI tooling (per `rules/doc-health-criteria.md`)

---

## Anti-Patterns

### ✅ Correct: one step, then verification, then a continuation signal

```text
1. plan-next → 2 routing cards: capture-work-items (defer), prioritize-backlog (defer)
2. Take the highest priority: capture-work-items
3. Human gate: not a creative skill → continue
4. Run /capture-work-items
5. Re-run plan-next → the capture-work-items card is gone
6. Report continuation_signal: advance
```

**Why it is correct**: one bounded action keeps the three layers orthogonal; the post-check confirms real progress; /loop drives the next step naturally.

---

### ❌ Wrong: running two routing items at once

```text
1. plan-next → 2 routing cards
2. orchestrate-governance-step runs capture-work-items AND prioritize-backlog
```

**What goes wrong**: it violates the single-step semantics; if the second one fails, the rollback scope is hard to pin down; and it destroys /loop's control over granularity.

---

### ❌ Wrong: bypassing the human gate

```text
1. plan-next routes to /design-strategic-goals
2. orchestrate-governance-step runs it directly, without pausing
```

**What goes wrong**: the content of strategic goals needs human judgment; running it automatically produces a low-quality strategy document, and the user never notices.

---

### ❌ Wrong: one blocked item stops the whole /loop immediately

```text
1. plan-next → 3 routing cards: design-strategic-goals (important) + capture-work-items (defer) + prioritize-backlog (defer)
2. orchestrate-governance-step goes straight to blocked after the human gate fires on the 1st card, stopping /loop
3. The two non-blocked cards behind it could have advanced automatically, but are left hanging for nothing
```

**What goes wrong**: it conflates user-owned decisions with blocked work. Report the human-owned choice and proceed only to another independently eligible candidate already surfaced by plan-next; do not persist a skip or alter dependencies.

---

### ❌ Wrong: using the same planning ceremony for every action

```text
1. Step 2 finds a routine, reversible, single-artifact capture-work-items card
2. Enter plan mode and perform repeated self-reviews despite the clear bounded workflow
3. In another case, directly run a high-impact multi-artifact change without identifying scope or recovery
```

**What goes wrong**: both extremes ignore proportionality. Follow the called skill's contract for routine work; add an explicit reviewed plan when impact, ambiguity, irreversibility, or scope warrants it.

---

### ❌ Wrong: endlessly re-planning a contradictory route

```text
1. The recommendation says a required norms file is missing
2. Current project evidence shows that file exists and the project declares another artifact map
3. The executor calls plan-next repeatedly until one result happens to look actionable
```

**What goes wrong**: repetition does not resolve conflicting evidence. Re-run plan-next once; if applicability remains unclear, stop with `needs_input` and ask the smallest question that changes the route.

---

### ❌ Wrong: reporting advance while skipping the post-execution check

```text
1. /capture-work-items finishes
2. continuation_signal: advance is reported directly
3. In reality the file was never written
```

**What goes wrong**: without checking the intended evidence, advance is unsupported; the next plan-next may correctly produce the same routing and trigger stalled.

---

### ❌ Wrong: deciding "governance is finished" instead of re-running plan-next in step 6

```text
1. The sub-skill runs successfully
2. The model infers "every governance document that can be created has been created; the rest depends on the developer execution layer"
3. continuation_signal: done is emitted directly, with no plan-next re-run
```

**What goes wrong**: the model has taken over the "governance layer vs developer execution layer" judgment — that is plan-next's job, not orchestrate-governance-step's. An empty list is not completion. `done` requires the fresh plan-next diagnosis to state `complete` with acceptance met and no excluded unfinished route.

---

### ❌ Wrong: treating `strategic goal status=approved` as acceptance met → emitting done

```text
1. plan-next: G1 status=approved, and the acceptance KPI "citation visibility" has no monitoring data
2. orchestrate-governance-step takes an empty "Do now" (plan-next really ought to return routing here, but this example assumes plan-next misjudged it too)
3. done is emitted and /loop stops
4. G1 is in fact nowhere near met; the next wake-up check falls into a stalled loop
```

**What goes wrong**: `approved` only means the decision was approved; while acceptance is unmet, plan-next must continue routing or report missing evidence as `needs_input`. An empty list does not change that.

---

### ❌ Wrong: inferring done from a middle layer (M5/tasks)

```text
1. plan-next reports: every M5 task pending, the design ADRs complete, the requirement files complete
2. The model infers "the governance layer has no gaps" → emits done
3. It never returns to the G1 strategic-goal acceptance check
```

**What goes wrong**: scanning from a middle layer loses the causal chain of "why this task matters". The verdict of orchestrate-governance-step must start from "is the L1 acceptance KPI met", not from "are the middle-layer documents complete". This matches the direction in which plan-next traverses the goal tree — the root is the strategic goal's acceptance criteria.

---

### ❌ Wrong: emitting done repeatedly in cron mode without warning the user

```text
1. /loop 1m /orchestrate-governance-step registers a cron job
2. The first plan-next returns empty → done is emitted (wrong)
3. cron does not read the signal and keeps firing every minute, spinning on done
4. The user has no idea the cron job is spinning
```

**What goes wrong**: it violates the constraints in the "Interaction with /loop" section. In cron mode the signal is ignored, so the skill must actively warn the user to switch to a dynamic /loop, or suggest CronDelete.

---

## Examples

### Example 1: happy path — a requirement is registered

**Scenario**: plan-next routes to registering new backlog entries; first invocation; the sub-skill succeeds.

**Execution**:

1. Call plan-next internally → subject: "register the 3 backlog entries added in stage M5", recommended skill: `/capture-work-items`, priority: defer
2. Stall detection: first invocation, no fingerprint history → continue
3. Human gate: `capture-work-items` is not a creative skill → pass
4. The action creates three files, so prepare and review an explicit plan:
   - Goal: register the 3 M5-stage backlog entries (quoting the card subject)
   - Sub-skill command: `/capture-work-items register the 3 requirements newly found in M5 into the backlog`
   - Focus traceability: the card says "the M5 sweep found 3 requirements scattered through discussions"
   - Expected output: 3 new markdown files under `backlog/`, with frontmatter
   - Scope red lines: MUST NOT modify existing backlog entries; MUST NOT touch `roadmap/` or `requirements/`
   - Rollback points: the new files can be removed with `git clean -f backlog/<new-files>`
5. One review finds no scope or dependency defect → `plan_reviewed_rounds = 1`
6. Run `/capture-work-items register the 3 requirements newly found in M5 into the backlog`
7. Post-execution check: re-run plan-next → verify the three entries exist and the route is resolved; another eligible route remains → advance

**IterationStepReport**:

```markdown
## What this automatic step did

- **What was done**: registered the 3 requirements newly found in M5 into the backlog
- **Why it needed fixing**: the M5 sweep found 3 requirements scattered through discussions, never registered in structured form
- **What changed**:
  - Before: no matching entries under backlog/
  - After: 3 new backlog entry files, with frontmatter and a summary
- **Result**: Success ✅
- **Next**: keep going automatically (1 item still pending)
- **Decision state**: actionable
- **Evidence and blockers**: three registered entries verified; another eligible route remains
- _(internal) continuation signal: advance; plan_reviewed_rounds: 1_
```

---

### Example 2: the human gate skips a card → the next non-creative card is taken

**Scenario**: plan-next reports `actionable` with two cards: `design-strategic-goals` (important, strategic/creative) + `capture-work-items` (defer, registration).

**Execution**:

1. Call plan-next internally → two routing cards
2. Stall detection: first invocation → continue
3. Step 2 takes the highest priority: `design-strategic-goals`
4. The strategy decision is reported as human-owned; continue only because plan-next independently surfaced the capture route
5. Verify the capture route's target, prerequisites, and scope; the work is routine and reversible
6. Run `/capture-work-items …` with that bounded focus
7. Step 6 re-run plan-next; verify the intended artifacts/evidence changed, then emit `advance`

**IterationStepReport**:

```markdown
## What this automatic step did

- **What was done**: registered the 3 backlog entries added in stage M5
- **Why it needed fixing**: the strategic-goal card needs human judgment and was skipped; the same batch held another card that could run automatically
- **Result**: Success ✅
- **Next**: keep going automatically (skipped, awaiting a human: 1 — `design-strategic-goals`)
- **Decision state**: actionable
- **Evidence and blockers**: strategy decision awaits the user; capture route is independent and eligible
- _(internal) continuation signal: advance; plan_reviewed_rounds: 0; per-invocation deferral: [design-strategic-goals]_
```

---

### Example 2b: no candidate is eligible for automatic execution → blocked

**Scenario**: plan-next routes two cards, both either strategic/creative or "awaiting execution".

**Execution**:

1. plan-next → `define-mission` (important) + one `awaiting execution` card
2. Both are identified as human-owned or externally owned; no governance action is run
3. Emit `blocked` while preserving `decision_state: actionable`, listing the owner and next handoff for each

**IterationStepReport**:

```markdown
## What this automatic step did

- **What was done**: scanned 2 routing cards, all of which need a human
- **Why it needed fixing**: everything in "Do now" is either creative or waiting on outside execution, so nothing can be automated
- **Result**: Your call needed ⚠️
- **Next**: your decision needed:
  1. `define-mission`: a strategic skill that needs human judgment; running it by hand is recommended
  2. The "awaiting execution" card: governance is ready, waiting on outside development
- _(internal) continuation signal: blocked_
- **Decision state**: actionable
- **Evidence and blockers**: plan-next surfaced two candidates; both require a human decision or outside execution, so the executor ran neither
```

---

### Example 2c: a persistent exclusion leaves no visible action

**Scenario**: plan-next finds an unfinished route, but the user has excluded its exact route key in `.ai-cortex/plan-next.yaml`. Fresh diagnosis finds no independent eligible route, so `decision_state` is `no_applicable_action` and "Skipped recommendations" names the route.

**Result**: emit `continuation_signal: blocked` and report the excluded route. Do not emit `done`; the executor does not add, remove, or convert the persistent preference.

---

### Example 3 (edge case): stall detection — the sub-skill made no progress

**Scenario**: after the last `/capture-work-items` run, the requirement document was never written; this time plan-next routes the same card.

**Execution**:

1. Call plan-next internally → fingerprint = "analyze the requirements of roadmap node N1||strategic goal 'Goal A' → roadmap 'N1' current: requirements layer"
2. Stall detection: identical to the previous fingerprint → **stalled fires**

**IterationStepReport**:

```markdown
## What this automatic step did

- **What was done**: tried to analyze the requirements of roadmap N1, but detected 2 consecutive rounds with no progress
- **Why it needed fixing**: requirements/N1-requirements.md was never written after the last `/capture-work-items`
- **Result**: Error ❌
- **Next**: stuck: the same task made no progress twice in a row. Possible causes: the requirement file was not written, the path configuration is wrong, or the skill ran incorrectly. Suggested: run `/capture-work-items` by hand, check whether the output file exists, and re-run /orchestrate-governance-step once it is resolved
- _(internal) continuation signal: stalled_
```

---

## AI Repair Instructions

### Problem 1: several routing items were run

- **How to spot it**: the IterationStepReport has several `skill called` entries
- **How to correct it**:
  1. Identify the routing items that were run
  2. Keep only the 1 highest-priority item (`urgent` > `important` > `defer`)
  3. Re-emit the IterationStepReport, reporting only 1 action

---

### Problem 2: continuation_signal is missing

- **How to spot it**: the IterationStepReport lacks the internal continuation-signal field, or its value is outside the five-value enum
- **How to correct it**:
  1. Check the execution result and fill it in by this logic:
     - Sub-skill succeeded + routing remains → `advance`
     - Sub-skill succeeded + fresh plan-next says `complete` with acceptance evidence → `done`
     - Fresh plan-next says `needs_input` or `no_applicable_action` → `blocked`
     - Only human-owned/external candidates remain → `blocked`, preserving plan-next's state and naming the owner
     - The fingerprint repeated → `stalled`
     - The sub-skill failed → `error`
  2. Explain why in the `Next` field

---

### Problem 3: reporting advance while skipping the post-execution check

- **How to spot it**: the report says `advance` but plan-next was never re-run to verify the intended change
- **How to correct it**:
  1. Re-run `/plan-next` and check whether the intended evidence and decision state changed
  2. If the intended evidence is present and plan-next says `actionable` → `advance` is confirmed
  3. If the same eligible action remains unchanged → update the stall count; on the 2nd occurrence → `stalled`

---

### Problem 4: judging completion internally and skipping step 6

- **How to spot it**: the `Next` field carries self-assessment language such as "the whole governance layer is ready", "everything currently executable has been created", or "this belongs to the developer execution layer", with no record of a step 6 plan-next re-run
- **How to correct it**:
  1. Re-run `/plan-next`
  2. If plan-next explicitly says `complete` and provides acceptance evidence → `done` is valid
  3. If it says `needs_input` or `no_applicable_action` → `blocked`, preserving that state and the reason
  4. If it says `actionable` with an eligible route → `advance` only after the action and post-check

---

## Appendix: Output contract

### YAML schema (formal)

```yaml
type: object
# execution_trace is required for advance when a governance action ran;
# no-op states do not claim an execution trace.
required:
  - report_title
  - action_taken
  - result
  - next_step
  - continuation_signal
properties:
  report_title:
    type: string
    const: "What this automatic step did"
  action_taken:
    type: string
    minLength: 1
    description: describes the single action taken, by file name or feature name
  why_fix:
    type: string
    minLength: 1
    description: optional; may be omitted when a file is created for the first time
  changes:
    type: object
    required: [before, after]
    properties:
      before:
        type: string
      after:
        type: string
  result:
    type: string
    enum: ["Success ✅", "Your call needed ⚠️", "Error ❌"]
  next_step:
    type: string
    minLength: 1
  decision_state:
    type: string
    enum: [actionable, needs_input, no_applicable_action, complete]
  continuation_signal:
    type: string
    enum: [advance, done, blocked, stalled, error]
  execution_trace:
    type: object
    required: [selected_skill, plan_reviewed_rounds]
    properties:
      selected_skill:
        type: string
        pattern: "^/[a-z0-9-]+"
      plan_reviewed_rounds:
        type: integer
        minimum: 0
        maximum: 3
      post_check_plan_next_rerun:
        type: boolean
        description: Required and true after a modifying action; omit for no-op or read-only checks.
additionalProperties: false
```

### JSON schema (formal)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "IterationStepReport",
  "type": "object",
  "required": [
    "report_title",
    "action_taken",
    "result",
    "next_step",
    "decision_state",
    "continuation_signal"
  ],
  "allOf": [
    {
      "if": {
        "properties": {
          "continuation_signal": { "enum": ["advance"] }
        },
        "required": ["continuation_signal"]
      },
      "then": { "required": ["execution_trace"] }
    }
  ],
  "properties": {
    "report_title": {
      "type": "string",
      "const": "What this automatic step did"
    },
    "action_taken": {
      "type": "string",
      "minLength": 1
    },
    "why_fix": {
      "type": "string",
      "minLength": 1
    },
    "changes": {
      "type": "object",
      "required": ["before", "after"],
      "properties": {
        "before": { "type": "string" },
        "after": { "type": "string" }
      },
      "additionalProperties": false
    },
    "result": {
      "type": "string",
      "enum": ["Success ✅", "Your call needed ⚠️", "Error ❌"]
    },
    "next_step": {
      "type": "string",
      "minLength": 1
    },
    "decision_state": {
      "type": "string",
      "enum": ["actionable", "needs_input", "no_applicable_action", "complete"]
    },
    "continuation_signal": {
      "type": "string",
      "enum": ["advance", "done", "blocked", "stalled", "error"]
    },
    "execution_trace": {
      "type": "object",
      "required": ["selected_skill", "plan_reviewed_rounds"],
      "properties": {
        "selected_skill": {
          "type": "string",
          "pattern": "^/[a-z0-9-]+"
        },
        "plan_reviewed_rounds": {
          "type": "integer",
          "minimum": 0,
          "maximum": 3,
          "description": "0 for direct routine work; otherwise number of explicit plan reviews"
        },
        "post_check_plan_next_rerun": {
          "type": "boolean",
          "description": "true after a modifying action; omit for no-op or read-only checks"
        }
      },
      "additionalProperties": false
    }
  },
  "additionalProperties": false
}
```

---

## Self-Check

### Required sections present

- [ ] All 11 required sections exist (Purpose / Core Objective / Scope Boundaries / Use Cases / Behavior / Input & Output / Restrictions / Anti-Patterns / Examples / AI Repair Instructions / Self-Check)
- [ ] The Semantic Role block exists and states the difference from plan-next / loop / orchestrate-repair-loop

### Core success criteria

- [ ] Each invocation runs at most 1 action; no-op outcomes identify why no action was safe/applicable
- [ ] Stall detection: a fingerprint repeated 2 times within a session fires stalled
- [ ] Execution safeguards match impact and ambiguity; any required plan was reviewed once before action
- [ ] After a modifying action, re-run plan-next and verify evidence/decision state, not merely card disappearance
- [ ] `actionable`, `needs_input`, `no_applicable_action`, and `complete` are represented distinctly
- [ ] Human-owned and external work is reported as deferred/waiting, not persisted as a recommendation skip
- [ ] A valid continuation_signal is emitted every time (advance / done / blocked / stalled / error)
- [ ] **The `done` signal requires a fresh plan-next `complete` state with acceptance evidence**, not an empty list
- [ ] Missing or conflicting route evidence triggers at most one re-diagnosis; unresolved applicability asks the user
- [ ] No human-gate decision wrote `.ai-cortex/plan-next.yaml`; an unfinished exclusion never satisfied a dependency
- [ ] **In cron mode (fixed interval), the first report carries the suggestion to switch to a dynamic /loop**
- [ ] **The 2nd consecutive `stalled` carries the "CronDelete `<job-id>` immediately" prompt**

### Quality gate checks

- [ ] Hard Boundaries use MUST / MUST NOT and state how each is verified
- [ ] Anti-Patterns has ≥ 2 contrasting examples (11 in practice)
- [ ] Examples has ≥ 2, of which ≥ 1 is an edge case (example 3 covers stall detection)
- [ ] The AI repair instructions cover ≥ 2 error patterns (3 in practice)

### Acceptance test

After execution, does the IterationStepReport state clearly what was done, how it turned out, and whether the next step is to continue or to bring in a human? If not → rewrite the IterationStepReport.
