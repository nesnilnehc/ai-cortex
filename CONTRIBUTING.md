# Contributing to AI Cortex

Thank you for your interest in contributing to AI Cortex. This document explains how to contribute skills, rules, and improvements.

## Quick Start

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-skill-name`
3. Make your changes following the guidelines below
4. Run verification: `npm run verify && node scripts/verify-skill-structure.mjs`
5. Submit a Pull Request

## Adding a New Skill

All skills must conform to the [Skill Specification](spec/skill.md). The quality assurance process is:

1. **Create draft**: Write `skills/<skill-name>/SKILL.md` following the spec
2. **Add supporting files**: Create `README.md` and `agent.yaml` in the skill directory
3. **Register**: Add the skill to `manifest.json` (`skills/INDEX.md` is generated)
4. **Verify**: Run `node scripts/verify-registry.mjs && node scripts/verify-skill-structure.mjs`
5. **Submit PR**: The CI will automatically verify registry sync and skill structure

### Skill Checklist

- [ ] Directory name is `kebab-case` and matches the YAML `name` field
- [ ] YAML metadata includes all required fields (name, description, tags, version, license)
- [ ] All required headings present (Purpose, Core Objective, Use Cases, Behavior, Input & Output, Restrictions, Self-Check, Examples)
- [ ] Core Objective has Primary Goal, Success Criteria (3-6 items), and Acceptance Test
- [ ] Self-Check aligns with Success Criteria
- [ ] Skill Boundaries section defines what the skill does NOT handle
- [ ] At least 2 examples (one edge case)
- [ ] `skills/INDEX.md` regenerated from manifest and frontmatter
- [ ] `manifest.json` updated with the new capability
- [ ] `verify-registry.mjs` and `verify-skill-structure.mjs` pass

### Naming Convention

Use `verb-noun` format (e.g. `review-typescript`, `generate-standard-readme`). For review skills, follow the existing pattern:

- Language: `review-<language>` (e.g. `review-python`)
- Framework: `review-<framework>` (e.g. `review-react`)
- Library: `review-<domain>-usage` (e.g. `review-orm-usage`)
- Cognitive: `review-<concern>` (e.g. `review-security`)

## Adding a New Rule

Rules go in the `rules/` directory and must be registered in `rules/INDEX.md`. Follow the existing rule format. Install rules into Cursor using the `install-rules` skill.

## Versioning

This project follows [Semantic Versioning](https://semver.org/). When modifying a skill:

- **PATCH** (e.g. 1.0.0 → 1.0.1): Typos, metadata tweaks, reference updates
- **MINOR** (e.g. 1.0.0 → 1.1.0): New steps, improved examples, interaction policy changes
- **MAJOR** (e.g. 1.0.0 → 2.0.0): Breaking structural changes

Update the version in SKILL.md YAML front-matter, then regenerate `skills/INDEX.md`.

## Code of Conduct

Be professional, constructive, and respectful. Focus on the technical merits of contributions.

## Questions?

Open an issue with the "question" label or check the [skill catalog](skills/INDEX.md) for existing capabilities.
