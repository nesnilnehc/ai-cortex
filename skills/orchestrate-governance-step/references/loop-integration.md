# orchestrate-governance-step: loop integration

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
