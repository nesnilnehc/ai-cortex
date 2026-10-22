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
| Policy | [Requirement Priority Policy](priority-policy.md) | One reusable rule source; current results link to records rather than a duplicated inventory |
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

The modern iteration outputs lead with the plan and place policy, closure and
maintenance evidence after revisions. Their policy link points to the independent
policy above. Old single-view snapshots keep their compatible presentation; the
linked source policy anchor remains valid. Titles follow document roles without
renaming established snapshot folders or requiring a separate planning-basis file.

## Phase and event interpretation

The 1.1 inputs also show PSEARCH as a work span, M0 as global kickoff, M1/M2 as acceptance events and M3 as production release. V1 initially carries search, then V2 carries it; distinct event IDs preserve the version span and both W6 events. See the source phase/event tables for timing and evidence.

## Retained revisions

Revision history is introduced with schema 1.2: initial is the adopted baseline, adjusted retains REV1, and after-delivery shows REV2 then REV1. The [revision register](change-record.md#revision-register) preserves reasons, impacts and evidence; rerendering never appends another decision.

## Iteration and layout examples

Read the [iteration decisions](iterations.md) first, then compare the
[single document](iteration-driven/roadmap.md) with the
[split main](iteration-driven-split/roadmap.md),
[delivery detail](iteration-driven-split/roadmap-delivery.md) and
[revision detail](iteration-driven-split/roadmap-history.md).
They render the same schema 1.3 [input](iteration-driven/input.json). There is no
second editable input in the split folder. Both output directories are siblings,
so their relative source links resolve identically. This is an alternate view of
the adjusted plan, not a new later delivery claim or a replacement for old snapshots.

BUG1 spans I1/I2 but remains in V1; I2 touches V1/V2; R1 spans I2/I3 and remains
in V2. R2/R3 stay unallocated. Near-term iteration goals do not grant release
permission or move priorities. REV3 records cadence/allocation adoption, preserving
REV1 and its original deadline impact.

Reproduce from the repository root:

```sh
python3 skills/define-roadmap/scripts/render-roadmap.py skills/define-roadmap/references/service-desk/iteration-driven/input.json --output-dir skills/define-roadmap/references/service-desk/iteration-driven --overwrite
python3 skills/define-roadmap/scripts/render-roadmap.py skills/define-roadmap/references/service-desk/iteration-driven/input.json --layout split --output-dir skills/define-roadmap/references/service-desk/iteration-driven-split --overwrite
```

## Structure-first topic split

The [paired structure and populated example](../structure-first.md) preserves this
case while separating iteration, version, milestone, planning-basis and revision
details. It demonstrates reader roles and review stages without making six files mandatory.
