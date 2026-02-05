# Review Codebase

**Status**: validated

## What it does

Reviews the current state of specified files, directories, or repo. Covers architecture, design, tech debt, patterns, dependencies, security and performance. Does not depend on git diff. Complements review-code (diff-focused).

## When to use

- New module/service: architecture and implementation review
- Legacy audit: quality and risk review for path or repo
- Pair/sampling: review specified paths without current diff
- Teaching: check arbitrary code against review dimensions

## Inputs

- Paths (file(s), dir(s), or repo root)
- Optional: focus (e.g. security only)

## Outputs

- Per-file or per-module conclusions and suggestions with file:line references

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
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-code, wshobson/agents:code-review-excellence, secondsky/claude-skills:code-review, trailofbits/skills:differential-review, cxuu/golang-skills:go-code-review, obra/superpowers:requesting-code-review, skillcreatorai/Ai-Agent-Skills:code-review |
| market_position | commodity |

## Full definition

See [SKILL.md](./SKILL.md) for complete behavior, restrictions, and examples.
