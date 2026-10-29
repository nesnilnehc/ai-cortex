---
artifact_type: guide
lifecycle: living
created_at: 2026-10-29
status: active
---

# Build and release workflow

Use [build-project](../../skills/build-project/SKILL.md) to build a project or
component without making a release. Its source revision, artifact identities and
actual result can be passed to [prepare-release](../../skills/prepare-release/SKILL.md).
Preparation may invoke the build Skill when an additional build is needed.

A release can have several candidate builds. For example, candidate A can fail a
project test and candidate B can pass; their results remain separate. The Release
Package records the selected candidate for each target and the checks applicable
at each stage. A required server check stays pending until upload makes it possible.

[publish-release](../../skills/publish-release/SKILL.md) reuses a verified selected
candidate, or invokes the build Skill when the project requires another build. A
combined build-and-upload tool is a publication operation, not a build-only tool.
Publication records per-target results and any relation between a candidate and a
transformed output. Unknown actions are reconciled before retry.

[announce-release](../../skills/announce-release/SKILL.md) uses verified published
target facts. It may announce a completed subset when the applicable contract allows
it; announcement recovery does not rerun builds or publication. The
[Release Package Spec](../../specs/release-package.md) owns the record contract;
individual Skills own their behavior. Existing 1.x semantics remain unchanged.
