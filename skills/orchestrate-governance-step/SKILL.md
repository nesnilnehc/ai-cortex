---
name: orchestrate-governance-step
description: Single-step governance executor — reads plan-next routing output, executes the highest-priority action, and emits a continuation signal for /loop-driven autopilot.
description_zh: 单步治理执行器——读取 plan-next 路由输出，执行最高优先级动作，发出继续信号以支持 /loop 全自动推进。
tags: [automation, workflow, meta-skill]
version: 2.2.0
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
  description: "IterationStepReport: action taken, skill invoked, outcome, continuation_signal (advance | done | blocked | stalled | error)."
---

# Skill: Auto-iterate (orchestrate-governance-step)

> **Role**: single-step governance executor — the execution half that pairs with plan-next
> **WHAT**: each invocation carries out 1 plan-next routing suggestion and emits a `continuation_signal` for `/loop` to drive the next iteration
> **HOW**: call plan-next internally → take the highest-priority card → apply the human gate → run the sub-skill → verify afterwards → emit the report
> **Distinct from**: `plan-next` (read-only diagnosis, no execution); `/loop` (scheduling only, no business logic); `orchestrate-repair-loop` (repairs code defects, does not advance the governance layer)

---

## Purpose

Turn a plan-next routing suggestion into one executable governance action, which is what makes a fully automatic autopilot (`/loop /orchestrate-governance-step`) possible.

plan-next can only diagnose and suggest; the user has to run each suggestion by hand. orchestrate-governance-step fills that execution gap and, together with `/loop`, gives three orthogonal layers of automation:

| Layer | Skill | Responsibility |
|---|---|---|
| Scheduling | `/loop` | Fires once every N minutes |
| **Driving** | **orchestrate-governance-step** | Read the routing → run 1 step → report |
| Diagnosis | `plan-next` | Inventory + gap identification + routing suggestions (read-only) |

---

## Core Objective

**Primary goal**: each invocation carries out exactly 1 governance action and states, through the IterationStepReport, what the result was and whether to continue.

**Success criteria** (all must be met):

1. ✅ **Single step**: each invocation runs exactly 1 routing action, and no more
2. ✅ **Stall detection**: when the same routing-card fingerprint appears 2 times in a row within a session and the target has not advanced, the `stalled` signal fires
3. ✅ **Post-execution verification**: after the sub-skill runs, plan-next is re-run to confirm whether the target card has disappeared
4. ✅ **Human gate**: a strategic or creative skill (define-mission, design-strategic-goals, and the like) must pause and tell the user before it runs
5. ✅ **Explicit continuation signal**: every invocation must emit one of the five `continuation_signal` values in the IterationStepReport

**Acceptance test**: after execution, does the IterationStepReport state clearly what was done, how it turned out, and whether the next step is to continue or to bring in a human?

---

## Scope Boundaries

**This skill covers**:
- Calling plan-next internally to get the routing
- Taking the highest-priority card from "Do now" (`urgent` > `important` > `defer`)
- Stall detection (fingerprint comparison within the session)
- The human gate (skip a blocked card by default and try the next one; emit blocked only once every card has been skipped)
- Drafting an execution plan + a self-review loop (3 rounds maximum)
- Running 1 sub-skill (once the plan passes)
- Light post-execution verification
- Emitting the IterationStepReport

**This skill does not cover**:
- Governance diagnosis and routing generation → `plan-next`
- Loop scheduling → `/loop` (built into Claude Code)
- The code-defect repair loop → `orchestrate-repair-loop`
- The content of strategic and creative decisions (mission, vision, strategic goals) → a human is needed

**Handoff points**:
- `continuation_signal: done` → governance is ready; tell the user and stop
- `continuation_signal: blocked | stalled | error` → a human is needed; stop and explain why

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

Record the **target card fingerprint** (used for stall detection):

```text
fingerprint = subject field + "||" + governance context field
```

### Step 2: parse the routing

Sort "Do now" by priority (`urgent` → `important` → `defer` → `awaiting execution`) and **try the cards one by one** until you reach the first that is not on the session skip-list and passes the step 4 human gate.

**Skip-list mechanism**: the session keeps a skip-list (a set of fingerprints); when step 4 triggers a skip, the current card's fingerprint is added to it. This step skips any card on the skip-list as it iterates.

**End states of the iteration**:

- An executable card is found → go to step 5
- Every card was skipped (the skip-list covers all of "Do now") → `continuation_signal: blocked`, and the report lists every skipped card with its blocking reason
- "Do now" is itself empty → apply the three-state decision below

**Three-state decision** (do not mistake "awaiting execution" for "finished"):

| plan-next output | continuation_signal | Meaning |
|---|---|---|
| Routing cards present (urgent / important / defer) | Continue at step 3 | Governance has a gap; a sub-skill can run |
| Only "awaiting execution" cards (tasks already broken down, waiting on development) | `blocked` | Governance is ready, waiting on outside work |
| Completely empty (every goal has status=done and the L1 KPI is met) | `done` | Governance and acceptance are both met |

**Key constraints**:
- An empty "Do now" ≠ done. It must first be confirmed that plan-next reached that verdict after the L1 acceptance-KPI check and the L5 awaiting-execution branch
- If the plan-next output carries no L1 acceptance-KPI status field → treat the plan-next call as non-compliant, emit `error`, and prompt for a plan-next upgrade
- A strategic goal with `status = approved` whose acceptance is not met → plan-next necessarily returns routing (establish the KPI, or an awaiting-execution card), so the result is not empty

### Step 3: stall detection

Compare this fingerprint with the **fingerprint of the previous execution** in the session:

- **Same** → `continuation_signal: stalled`, stating "the target card did not advance after the last execution", and stop
- **Different (or first invocation)** → continue

### Step 4: human gate (skip by default, do not abort)

In the following cases the current card counts as **blocked**: add its fingerprint to the session skip-list and **go back to step 2 to try the next one**, rather than terminating /loop right away:

- The recommended skill is a creative or strategic one: `define-mission`, `design-strategic-goals`, `define-vision`, `define-north-star`, `define-strategic-pillars`
- The card's completion marker contains "return to plan-next for re-evaluation if blocked", and that has already fired
- **The card's label is `awaiting execution`**: governance is ready and outside development has to run it, so there is no governance skill to call
- **The first routing item is to establish the L1 acceptance-KPI data source** and the recommended skill is a design or architecture one: the monitoring approach needs human confirmation and is not run automatically

**Only once the skip-list covers every card in "Do now"** is `continuation_signal: blocked` emitted, with the IterationStepReport listing every skipped item and its blocking reason and asking the user to step in.

**Why skip by default instead of stopping immediately**: the value of /loop lies in advancing everything that can be automated; stopping at the first creative card would pointlessly block the N non-creative cards behind it. Skipping keeps the non-blocked work flowing and collects the parts that need a human into one report.

### Step 5: plan-first execution (draft → self-review loop → run once it passes)

Once an executable card is located, **the recommended skill must not be called directly**. The execution plan must be drafted and pass self-review first; only then leave plan mode and run it.

#### 5.1 Draft the plan (EnterPlanMode)

Enter plan mode and produce an execution plan for that card, containing:

- **Goal**: quote the routing card's subject + completion marker, word for word
- **The sub-skill command to be called**: the complete `/skill-name [focus]`
- **Where the focus comes from**: the sentence in the routing card it was derived from (this prevents overreach)
- **Expected output**: the file paths to be created or modified, and the key fields
- **Scope red lines**: the files and scope this step MUST NOT touch (this prevents casual expansion)
- **Rollback points**: the recovery path when execution fails (which files are new and can simply be deleted, which are modifications needing git restore)

#### 5.2 Plan self-review loop (3 rounds maximum)

Each round checks the plan against the list below; on any defect, revise it and review again:

| Check | What counts as a defect |
|---|---|
| The goal matches the routing card | The plan's goal diverges from, or drops part of, the card's subject or completion marker |
| Single-step semantics | The plan implicitly runs ≥ 2 sub-skills or covers ≥ 2 cards |
| The focus is traceable | The focus has no support in the card's own text |
| Scope red lines are explicit | The "MUST NOT touch" paragraph is missing or written too broadly ("do not break other files" does not count as explicit) |
| Expected output is verifiable | File paths and fields are not made concrete, leaving the step 6 plan-next re-run nothing to compare against |
| Rollback points exist | A modifying operation declares no git restore anchor |

Passing verdict: **one review round with 0 defects**.

**Cap reached**: still defective after 3 consecutive rounds → `continuation_signal: error`, the IterationStepReport lists the defects left after the final round, and execution stops; **do not** push ahead with a known defect.

#### 5.3 Execution (after ExitPlanMode)

Once the self-review passes, leave plan mode and call `/skill-name [focus]` as planned.

- The plan turns out to diverge from reality during execution (the file already exists, a dependency is missing) → **do not** widen the scope on the spot; abort execution, emit `continuation_signal: error`, and record the divergence in the report
- Execution fails with no recovery path → `continuation_signal: error`, emit the report, stop

### Step 6: post-execution verification

**Re-running** `/plan-next` **is mandatory** (it cannot be skipped): check whether the target card has disappeared from "Do now".
The only legitimate source of a `done` signal is this step's verification result — substituting the model's own inference is forbidden.

| Result | Action |
|---|---|
| The card is gone, "Do now" still has entries | `continuation_signal: advance` |
| The card is gone, "Do now" is empty | `continuation_signal: done` |
| The card is still there | Update the stall counter; when the count reaches 2 → `continuation_signal: stalled` |

### Step 7: emit the IterationStepReport

---

## Interaction with /loop (important)

`/loop` has two modes, and they consume `continuation_signal` in completely different ways:

| /loop mode | How it fires | Signal consumption | Recommended use |
|---|---|---|---|
| **Dynamic** | No interval (self-scheduled ScheduleWakeup) | Reads `continuation_signal`: done/blocked/stalled/error stop the loop | ✅ **Recommended**: `/loop /orchestrate-governance-step` (no interval) |
| **Fixed-interval (cron)** | An interval is given (`5m`, say) | **Does not read** `continuation_signal`: cron keeps firing and the signal is ignored | ⚠️ Not recommended where automatic stopping matters; the user must CronDelete by hand |

**Mandatory behavior**:
- On detecting fixed-interval cron mode (through a CronCreate record in the session context whose prompt is `/orchestrate-governance-step`), the first IterationStepReport must warn the user: "this is cron mode and the signal is ignored; to stop the repeated firing, switch to a dynamic /loop, or CronDelete once you get stalled/blocked/done"
- On the 2nd consecutive `stalled` signal, the IterationStepReport must state "**CronDelete <job-id> immediately, strongly recommended**" and give the job ID

**The fix**: a user who wants it to "stop automatically once governance is ready" should use `/loop /orchestrate-governance-step` (no interval, dynamic mode), not `/loop 1m /orchestrate-governance-step`.

---

## Input & Output

### Input

| Parameter | Required | Default | Description |
|---|---|---|---|
| `docs_root` | No | auto | The governance docs root; auto means the same default path as plan-next |
| `pre_run_output` | No | — | A pre-run plan-next output; when supplied, the internal call is skipped |

### Output: IterationStepReport

```markdown
## What this automatic step did

- **What was done**: [describe it with file names or feature names; the words "routing card" and "governance layer" are banned]
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
|---|---|---|
| `advance` | The action finished and governance still has work | Fire again |
| `done` | "Do now" was empty when plan-next was re-run in step 6; **emitting this value from the model's own inference is forbidden** | Stop the loop |
| `blocked` | Every card in "Do now" either hit the human gate or is "awaiting execution" (nothing executable was left after trying and skipping each one) | Stop the loop and wait for the user |
| `stalled` | The same routing card made no progress for 2 rounds in a row | Stop the loop and report the stall |
| `error` | The sub-skill failed with no recovery path | Stop the loop and report the error |

---

## Restrictions

### Hard Boundaries

**Rule 1**: an invocation MUST NOT run more than 1 action
- Verification: the IterationStepReport has exactly 1 entry in the `skill called` field
- Consequence: REJECT (it breaks the single-step semantics of the three-layer model)

**Rule 2**: a strategic or creative skill MUST trigger the human gate and must not be run directly
- Verification: when the recommended skill is define-mission or similar, that card goes on the session skip-list and the next one is tried; if every card is skipped, the report shows `blocked` and lists every blocked item
- Consequence: REJECT (strategic decisions are not there to be automated)

**Rule 3**: every invocation MUST emit a valid `continuation_signal`
- Verification: the IterationStepReport carries the `continuation signal` field and its value is one of the five in the enum
- Consequence: REJECT (/loop depends on this signal to decide whether to continue)

**Rule 4**: the `done` signal MUST come from the step 6 plan-next re-run, and MUST NOT come from the model's own inference
- Verification: the IterationStepReport notes carry no self-assessment language such as "the whole governance layer is ready" or "everything currently executable has been created"; `done` is emitted only after step 6 confirms that "Do now" is empty
- Consequence: REJECT (the model took the routing judgment away from plan-next, breaking the responsibility boundaries of the three-layer model)

**Rule 5**: `done` MUST satisfy all three at once — the plan-next output declares "the L1 acceptance KPI is met" AND "Do now is empty" AND "there is no awaiting-execution card"
- Verification: when emitting `done`, the IterationStepReport quotes the KPI status field from the plan-next governance context (such as "citation visibility 85% ≥ 80% (met)"); as long as the KPI is unmet, its data is missing, or an "awaiting execution" card is present, `done` must never be emitted
- Consequence: REJECT (mistaking "strategic goal status=approved" for acceptance being met makes /loop stop at the wrong time)

**Rule 6**: a card labeled "awaiting execution" MUST go on the skip-list with the next one tried, and MUST NOT be executed or turned straight into done; `blocked` is emitted only once every card has been skipped
- Verification: selected_skill is left unfilled on an "awaiting execution" card; if the end state is blocked, next_step carries the words "governance is ready, waiting on outside execution" and lists every skipped item
- Consequence: REJECT

**Rule 7**: MUST enter plan mode, draft the plan, and pass the self-review loop before executing; MUST NOT call the recommended skill directly
- Verification: the IterationStepReport carries a `plan_reviewed_rounds` field (≥1) and the final round leaves no defect; a divergence found in a failed execution must not be used as grounds for "expanding the plan's scope"
- Consequence: REJECT (skipping the plan stage lets the single-step semantics and the scope red lines get out of hand, and leaves downstream auditing with nothing to go on)

**Rule 8**: plan self-review MUST NOT exceed 3 rounds; beyond that, emit error — a defective plan must not be forced through
- Verification: `plan_reviewed_rounds ≤ 3`; beyond it, `continuation_signal: error` and next_step carries the list of remaining defects
- Consequence: REJECT (unbounded self-review either loops forever or rationalizes the defect away)

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

**Why it is correct**: single-step execution keeps the three layers orthogonal; the post-check confirms real progress; /loop drives the next step naturally.

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

**What goes wrong**: it violates the skip-by-default constraint. /loop exists to advance everything automatable and to hand the blocked items to the user together at the end. The right move: put that card on the session skip-list and go back to step 2 for the next one; only when every card has been skipped does it become `blocked`.

---

### ❌ Wrong: skipping plan mode and calling the recommended skill directly

```text
1. Step 2 finds the capture-work-items card
2. Call /capture-work-items … directly
3. The skill "completes" 3 seemingly related fields along the way, beyond the card's scope
```

**What goes wrong**: it violates Rule 7. Without a plan stage writing down "focus / scope red lines / rollback points", a sub-skill very easily expands its reach along the way, and a downstream audit cannot work out "why X was changed". The right move: EnterPlanMode and draft the plan, pass the self-review, then ExitPlanMode and execute.

---

### ❌ Wrong: forcing a defective plan through after 5 review rounds

```text
1. Draft the plan → review 1: the focus has no traceable source → revise
2. Review 2: the scope red lines are missing → revise
3. Review 3: the rollback points are still not filled in
4. The model decides "what is left is minor" and forces execution
```

**What goes wrong**: it violates Rule 8. The 3-round self-review cap is a hard constraint; going past it means the plan drafting itself has a structural problem (an unclear card, a mismatched recommended skill), and the answer is to emit error and hand it back to a human rather than rationalizing "the self-review failed" into "a minor problem".

---

### ❌ Wrong: reporting advance while skipping the post-execution check

```text
1. /capture-work-items finishes
2. continuation_signal: advance is reported directly
3. In reality the file was never written
```

**What goes wrong**: without the post-check, advance is false; the next plan-next produces the same routing and triggers stalled.

---

### ❌ Wrong: deciding "governance is finished" instead of re-running plan-next in step 6

```text
1. The sub-skill runs successfully
2. The model infers "every governance document that can be created has been created; the rest depends on the developer execution layer"
3. continuation_signal: done is emitted directly, with no plan-next re-run
```

**What goes wrong**: the model has taken over the "governance layer vs developer execution layer" judgment — that is plan-next's job, not orchestrate-governance-step's. A blocked node (T48/T52 depending on T47/T49, say) is for plan-next to route and to trigger a `blocked` signal, not for the model to declare "governance finished" on its own. `done` has exactly one legitimate source: "Do now" is empty when plan-next is re-run in step 6.

---

### ❌ Wrong: treating `strategic goal status=approved` as acceptance met → emitting done

```text
1. plan-next: G1 status=approved, and the acceptance KPI "citation visibility" has no monitoring data
2. orchestrate-governance-step takes an empty "Do now" (plan-next really ought to return routing here, but this example assumes plan-next misjudged it too)
3. done is emitted and /loop stops
4. G1 is in fact nowhere near met; the next wake-up check falls into a stalled loop
```

**What goes wrong**: it violates Rule 5 — the plan-next output must first be confirmed to carry the L1 acceptance-KPI status field with the KPI met; otherwise done is wrong even when "Do now" is empty. `approved` only means the decision was approved; while acceptance is unmet the work carries on, and the output belongs as blocked (waiting on execution + waiting on KPI data).

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
4. **Enter plan mode and draft the plan**:
   - Goal: register the 3 M5-stage backlog entries (quoting the card subject)
   - Sub-skill command: `/capture-work-items register the 3 requirements newly found in M5 into the backlog`
   - Focus traceability: the card says "the M5 sweep found 3 requirements scattered through discussions"
   - Expected output: 3 new markdown files under `backlog/`, with frontmatter
   - Scope red lines: MUST NOT modify existing backlog entries; MUST NOT touch `roadmap/` or `requirements/`
   - Rollback points: the new files can be removed with `git clean -f backlog/<new-files>`
5. **Self-review loop**: round 1 passes all 6 checks → `plan_reviewed_rounds = 1`, leave plan mode
6. Run `/capture-work-items register the 3 requirements newly found in M5 into the backlog`
7. Post-execution check: re-run plan-next → that card is gone, "Do now" still has 1 entry → advance

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
- _(internal) continuation signal: advance; plan_reviewed_rounds: 1_
```

---

### Example 2: the human gate skips a card → the next non-creative card is taken

**Scenario**: plan-next routes two cards: `design-strategic-goals` (important, strategic/creative) + `capture-work-items` (defer, registration).

**Execution**:
1. Call plan-next internally → two routing cards
2. Stall detection: first invocation → continue
3. Step 2 takes the highest priority: `design-strategic-goals`
4. Step 4 human gate: it is strategic/creative → add to the skip-list, back to step 2
5. Step 2 takes the next one: `capture-work-items` is not on the skip-list
6. Step 4 human gate: not creative → pass
7. Step 5.1 enter plan mode and draft the plan (the same six-part structure as example 1, omitted here)
8. Step 5.2 self-review: passes in 1 round → `plan_reviewed_rounds = 1`
9. Step 5.3 leave plan mode and run `/capture-work-items …`
10. Step 6 re-run plan-next: the `capture-work-items` card is gone → `advance`

**IterationStepReport**:

```markdown
## What this automatic step did

- **What was done**: registered the 3 backlog entries added in stage M5
- **Why it needed fixing**: the strategic-goal card needs human judgment and was skipped; the same batch held another card that could run automatically
- **Result**: Success ✅
- **Next**: keep going automatically (skipped, awaiting a human: 1 — `design-strategic-goals`)
- _(internal) continuation signal: advance; plan_reviewed_rounds: 1; skipped this time: [design-strategic-goals]_
```

---

### Example 2b: every routing card is skipped → blocked

**Scenario**: plan-next routes two cards, both either strategic/creative or "awaiting execution".

**Execution**:
1. plan-next → `define-mission` (important) + one `awaiting execution` card
2. Step 2 takes `define-mission` → step 4 adds it to the skip-list → back to step 2
3. Step 2 takes the "awaiting execution" card → step 4 adds it to the skip-list → back to step 2
4. Every entry in "Do now" is on the skip-list → emit `blocked`

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
```

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
     - Sub-skill succeeded + no routing → `done`
     - The human gate fired → `blocked`
     - The fingerprint repeated → `stalled`
     - The sub-skill failed → `error`
  2. Explain why in the `Next` field

---

### Problem 3: reporting advance while skipping the post-execution check

- **How to spot it**: the report says `advance` but plan-next was never re-run to confirm
- **How to correct it**:
  1. Re-run `/plan-next` and check whether the target card is gone
  2. If it is gone → `advance` is confirmed correct
  3. If it is still there → update the stall count; on the 2nd occurrence → correct it to `stalled`

---

### Problem 4: judging completion internally and skipping step 6

- **How to spot it**: the `Next` field carries self-assessment language such as "the whole governance layer is ready", "everything currently executable has been created", or "this belongs to the developer execution layer", with no record of a step 6 plan-next re-run
- **How to correct it**:
  1. Re-run `/plan-next`
  2. If "Do now" is empty → `done` was right, and the report needs no change
  3. If "Do now" holds only blocked entries → correct the internal continuation signal to `blocked` and explain the blocking reason in `Next`
  4. If "Do now" still has executable entries → correct the internal continuation signal to `advance` and carry on

---

## Appendix: Output contract

### YAML schema (formal)

```yaml
type: object
# execution_trace is required only when continuation_signal ∈ {advance, done};
# the blocked / stalled / error paths run no sub-skill and do not require the field.
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
  continuation_signal:
    type: string
    enum: [advance, done, blocked, stalled, error]
  execution_trace:
    type: object
    required: [selected_skill, plan_reviewed_rounds, post_check_plan_next_rerun]
    properties:
      selected_skill:
        type: string
        pattern: "^/[a-z0-9-]+"
      plan_reviewed_rounds:
        type: integer
        minimum: 1
        maximum: 3
      post_check_plan_next_rerun:
        type: boolean
        const: true
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
    "continuation_signal"
  ],
  "allOf": [
    {
      "if": {
        "properties": {
          "continuation_signal": { "enum": ["advance", "done"] }
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
    "continuation_signal": {
      "type": "string",
      "enum": ["advance", "done", "blocked", "stalled", "error"]
    },
    "execution_trace": {
      "type": "object",
      "required": ["selected_skill", "plan_reviewed_rounds", "post_check_plan_next_rerun"],
      "properties": {
        "selected_skill": {
          "type": "string",
          "pattern": "^/[a-z0-9-]+"
        },
        "plan_reviewed_rounds": {
          "type": "integer",
          "minimum": 1,
          "maximum": 3,
          "description": "number of plan self-review rounds; execution is allowed only when the final round has 0 defects"
        },
        "post_check_plan_next_rerun": {
          "type": "boolean",
          "const": true
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

- [ ] Each invocation runs exactly 1 action, and no more
- [ ] Stall detection: a fingerprint repeated 2 times within a session fires stalled
- [ ] Plan before execution: enter plan mode and draft the plan; the self-review loop is ≤ 3 rounds and execution is allowed only once the final round has 0 defects
- [ ] Post-execution check: re-run plan-next and confirm that the target card is gone
- [ ] Was the step 6 plan-next re-run actually carried out? ("inferring governance completion internally" is not accepted as a substitute; the notes carry no self-assessment language)
- [ ] Human gate: a strategic or creative skill and an "awaiting execution" card go on the skip-list by default and the next card is tried; blocked is emitted only once every card in "Do now" has been skipped
- [ ] A valid continuation_signal is emitted every time (advance / done / blocked / stalled / error)
- [ ] **Does the "governance context" in the plan-next output carry the current L1 acceptance-KPI status**? If not, treat plan-next as non-compliant, emit error, and prompt for an upgrade
- [ ] **The `done` signal satisfies all three conditions**: the plan-next output has "Do now" empty + the KPI met + no "awaiting execution" card
- [ ] **In cron mode (fixed interval), the first report carries the suggestion to switch to a dynamic /loop**
- [ ] **The 2nd consecutive `stalled` carries the "CronDelete <job-id> immediately" prompt**

### Quality gate checks

- [ ] Hard Boundaries use MUST / MUST NOT and state how each is verified
- [ ] Anti-Patterns has ≥ 2 contrasting examples (4 in practice)
- [ ] Examples has ≥ 2, of which ≥ 1 is an edge case (example 3 covers stall detection)
- [ ] The AI repair instructions cover ≥ 2 error patterns (3 in practice)

### Acceptance test

After execution, does the IterationStepReport state clearly what was done, how it turned out, and whether the next step is to continue or to bring in a human? If not → rewrite the IterationStepReport.
