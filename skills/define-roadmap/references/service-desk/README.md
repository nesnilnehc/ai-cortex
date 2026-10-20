# Service Desk: a complete roadmap example

These are filled deliverables for one fictional project, not templates or evidence
of a real release. Each snapshot preserves its stage's facts. Real projects keep
one active roadmap; this teaching example retains several snapshots for comparison.
W1 is relative to an unspecified project start. The document update date is the
example's editorial date, not a claim that future work has happened.

## Read the deliverables

| Step | Finished deliverable | What it demonstrates |
| --- | --- | --- |
| 1 | [Source records](sources.md) | Four stable work IDs, project policy, stage facts and delivery evidence |
| 2 | [Priority decisions](priority-decisions.md) | Apply policy without replacing settled priorities |
| 3 | [Dependencies and blocked list](dependencies.md) | Preserve importance while exposing start conditions |
| 4 | [Initial roadmap](initial/roadmap.md) · [Gantt chart](initial/roadmap.svg) · [input](initial/input.json) | Requirement, version and schedule views agree |
| 5 | [Faulty roadmap](problematic/roadmap.md) · [invalid input](problematic/input.json) | Two deliberately planted defects, clearly separated from good examples |
| 6 | [Review findings](review-findings.md) | Findings cite evidence and quality criteria without claiming an unchecked pass |
| 7 | [Change record](change-record.md) · [placement decisions](placement-decisions.md) | Handle blocking, version movement and a missed deadline without conflating tier and version |
| 8 | [Adjusted roadmap](adjusted/roadmap.md) · [Gantt chart](adjusted/roadmap.svg) · [input](adjusted/input.json) | The blocker and downstream time changes agree |
| 9 | [After-delivery roadmap](after-delivery/roadmap.md) · [Gantt chart](after-delivery/roadmap.svg) · [input](after-delivery/input.json) | Actual delivery and still-planned work remain distinct |
| 10 | [Version archive](version-archive.md) | Planned versus actual scope and every unfinished item's destination |

The review also links its [corrected candidate](initial/roadmap.md), which removes
the two planted mistakes before the separate W1 blocking event.

## Follow one story

Fix duplicate submission (BUG1), then deliver search (R1), then export (R2).
Reminders (R3) wait for user demand. A missing acceptance sandbox blocks BUG1 at
W1. Search moves from V1 to V2; export moves from V2 to a new V3. Export misses
its original hard deadline, so the product owner explicitly accepts a new delivery
commitment. V1 and V2 eventually deliver; V3 and unassigned R3 remain visible.

## Reproduce a view

From the AI Cortex clone, validate an input and render it into a scratch directory:

```sh
python3 skills/define-roadmap/scripts/render-roadmap.py skills/define-roadmap/references/service-desk/initial/input.json --check
python3 scripts/test-roadmap-examples.py
```

The test validates inputs and reproduces the checked-in Markdown and SVG. It also
checks source links, decisions, scope, timing, execution and unfinished-item
disposition, and deliberately perturbs facts to prove that drift is detected.
For scratch-directory rendering, rebase the input's relative source links if the
output directory differs from the checked-in snapshot location. Do not edit
generated roadmaps independently of their input and source evidence.

The former `assets/roadmap-input-example.json` path remains a relative symlink to
`initial/input.json`; it is an alias, not an independently maintained input.

## Phase and event interpretation

The 1.1 inputs also show PSEARCH as a work span, M0 as global kickoff, M1/M2 as acceptance events and M3 as production release. V1 initially carries search, then V2 carries it; distinct event IDs preserve the version span and both W6 events. See the source phase/event tables for timing and evidence.
