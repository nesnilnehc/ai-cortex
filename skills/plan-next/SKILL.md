---
name: plan-next
description: Analyze governance state and suggest next actions from existing docs; read-only — never executes downstream skills.
description_zh: 基于现有治理文档分析状态并给出下一步行动建议；只读——不执行下游技能。
tags: [workflow, meta-skill, automation]
version: 13.3.1
license: MIT
recommended_scope: project
cognitive_mode: interpretive
metadata:
  author: ai-cortex
triggers: [plan next, next step, checkpoint, governance, iteration, task done, just finished, what's next, after completing]
input_schema:
  type: free-form
  description: Governance docs sources, optional scope, optional threshold overrides, optional glossary_path override.
  defaults:
    thresholds:
      task_stuck_days: 7
    task_source: auto
    roadmap_tier_source: docs/process-management/roadmap.md
    artifact_norms_path: docs/ARTIFACT_NORMS.md
    glossary_path: auto
output_schema:
  type: chat
  description: "Adaptive text suggestions + plain Diagnosis section (## heading, always present). Simple situations: 1-2 sentences of prose. Complex situations (≥2 parallel suggestions): structured cards each with TL;DR quote block, governance_context multi-line short-chain (≤25 words/line), recommended_skill, rationale, completion_marker, priority_label; 2 optional fields (deferral_cost / onboarding_threshold; omit when info insufficient). User-facing sections always jargon-free: no internal codes (L1-L5, G1-G4, P0-P3), no raw status values (pending/in-progress/done/blocked), no project codes without natural-language subtitle (T\\d+/M\\d+/Goal \\d+/BL-\\d+/ADR-\\d+), no MoSCoW words, no process slang. KPI/threshold first occurrence requires triplet (current/target/benchmark). Diagnosis section uses 4-column table and is a technical traceability zone where internal codes are allowed."
---

# Skill: Plan Next

> **Role**: governance entry-point advisor
> **WHAT**: three steps — **Scan** (inventory the governance assets) → **Diagnose** (goal-tree traversal: depth-first per goal to the first unfinished node, combined with a parallelism verdict) → **Recommend** (suggest the next action)
> **HOW**: read-only diagnosis; for a single-dimension problem (only a known omission to check), recommend the dedicated skill directly (`define-*` and the like)
> **Distinct from**: this skill only makes suggestions and runs nothing downstream; document health checks are run by the runtime / linter / CI tooling per `rules/doc-health-criteria.md`

---

## Purpose and Boundaries

Inventory the governance input sources and suggest the next action.

**When to use**: at any stage of a project; **running it after every completed task is recommended**, to confirm the next focus.

### Boundaries

| Dimension | Does | Does not |
|---|---|---|
| Suggestions | Suggests the next action (prose or structured cards) | Is not a task-status API; does not maintain or assign a task list; keeps no task history and does not answer time-series questions such as "how many were promoted this week" |
| Execution | Read-only — the suggestions go to the user or to an outer orchestrator to decide on | Does not advance anything downstream on its own; is not an automation engine — automation comes from an outer orchestrator combined with `loop` |

---

## Behavior

**Overall rule**: **stateless** — every run rescans from scratch and depends on no previous result. Three steps: **Scan → Diagnose → Recommend**.

### Step 0: resolve the norms

`cache` is used for the `path_pattern` resolution in step 2.1.

### Step 1: Scan — asset inventory

**What to scan**: 3 abstraction layers × 5 subjects (MECE in combination).

| Abstraction layer | Subject | Where to scan | Refinement fields |
|---|---|---|---|
| Intent | **Why** | `docs/project-overview/{mission,vision,north-star,strategic-goals,strategic-pillars}.md` | — |
| Intent | **What/When** | `docs/process-management/{roadmap,backlog/}.md`, `docs/requirements/`, `docs/tasks/` | roadmap → node status; tasks/ → `status` |
| Intent | **How** | `docs/adr/`, `docs/designs/` | `status` |
| Implementation | **Is** | the repository code | — |
| Meta-rule | **Rules** | `docs/ARTIFACT_NORMS.md`, `specs/`, `protocols/`, `rules/` | — |

The abstraction layers are mutually exclusive; the refinement fields are auxiliary dimensions of the same subject, **not a separate scan**, and are consumed by §2.1.

**How to scan** — record 2 fields for each asset:

| Field | Criterion |
|---|---|
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
|---|---|---|
| 2.0 Precondition gate | Is the Rules layer in place? | Otherwise short-circuit |
| 2.1 Goal-tree traversal | Traverse each goal depth-first, locate the first gap + the parallelism verdict | Each goal's current position + routing suggestions |
| 2.2 Drift sweep | Artifact updated_at vs the time the aligned goal changed; past the threshold, route to a dedicated skill | A list of drift entries |
| 2.3 Hygiene sweep | Archiving finished milestones, ADR status, repository structure, changes in the skills layer, and so on | A list of hygiene issues |

The G1-G4 gap types are used as sub-labels in the diagnostic-basis section.

#### 2.0 Precondition gate: check for a missing Rules layer

If `ARTIFACT_NORMS.md` is missing or `specs/` is empty, trigger a **short-circuit**: skip the goal-tree traversal, and let "Do now" list a single P0 route (establish the norms + re-run plan-next).

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
|---|---|
| Exactly 1 `in-progress`, the rest `pending` | **Focus**: finish the current one before starting the next |
| 1+ `blocked`, with an independent `pending` | **Parallel**: leave the blocked one waiting and start the next independent node |
| Several `in-progress` (none blocked) | **Converge**: identify the one lagging most and push it to completion first |
| All `done` | Advance the next sibling one level up |
| All `pending`, none `in-progress` | **Start**: route to the highest-priority pending node |

Where nodes carry an explicit `depends_on:` dependency → the depended-on node must finish first, and the two cannot run in parallel.

##### Level definitions

| Level | Name | Existence criterion | Completion criterion |
|---|---|---|---|
| L1 | Strategic goal | `strategic-goals.md` is present, not a placeholder, and holds ≥1 identifiable goal item | **Both** hold: (a) the goal has `status = done`; (b) every observable KPI in the goal's "acceptance criteria" is met (the data is available and at target). `status = approved` counts as `in-progress`, and drilling down must continue |
| L2 | Roadmap node | The roadmap node exists and traces back to an L1 goal | The node has `status = done` (explicit or inferred) |
| L3 | Requirement | The requirement file is present and not a placeholder | `status = done` (explicit or inferred) |
| L4 | Design | The design/ADR file is present and not a placeholder | `status = done` (explicit or inferred) |
| L5 | Task | The task record is present | `status = done` |

##### Mandatory L1 acceptance-KPI check (critical)

**Cannot be skipped**: every time an L1 goal is traversed, the "acceptance criteria" field must be parsed first, and the observable KPIs extracted from it (name + target threshold + data source). Then judge the current state of each KPI:

| KPI state | Meaning | L1 completion verdict |
|---|---|---|
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
|---|---|---|
| `drift_staleness_days` | 30 | An artifact not updated for more than this many days counts as drifted |
| `backlog_rescore_days` | 90 | A backlog last re-scored more than this many days ago counts as stale |
| `doc_health_staleness_days` | 30 | A document health report older than this many days counts as expired (produced by the runtime / CI) |

**Routing table**:

| Drift signal | Recommended skill |
|---|---|
| backlog `last_rescored_at` older than `backlog_rescore_days` | `/prioritize-backlog` |
| Architecture docs drifting from the code (the gap between an ADR's updated_at and the latest code commit exceeds the threshold) | `/review-architecture` |
| Health signals such as document SSOT, code alignment, or link rot | detected by the runtime / linter / CI tooling per `rules/doc-health-criteria.md` |

**Constraint**: a drift item must go into the "Also worth noting" section and must not take one of the first two slots in "Do now" (unless the main routing is idle and the drift priority reaches P1).

#### Step 2.3: hygiene sweep

Check for slowly accumulating governance debt and output a list of hygiene issues.

**Thresholds (internal constants)**:

| Parameter | Default | Meaning |
|---|---|---|
| `milestone_archive_age_days` | 60 | A milestone finished more than this many days ago is mature enough to archive |
| `milestone_archive_lookback` | 2 | A gap of ≥ N between the current in-progress milestone index and the slug counts as archivable |

**Checks**:

| Check | Condition | Recommended skill |
|---|---|---|
| A finished milestone is not archived | `milestones/{slug}/tasks.md` all done, and any one of the maturity conditions holds | `/archive-milestone {slug}` |
| ADR status loop violated | superseded / conflicting / no accepted conclusion | `/review-architecture` |
| Repository structure drift | `_templates/` entries missing / file naming violations | detected by the runtime / CI per `rules/repo-structure-hygiene.md` |
| Document health checks backed up | The health report has not been updated for > `doc_health_staleness_days` days | have the runtime / CI run one full `rules/doc-health-criteria.md` check |

**Constraint**: a hygiene item must go into the "Also worth noting" section and must not take one of the first two slots in "Do now".

### Step 3: Recommend — routing generation and tiering

**Source**: consumes the output of step 2 (see "Outputs of the Diagnose step").

#### 3.1 Tiering decision

Consume the per-goal traversal results from §2.1 and route them all into "Do now" (1-3 entries):

- The **main-chain route** (the first gap under the highest-priority goal) always goes into "Do now"
- A **parallel route** (an independent node opened up by a blocked one) also goes into "Do now" when it can start immediately
- Beyond 3 entries, truncate by priority; the secondary gaps of the other goals are not shown

**Parallel routing**: when the parallelism verdict is "parallel" or "converge", state the reason for parallelism or the convergence target explicitly in the routing evidence; when it is "focus", route only the current node.

**Sibling advance rule**: when a node finishes, advance automatically to the next sibling at the same level, with no re-run needed from the user; the traversal stops at the first gap of that next sibling.

**Multi-task, multi-card rendering rule**:

When an all-pending L5 triggers the "awaiting execution" branch and there are ≥2 independently startable tasks, **render several cards side by side** rather than merging them into one. Each card covers 1 task. At most 3; beyond that, truncate by priority per §3.2.

- ✅ Correct: 3 cards side by side, one task each (action name, TL;DR and completion marker all independent)
- ❌ Forbidden: merging several tasks into one card subject with a comma, a plus sign, or a verb like "start in parallel" (`T51 + T-SG5-002 start in parallel`)
- ❌ Forbidden: stacking several tasks' KPIs into one card's completion marker (`T51 dashboard reachable + T52 logs queryable + T-SG5-002 admin usable`)

For tasks that become ready tomorrow or later in the week, use the `defer` label + a TL;DR noting when they are ready; do not tuck them into a footnote on the current card.

#### 3.2 Priority (governance urgency)

- **Now (P0)**: a foundational problem blocking all other governance progress (the Rules layer is missing, or L1 has no goal)
- **Next (P1)**: the L2 roadmap is missing or not aligned to a goal
- **Later (P2)**: a gap at any of L3-L5
- **Ignorable (P3)**: the remaining secondary findings

#### 3.3 Output format selection

The output format adapts to the situation:

| Situation | Recommended format |
|---|---|
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
|---|---|
| P0 | `urgent` |
| P1 | `important` |
| P2 | `defer` |
| P3 | `minor` |
| —  | `awaiting execution` (special: governance is ready, waiting on execution; used only for the all-pending L5 branch) |

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
|---|---|
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

> **Format choice**: a single suggestion may use prose instead of the cards below. The structured template below applies where there are ≥2 parallel suggestions.

````
# Next-step suggestions

> **Situation**: [objective status summary, ≤25 words. Example: the M5 must-deliver items are clear, three expected-deliver items not started]
> **Core tension**: [the sticking point this cycle, ≤30 words. Example: the adoption-rate pipeline is live but the sample has not reached 100, so acceptance cannot be judged yet]

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
|---|---|
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

- ❌ Calling any downstream skill (the read-only hard boundary)
- ❌ Hiding the reason for a skip (a short-circuit must be stated explicitly)
- ❌ Mixing in downstream execution detail (no writing ADRs, no fixing code, no tidying structure)

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

**On tree traversal and scanning**:

- ❌ Reporting a gap on a done node in the main "Do now" routing (the hygiene sweep's checks on done nodes are the exception, and go to "Also worth noting")
- ❌ Reporting gaps at several levels of the same node at once (it violates depth-first)
- ❌ Introducing a mode enum or a config field (read the physical signals directly)
- ❌ Taking on manifest maintenance (plan-next is read-only; a difference is emitted as a G3 diagnostic entry, not repaired)

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

- [ ] The cache is loaded, or "no norms found" is stated explicitly
- [ ] The 2 asset fields are present (path + status)
- [ ] Whether the roadmap is tiered has been decided; where it is not, `promote-roadmap-items` has been routed

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
- [ ] Read-only was respected
- [ ] The diagnostic basis names each goal's traversal position and the blocked nodes

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
|---|---|---|---|
| Strategic goal | strategic-goals.md | missing | L1 gap, traversal stops; route design-strategic-goals |
| Roadmap | — | not evaluated | re-run once L1 is ready |

- **Drift sweep result**: none
- **Hygiene sweep result**: none

### Example 2: a new project starting up (the short-circuit case)

**Scenario**: a new project; `docs/ARTIFACT_NORMS.md` does not exist and `specs/` is empty.

**Output** (example):

#### Next-step suggestions

> **Situation**: a new project, the documentation norms file is missing
> **Core tension**: with no shared norms, every governance document that follows has no standard to work from, so the goal-tree traversal is skipped

---

##### Do now

**1. Establish the documentation norms foundation** · `urgent`

> Establish the documentation norms first, so every governance file that follows has a standard to work from.

- Governance context:
  - Strategic goal: not yet reachable (stopped early because the norms file is missing)
  - Current KPI: data missing (the governance norms are not established)
  - Roadmap: not yet evaluated (re-run once the norms file is ready)
  - Current position: the norms file is missing, the goal-tree traversal is skipped
- Recommended skill: `/define-docs-norms generate docs/ARTIFACT_NORMS.md from the project structure`
- Evidence: `docs/ARTIFACT_NORMS.md` is missing, `specs/` is empty
- Completion marker: re-run plan-next once ARTIFACT_NORMS.md lands

##### Diagnostic basis

- **Project situation**: the norms layer is absent, the goal-tree traversal is skipped

**Decision logic**:

| Level | Node | Status | Inference |
|---|---|---|---|
| Norms layer | ARTIFACT_NORMS.md | missing | the absent norms trigger an early stop, the goal-tree traversal is skipped |
| Strategic goal | — | not evaluated | re-run plan-next once the norms are ready |

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
|---|---|---|---|
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
|---|---|---|---|
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
|---|---|---|---|
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
|---|---|---|---|
| Strategic goal | G1 | approved (counts as in-progress) | status=approved ≠ done; the KPI data source is missing → the first route establishes the data source |
| Roadmap | M5 | in-progress | the only focus milestone, keep drilling down |
| Requirement | M5 requirement set | in-progress | designs/ADRs are ready, drill down to the task layer |
| Design | ADR-033/034 | done | no task gap |
| Task | T47 (17 in total, all-pending) | all-pending | the "awaiting execution" branch, emit the focus task card (label: awaiting execution) |

- **Drift sweep result**: none
- **Hygiene sweep result**: none
