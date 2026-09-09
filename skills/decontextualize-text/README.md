# Decontextualize Text

**Status**: Validated

## Purpose

Converts text that carries private context or internal dependencies into generic, unbiased wording. Keeps what was done and why; drops the people, the places, and the internal circumstances. Replaces proper nouns with generic descriptions fit for method abstraction, cross-team sharing, anonymization, or public release.

## When to use

- Generalization: turn lessons from one project into a general method
- Cross-team collaboration: strip jargon and code names
- De-identification: remove sensitive names before sharing
- Release preparation: the last pass before publishing

## Inputs

- Text containing organization/company/project names, internal conventions, or environment-specific details

## Outputs

- A generic version that keeps the logic and the structure; usable with no extra context

## Ecosystem

| Field | Value |
| :------------------------------------ | :-------------------------------------------------------- |
| overlaps_with (owner/repo: skill name) | nesnilnehc/ai-cortex:generate-standard-readme |
| Market position | Differentiated |

## Full definition

See [SKILL.md](./SKILL.md) for the full behavior, limits, and examples.
