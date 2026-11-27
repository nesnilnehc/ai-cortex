---
name: upgrade-dependencies
description: Upgrade a project's third-party dependencies to the latest stable versions it can support, including major releases. Use for a dependency refresh or a named dependency upgrade that needs package-manager updates, migration, and verification.
license: MIT
metadata:
  version: "1.0.0"
---

# Upgrade Dependencies

Bring selected third-party dependencies to the latest stable releases that can be installed, migrated, and verified within the project's support commitments. A general upgrade request includes major, minor, and patch releases. Apply ordinary upgrades and the code or configuration changes they require without per-package confirmation. Honor narrower scope and exact version targets.

For a read-only request, use existing local evidence and read-only queries to report candidate versions, compatibility findings, and checks still needed. Leave project files and installed dependencies untouched.

## Establish the baseline

1. Identify the affected projects or workspaces and their authoritative dependency declarations and lockfiles. Use the repository wrapper, toolchain declarations, and CI configuration to find the expected package manager, version, and sources. If the required tool or configured source is unavailable, report the affected operation and continue independent work with the tools and evidence available. Keep the project's package manager and source configuration in force. Include in-scope direct runtime and development dependencies by default. Let the package manager resolve transitive changes needed by the upgrade. Use the project's existing controls for any explicitly targeted transitive dependency.
2. Record current declared constraints and resolved versions. Read the project's runtime, platform, integration, and compatibility commitments from its manifests, CI matrix, and documentation. Distinguish a declaration or lockfile pin used for reproducibility from a documented hold or support constraint.
3. Inspect the working tree and index before editing. Preserve existing user changes and establish a recoverable baseline for the files each batch will edit. Run the relevant existing checks before the first batch or use current evidence for the same inputs. Record any pre-existing failure or missing baseline.

## Select targets

1. Query the project's configured sources using the ecosystem's version and stability rules. For general upgrades, identify the latest published stable release and the highest stable candidate permitted by the project's policy and support commitments. Exclude prereleases and releases withdrawn or deprecated for use by the publisher. For an exact target, evaluate that version. Use the resolver to confirm that it selects the intended candidate, especially when the current manifest range excludes it. Report unresolved version availability as unknown.
2. For a potentially breaking update, read the official release notes and migration guides for each crossed release line that contains breaking changes. Check the project's actual API, configuration, and behavior against those changes. Check runtime and platform requirements, peer compatibility, and shared version constraints. A minor or patch label alone does not establish compatibility, especially for pre-1.0 packages.
3. If the desired stable target requires changing a project support commitment, ask about that decision only. State the target, the impact on users or supported environments, and the newest viable target under current support. While waiting, continue independent batches and, when useful, verify a fallback within the requested scope. Keep existing support in force until the user chooses otherwise. Treat ordinary dependency range edits and local migrations as part of the upgrade.

## Apply and verify in batches

1. Update tightly coupled packages together when their versions must move in step. Keep unrelated breaking upgrades in separate batches and group compatible routine updates when failures will still be easy to isolate. Account for the team's documented dependency holds and policies. Use the project's package manager or build wrapper with its configured sources and version policy. Update authoritative declarations and let the manager generate lockfile changes. Review the resolved graph and investigate unexpected packages, registries, or unrelated changes before accepting the batch.
2. Make the smallest migration that preserves supported behavior. Update affected source, tests, and configuration, including matching versions in CI or containers when they must move with the dependency. Apply only upstream migration steps relevant to the repository. Inspect any migration tool and its effects before running it. Follow existing project verification and lifecycle requirements.
3. Verify each batch in an environment that uses the expected resolved versions. Use the project tooling to install them or let its normal build or test entry point resolve and load them. Check the dependency graph used by verification before marking the batch as passed. Run relevant build, type, unit, and integration checks, including affected runtime, data, or integration paths that fast checks miss. Repeat the relevant combined checks against the final graph. If they fail, isolate the interacting upgrades and apply the same recovery steps.
4. Compare failed checks with the recorded baseline. Identify regressions, failures already present before the upgrade, and checks blocked by missing tools, access, or environments. For unchanged baseline failures or unavailable checks, use equivalent evidence against the candidate where project policy permits it. If required verification remains blocked, keep the batch unverified and restore its edits. Report which checks ran and which remain blocked. Skip version retries while the same verification blocker applies to all candidates.
5. Fix in-scope migration issues, split the batch to isolate failures, or retry with a coupled dependency if the evidence warrants it. Restore only that batch's failed edits before retrying, keeping earlier successful batches and user changes. If the latest stable release remains blocked by a candidate-specific issue, try the next highest viable stable candidate within the authorized range. If an exact target cannot be verified, retain the baseline and report the blocker and any known alternatives for the user to consider. If no candidate can be verified, retain the baseline for that dependency and continue independent work. Never bypass resolver constraints, integrity checks, or required project checks to obtain a newer version.

## Report and self-check

- Report the old and final resolved versions, significant migration edits, and the checks that ran and their outcomes. Distinguish verified upgrades, unavailable verification, and dependencies already current.
- Include a version difference summary by default for completed upgrades. Compare each relevant dependency's previous resolved version with its final verified version. Focus on the major releases crossed, their breaking changes and migration impact, and new features relevant to the project, including features introduced in intermediate releases. Cite official release notes or changelogs and identify which changes the project adopted and verified. Report gaps in upstream documentation alongside the findings supported by available sources.
- For dependencies held below the latest stable version, report the latest known target, the specific blocker, and the highest verified result or retained version. Keep upstream availability distinct from local resolution and successful verification.
- Confirm that major updates were considered within scope, each retained batch has matching declarations and lockfiles where the project uses them, and existing support commitments and unrelated work were preserved. Commit, push, publish, or make other external changes only when separately authorized.

## Example

The user requests `3.2.0` for one dependency. It resolves and builds, but the required integration environment is unavailable. Record both results, restore the previous version, and report the missing integration check. Continue other authorized upgrades whose checks can run.
