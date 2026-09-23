---
name: plan-next
description: Analyze governance state and suggest next actions; ask whether a skipped recommendation lasts for the session or until revoked.
description_zh: 分析治理状态并推荐下一步；跳过建议时询问仅本会话有效还是持续有效直至撤销。
tags: [workflow, meta-skill, automation]
version: 15.0.0
license: MIT
recommended_scope: project
cognitive_mode: interpretive
metadata:
  author: ai-cortex
triggers: [plan next, next step, checkpoint, governance, iteration, task done, just finished, what's next, after completing, skip recommendation, skip and continue, permanently skip recommendation, restore recommendation]
input_schema:
  type: free-form
  description: Governance docs sources, optional scope and thresholds, plus a recommendation skip/restore directive. Missing project conventions may require clarification; a skip without a stated duration requires a session-or-persistent choice.
  defaults:
    thresholds:
      task_stuck_days: 7
    task_source: auto
    roadmap_tier_source: auto
    artifact_norms_path: auto
    glossary_path: auto
output_schema:
  type: chat
  description: "Always report decision_state: actionable, needs_input, no_applicable_action, or complete, including for simple results. Separate evidence, route-specific blockers, candidates, and suppressed candidates. User-facing prose stays jargon-free; diagnostic traceability may use internal codes. A skip result reports its duration and whether the project preference was saved."
---

# Skill: Plan Next

> **Role**: evidence-led governance router
> **WHAT**: discover the project's own governance model → diagnose applicable routes and blockers → rank and recommend eligible actions
> **HOW**: read-only diagnosis on ordinary runs; an explicit persistent skip or restore may update only the project preference file. For a single-dimension problem (only a known omission to check), recommend the dedicated skill directly (`define-*` and the like)
> **Distinct from**: this skill never executes downstream skills or changes governance state; document health checks are run by the runtime / linter / CI tooling per `rules/doc-health-criteria.md`

---

## Purpose and Boundaries

Inventory the governance input sources and suggest the next action.

**When to use**: at any stage of a project; **running it after every completed task is recommended**, to confirm the next focus.

### Boundaries

| Dimension | Does | Does not |
| --- | --- | --- |
| Suggestions | Suggests the next action (prose or structured cards) | Is not a task-status API; does not maintain or assign a task list; keeps no task history and does not answer time-series questions such as "how many were promoted this week" |
| Execution | Reads project state and suggests actions; an explicit persistent preference may write only `.ai-cortex/plan-next.yaml` | Does not advance anything downstream or act as an automation engine — automation comes from an outer orchestrator combined with `loop` |
| Skip choice | Omits a precisely identified recommendation for the chosen duration: this conversation or until revoked | Does not change a task, roadmap item, dependency, norm, or any other governance artifact |

**Skipping a recommendation is distinct from changing the work item**. “Never recommend this action again” records a routing preference. “Cancel the task”, “move it to Later”, or “defer the roadmap item indefinitely” requests a governance change; use `update-roadmap` for a status or date change within a tier, `promote-roadmap-items` for a tier change, and the project's task-record workflow for a task lifecycle change. Do not infer either intent from the other.

---

## Behavior

**Overall rule**: each run rescans governance state from scratch: **Discover → Diagnose → Build candidates → Filter preferences → Recommend**. Keep observations, interpretations, route-specific blockers, and user preferences distinct. A preference changes only which eligible recommendation is shown; it never changes evidence, dependency state, or completion. The only permitted write is an explicit, precisely scoped persistent exclusion or its removal in `.ai-cortex/plan-next.yaml`.

### Skip a recommendation and continue

Use this when a user wants to set aside a displayed suggestion without claiming that its underlying work is complete, cancelled, or blocked. Examples include “skip the first suggestion and continue”, “skip **Establish the documentation norms foundation** for this conversation”, and “never recommend this task again”.

#### Selector resolution

For a new skip, resolve the user's explicit selector against the most recently rendered `plan-next` result in this conversation:

| User reference | Resolution |
| --- | --- |
| “first”, “second”, or “suggestion 2” | The displayed order in that result's **Do now** list. A single prose suggestion counts as position 1. |
| An action name, a unique project-code subtitle, or a quoted recommendation | The one displayed recommendation that matches it. |
| “this” or “the current suggestion” | The sole displayed recommendation; otherwise ask the user to name or number one. |

If no preceding `plan-next` result exists in the conversation, the selector is ambiguous, or it matches several displayed actions, do not guess. Ask the user for the displayed number or action name and make no exclusion.

For a restore, resolve against the most recent **Skipped recommendations** list, the conversation's skip set, and the exact entries in `.ai-cortex/plan-next.yaml`. In a new conversation, scan current candidates to map a user's action name to an exact excluded key; an exact `(route, target)` reference also works. “Show this again” selects the sole active exclusion only; if several match or the named action no longer maps to one exact key, ask which route and target to restore. A restored route is recommended only if it is still eligible after a fresh scan.

#### Duration choice

After resolving the target, ask: “Skip this recommendation only for this conversation, or keep it excluded in this project until you restore it?” Ask whenever the user's wording does not specify the duration; “for now” alone does not decide it. Do not apply an exclusion before the answer. “This conversation” selects the session scope; “always”, “permanently”, “never recommend it again”, or an equivalent explicit duration selects the persistent scope. An explicit duration needs no second confirmation.

For a session skip, keep the route key only in the current conversation's skip set. Later `plan-next` runs in that conversation honor it; a new conversation starts with an empty session set. The user may say “show this again” to remove it early. Session skips are never written to disk. If the same key is already persistently excluded, a session-only choice cannot make it session-only: explain the existing persistent preference and ask whether to restore that preference or leave it unchanged.

For a persistent skip, add the route key to the project-local preference file defined in [plan-next-preferences](../../specs/plan-next-preferences.md). Every later run in that same project reads the file, even in a new conversation, until the user explicitly restores the route or removes its entry. “Persistent” means until revoked, not a change to task status or a waiver of governance checks. Report the file path and exact route in the response. A missing file means no persistent exclusions; a malformed file or failed write stops the preference change and must be reported rather than treated as success.

#### Persistent preference file

Use the target project's `.ai-cortex/plan-next.yaml` under the [plan-next-preferences](../../specs/plan-next-preferences.md) contract. Preserve other entries when adding or removing one. The file is project-local and may be version-controlled so collaborators see the same preference; `plan-next` does not commit it.

```yaml
schema_version: 1
exclusions:
  - route: define-docs-norms
    target: docs/ARTIFACT_NORMS.md
```

The pair `(route, target)` is the exact route key. Do not persist display titles, ordinals, wildcards, or whole categories. If several displayed actions would share a key, identify a narrower target before persisting; if that is impossible, ask the user to choose a concrete artifact or item. Adding a key already present in the selected scope is a no-op, reported as already excluded. “Recommend this again” removes the selected key from both scopes where it is active, so a session skip cannot silently keep it hidden after a persistent restoration. When both scopes contain it, update the validated file first and clear the session set only after that write succeeds; on failure, report that neither exclusion was restored. Do not edit the underlying governance artifact. Validate the file against its Spec before a read or write; if it is malformed, stop the run and name the problem.

#### Scope and continuation algorithm

1. Discover the project's declared governance conventions and diagnose normally. The scan, priority rules, prerequisites, and dependency graph remain authoritative.
2. Build the complete ordered sequence of currently eligible recommendation candidates before applying preferences or the normal display limit. Assign each candidate its exact `(route, target)` key. A candidate is eligible only if its evidenced prerequisites and `depends_on:` predecessors are satisfied.
3. Read `.ai-cortex/plan-next.yaml` when present; combine its exact route keys with the current conversation's skip set. After resolving the displayed action and duration, re-scan before changing either scope. If that exact candidate is no longer eligible or its route key changed, do not save a stale skip; explain the change and offer the current recommendations. For a restore, validate the file and remove the selected key from every active scope before recommending again.
4. Continue through the ordered sequence, omitting only matching keys. Never treat an exclusion as a completion, a blocked node, or permission to traverse beneath it. A candidate that depends on unfinished work represented by an excluded route, an unfinished ancestor, or a global prerequisite remains ineligible.
5. Render the first one to three remaining eligible candidates under the normal priority and parallelism rules. Report omitted actions and their durations separately. If every otherwise eligible route is excluded, report that fact distinctly from “all governance work is complete”.

**Prerequisite and dependency protection**: skipping a route never unlocks its dependents. A true global prerequisite blocks every route it governs; a route-scoped prerequisite blocks only its dependents; an uncertain relationship is not silently promoted to a global blocker—ask for clarification if it changes which action is safe. Continue evaluating independent candidates. Never invent a lower-level alternative just to fill the slot.

### Step 0: discover the project's governance model

Resolve canonical artifact types and locations from the strongest project-local evidence available, in this order: explicit project configuration or agent entry point; the project's own artifact norms/indexes; existing linked governance artifacts and repository structure; AI Cortex defaults only when the project declares or clearly adopts them. Record the source and confidence. Existing artifacts in a coherent project-native structure are evidence of a valid local convention, not an omission merely because a conventional directory is absent.

If sources conflict, prefer the higher-authority project declaration and report the conflict. If the project has no declared map and repository evidence cannot resolve a route's target or its applicability, mark that decision `needs_input`; ask a focused question rather than manufacturing a directory requirement. The optional cache may speed up path resolution but is not authority and never substitutes for inspecting current evidence.

### Step 1: Scan — asset inventory

**What to scan**: 3 abstraction layers × 5 subjects (MECE in combination).

| Abstraction layer | Subject | Where to scan | Refinement fields |
| --- | --- | --- | --- |
| Intent | **Why** | Project-declared locations for mission, vision, goals, and success measures (common default: `docs/project-overview/`) | — |
| Intent | **What/When** | Project-declared roadmap, backlog, requirements, and task locations (common defaults: `docs/process-management/`, `docs/requirements/`, `docs/tasks/`) | roadmap → node status; tasks → `status` |
| Intent | **How** | Project-declared design and decision-record locations (common defaults: `docs/adr/`, `docs/designs/`) | `status` |
| Implementation | **Is** | the repository code | — |
| Meta-rule | **Rules** | Project-declared locations for norms, specs, protocols, and rules; common defaults are examples, not required names | — |

The abstraction layers are mutually exclusive; the refinement fields are auxiliary dimensions of the same subject, **not a separate scan**, and are consumed by §2.1.

**How to scan** — resolve paths using Step 0, then record 2 fields for each expected asset:

| Field | Criterion |
| --- | --- |
| **Path** | The filesystem path |
| **Status** | `present` (exists, content non-empty and not a placeholder) / `placeholder` (contains only `[TODO]`/`<to-fill>`/`TBD`) / `missing` (does not exist) |

### Step 2: Diagnose — goal-tree traversal

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

#### 2.0 Applicability and prerequisite assessment

Do not treat the presence/absence of a conventional path (including `docs/ARTIFACT_NORMS.md` or `specs/`) as a universal prerequisite by itself. First determine whether the project's declared model requires it and which artifact types/routes it governs. A missing required norms artifact may create a high-priority candidate, but it blocks only routes whose applicability or safe evaluation genuinely depends on it. Scan and report independent routes regardless. If an applicable artifact location cannot be determined from project evidence, ask for the missing convention; do not guess a directory.

For every prerequisite, record: `evidence`, `scope` (`global` / named route or artifact types), and `effect` (`satisfied` / `blocks route` / `blocks all governed routes` / `uncertain`). An excluded recommendation stays unfinished and its prerequisites retain their original effect.

#### 2.0.1 Decision state

Set exactly one top-level result state after considering the complete candidate sequence and all evidence:

| State | Use when | Required user-facing behavior |
| --- | --- | --- |
| `actionable` | At least one candidate passes its prerequisites, dependencies, and safety checks after preferences are applied | Recommend the highest-priority eligible action(s); report independent blockers separately |
| `needs_input` | Missing or conflicting evidence could materially change route applicability, target, or safe next action | Ask one focused question; do not imply that no work exists or that the project is complete |
| `no_applicable_action` | Diagnosis is sufficient but no action can proceed now (waiting, dependency-protected, or all eligible routes excluded) | State the specific cause, excluded work, and any owner/wait condition; explicitly say this is not completion |
| `complete` | All project-declared goals and acceptance conditions are met; no unfinished, excluded, waiting, or evidence-limited route remains | State the evidence supporting completion; do not infer this merely from an empty candidate list |

When independent candidates remain alongside a blocked route, use `actionable` and retain the blocker as a separate finding. When applicability is genuinely unknown and changes whether those candidates are safe, use `needs_input`.

#### 2.1 Goal-tree traversal

##### Node status resolution

The status of every artifact node (roadmap node / requirement / design / task) is resolved by these rules:

1. **Explicit first**: read the `status:` field in the artifact file's frontmatter
   - Valid values: `pending` (default) | `in-progress` | `done` | `blocked`
2. **Inferred from children** (when there is no explicit `status:`):
   - All direct children `done` → the node counts as `done`
   - Any direct child `in-progress` → the node counts as `in-progress`
   - No children → counts as `pending`
3. **Precedence**: the explicit field beats inference from children

##### Parallelism decision rules

At any level, after scanning every sibling node at that level, decide as follows:

| Sibling status at this level | Parallelism suggestion |
| --- | --- |
| Exactly 1 `in-progress`, the rest `pending` | **Focus**: finish the current one before starting the next |
| 1+ `blocked`, with an independent `pending` | **Parallel**: leave the blocked one waiting and start the next independent node |
| Several `in-progress` (none blocked) | **Converge**: identify the one lagging most and push it to completion first |
| All `done` | Advance the next sibling one level up |
| All `pending`, none `in-progress` | **Start**: route to the highest-priority pending node |

Where nodes carry an explicit `depends_on:` dependency → the depended-on node must finish first, and the two cannot run in parallel.

##### Level definitions

| Level | Name | Existence criterion | Completion criterion |
| --- | --- | --- | --- |
| L1 | Strategic goal | `strategic-goals.md` is present, not a placeholder, and holds ≥1 identifiable goal item | **Both** hold: (a) the goal has `status = done`; (b) every observable KPI in the goal's "acceptance criteria" is met (the data is available and at target). `status = approved` counts as `in-progress`, and drilling down must continue |
| L2 | Roadmap node | The roadmap node exists and traces back to an L1 goal | The node has `status = done` (explicit or inferred) |
| L3 | Requirement | The requirement file is present and not a placeholder | `status = done` (explicit or inferred) |
| L4 | Design | The design/ADR file is present and not a placeholder | `status = done` (explicit or inferred) |
| L5 | Task | The task record is present | `status = done` |

##### Mandatory L1 acceptance-KPI check (critical)

**Cannot be skipped**: every time an L1 goal is traversed, the "acceptance criteria" field must be parsed first, and the observable KPIs extracted from it (name + target threshold + data source). Then judge the current state of each KPI:

| KPI state | Meaning | L1 completion verdict |
| --- | --- | --- |
| Met (data ≥ threshold, the continuity condition holds) | Acceptance passes | L1 done (given status=done) |
| Not met (data < threshold, or the continuity condition fails) | Acceptance fails | L1 in-progress, keep drilling down |
| **Data missing** (no monitoring, no query path) | Acceptance cannot be verified | **L1 in-progress, and the first route must be to establish the KPI data source** (ahead of any downstream route) |

**Key anti-pattern**: `status = approved` ≠ L1 finished. `approved` means the decision was approved and says only that the document has taken shape; `done` means acceptance is met. Confusing the two skips the downstream traversal of the whole L1 subtree, so scanning starts from a middle layer (M5/tasks) and the causal chain of "why this task matters" is lost.

**No-goal cases**: `strategic-goals.md` missing and `mission.md` missing too → route `define-mission` (P0); `mission.md` present but with no strategic goal → route `design-strategic-goals` (P0).

**Roadmap not tiered**: the roadmap exists but has no Now/Next/Later tiers → route `promote-roadmap-items` (P1), and evaluate nothing downstream.

##### Traversal algorithm

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

##### Physical scan method (L3-L5 existence detection)

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

#### Outputs of the Diagnose step

Step 3 consumes the following:

- **Per-goal traversal result**: {goal name, current focus node, level, parallelism suggestion, gap sub-label (G1/G2/G3), recommended skill}
- **List of blocked nodes**: [(level, node name, blocking reason if any)]
- **Secondary findings**: findings outside the focus goal
- **List of drift entries** (from step 2.2): [(artifact path, drift type, recommended skill)]
- **List of hygiene issues** (from step 2.3): [(issue description, recommended skill)]

#### Step 2.2: drift sweep

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

#### Step 2.3: hygiene sweep

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

### Step 3: Recommend — routing generation and tiering

**Source**: consumes the output of step 2 (see "Outputs of the Diagnose step"). Keep the candidate sequence separate from its visible projection: diagnosis first; preference filtering only after eligibility and ranking.

#### 3.1 Tiering decision

Consume the traversal and independent drift/hygiene results into a complete ordered candidate sequence, then route the first 1-3 eligible, non-excluded entries into "Do now":

- The **main-chain route** (the first gap under the highest-priority goal) is considered first when its actual prerequisites pass; if blocked, record why and continue to independent candidates
- A **parallel route** (an independent node opened up by a blocked one) also goes into "Do now" when it can start immediately
- When a displayed route is excluded for the session or persistently, omit it and continue through the candidate sequence. A dependent or lower-level route still cannot displace it.
- Beyond 3 rendered entries, truncate by priority; candidate lists are recomputed on each run. Only exact persistent route keys are stored. Blocked candidates are never promoted to executable candidates by ordering, exclusion, or display truncation.

**Parallel routing**: when the parallelism verdict is "parallel" or "converge", state the reason for parallelism or the convergence target explicitly in the routing evidence; when it is "focus", route only the current node.

**Sibling advance rule**: when a node finishes, advance automatically to the next sibling at the same level, with no re-run needed from the user; the traversal stops at the first gap of that next sibling.

**Multi-task, multi-card rendering rule**:

When an all-pending L5 triggers the "awaiting execution" branch and there are ≥2 independently startable tasks, **render several cards side by side** rather than merging them into one. Each card covers 1 task. At most 3; beyond that, truncate by priority per §3.2.

- ✅ Correct: 3 cards side by side, one task each (action name, TL;DR and completion marker all independent)
- ❌ Forbidden: merging several tasks into one card subject with a comma, a plus sign, or a verb like "start in parallel" (`T51 + T-SG5-002 start in parallel`)
- ❌ Forbidden: stacking several tasks' KPIs into one card's completion marker (`T51 dashboard reachable + T52 logs queryable + T-SG5-002 admin usable`)

For tasks that become ready tomorrow or later in the week, use the `defer` label + a TL;DR noting when they are ready; do not tuck them into a footnote on the current card.

#### 3.2 Priority (governance urgency)

- **Now (P0)**: a foundational problem with evidence that it blocks all governed routes (or L1 has no goal and the project has no higher-authority alternative)
- **Next (P1)**: the L2 roadmap is missing or not aligned to a goal
- **Later (P2)**: a gap at any of L3-L5
- **Ignorable (P3)**: the remaining secondary findings

#### 3.3 Output format selection

The output format adapts to the situation:

| Situation | Recommended format |
| --- | --- |
| One suggestion, the situation is clear | **Prose**: 1-3 sentences saying what to do, why, and what counts as done |
| ≥2 parallel suggestions, or a parallel / converge judgment is needed | **Structured cards** (format below) |

**Prose format (simple situations)**: state it directly in natural language, covering what to do → why now → what counts as done. No fields, labels or card headers needed.

**Structured card format (complex situations, ≥2 parallel suggestions)**:

```text
**N. [action name]** · `priority label`

> [TL;DR card header: one sentence answering "what to do → the immediately visible benefit", ≤30 words]

- Governance context: [multi-line short chain, ≤25 words per line; see "Writing the governance context" below]
- Recommended skill: `/skill-name [focus ≤40 words]`
- Evidence: [file path or observable signal ≤20 words]
- Completion marker: [observable result, 1 sentence]
- [optional] Cost of deferral: [the impact of not doing it ≤30 words]
- [optional] Onboarding threshold: [prior knowledge / doc path ≤30 words]
```

**Shared constraints (prose and cards alike)**: whichever format is used, every suggestion must carry what to do, why, and an observable completion marker. A project code must carry a natural-language subtitle on first appearance (see §3.3.1 + §3.7).

**Writing the TL;DR card header**:

A quote block (`> ...`), placed under the priority label and above the field list. It answers "what to do → the immediately visible benefit" in ≤30 words. It is the strongest visual anchor, so the reader sees the core action on the first screen.

- ✅ Good: `> Let the PM see coverage progress live, filling the visibility gap in Goal 1's acceptance.`
- ❌ Bad: `> Start parallel tasks to advance the milestone (repeats the subject field below, no new information).`

**Writing the governance context**:

Show the trace chain from the strategic goal down to the current gap, **and it must carry the current state of the L1 acceptance KPI**. Use a multi-line short-chain format (≤25 words per line):

```text
- Governance context:
  - Strategic goal: [the goal's natural-language name + its core KPI in one sentence]
  - Current KPI: [current value / target value / benchmark; write "data missing" when there is none]
  - Roadmap: [the milestone's natural-language name + its current stage]
  - Current position: [the layer the blockage sits in + why, ≤15 words]
```

The ≤25-word limit per line is hard. Wrap onto the next line when it overflows; nest parentheses no more than 1 level deep.

**Mandatory constraint**: every route must answer explicitly, "how does this action lead back to the strategic goal's acceptance?" If it cannot, route to the task of establishing the KPI data source instead; it must not route straight to downstream execution.

**Three ways to express KPI state** (following the triplet; see the threshold annotation in §3.3):

- Met: `citation visibility 85% / target ≥80% / industry 75-85% (met)`
- Not met: `citation visibility 62% / target ≥80% / industry 75-85% (not met)` or `citation visibility not yet measured / target ≥80% (pending measurement)`
- Data missing: `citation visibility data source missing / target ≥80% / no benchmark (data source to be built)`

**The threshold annotation triplet**:

Any KPI or threshold must carry the triplet on first appearance:

> Format: `[metric name (plain-language gloss)]: current X / target Y / benchmark Z`
>
> Example: `Adoption rate (share of recommendations users accept): current 42% / target ≥70% / 50-65% counts as good in the industry`

**The benchmark** is one of: an industry baseline, the project's own historical value, or an empirical threshold. With no benchmark available, write "project-defined (no external benchmark)" to put the reader on guard. On a metric's second appearance within the same card, the benchmark may be omitted.

> The authoritative definition of the triplet format is [rules/roadmap-quality.md](../../rules/roadmap-quality.md) §3; the roadmap's success metrics are produced by `define-roadmap` in the same format, and the wording at both ends must stay consistent.

**Writing the recommended skill**: a slash command + a completion prompt, in the format:

> `/skill-name [focus: what to do this time, the scope, the key asset path or task ID]`

Prompt requirements: state the specific focus of this call, include the key asset path or task ID, ≤40 words, and make it directly copy-pasteable. When the all-pending L5 "awaiting execution" branch has no governance skill available, write "(no governance skill; hand to the development team to implement per `[path]`)".

**Priority labels** (mapped from the internal priorities in §3.2; the "Do now" section uses only labels, never the codes):

| Internal code | User-facing label |
| --- | --- |
| P0 | `urgent` |
| P1 | `important` |
| P2 | `defer` |
| P3 | `minor` |
| — | `awaiting execution` (special: governance is ready, waiting on execution; used only for the all-pending L5 branch) |

**Completion marker**: an observable result, 1 sentence; where execution can be blocked (a strategic conflict, a dependency cycle), append "return to plan-next for re-evaluation if blocked". With several tasks, **each card owns its own completion marker**; they are not stacked at the outer level.

**Cost of deferral (optional)**:

Answers "what happens if this is not done", so the reader can judge "this one first vs something else first". ≤30 words.

- ✅ Good: `Goal 1's acceptance has no visible route, so the PM cannot judge when to wrap up the deliverables`
- ❌ Placeholder filler (forbidden): `to be added` / `see the task` / `affects the schedule` (the same as the vague-wording anti-pattern)

When there is not enough information, **omit this field**; inventing one is not allowed.

**Onboarding threshold (optional)**:

Answers "who does this next, and do they need to read up first". ≤30 words. Attach the path when pointing at a specific document.

- ✅ Good: `Requires knowing how to configure a Grafana data source; if unfamiliar, see docs/runbooks/grafana-setup.md`
- ❌ Placeholder filler (forbidden): `needs relevant knowledge` / `see the docs`

When there is not enough information, **omit this field**; inventing one is not allowed.

#### 3.3.1 Words banned from the "Do now" section

In the "Do now" section the following are **banned outright** — the codes themselves and their natural-language equivalents alike:

| Banned | Allowed instead |
| --- | --- |
| L1, L2, L3, L4, L5; goal layer, roadmap layer, requirement layer, design layer, task layer | Say "strategic goal", "roadmap", "requirement document", "design document", "task" directly |
| G1, asset missing | Describe what is actually missing: "`xxx.md` does not exist" |
| G2, incomplete content | Describe what content is missing: "missing field X / section X" |
| G3, truth drift, completion drift, traceability drift | Describe the actual inconsistency: "the task status does not reflect the code progress" |
| G4, misplacement | Describe the actual problem: "the file name does not follow the norms" |
| P0, P1, P2, P3; now/next time/later/ignorable (as a priority annotation) | Use `urgent` / `important` / `defer` / `minor` |
| pending, in-progress, done, blocked (verbatim in user-facing output) | Say "not started", "in progress", "finished", "blocked" |
| Rules layer, Why layer, What layer, How layer, Is layer | Say "norms files", "strategy documents", "planning documents", "design documents", "code implementation" |
| **A bare project code**: `T\d+` / `M\d+` / `Goal \d+` / `BL-\d+` / `ADR-\d+` / a commit hash and other internal IDs | In the header summary and the "Do now" and "Also worth noting" sections, the first appearance must carry a natural-language subtitle: `T51 (coverage dashboard)` / `M5 (hybrid-retrieval maturity milestone)`; later appearances within the same card may use the bare code; for a missing dictionary entry see the §3.7 fallback |
| **MoSCoW framework words**: Must Have / Should Have / Could Have / Won't Have | Use "must-deliver / expected-deliver / optional / not for now" instead |
| **Governance process jargon**: precondition gate / short-circuit / soft-blocked / sibling scan / focus node / all-pending branch / inference from children | Use a plain description: "the norms file is missing, establish it first" / "waiting on the developers" / "the scan result for the other nodes at this level" |
| **A bare threshold with no benchmark**: `≥70%` / `P95 ≤30s` / `a 14-day continuous window` (a number with no benchmark) | Use the triplet: `[metric name (plain-language gloss)]: current X / target Y / benchmark Z` (see the threshold annotation in §3.3) |

Violating this table = the "Do now" output is unacceptable; the offending fields must be rewritten and must not be kept.

#### 3.4 User output structure

> **Format choice**: a single suggestion may use prose instead of the cards below. The structured template below applies where there are ≥2 parallel suggestions. When any route is excluded, render `Skipped recommendations` before `Do now`, even when the remaining recommendation uses prose.

````markdown
# Next-step suggestions

> **Decision state**: `actionable` | `needs_input` | `no_applicable_action` | `complete`

> **Situation**: [objective status summary, ≤25 words. Example: the M5 must-deliver items are clear, three expected-deliver items not started]
> **Core tension**: [the sticking point this cycle, ≤30 words. Example: the adoption-rate pipeline is live but the sample has not reached 100, so acceptance cannot be judged yet]

---

## Skipped recommendations

- **[action name; displayed position when known]** — [this conversation / persistently until restored from `.ai-cortex/plan-next.yaml` / both, when both scopes contain the key]; no governance artifact or status changed.

---

## Do now

**1. [action name (project code with a natural-language subtitle)]** · `urgent / important / defer / awaiting execution`

> [TL;DR card header: what to do → the immediately visible benefit, ≤30 words]

- Governance context:
  - Strategic goal: [the goal's natural-language name + its core KPI in one sentence]
  - Current KPI: [current value / target value / benchmark; write "data missing" when there is none]
  - Roadmap: [the milestone's natural-language name + its current stage]
  - Current position: [the layer the blockage sits in + why, ≤15 words]
- Recommended skill: `/skill-name [focus ≤40 words]`
- Evidence: [file path or observable signal ≤20 words]
- Completion marker: [observable result, 1 sentence]
- [optional] Cost of deferral: [the impact of not doing it ≤30 words; omit when information is short, inventing one is not allowed]
- [optional] Onboarding threshold: [prior knowledge / doc path ≤30 words; omit when information is short]

---

**2. [action name]** · `priority label`

...(same format as above, at most 3; several tasks starting in parallel render as several side-by-side cards, see the multi-task multi-card rendering rule in §3.1)

When no candidate remains, use the appropriate state-specific behavior from §2.0.1. State the blocker or completion evidence plainly; an empty list alone is never a completion claim.

---

## Also worth noting

<!-- The drift sweep (step 2.2) and hygiene sweep (step 2.3) entries collect here, at most 5, truncated by priority -->

**[drift/hygiene name]** · `defer / minor`

[one sentence: what problem was found]

- Evidence: [file path or observable signal]
- Recommended skill: `/skill-name [focus]`

---

## Diagnostic basis (technical traceability)

<!-- This section is the internal traceability zone: L1-L5, G1-G4, P0-P3 and the status codes (pending/in-progress/done/blocked) are allowed here -->

- **Project situation**: [one-sentence summary]
- **Asset inventory**: [list only the assets whose status changed]
- **Excluded routes**: [action name, exact route key, evidence path, and session/persistent duration; write "none" when empty]
- **Route blockers**: [candidate/action, blocker evidence, scope, and whether independent candidates remain; write "none" when empty]
- **Open decision** (when `needs_input`): [the one fact needed and how its answer changes routing]

**Decision logic**:

| Level | Node | Status | Inference |
|---|---|---|---|
| Strategic goal | [goal name] | [KPI state] | [keep drilling down / skip / route] |
| Roadmap | [node name] | [pending/in-progress/done/blocked] | [sibling scan conclusion + focus node / the rule that fired] |
| Requirement | [requirement name] | [status] | [verdict] |
| Design | [design name] | [status] | [verdict] |
| Task | [task name / set] | [status] | ["awaiting execution" branch / route downstream / completion verdict] |

- **Drift sweep result**: [list of drift entries; write "none" when empty]
- **Hygiene sweep result**: [list of hygiene issues; write "none" when empty]
- **Missing dictionary notice** (if any): [the project codes not found in the dictionary, with a suggestion to add them to `docs/glossary.md`]
````

#### 3.7 Terminology dictionary lookup

**Purpose**: inject a natural-language subtitle for project codes automatically, so the user-facing output can be read on its own and no one has to consult an internal ID dictionary to understand it.

**Dictionary sources (in discovery order)**:

1. The `glossary_path` input parameter (when the caller supplies it)
2. `.ai-cortex/glossary.yaml`
3. `docs/glossary.md`
4. **Fallback**: read the source artifact's frontmatter `title:` field (the `title:` of `docs/tasks/T51.md`, say); with no frontmatter, take the first H1 heading

**Dictionary schema** (in YAML):

```yaml
T51:
  full_name: coverage dashboard task
  one_liner: lets the PM see coverage progress live
M5:
  full_name: milestone 5, "hybrid retrieval matures"
Goal 1:
  full_name: requirement clarification depends on the knowledge base running reliably
  kpi: adoption rate ≥70% for 14 consecutive days
```

**Field notes**:

- `full_name` (required): the natural-language name, used to inject the subtitle
- `one_liner` (optional): the core value in one sentence, usable to help generate the TL;DR card header
- `kpi` (optional, strategic goals only): a short statement of the core KPI

**Lookup rules at the output layer**:

| Situation | Rendering |
| --- | --- |
| A project code appears for the first time and the dictionary has it | Inject `code (full_name)`, for example `T51 (coverage dashboard task)` |
| Later appearances within the same card | The bare code only |
| The dictionary has no matching entry | Fall back to the source artifact's frontmatter `title:`, injecting the first ≤12 words |
| Both the dictionary and the fallback are missing | Mark it in the diagnostic-basis section as "dictionary miss: suggest adding `<code>` to `docs/glossary.md`", and **do not show that code in the user-facing sections**; use a generic description instead ("the task awaiting execution", say) |

**Constraints**:

- A missing dictionary is not an error and blocks nothing — the degraded output is still usable
- The dictionary lookup injects only into the "Do now" and "Also worth noting" sections; the diagnostic-basis section allows bare codes
- A malformed dictionary source YAML → HALT and ask the user to fix it (the same behavior as the norms resolution in §0)

---

## Anti-Patterns

**On responsibility boundaries**:

- ❌ Calling any downstream skill or editing a governance artifact
- ❌ Hiding the reason for a skip or treating a route-level blocker as global
- ❌ Mixing in downstream execution detail (no writing ADRs, no fixing code, no tidying structure)
- ❌ Treating a skipped recommendation as `done`, `blocked`, `cancelled`, a date change, or any other persisted governance state
- ❌ Choosing session or persistent scope when the user did not specify one
- ❌ Carrying a session skip into another conversation, or silently dropping a persistent preference on a later run
- ❌ Reporting a saved preference when `.ai-cortex/plan-next.yaml` was not written successfully
- ❌ Guessing which recommendation an ambiguous ordinal or title means

**On the routing itself**:

- ❌ Vague wording ("possibly / perhaps / could consider")
- ❌ Omitting the completion marker
- ❌ Mixing several gap types into one route
- ❌ Assigning priority by the number of gaps
- ❌ Skipping a level in the tree-traversal report (reporting an L3 route while L2 is missing) — it violates "first gap first"
- ❌ Judging "finished" from git signals — completion at L2-L5 is judged by the `status` field; **L1 completion must additionally pass the acceptance-KPI check**
- ❌ Ignoring an explicit `status:` field and relying only on inference from children — explicit wins
- ❌ **Treating `status = approved` as the criterion for L1 done** — approved = the decision was approved ≠ acceptance met; confusing them skips the whole L1 subtree
- ❌ **Bypassing L1 and reporting a middle layer (M5/tasks) directly** — answer "is the L1 acceptance KPI met" first, then drill down
- ❌ A governance-context field with no current L1 acceptance-KPI value — it violates the "a route must lead back to the strategic goal's acceptance" constraint
- ❌ Routing straight to downstream execution while the L1 acceptance-KPI data source is missing — the first route should establish the KPI data source
- ❌ Forcing a downstream skill in when L5 is all pending — with the tasks already there, no governance skill applies, and the output should be an "awaiting execution" card
- ❌ Not considering a parallel start when a blocked node is present — blocked is a parallelism signal
- ❌ Recommending yet more parallel expansion when several nodes are in-progress and none blocked — the suggestion is to converge
- ❌ Merging routes for several goals without naming each goal's source in the evidence
- ❌ Evaluating downstream while the roadmap is untiered, skipping `promote-roadmap-items`
- ❌ Ignoring the `depends_on:` field and suggesting parallelism anyway — a dependency forces sequence
- ❌ Using a skipped precondition or unfinished ancestor as permission to route to its children
- ❌ Replacing an excluded recommendation with a dependent route merely to ensure that "Do now" is non-empty

**On tree traversal and scanning**:

- ❌ Reporting a gap on a done node in the main "Do now" routing (the hygiene sweep's checks on done nodes are the exception, and go to "Also worth noting")
- ❌ Reporting gaps at several levels of the same node at once (it violates depth-first)
- ❌ Introducing a mode enum or configuration override for the governance scan (read the physical signals directly)
- ❌ Taking on manifest maintenance (a difference is emitted as a G3 diagnostic entry, not repaired)

**On internal terminology leaking**:

- ❌ A code appearing in the "Do now" section: any form of L1-L5, G1-G4, P0-P3
- ❌ The natural-language equivalents of those codes appearing in "Do now": asset missing, incomplete content, truth drift, completion drift, traceability drift, misplacement, goal layer, roadmap layer, requirement layer, design layer, task layer, Rules layer, Why layer, What layer, How layer, Is layer
- ❌ Priorities using the old labels "now/next time/later/ignorable" or the P0-P3 numbering (use `urgent/important/defer/minor`)
- ❌ Verbatim status values in the "Do now" section: pending/in-progress/done/blocked (use: not started/in progress/finished/blocked)
- ❌ Using a level number as the subject in the diagnostic basis (a parenthetical trace is allowed, a subject is not)
- ❌ An example titled "L2→L3 advance" (use a natural-language description of the situation)

**On jargon and judgment scaffolding**:

- ❌ A bare project code (`T51` / `M5` / `Goal 1` / `BL-001` / `ADR-033`, and so on) with no natural-language subtitle on first appearance
- ❌ MoSCoW framework words in a user-facing section (Must Have / Should Have / Could Have / Won't Have)
- ❌ Governance process jargon in a user-facing section (precondition gate, short-circuit, soft-blocked, sibling scan, focus node, all-pending branch, inference from children)
- ❌ A threshold with no benchmark (a bare `≥70%` / `P95 ≤30s` / `14-day continuous window`) — the triplet is mandatory: current value / target value / benchmark
- ❌ Merging several tasks into one card subject with a comma, a plus sign, or "start in parallel" (`T51 + T-SG5-002` / `T51, T52 in parallel`) — several tasks render as several cards
- ❌ Stacking several tasks' KPIs into one card's completion marker (`A reachable + B queryable + C usable`) — each card owns its own completion marker
- ❌ A governance context nesting parentheses more than 1 level deep (`Goal X (acceptance: KPI A current 80% (met) / target ≥70% (stretch))`) — split it into a multi-line short chain
- ❌ A governance context written as a single chain over 60 words — it must become a multi-line short chain of ≤25 words per line
- ❌ Filling the cost-of-deferral / onboarding-threshold fields with placeholder text ("to be added" / "see the task" / "affects the schedule" / "needs relevant knowledge") — omit when information is short
- ❌ A TL;DR card header that repeats the subject field ("start parallel tasks to advance the milestone" restates the subject) — it must answer "the immediately visible benefit"
- ❌ Forcing a code missing from the dictionary into a user-facing section (mark it in the diagnostic basis, and use a generic description in the user-facing section)

---

## Self-Check

**Scan**:

- [ ] Project governance sources were discovered in precedence order; unresolved conventions are reported rather than replaced with assumed directories
- [ ] The 2 asset fields are present (path + status)
- [ ] Whether the roadmap is tiered has been decided; where it is not, `promote-roadmap-items` has been routed
- [ ] The project-declared artifact conventions and evidence source for each path mapping were identified; no conventional directory was assumed mandatory

**Diagnose**:

- [ ] The strategic goals were read; with no goal, the L1 route fired
- [ ] **The L1 acceptance-criteria KPIs were parsed**; each goal's current KPI state was decided (met / not met / data missing)
- [ ] **L1 status=approved counts as in-progress**, and drilling down was not skipped
- [ ] **Where the KPI data source is missing**, the first route establishes the data source rather than routing downstream
- [ ] Every node's status was resolved by "explicit first > inference from children"
- [ ] Every level's sibling nodes were scanned in full and classified (done / in-progress / blocked / pending)
- [ ] The parallelism decision rules were applied; the suggestion (focus / parallel / converge / start) is stated
- [ ] The L3-L5 physical scan is complete (glob + optional parent: + optional manifest)
- [ ] The L3→L4 / L4→L5 G3 chain check was run; depth first (an upper-level G3 hit stops the lower-level report)
- [ ] The "finished" verdict rests on the status field alone, with no git signals introduced
- [ ] The drift sweep (step 2.2) was run; artifacts past the threshold are in the drift entry list
- [ ] The hygiene sweep (step 2.3) was run; finished-but-unarchived milestones, ADR status problems and repository structure problems were all scanned
- [ ] Prerequisites were scoped to the routes they actually govern; uncertain applicability was surfaced as `needs_input`, not inflated into a global blocker

**Recommend**:

- [ ] Every suggestion carries what to do, why, and an observable completion marker (prose or card alike)
- [ ] **The format choice is right**: prose for a single suggestion; structured cards for ≥2 parallel suggestions
- [ ] **A KPI or threshold carries the triplet on first appearance** (current value / target value / benchmark); with no benchmark, "project-defined (no external benchmark)" is noted
- [ ] Depth first (only the first gap in the tree is reported per goal)
- [ ] A parallel suggestion states the reason for parallelism in the text
- [ ] Drift and hygiene entries are all in the "Also worth noting" section and have not crowded out the first two slots of "Do now"
- [ ] **(When using structured cards)** The TL;DR quote block is ≤30 words and does not repeat the subject
- [ ] **(When using structured cards)** The governance context is a multi-line short chain (≤25 words per line) carrying the current L1 acceptance-KPI state
- [ ] **(When using structured cards)** The priority label is mapped correctly (urgent / important / defer / minor / awaiting execution)
- [ ] **(When using structured cards)** An all-pending L5 with several tasks (≥2 independently startable) renders as several side-by-side cards, not merged
- [ ] **(When using structured cards)** The cost-of-deferral / onboarding-threshold fields are omitted where information is short, not filled with placeholder text
- [ ] **(When a skip directive is present)** The selector was resolved against the conversation's displayed recommendation and its exact route key, or clarification was requested without excluding anything
- [ ] **(When duration is unspecified)** The user chose session or persistent scope before any exclusion was applied
- [ ] **(When persistent scope is chosen)** The preference file was validated and updated once, with unrelated entries preserved; a failed write was reported as a failure
- [ ] **(When a restore directive is present)** The selected active exclusion was identified exactly and cleared from every scope where it was active, or clarification was requested without a partial change
- [ ] **(When the project changed during a duration choice)** The displayed route was revalidated before any skip was saved; a stale suggestion was not persisted
- [ ] **(When a skip directive is present)** The complete eligible candidate sequence was considered before the display limit; every remaining route still passed its normal preconditions and dependencies
- [ ] **(When an exclusion is active)** The omitted action and its duration are reported, and a no-candidate result says so plainly rather than exposing a dependent route
- [ ] A `no_applicable_action` result is not called complete; `complete` requires all declared acceptance conditions met and no unfinished, excluded, or evidence-limited work

**Output**:

- [ ] **The header summary (situation/core tension) is within the word limits**: situation ≤25 words, core tension ≤30 words; no bare project code (the same rule as the "Do now" section)
- [ ] The "Do now" section carries no codes: L1-L5, G1-G4, P0-P3
- [ ] The "Do now" section carries no natural-language equivalents of the codes: asset missing, incomplete content, truth drift, completion drift, traceability drift, misplacement
- [ ] The "Do now" section carries no old priority labels: now/next time/later/ignorable; priorities are uniformly `urgent/important/defer/minor`
- [ ] The "Do now" section carries no English status codes: pending, in-progress, done, blocked
- [ ] **The "Do now" and "Also worth noting" sections carry no bare project code** (`T\d+` / `M\d+` / `Goal \d+` / `BL-\d+` / `ADR-\d+`) — every first appearance carries a natural-language subtitle
- [ ] **The "Do now" section carries no MoSCoW words** (Must Have / Should Have / Could Have / Won't Have)
- [ ] **The "Do now" section carries no governance process jargon** (precondition gate / short-circuit / soft-blocked / sibling scan / focus node / all-pending branch / inference from children)
- [ ] **A code missing from the dictionary is marked in the diagnostic-basis section**, not forced into a user-facing section
- [ ] **The diagnostic-basis decision logic uses a table** (4 columns: level / node / status / inference), not prose
- [ ] Ordinary diagnosis made no writes; an explicit persistent skip or restore touched only `.ai-cortex/plan-next.yaml`
- [ ] The diagnostic basis names each goal's traversal position and the blocked nodes
- [ ] No session skip was written to disk; no persistent skip was treated as completion

---

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
