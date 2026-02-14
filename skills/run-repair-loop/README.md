# Run Repair Loop

**Status**: experimental

## What it does

Runs an iterative loop to converge code to "clean": review -> test -> fix -> repeat until tests pass and no blocking review findings remain (or a stop condition is reached).

## When to use

- You want an agent to keep fixing until tests are green.
- You want repeated review + test cycles to prevent regressions while repairing.

## Inputs

- Target path (default `.`)
- Scope: `diff` (default) or `codebase`
- Test mode: `fast` (default), `ci`, `full`
- Constraints: allow installs/network/Docker/services
- `max_iterations` (default `5`)

## Outputs

- Repair Loop Report with iteration-by-iteration test results and patches applied.

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
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-code, nesnilnehc/ai-cortex:run-automated-tests |
| market_position | experimental |

## Full definition

See [SKILL.md](./SKILL.md) for full behavior, restrictions, and examples.
