---
id: PROJECT-REQ-nn
artifact_type: requirement
lifecycle: snapshot
created_at: YYYY-MM-DD
status: draft
# Optional: priority: P0 | P1 | P2
# Optional: parent: {upstream objective or roadmap node path}
---

# Requirement: [Functional or Non-functional] {subject}

<!-- Authoring aid: specs/requirement-modeling.md and rules/requirement-quality.md
remain authoritative. Copy to a unique PROJECT-REQ-nn filename in the project's
requirement directory. Ground every value in sources; placeholders do not pass
review. Remove these comments before submission. Resolve references relative to
the destination. Preserve approved snapshots; revisions need a successor draft.
Keep all six required sections, apply conditional triggers and preserve the
relative order of retained sections defined in the Spec. -->

## Background & Value

{Problem statement or user story, at most 300 characters, without solution or technology choices.}

## Objective

{One line describing the change in the user's world, without implementation choices.}

## Scope

<!-- Required for multi-system integration, boundary ambiguity or estimated effort
over five days; otherwise optional. Remove if unused. -->

In scope: {Included capabilities and boundaries.}

Out of scope: {Explicit exclusions.}

## Business Rules

<!-- Required when rules are the deliverable, one rule serves at least two acceptance
criteria, rules form a state machine/decision table, or rules are the authority for
compliance audit. Otherwise remove if unused. Use declarative rules, stable IDs
and back-references from rule-derived acceptance criteria. -->

| id | Condition | Required outcome |
| --- | --- | --- |
| R1 | {Source-backed condition} | {Source-backed outcome} |

## Acceptance Criteria

- [ ] {Source-backed, verifiable criterion 1.}
- [ ] {Source-backed, verifiable criterion 2.}
- [ ] {Source-backed, verifiable criterion 3.}

<!-- Cite business rule IDs and quality scenario IDs when applicable. Non-functional
criteria need concrete numbers and representative conditions. Do not invent or
artificially split behavior merely to reach the minimum count. -->

## Quality Attribute Scenarios

<!-- Required for non-functional requirements or targets that shape architecture or
block release. Otherwise remove if unused. Cite scenarios from acceptance criteria.
Known rule_refs must resolve; unknown project references may explicitly be deferred
to technical design. Do not choose implementation tactics here. -->

| id | quality | source/stimulus | environment | affected artifact | response | measure | rule_refs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| QAS-01 | {Attribute} | {Actor and event} | {Representative conditions} | {Journey or contract} | {Required behavior} | {Binary or numeric threshold and conditions} | {Known Rule IDs or explicit deferral} |

## Dependencies & Prerequisites

Dependent requirements: {IDs and critical dependencies, or explicitly none.}

Preconditions: {Each condition and how it is verified, or explicitly none.}

External dependencies: {Dependencies and availability, or explicitly none.}

## Risks, Constraints & Assumptions

Risks:

- {Risk}: probability = {value}; impact = {value}; priority = {derived priority}.
  Mitigation: {Source-backed mitigation.}

Confirmed constraints:

- {Confirmed constraint 1 and its source.}
- {Confirmed constraint 2 and its source.}

Assumptions:

- {Assumption}; verification: {method}; owner: {established owner}.

<!-- The Spec requires at least one risk and two confirmed constraints. Use its
probability/impact priority convention. Ask for missing facts; do not invent
risks, constraints, owners or verification evidence to fill the template. -->

## Open Questions

<!-- Optional; remove if unused. Classify by actual impact under requirement-quality, regardless of lifecycle
status. Recording a question does not resolve it. A non-blocking item needs an
impact rationale, established owner and resolution plan. Do not invent them. -->

| Question | Blocking or non-blocking | Impact rationale | Owner | Resolution plan |
| --- | --- | --- | --- | --- |
| {Missing decision or fact} | {Classification} | {Effect on requirement and acceptance} | {Established owner} | {Agreed next step} |

## Source

- Source type: {feature request / business objective / incident / technical debt}.
- Source link or ID: {Traceable authoritative reference.}
- Decision context: {Why this requirement was selected.}

## Definition of Done

<!-- Optional process/release gates, distinct from acceptance; remove if unused. -->

- [ ] {Applicable process or quality gate.}

## Timeline

<!-- Optional; remove if unused. Use established scheduling evidence. Effort in
this repository uses Fibonacci story points; split work above 13 points. -->

{Scheduling window and source-backed effort estimate.}
