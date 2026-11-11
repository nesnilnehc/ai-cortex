---
artifact_type: guide
created_by: ai-cortex
lifecycle: living
created_at: 2026-11-11
status: active
---

# Clarify and split product requirements

Use either method when its trigger applies. A request with settled scope and
observable acceptance can go straight to the project's requirements workflow.
These methods support the runtime that authors requirements and the planner
that decides which work to schedule.

## Clarify business decisions

Use this when an unresolved choice changes the objective, scope, business
rules, or acceptance. Start from the request, any existing item, and its source
evidence. Classify raw input with [requirement intake triage](../../rules/requirement-intake-triage.md).
Route defects and technical work according to their kind.

1. Resolve facts from available evidence. Identify the business choices that
   remain and note which choices depend on others.
2. Ask about choices whose prerequisites are settled. Group independent
   questions when useful. Explain the consequence of each option and recommend
   one when the evidence supports it.
3. Carry confirmed answers forward. If an answer changes an earlier premise,
   revisit the decisions affected by that change.
4. Hand off the objective, scope and exclusions, observable acceptance,
   decision sources, and remaining questions to the runtime. Use
   [requirement modeling](../../specs/requirement-modeling.md) for the draft,
   including Open Questions when applicable. Keep material unresolved choices
   visible for [requirements review](../../skills/review-requirements/SKILL.md).

For example, for an automatic approval request, settle which application types
are in scope before asking which exceptions still need manual review. An
existing approval policy may already answer some of those questions.

## Split delivery by product outcome

Use this when the desired outcome is clear but the proposed scope is too broad
to deliver or accept together. Read the objective, constraints, and existing
commitments. Consider splitting by workflow variant, user group, or business
rule. Keep the steps needed to achieve each outcome together.

For each proposed slice, state the outcome, included and deferred scope, an
observable acceptance scenario, and any known prerequisite. Check that the
slices preserve the agreed objective and that each can be accepted separately.
Keep mandatory controls with every slice that needs them. If the outcome or a
required control cannot be separated, keep it together and explain why.

For example, first support automatic approval for one eligible application
type, with an observable result and manual handling for exceptions. A later
slice can cover another application type with its own eligibility rules and
acceptance conditions.

Return the proposal to the requester. When recording the chosen slices is in
scope, reuse existing source records and follow the requirement lifecycle for
any change to an approved requirement. Record independently accepted
deliverables in source records, as described in
[roadmap modeling](../../specs/roadmap-modeling.md#55-optional-iteration-view-schema-13).
Use the project's existing [roadmap planning workflow](roadmap-planning-usage.md)
for priority, dependency readiness, and placement. Derive implementation
tasks from technical design under [task modeling](../../specs/task-modeling.md).

## Method references

- [Product Grilling](https://github.com/Dengk3Li/product-manager-skill/blob/main/skills/product-grilling/SKILL.md) informed the order of business questions.
- [Epic Breakdown Advisor](https://github.com/deanpeters/Product-Manager-Skills/blob/main/skills/epic-breakdown-advisor/SKILL.md) informed the focus on independently verifiable outcomes.

Use the corresponding Skill for each method:
[Clarify Product Requirement](../../skills/clarify-product-requirement/SKILL.md),
[Split Product Delivery](../../skills/split-product-delivery/SKILL.md),
and their [provenance review packet](../../experiments/product-requirement-skills/review-packet.json).
