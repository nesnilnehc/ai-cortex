# Changelog

## [Unreleased] — 2026-05-15

### Added
- `bin/cortex` POSIX sh script: 5 subcommands (install / update / clean / status / uninstall) for cross-IDE asset management
- Codex-compatible skill sync via per-skill symlinks under `~/.agents/skills/<skill>`
- `docs/adr/0010-installation-strategy.md`: decision record for XDG canonical path + bin/cortex strategy
- `rules/*.md`: added `recommended_scope` field and standardized `# Rule: ...` H1 titles to all 12 rules files

### Changed
- `README.md` §安装与使用: replaced IDE-specific prompt blocks with `git clone` + `cortex install` quickstart
- `AGENTS.md` §2: added canonical install path reference for Agent direct access

### Removed
- Vercel `skills` CLI as recommended install path (now superseded by `cortex install`; existing Vercel CLI installs remain compatible via coexistence mode)
