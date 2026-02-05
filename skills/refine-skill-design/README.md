# Refine Skill Design

**Status**: validated

## What it does

Audits and refactors existing SKILLs. Applies meta-audit model: intent, logic, constraints, examples. Aligns to spec, improves robustness and scenario coverage. For drafts and quality fixes; not for creating new skills from scratch.

## When to use

- New skill onboarding: expert review after draft generation
- Quality fixes: align logic when behavior is inconsistent
- Consistency audit: match tagging and naming in INDEX.md
- Upgrade: turn simple formatting into full Agent capability

## Inputs

- SKILL Markdown document or rough draft

## Outputs

- Optimized SKILL Markdown
- Diff summary (what changed and why)
- Version suggestion (SemVer)

## Scores (ASQM)

| Dimension      | Score |
| :---           | :---  |
| agent_native   | 4     |
| cognitive      | 5     |
| composability  | 5     |
| stance         | 5     |
| **asqm_quality** | 19   |

## Ecosystem

| Field | Value |
| :--- | :--- |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:curate-skills, nesnilnehc/ai-cortex:discover-skills |
| market_position | differentiated |

## Full definition

See [SKILL.md](./SKILL.md) for complete behavior, restrictions, and examples.
