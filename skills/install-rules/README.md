# Install Rules

**Status**: validated

## What it does

Installs rules (passive constraints for AI behavior) from a source into an editor’s rules directory. Supports this project’s `rules/` or a user-specified Git repo. Writes Cursor `.mdc` files to `.cursor/rules/`. Trae IDE support is planned; currently Cursor only.

## When to use

- Install this repo’s rules into the current project’s Cursor rules
- Install rules from another Git repo (owner/repo, optional branch and subpath)
- Bootstrap: after cloning a rule-providing repo, install its rules into the workspace

## Inputs

- Source: default this project `rules/`, or Git `owner/repo` with optional branch and subpath (e.g. `rules`, `docs/rules`)
- Target: Cursor (Trae not yet supported)
- Optional: rule subset or “all”; project-level vs user-level destination

## Outputs

- Before install: list of installable rules (name, description/scope)
- After install: installed rule names, target path, conversion notes, any failures (per SKILL Appendix: Output contract)

## Scores (ASQM)

| Dimension      | Score |
| :---           | :---  |
| agent_native   | 5     |
| cognitive      | 4     |
| composability  | 5     |
| stance         | 5     |
| **asqm_quality** | 19   |

## Ecosystem

| Field | Value |
| :--- | :--- |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:discover-skills |
| market_position | differentiated |

## Full definition

See [SKILL.md](./SKILL.md) for complete behavior, restrictions, and examples.
