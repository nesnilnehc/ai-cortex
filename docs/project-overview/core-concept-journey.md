# Core Concept Journey (Archived)

This document archives the original design concept diagram for AI Cortex.

**Source Diagram**: `docs/designs/share-diagram-journey.mmd` (and `.svg`)

## Original Design Intent

The diagram below illustrates the comprehensive journey of a user intent through the AI Cortex governance system:

1.  **Intent**: User provides input (e.g., "Start project").
2.  **Router**: The system matches the intent to a scenario using `skills/scenario-map.json`.
3.  **Governance Layer**: The execution is constrained by `spec/skill.md` and `AGENTS.md`.
4.  **Skill Application**: Orchestrators (like `review-code`) and atomic skills (`review-python`) execute the work.
5.  **Output**: The result is a standardized, auditable artifact (Docs, Delivery, Narrative).

## Diagram

![AI Cortex - Spec, Rules, 11 Scenarios](../designs/share-diagram-journey.svg)

*(Note: This diagram was replaced in the README by simplified Mermaid diagrams for better clarity and maintenance.)*
