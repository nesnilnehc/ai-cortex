# Release notes

## 0.2.1 — 2026-09-18

A patch release. One correction reaches a rule you may have copied from; everything else hardens this repository's own checks and does not change an asset you install.

### Fixed

- **`workflow-documentation` carried a regex that could not be copied.** The version-narration pattern contains a backtick and sat inside a single-backtick code span, where a backslash does not escape it — the span closed early and the rest rendered as prose. Anyone who copied that pattern got something that does not compile. It is written as a double-backtick span now, and all 35 patterns in that section compile.

### Changed

- **`workflow-documentation` says which of its patterns are enforced.** Part of its detection list runs in CI and part needs a reader, and the rule now states the split rather than leaving you to assume the whole list is automated. The Chinese conversational residue and heading suffixes are not automated because they match almost nothing; conversational shorthand is not, because the criterion excuses a shorthand that the document defines, and no grep can decide that.
- **Five rules take a patch bump**: `standards-coding` 1.0.2, `standards-import` 1.0.1, `standards-shell` 1.0.1, `writing-chinese-technical` 1.3.1, `workflow-documentation` 1.1.1. Four of them changed only in frontmatter, gaining the `artifact_type` and `status` their peers declare.

### Upgrading

```bash
cortex update
```

Nothing to migrate. No rule's obligations changed, so a project that adopted these rules needs no action beyond the update.

`cortex update` hard-resets the canonical clone onto `origin` and refuses to run on a dirty tree; keep local edits on a branch or a fork rather than in that clone.
