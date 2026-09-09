# CLAUDE.md

A briefing for Claude Code working in this repository.

## What this repository is

Not a code project: a markdown asset library of skills, protocols, rules and specs. **Do not** try `npm test` / `npm run build` / `npm run verify` — this repository's `package.json` has an empty `scripts`, and there is nothing to run.

The working tree is `skills/`, `protocols/`, `rules/` and `specs/`, and a change here means editing markdown.

## Where to go next

- **The execution contract, required reading**: [AGENTS.md](AGENTS.md) — load order, skill matching, failure handling, precedence
- **How to contribute**: [CONTRIBUTING.md](CONTRIBUTING.md) — forking, PRs, version numbers
- **Terminology**: [docs/architecture/terminology.md](docs/architecture/terminology.md) — the definitions and boundaries of the 4 asset types
- **Naming**: [docs/architecture/asset-naming.md](docs/architecture/asset-naming.md) — the naming formula and examples for each of the 4 asset types

## Traps Claude Code falls into here

- Skills follow the [agentskills.io](https://agentskills.io) standard format. This repository no longer maintains a private spec — there is no `agent.yaml`, no `manifest.json`, no `specs/skill.md`
- After editing a SKILL.md, the only registry to update is `skills/INDEX.md`; there is no other
- Older ADRs and CHANGELOG entries describe mechanisms that have since been deleted — manifest, agent.yaml, artifact-contract, Stage 0 Norms Resolution and others. Mind the timeline as you read, and do not go looking for files those descriptions name
