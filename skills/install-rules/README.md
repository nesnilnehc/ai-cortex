# Install Rules

**Status**: validated

## What it does

Installs rules (passive constraints for AI behavior) from a source into an editor’s rules destination. Supports this project’s `rules/` or a user-specified Git repo.

- Cursor: writes one `.mdc` file per rule to `.cursor/rules/`
- Trae IDE: writes a managed block to `.trae/project_rules.md` (or `.trae/user_rules.md`), without modifying content outside the block

## When to use

- Install this repo’s rules into the current project’s Cursor or Trae rules
- Install rules from another Git repo (owner/repo, optional branch and subpath)
- Bootstrap: after cloning a rule-providing repo, install its rules into the workspace

## Inputs

- Source: default this project `rules/`, or Git `owner/repo` with optional branch and subpath (e.g. `rules`, `docs/rules`)
- Target: Cursor or Trae
- Optional: rule subset or “all”; project-level vs user-level destination

## Outputs

- Before install: rule list, destination analysis summary, and a plan (`create/skip/conflict/update`)
- After install: executed actions, target path(s), conversion notes, and any failures (per SKILL Appendix: Output contract)

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
