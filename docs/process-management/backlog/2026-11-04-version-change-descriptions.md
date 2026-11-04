---
artifact_type: backlog-item
created_by: capture-work-items
lifecycle: living
type: issue
subtype: improvement
date: 2026-11-04
status: captured
priority: unset
strategic_goal_id: goal-1
source: user
---

# Prepare version change descriptions independently

## Need and evidence

Delivery may need a trustworthy description for a chosen component, version and
source. Authoring must remain separate from version edits and delivery execution.
No general active Skill in the current catalogue owns this task: bump-version
excludes descriptions, delivery consumes them, and commit-work commits existing
work. Project-owned capabilities may cover individual projects; catalogue absence
does not establish their absence. Goal mapping is inferred from
[Goal 1](../../project-overview/strategic-goals.md#goal-1-delivery-chain-capabilities-are-available).

## Confirmed boundaries

- Consume target version and delivery scope decided offline or in project records;
  ask only for specific gaps. Do not require a version-planning Skill.
- Reuse existing changelogs, notes or release lists. Do not require a new JSON
  handoff, Release Package or release-note gate for every build.
- Where needed, identify component/target version, comparison purpose, explicit
  baseline and source association, target source, description location and
  identifiable revision/digest, plus unresolved issues.
- For changes since the previous formal delivery, prefer the source commit
  associated with the selected formal-channel artifact. The latest bump commit
  or highest version number is not an automatic substitute. Candidate comparisons
  may use a previous candidate with an explicit purpose.
- Divergence or unknown identities are evidence gaps. Commits within a range do
  not automatically establish requirement membership. Omitting an item from notes
  cannot remove code already included in the package.
- Own description facts, scope and target consistency. Version-reference checks,
  code/build/package checks and reviewed commits retain their separate owners.
  Description and version edits may iterate independently, without automatic
  companion calls or per-Skill commits; a project may commit both together.
- Delivery consumes required descriptions and checks target association; it does
  not author descriptions or repair upstream inputs to pass its checks.

## Proposal and remaining decision

First inventory the consuming project's existing authoring mechanism. Then choose
between a project-owned authoring entry and a narrow shared Skill. Recommend a
separate authoring capability if a reusable gap remains; implementation and its
public name require an explicit scope decision. Do not restore prepare-release,
reserved IDs, or the Release Package under
[ADR 0017](../../adr/0017-project-owned-releases.md).

The next assessment is estimated at 3 story points: inspect existing mechanisms,
settle the input/output boundary and propose its home. This does not authorize
implementation, priority or roadmap promotion.

## Review criteria for a later proposal

- Formal-channel and candidate baselines keep their distinct purposes; unknown
  or divergent identities remain visible.
- Existing formats remain usable and test builds gain no blanket gate.
- Examples separate source-range facts from requirement membership and expose
  exclusions still present in the actual package.
- Output supports delivery without absorbing versioning, committing or publishing.

Source: maintainer's eight confirmed boundaries, relayed on 2026-11-04.
