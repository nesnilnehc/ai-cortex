---
name: prepare-release
description: Build and validate a Release Package from repository history, version policy, quality gates, and optional release artifacts; does not publish or announce.
description_zh: 基于仓库历史、版本策略、质量门禁和可选发布材料构造并校验 Release Package；不负责发布或公告。
tags: [release, versioning, changelog, release-package, orchestration]
version: 1.4.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [prepare release, release package, release readiness, cut release]
input_schema:
  type: free-form
  description: Repository path; optional target version/channel, previous tag, artifact preferences, and dry-run preference
output_schema:
  type: document-artifact
  description: Release decision and Package manifest with version domains, change items, artifacts, checks, and readiness; no commit, tag, push, upload, or announcement
---

# Skill: Prepare Release

## Purpose

Build an auditable [Release Package](../../specs/release-package.md): fix the version and the commit range, generate or collect release artifacts, run the necessary gates, and state `ready`, the blockers, and any gaps in optional artifacts. It orchestrates release preparation; it does not execute the release.

## Core goal

On success, emit an evidence-backed release decision: when a release is warranted, give the SemVer, channel, version domains, target SHA, git range, structured changes, artifacts, and readiness; when there is no product, compatibility, security, distribution, or operations significance to releasing, emit `decision=none` / `status=not_required` explicitly and manufacture no empty release.

## Behavior

### 1. Discover project conventions

Read `CLAUDE.md`, `.ai-cortex/config.yaml`, version files, CI configuration, repository docs, and git tags in priority order. Prefer reusing existing version scripts, changelog generators, test commands, and release configuration; do not invent commands out of thin air.

At the same time, build the version-domain inventory: identify the canonical source of the product version, plus independent version domains such as build, API, protocol, data format, prompt, and plugin. Record `current`, `source`, and this run's `action` for each version domain; you must not assume they must match the product version.

### 2. Resolve range and version

- Filter product release tags by the project's tag pattern first, excluding tags belonging to other version domains such as API contract, plugin, and data format; by default read only the current branch and the most recent product release tag.
- Decide `major` / `minor` / `patch` / `none` by actual release impact: user behavior and compatibility, and also security fixes, supported platforms, install/upgrade, distribution, and operations contracts. Conventional Commit prefixes and commit counts are only hints; inspect the diff, the requirement, or the change evidence when needed.
- Documentation-only, test, CI, internal-refactor, or rebuild-only ranges default to `none` unless they change one of the release impacts above. On `none`, emit a `not_required` report and stop generating artifacts.
- When the user supplies a version, validate it as SemVer and write it into the manifest without the `v` prefix; when none is supplied, present the candidate versions together with the evidence behind each.
- Identify the stable or pre-release channel. Where the project has rules, advance along its `alpha → beta → rc → stable` or equivalent states; where it has none, do not invent a channel — confirm with the user.
- Record the full commit SHA and a reproducible range; when there is no previous tag, mark it an initial release and flag the risk.

### 3. Confirm the artifact list

Before generating any artifact, propose an editable artifact list based on project conventions and have the user confirm it in one pass. You must not just ask the open-ended question "what artifacts do you need".

Selected by default:

- `changelog`: the change record for maintainers
- `release_notes`: the user-facing summary of this release
- `manifest`: the Release Package manifest

Recommended on project evidence, but not selected by default:

- `customer_notes`: recommended when there are external users, a customer portal, or a customer-documentation convention
- `sbom`: recommended when the project already has supply-chain, security, or compliance requirements
- `checksums`: recommended when the release ships downloadable binaries, archives, or installers
- `build`: recommended when the project wants candidate build outputs frozen during preparation; otherwise leave it to `publish-release`
- `video`: recommended when the user mentions a release video, or when `changelog-video` is present in the local AI Cortex installation

Show the user each item's purpose, default selection, required/optional status, and the evidence behind the recommendation. The user can add or remove artifacts and change what is required; explicit input takes precedence over defaults. When the user has already given a complete list, show only the normalized result for confirmation and do not ask again.

Example confirmation prompt:

```text
Proposed for this release:
[default/required] changelog, release notes, Release Package manifest
[optional/recommended] checksums (downloadable binary detected)
[optional] customer notes, SBOM, release video

Proceed with this list? You can add or remove artifacts, or switch an item between required and optional.
```

Only once the user has selected `video`, ask for the missing parameters that would change the outcome; at minimum confirm whether it is required. When audience, language, duration, and form are not supplied, defaults may be used as long as they are shown explicitly.

### 4. Build the release artifacts

First normalize the release range into `change_items`: each carries a stable ID, category, technical summary, user impact, source commit/requirement, and audience, plus module, breaking/migration, multilingual titles, highlight, and media as needed. Internal changes may stay as technical evidence, but must not flow into user-facing artifacts on their own.

Then identify the existing generators and produce only the changelog, release notes, customer notes, manifest, and SBOM/checksum/build artifacts the user confirmed: the technical changelog keeps interface, configuration, migration, and operations detail; the user-facing release notes carry only perceivable value. Both derive from the same set of change items — neither copies the other and then rewrites the facts. Do not reimplement `commit-work`, `automate-tests`, or `generate-github-workflow`.

#### Artifact shape: the reader is someone coming back after a while

The audience boundary (previous section) decides **what goes into** an artifact; its shape decides **whether it can be read**. An artifact counts as sound only when neither is met — writing for maintainers is not a licence to be unreadable: the writer holds all the background, so cramming causes, IDs, and paths into a single breathless paragraph costs them nothing, and that cost **is absent for the author alone**.

- **One meaning per entry**. An entry says one thing; when it will not fit, that is usually because it is two things — split it.
- **Conclusion first**: say what it became, then why; do not spend a whole paragraph on reasoning before delivering the conclusion.
- **Background and supporting detail stay out of the entry line** — add them in a separate sentence below the entry.
- **Restraint with internal markers**: requirement IDs, file paths, and commit hashes are things you look up in version control while diagnosing. If you keep one, keep it in the supporting sentence,
  and keep only the one that genuinely helps the reader locate something, not a whole string of them.
- **Upgrade notes must stand alone**: breaking changes, migration steps, and rollback cost get their own section — operations must not be made to read every feature entry just to confirm "whether data needs manual handling".

**The length threshold belongs to the project, not to this Skill**: it depends on the language, the readers, and the existing baseline, and a hard-coded number stops holding the moment the project changes.
Where the project has a threshold or an established entry shape, follow the project's. Where it does not, judge by the five points above, and a baseline can be measured from that project's **earliest, most readable releases**
for the project to settle on its own. The landing place is on the project side — its own rules and checks (one more red line in `rules/`, say) — not this Skill.

#### changelog-video integration boundary

`changelog-video` is a local, optional release-artifact Skill shipped with AI Cortex, not an implementation built into this Skill. Invoke it only after the user selects `video`; pass `decision=release`, the project identifier, version and channel, git range, the confirmed customer-facing change items, available media references, output directory, required status, and the confirmed preferences, then consume its `kind: video` artifact entry and check results. You must not ask it to re-parse git or long Markdown, and must not let it decide the version, edit the changelog, create a tag, or send an announcement.

- Present locally: invoke `changelog-video` and fold the video entry, with its producer information, into the manifest.
- Missing locally: you must not auto-install it from skills.sh, GitHub, or any other registry. When `video.required=false`, record `unavailable` and carry on; when required, hold at `draft` and tell the user to restore the local copy by updating the canonical AI Cortex installation.
- Execution failed: when optional, record the real failure and carry on with the other artifacts; when required, block ready.

### 5. Run the gates

Run the smallest relevant tests, lint, build, or security checks the project declares; the discovery logic of `automate-tests` can be reused. Prefer the commands the project has approved, and honor the verification methods it has explicitly forbidden. Record command, status, and evidence for each check. Where a review signal is needed, use the existing `review-diff` / `orchestrate-code-review` rather than rewriting review capability here.

### 6. Preview and write

`dry_run=true` by default: show the release/no-release conclusion, version and channel, the action for each version domain, the range, the change items, the files to be created or modified, artifact gaps, and gate results. Artifacts and the manifest are written only after the user confirms. This Skill creates no commit or tag, does not push, does not upload, and sends no announcement; those go to `publish-release` and `announce-release` respectively.

## Inputs and outputs

Input may include `repo_path`, `version`, `release_channel`, `previous_tag`, `artifacts`, `required_artifacts`, `video_preferences`, `output_path`, and `dry_run` (`true` by default). Output is the release/none decision, the artifact list the user confirmed, and the version domains, change items, artifacts, checks, and readiness that conform to the [Release Package Spec](../../specs/release-package.md).

## Limits

- Version files and release artifacts must not be modified until the preview is confirmed.
- Artifacts must not be generated until the artifact list is confirmed; optional artifacts must not all be selected by default.
- Do not fold commit/tag, build upload, registry publication, GitHub Release, or notification sending into the preparation stage.
- Do not decide the version from the commit prefix alone, and do not bump an independent version domain merely to keep it aligned.
- Do not report a failure of the optional video capability as an overall failure, and do not fake ready.
- Do not download, register, or upgrade any Skill at runtime; call the local AI Cortex copy only, with project-local conventions taking precedence.

## Self-check

- [ ] The manifest carries decision, full SHA, range, version domains, artifacts, checks, and status.
- [ ] The version candidate is judged by user impact and backed by evidence; `none` produces no empty release.
- [ ] The product version's canonical source, the independent version domains, and the pre-release channel are identified.
- [ ] Technical and user-facing artifacts come from the same set of traceable change items, with a clear audience boundary.
- [ ] Artifact shape holds up: one meaning per entry, conclusion first, background and internal markers out of the entry line, upgrade notes required to stand alone.
- [ ] Required checks and artifacts have each been decided.
- [ ] The default and optional artifacts, their purpose, required status, and the evidence behind each recommendation were shown and confirmed.
- [ ] changelog-video is wired in only as a local vendored optional Skill, and its absence triggered no external install.
- [ ] The dry-run preview was shown, and no publication or communication side effect occurred.

## Examples

### Example 1: an ordinary patch release

Input: "prepare the 1.4.2 release, generate the changelog and release notes". Read the most recent tag, reuse the project's test commands, generate the artifacts and the manifest; once the gates pass, emit a `ready` preview and wait for confirmation before writing to disk.

### Example 2: the video capability is unavailable

video is optional, but the local AI Cortex installation lacks `changelog-video`. The manifest records video as `unavailable`; with the other gates passing it can still be `ready`, and it tells the user to update the canonical AI Cortex installation and add the artifact afterwards, without offering a third-party runtime install command.

### Example 3: the user named no artifacts

The project is detected to ship binaries, but has no customer portal or SBOM convention. Select changelog, release notes, and manifest by default, mark checksums "recommended but not selected", and list customer notes, SBOM, and video as optional; generate only after the user confirms.

### Example 4: no new version is needed

The range holds only CI adjustments and an invisible test refactor. Although the commit prefix contains `fix`, no actual user behavior changed, so emit `decision=none`, preserve the product version and the other version domains, generate no release artifacts, and hand nothing off to `publish-release`.

### Example 5: advancing the pre-release channel

The project rules declare the current version to be `2.0.0-beta.2`, and the acceptance conditions for entering rc are met. The Skill proposes `2.0.0-rc.0` and states its basis; the API contract version is unchanged, marked `preserve`, and does not follow the product version bump.
