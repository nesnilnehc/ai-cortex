# Define Roadmap

Create a source-backed roadmap with requirement arrangement, optional version
delivery and schedule views. Recommend the three-view combination and let the
user choose views and destination.
Each requirement row links its source and states the outcome, priority, separate approval and execution status, and separate key
conditions. The execution cell uses one fixed label from the quality rule. Tasks and detailed acceptance evidence remain in source documents.

Use the bundled [template](assets/roadmap-template.md) and
[completed example](references/roadmap-example.md). Review against
[roadmap-quality](../../rules/roadmap-quality.md).

Default output: `docs/process-management/roadmap.md`, respecting project norms.
See [SKILL.md](SKILL.md) for the procedure and Self-Check.

## Offline generation

The bundled `scripts/render-roadmap.py` validates temporary JSON and generates
Markdown, SVG and dated Mermaid without extra packages. Relative weeks use SVG;
unknown dates remain unscheduled. See the [capability guide](../../docs/guides/roadmap-planning-usage.md)
for the input example, invocation and conditional platform-delivery support.

## Finished example

[Complete Service Desk deliverables](references/service-desk/README.md).

Phase spans and milestone events follow the [Roadmap Spec](../../specs/roadmap-modeling.md); legacy formats remain compatible.
