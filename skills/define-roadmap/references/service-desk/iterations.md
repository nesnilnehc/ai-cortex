# Service Desk iteration decisions

Fictional teaching facts for the adjusted plan. This is the editable iteration
source; generated main/detail views are projections. The existing
[change decision](change-record.md#w1-plan-change) retains version/deadline impact.
These iteration allocations add no release claim or tier movement. Their adoption
is recorded as REV3; illustrative record dates do not map W1 to real calendar dates.

## Cadence and allocation

Two-week iterations. W1 starts at the illustrative project origin; end is exclusive.
Only the near-term horizon is allocated; R2 export and R3 reminders remain outside
these iterations, with their existing version/readiness decisions preserved.

| ID | Name | Goal | Members | Start | End | Basis | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| I1 | Repair foundation | Diagnose and validate the duplicate-submission repair | BUG1 | 1 | 3 | target | Desk team |
| I2 | Repair closure and search start | Close the repair and start search validation | BUG1, R1 | 3 | 5 | target | Desk team |
| I3 | Search closure | Complete search acceptance and release checks | R1 | 5 | 7 | target | Desk team |

## I1

BUG1 contributes to the repair goal. The timebox end is a planning boundary, not
acceptance evidence. Execution task detail remains on the [repair source](sources.md#bug1).

## I2

BUG1 continues from I1 while R1 begins. V1 spans I1/I2; I2 touches V1 and V2.
This does not assign BUG1 to two versions or move R1 from Next into Now.
Execution detail stays in [BUG1](sources.md#bug1) and [R1](sources.md#r1).

## I3

R1 continues from I2. V2 spans I2/I3. Its M2/M3 acceptance and release observations
remain separate events with their original criteria and evidence requirements.
No actual iteration result is supplied in this planning snapshot.

## Adoption decision

| ID | Date | Change | Reason | Impact |
| --- | --- | --- | --- | --- |
| REV3 | 2026-10-21 | No iteration allocation → I1–I3 goal/scope/timeboxes | Team plans in two-week cycles | Version windows, tiers and event targets unchanged; R2/R3 remain unallocated |

Earlier decisions remain in the [full revision register](change-record.md#revision-register).
The main roadmap renders REV3 plus the unchanged REV1; no older decisions are dropped.
