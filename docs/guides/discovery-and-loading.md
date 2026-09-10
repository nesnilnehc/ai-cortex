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

1. Read `skills/INDEX.md` and `skills/INDEX.md` for the list of capabilities and their paths.
2. Match a skill against the task semantically, using the SKILL's `description`, `tags` and `triggers`.
3. Pass context through explicit artifacts — a requirement, a design, a report and the like — rather than implicitly; when chaining calls, follow the Handoff Point and Scope Boundaries each skill states in its prose.

---

## 3. Match priority, when several sources apply at once

1. An exact match on the SKILL's frontmatter `triggers`
2. A semantic match on `description` or `tags`

---

## 4. Routing rules

- The primary skill comes first: route every request to the primary skill, and call an optional skill only once the primary skill's output exposes a definite gap.
- Escalation: when several intents are live within one cycle, escalate the orchestration to `plan-next`.
- Artifact handoff: pass context through explicit artifacts — a requirement, a design, an alignment report, a doc-readiness report and the like — rather than implicitly.
- Defaults: where `input_schema.defaults` exists and the user supplied nothing explicit, use that default.

---

## 5. Injection

Load the selected SKILL's **complete Markdown** as system or context input, injected as one atomic unit.

---

## 6. Self-reference

When working inside this repository, take skill paths from the `capabilities` in `skills/INDEX.md`, and discover and load the assets under `skills/`.
