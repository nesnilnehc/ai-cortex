---
id: REQUIREMENT_MODELING_SPEC_V1
name: Requirement Modeling Protocol
description: |
  Universal protocol for structured requirement modeling and documentation.
  Defines 7 mandatory fields, 5-dimensional review checklist, and standardized
  acceptance criteria format (Gherkin BDD). Applicable to functional requirements,
  non-functional requirements, bug fixes, and technical tasks across any project.
version: 1.0.0
status: active
lifecycle: living
created_at: 2026-03-25
scope: |
  Applicable to all types of requirement modeling: functional requirements, non-functional
  requirements, bug fixes, and technical tasks. Defines the standard structure (7 mandatory
  fields) and quality criteria (5-dimensional review checklist) to ensure consistent,
  traceable, and testable requirements across any project or domain.
related: []
---

# Requirement Modeling Protocol v1.0.0

*Design Date: 2026-03-25 | Last Updated: 2026-03-25 | Applicable Scope: Universal requirements modeling framework (functional/defect/technical task/non-functional requirements)*

## Version History

| Version | Date | Status | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-03-25 | Published | Universal protocol extracted from project-specific template. 7 mandatory fields (with requirement source), 5-dimensional review checklist, Gherkin BDD acceptance criteria format, risk priority calculation (probability × impact), simplified guidance by requirement type, AI refactor instructions for automated validation |

---

## Protocol Scope & Applicability

This protocol defines a universal framework for requirement modeling applicable to:

1. **Functional Requirements**: New features, process modifications, experience optimization
2. **Non-Functional Requirements**: Performance, security, maintainability, scalability
3. **Bug Fixes**: Defect resolution, performance optimization, technical debt repayment
4. **Technical Tasks**: Architecture optimization, dependency upgrades, infrastructure improvements

### Simplified Guidance by Requirement Type

| Type | Mandatory Fields | Simplifiable Sections |
|------|------------------|-----------------------|
| Functional Requirement | All 7 mandatory fields | — |
| Bug Fix | All 7 mandatory fields | Background (problem format), Risk & Constraints (1 critical risk; constraints optional) |
| Technical Task | All 7 mandatory fields | Background (problem format acceptable) |
| Non-Functional | All 7 mandatory fields | — |

**Note**: Even with simplifications, all 7 mandatory fields must be completed. Risk priority and mitigation strategies are never optional.

---

## 7 Mandatory Fields

> **Conditional Mandatory - Scope Definition** becomes required when:
>
> - Requirement involves integration across multiple systems or modules
> - Requirement may cause ambiguity with other requirements (easily misinterpreted as out-of-scope)
> - Technical task or refactoring task (must clarify change boundaries)
> - Estimated work effort > 5 days
>
> Simple single-function requirements or defect fixes may omit scope definition, but it's recommended to at least list 1-2 "out of scope" items to clarify exclusions.

### 1. Requirement ID

**Purpose**: Uniquely identify the requirement for traceability and system integration

**Format**: `{PROJECT}-REQ-{nn}` (e.g., ACME-REQ-05, MYAPP-REQ-12)

**Validation**: ID must be unique, properly formatted, no duplicates

**Example**: `APP-REQ-042`

---

### 2. Requirement Title

**Purpose**: One-sentence summary of the requirement's core value or problem

**Format**: `[Type] Function or problem description`

**Examples**:
```
[Feature] System supports automated risk identification in requirement generation
[Defect] Requirement template missing testability verification field
[Enhancement] Reduce search latency from 500ms to <100ms
```

**Validation**: Title ≤ 80 characters, no technical implementation details

---

### 3. Background & Value

**Purpose**: Explain problem context, desired state, and importance—**WITHOUT solution or technical implementation**

**Recommended Format** (User Story):
```
As [role]
I want [desired functionality or result]
So that [value or purpose]
```

**Alternative Format** (Problem Description):
```
Background: [phenomenon or problem]
Desired State: [expected outcome]
Impact: [affected users or processes]
```

**Examples**:

**Example 1 (User Story - Recommended)**:
```
As a requirements engineer
I want an API to retrieve domain specifications semantically
So that the AI agent can obtain relevant specification context when generating
requirements, thereby improving requirement quality
```

**Example 2 (Problem Description)**:
```
Background: Requirements lack linkage with code commits; review records are scattered
Desired State: Requirements form complete traceability with commits; review history centralized
Impact: Requirement management, code traceability, compliance verification
```

**Example 3 (Anti-pattern)**:
```
❌ Need to implement a search API to allow the agent to query specifications
   (This describes a solution, not the background)
```

**Validation**:
- [ ] Not exceeding 300 characters
- [ ] Does not contain technical selection, implementation approach, or specific feature descriptions
- [ ] Clearly explains why this requirement matters

---

### 4. Acceptance Criteria

**Purpose**: Define specific, verifiable conditions for requirement completion (functional/behavioral level)

**Format**: Gherkin BDD or Checklist

**Example 1 (Gherkin)**:
```gherkin
Scenario: System automatically identifies critical dependencies

Given a requirements engineer configures risk detection rules in the generation prompt
And the prompt includes "identify critical dependencies", "identify prerequisites", "identify integration risks"
When the AI generates the initial requirement draft
Then the output should include a dedicated "Risk Identification" section
And the risk section contains at least 3 identified risks, each with:
  - Risk description
  - Probability
  - Impact level
  - Priority
  - Mitigation strategy
```

**Example 2 (Checklist)**:
```
Acceptance Criteria:
- [ ] Search interface deployed and responding to queries
- [ ] Query response time ≤ 500ms (p95)
- [ ] Returned relevant items ≥ 3
- [ ] Relevance precision ≥ 80%
- [ ] API documentation published with input/output examples
- [ ] Integration tests cover 10+ typical queries
```

**Example 3 (Bug Fix)**:
```
Acceptance Criteria:
- [ ] "Testability Verification" field added to requirement template
- [ ] New field appears in project management tool, positioned after "Acceptance Criteria"
- [ ] Historical requirements (>10) field backfill completed
- [ ] Documentation updated with field definition + 3+ usage examples
- [ ] Team feedback: new field helpful for review, usable without friction
```

**Example 4 (Non-Functional Requirement)**:
```
Acceptance Criteria:
- [ ] API response time ≤ 500ms (p95, based on 10M dataset)
- [ ] Precision validation: top-3 relevance ≥ 80% (50+ typical queries)
- [ ] Deployed to production with monitoring (latency, precision, error rate)
- [ ] Performance benchmark report published with before/after comparison
```

**Validation**: Minimum 3 acceptance criteria, each automatically or manually verifiable

**Acceptance Criteria Self-Check**:
- [ ] No vague adjectives (e.g., "fast", "simple", "user-friendly") → replaced with quantifiable metrics
- [ ] Each criterion independently verifiable by third party
- [ ] Non-functional requirements include specific values (e.g., latency ≤500ms, precision ≥80%)

---

### 5. Dependencies & Prerequisites

**Purpose**: Document requirement dependencies and prerequisite conditions

**Format**:
```
Dependent Requirements: [Requirement IDs or titles]
Prerequisites: [Conditions that must be met or possessed]
External Dependencies: [Third-party services, tools, teams]
```

**Example**:
```
Dependent Requirements:
  - APP-REQ-05 (Project management tool field customization)
  - APP-REQ-08 (Requirement review checklist)

Prerequisites:
  - Project management tool custom fields configured (status, review_links)
  - Requirement template v1.0 published
  - Git Webhook configured

External Dependencies:
  - Project management tool API (requires API key)
  - Git repository (requires Webhook permissions)
```

**Validation**: Dependency list has no circular references

**Circular Dependency Verification**:
- [ ] This requirement is not indirectly depended on by its dependencies (no cycles)
- [ ] For long dependency chains, create dependency graph to verify

---

### 6. Risks, Constraints & Assumptions

**Purpose**: Identify risks in advance (probability × impact), confirm constraints, document assumptions for validation

**Format**:
```
Risks: [Potential problem]
  - Probability: [very low/low/medium/high] (percentage)
  - Impact: [project/delivery impact if risk occurs]
  - Priority: [based on probability × impact, determines response order]
  - Mitigation: [actions to reduce risk]

Constraints (confirmed facts):
  - Technical Constraint: [validated technical limitations]
  - Time Constraint: [validated time limitations]
  - Resource Constraint: [validated resource limitations]

Assumptions (to be validated):
  - [Unvalidated assumption] | Validation Method | Responsible Party
```

**Example**:
```
Risks:
  - Search service deployment complex, high operational cost
    - Probability: Medium (30%)
    - Impact: Delivery delay 3-5 days → blocks Phase 2 KPI verification
    - Priority: High (must address in advance)
    - Mitigation: Use AI to auto-generate Dockerfile, K8s manifests, config scripts

  - Search precision may not meet requirements (<80%)
    - Probability: Low (15%)
    - Impact: Requirement quality decreases → increases manual review cost
    - Priority: Medium (lower impact but higher probability)
    - Mitigation: Complete embedding model POC before week 2, prepare alternatives (model-A vs model-B)

Constraints (confirmed):
  - Technical: Search service selection (Technology-X) immutable; migration cost 3-5 days
  - Time: Phase 2 total duration 40 workdays, no extension (Phase 3 already scheduled)
  - Resource: Search pipeline implementation requires technical team 2+ people

Assumptions (to be validated):
  - Project management tool API access obtainable | Confirm with ops team | Ops Lead
  - Embedding model Model-A achieves ≥80% precision on 10M vector dataset | Complete POC comparison by week 2 | Technical Lead
```

**Validation**:
- [ ] Functional requirements / Technical tasks: At least 1 risk, 2 constraints
- [ ] Bug fixes: At least 1 critical risk; constraints optional (if present, mark them)
- [ ] Each risk labeled with priority (based on probability × impact)
- [ ] Assumptions annotated with validation method + responsible party

**Risk Priority Calculation**: Priority = Probability × Impact
- High Priority: Probability ≥ Medium AND Impact ≥ High
- Medium Priority: (Probability = Medium AND Impact = Medium) OR (Probability = High AND Impact = Low)
- Low Priority: Probability ≤ Low OR Impact ≤ Low

---

### 7. Requirement Source

**Purpose**: Clarify requirement origin and upstream decision context for understanding business value and traceability

**Format**:
```
Source Type: [Feature Request / Business Objective / Incident / Technical Debt / Other]
Source Link/ID: [URL or Requirement ID]
Parent Requirement (if applicable): [Associated Requirement ID]
Decision Context: [Brief explanation of why this requirement is needed]
```

**Examples**:

**Example 1 - Feature Request**:
```
Source Type: Feature Request
Source Link: Issue #234 (User feedback: requirement template unclear on simplifiable fields)
Decision Context: Phase 2 user feedback → improve template usability → reduce authoring effort
```

**Example 2 - Business Objective**:
```
Source Type: Business Objective
Source Link: Q2 2026 OKR: Improve specification retrieval efficiency
Parent Requirement: None
Decision Context: Enable AI agent to reliably generate high-quality requirements
```

**Example 3 - Incident**:
```
Source Type: Incident
Source Link: Defect from Phase 1: requirement template missing testability field
Parent Requirement: APP-REQ-02 (Requirement template enhancement)
Decision Context: Retrospective fix for Phase 1 review gap; prevent similar issues
```

**Validation**:
- [ ] Requirement source clearly traceable (not "vague request from someone")
- [ ] Parent requirement ID noted if applicable
- [ ] Decision context clear (can explain "why we're doing this" to team members)

---

## Optional Fields (Enhanced Completeness)

### 8. Scope Definition

**Purpose**: Clarify requirement boundaries to prevent scope creep

**Note**: Although listed as optional, fill this section when any of the four conditions above apply.

**Format**:
```
In Scope (covered by this requirement):
  - [Clear list]

Out of Scope (not covered by this requirement):
  - [Clear list]

Minimum Viable Version (Walking Skeleton):
  - [Thinnest deliverable form]
```

**Example**:
```
In Scope:
- REST API for semantic search with configurable parameters (query, top_k, threshold)
- Integration with vector database for similarity computation
- API documentation with OpenAPI spec and 5+ examples
- Performance validation (p95 latency ≤500ms)

Out of Scope:
- User-facing search UI (handled by APP-REQ-25)
- Search relevance fine-tuning (handled by Phase 3)
- Real-time index updates (deferred to Phase 3)

Minimum Viable Version:
- Basic REST API (POST /search) accepting query text
- Returns top-3 results with similarity scores
- API documentation with 2 example queries
```

---

### 9. Open Questions

**Purpose**: Record unresolved items from requirement review/implementation, categorize as blocking or non-blocking

**Format**:
```
[Blocking/Non-Blocking] [Question description] | Responsible Party | Planned Resolution Approach
```

**Example**:
```
[Blocking] Embedding model selection not finalized | Technical Lead | Complete POC comparison by week 2; finalize selection
[Non-Blocking] Vector database rate-limiting policy | DevOps Lead | Confirm with vendor by week 3
[Blocking] API authentication method (OAuth vs API Key) | Security Lead | Architecture review by week 1
```

**Guidance**:
- **Blocking Questions**: Cannot start implementation without resolution; must address in requirement review or document in dependencies
- **Non-Blocking Questions**: Can resolve in parallel with implementation, but requires tracking and confirmation

---

### 10. Related Documentation & Standards Links

**Purpose**: Associate requirement with specifications and reference standards

**Format**:
```
Related Standards:
  - [Standard name]: [link or path]
  - [Architecture Decision Record ID]: [link]

Related Requirements:
  - [Other associated Requirement ID]
```

**Example**:
```
Related Standards:
  - Technology Stack Standard (Node.js v18+, TypeScript)
  - API Security Specification
  - ADR-002: Vector Database Selection

Related Requirements:
  - APP-REQ-12 (Knowledge Base Content Development)
  - APP-REQ-18 (Vectorization Pipeline Implementation)
```

---

### 11. Priority & Timeline

**Format**:
```
Priority: [P0/P1/P2]
  - P0: Blocking path, must complete
  - P1: Critical path, complete ASAP
  - P2: Non-critical, can be deferred

Planning Cycle: [Week-1 / Week-2-3 / Phase-2-Week-1, etc.]
Estimated Effort: [x workdays]
```

---

### 12. Definition of Done (Success Criteria)

**Purpose**: Measure requirement release readiness (process and quality gates). **Acceptance Criteria** answers "Is the feature complete?"; **Definition of Done** answers "Can we release it?"

**Format**:
```
- [ ] Requirement review approved (Reviewer: ___)
- [ ] Implementation complete, PR submitted
- [ ] Unit tests passed (coverage ≥ 80%)
- [ ] Integration tests passed
- [ ] Code review approved
- [ ] Documentation updated
- [ ] Deployed to test environment/production
```

---

## Quick-Fill Guide

### Step 1: Basic Information (3 minutes)

- [ ] Fill Requirement ID
- [ ] Fill Requirement Title

### Step 2: Define Background & Value (5 minutes)

- [ ] Fill Background & Value (user story or problem description)
- [ ] Verify no solution details included

### Step 3: Define Completion Criteria (10 minutes)

- [ ] List 3+ acceptance criteria
- [ ] Self-check acceptance criteria (no vague terms, verifiable)

### Step 4: Identify Risks & Constraints (5 minutes)

- [ ] List 1+ risks with probability and priority
- [ ] List 2+ constraints (confirmed facts)
- [ ] List assumptions with validation methods (if applicable)

### Step 5: Confirm Requirement Source (2 minutes)

- [ ] Fill Source Type (Feature Request / Business Objective / Incident / Technical Debt)
- [ ] Add source link/ID
- [ ] Brief decision context (optional)

### Step 6: Document Dependencies (5 minutes)

- [ ] Identify dependent requirements
- [ ] List prerequisites and validation methods
- [ ] Verify no circular dependencies

### Step 7: Enhance Completeness (Optional, 10 minutes)

- [ ] Add scope definition (**required if multi-system integration, cross-boundary ambiguity, technical task, or effort > 5 days**)
- [ ] List open questions (distinguish blocking/non-blocking)
- [ ] Add specification links
- [ ] Define priority and timeline
- [ ] List success criteria

**Time Estimates by Requirement Type**:

| Type | Core Fields | Time | +Optional Fields | Time |
|------|-------------|------|------------------|------|
| Functional Requirement | 1-7 | 30 min | +8-12 | 45 min |
| Bug Fix | 1-7 (simplified) | 20 min | +6,9 | 30 min |
| Technical Task | 1-7 | 25 min | +8-12 | 40 min |

---

## 5-Dimensional Review Checklist

Before submitting a requirement for review, authors should self-check using this list. These checkpoints correspond 1:1 with the 5-dimensional review standard (Completeness, Executability, Clarity, Reasonableness, Traceability).

### 1. Completeness (Is all information present?)

- [ ] All 7 mandatory fields completed (ID, Title, Background, Acceptance, Source, Dependencies, Risks)
- [ ] For bug fixes, risks can be simplified to 1 critical risk; constraints optional
- [ ] Background field contains user story or problem statement (**not** solution or technical details)
- [ ] 3+ acceptance criteria cover functionality scope and quality requirements
- [ ] Requirement source clearly traceable (not "hearsay" or "verbal request")

### 2. Executability (Can implementer start work immediately?)

- [ ] Dependency list clear, critical dependencies noted
- [ ] Each prerequisite annotated with verification method (no ambiguity)
- [ ] Every acceptance criterion automatically verifiable or clearly testable
- [ ] Scope definition exists (or meets "simple requirement" exemption), boundaries clear
- [ ] Open question list complete; blocking questions have solution plans

### 3. Clarity (Is it easy to understand without ambiguity?)

- [ ] Title concise and clear (≤15 words optimal), ≤80 characters
- [ ] Background contains no solution approach, technical implementation, or architecture details
- [ ] Acceptance criteria free of vague terms ("should", "reasonable", "suitable", "fast")
- [ ] All technical terms defined at first use or linked to documentation
- [ ] Risks, constraints, assumptions use consistent terminology (avoid mixing)

### 4. Reasonableness (Is it worth doing? Can it be done?)

- [ ] Priority and work effort proportionate (P0/P1 shouldn't be 1-day tasks)
- [ ] At least 1 critical risk identified with clear mitigation strategy
- [ ] Time constraints match requirement complexity (no optimistic estimates)
- [ ] No direct conflicts with existing requirements (or conflicts explicitly noted)
- [ ] Technical feasibility verified (POC completed or known technology stack)

### 5. Traceability (Can we track evolution and impact?)

- [ ] Requirement ID properly formatted (PROJECT-REQ-nn), no duplicates
- [ ] Requirement source explicit (Feature Request / Business Objective / Incident, etc.), traceable
- [ ] Dependencies accurate, no circular references
- [ ] Associated documentation complete (specifications, ADRs, knowledge base links)
- [ ] Version history clear (if iterated, changes documented with rationale)

---

## How to Use the Review Checklist

**What Authors Should Do**:

1. After completing requirement draft, check each item above
2. Fix immediately upon discovering issues (don't submit incomplete requirements)
3. Ensure all items checked (✓) before submitting for review

**What Reviewers Should Do**:

1. Use as quick pre-check that author has self-reviewed
2. Focus on areas likely to be missed (hidden scope creep, assumption validity)
3. Reference these 5 dimensions and specific checkpoints in feedback

---

## Universal Examples

### Example 1: Functional Requirement

```markdown
# Requirement: Semantic Search Interface for Knowledge Base

## Requirement ID
APP-REQ-15

## Requirement Title
[Feature] Implement semantic search API for knowledge base retrieval

## Background & Value
As a system integrator
I want an API that performs semantic search on stored specifications
So that external systems can efficiently retrieve relevant documentation
contextually

Current situation: Knowledge base exists but lacks an accessible semantic
search interface. External systems must implement custom solutions, creating
integration friction.

Expected outcome: Standardized REST API available for semantic queries.

Impact: Product team (reduces integration work), external integrators (faster
development), end users (improved documentation discoverability).

## Acceptance Criteria
- [ ] REST API `POST /search/semantic` implemented and responding to queries
- [ ] API accepts parameters: query (string), top_k (number, default 10), similarity_threshold (0-1, default 0.7)
- [ ] Response includes: document_id, relevance_score (0-1), content_snippet (max 500 chars), metadata
- [ ] Query response time ≤ 500ms (p95) for typical query on 10M item dataset
- [ ] Precision validation: top-3 results relevant ≥ 80% across 50+ typical query patterns
- [ ] API fully documented (OpenAPI spec + 5+ usage examples with expected responses)
- [ ] Integration tests cover 10+ realistic scenarios including edge cases
- [ ] Error responses follow standard format with appropriate HTTP status codes

## Dependencies & Prerequisites
Dependent Requirements:
  - APP-REQ-05 (Knowledge base vectorization pipeline)
  - APP-REQ-08 (Vector database deployment and indexing)

Prerequisites:
  - Knowledge base fully vectorized (≥10M vectors) | Verification: Database query count check
  - Vector database deployed and healthy | Verification: Database connectivity test passes
  - Embedding model selected and operational | Verification: Health check endpoint responds in <100ms

## Risks, Constraints & Assumptions

Risks:
  - Search precision degradation at scale (>10M vectors)
    - Probability: Low (15%)
    - Impact: Relevance drops below 80% threshold, requires tuning or embedding model change
    - Priority: Medium
    - Mitigation: Complete benchmark testing by week 2; prepare alternative embedding models

  - API performance degrades under load (>100 concurrent queries)
    - Probability: Medium (35%)
    - Impact: Introduces latency >500ms, poor user experience
    - Priority: High
    - Mitigation: Load testing week 1; implement caching and query optimization

Constraints (confirmed):
  - Technical: Vector database immutable (already selected and deployed)
  - Time: Must deliver by end of phase (2 weeks)
  - Resource: 2 backend engineers + 1 QA engineer required

Assumptions (to validate):
  - Embedding model precision ≥80% on 10M vectors | Complete benchmark testing week 1 | Tech Lead
  - API latency <500ms achievable with standard database indexing | Load testing week 1 | Tech Lead

## Requirement Source
Source Type: Business Objective
Source Link: Q2 2026 OKR: Enable third-party integrations with knowledge base
Parent Requirement: None
Decision Context: Strategic initiative to expand product ecosystem and reduce friction
for external integrators

## Scope Definition

**In Scope**:
- REST API implementation and deployment
- Vector database integration
- Basic authentication (API key)
- Standard error handling and HTTP status codes
- Performance optimization for <500ms p95 latency
- OpenAPI documentation and code examples

**Out of Scope**:
- Advanced authentication (OAuth, JWT) → handled separately
- Web UI for search → separate requirement
- Real-time vector updates → Phase 2
- Custom ranking/boosting algorithms → future enhancement

**Minimum Viable Version**:
- Basic POST /search API accepting query text
- Returns top-5 results with scores
- API documentation with 2 working examples

## Open Questions
[Blocking] Should API support filtering by document type? | Product Manager | Confirm requirements gathering feedback by week 1
[Non-Blocking] Rate limiting strategy? | Platform Team | Align with platform standards by week 2

## Related Documentation
- Specification: Knowledge Base Vectorization Standard v1.2
- ADR-003: Vector Database Selection (Database-X)
- API Security Standard: Rate Limiting & Auth Methods

## Priority & Timeline
- P1 (Critical Path)
- Phase 2, Week 3-4
- Estimated Effort: 4 workdays (2 backend + 2 QA integration)

## Definition of Done
- [ ] API code complete and merged to main branch
- [ ] Unit test coverage ≥ 80%
- [ ] Integration tests with vector database passing
- [ ] Load testing completed (p95 ≤ 500ms at 100 QPS)
- [ ] Code review approved
- [ ] API documentation published and reviewed
- [ ] Deployed to staging environment and tested
- [ ] Team trained on API usage
```

---

### Example 2: Bug Fix

```markdown
# Requirement: Add Testability Verification Field

## Requirement ID
APP-REQ-02

## Requirement Title
[Defect] Requirement template missing testability verification field

## Background & Value
As a QA engineer
I want requirement templates to include testability verification checks
So that acceptance criteria validation becomes standardized across reviews

Current issue: Phase 1 reviews revealed that ambiguous acceptance criteria
(e.g., "fast", "simple") were not caught, leading to testing delays and
rework.

Expected outcome: Standardized checklist in requirement template ensures
every acceptance criterion is independently verifiable before approval.

## Acceptance Criteria
- [ ] "Testability Verification" field added to requirement template
- [ ] Field contains ≥5 specific checks (e.g., "no vague adjectives", "each criterion independently verifiable")
- [ ] Field appears in project management tool with helpful inline guidance
- [ ] Documentation updated with field definition + 3+ usage examples
- [ ] Applied retrospectively to 10+ Phase 1 requirements
- [ ] Team feedback: ≥80% of reviewers report improved clarity

## Dependencies & Prerequisites
Dependent Requirements:
  - APP-REQ-03 (Requirement template v1.0 baseline)

Prerequisites:
  - Requirement template v1.0 deployed to project management tool | Verification: Check tool version
  - Testability verification checklist designed and reviewed | Verification: Review design document

## Risks, Constraints & Assumptions

Risks:
  - New verification field adds review overhead
    - Probability: Medium (40%)
    - Impact: Review cycle extends 10-15 minutes per requirement
    - Priority: Medium
    - Mitigation: Provide automated checklist template + 30-minute team training

Constraints (confirmed):
  - Time: 2 workdays (fits in current sprint)
  - Resource: 1 QA lead

Assumptions (to validate):
  - Checklist covers 90% of common acceptance criteria issues | Retrospective review of Phase 1 requirements | QA Lead

## Requirement Source
Source Type: Incident
Source Link: Phase 1 Postmortem - Issue #127 (acceptance criteria ambiguity)
Parent Requirement: APP-REQ-03
Decision Context: Prevent similar testing delays in Phase 2

## Priority & Timeline
- P1 (Blocking for Phase 2 requirement reviews)
- Phase 2, Week 1
- Estimated Effort: 2 workdays

## Definition of Done
- [ ] Checklist created and design-reviewed
- [ ] Project management tool field configured
- [ ] Phase 1 requirements updated (10+ items)
- [ ] Team trained (meeting recorded for async viewing)
- [ ] Documentation published with examples
- [ ] Verification: First 5 Phase 2 requirements pass new checklist
```

---

## AI Refactor Instructions

### Purpose

These instructions enable AI systems to automatically validate, improve, and refactor requirements according to the protocol. Use these when:

- Generating requirement drafts for human review
- Automatically scanning existing requirements for protocol compliance
- Suggesting improvements to requirement quality
- Refactoring project-specific requirements into generic ones

### Automated Validation Checklist

**Step 1: Extract and Validate Mandatory Fields**

```
For each requirement, verify:
1. Requirement ID exists and matches pattern {PROJECT}-REQ-{nn}
2. Title (≤80 chars, no technical implementation details)
3. Background contains no solution/tech details (check for keywords: API, database, algorithm, implementation)
4. Acceptance criteria: ≥3 items, no vague terms (fast, simple, easy, suitable)
5. Requirement source exists (Feature Request / Business Objective / Incident / Technical Debt)
6. Dependencies listed (if none, explicitly state "No dependencies")
7. Risks identified with probability and mitigation (even if N/A for simple fixes)

ACTION: If any mandatory field missing or invalid, flag with specific guidance for correction.
```

**Step 2: Validate Acceptance Criteria**

```
For each acceptance criterion:
1. Check for vague quantifiers: "should", "might", "may", "suitable", "reasonable", "quick"
   → Recommend specific metrics (e.g., "response time ≤ 500ms")
2. Verify criterion is independently testable (can be verified without others)
3. For non-functional requirements, check for unit/measurement (latency in ms, memory in MB, etc.)
4. Suggest Gherkin BDD format if not present

ACTION: Suggest rewrites for criteria failing these checks.
```

**Step 3: Risk & Constraint Validation**

```
1. Verify each risk has: probability, impact, priority, mitigation
2. Check priority calculation: Priority = Probability × Impact
3. For technical requirements, verify technical constraints documented
4. Validate assumptions include: assumption statement | validation method | responsible party

ACTION: Flag incomplete risk entries; suggest mitigation strategies if missing.
```

**Step 4: Dependency & Traceability Validation**

```
1. Verify no circular dependencies: Requirement A depends on B; B depends on C; C does not depend on A
2. Check dependency exists in system (cross-reference with requirement database)
3. Validate each prerequisite has verification method
4. Confirm source link is valid/accessible

ACTION: Flag broken dependencies; suggest resolution approaches.
```

**Step 5: Scope & Clarity Validation**

```
Scope Definition (if required):
  - Check "In Scope" items are concrete (not vague)
  - Verify "Out of Scope" items don't contradict "In Scope"
  - Confirm Walking Skeleton is minimal but complete

Clarity Checks:
  - Scan background for technical terms without definition
  - Check title for jargon requiring explanation
  - Verify all acronyms defined at first use

ACTION: Suggest scope clarifications; recommend definitions for unexplained terms.
```

### Automated Improvement Suggestions

**Pattern 1: Transform Solution-Focused Background into Value-Focused**

```
Input: "Need to implement vector search API to query specifications"
  (❌ Solution-focused)

Output: "Need reliable way for system to retrieve relevant specifications
contextually when generating requirements, improving requirement quality"
  (✓ Value-focused, no solution implied)

Action: Detect implementation keywords (API, database, algorithm) in Background.
Suggest rewriting to focus on problem → desired outcome → value.
```

**Pattern 2: Convert Vague Acceptance Criteria to Measurable**

```
Input: "API should be fast and responsive"
Output: "API response time ≤ 500ms (p95 percentile) for typical queries"

Detection keywords: should, be, fast, simple, easy, suitable, reasonable
Suggestion: Replace with specific metric (time, count, percentage, ratio)
```

**Pattern 3: Expand Single-Sentence Dependencies**

```
Input: "Depends on APP-REQ-08"
Output:
  - Dependent Requirement: APP-REQ-08 (Vector database deployment)
  - Prerequisite: Vector database health check passes
  - Verification: Database connectivity test completes successfully

Action: Detect sparse dependency sections; suggest structured format.
```

### Automated Refactoring (Project-Specific → Generic)

**Pattern 1: Remove Project-Specific Terminology**

```
Scan for and replace:
  - Phase names (Phase 1, Phase 2, M2-W1) → generic phase/timeline markers
  - Specific tool names (Zendesk, Jira, internal-tool-X) → "project management tool"
  - Organization roles (Knowledge Engineer, Test Lead) → generic roles
  - Project acronyms (M1-REQ, ACME-REQ) → generic pattern {PROJECT}-REQ

Example:
  Before: "M2-REQ-05 is blocked by M1 platform work"
  After: "APP-REQ-05 depends on APP-REQ-02 (foundational work)"
```

**Pattern 2: Extract Generic Example Templates**

```
For each requirement example, create generic version:
1. Replace project-specific values with placeholders or categories
2. Keep structure and logic intact
3. Annotate which parts are customizable vs. boilerplate

Example Domain Example → Generic Template:
  Before: "Query vector database (Milvus) for specifications (L1 knowledge base)"
  After: "[Query {DATA_STORE} for {CONTENT_TYPE}]"
```

### Usage Examples

**Example 1: Validate Incoming Requirement**

```python
def validate_requirement(req_dict):
    # 1. Check mandatory fields
    mandatory = ['id', 'title', 'background', 'acceptance_criteria',
                 'source', 'dependencies', 'risks']
    missing = [f for f in mandatory if not req_dict.get(f)]
    if missing:
        return f"Missing fields: {missing}"

    # 2. Validate acceptance criteria
    criteria = req_dict['acceptance_criteria']
    vague_terms = ['should', 'fast', 'simple', 'suitable', 'quick']
    for criterion in criteria:
        for term in vague_terms:
            if term in criterion.lower():
                suggest_metric_replacement(criterion)

    # 3. Check risks have mitigation
    for risk in req_dict['risks']:
        if not risk.get('mitigation'):
            flag("Risk missing mitigation strategy")

    return "Validation complete. See flags above."
```

**Example 2: Suggest Gherkin Conversion**

```
Input:
  "Acceptance Criteria:
   - API accepts queries
   - Returns results in <500ms"

Output (Suggested):
  "Gherkin BDD Format:
   Scenario: User queries knowledge base
   When user submits query to POST /search
   And query contains valid text
   Then response received within 500ms
   And response includes ≥1 matching document"
```

**Example 3: Detect & Flag Circular Dependencies**

```
Input:
  APP-REQ-05 depends on APP-REQ-08
  APP-REQ-08 depends on APP-REQ-12
  APP-REQ-12 depends on APP-REQ-05  ← CIRCULAR!

Output:
  ⚠️ CIRCULAR DEPENDENCY DETECTED
  Path: APP-REQ-05 → APP-REQ-08 → APP-REQ-12 → APP-REQ-05
  Action: Remove one dependency or restructure into separate requirements
```

---

## Protocol Compliance Checklist

Use this checklist to verify a requirement document follows the protocol:

- [ ] **Frontmatter**: Requirement includes metadata (ID, Title, version if applicable)
- [ ] **7 Mandatory Fields**: All present and complete
  - [ ] Requirement ID (PROJECT-REQ-nn format)
  - [ ] Title (<80 chars, typed)
  - [ ] Background & Value (no solutions, clear context)
  - [ ] Acceptance Criteria (≥3, measurable, no vague terms)
  - [ ] Dependencies & Prerequisites (none stated = explicitly "No dependencies")
  - [ ] Risks, Constraints, Assumptions (priority calculated, mitigation provided)
  - [ ] Requirement Source (type + link + decision context)
- [ ] **Conditional Mandatory**: Scope Definition present if:
  - [ ] Multi-system integration, OR
  - [ ] Cross-boundary ambiguity, OR
  - [ ] Technical task/refactoring, OR
  - [ ] Estimated effort > 5 days
- [ ] **5-Dimensional Review**: All checks passed:
  - [ ] Completeness: All info present
  - [ ] Executability: Implementer can start immediately
  - [ ] Clarity: No ambiguity or jargon
  - [ ] Reasonableness: Worth doing, technically feasible
  - [ ] Traceability: Source and dependencies clear
- [ ] **Optional Fields**: If used, complete and valid:
  - [ ] Scope Definition (if required above)
  - [ ] Open Questions (blocking vs. non-blocking marked)
  - [ ] Related Documentation (valid links)
  - [ ] Priority & Timeline (P0/P1/P2, dates realistic)
  - [ ] Definition of Done (checklist complete)

---

## Appendix: Glossary

| Term | Definition |
|------|-----------|
| **Acceptance Criteria** | Specific, measurable conditions that define when a requirement is complete |
| **Background & Value** | Context explaining the problem or opportunity without proposing a solution |
| **BDD (Behavior-Driven Development)** | Testing methodology using Gherkin syntax (Given-When-Then) to specify behavior |
| **Definition of Done (DoD)** | Checklist of process/quality gates required before a requirement can ship |
| **Dependency** | Requirement or resource that must exist/complete before another can start |
| **Gherkin** | Structured language for writing executable specifications (Given-When-Then format) |
| **Non-Functional Requirement** | Requirement specifying system properties (performance, security, scalability) rather than features |
| **P0/P1/P2** | Priority levels (P0=blocking, P1=critical, P2=non-critical) |
| **Prerequisite** | Condition or resource that must be satisfied before work can begin |
| **Risk Priority** | Calculated as Probability × Impact; determines mitigation urgency |
| **Scope Definition** | Clear boundaries of what is/isn't included in a requirement |
| **User Story** | Requirement format: "As [role] I want [feature] so that [value]" |
| **Walking Skeleton** | Minimum viable implementation that demonstrates core functionality |

---

## Related Standards & References

This protocol is compatible with and inspired by:

- **IEEE 830**: IEEE Recommended Practice for Software Requirements Specifications
- **Agile Manifesto**: Emphasis on clear requirements over comprehensive documentation
- **Gherkin/Cucumber**: Structured BDD format for acceptance criteria
- **Risk Management Standards**: ISO 31000 for risk identification and prioritization
- **SWEBOK**: Software Engineering Body of Knowledge traceability best practices

---

**Last Updated**: 2026-03-25
**Status**: Published
**Maintenance**: Community contributions welcome via pull requests
