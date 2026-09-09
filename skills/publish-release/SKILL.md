---
name: publish-release
description: Validate a ready Release Package and execute the repository's publication steps—tag, build, package, and provider release—with explicit mutation gates.
description_zh: 校验 ready 状态的 Release Package，并按仓库约定执行 tag、构建、打包和发布；所有外部写入均有明确闸门。
tags: [release, publish, tag, build, package]
version: 1.2.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [publish release, ship release, tag and publish, release artifact]
input_schema:
  type: free-form
  description: Ready Release Package path or preparation result; optional provider and dry-run preference
output_schema:
  type: side-effect
  description: Publication result with tag, build/package evidence, provider receipt, rollback path, and updated Release Package status
---

# Skill: Publish Release

## Purpose

Consume the `ready` Release Package produced by `prepare-release`, execute the publication actions the project has already configured, and write the actual result back into the package. Does not regenerate the changelog, does not write announcement copy, and does not silently assume a target platform.

## Core Goal

Complete a traceable publication only after the Release Package's required gates and materials are satisfied and the user has confirmed the external writes, then return a real receipt or an explicit failure state.

## Behavior

1. **Load and validate**: require `decision=release` and `status=ready`; confirm the version, channel, canonical version source, per-domain version actions, target SHA, required artifacts/checks, current branch and working-tree state. Stop on `not_required`, a failed gate, an SHA mismatch, or a dirty working tree that is not permitted.
2. **Discover the publication path**: find the version-sync, commit, tag and build/package/provider commands from local evidence such as `CLAUDE.md`, `.ai-cortex/config.yaml`, CI configuration, Makefile, manifests, bump tools and Docker/GoReleaser; prefer reusing an existing pipeline, and record the commands the project has explicitly forbidden.
3. **Establish a state baseline**: before any mutation, record the canonical version, the files expected to change, HEAD, the existing release commits/tags and the working tree. If a previous failure left behind the target version, partial file edits, a commit or a tag, enter the recovery path first instead of rerunning the mutator.
4. **dry-run**: show the per-domain version actions, the expected files, the commit boundary, the validation commands, the tag, the artifacts, the permissions/credentials, the provider and the rollback path for every step. Version sync, commit, tag, push, upload and release must each be confirmed first.
5. **Version and commit**: execute only the product version-sync plan the package has confirmed; an independent version domain set to `preserve` must not be changed along with it. Reuse the project's release tool when it commits on its own; otherwise call the locally vendored AI Cortex `commit-work` for precise staging and commit, with this Skill owning the ordering and the receipt. When that Skill is absent, stop the commit phase; do not install it from an external registry and do not substitute an inline simplified flow.
6. **Pre-tag gate**: before creating a tag that cannot be reused, run the project-approved required validation and verify that the canonical version, the derived versions, the first version entry in the user-facing material and the expected files all agree. Stop as soon as any required check fails; do not create the tag.
7. **Publish and receipt**: once validation passes, execute in the project dependency order that was discovered. A project that has to freeze artifacts before tagging runs build/package first and then creates the annotated tag; a project whose CI is triggered by the tag tags first and then waits for the pipeline's build/package receipt. Then push or trigger the provider release, as authorized. When a command or tool is missing, report that it did not run instead of faking success; discover the capability first when an external connection is needed.
8. Write the package status as `published` only when the provider release succeeded and left a receipt. With only a local commit/tag, it must not pose as published.

### Recovering from a partial change

After a version tool fails, first compare the state baseline against the current state: check the canonical version, the expected files, HEAD, and whether the target commit and tag already exist. Classify every step as `not_started` / `partially_applied` / `complete` and continue only the missing ones. Never rerun bump just to "try once more"; never bump the version twice; when the target tag already exists but points at the wrong SHA, stop and ask for a decision instead of deleting or rewriting remote state automatically.

## Boundary against existing capabilities

`generate-github-workflow` owns workflow generation, the locally vendored `commit-work` owns the quality of each commit, and `announce-release` owns post-release communication. `publish-release` only orchestrates the confirmed order of version sync, commit, tag and provider; it does not reimplement those atomic capabilities and does not download a missing Skill at runtime. Sources for externally derived Skills are maintained in one place, [`../SOURCES.yaml`](../SOURCES.yaml).

## Input and Output

Input is a `ready` Release Package path or a preparation result, plus an optional provider and `dry_run` (default `true`). Output is the publication receipt, the actual tag/artifact information, the provider receipt, the rollback path, and the package status updated per the Spec.

## Limits

- Without confirmation, must not push, upload, create a GitHub Release, publish to a registry or change production.
- Does not skip required checks, and does not replace the repository's existing release entry point with a new command.
- Does not create a tag before the required validation; does not blindly rerun a version tool over a repository that is already partially modified.
- Does not bump an independent version domain marked `preserve` in the package.
- Does not write credentials into a manifest, a log or the chat; stops when credentials are missing and states what environment is needed.
- On failure, keeps the state and rollback path accurate, and does not delete a remote tag or release automatically.

## Self-Check

- [ ] The package is `decision=release` / `status=ready`, and the version domains, SHA, range, checks and artifacts are traceable.
- [ ] Every command and provider has local configuration or tool-capability evidence behind it.
- [ ] A state baseline was recorded before any mutation, so a partial failure can be split into completed and missing steps.
- [ ] The canonical version, the derived versions and the version in the user-facing material agree, and the required validation passed before the tag.
- [ ] Every irreversible write action was confirmed beforehand.
- [ ] `published` was written only after a success receipt.
- [ ] Output carries the tag, the artifacts, the receipts, the failure point and the rollback path.

## Examples

### Example 1: GoReleaser already in place

After finding `.goreleaser.yaml` and a tag-triggered workflow, reuse them; once confirmed, run only the tag/push the project prescribes, and copy no Docker or GoReleaser configuration.

### Example 2: Local build capability only

A tarball can be produced but there is no provider. The Skill completes the local build/package and outputs a pending-publication receipt, but does not mark the status `published`.

### Example 3: The version tool fails in a commit hook

The canonical version and the expected files turn out to be updated already, but the release commit and tag do not exist. Do not run bump again; validate the change set, complete the missing commit, rerun the required validation, then create the tag. If the tag already exists with a mismatched SHA, stop and report the conflict.
