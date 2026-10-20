# Service Desk placement decisions

Finished W0 placement output, consumed by the [initial roadmap](initial/roadmap.md).
The [priority decisions](priority-decisions.md) and [dependency register](dependencies.md)
are the basis. The fictional product owner confirms every proposed tier below.

## Confirmed placement

| ID | Priority | Readiness | Previous tier | Confirmed tier | Reason |
| --- | --- | --- | --- | --- | --- |
| BUG1 | P0 | Approved; no unmet prerequisite | Backlog | Now | Customer data-integrity blocker; repair already underway |
| R1 | P1 | BUG1 acceptance pending | Backlog | Next | Preserve priority while waiting for retry contract |
| R2 | P1 | R1 acceptance pending | Backlog | Next | Accepted search/permission contract is unavailable |
| R3 | P2 | Draft; demand unvalidated | Backlog | Later | Explicit deferral until demand and approved scope exist |

Promoted from backlog: 4. Compared in priority order across the single project goal.
No priority, approval, execution, version membership or timing is changed by this
placement decision. Existing execution of BUG1 comes from its source, not from
entering Now. No capacity quota or effort gate is invented.

## W1 and end-of-W5 boundaries

The W1 [scope/time adjustment](change-record.md) changes versions, not tiers.
All four tier values remain identical across the retained snapshots. At the end of
W5, R2's prerequisite is satisfied, but starting it still requires a separate
placement/execution decision; the archive does not automatically promote it.
