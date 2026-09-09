# Orchestrate: Code Review (orchestrate-code-review)

Chains the atomic review-* skills in a fixed order (scope → language → framework → library → cognitive) and aggregates the findings into one unified report. This skill only orchestrates; it runs no code analysis of its own.

## When to use

- Full code review: the user asks to "review the code" or "review my changes" and expects one unified report
- pre-PR / pre-commit: run the whole pipeline once to get a baseline
- Paired with `orchestrate-repair-loop`: run this skill first for the findings, then hand them to `orchestrate-repair-loop` for iterative fixing

## When not to use

- A single-dimension review → call the matching atomic skill directly (`review-diff` / `review-security` / etc.)

## Inputs

- User intent (diff or codebase; the path given)
- Optional: language / framework hints

## Outputs

- One aggregated report (findings + risk_signals + notes on the steps that were skipped)

## Orchestration principles

It does four things only: detect the context / chain the sub-skills / halt-on-failure / aggregate the output. All domain detection logic lives inside the atomic review-* sub-skills.

## Full definition

See [SKILL.md](./SKILL.md).
