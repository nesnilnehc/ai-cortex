---
name: define-roadmap
description: Create a source-backed roadmap with user-selected requirement, version and schedule views, using an offline Markdown, SVG and dated Mermaid generator when useful.
version: 7.3.1
license: MIT
---

# Skill: Define Roadmap

## Purpose and scope

Turn project goals and existing requirements and defects into a readable plan.
Every requirement-view row is a requirement or defect. Now / Next / Later express arrangement,
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
Now/Next/Later view, optional version and schedule views, ordering rationale,
material boundaries and links to detail. Load [roadmap modeling](../../specs/roadmap-modeling.md)
for view structure and generator input; the quality rule owns evaluation criteria.

## Procedure

1. Read project norms and existing decisions, protecting concurrent edits. At first
   creation recommend requirement, version and schedule views and let the user choose.
   Confirm the new destination (repository path, local folder or knowledge-base document);
   an already explicit user destination counts as confirmation. Preserve existing view
   and destination choices during maintenance. Load
   [roadmap-quality](../../rules/roadmap-quality.md), the
   [template](assets/roadmap-template.md) and the
   [completed example](references/roadmap-example.md).
2. Inventory requirements and defects with IDs, source paths, outcomes, priorities,
   approval states, execution evidence, project closure criteria and dependencies. Extract from existing sources before asking.
   If an input is only a task or task group, resolve its parent requirement or defect.
   Merge references to the same parent into one row. An independent defect may have
   its own row linked to the affected requirement. Never invent a parent or approval;
   report missing registration and hand off to `capture-work-items`.
3. Preserve established priorities, pauses and capacity decisions. Arrange eligible
   records using priority, readiness and existing user decisions. State blockers
   separately from priority; missing prerequisites do not make a P0 item low priority.
4. Fill the template with concise outcome rows. Keep approval, execution status and
   key conditions in separate columns. Map source evidence to exactly one execution
   label from the quality rule; report unresolved mappings outside the status cell
   without guessing. State or link the existing project closure criterion.
   Development completion, acceptance and production release remain distinct.
   Do not add or waive a project gate.
   Fill conditions only with the next material condition and its source link.
   For Now, expose completion conditions;
   for Next, material start conditions; for Later, re-evaluation triggers. Link to
   source acceptance criteria rather than reproducing them. Empty tiers are valid.
5. Explain the evolution direction in one sentence and the ordering in a short paragraph.
   Include only boundaries affecting planning. Link exhaustive inventories, task lists
   and evidence. Add metrics or hypotheses only when they affect a real decision;
   do not fill sections or invent numbers to satisfy a template.
6. For selected version views, group source IDs by the existing delivery decision;
   retain unassigned work and unknown owners/windows visibly. For selected schedules,
   gather known spans, milestones, timing basis and dependencies; use relative weeks
   when the start date is unknown. Do not invent dates, auto-schedule resources or
   use a group status as evidence of member acceptance. See [generation](#local-generation-and-delivery).
   Review against the quality rule. Summarize current priorities, subsequent work and
   key blockers from the main view alone. If that requires task lists or evidence
   reports, revise the main view; remove detail that does not change those answers.
7. Apply the user's authorized scope. Ask only about unresolved product tradeoffs or
   missing facts that prevent a sound plan; do not repeat an existing authorization.
   Persist the dated roadmap and report changes and evidence limitations.

## Boundaries

- Only requirements and defects are requirement entries; version groups reference them, phases scope their work, and
  independent milestones relate to entries, versions or phases (or are global). Task IDs and task groups are not requirement entries.
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
- [ ] Approval and execution columns are separate; every execution cell has one fixed label.
- [ ] Key conditions are brief and linked; closure criteria and source-backed status mappings were checked.
- [ ] Detailed progress and evidence remain in their source documents.
- [ ] The quality rule passes; unverified facts and missing sources are reported.
- [ ] The requested change is persisted with its update date and authorization scope respected.
- [ ] Selected views and destination are grounded in user choice; all selected views agree.
- [ ] Tool validation, SVG inspection and destination receipts or limitations are reported.

## Local generation and delivery

Use `python3 <skill-dir>/scripts/render-roadmap.py INPUT.json --check` to validate
temporary facts under the Spec, then pass `--output-dir DIR` for the selected local
destination. Use `--overwrite` only for confirmed replacement of reserved generated
filenames. Never overwrite authoritative evidence or treat the temporary JSON as
a second project plan. The generator emits Markdown and, when selected, SVG and
dated Mermaid; inspect the SVG in a local browser or image-capable viewer. If Python
is unavailable, prepare the same views manually and state that tool validation did
not run. No runtime dependency installation is permitted.

Read the [generator example](references/service-desk/initial/input.json). Preserve the user's
source links relative to the chosen output path; the generator does not relocate
project records. Copying a roadmap to a new directory requires rebasing relative links.

For a knowledge-base destination, discover available document read/write and image
upload tools, map them to the selected operation, read the latest target before
editing and preserve unrelated content. Verify Mermaid support with a small preview
before relying on it. If native rendering is unavailable, use supported image upload
and retain source access. If upload/write is unavailable, report undelivered views
and the local output location; do not silently switch destination or claim publication.
External writes require the user's explicit destination/publication authorization.
This capability performs one delivery, never continuous or bidirectional sync.

## Filled deliverable example

[Complete Service Desk deliverables](references/service-desk/README.md). This is a fictional completed output, not a template
or authorization to change the adopting project.

## Phase and milestone contract

Resolve roadmap concepts from the [Roadmap Spec](../../specs/roadmap-modeling.md).
A version groups deliverables; a phase spans work; a milestone marks an event.
Collect phase scope, owner and exit condition, and milestone category, related IDs,
owner, occurrence criterion, state and evidence when these views are useful.
Do not insert events as fake requirements. Use JSON 1.1 for independent records;
retain 1.0 and single-view compatibility. Give version spans and approval/release
points separate IDs. Missing event dates remain unknown, never inferred.

Self-check: concepts, selected views and linked evidence agree with the source records.
