# discover-document-norms

Help users establish project-specific artifact norms (paths, naming, lifecycle) through dialogue and scanning.

## What it does

This skill scans project `docs/` structure, confirms paths via dialogue, and produces `docs/ARTIFACT_NORMS.md` and optionally `.ai-cortex/artifact-norms.yaml`. Other document-producing skills (capture-work-items, brainstorm-design, documentation-readiness) read these norms to align output paths.

## When to use

- New project with no artifact norms
- Existing project with custom docs structure that needs formalization
- Migration to AI Cortex defaults or project-documentation-template

## Inputs

- Project path (default: workspace root)
- Optional: starting point (ai-cortex | template | blank)

## Outputs

- `docs/ARTIFACT_NORMS.md`: Human-readable artifact norms table
- `.ai-cortex/artifact-norms.yaml` (optional): Machine-readable schema

## Related skills

- `bootstrap-project-documentation`: Full docs bootstrap; discover-document-norms focuses on norms only
- `documentation-readiness`: Assess doc readiness; discover-document-norms defines norms
- `validate-document-artifacts`: Validate docs against norms after norms are established

## Installation

```bash
npx skills add nesnilnehc/ai-cortex --skill discover-document-norms
```

## License

MIT
