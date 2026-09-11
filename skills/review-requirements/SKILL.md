---
name: review-requirements
description: "Review an existing requirement document against its modeling Spec and canonical quality Rule before design begins. Evaluative atomic skill; outputs findings without rewriting."
description_zh: 在设计开始前依据需求建模规范和权威质量规则审查既有需求文档，只输出 findings，不改写。
tags: [review, requirements, pre-coding]
version: 2.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [review requirements, requirements review, requirements quality, check requirements, validate requirements doc]
input_schema:
  type: document-artifact
  description: Existing requirement document path or content
  artifact_type: requirements
output_schema:
  type: findings-list
  description: Zero or more requirement-quality findings
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
2. Verify the artifact type, status, parent and required/conditional sections.
3. Apply every quality criterion to the document and its cited local parent where traceability requires it.
4. Emit one finding per violation with category `requirement-quality`, precise section/criterion location and actionable suggestion.
5. If no findings remain, state that the artifact is ready for the next design layer; do not create that design.

## Input and output

Input is one existing requirement path or its full content. Output is a findings list. Zero findings is a gate result, not a score.

## Restrictions

- Do not invent requirements, metrics, risks or acceptance criteria.
- Do not use the obsolete generic `R-NN` model when the active Spec defines project requirement IDs and document sections.
- Do not mix solution architecture into requirement findings.

## Self-Check

- [ ] The active Spec and Rule were loaded.
- [ ] Required and conditionally required sections were evaluated.
- [ ] Quality scenarios were checked when the trigger applied.
- [ ] Every finding is document-grounded, precise and category-compliant.
- [ ] The requirement was not rewritten.

## Examples

### Example 1: non-functional target is vague

Input: “The API should be fast.” Expected: a `major` finding at the acceptance section requiring a measurable target and representative conditions; do not choose the number.

### Example 2: small functional change

Input: a bounded UI wording change with no architecture-significant quality attribute. Expected: do not manufacture a Quality Attribute Scenarios section; review the normal requirement contract.

## Change record

- Replaced the embedded, obsolete checklist with the canonical requirement Spec and Rule.
- Added conditional quality-scenario review while preserving findings-list output.

Version `2.0.0` reflects the authority and criteria change.
