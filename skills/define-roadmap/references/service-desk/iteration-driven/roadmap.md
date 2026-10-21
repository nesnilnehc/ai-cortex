# Service Desk Roadmap

Updated: 2026-10-21

## Overview

Direction: Make request handling dependable, then reduce repeated work.

Current arrangement: Fix duplicate submission before search; export depends on accepted search. Reminders wait for demand.

## Priority arrangement

| Tier | Requirement / defect | Expected outcome | Priority | Approval status | Execution status | Key conditions |
| --- | --- | --- | --- | --- | --- | --- |
| Now | [BUG1 · Duplicate submission](../sources.md#bug1) | Refresh and retry create one external request | P0 | Approved | Blocked | [Restore sandbox by W3; local fixture cannot waive acceptance](../sources.md#bug1) |
| Next | [R1 · Search](../sources.md#r1) | Find a request by reference | P1 | Approved | Not started | [Wait for accepted retry behavior](../sources.md#r1) |
| Next | [R2 · Export](../sources.md#r2) | Export authorized search results | P1 | Approved | Not started | [Wait for accepted search contract](../sources.md#r2) |
| Later | [R3 · Reminders](../sources.md#r3) | Remember requests needing follow-up | P2 | Draft | Not started | [Re-evaluate after three users demonstrate missed follow-ups](../sources.md#r3) |

## Delivery plan

### Iterations

Cadence: Two-week iterations

| Iteration | Goal | Timebox / basis | Members | Versions touched | Owner | Source | Execution detail |
| --- | --- | --- | --- | --- | --- | --- | --- |
| I1 · Repair foundation | Diagnose and validate the duplicate-submission repair | target · W1–W2 | BUG1 | V1 | Desk team | [Source](../iterations.md#i1) | [Board](../sources.md#bug1) |
| I2 · Repair closure and search start | Close the repair and start search validation | target · W3–W4 | BUG1, R1 | V1, V2 | Desk team | [Source](../iterations.md#i2) | [Board](../sources.md#r1) |
| I3 · Search closure | Complete search acceptance and release checks | target · W5–W6 | R1 | V2 | Desk team | [Source](../iterations.md#i3) | [Board](../sources.md#r1) |

Not allocated to an iteration: R2, R3.

Iteration boundaries do not prove completion, reach milestones or authorize release.

### Versions

| Version | Members | Core outcome | Owner | Delivery window |
| --- | --- | --- | --- | --- |
| V1 · Dependable submission | BUG1 | Refresh and retry create one external request | Delivery owner | W1–W3 (target) |
| V2 · Search delivery | R1 | Find a request by reference | Delivery owner | W4–W5 (target) |
| V3 · Export delivery | R2 | Export authorized search results | Delivery owner | W6–W7 (committed) |

Unassigned: R3.

### Phases

| Phase | Scope | Owner | Exit condition | Source |
| --- | --- | --- | --- | --- |
| PSEARCH · Search delivery phase | R1 | Search owner | Search accepted and released | [PSEARCH](../sources.md#psearch) |

### Milestones

| Milestone | Category | Related | Owner | State | Occurrence criterion | Source | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M0 · Project kickoff | start | Global | Product owner | reached | Product owner starts the project | [Source](../sources.md#m0) | [Evidence](../sources.md#m0) |
| M1 · Repair acceptance | approval | BUG1 | Reviewer | planned | Reviewer approves BUG1 acceptance | [Source](../sources.md#m1) | — |
| M2 · Search acceptance | approval | R1, PSEARCH | Reviewer | planned | Reviewer approves R1 acceptance | [Source](../sources.md#m2) | — |
| M3 · Search production release | achievement | R1, V2 | Release owner | planned | Production deployment evidence for R1 recorded | [Source](../sources.md#m3) | — |

Milestones are events; dates and related work do not prove occurrence or grant approval.

## Timeline

W1 begins at project start; calendar start unknown. W1 revised planning snapshot.

Elapsed calendar days / whole weeks; spans have exclusive ends.

![Roadmap schedule](roadmap.svg)

<details>
<summary>Timing details</summary>

| Reference | Kind | Timing basis | Window | Depends on |
| --- | --- | --- | --- | --- |
| V1 | span | target | W1–W3 | None |
| V2 | span | target | W4–W5 | V1 |
| V3 | span | committed | W6–W7 | V2 |
| R3 | span | target | Unscheduled | None |
| PSEARCH | span | target | W4–W5 | M1 |
| M0 | milestone | actual | W1 | None |
| M1 | milestone | target | W4 | None |
| M2 | milestone | target | W6 | PSEARCH |
| M3 | milestone | target | W6 | M2 |
| I1 | span | target | W1–W2 | None |
| I2 | span | target | W3–W4 | None |
| I3 | span | target | W5–W6 | None |

</details>

Unscheduled: R3.

## Revision history

| Date / revision | Change | Reason | Impact | Details |
| --- | --- | --- | --- | --- |
| 2026-10-21 · REV3 | No iteration allocation → I1–I3 goal/scope/timeboxes | Team plans in two-week cycles | Version windows, tiers and event targets unchanged; R2/R3 remain unallocated | [Details](../iterations.md#adoption-decision) |
| 2026-10-20 · REV1 | R1: V1 → V2; R2: V2 → V3; M1: W2 → W4; M2/M3: W3 → W6 | Required repair acceptance sandbox unavailable; search and export depend on accepted upstream work | Export +3 weeks; original hard deadline breached; priorities and tiers unchanged | [Details](../change-record.md#w1-plan-change) |

[Full revision history](../change-record.md#revision-register).

## Planning basis and sources

[Priority policy](../priority-policy.md)

Closure criterion: Acceptance passed and accepted change released to production; see ../sources.md#project-policy.

Backlog requirements and defects map to this roadmap; items outside it are not done by default.
Placement grants no implementation or release approval.
