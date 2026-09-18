# CLAUDE.md

A briefing for Claude Code working in this repository.

## What this repository is

Mostly a markdown asset library: skills, protocols, rules and specs. **NEVER** try `npm test` / `npm run build` — there is no `package.json`, and no JavaScript toolchain to reach for.

There is plenty to run, just not with npm. `scripts/` holds the checkers and their tests, CI runs them on every pull request, and [CONTRIBUTING.md](CONTRIBUTING.md) says which to run for which kind of change. Run them before opening one.

The working tree is `skills/`, `protocols/`, `rules/` and `specs/` in markdown, plus `scripts/` and `tests/fixtures/` in Python.

## Where to go next

- **The execution contract, required reading**: [AGENTS.md](AGENTS.md) — load order, skill matching, failure handling, precedence
- **How to contribute**: [CONTRIBUTING.md](CONTRIBUTING.md) — forking, PRs, version numbers
- **Terminology**: [docs/architecture/terminology.md](docs/architecture/terminology.md) — the definitions and boundaries of the 4 asset types
- **Naming**: [docs/architecture/asset-naming.md](docs/architecture/asset-naming.md) — the naming formula and examples for each of the 4 asset types

## Traps Claude Code falls into here

- Skills follow the [agentskills.io](https://agentskills.io) standard format. This repository no longer maintains a private spec — there is no `agent.yaml`, no `manifest.json`, no `specs/skill.md`
- After editing a SKILL.md, the only registry to update is `skills/INDEX.md` — and it is generated, so run `python3 scripts/sync-skills-index.py` rather than editing it. The indexes under `rules/`, `specs/` and `protocols/` are hand-maintained; a new file there means a new row by hand
- Older ADRs and CHANGELOG entries describe mechanisms that have since been deleted — manifest, agent.yaml, artifact-contract, Stage 0 Norms Resolution and others. Mind the timeline as you read, and do not go looking for files those descriptions name
