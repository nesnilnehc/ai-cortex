# Generate GitHub Workflow

**Status**: validated

## What it does

Produces GitHub Actions workflow YAML that satisfies the skill's Appendix A output contract. Security-first, minimal permissions, version pinning. For CI, release, PR checks. Supports Node, Python, Go, Rust; includes Go + Docker + GoReleaser appendix.

## When to use

- New project setup: add CI or PR-check workflows
- Unified standards: align workflow style across repos
- Fill gaps: add missing CI/release workflows to legacy projects

## Inputs

- Scenario (CI, PR check, release, scheduled, matrix)
- Stack (language, version, package manager, test/build commands)
- Triggers (branches, paths, tags)
- Target path (default `.github/workflows/`)

## Outputs

- Workflow YAML file content
- Notes: placeholders, Secret names, config items

## Scores (ASQM)

| Dimension      | Score |
| :---           | :---  |
| agent_native   | 5     |
| cognitive      | 4     |
| composability  | 4     |
| stance         | 5     |
| **asqm_quality** | 18   |

## Ecosystem

| Field | Value |
| :--- | :--- |
| overlaps_with (owner/repo:skill-name) | — |
| market_position | differentiated |

## Full definition

See [SKILL.md](./SKILL.md) for complete behavior, restrictions, Appendix A/B, and examples.
