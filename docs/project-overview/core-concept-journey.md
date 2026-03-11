# Core Concept Journey (Archived)

This document archives the original design concept diagram for AI Cortex.

**Source Diagram**: 原始图文件未在仓库保留，仅保留设计意图归档。

## Original Design Intent

The diagram below illustrates the comprehensive journey of a user intent through the AI Cortex governance system:

1. **Intent**: User provides input (e.g., "Start project").
2. **Router**: The system matches the intent to a scenario using `skills/scenario-map.json`.
3. **Governance Layer**: The execution is constrained by `spec/skill.md` and `AGENTS.md`.
4. **Skill Application**: Orchestrators (like `review-code`) and atomic skills (`review-python`) execute the work.
5. **Output**: The result is a standardized, auditable artifact (Docs, Delivery, Narrative).

## Diagram Status

The original visual asset was replaced in the README by simplified Mermaid diagrams for better clarity and maintenance. This archive preserves the original intent and flow semantics.
