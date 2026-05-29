# Changelog

## [Unreleased] — 2026-05-15

### Added
- `specs/requirement-modeling.md`: mandatory 「目标」(Objective) body section — requirement-level outcome statement, distinct from upstream goals (referenced via `parent`)
- `specs/requirement-modeling.md`: conditionally-mandatory 「业务规则」(Business Rules) section with escalation triggers (rule-set-as-deliverable / one rule cited by ≥2 ACs / state machine / compliance SSOT); §5.3 declarative-form rules + rule↔AC boundary
- `specs/requirement-modeling.md` §1: explicit acceptance-criteria-centric content philosophy
- `bin/cortex` POSIX sh script: 5 subcommands (install / update / clean / status / uninstall) for cross-IDE asset management
- Codex-compatible skill sync via per-skill symlinks under `~/.agents/skills/<skill>`
- `docs/adr/0010-installation-strategy.md`: decision record for XDG canonical path + bin/cortex strategy
- `rules/*.md`: added `recommended_scope` field and standardized `# Rule: ...` H1 titles to all 12 rules files

### Changed
- `specs/requirement-modeling.md`: v3.0.0 → v4.0.0 (BREAKING — new mandatory 目标 section makes prior requirements non-compliant); id `_V3` → `_V4`
- `rules/requirement-quality.md`: 7 → 8 mandatory fields (added 目标); conditional 业务规则 completeness + rule↔AC traceability checks; v1.0.0 → v2.0.0
- `README.md` §安装与使用: replaced IDE-specific prompt blocks with `git clone` + `cortex install` quickstart
- `AGENTS.md` §2: added canonical install path reference for Agent direct access

### Removed
- Vercel `skills` CLI as recommended install path (now superseded by `cortex install`; existing Vercel CLI installs remain compatible via coexistence mode)
