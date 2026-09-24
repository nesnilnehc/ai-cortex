---
artifact_type: guide
created_by: ai-cortex
lifecycle: living
created_at: 2026-03-24
status: active
---

# Skill discovery and loading, in detail

This document sets out how an agent discovers and loads a **skill** inside this repository, for reference when you need the detail. AGENTS.md keeps only the summary.

> **Note**: discovery and loading for Protocols and Rules is in [AGENTS.md](../../AGENTS.md) §4 — agents read them straight from the canonical clone, with no install step.

---

## 1. The asset root

The root of the current repository, the root of the repository this file lives in, or a raw root URL supplied explicitly.

---

## 2. The discovery flow

1. Read `skills/INDEX.md` for the list of capabilities and their paths.
2. Match a skill against the task semantically, using its `description` and scope.
3. Pass context through explicit artifacts — a requirement, a design, a report and the like — rather than implicitly; when chaining calls, follow the Handoff Point and Scope Boundaries each skill states in its prose.

Research Skills optionally declare `metadata.ai_cortex_type` (`foundation`, `domain`, or `orchestrator`) and `metadata.ai_cortex_user_invocable` (`"true"` or `"false"`). The generated index displays these fields for opted-in Skills. They guide repository routing; an agent host may still display an internal Skill if it does not support hiding by metadata. The five public research entries and their handoffs are in the [research usage guide](./research-skills-usage.md).

---

## 3. Match priority, when several skills apply at once

Prefer the capability whose description and boundaries best fit the user's intent. Use an orchestrator for a request that spans its component capabilities. Read candidate skills when the index alone does not resolve an overlap.

---

## 4. Routing rules

- The primary skill comes first: route every request to the primary skill, and call an optional skill only once the primary skill's output exposes a definite gap.
- A request for a product opportunity selects `product-opportunity-analysis` as the primary Skill. It intentionally calls relevant policy, market and competitive Skills and passes their compatible Research Reports to the internal assessment Skill. A direct domain request ends at that domain's report.
- Escalation: when several intents are live within one cycle, escalate the orchestration to `plan-next`.
- Artifact handoff: pass context through explicit artifacts — a requirement, a design, an alignment report, a doc-readiness report and the like — rather than implicitly.
- Defaults: use the selected skill's stated defaults when the user supplied nothing explicit.

---

## 5. Injection

Load the selected SKILL's **complete Markdown** as system or context input, injected as one atomic unit.

For Rules, use `recommended_scope` as the context boundary:

- `user` or `both`: the installer exposes the Rule as long-lived IDE context.
- `project`: the Rule remains in the canonical AI Cortex clone and is loaded in full only when the matched Skill or explicit project configuration references it.

A project-scoped Rule is still mandatory when its applicability condition holds; on-demand loading controls context size, not policy strength.

---

## 6. Self-reference

When working inside this repository, take skill paths from the entries in `skills/INDEX.md`, and discover and load the assets under `skills/`.
