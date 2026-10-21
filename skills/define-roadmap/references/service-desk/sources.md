# Service Desk source records

All people, approvals, events and evidence below are fictional teaching facts.
These records define the scenario; generated snapshots reference them. No task
counts, commits or illustrated bars are treated as acceptance evidence.

## Project policy

Goal: make request handling dependable, then reduce repeated work.
Priority rules have one authority: [Requirement Priority Policy](priority-policy.md).
This section retains its stable anchor for older snapshot references.
The product owner approves this policy and the initial placement at W0.
Closure requires the item's acceptance criteria to pass and its accepted change
to be released to production. Version membership grants neither approval.
The selected destination is this local example bundle; all three views are selected.
Elapsed whole weeks are used, with exclusive ends. No real launch date is known.

## Work items

| ID | Name | Priority | Depends on |
| --- | --- | --- | --- |
| BUG1 | Duplicate submission | P0 | None |
| R1 | Search | P1 | BUG1 |
| R2 | Export | P1 | R1 |
| R3 | Reminders | P2 | None |

## Execution by stage

| ID | Initial | Adjusted | After delivery |
| --- | --- | --- | --- |
| BUG1 | In progress | Blocked | Completed |
| R1 | Not started | Not started | Completed |
| R2 | Not started | Not started | Not started |
| R3 | Not started | Not started | Not started |

## Delivery windows

The initial snapshot is W0 planning, adjusted is W1 planning, and after-delivery
is the end-of-W5 observation. A future target or commitment is not an actual result.

| Stage | Version | Members | Start | End | Basis |
| --- | --- | --- | --- | --- | --- |
| initial | V1 | BUG1, R1 | 1 | 3 | target |
| initial | V2 | R2 | 3 | 5 | target |
| adjusted | V1 | BUG1 | 1 | 4 | target |
| adjusted | V2 | R1 | 4 | 6 | target |
| adjusted | V3 | R2 | 6 | 8 | committed |
| after-delivery | V1 | BUG1 | 1 | 4 | actual |
| after-delivery | V2 | R1 | 4 | 6 | actual |
| after-delivery | V3 | R2 | 6 | 8 | committed |

## BUG1

Outcome: refresh and retry create exactly one external request. Approval: Approved.
Acceptance: replay the same submission after refresh and timeout; verify exactly
one external request and a recoverable user-visible result.
At W0, repair is underway; acceptance and release are pending.
At W1, the required acceptance sandbox is unavailable. Execution cannot advance,
so status is Blocked. Platform owner restores it by W3; a local fixture supports
diagnosis but cannot replace required external acceptance. Resume when the sandbox
is restored. At W3, the product owner records acceptance passed for both replay
paths, and the release operator records the accepted repair deployed in V1.
These two fictional receipts establish closure; development alone does not.

## R1

Outcome: users find an existing request by its reference. Approval: Approved.
Prerequisite: BUG1's retry behavior passes acceptance, so search fixtures are stable.
Acceptance: a known reference returns the correct request; an unknown reference
shows an explicit empty result; unauthorized requests are not exposed.
At W0 and W1, work has not started. Search moves from V1 to V2 in the W1 decision.
At W5, the product owner records all three acceptance cases passed, and the release
operator records the accepted feature deployed in V2. R1 is then Completed.

## R2

Outcome: users export authorized search results with matching rows and columns.
Approval: Approved. Prerequisite: R1's accepted result/permission contract.
Acceptance: exported rows match visible authorized results; unauthorized rows are
absent; an empty result yields an explicit empty export.
Work has not started in any retained snapshot. The original hard deadline is the
end of W4 (boundary W5). At W1 the product owner accepts a new end-of-W7 commitment
(boundary W8), preserving the original breach record. Export moves from V2 to V3;
its priority and Next tier do not change. No acceptance or release receipt exists.

## R3

Outcome: users remember requests needing follow-up. Approval: Draft.
No dependency is identified after checking the five dependency categories.
Work has not started and no version or date is committed. Re-evaluate when three
users demonstrate missed follow-ups; scope and acceptance must then be approved.
Absence of a prerequisite does not make this draft convenience request ready.

## PSEARCH

The search delivery phase spans search work through acceptance and production
release. Scope: R1. Owner: Search owner. Exit: search accepted and released.
The phase is not an event and may move between delivery versions with its scope.

## M0

Project kickoff occurs when the product owner starts the project. It is global.
Initial plan: W1 target. At the adjusted review the owner confirms kickoff at W1;
that confirmation remains evidence in the after-delivery snapshot.

## M1

Repair acceptance occurs when the reviewer approves BUG1 acceptance. Initial target
W2; adjusted target W4; after delivery the reviewer confirms acceptance at W4.

## M2

Search acceptance occurs when the reviewer approves R1 acceptance and PSEARCH exit
work is ready for release. Initial target W3; adjusted target W6; after delivery
the reviewer confirms acceptance at W6. The phase boundary is represented at W6.

## M3

Search production release occurs when production deployment evidence for R1 is
recorded. Initial target W3 related to V1; adjusted target W6 related to V2;
after delivery deployment evidence confirms occurrence at W6. It follows M2.

## Phase windows

| Stage | ID | Scope | Start | End | Basis |
| --- | --- | --- | --- | --- | --- |
| initial | PSEARCH | R1 | 2 | 3 | target |
| adjusted | PSEARCH | R1 | 4 | 6 | target |
| after-delivery | PSEARCH | R1 | 4 | 6 | actual |

## Event observations

| Stage | ID | Related | Week | Basis | State | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| initial | M0 | Global | 1 | target | planned | None |
| initial | M1 | BUG1 | 2 | target | planned | None |
| initial | M2 | R1, PSEARCH | 3 | target | planned | None |
| initial | M3 | R1, V1 | 3 | target | planned | None |
| adjusted | M0 | Global | 1 | actual | reached | ../sources.md#m0 |
| adjusted | M1 | BUG1 | 4 | target | planned | None |
| adjusted | M2 | R1, PSEARCH | 6 | target | planned | None |
| adjusted | M3 | R1, V2 | 6 | target | planned | None |
| after-delivery | M0 | Global | 1 | actual | reached | ../sources.md#m0 |
| after-delivery | M1 | BUG1 | 4 | actual | reached | ../sources.md#m1 |
| after-delivery | M2 | R1, PSEARCH | 6 | actual | reached | ../sources.md#m2 |
| after-delivery | M3 | R1, V2 | 6 | actual | reached | ../sources.md#m3 |

Week numbers on event points identify boundaries: W6 is the boundary after the complete W5 interval. The after-delivery observation at the end of W5 includes that boundary, rather than asserting an event later in W6.

## Delivery observation

REV2 records the source receipts already described under BUG1 and R1 and the
actual milestones M1/M2/M3. The product owner confirms acceptance and the release
operator confirms production deployment at the recorded observation boundaries.
The outcome changes the source execution summaries to Completed and event states
to reached; V1/V2 timing is now actual. R2 remains unstarted in V3. The prior REV1
scope and deadline decision remains unchanged, linked from the revision register.
