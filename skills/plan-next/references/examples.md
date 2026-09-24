# plan-next: worked examples

## Examples

### Example 1: a half-built strategy (the normal path)

**Scenario**: the project has mission / vision; no strategic-goals; a roadmap exists but cannot be traced back to a strategic goal.

**Output** (example):

#### Next-step suggestions

> **Situation**: mission and vision exist, the strategic-goals document is missing
> **Core tension**: roadmap nodes exist but trace back to no goal, so the governance traversal cannot start

---

##### Do now

**1. Add the strategic-goals document** · `important`

> Fill in the missing strategic-goals file, so the roadmap nodes have a traceable source.

- Governance context:
  - Strategic goal: missing (mission and vision already exist)
  - Current KPI: data missing (no strategic goal established, so no acceptance criteria)
  - Roadmap: exists, but its nodes trace back to no goal
  - Current position: the strategic goal is missing, traversal stops
- Recommended skill: `/design-strategic-goals generate strategic-goals.md from mission.md and vision.md, with identifiable goal items`
- Evidence: `docs/project-overview/strategic-goals.md` is missing
- Completion marker: strategic-goals.md is written and holds identifiable goal items; return to plan-next for re-evaluation if blocked

##### Diagnostic basis

- **Project situation**: mission and vision exist but there is no strategic goal; roadmap alignment is yet to be established

**Decision logic**:

| Level | Node | Status | Inference |
| --- | --- | --- | --- |
| Strategic goal | strategic-goals.md | missing | L1 gap, traversal stops; route design-strategic-goals |
| Roadmap | — | not evaluated | re-run once L1 is ready |

- **Drift sweep result**: none
- **Hygiene sweep result**: none

### Example 2: a new project with an explicit global documentation prerequisite

**Scenario**: a new project explicitly declares that all governance artifacts must follow its artifact norms, but the norms are absent and no alternate path map or linked governance artifacts exist. `specs/` is also absent, but that absence is not itself the prerequisite.

**Output** (example):

#### Next-step suggestions

> **Situation**: a new project, the documentation norms file is missing
> **Core tension**: the project makes its artifact norms a prerequisite, and no existing evidence can safely resolve governance targets before that convention is recorded
> **Decision state**: `actionable`

---

##### Do now

**1. Establish the documentation norms foundation** · `urgent`

> Establish the documentation norms first, so every governance file that follows has a standard to work from.

- Governance context:
  - Strategic goal: not yet established
  - Current KPI: data missing (the governance norms are not established)
  - Roadmap: not yet evaluated (re-run once the norms file is ready)
  - Current position: the declared global documentation prerequisite is missing
- Recommended skill: `/define-docs-norms generate docs/ARTIFACT_NORMS.md from the project structure`
- Evidence: project configuration requires artifact norms; the declared norms file is missing and no alternative path map exists
- Completion marker: the project records its artifact conventions; re-run plan-next to resolve any remaining independent foundation work

##### Diagnostic basis

- **Project situation**: a project-declared global prerequisite is missing; the route was scoped globally by that declaration, not by a default path heuristic

**Decision logic**:

| Level | Node | Status | Inference |
| --- | --- | --- | --- |
| Norms layer | ARTIFACT_NORMS.md | missing | candidate to establish local conventions; no global stop is inferred from the path alone |
| Strategic goal | project-declared target | not evaluated | target selection depends on the explicit project-wide artifact-norms prerequisite; re-run after it is satisfied |

- **Drift sweep result**: none
- **Hygiene sweep result**: none

### Example 3: sibling advance + parallelism decision

**Scenario**: goal A, roadmap node N1 (in-progress). Under N1 are requirement R1 (in-progress, inferred from children) and requirement R2 (pending). Under R1 are design D1a (done) and D1b (in-progress). No tasks have been broken out under D1b yet.

**Traversal path**: N1 → R1 (in-progress, inferred) → sibling scan: D1a done, D1b in-progress → enter D1b → no tasks (an L5 gap) → emit a "tasks to be broken down" awaiting-execution card (task breakdown is carried by the AgentFabric runtime).

**Parallelism verdict**: D1b is the only in-progress design, R2 is pending. Suggestion: **focus** on D1b; once it finishes, R2 becomes the next focus automatically.

**Output** (example):

#### Next-step suggestions

> **Situation**: goal A is in progress, design D1b is ready for task breakdown
> **Core tension**: D1a is finished and D1b has no tasks, so the execution layer cannot move

---

##### Do now

**1. Break design D1b into executable tasks** · `defer`

> The D1b design is ready; once tasks are broken out, D1b can move into execution.

- Governance context:
  - Strategic goal: goal A (in progress)
  - Current KPI: data missing (goal A has no quantified acceptance criteria)
  - Roadmap: roadmap node N1 (in progress)
  - Current position: design D1b is ready, the task layer has a gap
- Recommended skill: (no governance skill; task breakdown is carried by the AgentFabric runtime, at the same granularity as designs D1b and D1a)
- Evidence: the D1b design file exists, the task file is missing; D1a finishing triggers the advance
- Completion marker: the D1b task list is created and holds at least one task record

##### Diagnostic basis

- **Project situation**: goal A is in the execution stage, N1→R1→D1b, with a gap at the task layer

**Decision logic**:

| Level | Node | Status | Inference |
| --- | --- | --- | --- |
| Strategic goal | goal A | in-progress | keep drilling down |
| Roadmap | N1 | in-progress | focus (the only in-progress node) |
| Requirement | R1 | in-progress (inferred: D1b in-progress) | keep drilling down |
| Design | D1a | done | D1a done triggers the sibling advance |
| Design | D1b | in-progress | no tasks (G1), emit a "tasks to be broken down" awaiting-execution card |

- **Drift sweep result**: none
- **Hygiene sweep result**: none

### Example 4: the roadmap is not tiered

**Scenario**: strategic goals exist; a roadmap exists but its nodes have no Now/Next/Later tiers — it is only a flat list.

**Output** (example):

#### Next-step suggestions

> **Situation**: strategic goals exist, the roadmap is a flat list of nodes
> **Core tension**: with no Now/Next/Later tiers, the current execution focus cannot be determined

---

##### Do now

**1. Give the roadmap current/next/long-term tiers** · `important`

> Once tiered, the current focus node can be pinned down and the levels below it can be evaluated.

- Governance context:
  - Strategic goal: exists
  - Current KPI: data missing (the roadmap cannot be evaluated before it is tiered)
  - Roadmap: exists, but has no Now/Next/Later tiers
  - Current position: the roadmap layer, missing its priority tiers
- Recommended skill: `/promote-roadmap-items tier the nodes in roadmap.md by Now/Next/Later priority`
- Evidence: `docs/requirements-planning/roadmap.md` exists but has no tier structure
- Completion marker: re-run plan-next once the roadmap carries Now/Next/Later tiers

##### Diagnostic basis

- **Project situation**: the roadmap exists but is not tiered; traversal stops at L2

**Decision logic**:

| Level | Node | Status | Inference |
| --- | --- | --- | --- |
| Strategic goal | strategic-goals.md | present | keep drilling down |
| Roadmap | roadmap.md | not tiered (a flat list) | the untiered-roadmap rule fires, route promote-roadmap-items, do not evaluate downstream |

- **Drift sweep result**: none
- **Hygiene sweep result**: none

### Example 5: blocked triggers parallelism

**Scenario**: goal A, roadmap node N1. Under N1 are requirement R1 (blocked, waiting on an external dependency) and R2 (pending, with no depends_on link to R1).

**Parallelism verdict**: R1 blocked, R2 pending and independent → **parallel**: suggest starting R2 alongside it.

**Output** (example):

#### Next-step suggestions

> **Situation**: goal A is in progress; under N1, R1 is blocked by an external dependency
> **Core tension**: waiting for R1 to unblock wastes the window, and R2 is independent and safe to advance in parallel

---

##### Do now

**1. Start the solution design for requirement R2** · `defer`

> Advance R2 in parallel while R1 is blocked, so the wait is not wasted.

- Governance context:
  - Strategic goal: goal A (in progress)
  - Current KPI: data missing (goal A has no quantified acceptance criteria)
  - Roadmap: roadmap node N1 (in progress)
  - Current position: the design layer, R1 being blocked triggers parallelism
- Recommended skill: (no governance skill; the R2 design workflow is carried by the AgentFabric runtime, advanced in parallel while R1 is blocked)
- Evidence: R1 is blocked by an external dependency; R2 has no `depends_on` link
- Completion marker: the R2 design file is created; return to plan-next for re-evaluation if blocked (R2 turns out to be implicitly coupled to R1)

##### Diagnostic basis

- **Project situation**: goal A, with R1 blocked and R2 pending under N1

**Decision logic**:

| Level | Node | Status | Inference |
| --- | --- | --- | --- |
| Strategic goal | goal A | in-progress | keep drilling down |
| Roadmap | N1 | in-progress | focus |
| Requirement | R1 | blocked | blocked by an external dependency, triggers the parallelism decision |
| Requirement | R2 | pending | no depends_on link, safe to start in parallel |

- **Blocked nodes**: R1 (waiting on an external dependency, a human is needed to clear it)
- **Drift sweep result**: none
- **Hygiene sweep result**: none

---

### Example 6: a strategic goal with status=approved whose acceptance is not met (the easiest misjudgment)

**Scenario**: in `strategic-goals.md`, goal G1 has frontmatter `status: approved`, its acceptance criterion is "citation visibility ≥ 80% across two consecutive iterations", and there is no monitoring data. Under stage M5 (the milestone carrying G1) all 17 tasks are `pending`, the task breakdown is complete, and the designs/ADRs are in place.

**Key verdicts**:

- L1: G1 `status=approved` counts as `in-progress`; the acceptance KPI "citation visibility" has no data → the first route must establish the KPI data source
- L5: all tasks pending triggers the "awaiting execution" branch; the second route emits an "awaiting execution" card marking the focus task

**Output** (example):

#### Next-step suggestions

> **Situation**: G1's acceptance is not met, citation visibility has no monitoring; every M5 task is waiting to start
> **Core tension**: the KPI data source is missing so acceptance cannot be verified; the tasks are governance-ready but waiting on development

---

##### Do now

**1. Establish the acceptance-KPI data source for G1 (requirement clarification running reliably)** · `urgent`

> Establish citation-visibility monitoring, so it becomes possible to judge whether G1's acceptance is met.

- Governance context:
  - Strategic goal: G1, requirement clarification depends on the knowledge base running reliably
  - Current KPI: citation visibility (the share of user documents recalled) data source missing / target ≥80% / project-defined (no external benchmark)
  - Roadmap: M5 (hybrid-retrieval maturity milestone, in progress)
  - Current position: strategic goal acceptance, the KPI data source is not established
- Recommended skill: (no governance skill; citation-visibility instrumentation + the design of the monitoring query path is carried by the AgentFabric runtime, landing in docs/architecture/)
- Evidence: the acceptance field of `strategic-goals.md` names a KPI but points at no data source
- Completion marker: citation visibility can be read from a monitoring or query interface; the data source pointer is written into strategic-goals.md

---

**2. Start T47 (BM25 sparse retrieval integration)** · `awaiting execution`

> The task is governance-ready and waiting on a developer; T47 is the key dependency for raising citation visibility.

- Governance context:
  - Strategic goal: G1, requirement clarification depends on the knowledge base running reliably
  - Current KPI: citation visibility data source missing / target ≥80%
  - Roadmap: M5 (hybrid-retrieval maturity milestone, in progress)
  - Current position: the task layer, everything waiting to start (governance-ready, waiting on development)
- Recommended skill: (no governance skill; hand to the development team to implement T47 per m5/tasks.md)
- Evidence: M4 T31 (QueryRouter) is finished; T47 has not started and has no blocking predecessor
- Completion marker: T47 passes acceptance (BM25 recall ≥15% above pure vector search, hybrid retrieval P95 ≤1.5s); return to plan-next for re-evaluation once done

##### Diagnostic basis

- **Project situation**: G1 status=approved (design complete), acceptance not met, KPI data source missing; M5 in progress, tasks all pending

**Decision logic**:

| Level | Node | Status | Inference |
| --- | --- | --- | --- |
| Strategic goal | G1 | approved (counts as in-progress) | status=approved ≠ done; the KPI data source is missing → the first route establishes the data source |
| Roadmap | M5 | in-progress | the only focus milestone, keep drilling down |
| Requirement | M5 requirement set | in-progress | designs/ADRs are ready, drill down to the task layer |
| Design | ADR-033/034 | done | no task gap |
| Task | T47 (17 in total, all-pending) | all-pending | the "awaiting execution" branch, emit the focus task card (label: awaiting execution) |

- **Drift sweep result**: none
- **Hygiene sweep result**: none

### Example 7: skip an initially suggested but unsubstantiated route (Wright situation)

**Scenario**: an earlier `plan-next` result recommends creating a general `specs/` directory because that conventional path is absent. Wright already has its own requirements, designs, and integration-contract directories, and its artifact norms document exists. The user says: “skip the first suggestion for this conversation and continue.”

**Required handling**:

1. Resolve “first suggestion” against the latest displayed list. “For this conversation” explicitly selects the session scope, so do not write `.ai-cortex/plan-next.yaml`.
2. Revalidate the route against current project evidence before recording the session skip. The stated reason for creating general norms is contradicted by the existing norms document; absence of `specs/` alone does not establish a gap. Do not store a stale route key as a skip; explain that the route did not survive revalidation and leave it out of this fresh result.
3. Re-run candidate diagnosis using the project's own declared conventions and linked artifacts. Keep dependencies and genuine prerequisites intact; surface independent eligible work, or state `needs_input` if a specific mapping cannot be established.
4. Report that the suggestion was set aside for this conversation, explain why it did not survive revalidation, and give the next applicable recommendation. Do not modify tasks, roadmap, norms, or other governance documents.

This example uses Wright only to demonstrate revalidation and session-scoped skipping. Its directory structure is project evidence, not an AI Cortex convention.

**Output** (example):

> **Decision state**: `actionable`
>
> **Skipped recommendation**: establish a general `specs/` directory — omitted from this fresh result at your request. No session key was stored because revalidation found that the route itself is not applicable: the project has an artifact norms document and uses its own linked requirements, designs, and integration contracts. Absence of `specs/` alone is not a gap.
>
> **Do now**: [the highest-priority independent eligible action supported by the fresh scan]. Its prerequisites and dependencies were checked normally; no governance state was changed.
>
> **Diagnostic basis**: the former directory-based recommendation was not retained as an unfinished prerequisite. Wright's local directory names are project evidence only, not portable rules.

- **Drift sweep result**: none
- **Hygiene sweep result**: none

### Example 8: skip one independent action, then restore it

**Scenario**: the latest result shows two independently startable tasks, “Prepare the coverage dashboard” and “Add the audit log”. The user says “skip the dashboard for this conversation and show the next recommendation”.

**Result**: omit only the dashboard task's exact route key from this conversation. The audit-log task remains eligible and becomes the next recommendation, with its original priority and completion marker. Report that the dashboard was skipped for this conversation. A new conversation recommends it again if it remains unfinished.

**Restore**: if the user instead had selected persistent scope, the file would contain the dashboard task's exact `(execute-task, task-file-path#task-ID)` key. “Recommend the dashboard task again” resolves it from the skipped list or the saved key and removes that key from every active scope; the next scan may then show the task if it is still eligible. If the task completed while the user was choosing a skip duration, do not save the stale skip and report the changed recommendation instead.
