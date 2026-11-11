---
name: split-product-delivery
description: Split a broad product requirement into proposed increments with independently verifiable outcomes. Use when the objective is clear but the work is too large to deliver or accept together.
version: 0.2.0
license: MIT
---

# Split Product Delivery

Read the objective, scope, acceptance, mandatory controls, and existing
commitments. If a missing business choice changes what can be split, use
`clarify-product-requirement` for that choice. If the current scope already fits
one delivery, return it as a single increment.

1. Find a small outcome a user can achieve end to end. Consider a workflow
   variant, user group, or business rule. Keep required controls and exception
   handling with the outcome that depends on them.
2. For each proposed increment, state its outcome, included and deferred
   scope, an observable acceptance scenario, and any known prerequisite.
   Explain which parts must ship together when separating them would break
   the outcome or a required control.
3. Check coverage against the agreed scope and preserve existing commitments.
   Return only increments that can be accepted separately. If no such split
   preserves the intended outcomes and required controls, report what must
   ship together and why. If the evidence is insufficient to tell, name the
   missing fact instead of concluding that a split is impossible.
4. When recording selected increments is in scope, follow the requirement
   lifecycle in `specs/requirement-modeling.md` and the source-record guidance
   in `specs/roadmap-modeling.md`. Hand off to `prioritize-backlog` for
   priority, `map-item-dependencies` for prerequisite evidence, and
   `promote-roadmap-items` for placement as applicable. Implementation tasks
   are derived from technical design under `specs/task-modeling.md`.

For automatic approval, a first increment can handle one application type
with a visible result and manual handling for exceptions. A later increment
can add a different application type with its own rules and acceptance.

## Self-check

Each proposed increment delivers an outcome that can be accepted separately.
Required controls stay with the work they govern. Deferred scope and
prerequisites are visible. When no viable split is found, the result explains
the constraint or the missing evidence.
