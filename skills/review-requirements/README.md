# Review Requirements

Review one formal requirement before design begins. The skill loads the
[requirement-modeling Spec](../../specs/requirement-modeling.md) and
[requirement-quality Rule](../../rules/requirement-quality.md), checks the document
contract and applies the quality criteria. It reports findings without editing.

## Authoring and review

The [formal requirement template](../../docs/requirements-planning/templates/requirement-template.md)
is an authoring starting point. Review checks the authoritative Spec and Rule:
required metadata, six mandatory sections and conditionally required Scope,
Business Rules and Quality Attribute Scenarios. Matching headings is insufficient;
content, evidence and traceability must also pass. Retained body sections are
checked against the relative order in Spec §5.2.1; inapplicable optional or
conditional sections may be omitted.

The lightweight requirement template in `capture-work-items` creates a
`backlog-item`. Convert it into a formal requirement before using this review.

The same content criteria apply regardless of lifecycle status. Review examines
unresolved decisions throughout the document and verifies a non-blocking label
against actual impact under the Rule. Deferred implementation choices within
established constraints do not themselves constitute requirement gaps.

## Input and output

Input is one requirement path or full content. Output follows the shared
[findings-list contract](../../specs/findings-list.md), with category
`requirement-quality`. Zero findings indicates readiness for the next design layer;
the skill does not create that design or decide open business questions.

For review with iterative repair, use
[orchestrate-repair-requirements-loop](../orchestrate-repair-requirements-loop/SKILL.md).

## Full definition

See [SKILL.md](SKILL.md) for execution, boundaries and Self-Check.
