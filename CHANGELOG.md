# Changelog

## [Unreleased] — 2026-05-15

### Added
- `specs/functional-design-modeling.md` + `rules/functional-design-quality.md`: new business/product-facing design spec (artifact_type `functional-design`) — functional modules, business workflow, exceptions, with conditional state-diagram & permission-matrix sections
- `specs/technical-design-modeling.md` + `rules/technical-design-quality.md`: new engineering-facing design spec (artifact_type `technical-design`) — architecture, components, database, API contracts, tech selection
- `specs/requirement-modeling.md`: mandatory 「目标」(Objective) body section — requirement-level outcome statement, distinct from upstream goals (referenced via `parent`)
- `specs/requirement-modeling.md`: conditionally-mandatory 「业务规则」(Business Rules) section with escalation triggers (rule-set-as-deliverable / one rule cited by ≥2 ACs / state machine / compliance SSOT); §5.3 declarative-form rules + rule↔AC boundary
- `specs/requirement-modeling.md` §1: explicit acceptance-criteria-centric content philosophy
- `bin/cortex` POSIX sh script: 5 subcommands (install / update / clean / status / uninstall) for cross-IDE asset management
- Codex-compatible skill sync via per-skill symlinks under `~/.agents/skills/<skill>`
- `docs/adr/0010-installation-strategy.md`: decision record for XDG canonical path + bin/cortex strategy
- `rules/*.md`: added `recommended_scope` field and standardized `# Rule: ...` H1 titles to all 12 rules files

### Changed
- Split the `design` artifact into `functional-design` + `technical-design` along the business/engineering audience boundary. Chain is now sequential + conditional: `requirement → functional-design → technical-design → task` (functional layer skippable for pure-tech work; `technical-design.parent` is polymorphic over functional-design|requirement; `task.parent` always technical-design)
- `specs/task-modeling.md`: `parent` retargeted to technical-design; v2.0.0 → v2.1.0
- `specs/requirement-modeling.md` (→ v4.0.1) / `specs/test-case-modeling.md` (→ v1.0.1) / `specs/spec-modeling.md` (→ v2.0.1): repointed design-modeling references to the new split specs
- `docs/ARTIFACT_NORMS.md`: replaced `design` artifact_type with `functional-design` + `technical-design` (canonical-source / path / timestamp tables)
- `docs/designs/*`: migrated 2 existing design docs to `artifact_type: technical-design` and renamed to the `-technical-design.md` suffix
- `specs/requirement-modeling.md`: v3.0.0 → v4.0.0 (BREAKING — new mandatory 目标 section makes prior requirements non-compliant); id `_V3` → `_V4`
- `rules/requirement-quality.md`: 7 → 8 mandatory fields (added 目标); conditional 业务规则 completeness + rule↔AC traceability checks; v1.0.0 → v2.0.0
- `README.md` §安装与使用: replaced IDE-specific prompt blocks with `git clone` + `cortex install` quickstart
- `AGENTS.md` §2: added canonical install path reference for Agent direct access

### Removed
- `specs/design-modeling.md` + `rules/design-quality.md`: superseded by the functional/technical design split
- Vercel `skills` CLI as recommended install path (now superseded by `cortex install`; existing Vercel CLI installs remain compatible via coexistence mode)
