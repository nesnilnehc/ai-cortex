---
name: bump-version
description: Update a project's version references to an explicit target version or calculate the next version from a supplied increment, then verify consistency. Use for mechanical version changes; compatibility analysis, release scope, changelog authoring, and delivery are separate tasks.
version: 0.1.2
license: MIT
---

# Bump Version

Apply an already chosen version or increment through the project's version mechanism and verify the resulting references. Support different projects without hardcoding package managers, file names, registries, or Git conventions. Calculating a version from a supplied increment is arithmetic under the project's rules, not a recommendation about the impact of code changes.

## Inputs

Require a project/component and either an exact target version or an explicit increment supported by its version policy. The current checkout can supply project context. Discover current version and policy from authoritative project configuration and instructions.

The version decision may come from the user, an offline decision or an existing project record; no version-planning skill is required. Version edits and separately prepared change descriptions may be revised in either order without forcing one capability to invoke the other. This skill verifies version references; description facts and scope, code/package verification, and reviewed commits belong to their respective project mechanisms. A version edit does not require an automatic commit.

If neither target nor increment is available, ask for that specific input before editing. Do not inspect requirements, commit history, a release diff, or a registry's latest version to choose major/minor/patch. If the user asks which increment is warranted, explain the missing impact decision and leave that analysis to a separate task. An exact target fixes the intended value; if both target and increment are supplied and disagree, resolve the conflict rather than choosing one silently.

## Discover the version mechanism

1. Read project instructions. Inspect repository root, branch, HEAD, staged/unstaged changes, and existing version-update scripts/configuration. Preserve unrelated work and its staging.
2. Identify the selected component and version domain, authoritative current version, version scheme, synchronized references, and project-owned update entry point. Product, API, protocol and data-format versions can be independent, including within a single component. In a monorepo, establish whether versions are independent or coordinated. Update only the selected domain and components plus those the project's rules require to move with them. If the selection or required coordination is ambiguous, ask before editing.
3. Before executing any project command, including consistency checks and other verification commands, inspect its invoked commands and lifecycle hooks for changelog generation, builds, Git commits/tags/pushes, publication, or other effects outside this task. Disable these effects only through a documented scoped mode or use a narrow supported file edit. For verification, use direct comparison of required references when the command cannot safely run. If safety cannot be established or no safe method is available, report the gap rather than running the broader workflow.

Prefer existing project tools and available local dependencies. Do not add a version-management dependency or global installation merely to increment a version. Existing lockfiles should be updated by their package manager where supported, not by broad text replacement. If the necessary tool is unavailable, report what is missing and preserve the current state.

If a tag or build-time generator is the sole version authority, report how this target would be supplied through that mechanism. Do not invent a persistent version file or create a tag. If the project has no established version mechanism, identify the missing project decision rather than designing one inside this operation.

## Resolve the exact target

- For an explicit target, validate its syntax and applicable project constraints. Do not reclassify its compatibility impact.
- For an explicit increment, calculate the target from the authoritative current version using the project's scheme and supported tool. SemVer projects follow their SemVer arithmetic; calendar or custom versions follow their own documented rules. Do not impose SemVer or infer a new numbering policy.
- A prerelease transition needs the project's existing rule and enough input to resolve the identifier/counter; do not guess the channel or reset counters silently.
- If sources disagree or an unfinished version edit exists, inspect ownership and the intended target. Resume a clearly identified change at the same target rather than incrementing it again. If an increment is repeated after a completed update, do not assume it is a retry or a new request: resolve the intended target from the request and available evidence, and ask if ambiguous. If unresolved, report the specific conflict before modifying files.
- If the target already matches all required references, report no change. Reject an unsupported decrement or reuse under the project's rules; an explicit correction permitted by those rules is not automatically a release.

An availability check in a registry, published-artifact baseline, or last version-bump commit is not required for this local edit. Publication/version-allocation checks belong to the relevant release or delivery workflow. Do not claim a locally valid version is available to publish.

Before editing, fix the baseline, exact target and required synchronization mapping for each selected component/version domain in the working context. On interruption or partial failure, retain those targets and complete only the outstanding references; do not calculate another increment from an already updated value. For example, if a 1.2.3 → 1.3.0 change updates one of two required references before interruption, resume by bringing the remaining reference to 1.3.0, not by advancing to 1.4.0. Recover the intended targets from available evidence when needed; if they remain ambiguous, ask before editing. This does not require a new persistent state file.

## Modify and verify

Apply the exact target only to the selected version domain and required synchronized references and generated metadata. An explicitly selected API, protocol or data-format version is a valid target. Change dependency constraints or other version domains only when the project's rules require them to synchronize with that target; do not change unrelated versions, application behavior, requirements, or historical release entries merely because they contain similar numbers.

Run the project-supported consistency check, or explicitly compare the authoritative value and every reference that must synchronize according to the project's mapping; coordinated domains need not have identical version numbers. Missing or ambiguous references are failures, not default values. Inspect the diff for unintended edits and check whitespace. Run additional targeted checks only when the project requires them or the version change affects generated code or behavior; a full test/build/package run is not an automatic requirement for a metadata-only change.

On failure, keep the edits inspectable, report which values/files differ, and fix only within the authorized scope. Do not reset or stash unrelated work, weaken checks, or calculate another target to conceal a failed attempt. Reuse prior passing evidence only while its relevant inputs still match.

## Output and boundary

Report the previous and exact target versions, whether the target was supplied or calculated from a supplied increment, the project mechanism, changed file links, consistency-check results, and remaining blockers. If the version is derived solely from tags or build parameters, explain that no persistent file change was made and give the established handoff. Keep the response short and distinguish verified equality from merely displaying values.

This skill ends with verified local version edits (or an explained no-op/blocker). Do not select release scope, analyze compatibility, write changelogs/release notes, commit, create/move tags, push, build deliverables, or publish. Those are separate operations; a request to bump a version alone does not authorize them. No companion skill or specific Agent API is required to perform this capability.
