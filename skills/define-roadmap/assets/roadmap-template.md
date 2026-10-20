# {Project} Roadmap

Updated: {YYYY-MM-DD}

{One sentence describing the evolution direction and goal served.}

## Roadmap

| Tier | Requirement / defect | Expected outcome | Priority | Approval status | Execution status | Key conditions |
| --- | --- | --- | --- | --- | --- | --- |
| Now | {ID · meaningful name · source link} | {Capability delivered or behavior restored} | {P0–P3} | {Source approval label} | {One fixed execution label} | {Next completion condition · source link} |
| Next | {ID · meaningful name · source link} | {Expected result} | {P0–P3} | {Source approval label} | {One fixed execution label} | {Material start condition · source link} |
| Later | {ID · meaningful name · source link} | {Directional result} | {P0–P3} | {Source approval label} | {One fixed execution label} | {Re-evaluation prerequisite · source link} |

Closure criterion: {Link the existing project definition; distinguish development
completion, acceptance and production release where applicable. Flag undefined closure.}

Use the execution labels and boundaries in
[roadmap-quality](../../../rules/roadmap-quality.md#execution-status-vocabulary).
Approval follows the source contract; use explicit unverified / not applicable when
appropriate. Keep each execution cell to one label and each key condition to one
short next-step condition plus a source link; use `—` when none applies.

## Why this order

{Brief priority and dependency rationale. Explain exceptions without copying scores.}

Priority policy: {Link the project's policy; distinguish unresolved priority from low priority.}

## Versions

<!-- Include only if selected. References are the same requirement/defect IDs. -->

| Planning version | Member IDs | Core outcome | Owner | Target window |
| --- | --- | --- | --- | --- |
| {Version ID · name} | {Source IDs} | {Delivery result} | {Owner or Unknown} | {Window or Unknown} |

Unassigned: {IDs not yet assigned, or None. Do not imply all work is committed.}

## Phases

<!-- Optional: retain when phase records exist. A phase is work over time. -->

| Phase | Scope IDs | Owner | Exit condition | Source |
| --- | --- | --- | --- | --- |
| {ID · name} | {Entry/version IDs} | {Owner} | {Completion condition} | {Source link} |

## Milestones

<!-- Optional: events, not task groups. Unknown dates remain unscheduled. -->

| Milestone | Category | Related IDs | Owner | State | Occurrence criterion | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| {ID · name · source} | {start/approval/achievement/deadline/event} | {Entry/version/phase IDs or Global} | {Owner} | {planned/reached/missed/cancelled} | {What establishes occurrence} | {Required for non-planned state} |

## Schedule

<!-- Include only if selected. Use the local generator for SVG and dated Mermaid,
or an established project format. Do not invent calendar dates for relative weeks. -->

Origin / calendar: {Real dates or W1 origin; elapsed calendar days or whole weeks.}

| Reference | Kind | Timing basis | Window | Depends on |
| --- | --- | --- | --- | --- |
| {Entry, version, phase or milestone ID} | {span / milestone} | {target / committed / actual} | {Known span or Unscheduled} | {References or None} |

{Embed the verified diagram in the chosen destination. A bar is time, not completion.}

## Current boundaries

{Only pauses, exclusions or approved capacity constraints that affect this plan.
Omit this section when none apply.}

Backlog requirements and defects must map to the roadmap; items outside it are
not done by default. Placement does not grant implementation or release approval.

## Sources

{Links to the project's existing requirement/defect index, task lists and evidence.
Do not create additional documents just to fill this section.}

<!-- Replace placeholders and remove author guidance. Each requirement-view row is a requirement or
 defect, never a task. Multiple rows per tier and empty tiers are valid. Keep detailed
 metrics, hypotheses, task progress and evidence in linked sources when available. -->
