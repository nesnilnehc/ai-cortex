---
name: review-roadmap
description: Review a concise requirement-and-defect roadmap for entry granularity, priority, readiness, readability, iteration views, document layering, revision history and source traceability; emit findings without rewriting.
version: 3.10.0
license: MIT
output_schema:
  type: findings-list
---

# Skill: Review Roadmap

## Purpose

Evaluate an existing roadmap against [roadmap-quality](../../rules/roadmap-quality.md).
Emit findings under [findings-list](../../specs/findings-list.md); do not rewrite,
change placement or invent additional criteria. Use category `roadmap-quality`.

For first alignment, discover the actual plan/source locations before checking
conventional paths. Classify findings as structural repair, evidence unavailable/
conflicting, or a separately proposed business decision in the findings description
and handoff, using the existing findings schema. A format gap is not evidence of
wrong priority, stalled execution or absent strategy. Preserve known facts and stable
links as the baseline for re-review; missing evidence cannot become a full pass.

## Procedure

1. Load the quality rule and [roadmap modeling](../../specs/roadmap-modeling.md);
   halt if a required resource is missing. Read the roadmap at the project path
   (default `docs/process-management/roadmap.md`) and project norms.
2. Read linked requirement and defect records, goals, acceptance criteria, priorities
   and dependencies. Verify that every requirement-view entry is a requirement or
   defect, not a task or task group. Version groups and schedule milestones are
   valid additional views. Check duplicates against stable parent IDs.
3. Evaluate all five dimensions in the rule: completeness, executability, clarity,
   soundness and traceability. Missing four-part stage dossiers, fixed hypothesis
   sentences or inline metric tables are not defects. Linked evidence is valid.
4. Test readability by summarizing current priorities, subsequent work and key blockers
   from the main view alone. Locate detail that obstructs those answers or duplicates
   source task lists and evidence. Report concrete locations, not a subjective score.
   Check that policy is the reusable rule and arrangement rationale explains its
   application, not another scoring policy. A useful summary plus authority link,
   or a sufficient bare link, is valid. Do not require a separate rationale file,
   precise rank for genuine ties or migration to the Spec's suggested filenames.
   In the revised reading hierarchy, plan/unknowns precede maintenance metadata;
   policy, closure, selection and language evidence remain recoverable later.
5. Verify source agreement, approval boundaries and prerequisite readiness. Check
   separate approval, execution and key conditions columns; one fixed execution
   label per row; short linked next-step conditions; and no evidence in status cells.
   Compare every claimed transition with source records and the declared closure
   criterion. Distinguish development complete, acceptance passed and production
   release; flag undefined closure or unsupported Completed claims. Risk, approval,
   priority and tier are not execution labels. If sources
   are unavailable, mark the affected criteria `cannot evaluate` with the reason;
   never infer a pass. Missing evidence becomes a finding or limitation, not a question.
6. For change frequency, discover the project's window and threshold and inspect git
   history if available. Without a defined window or sufficient history, report that
   frequency cannot be evaluated; do not invent a cycle or threshold.
7. Check selected-view and destination criteria in quality rule §6. Compare version
   membership, requirement scope, timing basis, calendars, dependencies and delivery
   evidence. Do not demand a version or schedule view that the user did not select,
   or treat generation as proof of publication. Mark unavailable source/platform
   checks cannot evaluate. Emit actionable findings, citing the deriving rule section, plus evidence limitations.
   Assign severity under the findings Spec: misleading completion or authorization
   with correctness or safety consequences may be critical; task entries, missing
   source identity, unreadable planning or unexplained ordering are normally major;
   cosmetic omissions are normally minor. Do not invent a local findings schema.

## Output and handoff

A findings list and explicit unchecked criteria. A full pass is allowed only when
all applicable criteria were evaluated. Structural findings go to `define-roadmap`,
placement to `promote-roadmap-items`, status or timing to `update-roadmap`.
The orchestrator determines its mode; this skill emits no mode.

## Self-Check

- [ ] The quality rule and project norms were loaded.
- [ ] All five dimensions and source-dependent criteria were examined.
- [ ] Requirement/defect granularity, parent consolidation and readability were checked.
- [ ] Status vocabulary, column separation, source-backed transitions and closure evidence were checked.
- [ ] No missing strategic dossier was treated as a mandatory-format failure.
- [ ] Evidence and history limitations are explicit and not reported as passes.
- [ ] Findings follow the shared Spec and cite rule sections.
- [ ] No file or placement was changed; a full pass has no unchecked applicable criteria.
- [ ] Selected views, cross-view consistency and destination evidence were evaluated.

## Filled deliverable example

[Filled review findings and corrected candidate](../define-roadmap/references/service-desk/review-findings.md). This is a fictional completed output, not a template
or authorization to change the adopting project.

## Phase and milestone contract

Use the [Roadmap Spec](../../specs/roadmap-modeling.md) to distinguish delivery groups,
work spans and event points. Check phase scope/exit conditions and milestone
criterion, owner, related IDs, evidence and timing basis. Detect unsupported event
occurrence and conflation with approval or requirement completion. Multiple events
for one version are valid. Legacy 1.0 markers and single-view plans remain valid;
do not demand new registers or impose a new gate.

Self-check: concepts, selected views and linked evidence agree with the source records.

## Revision history maintenance

Check the [revision contract](../../specs/roadmap-modeling.md#54-revision-records)
against available source decisions and preceding retained snapshots. Identify known
material changes absent from history, unsupported before/after claims, dropped or
duplicated records, unreadable history links and missing reasons/impacts. Check
latest-five display separately from durable retention. Do not treat a removed
historical object as an invalid current reference. Legacy adoption does not require
fabricated backfill; report unknown prior history as a limitation, not a failure.

Self-check: material changes are traceable, retained links resolve, and repeated execution adds no duplicate revision.

## Layered and iteration views

Check the Rule's reading/iteration criteria. Read main plus selected children and
source records: main alone must explain priorities, blockers and near-term delivery;
children must link back. Check facts and dates against their declared editable source,
not against another generated copy. Inspect selected iteration cadence/goals/scope,
timeboxes, unallocated work, version mapping and board links. Carry-over is valid;
iteration end is no evidence of release, completion or event occurrence. Do not demand
iterations or child documents from a single-view plan. Structure/layout defects route
to define-roadmap; existing goal/scope/cadence/timebox drift routes to update-roadmap.

Self-check: all selected documents were examined; main readability, iteration
semantics, ownership and link limitations are reported without mandatory expansion.

## Scenario and selection review

Evaluate the Rule's scenario/intake criteria against existing source decisions.
Check primary/supporting views, rationale, layout and source facts; custom choices
need consistency, not conformity to a recipe. Missing optional metadata in legacy
plans is not a defect or demand for migration. Detect changed context or unexplained
choice resets and source/projection disagreement. Read selected flow policies and
metrics evidence; unknown baselines are valid, invented numeric defaults are not.
Report intake history as cannot evaluate when unavailable; never claim a real user
interview was verified merely because a generated selection table exists.

Self-check: recommendations are distinguished from settled choices; recipe adherence
and new-schema adoption were not imposed as quality gates.

## Deliverable language

Before writing roadmap-chain deliverables, apply the [language contract](../../specs/roadmap-modeling.md#57-deliverable-language-schema-15).
Read the user instruction, consuming-project policy and existing artifact first;
retain a settled choice across handoffs. For a new artifact infer only from consistent
reader/document evidence; ask only unresolved gaps or winning-level conflicts.
Conversation language and English templates alone do not select artifact language.
Record the choice and source in existing norms/planning decisions; no new mandatory
configuration. Localize all new prose and display labels consistently while preserving
IDs, machine fields, canonical enums, source links and historical originals.

Review without rewriting or prompting for missing evidence. Report unresolved language
basis as cannot evaluate where appropriate; flag actual inconsistency against the
Rule. Findings prose follows the established report language; findings keys and
severity/category values retain the findings-list contract.

Self-check: language evidence and retained choice are explicit; all new display prose
is consistent, machine contracts are unchanged, and unavailable checks are reported.
