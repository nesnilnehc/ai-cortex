---
name: archive-milestone
description: Archive completed roadmap work packages or phase/version/period snapshots while preserving milestone event evidence and unfinished work.
version: 1.5.0
license: MIT
---

# Archive Roadmap History

## Purpose and boundaries

Produce a lean, source-backed snapshot and fold historical roadmap detail. The
historical invocation name remains `archive-milestone`. Under the
[Roadmap Spec](../../specs/roadmap-modeling.md), a milestone is an event, a phase is
a work span and a version groups delivery scope. Archiving history does not change
those meanings or establish completion.

Use the general snapshot route for a phase, version, year/period or a milestone's
associated work. Use the legacy route only for an existing
`milestones/{slug}/tasks.md` work package. Do not invent or migrate directories.
Both routes load [roadmap-quality](../../rules/roadmap-quality.md) and project norms.
Preserve event identity, criterion, state, timing and evidence. An approval/release
point is not a task group to delete; task completion is not acceptance or release.

## Inputs

- Named phase, version, period or legacy work-package slug.
- Existing source records, closure evidence, project archive location and policy.
- `apply`, default `false`: preview without writes. Respect explicit existing user
  authorization to apply; do not ask for the same authorization again.

## General snapshot route

1. Resolve target, selected roadmap views and project archive policy. Report an
   undefined eligibility policy rather than inventing numeric thresholds. An
   explicit request to archive a named period can establish selection/eligibility,
   but cannot establish completion of unfinished work.
2. Read authoritative scope, acceptance and release evidence. Preserve separate
   approval and execution states. A reached, missed or cancelled event needs its
   evidence; do not infer occurrence from dates or completed tasks.
3. Draft a dated snapshot: scope, planned versus actual timing, outcomes (at most
   five key deliverables), linked evidence, decisions/ADRs, retained events and
   unresolved work with continuing destinations. Freeze snapshot facts; ongoing
   records remain authoritative. Do not mark unfinished year-end work completed.
4. Preview exact file changes, roadmap folding, incoming links and carryover.
   With `apply=false`, change no files. With authorized `apply=true`, create the
   snapshot and update active-view references while preserving source evidence.
   No directory removal occurs on this route.
5. Verify snapshot/source agreement, incoming/outgoing links and visibility of all
   unfinished work. Report changes and unverified evidence.

## Legacy work-package route

This compatibility route preserves the established maturity and cleanup behavior;
its `milestones/` name does not define the domain model.

1. Read `milestones/{slug}/tasks.md`. Every task must be done (the project's
   `status=done` or completed-checkmark convention). In addition, at least one
   maturity condition must hold:
   - At least 60 days since the source `completed_at` date.
   - The current in-progress **legacy work-package** numeric index is at least
     the target slug's index plus two.
   If neither holds, report the specific reason and stop without changes. These
   thresholds do not apply to independent events or the general snapshot route.
2. Check source closure criteria and acceptance/release evidence before folding
   anything as completed. All tasks done is only an archive prerequisite. If closure
   evidence is missing, leave the completion claim unresolved and report the gap.
3. Produce `milestones/_archive/{slug}-summary.md` containing completion date,
   at most five deliverables, evidence, decisions/ADRs, event history and gaps with
   continuing destinations. Retain key source facts needed after task cleanup.
4. Find every incoming task-path reference and the historical roadmap section.
   Preview the summary, a folded reference of at most three lines, each reference
   update and exact directory cleanup. `apply=false` changes nothing.
5. Before authorized `apply=true`, require a clean Git worktree under the legacy
   contract. Do not commit unrelated work to satisfy this check. Preserve required
   evidence outside the directory before cleanup; an incomplete summary or dangling
   reference blocks removal. Update references before removing the stale directory.
6. Verify the summary exists, roadmap folding agrees, old task-path references
   are gone, the selected stale directory is removed, and event evidence plus
   unfinished-item destinations still resolve.

## Anti-patterns

- Treating a milestone event as a phase or a release group.
- Applying legacy maturity thresholds or directory deletion to every event.
- Inferring production release or approval from completed tasks or a target date.
- Removing source evidence with stale task files.
- Dropping deferred work or retaining a false completion claim in an archive.
- Writing files during preview or requiring duplicate authorization.

## Self-Check

- [ ] Target and route match the actual project structure; required resources loaded.
- [ ] General eligibility or legacy maturity/task checks pass as applicable.
- [ ] Completion and event states agree with source evidence; unknowns remain explicit.
- [ ] Summary retains scope, timing, deliverables, evidence, ADRs, event history and gaps.
- [ ] Every unfinished item has a visible continuing destination.
- [ ] Preview/apply scope and the legacy clean-worktree requirement are respected.
- [ ] Applied changes preserve links/evidence and satisfy the selected route's cleanup checks.

## Examples

- `/archive-milestone m3`: preview an existing legacy work package. If all tasks
  are done and it completed 60 days ago, maturity passes even if only m4 is active.
- A legacy m5 completed 14 days ago with m5 active fails maturity; retry after
  60 days or when m7 is active. Do not create a snapshot or change the roadmap.
- Archive V1 after search moves to V2: retain V1's actual scope and continuing
  assignments, including its acceptance/release events. See the
  [filled version archive](../define-roadmap/references/service-desk/version-archive.md).
