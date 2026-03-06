---
name: project-cognitive-loop
description: Orchestrate project governance cycles by routing between requirements analysis, design, execution alignment, and documentation readiness checks.
tags: [workflow, automation, eng-standards]
version: 1.0.0
license: MIT
related_skills: [analyze-requirements, brainstorm-design, execution-alignment, documentation-readiness, run-repair-loop]
recommended_scope: project
metadata:
  author: ai-cortex
input_schema:
  type: free-form
  description: Project stage context, trigger event, and optional governance scope
output_schema:
  type: diagnostic-report
  description: Cycle report with executed steps, skipped steps, rationale, and next-cycle recommendations
---

# Skill: Project Cognitive Loop (Orchestrator)

## Purpose

Run a repeatable governance loop for projects by orchestrating specialized skills across planning, execution, alignment, and documentation readiness.

---

## Core Objective

**Primary Goal**: Produce a cycle report that shows what governance checks were run, what was learned, what is blocked, and what to do next.

**Success Criteria** (ALL must be met):

1. ✅ **Trigger classified**: The initiating event is mapped to a governance scenario
2. ✅ **Right skills routed**: Atomic skills are selected and sequenced according to scenario
3. ✅ **Decisions explained**: Every executed or skipped step has rationale
4. ✅ **Cross-skill handoffs explicit**: Outputs and next owners are documented
5. ✅ **Cycle report delivered**: One aggregated report is produced and persisted
6. ✅ **No scope bleed**: The orchestrator does not perform atomic analysis itself

**Acceptance Test**: Can a team run the next iteration without asking which skill to use or in what order?

---

## Scope Boundaries

**This skill handles**:

- Scenario detection and orchestration
- Cross-skill sequencing and handoff control
- Aggregating outputs into a single governance view
- Recommending next cycle actions

**This skill does NOT handle**:

- Requirements analysis content itself (`analyze-requirements`)
- Design content itself (`brainstorm-design`)
- Alignment analysis itself (`execution-alignment`)
- Documentation gap analysis itself (`documentation-readiness`)
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

### Phase 0: Trigger Classification

Classify trigger into one of:

- `task-complete`
- `milestone-closed`
- `release-candidate`
- `scope-change`
- `periodic-review`

### Phase 1: Scenario Routing

Use default routing matrix:

| Trigger | Sequence |
| :--- | :--- |
| task-complete | `execution-alignment` -> `documentation-readiness` (if confidence < high) |
| milestone-closed | `execution-alignment (full)` -> `documentation-readiness` -> `run-repair-loop` (if defects are active) |
| release-candidate | `brainstorm-design` (if architecture conflict) -> `execution-alignment (full)` -> `documentation-readiness` |
| scope-change | `analyze-requirements` -> `brainstorm-design` -> `execution-alignment` |
| periodic-review | `documentation-readiness` -> `execution-alignment` |

User override always takes precedence.

### Phase 2: Execute and Collect

For each selected skill:

1. Record why it is selected
2. Run the skill's logic in-process (do not persist atomic skill outputs)
3. Capture key findings for aggregation
4. Record skipped skills and reason
5. Capture blockers and dependencies

**Single artifact rule**: This orchestrator produces exactly one output file. Do NOT write separate reports for `documentation-readiness`, `execution-alignment`, or other routed skills. All findings are aggregated into the cycle report.

### Phase 3: Aggregate Governance Report

Report must include:

- Trigger and scenario
- Sequence executed vs skipped
- Key findings by skill (inline summary; no cross-references to separate files)
- Blockers and confidence level
- **Recommended Next Tasks** — explicit, prioritized, actionable tasks (owner, scope, and rationale)

### Phase 4: Persist

Write exactly one file to:

- Default: `docs/calibration/YYYY-MM-DD-cognitive-loop.md`
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
- From analyze-requirements:
- From brainstorm-design:
- From execution-alignment:
- From documentation-readiness:

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
- Do NOT route more than necessary for the trigger (avoid orchestration inflation)
- Do NOT present recommendations without tying them to collected outputs
- Do produce explicit Recommended Next Tasks (prioritized, actionable, with owner and rationale)

### Skill Boundaries (Avoid Overlap)

**Do NOT do these (other skills handle them)**:

- Requirement diagnosis -> `analyze-requirements`
- Design alternatives and approval -> `brainstorm-design`
- Drift typing and recalibration -> `execution-alignment`
- Documentation gap scoring -> `documentation-readiness`
- Automated fix loops -> `run-repair-loop`

**When to stop and hand off**:

- Cycle report complete -> hand off actions to selected atomic skills
- Missing context prevents routing -> request minimal trigger clarification

---

## Self-Check

### Core Success Criteria (ALL must be met)

- [ ] Trigger mapped to scenario
- [ ] Skill sequence chosen with rationale
- [ ] Executed/skipped steps clearly listed
- [ ] Aggregated findings captured
- [ ] Cycle report persisted
- [ ] No atomic analysis performed directly

### Process Quality Checks

- [ ] Routing remains minimal for trigger type
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

- Trigger: `task-complete`
- Route: `execution-alignment` -> `documentation-readiness`
- Outcome: alignment partially valid; missing architecture evidence; docs fill plan created

### Example 2: Scope Change Mid-Iteration

- Trigger: `scope-change`
- Route: `analyze-requirements` -> `brainstorm-design` -> `execution-alignment`
- Outcome: requirements updated, design adjusted, priorities recalibrated

### Example 3: Release Candidate Gate

- Trigger: `release-candidate`
- Route: `execution-alignment (full)` -> `documentation-readiness`
- Outcome: release blocked by missing roadmap-to-backlog traceability; next actions assigned
