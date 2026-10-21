---
name: orchestrate-roadmap-planning
description: Orchestrate roadmap planning or first alignment of an existing project; route review findings to structural repair or authorized maintenance, preserve settled decisions and links during alignment, and run planning steps only within the requested scope.
version: 2.9.0
license: MIT
---

# Orchestrator Skill: Roadmap Planning

## Purpose

Chain the roadmap-related atomic skills in a fixed order to complete one roadmap planning ceremony. This skill orchestrates only; it performs no domain analysis. For a single step, call the corresponding atomic skill directly (`promote-roadmap-items` for promotion alone, `review-roadmap` for a health check alone).

**Its reason to exist is satisfying the downstream halt conditions up front.** A missing roadmap or strategic-goals document stops promotion; discovering that only at the final step forces a backtrack. This skill checks and fills preconditions like that before the call.

---

## Orchestrator Role

By the naming convention, an orchestrator skill **does exactly 4 things**:

1. **Detect the context**: call step 0 for its findings, then derive the mode and each step's run condition mechanically from them
2. **Chain the calls**: run the atomic skills in a fixed order
3. **halt-on-failure**: the tier decides the failure semantics (see below)
4. **Aggregate the output**: merge every step's output into a single report

**Forbidden**: assessing roadmap quality, deciding dependencies, setting priorities, or reimplementing the logic of any atomic skill inside this skill.

---

## Execution order (fixed)

Resolve intent before applying this planning table. An existing-project alignment
request selects the bounded `align-existing` branch below; the table's mandatory
strategy/promotion steps apply to planning, not to that branch. Preserve relative
order for any steps actually selected. Alignment is not implicit planning intent.

Every step carries a tier — a **mandatory** step runs when its condition is hit and cannot be skipped, a **default** step runs when its condition is hit but the user can skip it explicitly, a **recommended** step is only surfaced and never runs on its own.

| Step | Kind | Atomic skill | Tier | Run condition |
| --- | --- | --- | --- | --- |
| 0 | Health check | `review-roadmap` | mandatory | Always runs. Read-only, no side effects; its findings are the input to every condition below |
| 1 | Upstream | `design-strategic-goals` | mandatory | `strategic-goals.md` does not exist |
| 2 | Structure | `define-roadmap` | mandatory | No roadmap.md / invalid requirement, iteration, phase or milestone structure, selection consistency or document layout / strategic goals out of step with the roadmap |
| 3 | Intake | `capture-work-items` | default | Unregistered raw input exists |
| 4 | Priority decisions | `prioritize-backlog` | mandatory when all are unset or reassessment is explicitly requested; default when only some are | Items with `priority: unset` exist or explicit full reassessment is requested; use policy application or offered framework assessment, never implicit full reassessment |
| 5 | Dependencies | `map-item-dependencies` | default | Any candidate has missing/stale dependency or required-deliverable evidence, or a relevant dependency changed; even one candidate may need checking |
| 6 | Promotion | `promote-roadmap-items` | mandatory | Always runs; with no candidates it still emits the priority-ordered tier report |
| 7 | Maintenance | `update-roadmap` | recommended | The user has an explicit status, date or existing-version scope change in mind |
| 8 | Archiving | `archive-milestone` | recommended | A legacy work package meets its maturity conditions, or a phase/version/period snapshot is eligible under project archive policy or explicit target selection |

A step whose condition does not match is skipped; the final report names which steps were skipped and why.

**The tiers are not adjustable at will**. The three tiers are a mechanical mapping of constraints the atomic skills already carry, not a domain judgement made here:

- Steps 1 and 2 are mandatory because a missing `strategic-goals.md` and a missing roadmap.md are all halt conditions `promote-roadmap-items` states outright; leave them unfilled and the chain never reaches the end
- The double tier on step 4 mirrors promote's two behaviors: it halts on "all unset" and merely skips those items on "some unset"
- Step 5 reuses sufficient current evidence rather than rerunning mapping by candidate count. One candidate may depend on existing items, another team or an external service; default tier permits explicit skipping, not an inferred readiness pass
- Step 8 is recommended because `archive-milestone` removes a directory — a destructive operation — and its own `apply` defaults to `false` (dry-run)

**Step 5 must come before step 6** when triggered: promotion consumes dependency
and next-step deliverable evidence. Pass the checked/unchecked distinction; a
skipped check does not establish readiness. Known cycles remain unresolved and
cannot become executable candidates through an orchestration downgrade.

---

## Behavior

### Step 1: detect the context

**Intent precedence: first alignment.** When the user requests first adoption or
alignment of an existing project's requirements/roadmap without replanning, select
`align-existing` before bootstrap/refresh/intake/maintain. Pass that intent through
review and repair. Discover the actual plan, source authority and stable locations;
if they cannot be found, report the location gap rather than bootstrap a new plan.

Run step 0 (`review-roadmap`), then route only its classified findings:

| Finding in alignment scope | Action |
| --- | --- |
| Needed structure/presentation repair | Step 2 `define-roadmap` in alignment mode, preserving known decisions and links |
| Existing requirement-body alignment explicitly in scope | Read-only `review-requirements`; route evidence-grounded draft repair to `orchestrate-repair-requirements-loop`, preserving its lifecycle and authorization guards |
| Existing structure adequate; separately requested, source-backed state/time correction | Step 7 `update-roadmap` for that correction only |
| Missing/conflicting source facts, policy/goal evidence, or unmapped requirement parent | Retain the gap and propose the responsible follow-up; do not invent or write business facts |
| Priority/tier/scope/commitment change proposed by diagnosis alone | Report as separate business decision; do not execute |
| No repair or separately authorized maintenance needed | Emit a no-write report with remaining limitations, if any |

After any repair/maintenance, re-run `review-roadmap` and compare the preserved
business facts and links. Report unresolved criteria instead of a full pass; do not
loop automatically until evidence is fabricated. Repeated alignment with no new
gap makes no change. This branch skips steps 1, 3–6 and 8 unless the user separately
authorizes the corresponding work. Missing strategy, unset priorities, unregistered
intake and unpromoted items alone do not expand alignment into those steps. Explicit
mixed requests are separated into alignment and the authorized planning/maintenance
actions; carry the intent and preservation boundary to every atomic call.

Requirement-body routing is a conditional alignment subflow, not backlog intake.
Do not recapture existing requirements, reset their priorities, or edit frozen
approved/implemented/superseded originals. A missing successor authorization or
business fact remains a limitation; do not create a new draft ID or approve it
merely to make alignment pass. Requirement review/repair owns that assessment.

The normal planning modes below remain unchanged for actual planning requests.

Run `review-roadmap` for its findings and map them mechanically to a mode with the table below. When several signatures match at once, take the one earlier in the table, because an earlier mode corresponds to a gap further upstream.

| mode | findings signature | Effect |
| --- | --- | --- |
| `bootstrap` | roadmap.md or strategic-goals.md missing | Steps 1 and 2 will run |
| `refresh` | Invalid requirement/defect entry structure, iteration/document layout or selection consistency, phase scope/exit condition or milestone identity/relations/criterion / strategic goals out of step with the roadmap | Step 2 will run; step 6 re-evaluates tier placement by priority and readiness |
| `intake` | Priority-set items not yet promoted or explicit priority reassessment intent | Main path 3→4→5→6 |
| `maintain` | No unpromoted priority-set items, but at-risk / blocked / overdue items, iteration goal/scope/cadence drift, main/detail inconsistency, phase/event timing conflicts, unsupported event states, missing post-adoption revision evidence/broken history links or explicit maintenance intent exist | Step 7 rises from recommended to a default prompt |
| `healthy` | No unresolved roadmap findings and no explicit reassessment or maintenance intent | Emit the health-check report and end normally; no write operation runs |

`review-roadmap` does not emit a mode itself — it emits findings only, and the mapping happens at this layer.

A concise roadmap is not incomplete merely because it omits stage hypotheses or
metric tables. Only requirements and defects enter promotion; task-level input resolves
to its parent. Keep aggregated evidence in the report, not in roadmap rows.
Version groups and schedule milestones are valid selected views, not invalid
requirement rows. Route scope/date changes to maintenance and view-structure changes
to definition. Preserve selected views and destination; an unchanged destination
does not need repeated confirmation. An explicit full-reassessment request routes
to `prioritize-backlog` even when no priorities are unset; pass that intent through.

Unresolved phase/event findings cannot fall through to `healthy`. Structural
findings choose `refresh`; existing timing/state/evidence discrepancies choose
`maintain`. Missing occurrence evidence blocks claiming an event reached; maintenance
must obtain evidence or retain/report the unresolved state, never invent a receipt.
If review reports another finding not mapped above, report it as unresolved and
stop for diagnosis rather than declare the roadmap healthy.

### Step 2: chain the calls

Call in the order of the table above, collecting each step's output. Before a call, go through that step's preconditions and fill what can be filled, to avoid a downstream halt and a backtrack.

**Archive target for step 8**: for legacy directory-backed work packages resolve `milestone_slug`
from project records, never guess it. For a phase/version/period snapshot pass the selected
phase/version/period identity and its existing source references. With several candidates,
obtain the user's selection; unavailable identity means skip and report the limitation.

### Step 3: halt-on-failure

The tier decides the failure semantics. This is a deliberate divergence from the single halt rule in `orchestrate-code-review` — there the atomic skills are independent of one another, here the steps carry data dependencies, and one blanket rule would cut short a flow that could have continued:

| Tier | On failure |
| --- | --- |
| mandatory | Terminate the orchestration; emit what completed plus the failure explanation |
| default | Record it and continue. If a later step depends on its output (step 5 for step 6's dependency guardrail, say), that later step drops to recommended and the report states that the guardrail did not take effect |
| recommended | Not running it does not count as a failure |

**The special halt in step 1**: if the user rejects the candidate goals `design-strategic-goals` produces in fallback mode, this layer does not walk back level by level to fill in the vision / North Star — that is the job of `plan-next`'s goal tree traversal. Then halt and prompt to run `plan-next` first to establish the strategy layer.

### Step 4: aggregate the output

A single report, containing:

- A summary of each step's result
- The skipped steps and the reason for each
- The roadmap change list (added / promoted / demoted / status changed)
- The priority-ordered tier report when step 6 ran; alignment instead reports repaired structure, preserved decisions/links, and post-repair findings
- Unresolved findings (those from step 0 that this round did not handle)
- Suggestions for the next step

---

## Input & Output

**Input**: an optional scope hint and any unregistered raw input; governance document paths are discovered automatically from the project norms.

**Output**: a single aggregated report (see above).

---

## Restrictions

### Hard Boundaries

- Do not assess roadmap quality, decide dependencies, or set priorities inside this skill
- Do not change the execution order; above all, step 5 must not be placed after step 6
- Do not adjust grades within a branch; alignment skips out-of-scope planning steps by the explicit intent contract, not by waiving their preconditions
- Do not confirm on the user's behalf: the item-by-item confirmation each atomic skill asks for goes ahead as usual, and the orchestration layer does not approve in bulk
- Do not call `plan-next` or `orchestrate-governance-step` in reverse, to avoid a call cycle
- Do not reimplement `plan-next`'s goal tree traversal

### Orthogonal boundary against the existing orchestration layers

| Skill | Coverage | Behavior | Relationship |
| --- | --- | --- | --- |
| `plan-next` | Cross-layer diagnosis | Traverses the goal tree into a routing suggestion; explicit preference changes affect only its exclusion file | This skill must not reimplement the traversal; it may read that state |
| `orchestrate-governance-step` | Cross-layer, executes 1 suggestion | Generic single-step executor | May call this skill as one executable action |
| `orchestrate-roadmap-planning` | The roadmap vertical slice only | Runs the fixed sequence end to end | Must not call either of the two above in reverse |

In one line: `plan-next` answers "what the whole project does next", this skill answers "the roadmap line, from strategy through promotion, in a single pass".

### Skill Boundaries

**Not done inside the orchestrator skill** (the atomic sub-skills carry it): roadmap assessment → `review-roadmap`; structure definition → `define-roadmap`; scoring → `prioritize-backlog`; dependencies → `map-item-dependencies`; promotion → `promote-roadmap-items`; status and dates → `update-roadmap`; archiving → `archive-milestone`.

---

## Self-Check

- [ ] Does only the 4 things: "detect the context / chain the calls / halt-on-failure / aggregate the output"
- [ ] No domain judgement logic was implemented inside this skill
- [ ] Intent selects alignment versus planning first; within that branch, review findings determine actions without independent roadmap assessment
- [ ] Selected planning steps retain order, with step 5 ahead of step 6; alignment additionally re-runs read-only review after repair
- [ ] Skipped steps carry their reason in the report
- [ ] Failure semantics follow the tier; when a default step fails, the report states whether the downstream guardrail is void
- [ ] The archive target for step 8 has a definite source and was not guessed
- [ ] The report carries priority order and unresolved findings
- [ ] Alignment intent was resolved before normal planning routes; no skipped strategy/intake/scoring/promotion/archive action ran implicitly, and post-repair review checked preservation

---

## Examples

### Example 1: pulling in newly prioritized items (mainstream case)

- **Context**: `review-roadmap` findings show a complete structure, but 3 scored items are unpromoted → mode = `intake`
- **Schedule**: step 0 → skip 1 and 2 (governance documents complete) → skip 3 (no unregistered input) → skip 4 (no unset items) → step 5 (dependency evidence needs checking) → step 6 → skip 7 and 8
- **Step 5 output**: 1 candidate has an unresolved prerequisite and is marked as not admissible to Now
- **Step 6**: the other 2 are promoted to Now; the blocked one goes to Next
- **Aggregation**: priority-ordered tier report + change list + a suggestion to run `capture-work-items` on the newly promoted Now items

### Example 2: cold start on a new project (edge case)

- **Context**: `docs/` holds nothing but README → findings show roadmap.md and strategic-goals.md are both missing → mode = `bootstrap`
- **Schedule**: step 0 → step 1 (`design-strategic-goals` detects missing upstream context and derives fallback goals from repository evidence) → step 2 → step 3 → step 4 → step 5 if dependency evidence is missing or stale, otherwise reuse it → step 6
- **Key point**: the orchestration layer does **not** call `define-vision` just because the vision is missing. Whether the upstream is complete, and whether to run in normal or fallback mode, is `design-strategic-goals`'s own call
- **If the user rejects the fallback candidates**: halt, prompt to run `plan-next` first to establish the strategy layer, and emit the completed step 0 health-check report

### Example 3: downgrade after the dependency step fails (edge case)

- **Context**: mode = `intake`, 5 promotion candidates
- **Step 5 fails**: `map-item-dependencies` detects a dependency cycle and halts
- **Handling**: step 5 sits at the **default** tier, so the orchestration is not terminated; record the failure and carry on
- **Step 6 downgraded**: report the missing verified dependency result before any recommended comparison. Known cyclic candidates remain unresolved; downgrading never authorizes them into Now. Independently verified candidates may still be compared under the atomic skill's rules.
- **Aggregated report**: retain the cycle `#12 → #19 → #25 → #12`, affected candidates and the limitation. Suggest resolving the cycle before reconsidering those candidates; do not describe them as unchecked but executable.

## Phase and milestone contract

Apply the [Roadmap Spec](../../specs/roadmap-modeling.md) across component outputs.
Creation of phase/event objects belongs to define-roadmap; existing dates and
source-backed event states belong to update-roadmap; structural/evidence findings
belong to review-roadmap. Scoring and promotion operate on requirements/defects.
Archive completed work packages or snapshots without deleting event evidence;
legacy milestone directories do not define a mandatory roadmap hierarchy.

Self-check: concepts, selected views and linked evidence agree with the source records.

## Revision history maintenance

Carry the selected durable history source and decision identity across definition,
promotion and maintenance under the [revision contract](../../specs/roadmap-modeling.md#54-revision-records).
A known post-adoption material change with missing/dropped revision evidence routes
to maintain; an unknown pre-adoption history does not force reconstruction. Do not
let unresolved history findings fall through to healthy. One coherent decision
shared across component skills is recorded once, not once per step. Archive
verification includes retained history links.

Self-check: material changes are traceable, retained links resolve, and repeated execution adds no duplicate revision.

## Iteration and layout routing

Pass established cadence, selected views, single/split layout, source ownership and
related document paths to atomic skills. Review findings about iteration identity,
missing structural fields or unreadable main/detail layout select refresh; existing
iteration scope/timebox/cadence and projection drift select maintain. Unmapped findings
remain unresolved. The orchestrator does not design iterations, expand layout or infer
release from an iteration boundary. Period archives retain carry-over through step 8.

Self-check: atomic findings determine layout/iteration routing and no unresolved
cross-document drift falls through to healthy.

## Scenario handoff

Pass known context, selection source, primary perspective, enabled views, layout and
destination to atomic skills. Bootstrap/refresh delegates information gathering and
recommendation to define-roadmap; do not run another interview here. Existing choices
win during ordinary maintenance. Route review findings about invalid choice structure
or primary/view conflicts to refresh; changed context with a consistent existing
choice is an unresolved reconsideration suggestion, never automatic replacement.
A recipe mismatch alone is not a finding and new features do not force migration.

Self-check: selection evidence survives every handoff and no proposed default silently
replaces a team choice; unmapped findings remain explicit.

## Deliverable language

Before writing roadmap-chain deliverables, apply the [language contract](../../specs/roadmap-modeling.md#57-deliverable-language-schema-15).
Read the user instruction, consuming-project policy and existing artifact first;
retain a settled choice across handoffs. For a new artifact infer only from consistent
reader/document evidence; ask only unresolved gaps or winning-level conflicts.
Conversation language and English templates alone do not select artifact language.
Record the choice and source in existing norms/planning decisions; no new mandatory
configuration. Localize all new prose and display labels consistently while preserving
IDs, machine fields, canonical enums, source links and historical originals.

Pass locale, basis and source to every atomic step alongside view choices. Delegate
resolution to the writing skill; run no duplicate interview here. Unresolved language
findings cannot fall through to healthy; report or route them to the appropriate
writer without translating source evidence in the orchestrator.

Self-check: language evidence and retained choice are explicit; all new display prose
is consistent, machine contracts are unchanged, and unavailable checks are reported.
