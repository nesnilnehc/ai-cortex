---
name: assess-docs
description: Assess documentation health in one pass — validate artifact norms compliance (paths, naming, front-matter) and evidence readiness by layer; report gaps and produce a minimum-fill plan.
tags: [documentation, workflow]
version: 3.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [doc readiness, documentation readiness, doc gap, doc triage, validate docs, validate documents]
input_schema:
  type: free-form
  description: Project docs scope, optional layer mapping, optional target readiness level, optional docs root
output_schema:
  type: document-artifact
  description: Documentation Assessment Report (compliance findings + layer readiness + minimal fill plan)
  artifact_type: doc-assessment
  path_pattern: docs/calibration/doc-assessment.md
  lifecycle: living
---

# Skill: Documentation Assessment

## Purpose

In a single run, check that project documentation both **conforms to artifact norms** (paths, naming, front-matter) and is **sufficient for reliable AI-assisted planning and alignment**. Produce one report with compliance findings, layer readiness scores, and a minimal, prioritized fill plan to close critical gaps.

---

## Core Objective

**Primary Goal**: Produce a documentation assessment report that (1) lists norm violations with actionable suggestions, and (2) quantifies evidence quality by layer and prescribes the smallest set of document actions needed to reach target readiness.

**Success Criteria** (ALL must be met):

1. ✅ **Norms resolved**: Project norms from `docs/ARTIFACT_NORMS.md` or `.ai-cortex/artifact-norms.yaml`; fallback to spec/artifact-contract.md
2. ✅ **Compliance checked**: All relevant Markdown under `docs/` scanned; path, naming, front-matter validated; each violation emitted as a finding (Location, Category, Severity, Title, Description, Suggestion)
3. ✅ **Layer coverage assessed and readiness scored**: Goal, requirements, architecture, milestones, roadmap, and backlog layers evaluated and each layer scored as `strong`, `weak`, or `missing`; overall readiness computed
4. ✅ **Gaps prioritized**: Missing and weak layers ranked by impact on delivery and alignment
5. ✅ **Minimal fill plan produced**: Actionable steps with what to create/update first and why; handoff skills indicated
6. ✅ **Report persisted**: Single output document written to agreed path with compliance findings and readiness sections

**Acceptance Test**: Can a teammate fix norm violations and improve readiness using only this report, without guessing what to do first?

---

## Scope Boundaries

**This skill handles**:

- Resolving project artifact norms and scanning `docs/` for Markdown
- Compliance validation: path, naming, front-matter against norms; findings list in standard format
- Documentation inventory and layer mapping; readiness scoring and gap prioritization
- Minimal fill plan and handoff recommendations to specialized skills

**This skill does NOT handle**:

- Establishing or updating norms (use `discover-docs-norms`)
- Full requirements authoring from vague intent (use `analyze-requirements`)
- Full design synthesis (use `design-solution`)
- Structural docs bootstrap from scratch (use `bootstrap-docs`)
- Post-task drift calibration (use `align-planning`)
- Auto-fixing violations (user or other tools apply suggestions)

**Handoff point**: After report delivery, hand off norm creation to `discover-docs-norms`, and creation/update actions to the relevant documentation or planning skill.

---

## Use Cases

- **Pre-commit or audit**: Ensure docs comply with norms and are sufficient before milestone
- **Alignment confidence is low**: `align-planning` reports weak evidence quality
- **New repo with partial docs**: Team needs compliance check and minimum docs to add first
- **After norms change**: Re-validate and re-assess after updating ARTIFACT_NORMS.md
- **Documentation debt triage**: One report for both compliance and readiness prioritization

---

## Behavior

### Interaction Policy

- **Defaults**: Docs root = repository `docs/`; use project norms if present
- **Choice options**: Target readiness `[medium][high]`; path mapping when non-default
- **Confirm**: Output path when different from project norms; before write

### Phase 0: Resolve Scope and Mapping

1. Resolve docs root and optional custom path mapping
2. **Resolve project norms**: Check `.ai-cortex/artifact-norms.yaml` then `docs/ARTIFACT_NORMS.md` per [spec/artifact-norms-schema.md](../../spec/artifact-norms-schema.md). If found, use for path patterns, naming, and layer mapping; otherwise use [spec/artifact-contract.md](../../spec/artifact-contract.md) defaults.
3. Detect expected layer paths: Goals `docs/project-overview/`, Requirements `docs/requirements-planning/`, Architecture `docs/architecture/`, Milestones/Roadmap/Backlog `docs/process-management/` (and backlog paths). Accept backward-compatible aliases (e.g. `docs/requirements/`).

### Phase 1: Compliance Validation

1. Enumerate Markdown under `docs/` (or user-specified root)
2. For each file: read front-matter for `artifact_type`; if absent, infer from path (e.g. `backlog/` → backlog-item, `design-decisions/` → design). Map to expected path_pattern and naming from norms.
3. Validate path, filename, and front-matter (required fields such as `artifact_type`, `created_by` when applicable) against norms.
4. Emit one finding per violation: Location (path), Category (`artifact-norms` | `path` | `naming` | `front-matter`), Severity (`critical` | `major` | `minor` | `suggestion`), Title, Description, Suggestion. Summary: total files scanned, violations count by severity.

**Findings format** (each finding MUST follow):

| Field | Content |
| :--- | :--- |
| Location | `path/to/file.md` |
| Category | `artifact-norms` \| `path` \| `naming` \| `front-matter` |
| Severity | `critical` \| `major` \| `minor` \| `suggestion` |
| Title | Short violation summary |
| Description | What is wrong |
| Suggestion | How to fix (e.g. move to X, add front-matter Y) |

### Phase 2: Inventory and Evidence Collection

1. Enumerate relevant docs per layer
2. Check freshness signals (last updated date, stale references, broken links where obvious)
3. Label evidence source: `canonical` (project planning docs), `secondary` (issue/PR/commit context), `none`

### Phase 3: Readiness Scoring

Assign one readiness level per layer:

- **strong**: canonical docs exist and appear current enough for decision support
- **weak**: docs exist but incomplete, stale, or dependent on secondary evidence
- **missing**: no usable docs for the layer

Score overall readiness:

- `high`: no missing layers and at most one weak layer
- `medium`: one or more weak layers, no critical missing layer
- `low`: at least one critical missing layer (requirements, architecture, or roadmap/backlog)

### Phase 4: Gap Prioritization

For each gap, rate impact (high | medium | low), effort (small | medium | large), owner, dueWindow (this-sprint | next-sprint | backlog). Prioritize by highest delivery risk reduction per smallest effort first.

### Phase 5: Minimal Fill Plan

Produce the smallest set of actions to raise readiness to target level: layer to fix first, exact document path(s) to create/update, suggested handoff skill (`bootstrap-docs`, `analyze-requirements`, `design-solution`), and stop condition for this cycle.

### Phase 6: Persist Report

Write to path per resolved project norms or default `docs/calibration/doc-assessment.md`. Overwrite the canonical file unless the user explicitly requests a dated snapshot. Include front-matter: `artifact_type: doc-assessment`, `created_by: assess-docs`, `lifecycle: living`, `created_at: YYYY-MM-DD`. Create output directory if it does not exist. Report MUST include Compliance Findings and Readiness sections below.

---

## Input & Output

### Input

- Docs root path (default repository docs root)
- Optional path mapping for non-template projects
- Optional target readiness (`medium` or `high`)

### Output

Single document artifact with the following structure:

```markdown
---
artifact_type: doc-assessment
created_by: assess-docs
lifecycle: living
created_at: YYYY-MM-DD
---

# Documentation Assessment Report

**Date:** YYYY-MM-DD
**Overall Readiness:** high | medium | low
**Target Readiness:** medium | high

## Compliance Findings

Summary: N files scanned; M violations (by severity: critical, major, minor, suggestion).

| Location | Category | Severity | Title | Description | Suggestion |
| :--- | :--- | :--- | :--- | :--- | :--- |
| path/to/file.md | artifact-norms | major | ... | ... | ... |

(If no violations: "No norm violations found.")

## Layer Readiness

- Goal: strong | weak | missing
- Requirements: strong | weak | missing
- Architecture: strong | weak | missing
- Milestones: strong | weak | missing
- Roadmap: strong | weak | missing
- Backlog: strong | weak | missing

## Gap Priority List

1. Gap: ...
   Impact: high | medium | low
   Effort: small | medium | large
   Owner: ...
   DueWindow: this-sprint | next-sprint | backlog

## Minimal Fill Plan

1. Path: ...
   Why now: ...
   Handoff skill: ...
   Done condition: ...

## Machine-Readable Summary

    overallReadiness: "medium"
    complianceSummary: { filesScanned: N, violations: M }
    layers:
      requirements: "missing"
      architecture: "weak"
    gaps:
      - id: "gap-req-core"
        impact: "high"
        effort: "small"
        owner: "product-owner"
        dueWindow: "this-sprint"
```

---

## Restrictions

### Hard Boundaries

- Do NOT fabricate non-existent docs
- Do NOT rewrite product strategy, requirements, or architecture decisions in this skill
- Do NOT prescribe a full documentation overhaul when a minimal plan is sufficient
- Do NOT mark readiness as high when critical layers are missing
- **Compliance phase**: Do not modify files; only report findings. Findings MUST follow the standard format above.

### Skill Boundaries (Avoid Overlap)

**Do NOT do these (other skills handle them)**:

- Create or update artifact norms → `discover-docs-norms`
- Template bootstrap and structural initialization → `bootstrap-docs`
- Requirement content development → `analyze-requirements`
- Architecture/design decision workflow → `design-solution`
- Post-task drift and recalibration → `align-planning`
- Auto-fix violations → User applies suggestions

**When to stop and hand off**:

- If norms are missing or need update → hand off to `discover-docs-norms`
- If the primary gap is requirements quality → hand off to `analyze-requirements`
- If the primary gap is architecture clarity → hand off to `design-solution`
- If docs skeleton is missing broadly → hand off to `bootstrap-docs`

---

## Self-Check

### Core Success Criteria (ALL must be met)

- [ ] Norms resolved; docs scanned
- [ ] Compliance findings emitted in standard format (Location, Category, Severity, Title, Description, Suggestion)
- [ ] All planning layers assessed; readiness per layer scored with rationale
- [ ] Gaps prioritized by impact and effort
- [ ] Minimal fill plan includes concrete paths and handoffs
- [ ] Output persisted to agreed path with both Compliance Findings and Readiness sections

### Process Quality Checks

- [ ] Canonical vs secondary evidence clearly separated
- [ ] Critical missing layers not hidden in aggregate score
- [ ] Recommendations are minimal and sequencing-aware
- [ ] Handoff skill names are valid and current

### Acceptance Test

**Can the team fix norm violations and improve readiness using the top 3 actions in the report?**

If NO: reduce ambiguity and tighten prioritization or findings.
If YES: report is complete.

---

## Examples

### Example 1: Compliance + Readiness

- Compliance: `docs/designs/2026-03-06-auth.md` in non-standard path → finding with Suggestion "Move to docs/design-decisions/2026-03-06-auth.md"
- Readiness: requirements layer missing → Plan: create `docs/requirements-planning/core-v1.md` first using `analyze-requirements`

### Example 2: Missing Requirements Layer

- Findings: goals and roadmap exist, requirements docs missing
- Readiness: `low`
- Plan: create `docs/requirements-planning/core-v1.md` first using `analyze-requirements`

### Example 3: Weak Architecture Layer

- Findings: architecture docs exist but stale and contradicted by recent ADRs
- Readiness: `medium`
- Plan: refresh architecture decision docs, then rerun `align-planning`

### Example 4: Path Mismatch (Compliance)

- File: `docs/designs/2026-03-06-auth.md` (project norm: `docs/design-decisions/`)
- Finding: Location `docs/designs/2026-03-06-auth.md`, Category `artifact-norms`, Severity `major`, Title "Design doc in non-standard path", Description "File is under docs/designs/ but norms specify docs/design-decisions/", Suggestion "Move to docs/design-decisions/2026-03-06-auth.md"
