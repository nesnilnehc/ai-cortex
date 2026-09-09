---
id: REQUIREMENT_MODELING_SPEC_V4
name: Requirement Modeling Schema
description: Spec defining requirement document fields, formats, and validation rules. Covers frontmatter contract, 6 mandatory body sections (Background/Objective/Acceptance/Dependencies/Risks/Source), and conditionally-mandatory optional sections (Scope, Business Rules).
version: 5.0.0
status: active
lifecycle: living
created_at: 2026-03-25
scope: |
  Defines the structural contract for requirement documents: frontmatter fields, required body
  sections, optional sections, and field formats. Applies to functional requirements
  and non-functional requirements.
related:
  - ./spec-modeling.md
  - ./functional-design-modeling.md
  - ../rules/requirement-quality.md
---

# Requirement Modeling Schema

> **Data contract**: defines the field structure and body skeleton of a requirement document

---

## 1. Position and scope

A requirement document answers "what are we building" — through a user story or problem statement, verifiable acceptance criteria, dependencies and risks, it brings the team to a shared understanding of what will be delivered. It is the bridge between an upstream objective (a goal or roadmap node) and a downstream design document.

This spec is centred on acceptance criteria: business rules are inlined into the acceptance criteria by default rather than listed separately, and implementation-level scenario flows (step sequences, state-transition detail) are pushed down to the downstream design document. These omissions are deliberate and are part of the contract — they spare the author from guessing repeatedly where a rule or a scenario belongs.

In scope:

- **Functional requirements**: new features, process changes, experience improvements
- **Non-functional requirements**: performance, security, maintainability, extensibility

Out of scope:

- Exploratory research or option comparison (an ADR or an RFC)
- Internal component API design (a design document)
- One-off bug fixes or code cleanups (a commit or PR description is enough)
- Defects, technical tasks, implementation proposals and insufficient information — these are the non-requirement classes of raw intake, triaged by [rules/requirement-intake-triage.md](../rules/requirement-intake-triage.md) and not modelled as requirement documents

### 1.1 Simplification guidance by requirement type

| Type | Required sections | What may be simplified |
|---|---|---|
| Functional requirement | All 6 body sections | — |
| Non-functional requirement | All 6 body sections | — |

Risk priority and mitigation strategy are **never optional**.

---

## 3. Naming

```text
<PROJECT>-REQ-<nn>.md
```

- `<PROJECT>`: the project abbreviation (upper case, 2-6 characters, for example `ACME` / `MYAPP`)
- `<nn>`: the sequence number, at least 2 digits, monotonically increasing, and **never reused**
- Examples: `ACME-REQ-05.md` / `MYAPP-REQ-042.md`
- The storage location is decided by project governance (typically `docs/requirements/`)

---

## 4. Frontmatter contract

```yaml
---
id: <PROJECT>-REQ-<nn>
artifact_type: requirement
lifecycle: snapshot
created_at: YYYY-MM-DD
status: draft | approved | implemented | superseded
priority: P0 | P1 | P2
parent: <upstream goal / roadmap node path>
# conditional fields
superseded_by: <new-requirement-id>   # required when status: superseded
implemented_at: YYYY-MM-DD             # required when status: implemented
---
```

### 4.1 Field table

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | Yes | Format `<PROJECT>-REQ-<nn>` (for example `ACME-REQ-05`) |
| `artifact_type` | string | Yes | Fixed as `requirement` |
| `lifecycle` | enum | Yes | Fixed as `snapshot` (a requirement freezes once approved; a change creates a new requirement) |
| `created_at` | date | Yes | The date the requirement was written down |
| `status` | enum | Yes | `draft` / `approved` / `implemented` / `superseded` (semantics in §4.2) |
| `priority` | enum | Optional | `P0` (blocking path) / `P1` (critical path) / `P2` (non-critical) |
| `parent` | path | Optional | Path to the upstream objective or roadmap node |
| `superseded_by` | string | Conditional | Required when `status: superseded`; points at the successor requirement id |
| `implemented_at` | date | Conditional | Required when `status: implemented`; records the date implementation completed |

### 4.2 State machine semantics

| Status | Meaning | Entry condition |
|---|---|---|
| `draft` | Being drafted | The requirement document has just been written and has not passed review |
| `approved` | Approved | Review passed; a design document may be derived from it (as the design's `parent`) |
| `implemented` | Implemented | Every associated implementation task is `Done` and every acceptance criterion is met (`implemented_at` must be filled in) |
| `superseded` | Replaced by a newer requirement | A business change caused the requirement to be rewritten (`superseded_by` must be filled in) |

---

## 5. Body structure contract

### 5.1 Required sections (6)

Every requirement document must contain the following 6 body sections (the H1 title is not counted).

**H1 title**: `# Requirement: [type] one-line description`
- Example types: `[Functional]` / `[Non-functional]`
- The title is ≤ 80 characters and carries no technical implementation detail
- It states the subject of the requirement (a capability, a problem, a task), not the expected outcome — outcomes belong to the "Objective" section; any grammatical form is acceptable (a capability phrase, a problem statement or a constraint statement)

| # | Section | Purpose | Validation |
|---|---|---|---|
| 1 | Background & Value | Explain the problem's background and why it matters | ≤ 300 characters; carries **no** solution or technology choice; a user-story form (`As X / I want Y / so that Z`) or a problem statement (`background / desired state / impact`) is recommended |
| 2 | Objective | State how the world changes once this requirement ships | One line; states a requirement-level objective (as distinct from the upstream strategic or product objective, which is referenced through frontmatter `parent` and not repeated here); carries **no** solution or technology choice |
| 3 | Acceptance Criteria | Define the verifiable conditions under which the requirement is complete | ≥ 3 of them; each verifiable automatically or by hand; **no** vague adjectives ("fast" / "reasonable" / "friendly"); a non-functional requirement carries concrete numbers (for example latency ≤ 500ms) |
| 4 | Dependencies & Prerequisites | Dependency relationships and preconditions | Covers 3 kinds: dependent requirement IDs / preconditions (with how each is verified) / external dependencies; the dependency graph is acyclic; when there is no dependency, write "no dependencies" explicitly |
| 5 | Risks, Constraints & Assumptions | Risks (probability × impact) / confirmed constraints / assumptions still to be verified | Functional and non-functional requirements alike: ≥ 1 risk and ≥ 2 constraints; each risk carries a priority = probability × impact; each assumption carries how it will be verified plus who owns it |
| 6 | Source | The business origin and the decision context | Carries the source type (feature request / business objective / incident / technical debt) + a source link or ID + the decision context; traceable, not "someone mentioned it" |

### 5.2 Optional sections

Add them as the situation requires:

| Section | Triggering situation |
|---|---|
| Scope | Multi-system integration, ambiguity across a boundary, or estimated effort > 5 days (any one of these makes the section **required**) |
| Business Rules | The rule set is itself the deliverable (pricing / eligibility / tax / risk scoring), a single rule is cited by ≥ 2 acceptance criteria, the rules form a state machine or decision table, or the rules must serve as the authoritative source (SSOT) for a downstream compliance audit (any one of these makes the section **required**) |
| Open Questions | Items left unresolved in review; classified as "blocking" or "non-blocking", with an owner and a plan for resolving each |
| Definition of Done | Process and quality gates (test coverage, documentation updates, deployment gates), distinct from the acceptance criteria (acceptance = the feature is complete; DoD = it is releasable) |
| Timeline | The scheduling window plus the estimated effort (for example "Phase 2, weeks 3-4 / 4 person-days") |

### 5.3 Format details

#### 5.3.1 Computing risk priority

```text
priority = probability × impact

- High priority: probability >= medium AND impact >= high
- Medium priority: (probability = medium AND impact = medium) OR (probability = high AND impact = low)
- Low priority: probability <= low OR impact <= low
```

#### 5.3.2 Recommended acceptance-criteria formats

Pick either Gherkin BDD (`Given / When / Then`) or a checklist (`- [ ] ...`). Gherkin suits behavioural requirements; a checklist suits a stack of features.

#### 5.3.3 Declarative form for business rules (once they become required)

Once business rules become required (one of the §5.2 triggers has fired):

- Express them declaratively, as a decision table or a state table; do not write procedural steps.
- Every rule carries a stable id (for example `R1` / `R2`), and ids are never reused.
- Acceptance criteria cite the rule id back (for example `Covers R3`), establishing a traceable chain from rule to acceptance.

#### 5.3.4 The boundary between business rules and acceptance criteria

- A business rule is normative: it declares "what must be true", and one rule can yield several acceptance criteria.
- An acceptance criterion is the verifiable projection of a rule: it declares "how we verify that it is true", and it also covers non-rule items such as performance, availability and the existence of an interface.
- Rule-derived acceptance criteria cite their rule id back, closing the MECE overlap between rules and acceptance.

---

## 6. Anti-patterns

- ❌ A required frontmatter field is missing (id / artifact_type / status / created_at)
- ❌ The `id` format is wrong (lower case, missing PROJECT prefix, a reused number)
- ❌ The background section carries a technology choice, an implementation path or a concrete feature description
- ❌ The title states the expected outcome rather than the subject of the requirement (duplicating the "Objective" section)
- ❌ The "Objective" section is missing, or the requirement-level objective is mixed into "Background & Value"
- ❌ Fewer than 3 acceptance criteria
- ❌ Acceptance criteria contain vague words ("should", "reasonable", "friendly", "fast")
- ❌ A non-functional requirement's acceptance criteria carry no concrete numbers
- ❌ The dependency graph contains a cycle
- ❌ The risk section is missing, or risks carry no priority
- ❌ A risk lists only its description with no mitigation strategy
- ❌ The source is vague ("someone asked for it", "we discussed it verbally")
- ❌ Status `superseded` with `superseded_by` left empty
- ❌ Status `implemented` with `implemented_at` left empty
- ❌ One of the 4 conditions that make Scope required is met, but the Scope section is missing
- ❌ One of the triggers that make Business Rules required is met, but the rules are still scattered through the acceptance criteria with no separate declarative rules section
- ❌ Business rules that have become required are expressed as procedural steps instead of a decision table or state table
- ❌ Rule-derived acceptance criteria do not cite their business rule id back, leaving the MECE overlap between rules and acceptance unclosed
- ❌ A self-check list written into the spec body (review checklists belong to [rules/requirement-quality.md](../rules/requirement-quality.md))

---

## 7. Examples

### 7.1 A complete functional requirement

````markdown
---
id: ACME-REQ-15
artifact_type: requirement
lifecycle: snapshot
created_at: 2026-04-12
status: approved
priority: P1
parent: ../roadmap/2026-q2.md#open-integration
---

# Requirement: [Functional] Semantic search API for knowledge base retrieval

## Objective

The cost for an integrator to adopt knowledge base retrieval drops from reinventing the wheel to near zero, and the official semantic search API becomes the single authoritative retrieval entry point.

## Background & Value

As a systems integrator
I want an API that runs semantic search over the stored specifications
so that external systems can retrieve relevant documents efficiently from context

The knowledge base currently supports keyword search only, so an external agent has to build its own embedding and vector recall — reinventing the wheel.

## Acceptance Criteria

- [ ] The REST API `POST /search/semantic` is implemented and answers queries
- [ ] Response time ≤ 500ms (p95) on a 10M-entry dataset
- [ ] top-3 relevance precision ≥ 80% (verified over 50+ representative queries)
- [ ] The API documentation is complete (an OpenAPI specification + 5+ examples)
- [ ] API key authentication + rate limiting (10 QPS per key by default)

## Dependencies & Prerequisites

Dependent requirements:
- ACME-REQ-05 (the vectorisation pipeline)
- ACME-REQ-08 (vector database deployment)

Preconditions:
- Knowledge base vectorisation is complete (≥ 10M vectors) — verified through the vector store's `count` API
- Vector database health ≥ 99.5% (visible on the monitoring dashboard)

External dependencies:
- The vector database (already deployed, nothing extra to request)
- The API gateway (already in place, a new route is needed)

## Risks, Constraints & Assumptions

Risks:
- **API performance degrades under high concurrency** (probability = medium 35% / impact = high → high priority)
  Mitigation: finish load testing in week 1 and introduce a Redis query cache (TTL 5min)
- **The embedding model falls short on precision** (probability = low 15% / impact = medium → medium priority)
  Mitigation: finish benchmarking in week 1 and keep model-B ready as an alternative

Constraints (confirmed):
- The choice of vector database cannot be changed (an infrastructure constraint)
- Delivery must happen by the end of Phase 2 (2 weeks from now), because Phase 3 depends on it serially

Assumptions (to be verified):
- The current embedding model reaches ≥ 80% precision on the 10M dataset | benchmark in week 1 | tech lead

## Source

- **Source type**: business objective
- **Source link**: the 2026 Q2 OKR — "open up third-party integration with the knowledge base"
- **Decision context**: the developer community reports that adoption costs are high (community survey report §3); in 2026 Q1, 3 integrators independently built their own embedding pipeline, about 40 person-days of duplicated work

## Scope

In Scope:
- The REST API implementation, vector database integration, API key authentication, OpenAPI documentation
- Server-side caching (Redis)

Out of Scope:
- OAuth authorization (a later requirement)
- The search results UI (a front-end project)
- Real-time vector updates (handled in Phase 3)

## Timeline

P1 · Phase 2, weeks 3-4 · 4 person-days
````

### 7.2 Business rules escalated to mandatory (decision table + acceptance back-reference)

The rule set is the deliverable here (pricing discounts), so business rules are escalated to mandatory, declared as a decision table, with the acceptance criteria citing the rule ids back.

````markdown
## Business Rules

| id | Condition | Discount |
|---|---|---|
| R1 | order total < 100 | 0% |
| R2 | 100 <= order total < 500 | 5% |
| R3 | order total >= 500 and the customer is a member | 15% |

## Acceptance Criteria

- [ ] An order total of 80 is charged 80 (Covers R1)
- [ ] A member's order total of 600 is charged 510 (Covers R3)
````

---

## 8. Relationship to other assets

- **Companion rule**: [rules/requirement-quality.md](../rules/requirement-quality.md) — the quality review checklist for requirement documents (5 dimensions: completeness / actionability / clarity / soundness / traceability). This spec defines the data contract only; every review checklist belongs to the rule.
- **Downstream spec**: [functional-design-modeling.md](./functional-design-modeling.md) — only a requirement in `approved` status may yield a functional design, whose `parent` points at the requirement document path
- **Intake triage**: [rules/requirement-intake-triage.md](../rules/requirement-intake-triage.md) — raw intake is triaged first; only intake classified as a requirement (functional or non-functional) is modelled by this spec, while defects, technical tasks, proposals and other non-requirement classes are not
- **Related industry standards**: IEEE 830 (software requirements specifications), Gherkin / Cucumber (the BDD acceptance format), ISO 31000 (risk management), SWEBOK (traceability best practice)
- **Recursive basis**: this spec itself follows the 8-section skeleton of [spec-modeling.md](./spec-modeling.md) v2.0.0, skipping §2 Mental model — the questions a requirement must answer are already carried by the 6 sections in §5.1
