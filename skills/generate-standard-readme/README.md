# generate-standard-readme

**Status**: Validated

## Purpose

Generates a high-density README. Sections are pruned by a value threshold, not a fixed count. Within 30 seconds the reader knows what the project is, where to look, and how to use it.

## When to use

- New project: produce a lean front-page document fast
- Asset governance: unify README style across services
- Legacy system: fill in the missing documentation with the least information that works

## When not to use

- A full docs/ suite is needed → carried by the AgentFabric runtime or by hand, following `docs/ARTIFACT_NORMS.md`
- AGENTS.md is needed → `generate-agent-entry`

## Inputs

- Project name + one-line description (required)
- Project type: `code` or `doc` (optional, inferred from the repository structure)
- License type + file path (optional)
- Install command, quick-start example (optional for the code type)
- List of core entry points (optional)

## Outputs

The value threshold decides how many sections there are, with a floor of 3: title + description / entry points or usage / license.

## Full definition

See [SKILL.md](./SKILL.md): the section strategy, the anti-fluff rules, project-type routing, failure cases.
