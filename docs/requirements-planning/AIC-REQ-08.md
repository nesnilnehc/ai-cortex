---
id: AIC-REQ-08
artifact_type: requirement
lifecycle: snapshot
created_at: 2026-10-28
status: approved
parent: ../project-overview/strategic-goals.md#goal-4-adoption-friction-is-low
---

# Requirement: [Functional] Skill provenance presentation

## Background & Value

Users cannot reliably distinguish repository-original Skills from unchanged or adapted third-party copies, and repeated editable claims can drift.

## Objective

Users can identify evidenced Skill provenance in the index and website without treating provenance as a quality certification.

## Scope

Index and website provenance presentation, recorded source evidence, consistent classification and maintainer confirmation guidance. Excludes a provenance field in every Skill body, blanket authorship claims, runtime downloads and a security certification.

## Business Rules

| ID | Condition | Required behavior |
| --- | --- | --- |
| R1 | A Skill is presented in the index or website | Record exactly one evidenced classification: AI Cortex original, third-party original or third-party adapted. Confirmed AI Cortex originals have no display badge; both third-party categories show their respective text badges. Every Skill must have its provenance investigated and classified before acceptance; an unresolved record fails validation rather than producing a fourth label, hiding an unresolved classification or defaulting to original. |
| R5 | A Skill is labeled AI Cortex original | It was built from scratch in this repository without external creative reference, supported by a creation commit or related requirement record and an explicit maintainer confirmation. Git history alone does not prove absence of external reference; absolute proof is not required. Consulting API parameters or command usage alone does not affect original status. |
| R2 | An upstream copy is labeled original | All distributed Skill files must match the pinned upstream version; any local change makes it adapted. |
| R3 | A Skill is displayed on the website | For third-party categories, show the short provenance text at the upper right without obscuring name or purpose; use text as well as color. Confirmed originals omit that text badge. Keep recorded classification evidence in repository maintenance records; do not display audit-material links on the website. |
| R4 | The same Skill appears in different surfaces | Index and website derive claims from the same authority; individual Skill bodies need not repeat display labels. |
| R6 | External content informed a Skill's method, workflow or expression | If all distributed files match the pinned upstream version under R2, classify it as third-party original. Otherwise classify it as third-party adapted, including copied-and-modified content and independent rewrites based on external Skills, articles, methods or workflows. Record actual sources and the local adaptation; a source need not be a Skill repository or have a comparable upstream file version. Tool documentation consulted only for API parameters or command usage is not creative reference. |
| R7 | Maintainer confirmation is needed | Present the Skill and version under review, creation records, discovered sources and their role, relevant comparison or modification evidence, missing facts, a recommended classification and its rationale. Ask the maintainer to confirm or correct the recommendation, explicitly addressing external creative reference and tool-documentation-only use. Record the maintainer identity, confirmation date, decision, rationale and evidence references; a recommendation is not a confirmation, and unresolved facts prevent acceptance. |

## Acceptance Criteria

- [x] Examples for all three evidenced categories render consistently in the index and website: confirmed originals have no badge, while both third-party categories have visible text badges. Every Skill in the delivery scope has a reviewed, evidenced classification and repository-accessible evidence; missing or unresolved classification fails validation. No fourth provenance category or unresolved unlabeled fallback is accepted. Covers R1 and R4.
- [x] An original-classification case includes a creation commit or related requirement record and an explicit maintainer confirmation that no external creative reference was used. A Git-history-only case fails the evidence check; consulting tool documentation solely for API parameters or command usage does not disqualify original status. Covers R5.
- [x] Cases for a copied-and-modified Skill and an independent rewrite informed by an external article, method or workflow are classified as third-party adapted, with actual source references and local adaptation recorded, including a source without an upstream Skill repository or comparable file version. Covers R6.
- [x] A maintainer confirmation request includes every review point in R7 and a reasoned recommendation. Confirmation and correction cases preserve the maintainer identity, date, final decision, rationale and evidence references; an unanswered request or recommendation alone cannot satisfy acceptance. Covers R7.
- [x] A complete copy whose distributed files all match the pinned upstream version is classified as third-party original, not third-party adapted. Changing, adding or removing a distributed upstream file invalidates the unchanged classification until the record is corrected. Covers R2 and R6.
- [x] At 360px and 1280px in light/dark themes, provenance text is readable and does not overlap the Skill name or purpose; no audit-material links are displayed. Covers R3 and QAS-01.
- [x] Registry conflicts fail validation; presentation changes do not fetch upstream or alter Skill execution behavior. Covers R4.

## Quality Attribute Scenarios

| id | quality | source/stimulus | environment | affected artifact | response | measure | rule_refs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| QAS-01 | accessibility | A user reads a displayed third-party provenance claim | Website at 360px and 1280px in light and dark themes | Skill provenance display | Provide readable classification text without audit-material links or obscuring the Skill name or purpose | At both widths and in both themes, text is readable and does not overlap the name or purpose; no audit-material links are rendered | Resolve applicable engineering Rule IDs during design |

## Dependencies & Prerequisites

No requirement dependencies. Existing provenance implementation and eli5/Ponytail intake are starting evidence, not final acceptance. Before acceptance, maintainers must complete the provenance review for every Skill in scope; verify this by checking full catalogue coverage and the evidence supporting each classification.


## Risks, Constraints & Assumptions

- Incorrect completion or provenance claim: probability medium, impact high, priority high. Mitigation: preserve source evidence and verify the negative cases in acceptance fixtures.
- Current experimental documents are proposals, not approved contracts. No remote write, deployment or consumer-project release is authorized by this requirement.

## Open Questions

None. The classification and evidence standards are settled; per-Skill investigation and maintainer confirmation are delivery work under R5–R7. eli5 and Ponytail intake closeout is a maintenance task, not a separate requirement.

## Source

Feature request: user-directed split on 2026-10-28 in chat `01a1803e-9883-7aa0-b887-8861238d233f`. See the [provenance proposal](../../experiments/skill-provenance/proposal.md) and [existing source contract](../../specs/skill-source-modeling.md). In the requirement review, the user defined AI Cortex original as built entirely from scratch in this repository without reference to external material.

The user subsequently required a visible provenance badge for every Skill and rejected an unconfirmed-source category. All Skills must therefore have an evidenced classification in one of the three categories before acceptance. This supersedes both hiding labels for insufficient evidence and displaying an unconfirmed-source fallback.

The user approved creation records plus explicit maintainer confirmation as the original-authorship evidence standard, and classified external creative reference as adaptation while exempting tool-documentation-only consultation. Confirmation requests must provide review points and a reasoned recommendation. These decisions must be reconciled with the existing source contract during subsequent design and implementation, including support for sources without upstream Skill files.

The user approved this requirement after the final review correction: an upstream-identical distribution is third-party original under R2 and is explicitly excluded from the adapted classification in R6. Requirement approval authorizes downstream design, not implementation completion or external publication.

### Display amendment — 2026-10-28

The user subsequently requested that originals omit redundant badges. This supersedes the earlier all-Skill visible-badge decision above. Classification, evidence and maintainer confirmation remain mandatory for every Skill; only confirmed `native` records omit the display badge. Third-party original and adapted badges remain visible. An absent badge alone does not prove originality.

Implementation and acceptance evidence: [REQ 08 delivery closeout](../../experiments/skill-provenance/delivery-closeout.md).

### Website display amendment — 2026-10-29

The user removed audit-material links from the website. This supersedes earlier website evidence-navigation requirements. Third-party text badges remain; originals remain unbadged. Evidence validation and repository maintenance records are unchanged.

### Original-source navigation amendment — 2026-10-29

The user approved linking both third-party classification badges to their actual original sources. A single source opens in a new tab; multiple sources expand a titled link list. This applies to all website Skill surfaces and static fallbacks. Audit-material links remain hidden, originals remain unbadged, and classification confirmation is unchanged. Covers R3 and AC6.
