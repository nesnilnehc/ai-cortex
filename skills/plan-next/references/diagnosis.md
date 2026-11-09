# plan-next: diagnosis

## Step 2: Diagnose — goal-tree traversal

**Core question**: which evidenced action helps the user make progress on the current question? Is the next step focus or parallelism?

**Model**: use the selected question and scope from SKILL.md. The governance tree helps trace a candidate's purpose, prerequisites and unfinished work. For project-wide diagnosis, traverse all applicable goals in their recorded order. For focused diagnosis, inspect the current work and follow only the links needed to judge the choice. A higher-level omission is not automatically the next action.

```text
Strategic goal
└── Roadmap node (several, ordered)
    └── Requirement (several, one set per roadmap node)
        └── Design/ADR (several, one set per requirement)
            └── Task (several, one set per design)
```

**4 sub-steps** (run in order):

| Sub-step | What it does | Output |
| --- | --- | --- |
| 2.0 Applicability and prerequisite assessment | Which declared prerequisites govern which routes? | Classify each as satisfied, route-blocking, globally blocking, or uncertain; do not short-circuit unrelated routes |
| 2.1 Goal-tree traversal | Inspect relevant work and dependencies; in project-wide scope, traverse every applicable goal | Current positions, choices and the parallelism verdict |
| 2.2 Drift sweep | Artifact updated_at vs the time the aligned goal changed; past the threshold, route to a dedicated skill | A list of drift entries |
| 2.3 Hygiene sweep | Archiving finished milestones, ADR status, repository structure, changes in the skills layer, and so on | A list of hygiene issues |

The G1-G4 gap types are used as sub-labels in the diagnostic-basis section. In a focused run, drift and hygiene checks cover relevant sources only. Report other areas as not inspected, not as having no findings.

### 2.0 Applicability and prerequisite assessment

Do not treat the presence/absence of a conventional path (including `docs/ARTIFACT_NORMS.md` or `specs/`) as a universal prerequisite by itself. First determine whether the project's declared model requires it and which artifact types/routes it governs. A missing required norms artifact may create a high-priority candidate, but it blocks only routes whose applicability or safe evaluation genuinely depends on it. Scan and report independent routes regardless. If an applicable artifact location cannot be determined from project evidence, ask for the missing convention; do not guess a directory.

For every prerequisite, record: `evidence`, `scope` (`global` / named route or artifact types), and `effect` (`satisfied` / `blocks route` / `blocks all governed routes` / `uncertain`). An excluded recommendation stays unfinished and its prerequisites retain their original effect.

### 2.0.1 Decision state

Set exactly one top-level result state after considering the complete candidate sequence within the declared scope and its evidence. Keep the existing state values for callers such as orchestrate-governance-step. An internal call without current-work context defaults to project-wide diagnosis. Explicit caller scope limits and existing decisions are carried through unchanged unless conflicting evidence requires clarification. An implicit current focus follows SKILL.md's scope-expansion rule before the final state is assigned.

| State | Use when | Required user-facing behavior |
| --- | --- | --- |
| `actionable` | At least one candidate passes its prerequisites, dependencies, and safety checks after preferences are applied | Recommend the highest-priority eligible action(s); report independent blockers separately |
| `needs_input` | Missing or conflicting evidence could materially change route applicability, target, or safe next action | Ask one focused question; do not imply that no work exists or that the project is complete |
| `no_applicable_action` | Diagnosis is sufficient but no action can proceed now (waiting, dependency-protected, or all eligible routes excluded) | State the specific cause, excluded work, and any owner/wait condition; explicitly say this is not completion |
| `complete` | All project-declared goals and acceptance conditions are met; no unfinished, excluded, waiting, or evidence-limited route remains | State the evidence supporting completion; do not infer this merely from an empty candidate list |

When independent candidates remain alongside a blocked route, use `actionable` and retain the blocker as a separate finding. When applicability is genuinely unknown and changes whether those candidates are safe, use `needs_input`.

A focused result never establishes project completion. If no eligible action remains in an implicit focus, expand read-only diagnosis under SKILL.md before assigning the final state. An independent eligible project route yields `actionable` while the original wait remains a separate finding. With an explicit scope limit, use `no_applicable_action` for local exhaustion and offer broader inspection. Reserve `complete` for project-wide evidence meeting the table's criterion; unavailable evidence may require `needs_input`.

### 2.1 Goal-tree traversal

#### Requirement-and-defect roadmap adapter

When roadmap rows directly reference requirements or defects, L2 is a planning view
of the L3 source record, not an extra artifact with mandatory children. Resolve each
row by its stable source ID, visit that source once, and continue to its existing
designs and tasks. Do not call `capture-work-items` merely because the row has no
nested requirement. Defects use their project's record and repair-evidence contracts;
no new requirement or design document is required solely to fit this tree.

Read approval/lifecycle and execution states separately according to project norms.
`draft`, `approved` and tier placement do not prove completion. An execution summary
must follow [roadmap-quality](../../../rules/roadmap-quality.md), with separate
approval, execution and key conditions. Verify the declared closure criterion and
source acceptance/release evidence before treating a row as finished; development
complete, acceptance passed and production release are not interchangeable.
For traversal only, Not started maps to pending, In progress to in-progress,
Completed to done only after closure verification, and Blocked to blocked.
Awaiting acceptance and Awaiting release remain unfinished: recommend the applicable
existing acceptance/release action or report its waiting condition; do not infer done
from finished tasks or route back to development solely because they are unfinished.
Paused retains its resume condition and is not recommended for execution without
an explicit resume decision. Cancelled work is also ineligible without an explicit
reactivation decision; neither state maps to pending merely to fill the queue. These are diagnostic mappings, not replacement roadmap
labels or new authorization. Missing/conflicting execution evidence stays unknown;
report a limitation rather than defaulting to pending or inferring completion.
Apply
this adapter before the legacy milestone-node traversal below. The legacy form is
readable for existing projects; new requirement-view rows are requirements or defects.
Load [roadmap modeling](../../../specs/roadmap-modeling.md) for selected views.
Version groups reference entry IDs; phases reference entry/version scope; milestone
events have their own IDs and relate to entries, versions or phases (or are global).
Do not create duplicate governance-tree requirements for them. Event occurrence
requires evidence, never child-status inference; do not demand design/tasks for an
event itself. Legacy milestone directories are work-package containers. Check scope/time agreement across enabled
views, and route version-scope/date problems to `update-roadmap`, structure problems
to `define-roadmap`. Missing unselected views are not governance defects.
Known post-adoption material changes without revision evidence, dropped decision
records or broken retained-history links route to `update-roadmap`. Unknown prior
history is disclosed rather than reconstructed. Revision rows are history, not
new requirement nodes or evidence that current work is complete.
Priority policy application and explicit reassessment are separate intents; stale
assessment history may justify suggesting reassessment, never running it implicitly.

#### Node status resolution

For requirement-and-defect roadmap rows and their source completion, the adapter above takes precedence over the legacy rules below, including child inference. Other artifact nodes use their project contract; the following is the legacy fallback:

1. **Explicit first**: read the `status:` field in the artifact file's frontmatter
   - Valid values: `pending` (default) | `in-progress` | `done` | `blocked`
2. **Inferred from children** (when there is no explicit `status:`):
   - All direct children `done` → the node counts as `done`
   - Any direct child `in-progress` → the node counts as `in-progress`
   - No children → counts as `pending`
3. **Precedence**: the explicit field beats inference from children

#### Parallelism decision rules

At any level, after scanning every sibling node at that level, decide as follows:

| Sibling status at this level | Parallelism suggestion |
| --- | --- |
| Exactly 1 `in-progress`, the rest `pending` | **Focus**: finish the current one before starting the next |
| 1+ `blocked` or externally waiting, with an independent `pending` | **Parallel**: leave the blocked one waiting and start the next independent node |
| Several `in-progress` (none blocked) | **Converge**: identify the one lagging most and push it to completion first |
| All `done` | Advance the next sibling one level up |
| All `pending`, none `in-progress` | **Start**: route to the highest-priority pending node |

Where nodes carry an explicit `depends_on:` dependency → the depended-on node must finish first, and the two cannot run in parallel.

#### Level definitions

| Level | Name | Existence criterion | Completion criterion |
| --- | --- | --- | --- |
| L1 | Strategic goal | Resolve identifiable goals from project authority | Use the project's goal and closure contract. A finite goal needs its declared status and acceptance evidence. A declared continuing direction has no inferred terminal state. |
| L2 | Roadmap node | The roadmap node exists and traces back to an L1 goal | The node has `status = done` (explicit or inferred) |
| L3 | Requirement | The requirement file is present and not a placeholder | `status = done` (explicit or inferred) |
| L4 | Design | The design/ADR file is present and not a placeholder | `status = done` (explicit or inferred) |
| L5 | Task | The task record is present | `status = done` |

#### Acceptance evidence and measurement

For every inspected goal, read its project-defined meaning and applicable acceptance criteria. Extract declared observable KPIs with their target and data source. Retain unknown measurements explicitly. Continuing strategic directions do not acquire a mandatory completion KPI merely because the diagnostic template expects one.

| KPI state | Meaning | L1 completion verdict |
| --- | --- | --- |
| Met (the declared threshold and continuity condition hold) | Supports that acceptance criterion | Close only under the project's full closure contract |
| Not met | That criterion remains unsatisfied | Inspect relevant unfinished work |
| Data missing or conflicting | That criterion cannot be verified | Recommend measurement or clarification first only when the missing fact changes the current choice, readiness or closure verdict; otherwise report the limitation and continue independently supported work |

**Key anti-pattern**: `status = approved` ≠ L1 finished. `approved` means the decision was approved and says only that the document has taken shape; `done` means acceptance is met. Confusing the two skips the downstream traversal of the whole L1 subtree, so scanning starts from a middle layer (M5/tasks) and the causal chain of "why this task matters" is lost.

**No-goal cases**: when project-wide diagnosis has no higher-authority alternative and cannot identify purpose or direction, suggest `define-mission` if both mission and goals are absent, or `design-strategic-goals` if mission exists. Explain which planning choice needs that work. In a focused run, a safely bounded current task need not wait for unrelated strategy documentation.

**Roadmap not tiered**: when the project requires tier placement and the current choice depends on it, suggest `promote-roadmap-items`. Otherwise retain the project's valid planning model and assess independent work. An absent default tier layout alone is not a global stop.

#### Traversal algorithm

```text
Resolve the current question, scope, user decisions and project conventions.
In focused scope, start at the selected work and inspect relevant dependencies.
If no eligible action remains in an implicit focus, expand read-only project diagnosis
before assigning the final decision state; preserve explicit scope limits.
In project-wide scope, inspect each applicable goal in its recorded priority order.
Apply the source-record adapter and project closure contract before legacy fallback.
For each relevant goal G, finite or continuing, not verified complete:

  [L1] Is closure verified from status and declared acceptance? → check the next goal

  [L2] Take every roadmap node under G and apply the parallelism decision rules:
    No nodes → route: define-roadmap (P1); stop on this goal
    All done → verify G's own closure evidence; continuing directions remain open
    Take the set F of "current focus nodes" (per the parallelism decision)

  For each node N in F (in priority order):

    [L3] Take every requirement under N and apply the parallelism decision rules:
      No requirements → route: capture-work-items (P2); stop on this node
      All done → N is finished; move to the next sibling roadmap node

    For the current focus requirement R:

      [L4] Take every design under R and apply the parallelism decision rules:
        No design → emit a "design to be produced" awaiting-execution card (the design workflow is carried by the AgentFabric runtime); stop on this requirement
        All done → R is finished; move to the next sibling requirement

      For the current focus design D:

        [L5] Take every task under D and apply the parallelism decision rules:
          No tasks → emit a "tasks to be broken down" awaiting-execution card (task breakdown is carried by the AgentFabric runtime); stop on this design
          All done → D is finished; move to the next sibling design
          Blocked tasks + independent pending tasks → parallel: route to start a pending one
          An in-progress task (not blocked) → focus: it is running, look for the sticking point
          ★ All pending, none in-progress (tasks broken down but not started) →
             no governance sub-skill to route to (execution belongs to the developer layer, outside plan-next's scope);
             "Do now" emits an "awaiting execution" marker card (distinct from "nothing to show"), carrying:
               - the focus task name + task ID + the intended result it serves + its relevant acceptance evidence
               - label: `awaiting execution` (a new priority label, distinct from urgent/important/defer/minor)
             This card tells orchestrate-governance-step: governance is ready, waiting on outside execution (the signal emitted is blocked, not done)
```

#### Physical scan method (L3-L5 existence detection)

```text
2.1.1 Read each artifact_type's path_pattern from the step 0 cache
      (use the project value on a hit; fall back to the skill's default norm path on a miss)
2.1.2 Glob each path_pattern directory by node slug
      → matched = exists; unmatched = a G1 gap
2.1.3 (enhancement) Scan the `parent:` frontmatter field to build a reverse index and raise confidence
2.1.4 (enhancement) Detect manifest files (`now/<slug>.md`, say)
      → when one exists, compare manifest vs physical; treat a difference as G3 drift
2.1.5 After G1 passes, check the content correspondence between levels (the G3 chain):
      L3→L4: the design carries parent/upstream_ref pointing at the requirement, or its content clearly answers the requirement's key constraints
      L4→L5: the task carries parent pointing at the design, or covers the main implementation modules of the design
      Depth first: when L3→L4 hits a G3, do not go on to report an L4→L5 G3
```

The diagnostic basis has to name the combination of physical signals the scan relied on (for example: "slug + 2 manifests detected + no parent field").

Use the fallback tree only for artifact types the project requires. Stop descending a branch whose prerequisite prevents safe evaluation, while continuing independent branches. Missing optional designs, task files or conventional directories create no work by themselves. Once candidates are eligible, apply SKILL.md's current-work ordering rather than ranking by the number or depth of omissions.

### Outputs of the Diagnose step

Step 3 consumes the following:

- **Per-goal traversal result**: {goal name, current focus node, level, parallelism suggestion, gap sub-label (G1/G2/G3), recommended skill}
- **List of blocked nodes**: [(level, node name, blocking reason if any)]
- **Secondary findings**: findings outside the focus goal
- **List of drift entries** (from step 2.2): [(artifact path, drift type, recommended skill)]
- **List of hygiene issues** (from step 2.3): [(issue description, recommended skill)]

### Step 2.2: drift sweep

Compare the artifact's `updated_at` with the time of the change event at the matching level; past the threshold, route to a dedicated skill.

**Thresholds (internal constants, not exposed to the user)**:

| Parameter | Default | Meaning |
| --- | --- | --- |
| `drift_staleness_days` | 30 | An artifact not updated for more than this many days counts as drifted |
| `backlog_rescore_days` | 90 | A backlog last re-scored more than this many days ago counts as stale |
| `doc_health_staleness_days` | 30 | A document health report older than this many days counts as expired (produced by the runtime / CI) |

**Routing table**:

| Drift signal | Recommended skill |
| --- | --- |
| backlog `last_rescored_at` older than `backlog_rescore_days` | `/prioritize-backlog` |
| Architecture docs drifting from the code (the gap between an ADR's updated_at and the latest code commit exceeds the threshold) | `/review-architecture` |
| Health signals such as document SSOT, code alignment, or link rot | detected by the runtime / linter / CI tooling per `rules/doc-health-criteria.md` |

**Constraint**: report drift in "Also worth noting" unless its evidenced effect blocks the current choice or safe progress. In that case recommend the relevant resolution with its causal rationale under SKILL.md's ordering rules.

### Step 2.3: hygiene sweep

Check for slowly accumulating governance debt and output a list of hygiene issues.

**Thresholds (internal constants)**:

| Parameter | Default | Meaning |
| --- | --- | --- |
| `milestone_archive_age_days` | 60 | A legacy work package finished more than this many days ago meets the age condition |
| `milestone_archive_lookback` | 2 | A gap of ≥ N between the active legacy work-package index and target slug meets the index condition |

**Checks**:

| Check | Condition | Recommended skill |
| --- | --- | --- |
| A finished legacy work package is not archived | `milestones/{slug}/tasks.md` all done, and any one of the maturity conditions holds | `/archive-milestone {slug}` |
| ADR status loop violated | superseded / conflicting / no accepted conclusion | `/review-architecture` |
| Repository structure drift | `_templates/` entries missing / file naming violations | detected by the runtime / CI per `rules/repo-structure-hygiene.md` |
| Document health checks backed up | The health report has not been updated for > `doc_health_staleness_days` days | have the runtime / CI run one full `rules/doc-health-criteria.md` check |

**Constraint**: report hygiene in "Also worth noting" unless a verified prerequisite makes its resolution necessary for the current choice or safe progress. A generic cleanup opportunity alone does not displace current work.

### Roadmap family diagnosis

Load linked delivery/iteration/version/history views under the main roadmap as
projections, not extra goal-tree nodes. Check the Roadmap Spec reading/ownership
contract and selected iteration view against the quality Rule. Structure/layout
findings suggest define-roadmap; existing iteration goals/scope/cadence/timeboxes
or source/projection disagreement suggest update-roadmap. Missing optional views
are not defects. Iteration boundaries prove neither completion nor release.

Scenario choices are project evidence, not a checklist requiring all views. Preserve
custom and legacy combinations; missing 1.4 metadata alone is no gap. Source/view/
primary conflicts suggest define-roadmap; changed needs suggest reconsideration
without replacing existing choices. Do not count recommendation output as approval.
