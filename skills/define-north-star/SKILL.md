---
name: define-north-star
description: Define the single most important metric representing the core value delivered to users. Produces North Star Metric with rationale, optional supporting metrics, and anti-pattern examples; persisted to docs.
description_zh: 定义代表向用户交付核心价值的单一最重要指标；产出 North Star Metric 及理由、辅助指标与反例。
tags: [documentation, workflow]
version: 1.2.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [north star, define north star, North Star Metric, NSM, define NSM]
input_schema:
  type: free-form
  description: Project/product description; target users; core value proposition; optional mission/vision or paths
output_schema:
  type: document-artifact
  description: North Star document with NSM, rationale, optional supporting metrics, anti-examples; optional measurement constraints section when metric has known limits
  artifact_type: north-star
  path_pattern: docs/project-overview/north-star.md
  lifecycle: living
---

# Skill: Define North Star

## Purpose

Define the **North Star Metric (NSM)**: the single most important metric capturing the core value delivered to users. Produce a document with the NSM, why it represents user value, optional supporting metrics (3-5), and anti-North-Star examples. Do not define mission, vision, strategic goals, or milestones.

---

## Core Objective

**Primary goal**: produce a user-confirmed North Star document holding one primary metric that reflects user value and behavior the product can influence, persisted to the path the project agreed on.

**Success criteria** (all of them must hold):

1. ✅ **North Star Metric defined**: one primary metric with a clear, measurable definition (name + how it is measured).
2. ✅ **Rationale recorded**: why this metric represents user value (not vanity, and not revenue alone).
3. ✅ **Principles satisfied**: the NSM reflects user value, represents user behavior, measures sustained engagement, is product-driven, and is plain and simple.
4. ✅ **User confirmation**: the user approves explicitly ("approved", "looks good", "go ahead", or equivalent).
5. ✅ **Document persisted**: written to the agreed path (`docs/project-overview/north-star.md` by default, or the per-project norm).
6. ✅ **Anti-patterns listed**: at least 2-3 vanity or anti-North-Star metrics listed as examples of what not to optimize (e.g. revenue, total users, sign-ups, downloads, raw page views).

**Acceptance** test: can a reader understand within a minute which single metric defines success for this product, and why it reflects user value rather than vanity?

**Handoff point**: once the North Star is approved and persisted, hand it to `design-strategic-goals` to set the goals that drive the NSM, or stop.

---

## Scope Boundaries

**This skill owns**:

- Deriving one primary North Star Metric from user value and product context.
- Recording why that metric represents user value (rather than vanity).
- Optional: 3-5 supporting metrics that complement the NSM.
- Listing the anti-North-Star metrics (vanity examples) that are not to be used as a North Star.
- Persisting to the path the project agreed on (`docs/project-overview/north-star.md` by default).

**This skill does not own**:

- Defining the mission or the vision (use `define-mission`, `define-vision`).
- Defining strategic goals or OKRs (use `design-strategic-goals`).
- Defining milestones (use `define-milestones`).
- Writing the roadmap, requirements, or backlog (use project planning, `analyze-requirements`, `capture-work-items`).

---

## Use Cases

- **After the vision**: once the vision is clear, establish the metric that best captures "value delivered".
- **Product prioritization**: when the team needs a single metric to guide what gets optimized.
- **Replacing a vanity metric**: when the current focus is revenue, total users, downloads, or page views and the team wants a user-value anchor.
- **The third layer of the strategy chain**: follows mission and vision when the full hierarchy is being built.

---

## Behavior

### Interaction strategy

Follow Defaults first, Prefer choices, Context inference:

- **Defaults**: load mission/vision from `docs/project-overview/` or from the project norm; the output path comes from the project norm or `docs/project-overview/north-star.md`. With no further input, run the derivation framework directly.
- **Offer choices**: where several candidate metrics exist, offer 1–3 of them with the reasoning and let the user choose or refine.
- **Confirm**: user approval must be obtained before overwriting an existing north-star file and before persisting. When a candidate is a vanity metric, warn and suggest a behavior-based alternative.

### North Star principles (applied while deriving the metric)

1. **Reflects user value**, not company revenue alone.
2. **Represents user behavior**, not a vanity count.
3. **Measures sustained engagement**, not a one-off event.
4. **Is product-driven**: the product team can influence it.
5. **Is plain and simple**: ideally a single measurable quantity.

### Derivation framework (execution flow)

Derive the North Star with this reasoning chain:

```text
User
  ↓
Core Value Delivered
  ↓
Primary User Action
  ↓
Observable Behavior
  ↓
Measurable Metric (North Star)
```

1. **Context**: load mission/vision from `docs/project-overview/` or from the user; determine the target users and the core value proposition.
2. **Core value**: what value does the product bring users? (Not "revenue" — user outcomes.)
3. **Primary action**: what is the main user action that reflects that value?
4. **Observable behavior**: which behaviors can be observed (e.g. messages sent, nights booked, time spent)?
5. **Metric**: define one measurable metric that captures that behavior; keep it simple.
6. **Validate**: check against the five principles; avoid vanity (revenue, total users, sign-ups, downloads, raw page views as the North Star).
7. **Measurement and limits** (optional): when the metric depends on an external data source, or cannot currently be measured directly, add a "Measurement and limits" section to the output document covering the dependency and the fallback strategy.
8. **Supporting metrics** (optional): add 3–5 metrics that support or complement the NSM.
9. **Anti-examples**: list 2–3 metrics that are not to be used as a North Star, each with a short reason.
10. **Persist**: write to the agreed path; create the directory if it does not exist.

### Anti-patterns (not suggested as a North Star)

- Revenue (a company outcome, not user value).
- Total users (vanity; reflects neither engagement nor value).
- Sign-ups (one-off; not sustained engagement).
- Downloads (one-off; not a behavior).
- Raw page views (vanity; not a value-delivering behavior).

These may appear in the output only as **anti-North-Star examples**, and not as the chosen metric.

---

## Input & Output

**Input**:

- **Required**: project/product description; target users; core value proposition (or a mission/vision path).
- **Optional**: mission/vision text or path; current metrics; constraints; examples from comparable products.

**Output**:

- **Artifact**: the North Star document.
- **Path**: `docs/project-overview/north-star.md` (or the project norm).
- **Structure**: metric definition, derivation chain, principles, optional supporting metrics, optional measurement and limits, anti-North-Star examples. Keep it lean (YAGNI, DRY).
- **Lifecycle**: living (updated when the product or the strategy changes).

---

## Restrictions

### Hard Boundaries

- Do not define the mission, the vision, strategic goals, or milestones in this skill.
- Do not put forward a vanity metric (revenue, total users, sign-ups, downloads, raw page views) as the North Star; list them as anti-examples only.
- Do not overwrite an existing North Star file without explicit user confirmation.

### When to Stop (handoff)

- The user says "approved" or equivalent → the North Star is done; hand off to `design-strategic-goals`.
- The user asks about goals or milestones → hand off to `design-strategic-goals` or `define-roadmap`.

### Skill Boundaries (avoid overlap)

**Do not do these (other skills handle them)**:

- **Mission**: why it exists → use `define-mission`
- **Vision**: what future is being built → use `define-vision`
- **Strategic goals**: 3–5 outcomes → use `design-strategic-goals`
- **Milestones**: stage checkpoints → use `define-roadmap`

---

## Self-Check

### Core success criteria (all of them must hold)

- [ ] **North Star Metric defined**: one primary metric with a clear, measurable definition.
- [ ] **Rationale recorded**: why this metric represents user value (rather than vanity).
- [ ] **Principles satisfied**: user value, behavior, sustained engagement, product-driven, simple.
- [ ] **User confirmation**: the user said "approved", "looks good", "go ahead", or something similar.
- [ ] **Document persisted**: written to the agreed path (`docs/project-overview/north-star.md` by default, or the project norm).
- [ ] **Anti-patterns listed**: at least 2-3 vanity / anti-North-Star examples in the document.

### Process quality checks

- [ ] **Derivation used**: was the user → core value → action → behavior → metric chain applied?
- [ ] **Measurement and limits**: when the metric depends on external data or is currently unobservable, was a "Measurement and limits" section added?
- [ ] **No vanity NSM**: did it avoid revenue, total users, sign-ups, downloads, or raw page views as the North Star?

### Acceptance test

**Can a reader understand within a minute which single metric defines success, and why it reflects user value?**

If no: the NSM is unclear or vanity. Re-derive it with the framework and the principles.
If yes: the North Star is done. Move on to the handoff, or stop.

---

## Examples

### Example 1: from vision to North Star

**Context**: the vision is "every team ships to production in under 5 minutes with a single click." Target users: engineering teams. Core value: reliable, fast deployment.

**Process**: core value = successful, low-friction deployment. Primary action = completing a deployment. Observable behavior = the number of deployments that succeed within the time/simplicity bar. Metric: "weekly successful deployments (completed within 5 minutes of trigger)". Supporting: deployment frequency, rollback rate, deployment duration. Anti-examples: total users, revenue, page views. The user confirms. Write to `docs/project-overview/north-star.md`.

**Result**: the North Star is persisted; hand off to `design-strategic-goals`.

### Example 2: the user suggests a vanity metric

**Context**: the user says "our North Star should be total registered users."

**Process**: apply the principles — total users is vanity, not sustained engagement or behavior. Use the derivation: user → core value ("users get X done", say) → primary action → observable behavior → metric. Put forward a behavior-based alternative ("weekly active users who complete at least one core action", say) and list "total registered users" as an anti-North-Star example. Ask the user to confirm the behavior-based NSM, or to refine it.

**Result**: the document holds the chosen NSM together with the anti-example "total registered users - not sustained engagement"; persistence complete.

### Example 3: the metric has measurement limits

**Context**: the NSM is "monthly skill adoption", but it depends on an external ecosystem (skills.sh, say) opening its API, and cannot currently be obtained directly.

**Process**: after deriving the NSM, verify that every principle holds. Add a "Measurement and limits" section stating the dependency on vercel-labs/skills#426 or an equivalent capability landing; until then it cannot be measured directly. Optionally add the counting strategy for an in-house registry (SkillReg, SkillHub) inside the organization. Persist once the user confirms.

**Result**: the document holds the NSM, the derivation, the principles, measurement and limits, and the anti-examples; the reader knows the metric is correctly defined but currently unobservable.
