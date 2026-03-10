---
name: align-architecture
description: Verify architecture and design documents against code implementation; produce an Architecture Compliance Report when implementation diverges from ADR or design decisions.
tags: [workflow, eng-standards, documentation]
version: 1.0.0
license: MIT
related_skills: [align-planning, review-architecture, brainstorm-design, assess-documentation-readiness]
recommended_scope: project
metadata:
  author: ai-cortex
  evolution:
    sources:
      - name: "align-execution"
        repo: "nesnilnehc/ai-cortex"
        version: "1.0.0"
        license: "MIT"
        type: "reference"
        borrowed: "Drift model, traceback pattern, report template structure"
    enhancements:
      - "Split from align-execution (renamed align-planning) per planning vs implementation boundary; focuses on design vs code compliance"
triggers: [align architecture, architecture compliance, design vs code]
input_schema:
  type: free-form
  description: ADR or design doc scope, optional code scope, optional project docs root
output_schema:
  type: document-artifact
  description: Architecture Compliance Report written to docs/calibration/YYYY-MM-DD-architecture-compliance.md
  artifact_type: architecture-compliance
  path_pattern: docs/calibration/YYYY-MM-DD-architecture-compliance.md
  lifecycle: snapshot
---

# Skill: Align Architecture

## Purpose

Verify that code implementation aligns with architecture and design decisions documented in ADRs, design documents, or architecture specs. Produce an Architecture Compliance Report when the implementation diverges from documented decisions.

---

## Core Objective

**Primary Goal**: Produce an actionable Architecture Compliance Report that compares documented architecture/design decisions with the current implementation and lists compliance gaps with impact and remediation suggestions.

**Success Criteria** (ALL must be met):

1. ✅ **Design sources identified**: ADRs, design docs, or architecture specs are located and parsed
2. ✅ **Implementation compared**: Code is analyzed against documented decisions
3. ✅ **Gaps classified**: Each compliance gap is typed (e.g. boundary violation, missing component, divergent pattern) with impact and root cause
4. ✅ **Report persisted**: Architecture Compliance Report is written to the agreed path
5. ✅ **Evidence referenced**: Each gap cites specific design sources and code locations
6. ✅ **Handoff suggested**: When design is outdated or conflicting, suggest `brainstorm-design`; when structure review needed, suggest `review-architecture`

**Acceptance Test**: Can a teammate read the report and immediately understand which architecture decisions are violated, where in code, and what to do next?

---

## Scope Boundaries

**This skill handles**:

- Design document vs code comparison
- Compliance gap detection and classification
- Impact scope and root cause for each gap
- Remediation and handoff recommendations

**This skill does NOT handle**:

- Code structure review without design reference (use `review-architecture`)
- Requirements analysis (use `analyze-requirements`)
- Design creation or design alternatives (use `brainstorm-design`)
- Planning layer alignment (use `align-planning`)

**Handoff point**: After the report, hand off to `brainstorm-design` if design must change, or to `review-architecture` for structural code review without design comparison.

---

## Use Cases

- **Post-implementation check**: Validate that implementation matches ADR or design doc
- **Milestone or release gate**: Ensure architecture decisions are reflected in code
- **Drift investigation**: Diagnose when implementation has drifted from documented design
- **Onboarding audit**: Help new contributors understand design vs actual state

---

## Behavior

### Agent Prompt Contract

```text
You are responsible for architecture compliance verification.

Compare documented architecture and design decisions (ADRs, design docs) against
the codebase and produce an Architecture Compliance Report when divergence exists.
```

### Interaction Policy

- **Defaults**: ADR/design paths from project norms or `docs/architecture/`, `docs/design-decisions/`, `docs/process-management/decisions/`; code scope from workspace
- **Choice options**: Explicit design doc paths when non-default; explicit code paths when partial scope
- **Confirm**: Before proposing edits to design docs; before large code scope

### Phase 0: Resolve Design Sources and Code Scope

1. Resolve design source paths (project norms or default: `docs/architecture/`, `docs/design-decisions/`, `docs/process-management/decisions/`)
2. Resolve code scope (full repo or user-specified paths)
3. If no design docs exist, output blocked report with required minimum inputs; suggest `brainstorm-design` or `bootstrap-project-documentation`

### Phase 1: Extract Design Decisions

1. Parse ADRs, design docs, and architecture specs
2. Extract key decisions: boundaries, components, patterns, constraints
3. Build a decision index for comparison

### Phase 2: Compare Implementation

1. Analyze code against each documented decision
2. For each decision, assess: `compliant` | `partial` | `violated` | `unknown`
3. Capture evidence: file paths, modules, or snippets
4. Classify gaps:
   - **Boundary violation**: Code crosses documented module/layer boundaries
   - **Missing component**: Documented component or interface not implemented
   - **Divergent pattern**: Implementation uses a different pattern than documented
   - **Outdated design**: Design doc may be stale; implementation reflects current intent

### Phase 3: Produce Report

1. Aggregate findings with impact scope and root cause per gap
2. Suggest remediation: update code, update design, or both
3. Recommend handoff to `brainstorm-design` when design conflict; to `review-architecture` when structure-only review needed

### Phase 4: Persist Report

Write report to:

- Default: `docs/calibration/YYYY-MM-DD-architecture-compliance.md`
- Or user-specified path

Report must include a machine-readable compliance block (YAML or JSON).

---

## Input & Output

### Input

- Optional ADR/design doc paths
- Optional code scope (paths or modules)
- Optional project docs root

### Output

#### Architecture Compliance Report Template

```markdown
# Architecture Compliance Report

**Date:** YYYY-MM-DD
**Design Sources:**
**Code Scope:**
**Status:** compliant | partial | violated

## Summary
- Total decisions checked:
- Compliant:
- Partial:
- Violated:

## Compliance Gaps

### Gap 1
- **Type:** boundary violation | missing component | divergent pattern | outdated design
- **Design Source:**
- **Code Location:**
- **Impact Scope:**
- **Root Cause:**
- **Remediation:**

## Recommended Next Actions
1.
2.

## Machine-Readable Compliance

    gaps:
      - type: "boundary violation"
        designSource: "docs/architecture/adr-001.md"
        codeLocation: "pkg/infra/db.go"
        impactScope: "Domain layer imports infrastructure"
        rootCause: "Repository interface not used; direct DB import"
        remediation: "Implement repository pattern per ADR-001"
```

---

## Restrictions

### Hard Boundaries

- Do NOT invent design decisions when docs are missing; report blocked and suggest design workflow
- Do NOT claim compliance when design sources are incomplete or ambiguous
- Do NOT silently modify design docs without explicit user approval
- Do NOT perform structural code review without design reference (that is `review-architecture`)

### Skill Boundaries (Avoid Overlap)

**Do NOT do these**:

- Code-only structure review → `review-architecture`
- Design creation or alternatives → `brainstorm-design`
- Planning layer traceback → `align-planning`

**When to stop and hand off**:

- No design docs exist → suggest `brainstorm-design` or `bootstrap-project-documentation`
- Design is conflicting or outdated → hand off to `brainstorm-design`
- Structural code review needed without design comparison → hand off to `review-architecture`

---

## Self-Check

### Core Success Criteria (ALL must be met)

- [ ] Design sources identified and parsed
- [ ] Code compared against documented decisions
- [ ] Each gap typed with impact scope and root cause
- [ ] Report persisted to agreed path
- [ ] Evidence references present for each gap
- [ ] Handoff recommendations provided when applicable

### Acceptance Test

**Can a teammate act on the top 1–3 compliance gaps without additional clarification?**

If NO: refine evidence and remediation clarity.

If YES: report is complete; proceed to handoff or remediation.

---

## Examples

### Example 1: Boundary Violation

**Context**: ADR-001 states domain must not import infrastructure. Code shows domain package importing DB driver.

**Output**:

- Type: boundary violation
- Design Source: `docs/process-management/decisions/20240101-adr-001-layered-architecture.md`
- Code Location: `pkg/domain/order.go` (imports `pkg/infra/db`)
- Impact: Domain is coupled to infrastructure; violates clean architecture
- Remediation: Define repository interface in domain; implement in infrastructure; inject via constructor

### Example 2: No Design Docs

**Context**: Project has no ADRs or design docs.

**Output**:

- Status: blocked
- Message: No architecture or design documents found. Run `brainstorm-design` to create design docs, or `bootstrap-project-documentation` to establish structure.
- Confidence: N/A
