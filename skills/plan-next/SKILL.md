---
name: plan-next
description: Analyze governance state and suggest next actions; ask whether a skipped recommendation lasts for the session or until revoked.
version: 15.0.1
license: MIT
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

Unless the project sets another threshold, treat a task without progress for 7 days as stuck. Discover task, roadmap, artifact-norm, and glossary locations from project evidence; `auto` means no path is imposed in advance.

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

Read the [diagnosis procedure](references/diagnosis.md) before assessing goal, roadmap, requirements, design, tasks, drift, and hygiene. Follow its prerequisite and status rules before ranking candidates; do not infer completion from an empty result.

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

Give each suggestion an action, reason, and observable completion marker. Use prose for one clear suggestion; use separate cards for parallel actions. Read [output guidance](references/output-guidance.md) when formatting a complex recommendation or checking terminology.

---

## Self-Check

Before reporting completion, run the [full self-check](references/self-check.md). Confirm that project paths came from evidence, every goal and applicable sibling was assessed, all blockers and exclusions are represented, and every recommendation has a completion marker.

---

## Examples

Consult [worked examples](references/examples.md) when a routing case is ambiguous.
