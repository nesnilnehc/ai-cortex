---
name: prepare-version-notes
description: Prepare or revise version change descriptions for an already selected component, target version and scope, using project conventions and explicit source comparisons. Use for changelog entries, version notes or release lists; version selection, source edits and artifact delivery are separate tasks.
version: 0.1.0
license: MIT
---

# Prepare Version Notes

Describe the changes in an already selected version and verify the description against its scope and source evidence. Reuse the project's changelog, version notes or release list. This capability can run before or after mechanical version edits; it does not require a version-planning skill, an automatic companion call or a commit after each revision.

## Resolve the request and existing notes

Read project instructions, documentation conventions, current branch/HEAD, staged and unstaged changes, and existing note entries. Preserve unrelated work, human edits and released history. Identify the component/version domain, exact target version, selected delivery scope, intended readers, output location and comparison purpose. Accept offline decisions or existing project records; ask only for missing or conflicting inputs instead of choosing the version or assigning requirements to it.

Discover existing authoring entry points and formats. Prefer the maintained document over a parallel inventory or mandatory JSON handoff. If there is no established location, choose one consistent with project documentation norms; ask when competing destinations or reader needs remain unresolved. Do not design a release framework to write an entry.

Before running a project command, inspect its invoked commands and hooks. Use a documented authoring-only mode or a narrow document edit when the entry point also bumps versions, commits, tags, builds or publishes. If no safe mode is available, report the specific gap rather than invoking the broader workflow. Prefer available local tools; do not install dependencies just to produce notes.

## Establish comparison evidence

Resolve the target source to an exact commit SHA where applicable. If the project supports a working-tree target, record the base commit and enough changed-input identity to distinguish it from a pure commit snapshot. Version labels, branches and movable tags alone are not exact source identities.

Use an explicit comparison purpose and baseline:

- For changes since the previous formal delivery, prefer the source commit associated with the selected formal-channel artifact. Identify the component, channel and artifact/version concerned; do not substitute the highest version, most recent bump commit or nearest tag automatically.
- For comparison between candidates, a previous candidate may be the baseline when that is the stated purpose. Do not present candidate-to-candidate changes as the full difference from the previous formal delivery.
- An explicitly supplied baseline or first-version scope is valid when its purpose is clear. A first version has no implied prior delivery; do not invent a zero baseline or scan all history as the default scope.

Accept supplied artifact/source associations or collect them through available read-only registry, directory or project-record capabilities. Discover tools by operation and match the selected artifact source; no particular companion skill or service API is required. Distinguish a recorded source claim from independently verified provenance. If access or association evidence is missing, report the concrete gap and request the needed baseline/source evidence rather than guessing or changing credentials.

Inspect source relationships and actual changes. Where Git applies, check whether the baseline is an ancestor of the target before treating a commit range as a linear progression. Divergence, unknown identities or unavailable history require an explicit comparison method or evidence; do not silently choose a merge base. Continue independent drafting from established facts, but keep unsupported comparisons unresolved.

## Prepare or revise the description

Compare relevant commits and file changes with the supplied scope and authoritative project records. Commits in a range are discovery evidence, not automatic requirement membership or proof that a planned item shipped. Identify incomplete items, unrelated changes and missing associations. If excluded behavior remains in the target/package inputs, expose the mismatch: omitting it from notes does not remove it from the artifact. Do not cherry-pick, rewrite history or change implementation to reconcile the scope.

Write concise, reader-appropriate descriptions of evidenced changes using the project's language, sections and terminology. Include relevant behavior changes, fixes, migration instructions and known issues when supported by evidence. Do not infer compatibility promises, test success, publication, acceptance or deployment from version numbers, commit messages or planned scope. Consume established compatibility decisions; leave unresolved decisions explicit.

Update the existing in-progress entry at the same target rather than adding duplicates or advancing the version. Preserve its established date unless project rules or the user require a change. Edit only owned content; resolve conflicting human edits before replacing them. Keep released entries frozen unless a historical correction is explicitly authorized. If the requested description already matches current evidence, report no change.

## Verify and hand off

Check the description's component/target version, comparison purpose, baseline/source association and target source against the resolved inputs. Verify material statements against the actual comparison and scope records; check for omissions, contradictory exclusions and unsupported completion claims. Record unresolved evidence or scope issues rather than declaring them passed. Inspect the document diff and run relevant local document checks; code/build/package verification belongs to the project's verification workflow.

Return the description location and an identifiable revision or content digest, with component/target version, comparison purpose, baseline and association evidence, target source identity, verification result and unresolved issues as needed for another agent to consume without this chat. Use the existing document or project handoff; no new machine-readable file or fixed output schema is required. The content digest identifies the notes, not a successful build or delivery.

Keep implementation-source identity distinct from the revision containing the note edit; do not invent the SHA of a future commit or embed a self-referential digest. A later commit containing notes may change the commit identity without changing implementation content. The project must preserve that association, and changed implementation/scope inputs require refreshing the affected description and checks before delivery consumes it.

Report whether notes are prepared, already current, or awaiting specific evidence/decisions. On failure, preserve inspectable edits and the same target; resume only affected work without resetting or stashing unrelated changes. Reuse prior checks only while their relevant inputs still match.

This skill owns description facts, scope and target consistency. It does not decide the next version or compatibility impact, change requirement assignments, modify version files or source code, commit, tag, push, build, upload or publish. Notes are a delivery prerequisite only when project/target rules require them; ordinary branch/test builds gain no universal release-note gate. A project can review and commit version edits and notes together through its existing mechanism.
