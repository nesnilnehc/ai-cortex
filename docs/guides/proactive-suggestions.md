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
| Open research question | `deep-research` | Decomposes an uncertain question and returns source-backed findings, conflicts and gaps |
| Policy or compliance research | `policy-research` | Studies a named jurisdiction, effective dates, applicability and product implications |
| Market demand or size research | `market-research` | Defines the market boundary, demand and defensible sizing or an explicit evidence gap |
| Competitor comparison | `competitive-research` | Produces a dated, cited capability or positioning comparison with Unknown cells |
| Product or feature opportunity decision | `product-opportunity-analysis` | Combines relevant lanes into an Opportunity Package with recommendation and trace |
| Roadmap planning | `orchestrate-roadmap-planning` | One full pass from strategic goals to items entering Now; it checks the roadmap's health first, then decides which steps to run |
| Roadmap health check | `review-roadmap` | Evaluates an existing roadmap against the roadmap-quality criteria and produces findings |
| Roadmap upkeep | `update-roadmap` | Changes an item's status, moves its dates, and computes the downstream impact |
| Recording a requirement | `capture-work-items` | Turns free text into a structured item quickly |
| Prioritisation | `prioritize-backlog` | Re-scores the backlog through four frameworks in parallel and surfaces the disagreements for a person to decide |
| Dependency mapping | `map-item-dependencies` | Records the dependencies between items before promotion, and blocks the ones that are stuck |
| Requirement review | `review-requirements` | Runs the 5-dimension quality review over a requirement document |
| Functional-design review | `review-functional-design` | Checks business workflows, states, permissions, exceptions and traceability before technical design |
| Technical-design review | `review-technical-design` | Checks engineering executability and profiled quality tactics before task derivation |
| Task review | `review-tasks` | Checks task readiness, dependency safety, design coverage and verification annotations before coding |
| Engineering gate after coding | `orchestrate-code-review` | Aggregates intrinsic code quality across scope, stack and engineering concerns |
| Functional gate after coding | `review-implementation-alignment` + `automate-tests` | Compares approved intent with production code, then executes acceptance evidence |
| Repair and convergence | `orchestrate-repair-loop` | Applies targeted fixes and reruns every affected sibling gate until both pass or a stop condition is reached |
| Committing work | `commit-work` | Produces a conventional commit with the quality checks attached |

> The full usage of the roadmap chain — the entry points, the halts you will hit, and why dependency mapping comes before promotion — is in [roadmap-planning-usage.md](./roadmap-planning-usage.md).

> The research entry routes, scope inputs and package handoff are in [research-skills-usage.md](./research-skills-usage.md).

> Document authoring and task derivation may be carried by an AgentFabric runtime or another producer. AI Cortex owns the review contracts above and keeps their criteria in the paired Rules.
