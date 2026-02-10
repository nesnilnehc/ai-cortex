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
- **Rules for AI behavior**: `rules/` provides coding standards, writing norms, and workflow policies; install via the install-rules skill or manually.
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

### Rules

Rules are passive constraints for AI behavior (coding standards, writing norms, workflow policies). Install them into Cursor or Trae so the Agent respects them in your workspace.

**Option A — via the install-rules skill** (recommended): After installing this project, ask your Agent to install rules. Use the prompt that matches your scenario:

| Scenario | Prompt |
| :--- | :--- |
| You are inside this repo (ai-cortex) | “Install this project’s rules into Cursor” |
| You are in another project and want ai-cortex rules | “Install rules from nesnilnehc/ai-cortex to my Cursor rules” |

The [install-rules](skills/install-rules/SKILL.md) skill lists available rules, asks for confirmation, and writes to Cursor (`.cursor/rules/` `.mdc` files) or Trae (`.trae/project_rules.md` concatenated Markdown). You can install all rules or a subset.

**Option B — manual copy**: Copy from `rules/` to `.cursor/rules/` (convert to `.mdc` with frontmatter per Cursor format) or to `.trae/project_rules.md` (concatenate as Markdown sections). See [rules/INDEX.md](rules/INDEX.md) for the rule registry.

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
