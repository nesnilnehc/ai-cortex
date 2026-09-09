---
artifact_type: guide
created_by: ai-cortex
lifecycle: living
created_at: 2026-03-26
status: active
---

# Proactive suggestions: stage to skill

This table offers an entry-point skill for each stage of collaboration.  
It is a suggested mapping and does not replace semantic matching against the task.

| Stage | Suggested skill | Note |
| :--- | :--- | :--- |
| Roadmap planning | `orchestrate-roadmap-planning` | One full pass from strategic goals to items entering Now; it checks the roadmap's health first, then decides which steps to run |
| Roadmap health check | `review-roadmap` | Evaluates an existing roadmap against the roadmap-quality criteria and produces findings |
| Roadmap upkeep | `update-roadmap` | Changes an item's status, moves its dates, and computes the downstream impact |
| Recording a requirement | `capture-work-items` | Turns free text into a structured item quickly |
| Prioritisation | `prioritize-backlog` | Re-scores the backlog through four frameworks in parallel and surfaces the disagreements for a person to decide |
| Dependency mapping | `map-item-dependencies` | Records the dependencies between items before promotion, and blocks the ones that are stuck |
| Requirement review | `review-requirements` | Runs the 5-dimension quality review over a requirement document |
| Code review | `orchestrate-code-review` | Orchestrates a multi-dimension code review in one place |
| Committing work | `commit-work` | Produces a conventional commit with the quality checks attached |

> The full usage of the roadmap chain — the entry points, the halts you will hit, and why dependency mapping comes before promotion — is in [roadmap-planning-usage.md](./roadmap-planning-usage.md).

> Document health checks, SSOT assessment, design and task breakdown are carried by the AgentFabric runtime and by linter and CI tools; the criteria are in [rules/doc-health-criteria.md](../../rules/doc-health-criteria.md), [specs/functional-design-modeling.md](../../specs/functional-design-modeling.md), [specs/technical-design-modeling.md](../../specs/technical-design-modeling.md) and [specs/task-modeling.md](../../specs/task-modeling.md).
