---
name: review-requirements
description: "Review an existing requirements document for quality: problem clarity, testable needs, constraint inventory, scope boundedness, requirement IDs, and open questions. Evaluative atomic skill; output is a findings list."
description_zh: 审查既有需求文档质量：问题清晰度、可测试需求、约束清单、范围边界、需求 ID 与遗留问题。
tags: [code-review]
version: 1.0.4
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [review requirements, requirements review, requirements quality, check requirements, validate requirements doc, requirements check]
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

Evaluate an **existing requirements document** against defined quality criteria. Does not produce or rewrite requirements; authoring is carried by the runtime, per [docs/requirements-planning/README.md](../../docs/requirements-planning/README.md). Emit a **findings list** so the author can improve the document before design starts or before a review.

---

## Core Objective

**Primary goal**: produce a requirement-quality findings list that names the gaps across all six quality dimensions, so the author can reach a reviewable standard before handing off to design.

**Success criteria** (all must hold):

1. ✅ **All six dimensions reviewed**: problem clarity, testability, constraint inventory, scope boundedness, requirement IDs, and open questions are assessed
2. ✅ **Findings confined to the document**: reviews only what the supplied document contains; no outside assumptions, no generative additions
3. ✅ **Findings format compliant**: each finding carries location, category (`requirement-quality`), severity, title, description, and an optional suggestion
4. ✅ **Locations cited precisely**: every finding names a specific section of the document or a requirement ID (not a vague description)
5. ✅ **Actionable output**: every finding gives a concrete direction for improvement, keyed to the relevant section or ID

**Acceptance** test: can the author read the findings list, know exactly which section or requirement to fix, and understand what "fixed" looks like - without asking a clarifying question?

---

## Scope Boundaries

**This skill owns**:

- Assessing the clarity of the problem statement (free of solution/technology references)
- Verifying that every requirement has testable acceptance criteria
- Checking the constraint inventory for completeness (real constraints separated from assumptions)
- Assessing scope boundedness (V1 boundary, deferred items, open questions present)
- Verifying requirement ID format and uniqueness (R-01, R-02, ...)
- Identifying open questions that are missing or unspecified

**This skill does not own**:

- Producing or rewriting requirements — use `capture-work-items`
- Designing from the requirements — carried by the AgentFabric runtime
- Reviewing code, architecture, or implementation — use the `review-*` family of skills

**Handoff point**: once the findings are emitted, hand them to the author to close the gaps, or confirm the document is finding-free and hand it to the AgentFabric runtime for the downstream design workflow.

---

## Use Cases

- **Pre-design gate**: validate the requirements document before it is handed to the design stage.
- **Collaborative review**: one team member writes the requirements; another runs this skill to assess quality.
- **Imported requirements**: the requirements were written outside this workflow (e.g. Confluence, Notion, Jira); a quality assessment is needed before they are used.
- **Post-authoring validation**: run after the requirements are written as an independent check that all success criteria are met.

---

## Behavior

### Interaction policy

- **Default**: take the document as supplied; do not ask the author for what is missing — emit a finding instead.
- **Rewriting is forbidden**: state what is missing or wrong; never rewrite the requirement text on the author's behalf.
- **Confirm only when the input is unclear**: if the input is not a requirements document (a design document, say), clarify before continuing.

### Review checklist (six quality dimensions)

For each dimension, scan the whole document and emit a finding for every violation found:

1. **Problem clarity**
   - Is there a problem statement describing who hits what problem and why it matters?
   - Does the problem statement stay clear of solution or technology references?
   - Is the problem statement distinct from the needs/requirements list?

2. **Testability of requirements**
   - Does every requirement (Must Have, Should Have, Could Have) carry explicit acceptance criteria?
   - Are the acceptance criteria concrete (Given/When/Then, or a measurable metric) rather than adjective-based ("fast", "simple", "intuitive")?
   - Can each requirement be verified independently by a third party?

3. **Constraint inventory**
   - Is there an explicit constraint inventory section (or equivalent)?
   - Are real constraints (budget, time, skills, dependencies) separated from unvalidated assumptions?
   - Can every constraint and assumption be traced to a source or a validation plan?

4. **Scope boundedness**
   - Is the V1 boundary stated explicitly (in scope vs out of scope)?
   - Do deferred items list the trigger for reconsidering them?
   - Is a walking skeleton or minimal viable version described?

5. **Requirement IDs**
   - Does every requirement carry a unique ID in the form "R-NN" (e.g. R-01, R-02)?
   - Are the IDs sequential, with no gaps or duplicates?
   - Do all cross-references in the document use the ID rather than a free-text description?

6. **Open questions**
   - Is there an open questions section (or equivalent)?
   - Does each open question have a resolution plan or an owner?
   - Are there implicit unknowns in the requirement text that belong in open questions, stated explicitly?

### Severity guidance

|Severity |When to use |
| :--- | :--- |
| `critical` |Problem statement missing; no acceptance criteria for any Must Have requirement; no scope definition |
| `major` |Acceptance criteria present but untestable (adjectives only); constraint inventory missing; no V1 boundary |
| `minor` |Some requirements lack an ID; some acceptance criteria are incomplete; assumptions not separated|
| `suggestion` |Open questions could be more explicit; IDs not sequential; small wording improvements |

---

## Input & Output

### Input

- **Requirements document**: a file path (`docs/requirements-planning/<topic>.md`, for example) or the raw content pasted inline.
- **Optional context**: project name, target audience, or what consumes the document downstream (for example "this feeds a technical design").

### Output

- Emit zero or more **findings** in the format defined in [specs/findings-list.md](../../specs/findings-list.md), with **Category** `requirement-quality`.
- The category for every finding from this skill is **requirement-quality**.
- With no findings: emit the short confirmation "The requirements document meets all six quality dimensions. Ready for the design stage."

---

## Restrictions

### Hard Boundaries

- **Do not rewrite**: do not produce new requirement text, acceptance criteria, or problem statements. Emit findings with a suggestion; leave the authoring to the user, or to the runtime workflow that carries it (see [docs/requirements-planning/README.md](../../docs/requirements-planning/README.md)).
- **Do not add scope**: do not invent missing requirements or widen the document's scope.
- **Document only**: base findings on the supplied document alone. Do not add findings drawn from outside knowledge of what a requirements document "should" contain beyond the six dimensions.

### Skill Boundaries

**Do not do these** (other skills handle them):

- Do not elicit, clarify, or rewrite requirements — use `capture-work-items`
- Do not design from the requirements — carried by the AgentFabric runtime
- Do not review code, architecture, or implementation quality — use `orchestrate-code-review`, `review-architecture` and so on

**When to stop and hand off**:

- Once all findings are emitted, hand them to the author to close the gaps
- When the document draws zero findings, confirm it is ready and name the design stage as the next step
- When the input is not a requirements document, clarify and redirect to the appropriate skill

---

## Self-Check

### Core success criteria

- [ ] **All six dimensions reviewed**: problem clarity, testability, constraint inventory, scope boundedness, requirement IDs, and open questions are assessed
- [ ] **Findings confined to the document**: no outside assumptions; findings based on the supplied document alone
- [ ] **Findings format compliant**: each finding carries location, category (`requirement-quality`), severity, title, description, and an optional suggestion
- [ ] **Locations cited precisely**: every finding names a specific section heading or requirement ID
- [ ] **Actionable output**: every finding states what is wrong and what to improve

### Process quality checks

- [ ] Was every requirement (Must Have, Should Have, Could Have) scanned for acceptance criteria?
- [ ] Was the problem statement checked for solution/technology language?
- [ ] Was the separation of real constraints from assumptions checked explicitly?
- [ ] Were all requirement IDs checked for uniqueness and format (R-NN)?
- [ ] Were the open questions checked for resolution plans?

### Acceptance test

**Can the author read the findings list, know exactly which section or requirement ID to fix, and understand what "fixed" looks like - without asking a clarifying question?**

If no: the findings are incomplete or imprecise. Add location references and a concrete suggestion.

If yes: the findings are ready. Hand them to the author for improvement, or confirm the document is ready for the design stage.

---

## Examples

### Example 1: Must Have requirement missing acceptance criteria

**Input**: a requirements document with 5 Must Have items; 3 of them have no acceptance criteria.

**Expected finding**:

```markdown
- **Location**: `## Need Hierarchy / Must Have / R-02`
- **Category**: requirement-quality
- **Severity**: major
- **Title**: Must Have requirement lacks acceptance criteria
- **Description**: R-02 ("Users can export data") has no acceptance criteria. Without a testable criterion, this requirement cannot be verified or designed against.
- **Suggestion**: Add acceptance criteria in the form "Given [context], when [action], then [outcome]". Example: "Given a user has at least one dataset, when they click Export, then a CSV file is downloaded within 3 seconds."
```

### Example 2: problem statement references a solution

**Input**: the problem statement reads "We need a React app with a PostgreSQL database, because users cannot track inventory."

**Expected finding**:

```markdown
- **Location**: `## Problem Statement`
- **Category**: requirement-quality
- **Severity**: major
- **Title**: Problem statement contains solution references
- **Description**: "React app" and "PostgreSQL database" are technology choices, not problem descriptions. The problem statement should describe the pain without referencing solutions.
- **Suggestion**: Rewrite as: "Small business owners lose inventory data due to manual tracking limitations. They need a reliable way to track and query inventory across devices."
```

### Example 3: no scope definition

**Input**: a requirements document with 10 requirements, no in-scope/out-of-scope section, and no V1 boundary.

**Expected finding**:

```markdown
- **Location**: (document-level — no scope section present)
- **Category**: requirement-quality
- **Severity**: critical
- **Title**: No scope definition or V1 boundary
- **Description**: The document lists requirements but does not define what is in scope for V1, what is deferred, or what a minimal useful version looks like. Without scope boundaries, design and implementation have no stopping condition.
- **Suggestion**: Add a "## Scope Definition" section with explicit In scope (V1), Out of scope, and Walking skeleton entries.
```

### Edge case: complete document, zero findings

**Input**: a requirements document that satisfies everything — problem statement, testable acceptance criteria for all requirements, constraint inventory, V1 scope, unique validated R-NN IDs, and open questions with resolution plans.

**Expected output**:

> The requirements document meets all six quality dimensions. Every Must Have requirement has testable acceptance criteria; the problem statement is free of solutions; constraints and assumptions are separated; V1 scope is explicit; all requirements carry an R-NN ID; open questions have resolution plans. Ready for the design stage.
