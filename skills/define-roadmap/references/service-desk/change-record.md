# Service Desk scope and timing change

Finished W1 change output. Compare the [initial](initial/roadmap.md) and
[adjusted](adjusted/roadmap.md) snapshots, with the [source event](sources.md#bug1).
This is a fictional approved planning decision, not a silent date recalculation.

## Changed items

| Reference | Before | After | Reason |
| --- | --- | --- | --- |
| BUG1 execution | In progress | Blocked | Required acceptance sandbox unavailable |
| V1 scope / target | BUG1, R1 · W1–W2 | BUG1 · W1–W3 | Repair acceptance must precede search |
| R1 membership | V1 | V2 | Move search behind restored acceptance |
| V2 scope / target | R2 · W3–W4 | R1 · W4–W5 | Reserve the next delivery for accepted search |
| R2 membership | V2 | V3 | Export waits for the accepted search contract |
| V3 commitment | No version | R2 · W6–W7 | Explicitly accepted new export delivery |

Scope moves: R1: V1 → V2; R2: V2 → V3. Priorities, approvals and Now/Next/Later
tiers are unchanged. The change affects both source/version assignments and the
schedule; all selected views are refreshed at the same chosen destination.

## Blocker, owner and mitigation

Blocker: the external acceptance sandbox is unavailable. Owner: platform owner.
Resolve by W3; resume when the sandbox is restored. A local fixture supports
diagnosis but does not replace external acceptance. The accepted repair must still
be released before its source can claim closure.

## Downstream impact and hard deadline

V1's end moves from boundary W3 to W4, a one-week delay. R1 moves to the W4–W5
delivery window. R2's delivery moves from W3–W4 to W6–W7: **3 weeks later**.
Its original hard deadline is end of W4, boundary W5; the new boundary W8 breaches it.
The fictional product owner explicitly accepts the end-of-W7 replacement commitment
and informs the affected adopter in this scenario. The original missed deadline
remains visible; the new date does not erase it. No real message is sent by this example.

## Ownership and execution result

`define-roadmap` first establishes new version V3 under the owner's scope decision.
`update-roadmap` applies existing-version membership, status and date changes and
checks downstream impacts. `promote-roadmap-items` is not needed because no tier moves.
The review's earlier incorrect status/date claims have already been corrected in
the W0 candidate; this W1 change records new source facts rather than rewriting W0.

Result: [adjusted roadmap](adjusted/roadmap.md), [adjusted Gantt chart](adjusted/roadmap.svg).
R3 remains unassigned and unscheduled. Next check: sandbox restoration and BUG1
acceptance; no automatic Completed transition or publication authorization is granted.

## Phase and event interpretation

PSEARCH shifts from W2–W2 to W4–W5. M1 target moves W2 → W4; M2 and M3 move W3 → W6. M3 relates to V1 → V2 with R1. Kickoff M0 is confirmed at W1 during the adjusted review. After delivery M1/M2/M3 have actual occurrence evidence; moving targets alone did not change their states.
