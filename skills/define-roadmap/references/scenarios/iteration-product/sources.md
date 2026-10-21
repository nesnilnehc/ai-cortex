# Request Search Product source facts

Fictional completed planning example, adopted 2026-10-21. These are teaching facts,
not universal defaults or real commitments. Planned work is not claimed completed.

## Context

| Field | Value |
| --- | --- |
| work_mode | iterations |
| delivery | versioned |
| audience | Product team, release coordinator and pilot customer |
| constraints | Two-week planning; monthly named releases; no external hard deadline |

## Planning basis

| Field | Value |
| --- | --- |
| project | Request Search Product |
| updated | 2026-10-21 |
| direction | Make requests findable before adding reuse through export. |
| ordering | Search is prerequisite to reliable export; reminders wait for validated demand. |
| closure | Accepted search/export functionality is deployed to production with release evidence. |
| priority_policy | Customer blockers P0; confirmed outcomes P1; unvalidated convenience P2. Source policy applies. |
| cadence | Two-week iterations |

## Work items

| ID | Name | Outcome | Tier | Priority | Approval | Execution | Conditions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | Search requests | Find requests by reference | Now | P1 | Approved | In progress | Validate search acceptance with pilot users |
| R2 | Export search results | Reuse authorized results | Next | P1 | Approved | Not started | Accepted search contract available |
| R3 | Reminders | Reduce missed follow-ups | Later | P2 | Draft | Not started | Re-evaluate after observed missed follow-ups |

## R1

Find requests by reference. Validate search acceptance with pilot users. No closure receipt is supplied.

## R2

Reuse authorized results. Accepted search contract available. No closure receipt is supplied.

## R3

Reduce missed follow-ups. Re-evaluate after observed missed follow-ups. No closure receipt is supplied.

## Versions

| ID | Name | Members | Outcome | Owner | Window |
| --- | --- | --- | --- | --- | --- |
| V1 | Search and export delivery | R1, R2 | Find and reuse requests | Release coordinator | W1–W4 target |

## Iterations

| ID | Name | Goal | Members | Owner |
| --- | --- | --- | --- | --- |
| I1 | Validate search | Validate request lookup | R1 | Product team |
| I2 | Prepare export | Finish search and validate export | R1, R2 | Product team |

## I1

Source planning record for Validate search. Scope and criteria are recorded in the table above.

## I2

Source planning record for Prepare export. Scope and criteria are recorded in the table above.

## Milestones

| ID | Name | Related | Owner | Criterion | Category | State | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MS1 | Release accepted batch | V1 | Acceptance owner | Acceptance and production deployment receipts recorded | approval | planned | None |

## MS1

Source planning record for Release accepted batch. Scope and criteria are recorded in the table above.

## Timing

| ID | Kind | Basis | Start | End | Depends on |
| --- | --- | --- | --- | --- | --- |
| V1 | span | target | 1 | 5 | None |
| I1 | span | target | 1 | 3 | None |
| I2 | span | target | 3 | 5 | None |
| MS1 | milestone | target | 5 | 5 | V1 |

Whole-week spans have exclusive ends. Event points are zero-duration. No actual
event occurrence, acceptance or release is inferred from these planned endpoints.

## Execution board

This fictional source board retains task detail outside roadmap requirement rows.
Current requirement execution is recorded above; no task count proves closure.

| Parent | Next execution detail |
| --- | --- |
| R1 | Validate search acceptance with pilot users |
| R2 | Accepted search contract available |
| R3 | Re-evaluate after observed missed follow-ups |

[Selection decision](selection.md#decision) · [Main roadmap](roadmap.md).
