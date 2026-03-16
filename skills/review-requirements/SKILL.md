---
name: review-requirements
description: "Review an existing requirements document for quality: problem clarity, testable needs, constraint inventory, scope boundedness, requirement IDs, and open questions. Evaluative atomic skill; output is a findings list."
tags: [eng-standards]
related_skills: [analyze-requirements, design-solution]
version: 1.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [review requirements, requirements review, requirements quality]
input_schema:
  type: document-artifact
  description: Existing requirements document (path or content) to evaluate
  artifact_type: requirements
output_schema:
  type: findings-list
  description: Zero or more findings with location, category, severity, and suggestion covering all six requirements quality dimensions
---

# Skill: Review Requirements

## Purpose

Evaluate an **existing requirements document** against a defined quality standard. Do not generate or rewrite requirements; those are `analyze-requirements` responsibilities. Emit a **findings list** so the author can improve the document before design begins or before review gates.

---

## Core Objective

**Primary Goal**: Produce a requirements-quality findings list that identifies gaps across all six quality dimensions, enabling the author to reach a reviewable standard before handing off to design.

**Success Criteria** (ALL must be met):

1. ✅ **All six dimensions reviewed**: Problem clarity, testability, constraint inventory, scope boundedness, requirement IDs, and open questions are assessed
2. ✅ **Document-scoped findings only**: Only content in the provided document is reviewed; no external assumptions or generative additions
3. ✅ **Findings format compliant**: Each finding includes Location, Category (`requirements-quality`), Severity, Title, Description, and optional Suggestion
4. ✅ **Location-precise references**: All findings reference specific section or requirement ID in the document (not vague descriptions)
5. ✅ **Actionable output**: Each finding provides a concrete improvement direction referencing the relevant section or ID

**Acceptance Test**: Can the author read the findings list, know exactly which section or requirement to fix, and understand what "fixed" looks like — without asking clarifying questions?

---

## Scope Boundaries

**This skill handles**:

- Evaluating problem statement clarity (free of solution/technology references)
- Verifying each requirement has a testable acceptance criterion
- Checking constraint inventory completeness (real constraints vs. assumptions separated)
- Assessing scope boundedness (V1 boundary, deferred items, open questions present)
- Validating requirement ID format and uniqueness (R-01, R-02, ...)
- Identifying missing or under-specified open questions

**This skill does NOT handle**:

- Generating or rewriting requirements — use `analyze-requirements`
- Producing a design from requirements — use `design-solution`
- Reviewing code, architecture, or implementation — use the `review-*` code skills
- Full requirements elicitation or diagnostic state progression (RA0–RA5) — use `analyze-requirements`

**Handoff point**: When findings are emitted, hand off to the author to fix gaps using `analyze-requirements`, or confirm the document is finding-free and proceed to `design-solution`.

---

## Use Cases

- **Pre-design gate**: Verify a requirements document before handing off to `design-solution`.
- **Collaborative review**: A team member authored requirements; another party runs this skill to assess quality.
- **Imported requirements**: Requirements were written outside this workflow (e.g. Confluence, Notion, Jira); need quality assessment before use.
- **Post-`analyze-requirements` validation**: Run after `analyze-requirements` as an independent check that all success criteria were met.

---

## Behavior

### Interaction Policy

- **Defaults**: Accept the document as provided; do not ask the author to supply missing content — emit a finding instead.
- **No rewriting**: State what is missing or incorrect; never rewrite requirement text on the author's behalf.
- **Confirm only if ambiguous input**: If the input is not a requirements document (e.g. a design doc), clarify before proceeding.

### Review checklist (six quality dimensions)

For each dimension, scan the entire document and emit findings for all violations found:

1. **Problem clarity**
   - Does a problem statement exist that describes who has what problem and why it matters?
   - Does the problem statement avoid solution or technology references?
   - Is the problem statement distinct from the need/requirement list?

2. **Testability of needs**
   - Does every requirement (Must Have, Should Have, Could Have) have explicit acceptance criteria?
   - Are acceptance criteria concrete (Given/When/Then or measurable metric) rather than adjective-based ("fast", "easy", "intuitive")?
   - Can each requirement be independently verified by a third party?

3. **Constraint inventory**
   - Is there an explicit constraint inventory section (or equivalent)?
   - Are real constraints (budget, time, skills, dependencies) separated from unvalidated assumptions?
   - Are all constraints and assumptions traceable to a source or validation plan?

4. **Scope boundedness**
   - Is the V1 boundary explicitly stated (in-scope vs. out-of-scope)?
   - Are deferred items listed with triggers for reconsidering?
   - Is a walking skeleton or minimum viable version described?

5. **Requirement IDs**
   - Does every requirement have a unique ID in the format `R-NN` (e.g. R-01, R-02)?
   - Are IDs sequential with no gaps or duplicates?
   - Do all cross-references in the document use IDs rather than free-text descriptions?

6. **Open questions**
   - Is there an open questions section (or equivalent)?
   - Does each open question have a resolution plan or owner?
   - Are there implicit unknowns in the requirement text that should be made explicit as open questions?

### Severity guidance

| Severity | When to use |
| :--- | :--- |
| `critical` | Missing problem statement; no acceptance criteria on any Must Have requirement; no scope definition |
| `major` | Acceptance criteria present but untestable (adjective-only); constraint inventory missing; no V1 boundary |
| `minor` | Some requirements missing IDs; some acceptance criteria incomplete; assumptions not separated |
| `suggestion` | Open questions could be more explicit; IDs non-sequential; minor wording improvements |

---

## Input & Output

### Input

- **Requirements document**: Path to a file (e.g. `docs/requirements-planning/<topic>.md`) or raw content pasted inline.
- **Optional context**: Project name, intended audience, or downstream skill (e.g. "this will feed design-solution").

### Output

- Emit zero or more **findings** in the format defined in **Appendix: Output contract**.
- Category for all findings from this skill is **requirements-quality**.
- If no findings: emit a brief "Requirements document meets all six quality dimensions. Ready for `design-solution`." confirmation.

---

## Restrictions

### Hard Boundaries

- **Do not rewrite**: Do not generate new requirement text, acceptance criteria, or problem statements. Emit a finding with a suggestion; leave authoring to the user or `analyze-requirements`.
- **Do not add scope**: Do not invent missing requirements or extend the scope of the document.
- **Document-only**: Only findings grounded in the provided document. Do not add findings based on external knowledge about what requirements "should" contain beyond the six dimensions.

### Skill Boundaries

**Do NOT do these** (other skills handle them):

- Do NOT elicit, clarify, or rewrite requirements — use `analyze-requirements`
- Do NOT produce a design from requirements — use `design-solution`
- Do NOT review code, architecture, or implementation quality — use `review-code`, `review-architecture`, etc.
- Do NOT run the full RA0–RA5 diagnostic state progression — use `analyze-requirements`

**When to stop and hand off**:

- When all findings are emitted, hand off to the author to fix gaps (optionally using `analyze-requirements`)
- When the document has zero findings, confirm it is ready and suggest `design-solution` as the next step
- When the input is not a requirements document, clarify and redirect to the appropriate skill

---

## Self-Check

### Core Success Criteria

- [ ] **All six dimensions reviewed**: Problem clarity, testability, constraint inventory, scope boundedness, requirement IDs, and open questions are assessed
- [ ] **Document-scoped findings only**: No external assumptions; only findings grounded in the provided document
- [ ] **Findings format compliant**: Each finding includes Location, Category (`requirements-quality`), Severity, Title, Description, and optional Suggestion
- [ ] **Location-precise references**: All findings reference a specific section heading or requirement ID
- [ ] **Actionable output**: Each finding states what is wrong and what improvement looks like

### Process Quality Checks

- [ ] Was every requirement (Must Have, Should Have, Could Have) scanned for acceptance criteria?
- [ ] Was the problem statement checked for solution/technology language?
- [ ] Were real constraints and assumptions explicitly checked for separation?
- [ ] Were all requirement IDs checked for uniqueness and format (R-NN)?
- [ ] Were open questions checked for resolution plans?

### Acceptance Test

**Can the author read the findings list, know exactly which section or requirement ID to fix, and understand what "fixed" looks like — without asking clarifying questions?**

If NO: Findings are incomplete or imprecise. Add location references and concrete suggestions.

If YES: Findings are ready. Hand off to author for improvement or confirm document is ready for `design-solution`.

---

## Examples

### Example 1: Missing acceptance criteria on Must Have requirements

**Input**: Requirements document with 5 Must Have items; 3 of them have no acceptance criteria.

**Expected findings**:

```markdown
- **Location**: `## Need Hierarchy / Must Have / R-02`
- **Category**: requirements-quality
- **Severity**: major
- **Title**: Must Have requirement lacks acceptance criteria
- **Description**: R-02 ("Users can export data") has no acceptance criteria. Without a testable criterion, this requirement cannot be verified or designed against.
- **Suggestion**: Add acceptance criteria in the form "Given [context], when [action], then [outcome]". Example: "Given a user has at least one dataset, when they click Export, then a CSV file is downloaded within 3 seconds."
```

### Example 2: Problem statement references a solution

**Input**: Problem statement reads "We need a React app with a PostgreSQL database because users can't track inventory."

**Expected findings**:

```markdown
- **Location**: `## Problem Statement`
- **Category**: requirements-quality
- **Severity**: major
- **Title**: Problem statement contains solution references
- **Description**: "React app" and "PostgreSQL database" are technology choices, not problem descriptions. The problem statement should describe the pain without referencing solutions.
- **Suggestion**: Rewrite as: "Small business owners lose inventory data due to manual tracking limitations. They need a reliable way to track and query inventory across devices."
```

### Example 3: No scope definition

**Input**: Requirements document with 10 requirements but no in-scope / out-of-scope section and no V1 boundary.

**Expected findings**:

```markdown
- **Location**: (document-level — no scope section present)
- **Category**: requirements-quality
- **Severity**: critical
- **Title**: No scope definition or V1 boundary
- **Description**: The document lists requirements but does not define what is in scope for V1, what is deferred, or what a minimal useful version looks like. Without scope boundaries, design and implementation have no stopping condition.
- **Suggestion**: Add a "## Scope Definition" section with explicit In scope (V1), Out of scope, and Walking skeleton entries.
```

### Edge case: Document is complete and has zero findings

**Input**: Fully validated requirements document with problem statement, testable acceptance criteria for all requirements, constraint inventory, V1 scope, unique R-NN IDs, and open questions with resolution plans.

**Expected output**:

> Requirements document meets all six quality dimensions. All Must Have requirements have testable acceptance criteria; problem statement is solution-free; constraints and assumptions are separated; V1 scope is explicit; all requirements carry R-NN IDs; open questions have resolution plans. Ready for `design-solution`.

---

## Appendix: Output contract

Each finding MUST follow the standard findings format:

| Element | Requirement |
| :--- | :--- |
| **Location** | Section heading (e.g. `## Problem Statement`) or requirement ID (e.g. `R-03`) or `(document-level)` if no specific anchor exists. |
| **Category** | `requirements-quality`. |
| **Severity** | `critical` \| `major` \| `minor` \| `suggestion`. |
| **Title** | Short one-line summary. |
| **Description** | 1–3 sentences explaining the issue. |
| **Suggestion** | Concrete improvement direction (optional but strongly recommended). |

Example:

```markdown
- **Location**: `## Constraint Inventory`
- **Category**: requirements-quality
- **Severity**: minor
- **Title**: Assumptions not separated from real constraints
- **Description**: The constraint list mixes validated facts (e.g. "team has 3 engineers") with unvalidated assumptions (e.g. "users will have mobile devices"). Without separation, risk is hidden.
- **Suggestion**: Split into two sub-sections: "Real Constraints (Validated)" and "Assumptions (Unvalidated — need validation plan)".
```
