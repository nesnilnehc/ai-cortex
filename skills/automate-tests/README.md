# Run Automated Tests

**Status**: Experimental

## Purpose

Analyzes how the target repository runs automated tests (docs, CI workflows, and build manifests), then runs the best-matching test command under a safety-first strategy.

## When to use

- You need the correct test command without guessing.
- You want a safe default run (unit tests first) when reaching for integration/e2e.
- You want to reproduce the CI test run locally.

## Inputs

- Target repository path ("default")
- Mode: `fast` (default), `ci`, `full`
- Constraints: dependency installation allowed, network allowed, Docker allowed

## Outputs

- Test plan summary (evidence, selected commands, assumptions, what ran and what was skipped)
- Execution result (pass/fail, the first failing command and, on failure, its exit code)

## Ecosystem

| Field | Value |
| :--- | :--- |
| overlaps_with (owner/repo: skill name) | — |
| Market position | Commodity |

## Full definition

See [SKILL.md](./SKILL.md) for the full behavior, limits, and examples.
