# AI Cortex 0.5.1

Installation now preserves user-owned links and restores the selected asset set
more reliably when rolling back. This patch keeps the 0.5.0 asset contracts and
independent asset versions unchanged.

## What changed

- Foreign skill and rule links, including broken links, survive installation and
  uninstall. Similar path prefixes and traversal paths no longer imply ownership.
- Cursor rule generation preserves foreign links and recognizes generated files
  only by the exact first-line marker.
- Reinstalling prunes obsolete managed assets, so switching to an older asset set
  does not leave stale links or globally installed rules behind.

## Upgrade

Preserve local edits before updating the canonical installation. From a clean
installation, `cortex update` follows the remote default branch. To pin this patch,
fetch the tags, select `v0.5.1` in the canonical clone, and run its `bin/cortex install`.
Use the actual clone path when it differs from the default.

No consuming-project document migration is required. User-owned conflicts are
reported and preserved; move them explicitly only when you want Cortex to own
that installation path. Installation is not transactional.

## Rollback

Keep a copy of the 0.5.1-or-newer installer outside the clone before checking out
an older tag. Older tags also restore the older installer and its defects. Use the
retained manager with an explicit `CORTEX_HOME` to reinstall the selected old asset
set, and keep using that manager while pinned to the old tag.

The [recovery guide](https://github.com/nesnilnehc/ai-cortex/blob/v0.5.1/docs/guides/installer-recovery.md)
contains the complete commands, verification steps and uninstall procedure.
Asset rollback does not undo edits to consuming projects or remote pages.

## Verification

The 22 permanent installer integration tests pass locally and in CI on Linux and
macOS. A separate local check restored actual 0.5.0 assets to 0.4.0 using the retained
fixed installer and verified exact installed membership and no broken managed
links. These checks verify installed files, not runtime invocation inside IDEs.
