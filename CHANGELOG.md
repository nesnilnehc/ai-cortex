# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `scripts/generate-skillgraph.mjs` — auto-generate `skills/skillgraph.md` from manifest and SKILL frontmatter; includes global overview
- `scripts/generate-scenario-map.mjs` — auto-generate `skills/scenario-map.md` from `skills/scenario-map.json`
- `scripts/generate-skills-docs.mjs` — wrapper to run both generators
- `skills/scenario-map.json` — source of truth for scenario-to-skill mapping (edit this, not scenario-map.md)

### Changed

- `skills/skillgraph.md` — now auto-generated; adds global overview section (Code Review, Lifecycle, Onboarding, Governance, Standalone)
- `skills/scenario-map.md` — now auto-generated from scenario-map.json
- `scripts/verify-registry.mjs` — runs generate-skills-docs before validation; validates scenario-map.json skill refs
- `spec/skill.md` §9 — documents generation; scenario-map source is now scenario-map.json

## [2.1.0] - 2026-03-06

### Added

- `execution-alignment` skill — post-task traceback, drift detection, and top-down calibration
- `docs/requirements-planning/` and `docs/architecture/` — minimal scaffolding; point to goals, roadmap, milestones
- `documentation-readiness` skill — documentation evidence assessment and minimal-fill plan
- `project-cognitive-loop` skill — orchestrate governance cycles (requirements, design, alignment, docs)
- `skills/scenario-map.md` — scenario-to-skill mapping for task-based discovery
- `agent.yaml` and README for execution-alignment, documentation-readiness, project-cognitive-loop
- `analyze-requirements` skill (v1.0.0) — transform vague intent into validated requirements
- I/O schema contracts for 7 previously missing skills
- Verification script enhancements: agent.yaml/README.md existence, related_skills validity, marketplace.json sync
- CHANGELOG.md

### Changed

- `skillgraph.md` — added project governance loop (analyze-requirements → brainstorm-design → execution-alignment → documentation-readiness → project-cognitive-loop)
- `project-cognitive-loop` — single-artifact output rule; Recommended Next Tasks (owner, scope, rationale); no separate outputs from routed skills
- `analyze-requirements` default output path to `docs/requirements-planning/` (keeps `docs/requirements/` compatible)
- Curate Skills audit: ASQM_AUDIT §6.5, §7; run-repair-loop README status and scores normalized
- Graduated `run-automated-tests` and `run-repair-loop` from experimental (v0.1.0) to stable (v1.0.0)
- Upgraded `schemas/skill-metadata.json` to spec v2.2.0 (added `input_schema`/`output_schema` fields)
- Updated CI workflow version references from spec v2.0.0 to v2.2.0

### Removed

- Stale `.agents/skills/commit-work/` fork (canonical version lives in `skills/commit-work/`)

### Fixed

- ASQM audit coverage gap (7 unscored skills)
- Roadmap acceptance criteria checkboxes now reflect actual completion status
- 7 markdownlint issues in `skills/analyze-requirements/SKILL.md` (MD032, MD040)

## [2.0.0] - 2026-03-02

### Added

- Spec v2.0.0 → v2.2.0: Core Objective structure, I/O contract protocol, Scope Boundaries flexibility
- `brainstorm-design` skill — structured dialogue for design validation
- `commit-work` skill (v2.0.0) — Conventional Commits with pre-commit quality checks
- `review-typescript` skill — TypeScript/JavaScript language review
- `review-react` skill — React framework review
- `onboard-repo` orchestrator skill — end-to-end repository onboarding
- `review-orm-usage` skill — ORM usage pattern review
- `review-testing` cognitive skill — test existence, coverage, quality
- Spec verification infrastructure (`verify-skill-structure.mjs`, `schemas/skill-metadata.json`)
- CI workflows (`pr-check.yml`, `audit.yml`)
- `CONTRIBUTING.md` and GitHub Issue templates (bug, feature, new-skill)
- Evolution roadmap (`docs/designs/2026-03-02-ai-cortex-evolution-roadmap.md`)
- INDEX.md Stability column (experimental / stable / mature)

### Changed

- All 33 skills migrated to spec v2 structure (Core Objective, Success Criteria, Acceptance Test)
- `review-code` orchestrator updated to v2.6.0 (added review-testing to cognitive chain)
- Plugin selection criteria formalized (ASQM >= 18, standalone value)

## [1.0.0] - 2026-02-14

### Added

- 26 canonical skills across review, documentation, automation, and meta-skill categories
- `review-code` orchestrator (v2.5.0) with scope → language → framework → library → cognitive chain
- 15 review skills: diff, codebase, dotnet, java, go, php, powershell, python, sql, vue, security, architecture, performance
- `curate-skills` — ASQM scoring and lifecycle management
- `discover-skills` — skill discovery and recommendation
- `decontextualize-text` — privacy-preserving text generalization
- `generate-standard-readme` — standardized README generation
- `generate-github-workflow` — GitHub Actions workflow generation
- `refine-skill-design` — skill audit and optimization
- `write-agents-entry` — AGENTS.md authoring
- `install-rules` — rule installation for Cursor and Trae
- `bootstrap-project-documentation` — project documentation scaffolding
- `run-automated-tests` and `run-repair-loop` (experimental)
- ASQM audit framework with 4-dimension scoring
- `manifest.json` machine-readable registry
- `skills/INDEX.md` canonical catalog with tagging system
- `skillgraph.md` code review composition graph
- Claude Plugin integration (`.claude-plugin/marketplace.json`)
- 7 rules for coding standards, writing norms, and workflow policies

### Changed

- Rebranded from llm-skills to AI Cortex
- Adopted entry-file-driven contract (`AGENTS.md`)
- Consolidated to skills-only catalog (removed commands and obsolete specs)

## [0.1.0] - 2026-01-23

### Added

- Initial repository with decontextualization skill
- README, LICENSE (MIT), basic project structure

[Unreleased]: https://github.com/nesnilnehc/ai-cortex/compare/v2.1.0...main
[2.1.0]: https://github.com/nesnilnehc/ai-cortex/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/nesnilnehc/ai-cortex/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/nesnilnehc/ai-cortex/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/nesnilnehc/ai-cortex/releases/tag/v0.1.0
