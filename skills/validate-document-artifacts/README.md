# validate-document-artifacts

Validate documents under `docs/` against project artifact norms.

## What it does

Resolves project norms from `docs/ARTIFACT_NORMS.md` or `.ai-cortex/artifact-norms.yaml` (fallback: spec/artifact-contract.md), scans Markdown files, infers artifact type from path or front-matter, and emits a findings list for violations (path, naming, front-matter).

## When to use

- Pre-commit check for doc compliance
- Audit existing docs against norms
- After updating ARTIFACT_NORMS.md

## Inputs

- Project path (default: workspace root)
- Optional: docs root (default `docs/`)
- Optional: scope (all or specific artifact_type)

## Outputs

- Findings list in standard format (Location, Category, Severity, Title, Description, Suggestion)
- Summary: files scanned, violations by severity

## Related skills

- `assess-documentation-readiness`: Assess doc readiness; validate-document-artifacts checks norm compliance
- `discover-document-norms`: Establish norms; validate-document-artifacts checks against them
- `curate-skills`: Skill governance; validate-document-artifacts is doc governance

## Installation

```bash
npx skills add nesnilnehc/ai-cortex --skill validate-document-artifacts
```

## License

MIT
