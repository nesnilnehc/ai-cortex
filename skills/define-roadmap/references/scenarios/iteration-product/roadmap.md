# Request Search Product Roadmap

Updated: 2026-10-21

## Overview

Make requests findable before adding reuse through export.

Ordering rationale: Search is prerequisite to reliable export; reminders wait for validated demand.

Priority policy: Customer blockers P0; confirmed outcomes P1; unvalidated convenience P2. Source policy applies.

Closure criterion: Accepted search/export functionality is deployed to production with release evidence.

## Planning approach

Scenario: iterations · Primary: iterations · Layout: split

Enabled views: requirements, iterations, versions, milestones, schedule.

Use two-week iteration goals, named delivery batches and release events; omit phases because no distinct stage boundary exists. [Selection source](selection.md#decision).

## Priority arrangement

| Tier | Requirement / defect | Expected outcome | Priority | Approval status | Execution status | Key conditions |
| --- | --- | --- | --- | --- | --- | --- |
| Now | [R1 · Search requests](sources.md#r1) | Find requests by reference | P1 | Approved | In progress | [Validate search acceptance with pilot users](sources.md#r1) |
| Next | [R2 · Export search results](sources.md#r2) | Reuse authorized results | P1 | Approved | Not started | [Accepted search contract available](sources.md#r2) |
| Later | [R3 · Reminders](sources.md#r3) | Reduce missed follow-ups | P2 | Draft | Not started | [Re-evaluate after observed missed follow-ups](sources.md#r3) |

## Delivery outlook

Cadence: Two-week iterations

| Iteration / goal | Timebox / basis |
| --- | --- |
| I1 · Validate request lookup | target · W1–W2 |
| I2 · Finish search and validate export | target · W3–W4 |

| Version / outcome | Members | Delivery window |
| --- | --- | --- |
| V1 · Find and reuse requests | R1, R2 | W1–W4 target |

| Key event | State | Timing / basis |
| --- | --- | --- |
| MS1 · Release accepted batch | planned | target · W5 |

[Delivery details and timeline](roadmap-delivery.md).

## Revision history

No material revisions recorded; earlier history is not certified by this input.

Backlog requirements and defects map to this roadmap; items outside it are not done by default.
Placement grants no implementation or release approval.
