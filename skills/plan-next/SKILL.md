---
name: plan-next
description: Recommend next actions from the current problem, prior decisions and project evidence. Compare options, prepare a focused skill handoff, or diagnose the whole project when requested or no context exists.
version: 16.0.0
license: MIT
---

# Skill: Plan Next

> **Role**: evidence-led governance router
> **WHAT**: establish the current decision → inspect relevant project evidence → compare eligible actions → prepare the next skill handoff
> **HOW**: read-only diagnosis on ordinary runs; an explicit persistent skip or restore may update only the project preference file. For a single-dimension problem (only a known omission to check), recommend the dedicated skill directly (`define-*` and the like)
> **Distinct from**: this skill never executes downstream skills or changes governance state; document health checks are run by the runtime / linter / CI tooling per `rules/doc-health-criteria.md`

---

## Purpose and Boundaries

Help the user choose and enter the next useful action. Carry forward their current problem, settled decisions and authorization, check relevant evidence, and explain the available choices. Use project-wide diagnosis when requested or when no current context exists.

**When to use**: at any stage of a project; **running it after every completed task is recommended**, to confirm the next focus.

### Boundaries

| Dimension | Does | Does not |
| --- | --- | --- |
| Suggestions | Suggests the next action (prose or structured cards) | Is not a task-status API; does not maintain or assign a task list; keeps no task history and does not answer time-series questions such as "how many were promoted this week" |
| Execution | Reads project state and suggests actions; an explicit persistent preference may write only `.ai-cortex/plan-next.yaml` | Does not advance anything downstream or act as an automation engine — automation comes from an outer orchestrator combined with `loop` |
| Queue preferences | Reorders eligible recommendations in this conversation and omits exact recommendations for this conversation or until restored | Does not change project priorities, task status, roadmap placement, or dependencies |

**Skipping a recommendation is distinct from changing the work item**. “Never recommend this action again” records a routing preference. “Cancel the task”, “move it to Later”, or “defer the roadmap item indefinitely” requests a governance change; use `update-roadmap` for a status or date change within a tier, `promote-roadmap-items` for a tier change, and the project's task-record workflow for a task lifecycle change. Do not infer either intent from the other.

---

## Behavior

**Overall rule**: establish the question and scope, check current evidence, build eligible candidates, apply recommendation preferences, and help the user choose. The only permitted write is an explicit, precisely scoped persistent exclusion or its removal in `.ai-cortex/plan-next.yaml`.

### Establish the current decision

Read the request and relevant conversation before selecting sources. Identify the project, current work, intended result, settled decisions, unresolved choices and existing authorization. A bare invocation continues identifiable current work. An explicit project-wide request overrides that default; absent usable context, diagnose the whole project. Ask only when an unresolved scope choice would materially change the recommendation.

Start the response with the question being answered and the inspected scope. Inspect the current item's records, relevant decisions, dependencies and acceptance evidence first, then trace upstream or outward where those facts affect the choice. Project-wide diagnosis still inventories all applicable goals and siblings. Report uninspected areas rather than presenting a focused result as a whole-project assessment.

Distinguish a user's decision from a verified project state. A decision to pause work governs recommendations in this conversation; it does not itself update the source record. Verify a reported completion before relying on it for dependency readiness or closure. If source evidence conflicts with a current user decision, retain both, explain the effect and suggest record alignment when needed. Never silently discard the decision or assert an unverified transition.

Missing documents, conflicting thresholds and unmeasured metrics become first actions only when they materially affect the current choice or safe progress. State that causal link. Otherwise retain them as background findings. A verified prerequisite still blocks every route within its declared scope.

### Adjust the recommendation queue

After rendering suggestions in a user-facing conversation, accept relevant follow-up replies as part of `plan-next` without requiring another invocation. Interpret commands in the user's language. On each relevant reply, resolve any selector against the last result, rescan, apply the valid adjustment, and return the updated result in the same reply. Keep the latest result, skip set, and order adjustments scoped to this project in this conversation.

| Reply | Effect |
| --- | --- |
| “Next recommendation” or “next” while reviewing the queue | Skip the first displayed recommendation for this conversation and return the revised queue. If none is displayed, refresh and report the result without recording a skip. |
| “Skip 2 for this conversation” or “keep this recommendation hidden until I restore it” | Apply the existing skip rules below to the exact target and chosen duration. |
| “Show the dashboard recommendation again” | Apply the existing restore rules and return the revised queue. |
| “Put 2 first” or “move the audit log before the dashboard” | Move one eligible recommendation to the front or before another eligible recommendation for this conversation. |
| “Reset recommendation order” | Clear the conversation's order adjustments and return to the current default order. Keep skip choices. |
| “Show the queue” | Show the eligible recommendations beyond the usual display limit as well. |
| “Refresh” or a report that an action was completed | Recheck current evidence and advance where it supports doing so. Use the project's normal completion criteria. |
| “That is not the main problem” or a correction of the intended outcome | Revisit the current question and recommendation rationale, retain valid decisions, and rebuild candidates before proposing another action. |

For a move, resolve both items, when applicable, to exact route keys before rescanning. Apply the move to the fresh queue after exclusions. Retain the order of the other entries. Record each valid move in conversation order and replay it on refresh. Drop a move whose target or reference is no longer eligible or has been excluded, and report which move was dropped. A move that already matches the requested order needs no additional entry. Ranking preferences apply only to eligible candidates and respect the existing focus and dependency rules. A new conversation starts with the default order.

Use the latest **Do now** positions for unqualified numbers. When the user opens the queue, also accept a unique name from its extra entries. If a selector is ambiguous, ask only for the affected item. If the user chooses an action or ends queue review, conclude the recommendation interaction. Further scans happen in response to relevant user input or a fresh invocation.

Explain a reordered list as the user's conversation preference and retain each action's underlying priority rationale. If the current scope is exhausted or all eligible actions are skipped, state the remaining conditions and offer to inspect a broader scope. Wait for that choice before broadening merely to fill the list. Selection produces a focused handoff naming the skill or existing project workflow, objective, target, source evidence and completion marker. Carry authorization and unresolved decisions through it; selecting a recommendation grants no additional implementation or external-write permission. Downstream execution belongs to the selected workflow or outer executor.

### Skip a recommendation and continue

Use this when a user wants to set aside a displayed suggestion without claiming that its underlying work is complete, cancelled, or blocked. Examples include “skip the first suggestion and continue”, “skip **Establish the documentation norms foundation** for this conversation”, and “never recommend this task again”.

#### Selector resolution

For a new skip, resolve the user's selector against the most recently rendered `plan-next` result in this conversation. The queue command “next” explicitly selects its first displayed recommendation and conversation scope:

| User reference | Resolution |
| --- | --- |
| “first”, “second”, or “suggestion 2” | The displayed order in that result's **Do now** list. A single prose suggestion counts as position 1. |
| An action name, a unique project-code subtitle, or a quoted recommendation | The one displayed recommendation that matches it. |
| “this” or “the current suggestion” | The sole displayed recommendation; otherwise ask the user to name or number one. |

If no preceding `plan-next` result exists in the conversation, the selector is ambiguous, or it matches several displayed actions, do not guess. Ask the user for the displayed number or action name and make no exclusion.

For a restore, resolve against the most recent **Skipped recommendations** list, the conversation's skip set, and the exact entries in `.ai-cortex/plan-next.yaml`. In a new conversation, scan current candidates to map a user's action name to an exact excluded key; an exact `(route, target)` reference also works. “Show this again” selects the sole active exclusion only; if several match or the named action no longer maps to one exact key, ask which route and target to restore. A restored route is recommended only if it is still eligible after a fresh scan.

#### Duration choice

After resolving the target, ask: “Skip this recommendation only for this conversation, or keep it excluded in this project until you restore it?” Ask for an ordinary skip whose wording does not specify the duration. “For now” alone does not decide it. The queue command “next” already selects conversation scope. Do not apply an exclusion before the answer. “This conversation” selects the session scope; “always”, “permanently”, “never recommend it again”, or an equivalent explicit duration selects the persistent scope. An explicit duration needs no second confirmation.

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

1. Establish the current question and scope, discover the project's declared governance conventions, and diagnose relevant evidence. The scan, priority rules, prerequisites, and dependency graph remain authoritative.
2. Build the complete ordered sequence of currently eligible recommendation candidates before applying preferences or the normal display limit. Assign each candidate its exact `(route, target)` key. A candidate is eligible only if its evidenced prerequisites and `depends_on:` predecessors are satisfied.
3. Read `.ai-cortex/plan-next.yaml` when present; combine its exact route keys with the current conversation's skip set. After resolving the displayed action and duration, re-scan before changing either scope. If that exact candidate is no longer eligible or its route key changed, do not save a stale skip; explain the change and offer the current recommendations. For a restore, validate the file and remove the selected key from every active scope before recommending again.
4. Omit matching keys, then apply valid conversation order adjustments. Never treat an exclusion or move as a completion, a blocked node, or permission to traverse beneath it. A candidate that depends on unfinished work represented by an excluded route, an unfinished ancestor, or a global prerequisite remains ineligible.
5. Recommend the first remaining eligible candidate, with up to two alternatives when they help a real choice or can start independently. Explicit queue inspection may show additional eligible candidates. Report exclusions and their durations separately. If every otherwise eligible route is excluded, report that fact and offer broader inspection.

**Prerequisite and dependency protection**: skipping a route never unlocks its dependents. A true global prerequisite blocks every route it governs; a route-scoped prerequisite blocks only its dependents; an uncertain relationship is not silently promoted to a global blocker—ask for clarification if it changes which action is safe. Continue evaluating independent candidates. Never invent a lower-level alternative just to fill the slot.

### Step 0: discover the project's governance model

Unless the project sets another threshold, treat a task without progress for 7 days as stuck. Discover task, roadmap, artifact-norm, and glossary locations from project evidence; `auto` means no path is imposed in advance.

Resolve canonical artifact types and locations from the strongest project-local evidence available, in this order: explicit project configuration or agent entry point; the project's own artifact norms/indexes; existing linked governance artifacts and repository structure; AI Cortex defaults only when the project declares or clearly adopts them. Record the source and confidence. Existing artifacts in a coherent project-native structure are evidence of a valid local convention, not an omission merely because a conventional directory is absent.

Apply this discovery to the selected scope. The inventory dimensions below guide a project-wide scan; a focused run inspects only relevant records and the prerequisites needed to judge them.

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

- Eliminate actions with unmet prerequisites or dependencies, paused work without a resume decision, and actions outside the authorized scope. A necessary human decision may itself be recommended with its options and owner.
- Prefer eligible actions that resolve an evidenced blocker of the current work, then continue already selected or active work, then use the project's recorded priorities and precedence for other actions. Explain why the first action deserves attention now.
- For project-wide diagnosis, use the highest-priority goal's first relevant unfinished route as the starting candidate; a gap alone does not outrank a current action without an evidenced effect on progress.
- A **parallel route** (an independent node opened up by a blocked one) also goes into "Do now" when it can start immediately
- When a displayed route is excluded for the session or persistently, omit it and continue through the candidate sequence. A dependent or lower-level route still cannot displace it.
- Use default priority to build the queue and apply any conversation order adjustments before the display limit. Candidate lists are recomputed on each run. Blocked candidates are never promoted to executable candidates by ordering, exclusion, or display truncation.

**Parallel routing**: when the parallelism verdict is "parallel" or "converge", state the reason for parallelism or the convergence target explicitly in the routing evidence; when it is "focus", route only the current node. For genuinely tied choices, explain their respective benefits, costs and waiting conditions. Use source order, then exact route key for stable display only; do not invent a business rank. Conversation moves can reorder eligible choices, including differing urgency labels, while retaining dependencies, focus constraints and the underlying rationale.

**Sibling advance rule**: when a scan verifies that a node finished, advance to the next sibling at the same level in that reply. The traversal stops at the first gap of that next sibling.

**Multi-task, multi-card rendering rule**:

When several independently startable tasks help the current choice, render separate entries rather than merging them into one. Each entry covers one task with its own evidence and completion marker. Recommend one clear first action, adding up to two independent actions or meaningful alternatives under §3.1.

- ✅ Correct: 3 cards side by side, one task each (action name, TL;DR and completion marker all independent)
- ❌ Forbidden: merging several tasks into one card subject with a comma, a plus sign, or a verb like "start in parallel" (`T51 + T-SG5-002 start in parallel`)
- ❌ Forbidden: stacking several tasks' KPIs into one card's completion marker (`T51 dashboard reachable + T52 logs queryable + T-SG5-002 admin usable`)

For tasks that become ready tomorrow or later in the week, use the `defer` label + a TL;DR noting when they are ready; do not tuck them into a footnote on the current card.

#### 3.2 Governance urgency annotations

These annotations describe a finding's scope and severity. Apply the ordering rules above before rendering; artifact depth alone does not establish what the user should do first.

- **Now (P0)**: a foundational problem with evidence that it blocks all governed routes (or L1 has no goal and the project has no higher-authority alternative)
- **Next (P1)**: the L2 roadmap is missing or not aligned to a goal
- **Later (P2)**: a gap at any of L3-L5
- **Ignorable (P3)**: the remaining secondary findings

#### 3.3 Output format selection

Give each suggestion an action, reason, and observable completion marker. Use prose for one clear suggestion; use separate cards for parallel actions. Read [output guidance](references/output-guidance.md) when formatting a complex recommendation or checking terminology.

---

## Self-Check

Before reporting completion, run the [full self-check](references/self-check.md). Confirm that the current question and inspected scope are explicit, project paths came from evidence, relevant goals and siblings were assessed, blockers and exclusions are represented, and every recommendation has a completion marker. Project-wide diagnosis covers all applicable goals.

---

## Examples

Consult [worked examples](references/examples.md) when a routing case is ambiguous.

## Phase and milestone contract

Read the [Roadmap Spec](../../specs/roadmap-modeling.md) when diagnosing roadmap nodes.
A milestone is an event, so do not recursively require requirements, design and
tasks for that event itself. Diagnose underlying work through its related source
records. Route pending approval through the project's existing approval process;
a planned milestone introduces no universal gate. Treat legacy milestone task
directories as work packages and preserve their established archive route.

Self-check: concepts, selected views and linked evidence agree with the source records.

## Revision history maintenance

When diagnosing roadmap maintenance, inspect the [revision contract](../../specs/roadmap-modeling.md#54-revision-records)
and existing source decisions. A known material change after adoption without a
revision or a broken retained-history link recommends update-roadmap. Do not infer
missing earlier decisions from the current snapshot or treat history rows as
unfinished requirements, phases or milestone work. Dates in revision history do
not grant execution approval or define current item status.

Self-check: material changes are traceable, retained links resolve, and repeated execution adds no duplicate revision.

## Roadmap document family

Discover the main roadmap and linked delivery/iteration/version/history views from
project norms. They are one plan's projections, not duplicate requirement nodes.
Apply the Roadmap Spec and quality Rule through the diagnosis procedure. Route
structural/layout defects to define-roadmap, existing iteration/scope/date drift to
update-roadmap and tier decisions to promote-roadmap-items. Unselected iterations
or absent optional child documents are not gaps. Do not infer completion from an
iteration boundary or traverse revision history as current work.

Self-check: linked planning views and their source authority were checked without
creating duplicate work nodes or mandatory iteration artifacts.

## Scenario selection diagnosis

Read an existing roadmap combination and decision source as project evidence. Missing
new selection metadata in a legacy plan is not a gap. Invalid primary/view/layout
consistency routes to define-roadmap; changed needs suggest focused reconsideration,
not an automatic reset. Diagnosis recommends; it does not interview the user for all
four context dimensions, alter view choices or execute recommendation tools as approval.

Self-check: source-backed custom/legacy choices remain valid and new recipe availability
alone creates no governance work.

## Deliverable language

Before writing roadmap-chain deliverables, apply the [language contract](../../specs/roadmap-modeling.md#57-deliverable-language-schema-15).
Read the user instruction, consuming-project policy and existing artifact first;
retain a settled choice across handoffs. For a new artifact infer only from consistent
reader/document evidence; ask only unresolved gaps or winning-level conflicts.
Conversation language and English templates alone do not select artifact language.
Record the choice and source in existing norms/planning decisions; no new mandatory
configuration. Localize all new prose and display labels consistently while preserving
IDs, machine fields, canonical enums, source links and historical originals.

Diagnose language drift from source evidence without rewriting the roadmap. Preserve
the established artifact choice in suggested handoffs; conversational suggestions
follow the user language. Missing optional legacy metadata alone triggers no repair.

Self-check: language evidence and retained choice are explicit; all new display prose
is consistent, machine contracts are unchanged, and unavailable checks are reported.
