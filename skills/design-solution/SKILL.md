---
name: design-solution
description: Produce a validated design document from requirements (architecture, components, data flow, trade-offs) with no implementation. Use when requirements are clear and you need a single source of truth for downstream task breakdown.
tags: [writing, eng-standards, documentation]
version: 1.1.0
license: MIT
related_skills: [analyze-requirements, breakdown-tasks]
recommended_scope: both
metadata:
  author: ai-cortex
  evolution:
    sources:
      - name: "design-solution"
        repo: "nesnilnehc/ai-cortex"
        version: "1.0.0"
        license: "MIT"
        type: "reference"
        borrowed: "Phase-based validation, HARD-GATE, trade-off framework, design doc structure"
    enhancements:
      - "Explicit input: requirements document (from analyze-requirements)"
      - "Output contract: design as single source of truth for breakdown-tasks"
      - "Strict no-implementation boundary"
triggers: [design solution, design from requirements, design doc]
input_schema:
  type: document-artifact + optional free-form
  description: Validated requirements document (e.g. requirements.md or docs/requirements-planning/<topic>.md); optional project context
output_schema:
  type: document-artifact
  description: Design document per [spec/artifact-contract.md](../../spec/artifact-contract.md)
  artifact_type: design
  path_pattern: docs/designs/YYYY-MM-DD-{topic}.md
  lifecycle: snapshot
---

# Skill: Design Solution

## Purpose

Turn validated requirements into a single, implementation-free design document. The design describes architecture, components, data flow, and trade-offs so that downstream skills (e.g. `breakdown-tasks`) can derive an executable task list without ambiguity.

---

## Core Objective

**Primary Goal**: Produce a validated design document from requirements that serves as the single source of truth for implementation planning; no code or implementation steps are produced.

**Success Criteria** (ALL must be met):

1. ✅ **Design document exists**: Written to `docs/designs/YYYY-MM-DD-<topic>.md` (or project-convention path per `docs/ARTIFACT_NORMS.md`) and committed
2. ✅ **User explicitly approved**: User said "approved", "looks good", "proceed", or equivalent
3. ✅ **Requirements traceability**: Design explicitly references or summarizes the requirements it satisfies
4. ✅ **Alternatives documented**: At least 2–3 approaches considered with trade-offs (pros/cons/best-for)
5. ✅ **Error handling strategy**: Key failure paths and how the design handles them are documented
6. ✅ **Testing strategy**: How the design will be verified against requirements is documented (test approach, not test code)
7. ✅ **No implementation**: Zero code, scaffolding, or implementation tasks; design only
8. ✅ **Downstream-ready**: A reader can break the design into tasks with dependencies and acceptance criteria

**Acceptance Test**: Can someone use this design document alone to produce a complete, ordered task list (e.g. via `breakdown-tasks`) without asking clarifying questions?

---

## Scope Boundaries

**This skill handles**:

- Requirements document → Design document (architecture, components, data flow, interfaces)
- Trade-off analysis and alternative approaches
- Design approval and persistence as single source of truth for implementation planning

**This skill does NOT handle**:

- Eliciting or validating requirements (use `analyze-requirements`)
- Turning design into task list (use `breakdown-tasks`)
- Writing code or implementation (any implementation skill)
- Rough-idea-to-design without a requirements doc (use this skill with rough idea as input)

**Handoff point**: When design is approved and persisted, hand off to `breakdown-tasks` to produce tasks.md (or equivalent).

---

## Use Cases

- **Post-requirements design**: You have a validated requirements document and need a detailed design before implementation.
- **Architecture from requirements**: Requirements are clear; you need component boundaries, data flow, and technology trade-offs.
- **Single source of truth**: You want one design doc that implementation and task breakdown can rely on.

---

## Behavior

### Interaction Policy

- **Defaults**: Require a requirements artifact (path or content); use project norms for design path if present
- **Choice options**: One question at a time when clarifying; offer `[A][B][C]` for design choices where useful
- **Confirm**: User must approve design before handoff; no implementation before approval

### HARD-GATE: No Implementation

```text
DO NOT write code, scaffold projects, or produce implementation steps.
Output is design documentation only. Implementation is downstream (e.g. breakdown-tasks then execution).
```

### Phase 1: Ingest Requirements

1. **Load requirements**: Read the requirements document (e.g. requirements.md or docs/requirements-planning/*.md).
2. **Confirm scope**: Briefly confirm with user that this requirements doc is the scope for this design (or agree on subset).
3. **Identify constraints**: Extract constraints, acceptance criteria, and out-of-scope items from requirements.

### Phase 2: Explore Alternatives and Trade-offs

1. **Propose 2–3 approaches**: Architecture/component/data-flow options that satisfy the requirements.
2. **Document trade-offs**: For each option: pros, cons, "best for".
3. **Recommend one**: State recommended approach and rationale; invite user to choose or adjust.

### Phase 3: Produce Design Document

1. **Structure**: Goal, architecture, components, data flow, error handling strategy (key failure paths), testing strategy (verification approach, not test code), trade-offs considered, acceptance criteria (traceable to requirements).
2. **Scale to complexity**: Short for simple scope; more detail when needed so that task breakdown is unambiguous.
3. **Resolve path**: Check `docs/ARTIFACT_NORMS.md` first (project override); default fallback is `docs/designs/YYYY-MM-DD-<topic>.md` per [spec/artifact-contract.md](../../spec/artifact-contract.md).
4. **Write and persist**: Save design with front-matter (`artifact_type: design`, `created_by: design-solution`, `lifecycle: snapshot`, `created_at`).

### Phase 4: Approve and Hand Off

1. **User approval**: Obtain explicit approval before declaring done.
2. **Handoff**: Suggest `breakdown-tasks` with this design as input to produce tasks.md.

---

## Input & Output

| Role | Content |
| :--- | :--- |
| **Input** | Requirements document (path or content); optional project context, existing design or ADRs |
| **Output** | Design document at `docs/designs/YYYY-MM-DD-<topic>.md` (or project path per `docs/ARTIFACT_NORMS.md`); single source of truth for implementation and task breakdown |

---

## Restrictions

### Hard Boundaries

- **No implementation**: Do not generate code, file layouts, or step-by-step implementation instructions.
- **Requirements first**: Do not run this skill when requirements are vague or missing; hand off to `analyze-requirements` first.
- **Design only**: Do not produce task lists; hand off to `breakdown-tasks` for that.

### Skill Boundaries (Avoid Overlap)

**Do NOT do these (other skills handle them)**:

- Requirements elicitation or validation → `analyze-requirements`
- Task breakdown or planning → `breakdown-tasks`
- Code implementation or refactoring → implementation skills

---

## Self-Check

- [ ] Design document exists at `docs/designs/YYYY-MM-DD-<topic>.md` (or project path per `docs/ARTIFACT_NORMS.md`) and is committed
- [ ] User explicitly approved the design
- [ ] Requirements are referenced or summarized; traceability is clear
- [ ] At least 2–3 alternatives with trade-offs are documented
- [ ] Error handling strategy documented: key failure paths and handling approach present
- [ ] Testing strategy documented: how design is verified against requirements described (approach, not test code)
- [ ] No code or implementation steps in the output
- [ ] A reader could produce a task list from this design without further clarification

---

## Examples

### Example 1: Standard design from validated requirements

**Invocation**: "We have requirements in docs/requirements-planning/core-v1.md. Produce a design doc for it."

**Agent**: Uses design-solution; reads requirements; proposes 2–3 architectural options with trade-offs; writes design to docs/designs/YYYY-MM-DD-core-v1.md; gets user approval; suggests running breakdown-tasks on that design to get tasks.md.

### Example 2: Edge case — very small scope

**Invocation**: "Requirements for a tiny CLI tool are captured in docs/requirements-planning/one-off-migration.md. Do we still need a full design doc?"

**Agent**:

- Confirms that requirements are validated but scope is small.
- Produces a concise design doc that still covers architecture, data flow, and constraints, but keeps sections short and focused.
- Explicitly documents why a lightweight design is sufficient and marks the document as the single source of truth for later regression or repeat runs.
- Gets user approval, then recommends `breakdown-tasks` if implementation will be shared or repeated.
