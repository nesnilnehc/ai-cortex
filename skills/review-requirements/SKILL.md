---
name: review-requirements
description: "Review an existing requirement document against its modeling Spec and canonical quality Rule before design begins. Evaluative atomic skill; outputs findings without rewriting."
version: 2.2.0
license: MIT
output_schema:
  type: findings-list
---

# Skill: Review Requirements

## Purpose

Evaluate an existing requirement against [requirement-modeling](../../specs/requirement-modeling.md) and [requirement-quality](../../rules/requirement-quality.md). Emit [findings-list](../../specs/findings-list.md) output; do not author or rewrite the requirement.

## Core objective

Decide whether the requirement is a safe, testable and traceable input to design, including measurable quality-attribute scenarios when their trigger applies.

## Scope boundaries

This Skill reviews one requirement artifact. It does not elicit needs, design a solution, review code, approve open decisions or repair the document.

## Use cases

- Immediately after a requirement draft, before functional or technical design
- After a requirement changes and downstream impact must be re-evaluated
- Before adopting an externally authored requirement into the repository

## Behavior

1. Load the modeling Spec and quality Rule in full.
2. Verify the artifact type, frontmatter contract and required/conditional sections against the Spec. Check retained body sections against the relative order in Spec §5.2.1, allowing omission only according to section applicability. Check status-dependent metadata as structural compliance, not as a content-quality exemption.
3. Apply every quality criterion to the document and its cited local parent where traceability requires it.
4. Apply the Rule's unresolved-decision criteria across the whole document, including placeholders, assumptions and deferred acceptance targets. Verify the actual effect of each open item rather than trusting its blocking/non-blocking label. Distinguish missing requirement decisions from design choices that remain within established constraints.
5. Emit one finding per violation with category `requirement-quality`, precise section/criterion location and actionable suggestion.
6. If no findings remain, state that the artifact is ready for the next design layer; do not create that design.

## Input and output

Input is one existing requirement path or its full content. Output is a findings list. Zero findings is a gate result, not a score.

The [formal requirement template](../../docs/requirements-planning/templates/requirement-template.md)
is an authoring aid. Review against the active Spec and Rule, not a literal
template match; placeholders and matching headings do not establish compliance.
The `capture-work-items` requirement template produces a backlog item, which is
not the formal requirement artifact reviewed here.

## Restrictions

- Do not invent requirements, metrics, risks or acceptance criteria.
- Do not use the obsolete generic `R-NN` model when the active Spec defines project requirement IDs and document sections.
- Do not mix solution architecture into requirement findings.

## Self-Check

- [ ] The active Spec and Rule were loaded.
- [ ] Required and conditionally required sections were evaluated, and retained sections follow the Spec’s relative order.
- [ ] Quality scenarios were checked when the trigger applied.
- [ ] The same content criteria were applied regardless of lifecycle status.
- [ ] Unresolved decisions were checked throughout the document; non-blocking labels and deferred design choices were verified against their actual impact.
- [ ] Every finding is document-grounded, precise and category-compliant.
- [ ] The requirement was not rewritten.

## Examples

### Example 1: non-functional target is vague

Input: “The API should be fast.” Expected: a `major` finding at the acceptance section requiring a measurable target and representative conditions; do not choose the number.

### Example 2: small functional change

Input: a bounded UI wording change with no architecture-significant quality attribute. Expected: do not manufacture a Quality Attribute Scenarios section; review the normal requirement contract.

### Example 3: unresolved business rule under different statuses

Input: eligibility is "to be decided", marked non-blocking, in either a draft or
an approved requirement. Expected: the same `major` finding because eligibility
and its acceptance result are indeterminate. An owner and a resolution date do
not resolve the rule; do not choose the rule on the user's behalf.

### Example 4: deferred implementation choice

Input: the requirement establishes retention duration, deletion behavior and
verifiable acceptance conditions, while the storage engine is left to technical
design. Expected: do not report the implementation choice itself as an unresolved
requirement decision. Check that the established constraints remain sufficient.

### Example 5: section order

Input: Scope appears after Acceptance Criteria. Expected: a `minor` finding
identifying the misplaced section and its required position under Spec §5.2.1.
If Scope is inapplicable and omitted, do not emit an ordering finding for its
absence. Evaluate missing applicable sections and content defects separately.
