---
artifact_type: backlog-item
created_by: capture-work-items
lifecycle: living
type: issue
subtype: improvement
date: 2026-11-04
status: in-progress
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

The 3-point assessment is complete as recorded below. On 2026-11-04 the maintainer
authorized creation of prepare-version-notes with this bounded responsibility.
Implementation and catalogue intake are in progress; priority and roadmap
promotion remain unset.

## Assessment result — 2026-11-04

Read-only inspection of the originating project's current local files found:

| Existing mechanism | Verified responsibility | Gap against this request |
| --- | --- | --- |
| update-version-files | Writes the existing changelog and updates package, lockfile and server versions | Couples authoring to mechanical version edits and a project-specific four-file workflow |
| resolve-version-scope | Reads scope evidence and compares implementation with supplied decisions | Defaults to the last completed version update, which cannot establish the previous formal-channel delivery baseline |
| verify-version | Checks version equality, changelog entry, tests and package contents | Combines project verification and description checks rather than owning description authoring |
| commit-version | Reviews and commits the project's verified upgrade files | Commits existing work; does not provide independent authoring |

The project already has a maintained changelog with versioned entries. Its package
and pipeline define build/test/pack/publish behavior; no independent authoring
entry was found in the inspected project-local Skill and command directories,
package scripts or delivery documentation. This is a scoped local observation,
not a claim that every project lacks such a mechanism. The inspected source
working tree was left unchanged; no registry or live pipeline was queried.

Recommendation: assess a narrow shared capability named **prepare-version-notes**.
Its trigger would be a request to prepare or revise notes for an already selected
component/version/scope and comparison purpose. Inputs are the selected source,
scope and baseline evidence plus the project's existing note convention. Output
is an updated existing description and a concise, source-associated handoff with
unresolved gaps. It owns facts/scope/target consistency, not compatibility advice,
requirement assignment, version edits, commits or artifact delivery. A previous
formal-channel artifact's recorded source may be supplied by the user or an
existing inspection result; no mandatory companion Skill is implied.

The reusable responsibility is independent of the observed package manager and
four-file layout, so a shared atomic capability is preferable to transferring
the coupled project workflow unchanged. A project-owned adapter remains valid
when its local convention already performs this responsibility. Before creating
the shared Skill, the maintainer must approve the name and this bounded scope.
That decision is separate from delivering the three already reviewed Skills.

## Implementation

The maintainer subsequently approved creating the independent AI Cortex asset.
The [Skill source](../../../skills/prepare-version-notes/SKILL.md) implements note
authoring, explicit baseline purpose/source association, factual verification and
a reusable handoff. It adds no executable release framework. Catalogue provenance,
distribution and document checks complete intake; no live project release is
required to validate this prose-only asset.

## Review criteria for a later proposal

- Formal-channel and candidate baselines keep their distinct purposes; unknown
  or divergent identities remain visible.
- Existing formats remain usable and test builds gain no blanket gate.
- Examples separate source-range facts from requirement membership and expose
  exclusions still present in the actual package.
- Output supports delivery without absorbing versioning, committing or publishing.

Source: maintainer's eight confirmed boundaries, relayed on 2026-11-04.
