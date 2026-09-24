---
name: orchestrate-governance-step
description: Safely advances one governance action from plan-next, re-diagnoses stale or conflicting routes, and reports whether to continue, ask, wait, or stop.
version: 3.0.1
license: MIT
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

## Interaction with /loop

When invoked by a scheduler, read the [loop integration guidance](references/loop-integration.md).

---

## Input & Output

### Input

| Parameter | Required | Default | Description |
| --- | --- | --- | --- |
| `docs_root` | No | auto | The governance docs root; auto means the same default path as plan-next |
| `pre_run_output` | No | — | A pre-run plan-next output; when supplied, the internal call is skipped |

### Output: IterationStepReport

## Report format

Before reporting, read the [IterationStepReport format](references/report-format.md). For machine-readable output, also use the [formal schema](references/output-contract.md).

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

Consult [anti-patterns](references/anti-patterns.md) when a routing or execution choice is unclear.

---

## Examples

Consult [worked examples](references/examples.md) for unusual gating or stall cases.

---

## Repair guidance

Consult [repair instructions](references/repair-instructions.md) if this skill itself fails a step.

---

## Output contract

Use the [formal report schema](references/output-contract.md) when a machine-readable IterationStepReport is needed.

---

## Self-Check

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

### Acceptance test

After execution, does the IterationStepReport state clearly what was done, how it turned out, and whether the next step is to continue or to bring in a human? If not → rewrite the IterationStepReport.
