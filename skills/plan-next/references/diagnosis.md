# plan-next: diagnosis

## Step 2: Diagnose — goal-tree traversal

**Core question**: where is the goal chain stuck? Is the next step focus or parallelism?

**Model**: the governance artifacts form a tree; "the next step" = the first unfinished node found depth-first under the highest-priority goal, combined with the parallelism verdict, to give an execution suggestion.

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
| 2.1 Goal-tree traversal | Traverse each goal depth-first, locate the first gap + the parallelism verdict | Each goal's current position + routing suggestions |
| 2.2 Drift sweep | Artifact updated_at vs the time the aligned goal changed; past the threshold, route to a dedicated skill | A list of drift entries |
| 2.3 Hygiene sweep | Archiving finished milestones, ADR status, repository structure, changes in the skills layer, and so on | A list of hygiene issues |

The G1-G4 gap types are used as sub-labels in the diagnostic-basis section.

### 2.0 Applicability and prerequisite assessment

Do not treat the presence/absence of a conventional path (including `docs/ARTIFACT_NORMS.md` or `specs/`) as a universal prerequisite by itself. First determine whether the project's declared model requires it and which artifact types/routes it governs. A missing required norms artifact may create a high-priority candidate, but it blocks only routes whose applicability or safe evaluation genuinely depends on it. Scan and report independent routes regardless. If an applicable artifact location cannot be determined from project evidence, ask for the missing convention; do not guess a directory.

For every prerequisite, record: `evidence`, `scope` (`global` / named route or artifact types), and `effect` (`satisfied` / `blocks route` / `blocks all governed routes` / `uncertain`). An excluded recommendation stays unfinished and its prerequisites retain their original effect.

### 2.0.1 Decision state

Set exactly one top-level result state after considering the complete candidate sequence and all evidence:

| State | Use when | Required user-facing behavior |
| --- | --- | --- |
| `actionable` | At least one candidate passes its prerequisites, dependencies, and safety checks after preferences are applied | Recommend the highest-priority eligible action(s); report independent blockers separately |
| `needs_input` | Missing or conflicting evidence could materially change route applicability, target, or safe next action | Ask one focused question; do not imply that no work exists or that the project is complete |
| `no_applicable_action` | Diagnosis is sufficient but no action can proceed now (waiting, dependency-protected, or all eligible routes excluded) | State the specific cause, excluded work, and any owner/wait condition; explicitly say this is not completion |
| `complete` | All project-declared goals and acceptance conditions are met; no unfinished, excluded, waiting, or evidence-limited route remains | State the evidence supporting completion; do not infer this merely from an empty candidate list |

When independent candidates remain alongside a blocked route, use `actionable` and retain the blocker as a separate finding. When applicability is genuinely unknown and changes whether those candidates are safe, use `needs_input`.

### 2.1 Goal-tree traversal

#### Node status resolution

The status of every artifact node (roadmap node / requirement / design / task) is resolved by these rules:

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
| 1+ `blocked`, with an independent `pending` | **Parallel**: leave the blocked one waiting and start the next independent node |
| Several `in-progress` (none blocked) | **Converge**: identify the one lagging most and push it to completion first |
| All `done` | Advance the next sibling one level up |
| All `pending`, none `in-progress` | **Start**: route to the highest-priority pending node |

Where nodes carry an explicit `depends_on:` dependency → the depended-on node must finish first, and the two cannot run in parallel.

#### Level definitions

| Level | Name | Existence criterion | Completion criterion |
| --- | --- | --- | --- |
| L1 | Strategic goal | `strategic-goals.md` is present, not a placeholder, and holds ≥1 identifiable goal item | **Both** hold: (a) the goal has `status = done`; (b) every observable KPI in the goal's "acceptance criteria" is met (the data is available and at target). `status = approved` counts as `in-progress`, and drilling down must continue |
| L2 | Roadmap node | The roadmap node exists and traces back to an L1 goal | The node has `status = done` (explicit or inferred) |
| L3 | Requirement | The requirement file is present and not a placeholder | `status = done` (explicit or inferred) |
| L4 | Design | The design/ADR file is present and not a placeholder | `status = done` (explicit or inferred) |
| L5 | Task | The task record is present | `status = done` |

#### Mandatory L1 acceptance-KPI check (critical)

**Cannot be skipped**: every time an L1 goal is traversed, the "acceptance criteria" field must be parsed first, and the observable KPIs extracted from it (name + target threshold + data source). Then judge the current state of each KPI:

| KPI state | Meaning | L1 completion verdict |
| --- | --- | --- |
| Met (data ≥ threshold, the continuity condition holds) | Acceptance passes | L1 done (given status=done) |
| Not met (data < threshold, or the continuity condition fails) | Acceptance fails | L1 in-progress, keep drilling down |
| **Data missing** (no monitoring, no query path) | Acceptance cannot be verified | **L1 in-progress, and the first route must be to establish the KPI data source** (ahead of any downstream route) |

**Key anti-pattern**: `status = approved` ≠ L1 finished. `approved` means the decision was approved and says only that the document has taken shape; `done` means acceptance is met. Confusing the two skips the downstream traversal of the whole L1 subtree, so scanning starts from a middle layer (M5/tasks) and the causal chain of "why this task matters" is lost.

**No-goal cases**: `strategic-goals.md` missing and `mission.md` missing too → route `define-mission` (P0); `mission.md` present but with no strategic goal → route `design-strategic-goals` (P0).

**Roadmap not tiered**: the roadmap exists but has no Now/Next/Later tiers → route `promote-roadmap-items` (P1), and evaluate nothing downstream.

#### Traversal algorithm

```text
For each strategic goal G (in priority order, skipping any with status = done):

  [L1] Does the goal itself have status = done? → skip it, check the next goal

  [L2] Take every roadmap node under G and apply the parallelism decision rules:
    No nodes → route: define-roadmap (P1); stop on this goal
    All done → G is met; consider a new goal; stop
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
               - the focus task name + task ID + the strategic goal it serves + how that task affects the L1 acceptance KPI
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

**Constraint**: a drift item must go into the "Also worth noting" section and must not take one of the first two slots in "Do now" (unless the main routing is idle and the drift priority reaches P1).

### Step 2.3: hygiene sweep

Check for slowly accumulating governance debt and output a list of hygiene issues.

**Thresholds (internal constants)**:

| Parameter | Default | Meaning |
| --- | --- | --- |
| `milestone_archive_age_days` | 60 | A milestone finished more than this many days ago is mature enough to archive |
| `milestone_archive_lookback` | 2 | A gap of ≥ N between the current in-progress milestone index and the slug counts as archivable |

**Checks**:

| Check | Condition | Recommended skill |
| --- | --- | --- |
| A finished milestone is not archived | `milestones/{slug}/tasks.md` all done, and any one of the maturity conditions holds | `/archive-milestone {slug}` |
| ADR status loop violated | superseded / conflicting / no accepted conclusion | `/review-architecture` |
| Repository structure drift | `_templates/` entries missing / file naming violations | detected by the runtime / CI per `rules/repo-structure-hygiene.md` |
| Document health checks backed up | The health report has not been updated for > `doc_health_staleness_days` days | have the runtime / CI run one full `rules/doc-health-criteria.md` check |

**Constraint**: a hygiene item must go into the "Also worth noting" section and must not take one of the first two slots in "Do now".
