# Define Roadmap

Create a source-backed roadmap with requirement arrangement, optional version
delivery, iteration and schedule views. Choose useful views and single/split
layout from project needs; preserve established destinations.
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

Material planning changes retain the latest five revision summaries and a durable history link under the [revision contract](../../specs/roadmap-modeling.md#54-revision-records). Regeneration and archive cleanup preserve earlier decisions.

Optional iteration views and one-main-plus-detail layouts follow the
[Roadmap Spec](../../specs/roadmap-modeling.md#reading-order-and-document-boundaries).
Iteration boundaries do not prove acceptance or release; linked/generated summaries
retain one editable source per fact. See the skill for maintenance/review ownership.

Use `--layout split` to keep delivery/history details in generated sibling documents;
`single` remains the default. Schema 1.3 adds optional iteration planning.

Scenario-based intake and retention follow the
[selection contract](../../specs/roadmap-modeling.md#56-context-recommendations-and-retained-selection-schema-14):
read evidence first, ask only material gaps, recommend with reasons and reuse the
settled combination during maintenance. Legacy and custom choices remain valid.

Start from the [four template recipes](assets/scenarios/README.md) and
[complete scenario outputs](references/scenarios/README.md). The read-only
`--recommend` mode reports questions/proposals or retained choices; schema 1.4
generation reuses saved layout and independently selects flow/phase/event views.
