# AI Cortex 0.6.0

Select and upgrade stable releases with `cortex upgrade`, while `cortex update`
continues to follow origin's default branch. This is an additive installer release;
it does not declare 1.0 readiness or change independent asset versions.

## What changed

- `cortex upgrade` selects the highest numeric stable `vMAJOR.MINOR.PATCH` tag on
  origin. `cortex upgrade 0.6.0` selects an explicit version, with an optional `v`.
  Prerelease/build labels, malformed versions and local-only tags are excluded.
- Upgrade requires a clean existing clone, validates required release files, then
  selects a detached checkout and resynchronizes managed assets. Local tags and
  branch commits are retained. Previously fetched release tags that change on
  origin are rejected.
- Default-branch update now correctly falls back to main when the local origin
  HEAD reference is absent. Its existing update and force behavior is retained.
- The approved 1.0 preparation policy documents the bounded core, experimental
  capabilities, compatibility/deprecation rules and future latest-stable support.
  Current 0.x security support still targets main; 1.0 acceptance remains open.

## Upgrade from 0.5.1 or an older installation

Older installers do not contain `upgrade`. Preserve local edits first and use a
clean canonical clone. For the default installation path:

```sh
cortex_checkout="$HOME/.local/share/ai-cortex"
git -C "$cortex_checkout" fetch origin refs/tags/v0.6.0:refs/tags/v0.6.0
git -C "$cortex_checkout" checkout --detach v0.6.0
sh "$cortex_checkout/bin/cortex" install
```

Change the path for a custom clone. This bootstrap selects the release explicitly
instead of using main. Once installed, `cortex upgrade` chooses the newest stable
origin tag; an explicit version is not a persistent channel preference. The command
uses Git tags, not GitHub's latest Release API, and does not verify signatures.
No consuming-project document or configuration migration is required.

## Rollback and recovery

Retain the 0.6.0 manager outside the clone before selecting an older release:

```sh
cortex_manager_dir=$(mktemp -d "$HOME/.local/share/cortex-manager.XXXXXX")
cp "$cortex_checkout/bin/cortex" "$cortex_manager_dir/cortex"
CORTEX_HOME="$cortex_checkout" sh "$cortex_manager_dir/cortex" upgrade v0.5.1
```

Use that retained manager for subsequent upgrade, install or uninstall while
pinned to old code. The installed command still points at the selected clone's
installer, which may lack `upgrade` or earlier ownership fixes. `cortex update`
leaves a release pin and follows the default branch.

Installation is nontransactional. A failure after checkout can leave source and
installed assets out of sync; resolve the filesystem error and rerun the retained
manager's `install`. Fetched objects/private release refs may remain after a
pre-checkout failure. Asset rollback does not undo consuming-project edits or
remote state. Do not rewrite release tags to recover.

The [recovery guide](https://github.com/nesnilnehc/ai-cortex/blob/v0.6.0/docs/guides/installer-recovery.md)
has the full ownership, pinning and failure boundaries.

## Verification

All 29 permanent installer integration tests pass locally; the implementation's
Linux/macOS CI also passed. Coverage includes stable and explicit version
selection, dirty/missing/invalid targets, remote failure, moved tags, incomplete
release trees, resynchronization and continuity with main-following update.
These tests verify CLI/Git behavior in isolated homes, not invocation in running
IDEs. Host acceptance and broader consumer evidence remain 1.0 readiness work.
