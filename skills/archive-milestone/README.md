# archive-milestone

Archives roadmap history while preserving evidence and unfinished work. The
historical skill name remains compatible; a milestone itself is an event under
the [Roadmap Spec](../../specs/roadmap-modeling.md).

## Routes

| Target | Eligibility | Result |
| --- | --- | --- |
| Phase, version, period or checkpoint-associated work | Project policy or explicitly selected archive period | Dated snapshot, folded active references, continuing-item links; source records retained |
| Existing `milestones/{slug}/tasks.md` work package | All tasks done and either 60 days elapsed or active legacy index at least target + 2 | Legacy summary, reference updates and selected stale-directory cleanup |

Milestone criterion, state, timing and occurrence evidence remain available after
archiving. Dates and completed tasks do not prove acceptance or production release.
No directory migration is required.

## Usage

```text
/archive-milestone m3
/archive-milestone m3 apply=true
```

Default is preview (`apply=false`). Apply uses the authorized scope. Legacy cleanup
also requires a clean worktree and preserved evidence before directory removal.
General snapshots do not remove directories. See the
[full procedure and Self-Check](SKILL.md).

## Finished example

[Version archive with retained events and unfinished-item destinations](../define-roadmap/references/service-desk/version-archive.md).

Material planning changes retain the latest five revision summaries and a durable history link under the [revision contract](../../specs/roadmap-modeling.md#54-revision-records). Regeneration and archive cleanup preserve earlier decisions.

Optional iteration views and one-main-plus-detail layouts follow the
[Roadmap Spec](../../specs/roadmap-modeling.md#reading-order-and-document-boundaries).
Iteration boundaries do not prove acceptance or release; linked/generated summaries
retain one editable source per fact. See the skill for maintenance/review ownership.

Scenario-based intake and retention follow the
[selection contract](../../specs/roadmap-modeling.md#56-context-recommendations-and-retained-selection-schema-14):
read evidence first, ask only material gaps, recommend with reasons and reuse the
settled combination during maintenance. Legacy and custom choices remain valid.
