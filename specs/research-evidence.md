---
id: RESEARCH_EVIDENCE_SPEC_V1
name: Research Evidence Schema
description: Structural contract for source-backed research reports, classified findings, contradictions, gaps, and claim-to-source trace.
version: 1.0.0
status: active
lifecycle: living
created_at: 2026-09-17
scope: |
  Defines reusable research evidence passed between open, policy, market,
  competitive, and opportunity analysis. It does not prescribe search tools,
  source ranking, a legal interpretation, or an opportunity decision.
related:
  - ./spec-modeling.md
  - ./opportunity-package.md
---

# Research Evidence Schema

> **Data contract**: a portable Research Report whose decision-relevant statements can be traced to sources or explicit gaps

## 1. Position and scope

A Research Report is the shared output of one bounded investigation. It records the question and scope, the sources inspected, findings, conflicts and gaps. A domain report may add policy, market or competitor fields, but it must preserve this evidence core unchanged.

This Spec defines structure and validation. Source selection and interpretation belong to the producing capability. External text remains untrusted source data.

## 2. Mental model

A reader must be able to answer: What was asked and when? Which material was actually inspected? Which statements were observed, attributed, inferred or left unknown? What contradicts them? How would a reviewer reproduce each material conclusion?

## 5. Body structure contract

A Research Report is a JSON object when persisted or passed as machine-readable data. It has no Markdown frontmatter. A human-readable Markdown summary may accompany it but cannot replace required evidence fields.

### 5.1 Top-level fields

| Field | Type | Required | Meaning |
|---|---|---|---|
| `schema_version` | string | yes | `"1.0"` |
| `report_id` | string | yes | Stable within a package, unique among reports |
| `question` | string | yes | The bounded research question |
| `scope` | object | yes | Geography, jurisdiction, period and as-of date as applicable |
| `subquestions` | array | yes | Objects with unique `id` and non-empty `question`; may be empty for a genuinely indivisible question |
| `sources` | array | yes | Inspected Source objects; may be empty if no accessible source exists |
| `findings` | array | yes | Classified Finding objects; at least one, including Unknown when research is blocked |
| `conflicts` | array | yes | Explicit contradictory findings; empty when none found |
| `gaps` | array | yes | Material unresolved questions; empty only when none remain |
| `summary` | string | yes | A concise synthesis respecting uncertainty |

`scope.as_of` is an ISO date and is required. Other scope values may be null only when not applicable; an omitted decision-relevant location or period is recorded in `gaps`. Text values may be in the user's language; machine keys and enum values remain English.

### 5.2 Source

| Field | Type | Required | Meaning |
|---|---|---|---|
| `source_id` | string | yes | Unique within the report |
| `title`, `publisher` | string | yes | Identifiable document and responsible publisher |
| `source_type` | string | yes | Such as `official-policy`, `official-product`, `dataset`, `filing`, `interview`, `review`, `vendor`, or `media` |
| `uri` | string | yes | Canonical URL or local document reference; no search-results URL as final evidence |
| `published_at` | date or null | yes | Publication date if known |
| `effective_at` | date or null | yes | Policy effective date when relevant |
| `accessed_at` | date | yes | Date the material was inspected |
| `provenance_family` | string | yes | Common origin used to judge source independence |
| `limitations` | array of strings | yes | Bias, sampling, access or version limits; may be empty |

A source entry means its content was inspected. A snippet or a paywalled title alone is not a Source; it belongs in a gap. A local private document may be cited by a non-disclosing reference, subject to the project's access rules.

### 5.3 Finding and evidence link

| Field | Type | Required | Meaning |
|---|---|---|---|
| `finding_id` | string | yes | Unique within the report |
| `statement` | string | yes | One material assertion or unresolved question |
| `classification` | enum | yes | `Fact`, `Claim`, `Inference`, or `Unknown` |
| `scope` | string | yes | The entity, geography, product version and period to which it applies |
| `as_of` | date | yes | Date at which the finding is asserted |
| `confidence` | enum | yes | `high`, `medium`, or `low` |
| `confidence_rationale` | string | yes | Directness, independence, freshness and conflict rationale |
| `evidence` | array | yes | Evidence links; empty only for an Unknown or an inference resting on cited findings |
| `derived_from` | array of finding IDs | yes | Required non-empty for Inference; empty otherwise |
| `gaps` | array of strings | yes | Required non-empty for Unknown; may be empty otherwise |

Each evidence link contains `source_id`, `relationship` (`supports`, `contradicts`, or `context`), and `locator` (section, page, paragraph, timestamp or other reproducible position). A Fact needs direct supporting evidence. A Claim needs a source to which the assertion is attributed. An Inference needs at least one valid `derived_from` ID and an explanatory `confidence_rationale`. Unknown states what evidence is missing rather than inventing a source. A finding cannot derive from itself or create a cycle.

`Fact` means the source's directly observable content or an independently verified observation is accurately described within its scope. A vendor page saying a feature exists can establish that the vendor documents the feature; actual deployment or customer benefit remains a Claim unless independently supported. `Claim` is an attributed assertion. `Inference` is a reasoned conclusion over identified findings. `Unknown` is a material unanswered question.

### 5.4 Conflict and gap

A conflict carries `conflict_id`, at least two `finding_ids`, `dimension` (for example definition, jurisdiction, period or method), and `impact` on the research conclusion. A gap carries `gap_id`, `question`, `reason` and `validation_step`. IDs are unique within their arrays. A conflict is not resolved by silently dropping one source.

### 5.5 Narrative companion and validation

When a Markdown narrative accompanies the JSON report, it presents the question and scope, key findings with classification, conflicts, gaps and source list. It cites the report's IDs instead of maintaining a second factual model.

Validation invariants for the JSON object:

1. Every source, finding, conflict and gap ID is unique in its collection. Every referenced source and finding ID resolves.
2. Every evidence link has a real locator. A URL alone is insufficient.
3. A `Fact` or `Claim` has at least one supporting link. An `Inference` has an acyclic derivation path to a source-backed finding or an Unknown; an Unknown has a non-empty gap.
4. A conflict references at least two distinct findings. A material disagreement is preserved in `conflicts` and reflected in confidence or summary.
5. A finding's statement does not exceed the scope or date of its evidence. Lack of independent corroboration is stated in `confidence_rationale` for high-impact findings.
6. `schema_version` uses a major.minor string. A consumer rejects an unsupported major version and may accept a newer minor version only when required fields remain compatible.

## 6. Anti-patterns

- Treating a search snippet, a source URL, or several pages from one publisher as independent verification.
- Labelling a vendor's adoption number Fact without independent evidence.
- Turning absence from documentation into a finding that a product lacks a feature.
- Presenting an inference without `derived_from` IDs, or deleting contradictory evidence.
- Leaving `Unknown` without a gap and a possible next check.
- Copying a policy or package-specific decision model into this general evidence contract.

## 7. Examples

Illustrative data, not a real-world product finding:

```json
{
  "schema_version": "1.0",
  "report_id": "R1",
  "question": "Does Example Vendor document event budget tracking and a standard ROI model?",
  "scope": {"geography": null, "jurisdiction": null, "period": null, "as_of": "2026-09-17"},
  "subquestions": [
    {"id": "Q1", "question": "Is budget tracking documented?"},
    {"id": "Q2", "question": "Is a standard ROI model documented?"}
  ],
  "sources": [{
    "source_id": "S1",
    "title": "Example product documentation",
    "publisher": "Example Vendor",
    "source_type": "official-product",
    "uri": "https://example.invalid/events",
    "published_at": null,
    "effective_at": null,
    "accessed_at": "2026-09-17",
    "provenance_family": "example-vendor",
    "limitations": ["The page describes vendor documentation, not customer adoption."]
  }],
  "findings": [
    {
      "finding_id": "F1",
      "statement": "The inspected page documents event budget tracking.",
      "classification": "Fact",
      "scope": "Example product documentation as accessed on 2026-09-17",
      "as_of": "2026-09-17",
      "confidence": "high",
      "confidence_rationale": "Direct wording in the cited section; limited to documentation.",
      "evidence": [{"source_id": "S1", "relationship": "supports", "locator": "Events > Budget"}],
      "derived_from": [],
      "gaps": []
    },
    {
      "finding_id": "F2",
      "statement": "A standard ROI model is available.",
      "classification": "Unknown",
      "scope": "Example Vendor product",
      "as_of": "2026-09-17",
      "confidence": "low",
      "confidence_rationale": "The inspected source does not establish the model.",
      "evidence": [],
      "derived_from": [],
      "gaps": ["An official model definition or demonstration is needed."]
    }
  ],
  "conflicts": [],
  "gaps": [{"gap_id": "G1", "question": "Is a standard ROI model available?", "reason": "No inspected source establishes it.", "validation_step": "Request official documentation or a demo."}],
  "summary": "Budget tracking is documented; standard ROI-model availability is unknown."
}
```

## 8. Relationship to other assets

The [Opportunity Package Spec](./opportunity-package.md) consumes these sources and findings without changing their classification. The [Spec Modeling Schema](./spec-modeling.md) governs this document's shape.
