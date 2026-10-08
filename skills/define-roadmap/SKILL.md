---
name: define-roadmap
description: Create a concise Now/Next/Later roadmap containing only requirements and defects, using a bundled template and source links for task and acceptance details.
version: 6.0.0
license: MIT
---

# Skill: Define Roadmap

## Purpose and scope

Turn project goals and existing requirements and defects into a readable plan.
Every roadmap row is a requirement or defect. Now / Next / Later express arrangement,
not three mandatory strategic dossiers. Tasks, implementation steps, test procedures
and release operations remain in their source documents.

This skill creates or restructures the roadmap. It does not create requirements,
rescore priorities, break down tasks or approve execution. Use `capture-work-items`
for missing requirement or defect records, `promote-roadmap-items` for tier changes,
and `update-roadmap` for status and timing maintenance.

## Inputs and output

Read project norms, goals, the existing roadmap and source requirement and defect
records. Default output is `docs/process-management/roadmap.md`; preserve a project's
established path. The output is a living roadmap with a dated summary, a compact
Now/Next/Later view, ordering rationale, material boundaries and links to detail.

## Procedure

1. Read project norms and existing decisions, protecting concurrent edits. Load
   [roadmap-quality](../../rules/roadmap-quality.md), the
   [template](assets/roadmap-template.md) and the
   [completed example](references/roadmap-example.md).
2. Inventory requirements and defects with IDs, source paths, outcomes, priorities,
   approval states and dependencies. Extract from existing sources before asking.
   If an input is only a task or task group, resolve its parent requirement or defect.
   Merge references to the same parent into one row. An independent defect may have
   its own row linked to the affected requirement. Never invent a parent or approval;
   report missing registration and hand off to `capture-work-items`.
3. Preserve established priorities, pauses and capacity decisions. Arrange eligible
   records using priority, readiness and existing user decisions. State blockers
   separately from priority; missing prerequisites do not make a P0 item low priority.
4. Fill the template with concise outcome rows. For Now, expose completion conditions;
   for Next, material start conditions; for Later, re-evaluation triggers. Link to
   source acceptance criteria rather than reproducing them. Empty tiers are valid.
5. Explain the evolution direction in one sentence and the ordering in a short paragraph.
   Include only boundaries affecting planning. Link exhaustive inventories, task lists
   and evidence. Add metrics or hypotheses only when they affect a real decision;
   do not fill sections or invent numbers to satisfy a template.
6. Review against the quality rule. Summarize current priorities, subsequent work and
   key blockers from the main view alone. If that requires task lists or evidence
   reports, revise the main view; remove detail that does not change those answers.
7. Apply the user's authorized scope. Ask only about unresolved product tradeoffs or
   missing facts that prevent a sound plan; do not repeat an existing authorization.
   Persist the dated roadmap and report changes and evidence limitations.

## Boundaries

- Only requirements and defects are roadmap entries; task IDs and task groups are not.
- Preserve source status and authorization; inclusion is not approval to implement or release.
- Link one source of truth for detailed progress and acceptance.
- State that backlog requirements and defects map to the roadmap and that items outside
  it are not done by default.
- Follow explicit project capacity decisions; introduce no default quotas or item limits.
- Template structure is presentation guidance, not a reason to pad content.

## Self-Check

- [ ] Project norms, goals, source records, quality rule, template and example were read.
- [ ] Every entry is a linked requirement or defect; parent references are consolidated.
- [ ] Priority, approval, pauses, prerequisites and authorized capacity are preserved.
- [ ] Tier precision is appropriate and completion or start conditions are recoverable.
- [ ] The main view explains priorities, subsequent work and blockers without task detail.
- [ ] Detailed progress and evidence remain in their source documents.
- [ ] The quality rule passes; unverified facts and missing sources are reported.
- [ ] The requested change is persisted with its update date and authorization scope respected.
