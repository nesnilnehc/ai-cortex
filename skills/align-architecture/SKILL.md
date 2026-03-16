---
name: align-architecture
description: Verify architecture and design documents against code implementation; produce an Architecture Compliance Report when implementation diverges from ADR or design decisions.
tags: [workflow, eng-standards, documentation]
version: 1.2.0
license: MIT
related_skills: [align-planning, review-architecture, design-solution, assess-doc-readiness, bootstrap-docs]
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
      - "v1.1.0: Partial verification when only some modules have design docs; evidence readiness; orchestration guidance; remediation clarity for outdated design"
triggers: [align architecture, architecture compliance, design vs code, post implementation, post merge]
input_schema:
  type: free-form
  description: ADR or design doc scope, optional code scope (full repo, paths, or modules for incremental verification), optional project docs root
output_schema:
  type: document-artifact
  description: Architecture Compliance Report written to docs/calibration/architecture-compliance.md (default)
  artifact_type: architecture-compliance
  path_pattern: docs/calibration/architecture-compliance.md
  lifecycle: living
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
5. ✅ **Evidence referenced**: Each gap cites specific design sources and code locations; when partial verification is used, covered/uncovered scope and confidence are explicit
6. ✅ **Handoff suggested**: When design is outdated or conflicting, suggest `design-solution`; when structure review needed, suggest `review-architecture`

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
- Design creation or design alternatives (use `design-solution`)
- Planning layer alignment (use `align-planning`)

**Handoff point**: After the report, hand off to `design-solution` if design must change, or to `review-architecture` for structural code review without design comparison.

---

## Use Cases

- **Post-implementation check**: Validate that implementation matches ADR or design doc
- **Milestone or release gate**: Ensure architecture decisions are reflected in code
- **Drift investigation**: Diagnose when implementation has drifted from documented design
- **Onboarding audit**: Help new contributors understand design vs actual state

---

## Orchestration Guidance

| Scenario | Recommended Sequence |
| --- | --- |
| Routine task completed | `align-planning` (Lightweight) |
| Milestone or release gate | `align-planning` (Full) → then `align-architecture` |
| Post-implementation check | `align-architecture` |
| Planning and architecture both in question | `align-planning` first; if report suggests design-code drift → `align-architecture` |

Run `align-planning` before `align-architecture` when planning layer alignment is uncertain; otherwise run `align-architecture` standalone for design vs code verification.

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
2. Resolve code scope:
   - **Full**: entire repo (default)
   - **Incremental**: user-specified paths, packages, or modules (for large codebases; verify only affected design decisions)
3. If no design docs exist, output blocked report with required minimum inputs; suggest `design-solution` or `bootstrap-docs`

### Phase 0.5: Evidence Readiness Assessment

Assess design coverage before comparison:

- **strong**: Design docs exist for all relevant components/modules in scope
- **weak**: Partial design docs; some components have ADRs, others do not — perform partial verification with reduced confidence
- **missing**: No design docs; report blocked, suggest design workflow

Rules:

1. When readiness is `weak`, verify only decisions that have design sources; mark uncovered code as `unknown` and list in report.
2. Do NOT claim high confidence when readiness is `weak`.
3. Explicitly report: covered scope, uncovered scope, and confidence level.

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
   - **Outdated design**: Design doc may be stale; implementation may reflect current intent — assign `recommended_action`:
     - `update_design`: Implementation is authoritative; design should be updated to match (suggest `design-solution`)
     - `update_code`: Design remains authoritative; code should be refactored to match
     - `both`: Ambiguous; requires stakeholder decision; suggest `design-solution` to reconcile

### Phase 3: Produce Report

1. Aggregate findings with impact scope, root cause, and `recommended_action` per gap
2. For each gap, state clearly: update code, update design, or both (see gap type above)
3. Recommend handoff to `design-solution` when design must change; to `review-architecture` when structure-only review needed
4. Include evidence readiness and confidence when partial verification was used

### Phase 4: Persist Report

Write report to:

- Path resolved from project norms (`docs/ARTIFACT_NORMS.md` or `.ai-cortex/artifact-norms.yaml`)
- Default: `docs/calibration/architecture-compliance.md` (overwrite unless snapshot explicitly requested)
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
**Evidence Readiness:** strong | weak | missing (when partial verification used)
**Confidence:** high | medium | low

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
- **Recommended Action:** update_code | update_design | both
- **Remediation:**

## Covered / Uncovered Scope (when partial verification)
- Covered:
- Uncovered:
- Reason:

## Recommended Next Actions
1.
2.

## Machine-Readable Compliance

    evidence:
      readiness: "strong"  # strong | weak | missing
      confidence: "high"   # high | medium | low
    gaps:
      - type: "boundary violation"
        designSource: "docs/architecture/adr-001.md"
        codeLocation: "pkg/infra/db.go"
        impactScope: "Domain layer imports infrastructure"
        rootCause: "Repository interface not used; direct DB import"
        recommendedAction: "update_code"  # update_code | update_design | both
        remediation: "Implement repository pattern per ADR-001"
```

---

## Restrictions

### Hard Boundaries

- Do NOT invent design decisions when docs are missing; report blocked and suggest design workflow
- Do NOT claim high confidence when evidence readiness is `weak` (partial verification)
- Do NOT claim compliance when design sources are incomplete or ambiguous
- Do NOT silently modify design docs without explicit user approval
- Do NOT perform structural code review without design reference (that is `review-architecture`)

### Skill Boundaries (Avoid Overlap)

**Do NOT do these (other skills handle them)**:

- Code-only structure review → `review-architecture`
- Design creation or alternatives → `design-solution`
- Planning layer traceback → `align-planning`

**When to stop and hand off**:

- No design docs exist → suggest `design-solution` or `bootstrap-docs`
- Design is conflicting or outdated → hand off to `design-solution`
- Structural code review needed without design comparison → hand off to `review-architecture`

---

## Self-Check

### Core Success Criteria (ALL must be met)

- [ ] Design sources identified and parsed
- [ ] Code compared against documented decisions (or partial verification when readiness is weak)
- [ ] Each gap typed with impact scope, root cause, and `recommended_action` when type is outdated design
- [ ] Report persisted to agreed path
- [ ] Evidence references present for each gap (including covered/uncovered scope and confidence when partial verification used)
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
- Message: No architecture or design documents found. Run `design-solution` to create design docs, or `bootstrap-docs` to establish structure.
- Confidence: N/A

### Example 3: Partial Verification (Weak Readiness)

**Context**: Only `pkg/auth` has an ADR; `pkg/orders` and `pkg/inventory` have no design docs.

**Output**:

- Evidence Readiness: weak
- Confidence: medium
- Covered scope: `pkg/auth` (verified against ADR-002)
- Uncovered scope: `pkg/orders`, `pkg/inventory` (no design sources; marked unknown)
- Report continues with findings for `pkg/auth`; recommends creating design docs for uncovered packages if compliance is required

### Example 4: Outdated Design with Recommended Action

**Context**: ADR-003 specifies sync API; implementation uses async event-driven flow and stakeholders prefer it.

**Output**:

- Type: outdated design
- Recommended Action: update_design
- Remediation: Update ADR-003 to document async event-driven approach; implementation is authoritative. Hand off to `design-solution` to revise design doc.
