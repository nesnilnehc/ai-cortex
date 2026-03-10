---
name: align-execution
description: Perform post-task traceback, drift detection, and top-down recalibration to keep execution aligned with goals, requirements, architecture, milestones, and roadmap.
tags: [workflow, eng-standards, documentation]
version: 1.0.0
license: MIT
related_skills: [analyze-requirements, brainstorm-design, bootstrap-project-documentation, assess-documentation-readiness, run-repair-loop]
recommended_scope: both
metadata:
  author: ai-cortex
  evolution:
    sources:
      - name: "analyze-requirements"
        repo: "nesnilnehc/ai-cortex"
        version: "1.0.0"
        license: "MIT"
        type: "reference"
        borrowed: "State-based validation style, handoff boundaries, structured self-check"
      - name: "brainstorm-design"
        repo: "nesnilnehc/ai-cortex"
        version: "1.0.0"
        license: "MIT"
        type: "reference"
        borrowed: "Phase-based process, alternatives framing, output artifact discipline"
    enhancements:
      - "Added deterministic mode selection (Lightweight vs Full)"
      - "Added five-type drift model with impact and root cause format"
      - "Added mapping-confirmation gate when traceability links are missing"
triggers: [alignment, execution alignment, post task]
input_schema:
  type: free-form
  description: Completed task context, optional project docs root, optional mode and path mapping
  defaults:
    mode: lightweight
output_schema:
  type: document-artifact
  description: Execution Alignment Report written to docs/calibration/YYYY-MM-DD-task-slug-calibration.md
---

# Skill: Execution Alignment

## Purpose

Keep project execution aligned with higher-level planning by running a post-task alignment loop: traceback from completed work to strategy, detect drift, and produce top-down recalibration recommendations.

---

## Core Objective

**Primary Goal**: Produce an actionable Execution Alignment Report after task completion, with clear drift classification and prioritized recalibration actions.

**Success Criteria** (ALL must be met):

1. ✅ **Traceback completed**: The completed task is traced through applicable project layers for the selected mode
2. ✅ **Drift classified**: All detected misalignments use the drift model (goal, requirement, architecture, roadmap, priority), with impact scope and root cause per item
3. ✅ **Calibration produced**: A top-down recalibration recommendation list is provided, including next tasks
4. ✅ **Report persisted**: Execution Alignment Report is written to the agreed path
5. ✅ **Evidence readiness assessed**: Missing or weak documentation is explicitly scored and reflected in confidence
6. ✅ **Unsafe writes avoided**: If mapping is uncertain or updates are destructive, user confirmation is requested before proposing file-level changes

**Acceptance Test**: Can a teammate read the report and immediately understand whether execution is still aligned, what drift exists, what to do next, and why?

---

## Scope Boundaries

**This skill handles**:

- Post-task alignment assessment
- Bottom-up traceback across project layers
- Drift detection, impact analysis, and root cause labeling
- Top-down recalibration suggestions
- Next-task recommendations with priority hints
- Evidence readiness assessment and graceful degradation when planning documents are incomplete

**This skill does NOT handle**:

- Rewriting requirements from scratch (use `analyze-requirements`)
- Redesigning architecture (use `brainstorm-design`)
- Creating a new roadmap or milestone system from scratch
- Implementing code changes
- Team retrospective facilitation ("what went well / poorly")

**Handoff point**: After the report is produced and reviewed, hand off to the relevant skill by issue type (requirements, architecture, planning, or repair loop).

---

## Use Cases

- **Post-task checkpoint**: Validate alignment after any completed ticket
- **Milestone closure review**: Run full alignment before marking a milestone complete
- **Release readiness**: Detect planning drift before a release cut
- **Scope-shift diagnosis**: Investigate whether recent work still supports current goals
- **Backlog reprioritization input**: Generate evidence-backed next-task ordering signals

---

## Behavior

### Agent Prompt Contract

At execution start, follow this instruction contract:

```text
You are responsible for project execution alignment.

When a task is completed, perform traceback analysis to ensure alignment
with project layers and produce a structured Execution Alignment Report.
```

### Interaction Policy

- **Defaults**: Mode from context (`lightweight` unless release/milestone/epic); docs root from workspace
- **Choice options**: Mode override `[lightweight][full]` when user prefers
- **Confirm**: Before file-level change proposals; before proceeding when mapping is uncertain (NeedsMappingConfirmation)

### Phase 0: Mode and Context Resolution

1. Resolve mode with deterministic policy:
   - If user explicitly sets mode, use it
   - Else if context contains `release`, `milestone-closed`, or `epic-done`, use **Full Alignment Mode**
   - Else use **Lightweight Mode**
2. Resolve document paths:
   - Default mapping assumes project-documentation-template layout
   - Apply user path mapping overrides when provided
3. Confirm minimum context:
   - Completed task summary
   - At least one traceability anchor (requirement ID, roadmap item, milestone reference, or equivalent)

### Phase 0.5: Evidence Readiness Assessment

Assess evidence quality before traceback:

- **strong**: canonical docs exist for all required layers in selected mode
- **weak**: partial docs exist, but at least one required layer depends on secondary evidence (issues/PR/commit notes)
- **missing**: critical layers unavailable; traceback cannot produce reliable drift typing

Rules:

1. Missing docs must not silently pass as aligned.
2. Use secondary evidence only when canonical docs are missing, and label it explicitly.
3. Confidence in conclusions must be adjusted by readiness level:
   - `strong` -> high confidence
   - `weak` -> medium confidence
   - `missing` -> low confidence or blocked

### Mode Definitions

- **Lightweight Mode**: Task Backlog → Roadmap → Requirements
- **Full Alignment Mode**: Task Backlog → Roadmap → Milestones → Architecture → Requirements → Project Goals

### Phase 1: Traceback (Bottom-Up)

1. Identify completed task intent, output, and target outcome
2. Walk upward through selected layers and record per-layer alignment status:
   - `aligned` | `partial` | `misaligned` | `unknown`
3. Capture supporting evidence for each status
4. If critical mapping is missing, enter `NeedsMappingConfirmation`:
   - List missing links
   - Offer 1-3 candidate mappings with rationale
   - Request user confirmation before continuing
   - If unresolved, output blocked report with required minimum inputs
5. If readiness is `weak` or `missing`, annotate per-layer evidence source:
   - `canonical` (project docs)
   - `secondary` (issue/PR/commit context)
   - `none`

### Phase 2: Drift Detection

Classify each drift item as:

- **Goal Drift**: Work no longer supports current project objective
- **Requirement Drift**: Requirement changed, deprecated, or already superseded
- **Architecture Drift**: Implementation direction diverges from current architecture decisions
- **Roadmap Drift**: Sequencing or roadmap assumptions changed
- **Priority Drift**: Priority is stale relative to current business direction

For each item, output:

- `Type`
- `Impact Scope`
- `Root Cause`
- `Severity` (`low` | `medium` | `high`)

### Phase 3: Calibration (Top-Down)

1. Re-derive priority from top layers downward (Goals → Requirements → Architecture → Milestones → Roadmap → Backlog)
2. Produce recalibration actions:
   - Priority adjustments
   - Sequence changes
   - Dependency corrections
   - Follow-up analysis handoffs
3. Recommend next tasks with rationale and urgency window
4. If suggesting edits to canonical planning docs, request explicit confirmation before generating file-level change proposals

### Phase 4: Persist Report

Write report to:

- Default: `docs/calibration/YYYY-MM-DD-task-slug-calibration.md`
- Or user-specified path

Report must include a machine-readable drift block (YAML or JSON) in addition to human-readable sections.
Report must also include an evidence readiness block and explicit confidence level.

---

## Input & Output

### Input

- Completed task description and outcome
- Optional mode override (`lightweight` | `full`)
- Optional document root/path mapping
- Optional context: release/milestone/epic markers

### Output

#### Execution Alignment Report Template

```markdown
# Execution Alignment Report: <task title>

**Date:** YYYY-MM-DD
**Mode:** Lightweight | Full
**Status:** aligned | partial | misaligned | blocked
**Confidence:** high | medium | low

## Completed Task
- Summary:
- Outcome:

## Traceback Path
Task Backlog -> Roadmap -> Milestones -> Architecture -> Requirements -> Project Goals

## Evidence Readiness
- Readiness: strong | weak | missing
- Missing Layers:
- Secondary Sources Used:

## Alignment Status
- Goal Alignment:
- Requirement Alignment:
- Architecture Alignment:
- Milestone Alignment:
- Roadmap Alignment:

## Drift Detected
- Type:
  Impact Scope:
  Root Cause:
  Severity:

## Impact Analysis
- Delivery impact:
- Technical impact:
- Planning impact:

## Calibration Suggestions
1.
2.
3.

## Recommended Next Tasks
1.
2.
3.

## Machine-Readable Drift

    drifts:
      - driftType: "Architecture Drift"
        severity: "high"
        owner: "platform-team"
        dueWindow: "this-sprint"
        impactScope: "API gateway auth path"
        rootCause: "Service mesh ADR replaced gateway-centric pattern"
    evidence:
      readiness: "weak"
      confidence: "medium"
      missingLayers:
        - "architecture/adrs/latest-decision.md"
      secondarySources:
        - "PR#142"
        - "commit:abc1234"

```

---

## Restrictions

### Hard Boundaries

- Do NOT invent traceability links when evidence is missing
- Do NOT claim high confidence when readiness is `weak` or `missing`
- Do NOT silently modify planning truth sources (goals, requirements, architecture, roadmap) without explicit user approval
- Do NOT collapse drift categories into a generic "misalignment" bucket; keep typed drift outputs
- Do NOT skip layer checks in Full mode unless the layer is truly unavailable (mark as `unknown` and explain)
- Do NOT present recommendations without rationale tied to traceback evidence

### Skill Boundaries (Avoid Overlap)

**Do NOT do these (other skills handle them)**:

- Requirements redefinition workflow → `analyze-requirements`
- Architecture option design workflow → `brainstorm-design`
- Repo-level onboarding workflow → `onboard-repo`
- Automated test-and-fix loop execution → `run-repair-loop`

**When to stop and hand off**:

- Requirements are invalid or contradictory → hand off to `analyze-requirements`
- Architecture conflict is primary blocker → hand off to `brainstorm-design`
- Report indicates active implementation defects requiring repair → suggest `run-repair-loop`

---

## Self-Check

### Core Success Criteria (ALL must be met)

- [ ] Traceback completed for selected mode
- [ ] Drift items typed using the five-category model
- [ ] Each drift has impact scope and root cause
- [ ] Top-down calibration actions provided
- [ ] Report persisted to agreed path
- [ ] Evidence readiness level and confidence are explicitly reported
- [ ] Confirmation requested where mapping or write safety is uncertain

### Process Quality Checks

- [ ] Mode selection followed deterministic policy
- [ ] Mapping uncertainty triggered `NeedsMappingConfirmation`
- [ ] Canonical vs secondary evidence is clearly separated
- [ ] Evidence references are present for each alignment status
- [ ] Recommendations are prioritized and time-bounded
- [ ] Handoffs to adjacent skills are explicit when needed

### Acceptance Test

**Can a teammate execute the top 1-3 recommendations without additional clarification and explain why they are highest priority?**

If NO: report is incomplete; refine traceback evidence and recalibration details.

If YES: report is complete; proceed to handoff or execution planning.

---

## Examples

### Example 1: Lightweight Mode (Routine Task)

**Context**: Completed task updates search filter UI behavior.

**Mode resolution**: No explicit override, no release/milestone/epic marker → Lightweight.

**Traceback**:

- Task aligns with roadmap item `search-improvements-q2`
- Requirement still valid, but acceptance criteria changed last week
- Evidence readiness is `strong` because requirement and roadmap docs are both canonical and current

**Drift**:

- `Requirement Drift` (medium): Requirement wording changed to include keyboard navigation; completed task only covers click interactions

**Calibration**:

1. Add follow-up task for keyboard navigation
2. Move accessibility acceptance check before merging related UI tasks
3. Reorder backlog items to unblock regression testing

### Example 2: Full Mode (Milestone Closure)

**Context**: Milestone tagged `milestone-closed` after API gateway auth rollout.

**Mode resolution**: Marker hit → Full.

**Traceback**:

- Roadmap and milestone mapping valid
- Architecture layer conflicts with latest service mesh ADR
- Goal and requirements still valid
- Evidence readiness is `weak`; architecture context depends on a merged PR note pending ADR update

**Drift**:

- `Architecture Drift` (high): Gateway auth path no longer matches platform direction
- `Priority Drift` (high): Migration work was not promoted in backlog

**Calibration**:

1. Insert migration epic into current sprint planning
2. Defer non-critical gateway enhancements
3. Trigger architecture-focused follow-up using `brainstorm-design`

### Example 3: Edge Case (Blocked Mapping)

**Context**: Completed task has no requirement ID or roadmap link.

**Behavior**:

1. Enter `NeedsMappingConfirmation`
2. Present candidate mappings with confidence notes
3. Ask user to confirm mapping before drift classification

**Result**:

- If user confirms: continue normal flow
- If not confirmed: output `blocked` report with missing fields checklist
- Confidence remains `low` until canonical mappings are established
