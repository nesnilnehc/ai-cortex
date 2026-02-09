# AI Cortex

[![Version: 2.0.0](https://img.shields.io/badge/Version-2.0.0-blue.svg)](.)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![AI-Readiness: High](https://img.shields.io/badge/AI--Readiness-High-success.svg)](llms.txt)
[![Stability: Stable](https://img.shields.io/badge/Stability-Stable-orange.svg)](#positioning)

AI Cortex is an agent-first, governance-ready inventory of Skills. Specs turn Skills into reusable, composable engineering assets.

---

## ✨ Features

- **Standardized skill assets**: `spec/skill.md` defines structure, metadata, and quality requirements.
- **Discoverable catalog**: `skills/INDEX.md` and `manifest.json` provide stable indexes and metadata.
- **Agent entry contract**: `AGENTS.md` defines identity, authoritative sources, and behavior.
- **Ecosystem compatibility**: Works with [skills.sh](https://skills.sh) and [SkillsMP](https://skillsmp.com).

---

## 📦 Installation

Use the [skills.sh](https://skills.sh) CLI to install into Claude Code, Cursor, Codex, and similar:

```bash
npx skills add nesnilnehc/ai-cortex
```

Add `--force` to overwrite existing installation when reinstalling or updating:

```bash
npx skills add nesnilnehc/ai-cortex --force
```

Install only specific skills:

```bash
npx skills add nesnilnehc/ai-cortex --skill review-code --skill generate-standard-readme
```

---

## Positioning

This repository is the capability-asset library: it hosts Skills and provides Specs and the entry contract.

### Core principles

- **Contract-first**: Structure, metadata, and quality are defined under `spec/`.
- **Verifiable**: Self-Check is the minimum delivery guarantee.
- **Composable**: `related_skills` supports reuse from atomic capabilities to workflows.
- **Discoverable**: `INDEX.md` and `manifest.json` provide stable indexes and metadata.

### Boundaries (out of scope)

- Does not provide IDE/Agent/CI integration or usage guides, or install/sync scripts.
- Does not tie to any single IDE or runtime; no vendor-specific adapters.
- Does not implement model invocation, tool execution, or runtime orchestration infrastructure.

### Catalog scope

- **Canonical catalog**: Skills under `skills/` are the published capability list; `skills/INDEX.md` and `manifest.json` are the authoritative indexes.
- **Local or IDE-specific skills**: `.agents/` may hold skills used only in this repo or by a specific IDE; they are not part of the canonical catalog and are not listed in INDEX or manifest.
- **Subset lists**: `.claude-plugin/` and `llms.txt` list a subset of skills for Claude Plugin and LLM index respectively; update them when adding or promoting high-priority skills.

---

## 🤝 Contributing

Submit PRs that follow the [skill spec](spec/skill.md). Capability index: [skills/INDEX.md](skills/INDEX.md). When adding or moving a skill, update both `skills/INDEX.md` and `manifest.json`, then run `node scripts/verify-registry.mjs` to confirm they stay in sync.

---

## 📄 License

[MIT](LICENSE)
