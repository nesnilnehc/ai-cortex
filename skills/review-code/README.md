# Review Code (Orchestrator)

**Status**: validated

## What it does

Orchestrates atomic review skills in a fixed order (scope → language → framework → library → cognitive) and aggregates their findings into one report. Does not perform code analysis itself; invokes or simulates review-diff, review-codebase, review-dotnet, review-java, review-sql, review-vue, review-security, review-architecture.

## When to use

- Full code review: user asks to "review code" or "review my changes" and expects one combined report.
- Pre-PR or pre-commit: run the full pipeline and get one report.
- For a single-dimension review (e.g. only diff or only security), use the corresponding atomic skill instead.

## Inputs

- User intent (full review vs specific dimension).
- Code scope (git diff or paths) when known.

## Outputs

- Single aggregated report with findings in standard format (Location, Category, Severity, Title, Description, Suggestion).

## Scores (ASQM)

| Dimension      | Score |
| :---           | :---  |
| agent_native   | 5     |
| cognitive      | 5     |
| composability  | 5     |
| stance         | 5     |
| **asqm_quality** | 20   |

## Ecosystem

| Field | Value |
| :--- | :--- |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-diff, nesnilnehc/ai-cortex:review-codebase, wshobson/agents:code-review-excellence, secondsky/claude-skills:code-review, trailofbits/skills:differential-review, cxuu/golang-skills:go-code-review, obra/superpowers:requesting-code-review, skillcreatorai/Ai-Agent-Skills:code-review |
| market_position | differentiated |

## Full definition

See [SKILL.md](./SKILL.md) for execution order, behavior, and output contract.
