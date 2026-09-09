# Define Docs Norms

Creates or updates `docs/ARTIFACT_NORMS.md`, landing a norms proposal as the project's authoritative rules.

## Purpose

- Create the norms file from a confirmed proposal
- Merge updates into an existing norms file
- Produce an auditable change summary

## Outputs

- `docs/ARTIFACT_NORMS.md`

## Related skills

- Norms discovery and proposal: carried by a human or the AgentFabric runtime
- Norms compliance checking: run by the runtime / linter / CI tooling against `rules/doc-health-criteria.md`
- Structure tidying: run by the runtime against `rules/repo-structure-hygiene.md`
