# orchestrate-governance-step: anti patterns

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
