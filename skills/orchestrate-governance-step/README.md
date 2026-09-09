# orchestrate-governance-step

A single-step governance executor — the execution layer that pairs with plan-next.

## In one line

Reads the routing output of plan-next, runs the highest-priority action, and returns a `continuation_signal` that `/loop` uses to drive the iteration forward.

## Position in the three-layer model

```text
/loop /orchestrate-governance-step 30m
  └─ orchestrate-governance-step        ← driver layer (this skill)
       └─ /plan-next     ← diagnostic layer (read-only)
```

## How to use

| Scenario | Command |
|---|---|
| Run the next governance action | `/orchestrate-governance-step` |
| Fully automatic autopilot | `/loop /orchestrate-governance-step` |
| Advance automatically every 30 minutes | `/loop /orchestrate-governance-step 30m` |
| Only view the suggestions (no execution) | `/plan-next` |

## Output: IterationStepReport

Every invocation emits one report containing:
- The action executed and the governance context
- The sub-skills invoked
- The execution result
- `continuation_signal`: `advance` / `done` / `blocked` / `stalled` / `error`

## Stop conditions

| Signal | Reason |
|---|---|
| `done` | The whole governance chain is ready |
| `blocked` | A strategic or creative skill needs a human |
| `stalled` | The same routing card made no progress 2 times running |
| `error` | A sub-skill failed to execute |

## References

- `skills/plan-next/SKILL.md` — the diagnostic layer
- `docs/adr/0007-remove-plan-next-execute-flag.md` — the three-layer model decision
