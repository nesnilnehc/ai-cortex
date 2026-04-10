# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Cortex is an agent-first, governance-ready inventory of AI skills for software delivery and project governance. It provides a four-layer asset library: Skills (active capabilities), Specs (data structures/contracts), Protocols (interaction flows), and Rules (passive constraints). See `specs/terminology.md` for canonical definitions.

## Commands

```bash
# Verify registry, manifest, and skill structure (the only CI check)
npm run verify

# Full validation as used in contributions
node scripts/verify-registry.mjs && node scripts/verify-skill-structure.mjs
```

There are no traditional unit tests. Validation is done through the verify scripts. CI runs `npm run verify` on Node 20 when skills, scripts, specs, or config files change.

## Architecture

### Four-Layer Governance Model

| Layer | Type | Directory | Registry |
|-------|------|-----------|----------|
| Skills | Active capabilities | `skills/` | `skills/INDEX.md`, `manifest.json` |
| Specs | Data structures, contracts | `specs/` | `specs/INDEX.md` |
| Protocols | Interaction flows | `protocols/` | `protocols/INDEX.md` |
| Rules | Passive constraints | `rules/` | `rules/INDEX.md` |

### Authority Chain (highest to lowest)

`AGENTS.md` > `specs/` > `protocols/` > `rules/` > `docs/`

### Skill Structure

Each skill lives in `skills/<skill-name>/` with three files:
- `SKILL.md` — Full spec with YAML frontmatter (name, description, tags, version, etc.)
- `agent.yaml` — Metadata, ASQM scoring, status, overlap detection
- `README.md` — Quick reference

### Key Registries

- `manifest.json` — Master registry with all capability paths, version (2.0.0), and remote discovery URLs
- `skills/INDEX.md` — Generated from manifest and skill frontmatter (do not hand-edit)
- `llms.txt` — Machine-readable agent loading order (MUST LOAD > SHOULD LOAD > DISCOVERY)

### Orchestration Pattern

- **Orchestrator skills** (e.g., `review-code`) run atomic skills in sequence and aggregate results
- **Atomic skills** are single-purpose with clear input/output contracts
- **Meta-skills** (e.g., `curate-skills`, `refine-skill-design`) govern other skills

## Conventions

- **Skill naming**: `verb-noun` kebab-case (e.g., `review-typescript`, `generate-standard-readme`)
- **Review skill naming**: `review-<language>`, `review-<framework>`, `review-<domain>-usage`, `review-<concern>`
- **Language policy**: Documentation content in Chinese; machine-readable fields (YAML keys, IDs, tags) in English
- **Versioning**: SemVer — PATCH for errata/metadata, MINOR for new steps/examples, MAJOR for breaking structural changes
- **Markdown linting**: `.markdownlint.json` — line length (MD013) disabled, duplicate headings allowed among siblings only

## Adding a New Skill

1. Create `skills/<skill-name>/` with `SKILL.md`, `agent.yaml`, `README.md`
2. Follow the structure defined in `specs/skill.md`
3. Register in `manifest.json` (INDEX.md is generated)
4. Run `npm run verify` to validate
5. Required sections in SKILL.md: Purpose, Core Objective, Use Cases, Behavior, Input & Output, Restrictions, Self-Check, Examples (at least 2, including one edge case)

## Important Files

- `AGENTS.md` — Agent behavior contract and entry point (read this first when acting as an agent in this repo)
- `specs/skill.md` — Canonical skill structure and quality requirements
- `specs/terminology.md` — Core term definitions (Spec, Protocol, Skill, Rule)
- `specs/artifact-contract.md` — Documentation artifact contract
- `docs/ARTIFACT_NORMS.md` — Documentation placement and naming rules
- `scripts/verify-registry.mjs` — Main validation script
