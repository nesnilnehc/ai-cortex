---
artifact_type: technical-design
lifecycle: snapshot
created_at: 2026-10-21
parent: ../process-management/backlog/2026-10-20-roadmap-capabilities.md
status: draft
---

# Blank roadmap generation and conversation regression

## Goal

Implement the structure-before-content contract with an executable blank generator,
a retained six-document layout and multi-turn regression. This is local CLI/test
work; no visual interaction or UI design is introduced.

## Architecture and service decomposition

The existing renderer validates and renders facts. Blank generation reads clean
local templates and accepts no business input. Schema 1.6 extends 1.5 with the
retained `topic-split` layout; 1.0–1.5 retain their original layout contract.
A separate conversation runner receives model action decisions, executes the real
renderer in a temporary workspace, and evaluates trajectories and resulting files.
The model adapter is replaceable; renderer and oracle are never mocked.

## Components and detailed design

- `blank_documents(locale)` produces six Markdown strings from bundled templates.
- `topic_documents(data)` preserves supplied records in main plus five topics;
  optional phase/flow details remain in planning basis rather than being dropped.
- `write_topic_outputs(...)` preflights all reserved paths and records generated
  file digests in `.roadmap-outputs.json`. Only intact owned stale files may be
  deleted; unrelated files and modified stale files are preserved.
- The conversation adapter proposes `blank`, `review`, `populate` or `ask` per
  turn. The runner invokes the production renderer for generation. A forbidden
  proposal is a failed trajectory, never a remote operation.

## Database design

No database. JSON fixtures carry versioned multi-turn user inputs, scripted replay
choices and per-turn expected constraints. Temporary snapshots and reports are test
artifacts, not another editable project plan.

## Interface contracts

`--blank [--locale en|zh-CN] [--layout topic-split] --output-dir DIR` accepts no
positional input. `--blank --check` writes nothing. Populated six-document output
requires schema 1.6 and a retained `selection.layout=topic-split`. Existing CLI
layouts remain supported. `--overwrite` is explicit; repeat identical generation
preserves file bytes and modification times.

The conversation runner defaults to deterministic scripted replay. `--eval` is an
explicit live-model mode using the installed Codex CLI built-in defaults with user
configuration disabled; authentication still uses the normal Codex account.
The live adapter receives complete conversation history and skill/rule/spec context,
returns JSON actions, and runs read-only without tools; the host executes only local
renderer operations. Model invocations are sequential and bounded by timeout.

## Data flow and error handling

Validate input and preflight all paths before writes. Reject business input in
blank mode, selection conflicts, symlinks, hardlink aliases, invalid manifests and
modified stale outputs. I/O failure remains a nonzero result with the existing
partial-output warning. No transactional filesystem guarantee is claimed.
The oracle checks every turn's action, review scope, file count, blankness,
no-write turns, source-state preservation and unrelated-file preservation.
Infrastructure/model/schema errors are failures, not skipped or successful evals.

## Technology choices and trade-offs

Python standard library only. Live evaluation is opt-in and never runs in unit CI.
Replay gives deterministic renderer/trajectory regression; it does not measure model
intent recognition. Live evaluation supplies that distinct evidence. No LLM judge
or exact response wording is needed for this bounded action/trace contract.

## Test strategy

New behavior follows red/green tests. Fixtures cover structure confirmation,
formatting feedback, repeated review, authorized population, reset to empty and
missing facts, English/Chinese turns, empty input and absent source. Negative controls seed premature population, publication proposals,
false full-pass claims, source changes and leaked author guidance. Each must fail.

## Quality attribute design

File effects are limited to a temporary workspace in tests. The production writer
preserves unrelated files and rejects unsafe aliases before writing. Live logs
report adapter/model metadata without printing credentials. User-facing provider
errors are summarized, and test output remains local. Existing renderer outputs
are regression-tested for compatibility.

## Acceptance criteria

- G1: Blank generation creates six clean linked documents without business input.
- G2: Schema 1.6 retains six-topic output and supplied business facts in both locales.
- G3: Invalid requests and unsafe paths fail before mutation; repeated output is stable.
- G4: Only intact owned stale assets are removed; unrelated work survives transitions.
- G5: Multi-turn replay executes the renderer and detects forbidden or drifting behavior.
- G6: Explicit live eval uses actual model decisions and reports failures separately.
- G7: Existing skills select structure-only, content-on-settled-structure or continuous work; confirmation alone does not authorize population, and review scope is independent of populated files, including business review of a blank draft.

The ownership path also handles authorized transitions from topic layout back to
single/split; unowned stale reserved files fail before writing. Blank validation
checks the emitted structure. Topic output retains phase owners, flow board links,
timing conventions and the complete-history authority link.

Evidence export checks golden actions, scope and actual recorded stage/execution
independently of pass flags. Report provenance includes templates, the locale
catalog, both source input fixtures and the selected per-turn timeout.
