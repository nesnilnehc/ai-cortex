---
name: upgrade-dependencies
description: Upgrade a project's third-party dependencies to the latest stable versions it can support, including major releases. Use for a dependency refresh or a named dependency upgrade that needs package-manager updates, migration, and verification.
version: 0.1.0
license: MIT
---

# Upgrade Dependencies

Bring selected third-party dependencies to the latest stable releases that can be installed, migrated, and verified within the project's support commitments. A general upgrade request includes major, minor, and patch releases. Apply ordinary upgrades and the code or configuration changes they require without per-package confirmation. Honor narrower scope, exact version targets, and read-only requests.

## Establish the baseline

1. Identify the affected projects or workspaces and their existing package manager, version, package sources, and authoritative dependency declarations and lockfiles. Include in-scope direct runtime and development dependencies by default. Let the package manager resolve transitive changes needed by the upgrade. Use the project's existing controls for any explicitly targeted transitive dependency.
2. Record current declared constraints and resolved versions. Read the project's runtime, platform, integration, and compatibility commitments from its manifests, CI matrix, and documentation. Distinguish a declaration or lockfile pin used for reproducibility from a documented hold or support constraint.
3. Inspect the working tree and index before editing. Preserve existing user changes and establish a recoverable baseline for the files each batch will edit. Run the relevant existing checks before the first batch or use current evidence for the same inputs. Record any pre-existing failure or missing baseline.

## Select targets

1. Query the project's configured sources using the ecosystem's version and stability rules. Identify the latest published stable release and the highest stable candidate permitted by the project's policy and support commitments. Exclude prereleases and releases withdrawn or deprecated for use by the publisher. Use the resolver to confirm what will actually be installed, especially when the current manifest range excludes a newer release. Record registry or access failures as unknown.
2. For a potentially breaking update, read the official release notes and migration guides for each crossed release line that contains breaking changes. Check the project's actual API, configuration, and behavior against those changes. Check runtime and platform requirements, peer compatibility, and shared version constraints. A minor or patch label alone does not establish compatibility, especially for pre-1.0 packages.
3. If the desired stable target requires changing a project support commitment, ask about that decision only. State the target, the impact on users or supported environments, and the newest viable target under current support. While waiting, continue independent batches and, when useful, verify the fallback. Keep existing support in force until the user chooses otherwise. Treat ordinary dependency range edits and local migrations as part of the upgrade.

## Apply and verify in batches

1. Update tightly coupled packages together when their versions must move in step. Keep unrelated breaking upgrades in separate batches and group compatible routine updates when failures will still be easy to isolate. Account for the team's documented dependency holds and policies. Use the project's package manager or build wrapper with its configured sources and version policy. Update authoritative declarations and let the manager generate lockfile changes. Review the resolved graph and investigate unexpected packages, registries, or unrelated changes before accepting the batch.
2. Make the smallest migration that preserves supported behavior. Update affected source, tests, and configuration, including matching versions in CI or containers when they must move with the dependency. Apply only upstream migration steps relevant to the repository. Inspect any migration tool and its effects before running it. Follow existing project verification and lifecycle requirements.
3. Verify each batch by resolving or installing the expected versions and running the project checks that cover affected code or behavior. Use relevant build, type, unit, and integration checks from the repository or CI. Exercise paths affected by changes to runtime behavior, data, or integrations where the existing fast checks cannot cover them. Run the relevant combined checks once all successful batches are in place.
4. Diagnose a failed batch against the baseline. Fix in-scope migration issues, split the batch to isolate failures, or retry with a coupled dependency if the evidence warrants it. Restore only that batch's failed edits before retrying, keeping earlier successful batches and user changes. If the latest stable release remains blocked, try the next highest viable stable candidate within the authorized range. If no candidate can be verified, retain the baseline for that dependency, report what blocked it, and continue independent work. Never bypass resolver constraints, integrity checks, or required project checks to obtain a newer version.

## Report and self-check

- Report the old and final resolved versions, significant migration edits, and the checks that ran and their outcomes. Distinguish verified upgrades, unavailable verification, and dependencies already current.
- For dependencies held below the latest stable version, report the latest known target, the specific blocker, and the highest verified result or retained version. Keep upstream availability distinct from local resolution and successful verification.
- Confirm that major updates were considered within scope, each retained batch has matching declarations and lockfiles where the project uses them, and existing support commitments and unrelated work were preserved. Commit, push, publish, or make other external changes only when separately authorized.
