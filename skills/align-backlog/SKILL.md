---
name: align-backlog
description: Align the product or work backlog with the current strategy, goals, and roadmap. Analyze backlog items, identify misaligned or orphan work, and propose concrete changes (adds, cuts, reprioritization) so backlog clearly supports strategic outcomes.
tags: [workflow, eng-standards, documentation]
version: 1.0.0
license: MIT
related_skills: [align-planning, align-architecture, design-strategic-goals, define-roadmap, capture-work-items, run-strategy-checkpoint]
recommended_scope: both
aliases: [align-backlog-to-strategy]
metadata:
  author: ai-cortex
triggers: [align backlog, backlog alignment, backlog to strategy, align backlog to strategy]
input_schema:
  type: free-form
  description: Optional backlog location (path or convention), optional strategy docs root, optional scope (full backlog vs subset)
  defaults:
    scope: full
output_schema:
  type: document-artifact
  description: Backlog Alignment Report written to docs/calibration/backlog-alignment.md (default)
  artifact_type: backlog-alignment
  path_pattern: docs/calibration/backlog-alignment.md
  lifecycle: living
---

# Skill: Align Backlog

## Purpose

Align the product or work backlog with the current strategy, goals, and roadmap. Analyze existing backlog items against strategic sources, identify misaligned or orphan work, and produce a Backlog Alignment Report with concrete change proposals (adds, cuts, merges, reprioritization) so the backlog clearly supports strategic outcomes.

---

## Core Objective

**Primary Goal**: Produce an actionable Backlog Alignment Report that maps backlog items to strategy/goals/roadmap, classifies alignment status, and recommends concrete backlog changes.

**Success Criteria** (ALL must be met):

1. ✅ **Backlog and strategy sources located**: Backlog artifact(s) and strategy-layer docs (goals, roadmap, milestones) are identified and parsed
2. ✅ **Mapping produced**: Each backlog item (or representative sample) is mapped to at least one strategic anchor (goal, milestone, roadmap theme) or marked as orphan/unmapped
3. ✅ **Misalignment classified**: Items are classified (aligned, partial, misaligned, orphan) with rationale; impact and root cause are stated per finding
4. ✅ **Change proposals listed**: Concrete recommendations (add, cut, merge, reprioritize) are provided with priority and traceability to strategy
5. ✅ **Report persisted**: Backlog Alignment Report is written to the agreed path
6. ✅ **Unsafe writes avoided**: If backlog location is uncertain or proposed edits are destructive, user confirmation is requested before applying changes

**Acceptance Test**: Can a product or delivery lead read the report and immediately understand which backlog items support strategy, which do not, and what to add, cut, or reorder?

---

## Scope Boundaries

**This skill handles**:

- Backlog inventory and strategy-layer discovery
- Mapping backlog items to goals, milestones, and roadmap
- Classifying alignment (aligned, partial, misaligned, orphan)
- Proposing concrete backlog changes (adds, cuts, merges, reprioritization)
- Persisting a Backlog Alignment Report

**This skill does NOT handle**:

- Post-task traceback and planning drift (use `align-planning`)
- Architecture vs code compliance (use `align-architecture`)
- Defining or rewriting strategy (use `define-mission`, `design-strategic-goals`, `define-roadmap`, etc.)
- Creating new backlog items from scratch (use `capture-work-items` or `analyze-requirements`)
- Running a full strategy checkpoint or governance cycle (use `run-checkpoint`)

**Handoff point**: After the report is produced, hand off to the appropriate skill by need — e.g. `align-planning` for execution traceback, or product/backlog tooling for applying changes.

---

## Use Cases

- **Backlog health check**: Periodically ensure backlog items trace to current strategy
- **After strategy refresh**: Re-align backlog when goals, roadmap, or milestones have changed
- **Sprint or release prep**: Prioritize and trim backlog using strategy as the source of truth
- **Orphan cleanup**: Identify and propose removal or repurposing of work that no longer supports strategy

---

## Orchestration Guidance

| Scenario | Recommended use |
| --- | --- |
| Strategy docs updated | `align-backlog` to re-map backlog to new goals/roadmap |
| Backlog feels overloaded or off-strategy | `align-backlog` first; then `align-planning` if execution traceback is also needed |
| Milestone or release gate | Run `align-backlog` for the relevant backlog slice; governance status is aggregated via `run-checkpoint` when needed |

---

## Behavior

### Agent Prompt Contract

```text
You are responsible for backlog alignment with strategy.

Analyze the product or work backlog against the current strategy, goals, and roadmap.
Map items to strategic anchors, classify alignment, and produce a Backlog Alignment Report
with concrete change proposals (adds, cuts, reprioritization).
```

### Interaction Policy

- **Defaults**: Backlog from project norms or common paths (`docs/backlog/`, `*.md` in backlog dir, or project convention); strategy docs from `docs/project-overview/`, `docs/process-management/`; scope = full backlog
- **Choice options**: Explicit backlog path and strategy docs root when non-default; scope = subset when backlog is large (e.g. by epic or label)
- **Confirm**: Before proposing edits to backlog files; before large cut/merge recommendations

### Phase 0: Resolve Backlog and Strategy Sources

1. Resolve backlog location (project norms, `docs/ARTIFACT_NORMS.md`, or default: `docs/backlog/`, repo backlog convention)
2. Resolve strategy sources: goals, roadmap, milestones (e.g. `docs/project-overview/`, `docs/process-management/`)
3. If no strategy docs exist, report blocked and suggest defining strategy first (`design-strategic-goals`, `define-roadmap`, etc.)
4. If no backlog found, report blocked and suggest backlog location or `capture-work-items` to seed one

### Phase 1: Map Backlog to Strategy

1. List backlog items (or sampled set if backlog is very large)
2. For each item, determine traceability: which goal, milestone, or roadmap theme it supports (or mark orphan)
3. Record mapping and evidence (e.g. labels, descriptions, links)

### Phase 2: Classify Alignment

For each item (or aggregate by theme):

- **aligned**: Clearly supports a current goal/roadmap/milestone; priority consistent
- **partial**: Supports strategy but priority or scope may need adjustment
- **misaligned**: No longer fits current strategy or duplicates/conflicts with higher-priority work
- **orphan**: No traceable link to strategy; candidate for cut or repurposing

Include impact scope and root cause per finding.

### Phase 3: Propose Changes

1. **Cuts**: Items to remove or archive (orphan, superseded, or out of scope)
2. **Merges**: Items to combine or deduplicate
3. **Reprioritization**: Order changes so highest strategic value is clear
4. **Adds**: Gaps where strategy implies work not yet in backlog (optional; list as suggestions only)

Each proposal must reference strategy (goal/roadmap/milestone) and item ID or title.

### Phase 4: Persist Report

Write report to:

- Path from project norms or default: `docs/calibration/backlog-alignment.md`
- Or user-specified path

Report must include a machine-readable block (YAML or JSON) for alignment status and change proposals.

---

## Input & Output

### Input

- Optional backlog path or convention
- Optional strategy docs root
- Optional scope (full vs subset by epic/label/time window)

### Output

#### Backlog Alignment Report Template

```markdown
# Backlog Alignment Report

**Date:** YYYY-MM-DD
**Backlog source:**
**Strategy sources:**
**Status:** aligned | partial | misaligned | blocked
**Confidence:** high | medium | low

## Summary
- Total items reviewed:
- Aligned:
- Partial:
- Misaligned:
- Orphan:

## Mapping (sample or full)
| Item | Strategic anchor | Status |
| --- | --- | --- |
| ... | ... | ... |

## Misalignment and Orphans
- Item / theme:
  Impact:
  Root cause:
  Recommendation: cut | merge | reprioritize | add

## Change Proposals
1. [Cut] ...
2. [Reprioritize] ...
3. [Merge] ...
4. [Add] ...

## Recommended Next Actions
1.
2.

## Machine-Readable Block

    alignment:
      summary: { aligned: N, partial: N, misaligned: N, orphan: N }
      items: []
    proposals:
      cut: []
      merge: []
      reprioritize: []
      add: []
```

---

## Restrictions

### Hard Boundaries

- Do NOT invent strategy when docs are missing; report blocked and suggest strategy definition skills
- Do NOT silently edit backlog artifacts without explicit user approval
- Do NOT perform planning-layer traceback (that is `align-planning`) or architecture compliance (that is `align-architecture`)

### Skill Boundaries (Avoid Overlap)

**Do NOT do these (other skills handle them)**:

- Post-task planning alignment and drift detection → `align-planning`
- Architecture vs code compliance → `align-architecture`
- Defining mission, goals, roadmap → `define-mission`, `design-strategic-goals`, `define-roadmap`
- Creating new work items from free form → `capture-work-items`, `analyze-requirements`
- Full governance checkpoint at milestone or release gate → `run-checkpoint`

**When to stop and hand off**:

- Strategy docs missing or stale → suggest `design-strategic-goals`, `define-roadmap`, etc.
- User needs execution traceback after task → hand off to `align-planning`
- User needs design vs code check → hand off to `align-architecture`

---

## Self-Check

### Core Success Criteria (ALL must be met)

- [ ] Backlog and strategy sources identified and parsed
- [ ] Backlog items mapped to strategic anchors (or marked orphan)
- [ ] Alignment classified (aligned, partial, misaligned, orphan) with rationale
- [ ] Change proposals (cut, merge, reprioritize, add) listed with traceability
- [ ] Report persisted to agreed path
- [ ] User confirmation requested where edits or scope are uncertain

### Process Quality Checks

- [ ] Default paths and scope documented when used
- [ ] Each proposal references strategy source and item
- [ ] Machine-readable block included in report
- [ ] Handoffs to other skills suggested when applicable

### Acceptance Test

**Can a product or delivery lead act on the top 3–5 change proposals without additional clarification?**

If NO: refine mapping and proposal rationale.

If YES: report is complete; proceed to handoff or backlog update.

---

## Examples

### Example 1: Backlog After Strategy Refresh

**Context**: Strategic goals and roadmap were updated; backlog has 50+ items.

**Behavior**:

1. Load goals and roadmap from `docs/project-overview/`, `docs/process-management/`
2. Load backlog from `docs/backlog/` (or project convention)
3. Map each item to a goal/roadmap theme or mark orphan
4. Classify: 30 aligned, 10 partial, 5 misaligned, 5 orphan
5. Propose: cut 5 orphan, reprioritize 10 partial, merge 2 duplicate themes
6. Persist report to `docs/calibration/backlog-alignment.md`

### Example 2: No Strategy Docs

**Context**: Project has no goals or roadmap documents.

**Output**:

- Status: blocked
- Message: No strategy documents found. Define goals and roadmap first (e.g. `design-strategic-goals`, `define-roadmap`) then re-run align-backlog.
- Confidence: N/A

### Example 3: Large Backlog, Subset Scope

**Context**: Backlog has 200 items; user wants alignment for "Q2 theme" only.

**Behavior**:

1. Resolve backlog and strategy sources
2. Filter backlog by Q2 theme (label or path)
3. Map and classify subset; report notes "subset of full backlog"
4. Propose changes for the subset only; recommend full backlog run later
