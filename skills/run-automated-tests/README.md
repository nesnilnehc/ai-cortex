# Run Automated Tests

**Status**: experimental

## What it does

Analyzes a target repository's automated testing approach (docs, CI workflows, and build manifests) and runs the most appropriate test command(s) with a safety-first interaction policy.

## When to use

- You need the correct test command(s) without guessing.
- You want a safe default run (unit tests first) before attempting integration/e2e.
- You want to mirror CI test execution locally.

## Inputs

- Target repository path (default `.`)
- Mode: `fast` (default), `ci`, `full`
- Constraints: allow dependency install, allow network, allow Docker

## Outputs

- Test Plan Summary (evidence, chosen commands, assumptions, executed vs skipped)
- Execution results (success/failure, first failing command and exit code when failing)

## Scores (ASQM)

| Dimension | Score |
| :--- | :--- |
| agent_native | 4 |
| cognitive | 4 |
| composability | 4 |
| stance | 4 |
| **asqm_quality** | 16 |

## Ecosystem

| Field | Value |
| :--- | :--- |
| overlaps_with (owner/repo:skill-name) | — |
| market_position | commodity |

## Full definition

See [SKILL.md](./SKILL.md) for complete behavior, restrictions, and examples.

