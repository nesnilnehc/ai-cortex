---
name: build-project
description: Build a project or selected component using its own tools without publishing; use independently or for a release candidate.
version: 1.0.0
license: MIT
---

# Build Project

## Purpose

Build the requested source and report its actual outputs. A build is independently
usable and does not decide a release version, create a release or authorize upload.

## Behavior

1. Identify the project, requested revision, component, build configuration and
   output purpose. Inspect its instructions, build scripts and available tools;
   choose a supported project command rather than inventing one. If the command
   or its effects are ambiguous, explain the gap and stop.
2. Inspect the actual checkout and command side effects, including output cleanup,
   version files, network access, signing and packaging. Preserve unrelated work.
   When the only available operation also publishes or uploads, report the missing
   build-only capability and do not invoke it as a build-only request.
3. Execute only the requested, authorized build. Capture command, source revision,
   branch where known, build identity, result, artifacts and evidence. Distinguish
   actual values from planned or unknown values; do not invent missing hashes.
4. Return failures and incomplete outputs without claiming success. A caller may
   associate the returned outputs with a release candidate after verifying identity.
   Reuse existing artifacts only when the caller confirms their actual identity;
   do not rebuild merely because a release is resumed.

## Handoffs

The user can invoke this Skill alone. `prepare-release` or `publish-release` may
invoke it when a build is needed and the project supports a build-only operation.
Neither caller grants permission for extra remote actions. A project-managed
combined build and publication action belongs to the publication workflow, with
its full effects and authorization recorded before execution.

## Self-Check

- [ ] The selected command and its effects are supported by project evidence.
- [ ] The requested scope, revision, outputs and actual outcome are reported.
- [ ] Build-only execution did not initiate publication or create a release.
- [ ] Missing capability or ambiguous effects were reported without guessing.
