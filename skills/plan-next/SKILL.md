---
name: plan-next
description: Analyze project state and produce next-action plan by running alignment, doc readiness, and output-driven follow-ups. Single-cycle report with executed steps and Recommended Next Tasks.
tags: [workflow, automation, eng-standards]
version: 1.3.0
license: MIT
related_skills: [analyze-requirements, design-solution, align-planning, align-architecture, assess-docs, run-repair-loop, discover-docs-norms, bootstrap-docs]
recommended_scope: project
metadata:
  author: ai-cortex
  evolution:
    enhancements:
      - "v1.2.0: Phase 0.5 Planning Readiness Gate; discover-docs-norms, bootstrap-docs in preparation flow"
triggers: [checkpoint, run checkpoint, governance, iteration, next step, plan next step]
aliases: [run-checkpoint, pcl]
input_schema:
  type: free-form
  description: Project stage context, trigger event, and optional governance scope
  defaults:
    trigger: task-complete
output_schema:
  type: document-artifact
  description: Cycle report with executed steps, skipped steps, rationale, and next-cycle recommendations
  artifact_type: cognitive-loop
  path_pattern: docs/calibration/cognitive-loop.md
  lifecycle: living
---

# Skill: Run Checkpoint (Orchestrator)

## Purpose

Run a repeatable governance loop for projects by orchestrating specialized skills across planning, execution, alignment, and documentation readiness.

---

## Core Objective

**Primary Goal**: Produce a cycle report that shows what governance checks were run, what was learned, what is blocked, and what to do next.

**Success Criteria** (ALL must be met):

1. ✅ **Trigger classified (metadata only)**: The initiating event is recorded for reporting; it does not drive routing
2. ✅ **Unified sequence executed**: Fixed sequence runs; output-driven conditionals determine follow-up skills
3. ✅ **Decisions explained**: Every executed or skipped step has rationale
4. ✅ **Cross-skill handoffs explicit**: Outputs and next owners are documented
5. ✅ **Cycle report delivered**: One aggregated report is produced and persisted
6. ✅ **No scope bleed**: The orchestrator does not perform atomic analysis itself

**Acceptance Test**: Can a team run the next iteration without asking which skill to use or in what order?

---

## Scope Boundaries

**This skill handles**:

- Planning Readiness Gate: diagnostic and preparation orchestration (discover-docs-norms, bootstrap-docs, assess-docs)
- Scenario detection and orchestration
- Cross-skill sequencing and handoff control
- Aggregating outputs into a single governance view
- Recommending next cycle actions

**This skill does NOT handle**:

- Requirements analysis content itself (`analyze-requirements`)
- Design content itself (`design-solution`)
- Alignment analysis itself (`align-planning`)
- Architecture compliance analysis itself (`align-architecture`)
- Documentation gap analysis itself (`assess-docs`)
- Direct code repair execution (`run-repair-loop`)

**Handoff point**: After cycle report publication, hand off execution to the owning atomic skill or engineering team.

---

## Use Cases

- **Task completed**: verify alignment and docs sufficiency before next priority
- **Milestone closed**: run full governance check
- **Release candidate**: run design/alignment/docs readiness gate
- **Quarterly planning refresh**: revisit requirements and architecture drift

---

## Behavior

### Orchestration Rule

This is a meta skill. It must route work to atomic skills and aggregate outputs. It must not replace them.

### Phase 0: Trigger Classification (Metadata Only)

Classify trigger into one of the following for **reporting and statistics**; trigger does **not** drive skill routing:

- `task-complete`
- `milestone-closed`
- `release-candidate`
- `scope-change`
- `periodic-review`

### Phase 0.5: Planning Readiness Gate

Before Phase 1, determine whether the project has sufficient planning docs for align-planning to run meaningfully. If not, run preparation skills or short-circuit with a Minimal Fill Plan.

**Diagnostic**:

1. Check norms: `docs/ARTIFACT_NORMS.md` or `.ai-cortex/artifact-norms.yaml` exists; if not and `docs/` has non-standard paths, run `discover-docs-norms`.
2. Check structure: `docs/` exists with planning-related dirs (project-overview, requirements-planning, process-management). If missing, run `bootstrap-docs`.
3. Run `assess-docs` (in-process) to get readiness and Minimal Fill Plan.

**Branching**:

| State | Action |
| --- | --- |
| norms_missing | Run `discover-docs-norms`; re-run Phase 0.5 |
| structure_missing | Run `bootstrap-docs`; re-run Phase 0.5 |
| readiness=missing | Short-circuit: output cycle report with Minimal Fill Plan and Recommended Next Tasks; do NOT run Phase 1 |
| readiness=weak/strong | Proceed to Phase 1 |

**Short-circuit output**: When readiness=missing, persist a cycle report containing the Minimal Fill Plan from assess-docs and explicit Recommended Next Tasks (owner, scope, rationale). Do not run align-planning.

**Preparation skill outputs**: Outputs from `discover-docs-norms` and `bootstrap-docs` are project state (norms, docs structure) and MUST be persisted. Phase 1 skill outputs remain aggregated only.

### Phase 1: Unified Sequence + Output-Driven Branching

**Execute only when Phase 0.5 does not short-circuit.**

**Fixed sequence** (run when readiness is weak or strong):

1. `align-planning` (full) — planning layer traceback and drift
2. `assess-docs` — doc evidence assessment

**Output-driven follow-ups** (run only when outputs indicate need):

- `run-repair-loop` — when alignment or doc-readiness findings indicate active defects
- `design-solution` — when alignment reports architecture design conflict
- `analyze-requirements` — when alignment reports severe requirement drift
- `align-architecture` — when architecture vs code compliance check is needed (e.g. milestone/release context or alignment suggests)

User override always takes precedence.

### Interaction Policy

- **Defaults**: Infer trigger from context for metadata; always run unified sequence
- **Choice options**: Scope override or custom sequence before executing
- **Confirm**: Scope override or custom sequence before executing

### Phase 2: Execute and Collect

For each selected skill:

1. Record why it is selected
2. Run the skill's logic in-process (do not persist atomic skill outputs)
3. Capture key findings for aggregation
4. Record skipped skills and reason
5. Capture blockers and dependencies

**Single artifact rule**: This orchestrator produces exactly one output file. Do NOT write separate reports for `assess-docs`, `align-planning`, or other routed skills. All findings are aggregated into the cycle report.

### Phase 3: Aggregate Governance Report

Report must include:

- Trigger and scenario
- Sequence executed vs skipped
- Key findings by skill (inline summary; no cross-references to separate files)
- If planning/strategy alignment is in scope and `align-planning` or `align-backlog` ran: a **Strategy / Milestone status** subsection that summarizes per-milestone/goal status (on track / at risk / drifted / blocked) with brief evidence and recommended actions.
- Blockers and confidence level
- **Recommended Next Tasks** — explicit, prioritized, actionable tasks (owner, scope, and rationale)

### Phase 4: Persist

Write exactly one file to:

- Path resolved from project norms (`docs/ARTIFACT_NORMS.md` or `.ai-cortex/artifact-norms.yaml`)
- Default: `docs/calibration/cognitive-loop.md` (overwrite unless snapshot explicitly requested)
- Or user-defined path

---

## Input & Output

### Input

- Trigger event + context
- Optional target scope and mode overrides
- Optional urgency or release window

### Output

```markdown
# Project Cognitive Loop Report

**Date:** YYYY-MM-DD
**Trigger:** task-complete | milestone-closed | release-candidate | scope-change | periodic-review
**Scenario:** ...

## Routed Sequence
1. Skill: ...
   Why: ...
   Status: executed | skipped

## Aggregated Findings
- From align-planning:
- From assess-docs:
- From align-architecture: (if executed)
- From analyze-requirements: (if executed)
- From design-solution: (if executed)

## Strategy / Milestone Status (if applicable)
- Milestone / Goal: ...
  - Status: on track | at risk | drifted | blocked
  - Evidence: ...
  - Recommended action: ...

## Blockers and Confidence
- Blocker:
- Confidence: high | medium | low

## Recommended Next Tasks
1. [Task] — rationale; owner; scope
2. [Task] — rationale; owner; scope
3. [Task] — rationale; owner; scope
```

Next tasks must be explicit and actionable: what to do, why, who owns it, and in what order.

---

## Restrictions

### Hard Boundaries

- Do NOT perform atomic analysis directly in this skill
- Do NOT persist outputs of routed atomic skills; aggregate only; single artifact output
- Do NOT hide skipped steps; always disclose skip reason
- Do NOT route by trigger; use output-driven branching only
- Do NOT present recommendations without tying them to collected outputs
- Do produce explicit Recommended Next Tasks (prioritized, actionable, with owner and rationale)

### Skill Boundaries (Avoid Overlap)

**Do NOT do these (other skills handle them)**:

- Requirement diagnosis -> `analyze-requirements`
- Design alternatives and approval -> `design-solution`
- Drift typing and recalibration -> `align-planning`
- Architecture vs code compliance -> `align-architecture`
- Documentation gap scoring -> `assess-docs`
- Automated fix loops -> `run-repair-loop`
- Norms establishment -> `discover-docs-norms`
- Docs structure establishment -> `bootstrap-docs`

**When to stop and hand off**:

- Cycle report complete -> hand off actions to selected atomic skills
- Missing context prevents routing -> request minimal trigger clarification

---

## Self-Check

### Core Success Criteria (ALL must be met)

- [ ] Trigger recorded as metadata
- [ ] Phase 0.5 executed; short-circuit or proceed to Phase 1 with correct rationale
- [ ] Unified sequence executed when not short-circuited; output-driven follow-ups chosen with rationale
- [ ] Executed/skipped steps clearly listed
- [ ] Aggregated findings captured
- [ ] Cycle report persisted
- [ ] No atomic analysis performed directly

### Process Quality Checks

- [ ] Output-driven branching used for follow-ups
- [ ] User overrides honored
- [ ] Handovers contain explicit owners and next actions
- [ ] Report supports immediate next iteration

### Acceptance Test

**Can another operator continue the cycle using this report alone?**

If NO: refine sequence rationale and action clarity.

If YES: loop cycle output is complete.

---

## Examples

### Example 1: Task Complete with Weak Confidence

- Trigger: `task-complete` (metadata)
- Sequence: `align-planning` (full) -> `assess-docs`
- Output-driven: `assess-docs` executed because alignment confidence was medium
- Outcome: alignment partially valid; docs fill plan created

### Example 2: Milestone Closure with Architecture Compliance

- Trigger: `milestone-closed` (metadata)
- Sequence: `align-planning` (full) -> `assess-docs`
- Output-driven: `align-architecture` added because milestone context; `run-repair-loop` added because alignment reported active defects
- Outcome: planning aligned; architecture compliance gaps found; defects assigned for repair

### Example 3: Release Candidate Gate

- Trigger: `release-candidate` (metadata)
- Sequence: `align-planning` (full) -> `assess-docs`
- Output-driven: `align-architecture` added for release gate
- Outcome: release blocked by missing roadmap-to-backlog traceability; next actions assigned

### Example 4: Short-Circuit (Readiness Missing)

- Trigger: `task-complete` (metadata)
- Phase 0.5: assess-docs returns low readiness; gaps are content-only (structure exists, goals/requirements/roadmap empty)
- Short-circuit: Cycle report contains Minimal Fill Plan and Recommended Next Tasks; align-planning and Phase 1 skipped
- Outcome: User receives explicit next actions to fill docs before rerunning checkpoint

### Example 5: Phase 0.5 Bootstrap Then Proceed

- Trigger: `task-complete` (metadata)
- Phase 0.5: structure_missing detected; run bootstrap-docs (Initialize); re-run Phase 0.5
- Phase 0.5 (retry): assess-docs returns weak; proceed to Phase 1
- Phase 1: align-planning -> assess-docs; output-driven follow-ups as needed
