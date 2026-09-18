# Release notes

## 0.3.0 — 2026-09-18

A minor release. It adds a tenth engineering Rule set and the reviewer that runs it, so `orchestrate-code-review` now has a seventh cognitive step. Nothing you already adopted changes its obligations, but one rule you may have copied from now points at two of them instead of stating them.

### Added

- **A Rule set for where a defect is decided and whether the failure can be acted on.** `error-surfacing-quality`, prefix ERR, six items: decide untrusted input at the boundary it enters, stop once an invariant is known broken, detect at the earliest layer your project declares, and give a person the next action or a program a stable identifier. Two items are `major`, four are `minor`.

- **`review-error-surfacing` runs it**, and joins `orchestrate-code-review` as a seventh cognitive step. If you invoke the orchestrator, it runs without any change on your side. The Rule is project-scoped, so it stays in the canonical clone and loads on demand.

- **Its sixth item is about your check suite, not your code.** A check whose findings are mostly legitimate use must be narrowed, retargeted or withdrawn rather than left for readers to filter — a report that is mostly legitimate teaches its readers to skim. It needs a declared threshold to run, so it stays inactive until you set one.

- **Two project parameters, both optional.** `error.detection_layers` lists the layers your project can decide a defect at, earliest first. `error.false_positive_threshold` is the share of a check's findings that may be legitimate use before the check must be narrowed. Leave either unset and only its own item is unevaluable; the baseline items still run.

- **A maintainer guide for releasing this repository**, at `docs/guides/releasing.md`. Relevant if you maintain a fork.

### Changed

- **`standards-coding` points at two obligations instead of stating them.** Its error-handling constraint had carried "fail fast" and "messages carry context and a suggested resolution"; those are now `error-surfacing-quality`'s, defined precisely enough to waive. Its simplicity constraint had carried "keep no commented-out dead code"; that is `architecture-quality` ARC-010's. What stays is what only this document says: one consistent error-handling mechanism, and resources released on the error path.

  Worth knowing if you install user-scoped rules only. `standards-coding` is user-scoped and lands in your editor's rules directory, while both targets are project-scoped and load on demand — so you now get a pointer where you used to get the text.

### Upgrading

```bash
cortex update
```

Nothing to migrate, and nothing breaks. The new Rule set is additive, and its two `major` items only produce findings when you run a review that loads them.

If you want the new reviewer active in your own review runs, nothing is required: `orchestrate-code-review` dispatches it. If you want its two project parameters to do anything, declare them in `.ai-cortex/config.yaml`.

`cortex update` hard-resets the canonical clone onto `origin` and refuses to run on a dirty tree; keep local edits on a branch or a fork rather than in that clone.
