---
artifact_type: requirements
created_by: ai-cortex
lifecycle: living
created_at: 2026-03-24
status: active
---

# Requirements planning

AI Cortex's requirements are derived from the project's goals and its roadmap decisions.

## Canonical sources

- [Project overview](../project-overview/README.md) — the project's identity, its criteria for success, and its scope
- [Roadmap](../process-management/roadmap.md) — the milestones derived from strategy, the release scope, and the status

## When to add a requirement document

Add a structured requirement document, such as `docs/requirements-planning/<PROJECT>-REQ-<nn>.md`, in these situations:

- A significant change of scope
- Several stakeholders need formal requirement traceability

Write a requirement document to the field spec in [specs/requirement-modeling.md](../../specs/requirement-modeling.md), and self-check it against [rules/requirement-quality.md](../../rules/requirement-quality.md) before submitting. The workflow for writing requirements is carried by a runtime platform such as AgentFabric; AI Cortex supplies only the field contract and the quality rules.

Start from the [formal requirement template](templates/requirement-template.md).
It is an authoring aid; the Spec and Rule remain authoritative. Replace placeholders
with grounded facts and apply conditional section triggers. The lightweight
`capture-work-items` template records a backlog item rather than a formal requirement.

## Current requirements

- [AIC-REQ-01: research skills for product opportunity decisions](./AIC-REQ-01.md)
- [AIC-REQ-02: AI Cortex promotional website](./AIC-REQ-02.md)
- [AIC-REQ-04: work relationships and contextual asset use](./AIC-REQ-04.md) — implemented and published as Sites version 8; one homepage capability section offers Classification and Relationships with source-backed order/parent semantics and preserved state. Actual owner acceptance and public delivery checks are recorded in the task and publication evidence.
- [AIC-REQ-08: Skill provenance presentation](./AIC-REQ-08.md) — closed on 2026-10-29; implemented, accepted, merged into `main` and published as Sites version 11. [Closure and verification](../../experiments/skill-provenance/delivery-closeout.md#closure--2026-10-29).
