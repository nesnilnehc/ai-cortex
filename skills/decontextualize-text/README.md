# Decontextualize Text

**Status**: validated

## What it does

Converts text with private context or internal dependencies into generic, unbiased expressions. Keeps what is done and why; removes who, where, and internal conditions. Replaces proper nouns with generic descriptions for methodology abstraction, cross-team sharing, anonymization, or public release.

## When to use

- Generalization: turn project-specific lessons into generic methodology
- Cross-team collaboration: remove jargon or codenames
- De-identification: strip sensitive names before sharing
- Release preparation: final cleanup before publishing

## Inputs

- Text containing org/company/project names, internal conventions, or environment-specific details

## Outputs

- Generic version with logic and structure preserved; usable without extra context

## Scores (ASQM)

| Dimension      | Score |
| :---           | :---  |
| agent_native   | 5     |
| cognitive      | 4     |
| composability  | 4     |
| stance         | 4     |
| **asqm_quality** | 17   |

## Ecosystem

| Field | Value |
| :--- | :--- |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:generate-standard-readme |
| market_position | differentiated |

## Full definition

See [SKILL.md](./SKILL.md) for complete behavior, restrictions, and examples.
