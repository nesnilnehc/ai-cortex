---
name: plan-next
description: Recommend next actions from the current problem, prior decisions and project evidence. Compare options, prepare a focused skill handoff, and inspect independent project work when the current focus has no eligible action.
version: 17.2.0
license: MIT
---

# Skill: Plan Next

> **Role**: evidence-led governance router
> **WHAT**: establish the current decision → inspect relevant project evidence → compare eligible actions → prepare the next skill handoff
> **HOW**: read-only diagnosis on ordinary runs; an explicit persistent skip or restore may update only the project preference file. For a single-dimension problem (only a known omission to check), recommend the dedicated skill directly (`define-*` and the like)
> **Distinct from**: this skill never executes downstream skills or changes governance state; document health checks are run by the runtime / linter / CI tooling per `rules/doc-health-criteria.md`

---

## Purpose and Boundaries

Help the user choose and enter the next useful action. Carry forward their current problem, settled decisions and authorization, check relevant evidence, and explain the available choices. Use project-wide diagnosis when requested, when no current context exists, or when an implicit current focus has no eligible action.

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

Read the request and relevant conversation before selecting sources. Identify the project, current work, intended result, settled decisions, unresolved choices and existing authorization. A bare invocation starts with identifiable current work; this is an initial focus, not a user-imposed scope limit. An explicit project-wide request overrides that default; absent usable context, diagnose the whole project. Preserve an explicit scope limit from the user or caller, including a still-effective limit from earlier conversation. Ask only when the project or an explicit boundary is genuinely ambiguous.

Inspect the current item's records, relevant decisions, dependencies and acceptance evidence first, then trace upstream or outward where those facts affect the choice. For a project-wide request, identify what the owner is trying to decide or achieve now from the active goal, latest decisions, and relevant evidence of delivery or user outcomes. Use that context to evaluate the work items. Project-wide diagnosis still inventories all applicable goals and siblings. State the actual scope and material limits in the result.

**When the current focus has no eligible action**: after checking its evidence and preferences, if it is finished, externally waiting, blocked, or exhausted (including all eligible recommendations being excluded), continue read-only project-wide diagnosis in the same reply unless an explicit scope limit applies. Inspect the project's authoritative active-work sources, all applicable goals and siblings, and candidate source records. Look for independent work that can start now; do not ask permission merely to expand this read-only inspection. State the initial focus, why inspection expanded, actual coverage and limitations. A wait on one item is not a project-wide stop condition.

Expansion grants no implementation, authenticated-access or external-write permission. Use only sources accessible under existing authorization; disclose unavailable sources. Preserve priorities, exclusions, unmet dependencies and applicable global gates. Never resume paused or cancelled work without an explicit decision. Uncertain independence stays uncertain. Do not invent actions to fill the list or repeatedly recommend commit, push, synchronization or cleanup after their completion; compare remaining delivery and product work under existing priorities. Recommend such closeout work only when evidence shows a remaining obligation or prerequisite.

With an explicit limit, report local exhaustion and the remaining condition; offer broader inspection without performing it. Without one, report project-wide exhaustion only after sufficient project inspection. If evidence is insufficient, disclose coverage and use `needs_input` when the missing fact changes the safe next action. All-excluded or truly waiting projects retain their conditions under `no_applicable_action`; an empty list never proves completion.

Distinguish a user's decision from a verified project state. A decision to pause work governs recommendations in this conversation; it does not itself update the source record. Verify a reported completion before relying on it for dependency readiness or closure. If source evidence conflicts with a current user decision, retain both, explain the effect and suggest record alignment when needed. Never silently discard the decision or assert an unverified transition.

Missing documents, conflicting thresholds and unmeasured metrics become first actions only when they materially affect the current choice or safe progress. State that causal link. Otherwise retain them as background findings. A verified prerequisite still blocks every route within its declared scope.

### Adjust the recommendation queue

After rendering suggestions in a user-facing conversation, accept relevant follow-up replies as part of `plan-next` without requiring another invocation. Interpret commands in the user's language. On each relevant reply, resolve any selector against the last result, rescan, apply the valid adjustment, and return the updated result in the same reply. Keep the latest result, skip set, and order adjustments scoped to this project in this conversation.

| Reply | Effect |
| --- | --- |
| “2” or “Choose 2” in response to the displayed options | Select the action at that position. Revalidate its exact route and prepare its handoff if it is still eligible. |
| “Next recommendation” or “next” while reviewing the queue | Skip the first displayed recommendation for this conversation and return the revised queue. If none is displayed, refresh and report the result without recording a skip. |
| “Skip 2 for this conversation” or “keep this recommendation hidden until I restore it” | Apply the existing skip rules below to the exact target and chosen duration. |
| “Show the dashboard recommendation again” | Apply the existing restore rules and return the revised queue. |
| “Put 2 first” or “move the audit log before the dashboard” | Move one eligible recommendation to the front or before another eligible recommendation for this conversation. |
| “Reset recommendation order” | Clear the conversation's order adjustments and return to the current default order. Keep skip choices. |
| “Show the queue” | Show the eligible recommendations beyond the usual display limit as well. |
| “Refresh” or a report that an action was completed | Recheck current evidence and advance where it supports doing so. Use the project's normal completion criteria. |
| “That is not the main problem” or a correction of the intended outcome | Revisit the current question and recommendation rationale, retain valid decisions, and rebuild candidates before proposing another action. |

For a move, resolve both items, when applicable, to exact route keys before rescanning. Apply the move to the fresh queue after exclusions. Retain the order of the other entries. Record each valid move in conversation order and replay it on refresh. Drop a move whose target or reference is no longer eligible or has been excluded, and report which move was dropped. A move that already matches the requested order needs no additional entry. Ranking preferences apply only to eligible candidates and respect the existing focus and dependency rules. A new conversation starts with the default order.

Use the latest **Do now** positions for unqualified numbers. When the user opens the queue, also accept a unique name from its extra entries. If a selector is ambiguous, ask only for the affected item. Resolve a selection to its exact route key before rescanning. If that route is no longer eligible, explain what changed and return the current options or remaining condition. If the route is still eligible, hand off that route even if its display position changed. Conclude the recommendation interaction after a successful selection or when the user ends queue review.

Explain a reordered list as the user's conversation preference and retain each action's underlying priority rationale. If the current scope is exhausted or all eligible actions are skipped, apply the scope-expansion rule above before returning the revised result. Preserve exclusions across the expanded scan. Only an explicit scope limit requires the user to choose broader inspection. Selection produces a focused handoff naming the skill or existing project workflow, objective, target, source evidence and completion marker. Carry authorization and unresolved decisions through it; selecting a recommendation grants no additional implementation or external-write permission. Downstream execution belongs to the selected workflow or outer executor.

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
2. Build the complete ordered sequence of currently eligible recommendation candidates before applying preferences or the normal display limit. Assess [prerequisites for the specific action](references/diagnosis.md#20-applicability-and-prerequisite-assessment) and assign each eligible candidate its exact `(route, target)` key.
3. Read `.ai-cortex/plan-next.yaml` when present; combine its exact route keys with the current conversation's skip set. After resolving the displayed action and duration, re-scan before changing either scope. If that exact candidate is no longer eligible or its route key changed, do not save a stale skip; explain the change and offer the current recommendations. For a restore, validate the file and remove the selected key from every active scope before recommending again.
4. Omit matching keys, then apply valid conversation order adjustments. Never treat an exclusion or move as a completion, a blocked node, or permission to traverse beneath it. A candidate that depends on unfinished work represented by an excluded route, an unfinished ancestor, or a global prerequisite remains ineligible.
5. Recommend the first remaining eligible candidate and use §3.3 to show the available choices. Explicit queue inspection may show additional eligible candidates. Report exclusions and their durations separately. If no candidate remains, apply the scope-expansion rule before assigning the final state: expand an implicit focus read-only, or retain an explicit limit and offer broader inspection. Preserve exclusions throughout.

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

Read the [diagnosis procedure](references/diagnosis.md) before assessing goal, roadmap, requirements, design, tasks, drift, and hygiene. Apply its [roadmap-family checks](references/diagnosis.md#roadmap-family-diagnosis) when inspecting roadmap nodes. Use verified prerequisites and status evidence before ranking candidates or reporting completion.

### Step 3: Recommend — routing generation and tiering

**Source**: consumes the output of step 2 (see "Outputs of the Diagnose step"). Keep the candidate sequence separate from its visible projection: diagnosis first; preference filtering only after eligibility and ranking.

#### 3.1 Tiering decision

Use the traversal and independent drift/hygiene results to build the complete ordered sequence of eligible candidates. Apply preferences before the display rules in §3.3.

- Eliminate actions with unmet prerequisites or dependencies, paused or cancelled work without an explicit resume decision, and actions outside an explicit diagnostic scope limit. Inspect evidence only within existing access authorization. An eligible action may be recommended for its owner even when the caller lacks execution permission. State the owner and required authorization in the handoff for the executor to check separately. A necessary human decision may itself be recommended with its options and owner.
- Prefer eligible actions that directly advance the current decision or resolve an evidenced blocker of the current work, then continue already selected or active work, then use the project's recorded priorities and precedence for other actions. During a wait, check whether an allowed action can supply evidence the next decision needs. If the evidence is already ready or can only arrive later, state that wait for the decision and keep any independent work separate. Explain why the first action deserves attention now and cite the evidence for any departure from the recorded order. A recommendation leaves the roadmap tier and priority intact.
- For project-wide diagnosis, use the highest-priority goal's first relevant unfinished route as the starting candidate; a gap alone does not outrank a current action without an evidenced effect on progress.
- A parallel action enters the eligible queue when it can start independently of the blocked work.
- When a displayed route is excluded for the session or persistently, omit it and continue through the candidate sequence. A dependent or lower-level route still cannot displace it.
- Use default priority to build the queue and apply any conversation order adjustments before the display limit. Candidate lists are recomputed on each run. Blocked candidates are never promoted to executable candidates by ordering, exclusion, or display truncation.

**Parallel routing**: when the parallelism verdict is "parallel" or "converge", state the reason for parallelism or the convergence target explicitly in the routing evidence; when it is "focus", route only the current node. For genuinely tied choices, explain their respective benefits, costs and waiting conditions. Use source order, then exact route key for stable display only; do not invent a business rank. Conversation moves can reorder eligible choices, including differing urgency labels, while retaining dependencies, focus constraints and the underlying rationale.

**Sibling advance rule**: when a scan verifies that a node finished, advance to the next sibling at the same level in that reply. An unmet dependency or external wait at that gap does not stop inspection of other independent siblings or goals under the scope-expansion rule.

Keep waiting actions out of the eligible queue. Record their remaining conditions and exact time and timezone when known, and continue checking independent work.

#### 3.2 Governance urgency annotations

These annotations describe a finding's scope and severity. Apply the ordering rules above before rendering; artifact depth alone does not establish what the user should do first.

- **Now (P0)**: a foundational problem with evidence that it blocks all governed routes (or L1 has no goal and the project has no higher-authority alternative)
- **Next (P1)**: the L2 roadmap is missing or not aligned to a goal
- **Later (P2)**: a gap at any of L3-L5
- **Ignorable (P3)**: the remaining secondary findings

#### 3.3 Output format selection

For project-wide conversations, use two short sections with headings. Briefly connect what changed to the current goal, then summarize pending work in bullets. In **Do now**, show up to three eligible actions in order and make multiple actions selectable by number. Keep a single recommendation concise. Focused replies use only the inspected scope. Follow the [output guidance](references/output-guidance.md) for presentation, caller output and handoffs.

---

## Self-Check

Before reporting completion, run the [full self-check](references/self-check.md). Confirm that the current question and inspected scope are explicit, project paths came from evidence, relevant goals and siblings were assessed, blockers and exclusions are represented, and every recommendation has a completion marker. Project-wide diagnosis covers all applicable goals.

---

## Examples

Consult [worked examples](references/examples.md) when a routing case is ambiguous.
