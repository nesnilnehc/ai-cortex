# Request Search Product planning selection

## Intake

Existing sources establish two-week planning and monthly releases. Ask only who reads the plan; the fictional owner names the pilot customer and release coordinator.

Known context: [source facts](sources.md#context). No source fact is inferred from
a template. Any answer above is fictional and retained in that source record.

## Decision

Adopted 2026-10-21 by the fictional planning owner. This is the settled example
choice, not evidence of a real authorization or a new approval gate.

| Field | Value |
| --- | --- |
| scenario | iterations |
| primary | iterations |
| views | requirements, iterations, versions, milestones, schedule |
| layout | split |
| rationale | Use two-week iteration goals, named delivery batches and release events; omit phases because no distinct stage boundary exists. |

Recommended starting views: requirements, iterations, versions, milestones.
Timeline is selected only where this scenario has timing facts. Layout is tailored
to the intended readers; it does not change the selected work scope.

## Tailoring

Enabled modules are listed once above. Omitted perspectives are not missing
deliverables: Use two-week iteration goals, named delivery batches and release events; omit phases because no distinct stage boundary exists.

The [recipe](../../../assets/scenarios/iteration-product.md) is a starting point, not a
mandatory lifecycle. Each fact remains editable in sources.md or this decision,
not independently in input.json and generated outputs.

## Maintenance

A later status/timing update reuses this primary perspective, views, layout and
destination without another interview. Changed context gets a focused proposal;
current choices remain until the owner resolves it. A material selection change
retains one revision ID. Initial adoption has no earlier revision to reconstruct.

[Main roadmap](roadmap.md) · [Source facts](sources.md).
