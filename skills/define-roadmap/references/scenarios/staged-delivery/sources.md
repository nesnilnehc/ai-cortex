# Customer Data Onboarding source facts

Fictional completed planning example, adopted 2026-10-21. These are teaching facts,
not universal defaults or real commitments. Planned work is not claimed completed.

## Context

| Field | Value |
| --- | --- |
| work_mode | staged |
| delivery | acceptance |
| audience | Implementation team, customer acceptance owner and steering group |
| constraints | Customer pilot acceptance is committed at W5; scope changes require impact review |

## Planning basis

| Field | Value |
| --- | --- |
| project | Customer Data Onboarding |
| updated | 2026-10-21 |
| direction | Establish correct mappings before pilot acceptance and broader rollout. |
| ordering | Accepted mappings enable the pilot; broader rollout waits for pilot evidence. |
| closure | Customer signs acceptance of the agreed deliverable. |
| priority_policy | Customer blockers P0; confirmed outcomes P1; unvalidated convenience P2. Source policy applies. |

## Work items

| ID | Name | Outcome | Tier | Priority | Approval | Execution | Conditions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | Map source data | Map customer records correctly | Now | P1 | Approved | In progress | Customer validates representative records |
| R2 | Pilot onboarding | Prove the onboarding path | Next | P1 | Approved | Not started | Mapping acceptance available |
| R3 | Broader rollout | Extend onboarding beyond pilot | Later | P2 | Draft | Not started | Re-evaluate after pilot acceptance |

## R1

Map customer records correctly. Customer validates representative records. No closure receipt is supplied.

## R2

Prove the onboarding path. Mapping acceptance available. No closure receipt is supplied.

## R3

Extend onboarding beyond pilot. Re-evaluate after pilot acceptance. No closure receipt is supplied.

## Phases

| ID | Name | Scope | Owner | Exit condition |
| --- | --- | --- | --- | --- |
| PH1 | Mapping foundation | R1 | Project lead | Customer approves representative mapped records |
| PH2 | Customer pilot | R2 | Project lead | Customer signs pilot acceptance |

## PH1

Source planning record for Mapping foundation. Scope and criteria are recorded in the table above.

## PH2

Source planning record for Customer pilot. Scope and criteria are recorded in the table above.

## Milestones

| ID | Name | Related | Owner | Criterion | Category | State | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MS1 | Mapping accepted | R1, PH1 | Acceptance owner | Signed mapping acceptance recorded | approval | planned | None |
| MS2 | Pilot accepted | R2, PH2 | Acceptance owner | Customer signs pilot acceptance | approval | planned | None |

## MS1

Source planning record for Mapping accepted. Scope and criteria are recorded in the table above.

## MS2

Source planning record for Pilot accepted. Scope and criteria are recorded in the table above.

## Timing

| ID | Kind | Basis | Start | End | Depends on |
| --- | --- | --- | --- | --- | --- |
| PH1 | span | target | 1 | 3 | None |
| MS1 | milestone | target | 3 | 3 | PH1 |
| PH2 | span | target | 3 | 5 | MS1 |
| MS2 | milestone | committed | 5 | 5 | PH2 |

Whole-week spans have exclusive ends. Event points are zero-duration. No actual
event occurrence, acceptance or release is inferred from these planned endpoints.

## Execution board

This fictional source board retains task detail outside roadmap requirement rows.
Current requirement execution is recorded above; no task count proves closure.

| Parent | Next execution detail |
| --- | --- |
| R1 | Customer validates representative records |
| R2 | Mapping acceptance available |
| R3 | Re-evaluate after pilot acceptance |

[Selection decision](selection.md#decision) · [Main roadmap](roadmap.md).
