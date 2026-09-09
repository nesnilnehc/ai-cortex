# Generate GitHub Workflow

**Status**: Validated

## Purpose

Generates GitHub Actions workflow YAML that meets the output contract in Appendix A of the skill. Security first, least privilege, pinned versions. For CI, releases, and PR checks. Supports Node, Python, Go, Rust; includes a Go + Docker + GoReleaser appendix.

## When to use

- New project setup: add a CI or PR-check workflow
- Standardization: align workflow style across repositories
- Filling gaps: add the missing CI/release workflow to a legacy project

## Inputs

- Scenario (CI, PR check, release, schedule, matrix)
- Stack (language, version, package manager, test/build commands)
- Triggers (branches, paths, tags)
- Target path (default `.github/workflows/`)

## Outputs

- The workflow YAML file content
- Notes: placeholders, secret names, configuration items

## Ecosystem

| Field | Value |
| :------------------------------------ | :------------- |
| overlaps_with (owner/repo: skill name) | — |
| Market position | Differentiated |

## Full definition

See [SKILL.md](./SKILL.md) for the full behavior, limits, appendices A/B, and examples.
