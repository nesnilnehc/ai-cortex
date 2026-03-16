---
name: define-north-star
description: Define the single most important metric representing the core value delivered to users. Produces North Star Metric with rationale, optional supporting metrics, and anti-pattern examples; persisted to docs.
tags: [documentation, workflow, eng-standards]
version: 1.0.0
license: MIT
related_skills: [define-mission, define-vision, design-strategic-goals, align-planning]
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [north star, define north star, North Star Metric, NSM]
input_schema:
  type: free-form
  description: Project/product description; target users; core value proposition; optional mission/vision or paths
output_schema:
  type: document-artifact
  description: North Star document with NSM, rationale, optional supporting metrics, anti-examples; written to docs/project-overview/north-star.md (or project norms)
  artifact_type: north-star
  path_pattern: docs/project-overview/north-star.md
  lifecycle: living
---

# Skill: Define North Star

## Purpose

Define the **North Star Metric (NSM)**: the single most important metric that captures the core value delivered to users. Produce a document with the NSM, why it represents user value, optional supporting metrics (3–5), and anti–North-Star examples. Does not define mission, vision, strategic goals, or milestones.

---

## Core Objective

**Primary Goal**: Produce a user-confirmed North Star document containing one primary metric that reflects user value and product-influenced behavior, persisted to the project-agreed path.

**Success Criteria** (ALL must be met):

1. ✅ **North Star Metric defined**: One primary metric with a clear, measurable definition (name + how it is measured).
2. ✅ **Rationale documented**: Explanation of why this metric represents user value (not vanity or revenue-only).
3. ✅ **Principles satisfied**: NSM reflects user value, represents user behavior, measures ongoing engagement, is product-driven, and is simple and clear.
4. ✅ **User confirmed**: User explicitly approved (e.g. "approved", "looks good", "proceed", or equivalent).
5. ✅ **Document persisted**: Written to agreed path (default `docs/project-overview/north-star.md` or per project norms).
6. ✅ **Anti-patterns listed**: At least 2–3 vanity or anti–North-Star metrics listed as examples of what not to optimize for (e.g. revenue, total users, registrations, downloads, raw page views).

**Acceptance Test**: Can a reader understand in under a minute which single metric defines success for this product and why it reflects user value rather than vanity?

**Handoff Point**: When North Star is approved and persisted, hand off to `design-strategic-goals` to set goals that move the NSM, or stop.

---

## Scope Boundaries

**This skill handles**:

- Deriving one primary North Star Metric from user value and product context.
- Documenting why the metric represents user value (and not vanity).
- Optional: 3–5 supporting metrics that complement the NSM.
- Listing anti–North-Star metrics (vanity examples) that should not be used as the North Star.
- Persisting to project-agreed path (default `docs/project-overview/north-star.md`).

**This skill does NOT handle**:

- Defining mission or vision (use `define-mission`, `define-vision`).
- Defining strategic goals or OKRs (use `design-strategic-goals`).
- Defining milestones (use `define-milestones`).
- Writing roadmap, requirements, or backlog (use project planning, `analyze-requirements`, `capture-work-items`).

---

## Use Cases

- **After vision**: Establish the one metric that best captures "value delivered" once vision is clear.
- **Product prioritization**: When the team needs a single metric to guide what to optimize for.
- **Replacing vanity metrics**: When current focus is on revenue, total users, downloads, or page views and the team wants a user-value anchor.
- **Third layer in strategy chain**: Run after mission and vision when building the full hierarchy.

---

## Behavior

### Interaction Policy

- **Defaults**: Output path from project norms if present; otherwise `docs/project-overview/north-star.md`. Read mission/vision from `docs/project-overview/` when available. Use derivation framework below to propose NSM.
- **Choice options**: If multiple candidate metrics exist, offer 1–3 with rationale and ask user to pick or refine.
- **Confirm**: Before overwriting an existing north-star file; before final persist. If proposed metric is vanity-like, warn and suggest a behavior-based alternative.

### North Star Principles (apply when deriving the metric)

1. **Reflects user value**, not company revenue alone.
2. **Represents user behavior**, not vanity statistics.
3. **Measures ongoing engagement**, not one-time events.
4. **Is product-driven**: the product team can influence it.
5. **Is simple and clear**: ideally a single measurable metric.

### Derivation Framework (Execution Process)

Use this reasoning chain to derive the North Star:

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

1. **Context**: Load mission/vision from `docs/project-overview/` or user; identify target users and core value proposition.
2. **Core value**: What value does the product deliver to users? (Not "revenue" — user outcome.)
3. **Primary action**: What is the main user action that reflects that value?
4. **Observable behavior**: What behavior can we observe (e.g. messages sent, nights booked, time spent)?
5. **Metric**: Define one measurable metric that captures that behavior; keep it simple.
6. **Validate**: Check against the five principles; avoid vanity (revenue, total users, registrations, downloads, raw page views as the North Star).
7. **Supporting metrics** (optional): Add 3–5 metrics that support or complement the NSM.
8. **Anti-examples**: List 2–3 metrics that should NOT be used as the North Star (e.g. revenue, total users, registrations, downloads, page views) with a brief reason.
9. **Persist**: Write to agreed path; create `docs/project-overview/` if missing.

### Anti-Patterns (do not propose as North Star)

- Revenue (company outcome, not user value).
- Total users (vanity; does not reflect engagement or value).
- Registrations (one-time; not ongoing engagement).
- Downloads (one-time; not behavior).
- Raw page views (vanity; not value-delivering behavior).

These may appear in the output only as **anti–North-Star examples**, not as the chosen metric.

---

## Input & Output

**Input**:

- **Required**: Project/product description; target users; core value proposition (or mission/vision paths).
- **Optional**: Mission/vision text or paths; current metrics; constraints; examples from comparable products.

**Output**:

- **Artifact**: North Star document.
- **Location**: `docs/project-overview/north-star.md` (or per project norms).
- **Content**: North Star Metric (name + definition); why it represents user value; 3–5 optional supporting metrics; anti–North-Star examples (what not to optimize for).
- **Lifecycle**: Living (update when product or strategy changes).

---

## Restrictions

### Hard Boundaries

- Do NOT define mission, vision, strategic goals, or milestones in this skill.
- Do NOT propose a vanity metric (revenue, total users, registrations, downloads, raw page views) as the North Star; list them only as anti-examples.
- Do NOT overwrite an existing north-star file without explicit user confirmation.

### Skill Boundaries (Avoid Overlap)

**Do NOT do these (other skills handle them)**:

- **Mission**: Why we exist → Use `define-mission`.
- **Vision**: What future we build → Use `define-vision`.
- **Strategic goals**: 3–5 outcomes → Use `design-strategic-goals`.
- **Milestones**: Phase checkpoints → Use `define-milestones`.

**When to stop and hand off**:

- User says "approved" or equivalent → North Star complete; offer handoff to `design-strategic-goals`.
- User asks for goals or milestones → Hand off to `design-strategic-goals` or `define-milestones`.

---

## Self-Check

### Core Success Criteria (ALL must be met)

- [ ] **North Star Metric defined**: One primary metric with clear, measurable definition.
- [ ] **Rationale documented**: Why this metric represents user value (not vanity).
- [ ] **Principles satisfied**: User value, behavior, ongoing engagement, product-driven, simple.
- [ ] **User confirmed**: User said "approved", "looks good", "proceed", or equivalent.
- [ ] **Document persisted**: Written to agreed path (default `docs/project-overview/north-star.md` or project norms).
- [ ] **Anti-patterns listed**: At least 2–3 vanity/anti–North-Star examples in the document.

### Process Quality Checks

- [ ] **Derivation used**: Did I apply User → Core Value → Action → Behavior → Metric?
- [ ] **No vanity as NSM**: Did I avoid proposing revenue, total users, registrations, downloads, or raw page views as the North Star?

### Acceptance Test

**Can a reader understand in under a minute which single metric defines success and why it reflects user value?**

If NO: NSM is unclear or vanity-like. Re-derive using the framework and principles.
If YES: North Star is complete. Proceed to handoff or stop.

---

## Examples

### Example 1: From vision to North Star

**Context**: Vision is "Every team can ship to production in under 5 minutes with one click." Target users: engineering teams. Core value: reliable, fast deployments.

**Process**: Core value = successful, low-friction deployments. Primary action = complete a deployment. Observable behavior = number of deployments that succeeded within a time/simplicity bar. Metric: "Weekly successful deployments (completed within 5 min of trigger)." Supporting: deployment frequency, rollback rate, time-to-deploy. Anti-examples: total users, revenue, page views. User confirms. Write to `docs/project-overview/north-star.md`.

**Outcome**: North Star persisted; handoff to `design-strategic-goals` offered.

### Example 2: User suggests a vanity metric

**Context**: User says "Our North Star should be total registered users."

**Process**: Apply principles — total users is vanity, not ongoing engagement or behavior. Use derivation: User → Core value (e.g. "users get X done") → Primary action → Observable behavior → Metric. Propose a behavior-based alternative (e.g. "weekly active users who completed at least one core action") and list "total registered users" as an anti–North-Star example. Ask user to confirm the behavior-based NSM or refine.

**Outcome**: Document includes chosen NSM plus anti-example "total registered users — not ongoing engagement"; persisted.
