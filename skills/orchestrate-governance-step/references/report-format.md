# orchestrate-governance-step: report format

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

### continuation_signal semantics

| Value | Meaning | /loop behavior |
| --- | --- | --- |
| `advance` | The action finished and governance still has work | Fire again |
| `done` | Fresh plan-next explicitly reports `complete` and supplies acceptance evidence; **emitting this value from the model's own inference is forbidden** | Stop the loop |
| `blocked` | No safe action can proceed now; report `needs_input` (user fact/decision needed) or `no_applicable_action` (waiting, excluded, or dependency-protected) distinctly | Stop the loop and ask or wait |
| `stalled` | The same routing card made no progress for 2 rounds in a row | Stop the loop and report the stall |
| `error` | The sub-skill failed with no recovery path | Stop the loop and report the error |

---
