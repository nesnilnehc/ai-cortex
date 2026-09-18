---
artifact_type: guide
created_by: ai-cortex
lifecycle: living
created_at: 2026-09-18
status: active
---

# Releasing AI Cortex

This guide covers releasing **this repository**. It is a usage map for the release Skills, not a second definition of them: `prepare-release` and `publish-release` own the behaviour, and [specs/release-package.md](../../specs/release-package.md) owns the Release Package shape.

## Use the Skills

Run `prepare-release` first, then `publish-release`. Neither step is done by hand, for two reasons: the Skills already encode the decisions a release needs, and this repository is where they come from, so releasing it is the most honest test they get.

| Skill | Does | Does not |
| :--- | :--- | :--- |
| `prepare-release` | Fixes the version and range, runs the gates, writes the Release Package | Commit, tag, push, publish |
| `publish-release` | Tags, builds, creates the provider release, writes the receipt | Regenerate the changelog, announce |
| `announce-release` | Writes and delivers announcements | Decide the version or edit the changelog |

`prepare-release` runs as a dry run by default and writes nothing until its artifact list is confirmed.

## What counts as worth releasing

The four directories `bin/cortex` installs are `skills/`, `rules/`, `specs/` and `protocols/`. A range that changes none of them changes nothing for anyone who installed AI Cortex, and `prepare-release` is expected to return `decision=none` for it.

A range of documentation, scripts, CI or tests alone is therefore not a release. A change to a rule's obligations, a skill's behaviour or a spec's contract is.

## Version domains are independent

The product version lives only in the git tag. Every skill and rule carries its own `version` in frontmatter, and those do not follow the product version.

Bump the version of every asset a release edits, per the [versioning rules](../../CONTRIBUTING.md#versioning) — a metadata-only correction is still a PATCH. A consuming project reads an asset's version to decide whether to re-read it, so an edited asset whose version is unchanged tells that project something untrue.

## Three things to get right

**Set `status: ready`, not `draft`.** A package whose required artifacts are all present and whose gates all pass is ready. `publish-release` refuses to load anything else, which is the intended guard rather than an obstacle to work around.

**Expect the tag to sit one commit past `commit`.** A manifest cannot contain the hash of the commit that contains it, so the tag points at the commit that finalised the package. Record the offset in `tag_offset` and the tag's real hash in `publication.tag_sha` rather than leaving the two to look like a mismatch.

**Put the release notes under `.cortex/release/<version>/`.** The Release Package Spec's example writes them to `RELEASE_NOTES.md` at the repository root, which fails this repository's own checks twice: nothing links there, so it is an orphaned document, and `NOTES` is on the process-record filename list in [repo-structure-hygiene](../../rules/repo-structure-hygiene.md). Keeping them beside the manifest also gives `publish-release` one source for the provider release body, instead of a file, a release page and a changelog entry all carrying the same prose.

## The changelog

Entries accumulate under `## [Unreleased]`. Cutting a release renames that heading to the version and its date, and opens a fresh empty `## [Unreleased]` above it.

Then check the cut: the released section must be byte-identical to `git show <tag>:CHANGELOG.md` for that section. Both changelog defects this repository has had were visible there — a tag created without cutting the section, and a later commit landing inside an already-released one.

## Afterwards

The Release Package records what happened. `status` becomes `published` only once the provider returned a receipt; a local commit and tag alone are not a publication, and the `publication` block carries the rollback path for when one is needed.
