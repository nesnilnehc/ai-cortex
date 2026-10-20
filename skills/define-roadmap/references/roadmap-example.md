# Service Desk examples and execution-status reference

The [complete casebook](service-desk/README.md) contains filled deliverables from
priority decisions through archival, using the same four source IDs throughout.
Start with the [initial three-view roadmap](service-desk/initial/roadmap.md) and
compare its [adjusted](service-desk/adjusted/roadmap.md) and
[after-delivery](service-desk/after-delivery/roadmap.md) snapshots. All facts are
fictional; unknown real project facts must not be inferred from these examples.

## Status examples and counterexamples

| Source facts | Correct execution cell | Key condition / source detail | Incorrect expression |
| --- | --- | --- | --- |
| Approved; execution has not begun | Not started | Start after the source prerequisite | Approved or Now as execution status |
| Development complete; acceptance pending | Awaiting acceptance | Acceptance session pending; evidence linked | Completed; 128 tests passed; commit abc123 |
| Acceptance passed; required production release pending | Awaiting release | Production release pending; acceptance linked | Completed because acceptance passed |
| An explicit decision suspends work, with a blocker also recorded | Paused | Resume decision required; blocker remains linked | Paused / Blocked |
| Release cannot proceed without a required credential | Blocked | Restore release credential; blocker linked | Awaiting release despite a confirmed impediment |
| A delivery risk exists but work continues | In progress | Link the next delivery condition and source risk | At risk |
| Project closure evidence is verified | Completed | —; detailed evidence stays in source | Completed plus a chronology of tests and commits |

Missing or conflicting evidence is reported as unverified outside the execution
cell. Do not guess Completed, or force Not started as a fallback. For work whose
existing closure criterion does not require production release, verified acceptance
may establish Completed; do not add a release requirement from this example.
