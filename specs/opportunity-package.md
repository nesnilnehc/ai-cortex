---
id: OPPORTUNITY_PACKAGE_SPEC_V1
name: Opportunity Package
description: Structural contract for an evidence-linked product opportunity decision with honest lane status and a reviewable recommendation.
version: 1.0.0
status: active
lifecycle: living
created_at: 2026-09-17
scope: |
  Defines the JSON package passed from research into a product decision.
  Does not approve a product, create a requirement, or prescribe research tools.
related:
  - ./research-evidence.md
  - ./spec-modeling.md
---

# Opportunity Package

> **Data contract**: a scoped recommendation whose material claims resolve to research findings and their sources or explicit unknowns

## 1. Position and scope

The package is the output of `product-opportunity-analysis`. It preserves research reports and adds a decision layer. A Markdown summary may accompany the JSON object, but the JSON object is the handoff contract. Machine keys and enum values are English; narrative fields may use the user's language.

## 2. Mental model

A decision owner should be able to answer: Which problem and audience are at stake? What was examined and omitted? What favors or opposes the opportunity? What is recommended, at what confidence, and what would change the decision? Which inspected source or acknowledged gap supports every decisive assertion?

## 5. Body structure contract

### 5.1 Package fields

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `schema_version` | string | yes | `"1.0"` |
| `package_id` | string | yes | Stable package identity |
| `status` | enum | yes | `draft` or `ready_for_decision` |
| `question` | string | yes | Product or feature decision being assessed |
| `context` | object | yes | `product`, `target_users`, `geography`, `as_of`, `decision_owner`; missing scope is disclosed in gaps, while `decision_owner` may be null in a draft |
| `problem` | object | yes | `statement`, `alternatives` (array), `why_now` |
| `lanes` | object | yes | Exactly `policy`, `market`, `competitive`, `user_signals` lane objects |
| `reports` | array | yes | Embedded Research Reports conforming to [research-evidence.md](./research-evidence.md) |
| `claims` | array | yes | Decision-critical claim records with unique IDs and trace references |
| `analysis` | object | yes | `unmet_needs`, `differentiation`, `constraints`, `size_or_impact`, `assumptions`, `opposing_evidence`, `conflicts`, `gaps` |
| `recommendation` | object | yes | Decision, confidence, rationale, product scope, risks and next validation steps |

Each lane has `status` (`complete`, `limited`, `not_applicable`, `missing`), `reason`, and `report_ids`. A `complete` or `limited` lane has at least one referenced report; `missing` or `not_applicable` has none. A lane may be `limited` when sources are stale, unavailable, or insufficient. The user-signals lane may use a Research Report of interviews or supplied evidence; it is never inferred solely from vendor marketing. Every report ID is unique in the package.

Each claim has `claim_id`, `statement`, `role` (`supports`, `opposes`, `context`), `finding_refs` (array of objects with `report_id` and `finding_id`), and `unknown_reason` (string or null). A material claim has at least one valid finding reference, or a non-empty `unknown_reason`. A referenced `Unknown` finding stays Unknown. A claim's wording and confidence cannot exceed the referenced findings.

`analysis.size_or_impact` is either null, or an object with `estimate`, `unit`, `method`, `assumptions`, and `claim_ids`. A precise estimate is not allowed without a defensible method and source-backed input findings. `analysis` lists claim IDs for material support, opposing evidence, and constraints; narrative fields may summarize these IDs but cannot introduce untraced decisive assertions.

`recommendation.decision` is `pursue`, `explore`, `defer`, or `do_not_pursue`. It also has `confidence` (`high`, `medium`, `low`), `rationale`, `claim_ids`, `proposed_scope`, `risks`, and `validation_steps`. Every recommendation claim ID resolves. `explore` and `defer` are valid finished recommendations when evidence is insufficient. A `pursue` decision needs at least one source-backed user-demand claim with `role: supports` from the user-signals lane and must list every `role: opposes` claim in `analysis.opposing_evidence`; otherwise use `explore` or `defer`.

### 5.2 Readiness and validation

`draft` is valid with missing or limited lanes if their reasons and next steps are visible. `ready_for_decision` requires a named decision owner, a non-empty problem and recommendation rationale, at least one source-backed decision claim, explicit lane statuses, a validation step for each blocking gap, and no unresolved schema or reference errors. Readiness means reviewable, not approved and not necessarily `pursue`.

All `report_id`, `finding_id` and `claim_id` references resolve. Source traces follow claim → finding → evidence source (or inference chain) → inspected document and locator. Unknown paths terminate in a documented gap and validation step. Unsupported major schema versions are rejected. A newer minor version is accepted only when required fields remain compatible.

## 6. Anti-patterns

- Reclassifying a vendor claim as a fact during synthesis.
- Omitting a missing lane or presenting `not_applicable` without a reason.
- Treating several sources from one provenance family as independent support.
- Recommending `pursue` when user-demand evidence is missing.
- Writing a recommendation assertion that has no claim ID and trace.
- Treating `ready_for_decision` as a funding or roadmap approval.

## 7. Examples

The smallest valid shape of an honest draft is:

```json
{
  "schema_version": "1.0",
  "package_id": "OP-1",
  "status": "draft",
  "question": "Should a hypothetical product add event ROI analysis?",
  "context": {"product": "Example CRM", "target_users": ["operations"], "geography": "Example market", "as_of": "2026-09-17", "decision_owner": null},
  "problem": {"statement": "Whether users can assess event value is unconfirmed.", "alternatives": ["manual analysis"], "why_now": "A feature request prompted investigation."},
  "lanes": {
    "policy": {"status": "not_applicable", "reason": "No regulated workflow is in scope.", "report_ids": []},
    "market": {"status": "missing", "reason": "No accessible demand research yet.", "report_ids": []},
    "competitive": {"status": "missing", "reason": "Comparison has not started.", "report_ids": []},
    "user_signals": {"status": "missing", "reason": "No customer evidence supplied.", "report_ids": []}
  },
  "reports": [],
  "claims": [{"claim_id": "C1", "statement": "User demand remains unknown.", "role": "context", "finding_refs": [], "unknown_reason": "No user research has been inspected."}],
  "analysis": {"unmet_needs": [], "differentiation": [], "constraints": [], "size_or_impact": null, "assumptions": [], "opposing_evidence": [], "conflicts": [], "gaps": ["Interview target users about current analysis."]},
  "recommendation": {"decision": "defer", "confidence": "low", "rationale": "Demand evidence is missing.", "claim_ids": ["C1"], "proposed_scope": null, "risks": ["Building without demand evidence"], "validation_steps": ["Interview target users."]}
}
```

## 8. Relationship to other assets

The [Research Evidence Spec](./research-evidence.md) owns the embedded report fields. [AIC-REQ-01](../docs/requirements-planning/AIC-REQ-01.md) owns the user need, and the [research technical design](../docs/designs/2026-09-17-research-skills-technical-design.md) owns the Skill composition.
