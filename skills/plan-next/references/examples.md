# plan-next: worked examples

## Examples

Examples 1-6 illustrate project-wide diagnosis under the stated project conventions. Their expanded trace fields are illustrative; focused recommendations use only the context needed for the user's choice. Examples 10-12 cover the version 16 default and its evidence boundaries.

### Example 1: a half-built strategy (the normal path)

**Scenario**: the user requests a project-wide planning diagnosis. The project requires goal-backed roadmap decisions, has mission / vision but no strategic goals, and its roadmap has no other evidenced direction. Goal clarification is needed to choose among competing roadmap actions.

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

**Scenario**: the user asks which items to pull into the current plan. Project policy requires Now/Next/Later placement for that decision, but the roadmap is a flat list without tiers or another source-backed current selection. Independent work with settled scope is unaffected.

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

**Scenario**: the user asks whether a finite goal can close. In `strategic-goals.md`, goal G1 has frontmatter `status: approved`, its acceptance criterion is "citation visibility ≥ 80% across two consecutive iterations", and there is no monitoring data. That missing measurement prevents the requested closure judgment. Under stage M5 (the milestone carrying G1) all 17 tasks are `pending`, the task breakdown is complete, and the designs/ADRs are in place. An independently authorized task can still be recommended separately.

**Key verdicts**:

- L1: G1 `status=approved` does not establish closure; the acceptance KPI "citation visibility" has no data → establish its data source because the current closure decision requires that evidence
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

### Example 9: reorder the queue across replies

The initial result recommends “Prepare the coverage dashboard” first and “Add the audit log” second. Both can start independently.

| Reply | Updated result |
| --- | --- |
| “Put 2 first.” | Rescan. If both remain eligible, show the audit log first and the dashboard second. The preference lasts for this conversation. |
| “Next.” | Skip the audit log, now in the first position, for this conversation. Show the dashboard first in the same reply. Report the dropped move and the new skip. |
| “Show the audit log again.” | Rescan and remove the skip. If both are still eligible, the dashboard is first in the default order. |

If the audit log becomes blocked before the first reply is processed, leave the move unapplied and explain the blocker. If the dashboard remains eligible, keep it in the updated result. A downstream action waiting on the audit log remains ineligible throughout.

### Example 10: continue after a completed review and a paused follow-up

**Input**: the conversation concerns feedback intake. The owner says the review is complete, pauses follow-up interviews, and invokes `plan-next` without another scope. The review's source record contains its accepted result. The interview record still says planned. An older roadmap has unresolved numeric thresholds unrelated to the available intake improvements.

**Expected recommendation**: state that this run compares next actions after the accepted review and carries the owner's interview pause forward. Inspect the review outcomes, candidate records and their dependencies. Do not recommend interviews, assert their record was updated, or promote the unrelated threshold dispute. Explain the source discrepancy and suggest synchronization if it affects coordination. Recommend only an evidenced ready action, with the benefit it delivers now, relevant alternatives and its completion marker.

If the owner reports review completion but no acceptance evidence exists, retain that report as unverified. A dependent action remains ineligible until the required evidence is found or obtained. An independent candidate can still proceed within existing authorization.

### Example 11: accept a correction, compare tied choices and hand off

**Input**: a result recommends resolving old roadmap thresholds. The owner replies, “That is not the main problem; I need people to find the right skill.” The skill-discovery records support both clarifying entry descriptions and revising public names, with no settled precedence between them. The request authorizes discussion only.

**Expected response**: revise the question to skill discovery. Compare clearer descriptions, which preserve existing invocation names, with renaming, which also requires reference and compatibility decisions. Show genuine uncertainty rather than inventing an urgency score. A missing unrelated usage metric stays a limitation. If both choices are equally supported, source order and route key provide stable display only.

When the owner selects “clarify the descriptions,” prepare a `refine-skill-design` handoff identifying the affected entries, their source paths, the discovery problem, retained names and discussion-only boundary. Its completion marker is an inspectable wording proposal distinguishing the intended use of each entry. Selection does not authorize source edits. A later explicit implementation instruction can authorize those edits through the normal workflow.

### Example 12: distinguish scope exhaustion from project completion

**Input**: the only remaining interview action is paused. Other eligible actions in this conversation were skipped. The owner asks for the next recommendation without an explicit scope limit.

**Expected response**: retain the pause and exact exclusions, then inspect other independent project work in the same reply. If an eligible route exists, return `actionable` with that route's evidence and completion marker. Otherwise report the project-wide conditions under `no_applicable_action`, or `needs_input` if material evidence is unavailable. Do not restore exclusions or recommend a dependent task merely to fill the queue.

**Explicit limit variant**: the owner previously said “only inspect feedback intake” and has not revoked it. Keep that scope, report local `no_applicable_action` and offer broader inspection. Do not assert project completion. Only verified project-wide closure supports `complete`.

### Example 13: release waiting while independent work is ready

**Reported reproduction**: after review verification, external-test notification, roadmap synchronization, commit and push for release item 327, feedback closure must wait until 2026-11-11 14:54:35 Asia/Shanghai (UTC+08:00). The next bare invocation should not stop at that release scope and ask whether to inspect the project. The timestamp is a not-before condition, not evidence that closure succeeds at that instant.

**Synthetic project evidence for review**: at 2026-11-08 10:00:00 Asia/Shanghai, the release source records the wait; the active roadmap also contains a higher-priority independent task A with approved prerequisites, an existing implementation workflow and a testable acceptance marker. Task B depends on feedback closure for 327. Task C is paused and task D is cancelled. The repository records the closeout operations as completed. These extra tasks are review fixtures, not claims about the actual consuming project's backlog.

**Walkthrough**: start with 327 and verify its source closure condition. Retain its exact wait outside **Do now**. No eligible release action remains, so expand read-only diagnosis across the active roadmap and linked sources. A passes readiness and independence checks; B fails its dependency; C and D remain ineligible. Return `actionable`, recommend A with its source, workflow and acceptance marker, and explain the expanded coverage. Do not repeat commit, push or synchronization. An implementation handoff retains the existing authorization; a bare invocation performs no implementation.

### Scope regression review cases

Apply these variations to Example 13's evidence. Review the input → inspection → eligibility → result → permission path, not the presence of a template phrase. These are manual contract walkthroughs; they do not execute an agent or prove runtime behavior.

| Case | Evidence or request variation | Expected inspection and result |
| --- | --- | --- |
| Waiting focus | Base fixture | Inspect independent project work in the same reply; `actionable` with A, retaining 327's exact wait. |
| Finished focus | 327 has verified closure; A remains ready | Inspect beyond 327; `actionable` with A. No repeated closeout work. |
| Explicit scope | “Only inspect release 327,” including an earlier unrevoked instruction | Inspect 327 only; local `no_applicable_action`, wait condition and optional offer to expand. |
| Dependency not met | A also depends on 327 | Inspect the project, but neither A nor B is eligible; C/D remain inactive. `no_applicable_action` with dependency and wait conditions. |
| Paused or cancelled | A is paused or cancelled | Do not reactivate A, C or D. B remains blocked. `no_applicable_action`. |
| All excluded | A's exact route is session-skipped or persistently excluded | Follow the queue continuation algorithm through expansion, preserving that exclusion; `no_applicable_action` with exclusions and blockers, without a forced restore or permission request merely to inspect. |
| Evidence missing | A's prerequisite/independence record is unavailable | Disclose unavailable sources and actual coverage; `needs_input` for the missing fact, not a claim of project-wide inactivity. |
| Truly no action now | All unfinished routes are waiting or dependency-blocked; source inventory is sufficient | Project-wide `no_applicable_action`; name the remaining conditions. Waiting is not completion. |
| Global gate | A verified prerequisite governs every route and is unmet | Expansion does not bypass it; recommend its evidenced resolution if eligible, otherwise report the global blocking condition. |
| Caller execution limit | Caller permits execution only on 327, without limiting read-only diagnosis | Diagnosis may return `actionable` with A; executor retains that state but makes no unauthorized change and reports its execution boundary. |
| Closeout competes | An optional cleanup remains beside higher-priority ready A | Compare the active backlog; recommend A under recorded priorities. Cleanup wins only with an evidenced priority or prerequisite effect. |
| Project complete | All finite goals have closure evidence and no unfinished, excluded, waiting or evidence-limited route remains | Full project diagnosis may return `complete`; mere exhaustion of 327 cannot. |

**Baseline review (16.0.0)**: SKILL.md's queue rule explicitly waits for a broader-scope choice after exhaustion; diagnosis returns local `no_applicable_action`; output guidance, self-check and the old Example 12 reinforce that stop. Thus the waiting-focus and finished-focus cases fail their required inspection path even when A is independently ready. Explicit scope and dependency safeguards already hold and must be retained.

**Revised contract review (17.0.0)**: the same inputs follow the expansion rule before final decision-state assignment. The waiting/finished cases reach A; explicit scope prevents expansion; dependencies, pauses, cancellations, exclusions and global gates prevent ineligible substitutions. Output and self-check distinguish original-item waiting from the inspected project's result. Caller guidance retains execution gates. This review establishes instruction consistency only; no live replay against the consuming project or model evaluation was performed.
