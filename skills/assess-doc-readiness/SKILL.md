---
name: assess-doc-readiness
description: Assess doc evidence readiness across project layers, report gaps, and produce a minimum-fill plan to improve alignment reliability.
tags: [documentation, eng-standards, workflow]
version: 1.1.0
license: MIT
related_skills: [bootstrap-docs, analyze-requirements, brainstorm-design, align-planning, align-architecture]
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [doc readiness, documentation readiness, doc gap, doc triage]
input_schema:
  type: free-form
  description: Project docs scope, optional layer mapping, and optional target readiness level
output_schema:
  type: document-artifact
  description: Documentation Readiness Report and Minimal Fill Plan
  artifact_type: doc-readiness
  path_pattern: docs/calibration/doc-readiness.md
  lifecycle: living
---

# Skill: Documentation Readiness

## Purpose

Evaluate whether project documentation is sufficient for reliable AI-assisted planning and alignment, then provide a minimal, prioritized fill plan to close critical gaps.

---

## Core Objective

**Primary Goal**: Produce a documentation readiness report that quantifies evidence quality by layer and prescribes the smallest set of document actions needed to reach target readiness.

**Success Criteria** (ALL must be met):

1. ✅ **Layer coverage assessed**: Goal, requirements, architecture, milestones, roadmap, and backlog layers are evaluated
2. ✅ **Readiness scored**: Each layer is scored as `strong`, `weak`, or `missing`
3. ✅ **Gaps prioritized**: Missing and weak layers are ranked by impact on delivery and alignment
4. ✅ **Minimal fill plan produced**: Actionable steps identify what to create/update first and why
5. ✅ **Boundaries preserved**: The skill does not rewrite product requirements or redesign architecture content
6. ✅ **Report persisted**: Output document is written to agreed location

**Acceptance Test**: Can a teammate start improving project documentation immediately using only this report, without guessing what to write first?

---

## Scope Boundaries

**This skill handles**:

- Documentation inventory and layer mapping
- Readiness scoring and confidence impact analysis
- Gap prioritization and minimum-fill planning
- Handoff recommendations to specialized skills

**This skill does NOT handle**:

- Full requirements authoring from vague intent (use `analyze-requirements`)
- Full design synthesis (use `brainstorm-design`)
- Structural docs bootstrap from scratch templates (use `bootstrap-docs`)
- Post-task drift calibration (use `align-planning`)

**Handoff point**: After report delivery, hand off creation/update actions to the relevant documentation or planning skill.

---

## Use Cases

- **Alignment confidence is low**: `align-planning` reports weak evidence quality
- **New repo with partial docs**: Team needs to know the minimum docs to add first
- **Pre-release governance**: Verify documentation sufficiency before milestone closure
- **Documentation debt triage**: Prioritize docs work without boiling the ocean

---

## Behavior

### Interaction Policy

- **Defaults**: Docs root = repository docs/; use project norms if present
- **Choice options**: Target readiness `[medium][high]`; path mapping when non-default
- **Confirm**: Output path when different from project norms; before write

### Phase 0: Resolve Scope and Mapping

1. Resolve docs root and optional custom path mapping
2. **Resolve project norms**: Check for `.ai-cortex/artifact-norms.yaml` or `docs/ARTIFACT_NORMS.md` per [spec/artifact-norms-schema.md](../../spec/artifact-norms-schema.md). If found, use project paths for layer mapping and output; otherwise use defaults.
3. Detect expected layer paths per resolved norms or [spec/artifact-contract.md](../../spec/artifact-contract.md):
   - Goals: `docs/project-overview/`
   - Requirements: `docs/requirements-planning/`
   - Architecture: `docs/architecture/`
   - Milestones/Roadmap/Backlog: `docs/process-management/` (backlog: `docs/process-management/project-board/backlog/` or `docs/backlog/`)
4. Accept backward-compatible aliases when present (for example, `docs/requirements/`)

### Phase 1: Inventory and Evidence Collection

1. Enumerate relevant docs per layer
2. Check freshness signals (last updated date, stale references, broken links where obvious)
3. Label evidence source:
   - `canonical`: project planning docs
   - `secondary`: issue/PR/commit context
   - `none`

### Phase 2: Readiness Scoring

Assign one readiness level per layer:

- **strong**: canonical docs exist and appear current enough for decision support
- **weak**: docs exist but incomplete, stale, or dependent on secondary evidence
- **missing**: no usable docs for the layer

Score overall readiness:

- `high`: no missing layers and at most one weak layer
- `medium`: one or more weak layers, no critical missing layer
- `low`: at least one critical missing layer (requirements, architecture, or roadmap/backlog)

### Phase 3: Gap Prioritization

For each gap, rate:

- `impact`: high | medium | low
- `effort`: small | medium | large
- `owner`: suggested role/team
- `dueWindow`: this-sprint | next-sprint | backlog

Prioritize by highest delivery risk reduction per smallest effort first.

### Phase 4: Minimal Fill Plan

Produce the smallest set of actions needed to raise readiness to target level:

1. Layer to fix first and expected outcome
2. Exact document path(s) to create/update
3. Suggested handoff skill (`bootstrap-docs`, `analyze-requirements`, `brainstorm-design`)
4. Stop condition for this cycle

### Phase 5: Persist Report

Write to path per resolved project norms (Phase 0) or default `docs/calibration/doc-readiness.md` from [spec/artifact-contract.md](../../spec/artifact-contract.md). Overwrite the canonical file unless the user explicitly requests a dated snapshot. Include front-matter: `artifact_type: doc-readiness`, `created_by: assess-doc-readiness`, `lifecycle: living`, `created_at: YYYY-MM-DD`. Create output directory if it does not exist.

---

## Input & Output

### Input

- Docs root path (default repository docs root)
- Optional path mapping for non-template projects
- Optional target readiness (`medium` or `high`)

### Output

```markdown
---
artifact_type: doc-readiness
created_by: assess-doc-readiness
lifecycle: living
created_at: YYYY-MM-DD
---

# Documentation Readiness Report

**Date:** YYYY-MM-DD
**Overall Readiness:** high | medium | low
**Target Readiness:** medium | high

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

### Skill Boundaries (Avoid Overlap)

**Do NOT do these (other skills handle them)**:

- Template bootstrap and structural initialization -> `bootstrap-docs`
- Requirement content development -> `analyze-requirements`
- Architecture/design decision workflow -> `brainstorm-design`
- Post-task drift and recalibration -> `align-planning`

**When to stop and hand off**:

- If the primary gap is requirements quality -> hand off to `analyze-requirements`
- If the primary gap is architecture clarity -> hand off to `brainstorm-design`
- If docs skeleton is missing broadly -> hand off to `bootstrap-docs`

---

## Self-Check

### Core Success Criteria (ALL must be met)

- [ ] All planning layers assessed
- [ ] Readiness per layer scored with rationale
- [ ] Gaps prioritized by impact and effort
- [ ] Minimal fill plan includes concrete paths and handoffs
- [ ] Output persisted to agreed path

### Process Quality Checks

- [ ] Canonical vs secondary evidence clearly separated
- [ ] Critical missing layers not hidden in aggregate score
- [ ] Recommendations are minimal and sequencing-aware
- [ ] Handoff skill names are valid and current

### Acceptance Test

**Can the team improve readiness in one sprint using only the top 3 actions?**

If NO: reduce ambiguity and tighten prioritization.

If YES: report is complete.

---

## Examples

### Example 1: Missing Requirements Layer

- Findings: goals and roadmap exist, requirements docs missing
- Readiness: `low`
- Plan: create `docs/requirements-planning/core-v1.md` first using `analyze-requirements`

### Example 2: Weak Architecture Layer

- Findings: architecture docs exist but stale and contradicted by recent ADRs
- Readiness: `medium`
- Plan: refresh architecture decision docs, then rerun `align-planning`

### Example 3: Empty Docs Skeleton

- Findings: no structured docs tree, only README exists
- Readiness: `low`
- Plan: hand off to `bootstrap-docs` for baseline structure, then rerun this skill
