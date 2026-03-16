# Install Rules

**Status**: experimental

## What it does

Installs rules from a source repository into Cursor (`.cursor/rules/`) or Trae IDE (`.trae/project_rules.md`) with explicit user confirmation and conflict detection. Resolves the source (this project's `rules/` or a specified Git repo), lists installable rules, analyzes the destination state, builds a conservative install plan (`create/skip/conflict/update`), and only writes after the user approves the plan.

## When to use

- After cloning ai-cortex or another rule-providing repo: install its rules so the Agent respects them.
- Bootstrapping a new project with a standard rule set from a shared repository.
- Selectively adding or updating individual rules without overwriting existing configurations.

## Inputs

- Source: this project's `rules/` directory (default) or a Git repo (`owner/repo`, optional branch/ref and subpath).
- Target IDE: Cursor or Trae (or both).
- Scope: all rules or a subset by name.
- Destination: project-level (default) or user-level.

## Outputs

- Rule files written to IDE-specific destination (`.cursor/rules/*.mdc` or `.trae/` managed block).
- Post-install summary: executed actions, target paths, and any conversion notes or failures.

## Scores (ASQM)

| Dimension        | Score |
| :--------------- | :---- |
| agent_native     | 3     |
| cognitive        | 3     |
| composability    | 3     |
| stance           | 4     |
| **asqm_quality** | 13    |

## Ecosystem

| Field                                 | Value                                    |
| :------------------------------------ | :--------------------------------------- |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:discover-skills    |
| market_position                       | experimental                             |

## Promotion path

To reach **validated** (quality ≥ 17, agent_native ≥ 4): add a formal `Appendix: Output contract` table to SKILL.md documenting the post-install summary format machine-readably.

## Full definition

See [SKILL.md](./SKILL.md) for checklist, restrictions, and output contract.
