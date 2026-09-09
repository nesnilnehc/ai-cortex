---
name: orchestrate-roadmap-planning
description: Orchestrator skill — run one roadmap planning pass by sequencing atomic skills from strategic goals through capture, scoring, dependency mapping, and promotion, satisfying each skill's halt conditions up front.
description_zh: 编排技能——按固定顺序串联从战略目标到晋升的原子技能，跑完一轮 roadmap planning；核心价值是提前满足各原子技能的 halt 条件。
tags: [planning, orchestration]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [roadmap planning, plan the roadmap, roadmap ceremony, orchestrate roadmap]
input_schema:
  type: free-form
  description: Optional scope hint and any unregistered raw input; auto-discovers governance docs from project norms
output_schema:
  type: chat
  description: Aggregated report — steps executed, steps skipped with reasons, roadmap changes, capacity usage, and next actions
---

# Orchestrator Skill: Roadmap Planning

## Purpose

Chain the roadmap-related atomic skills in a fixed order to complete one roadmap planning ceremony. This skill orchestrates only; it performs no domain analysis. For a single step, call the corresponding atomic skill directly (`promote-roadmap-items` for promotion alone, `review-roadmap` for a health check alone).

**Its reason to exist is satisfying the downstream halt conditions up front.** The most common waste in calling by hand: you get all the way to `promote-roadmap-items` before finding the roadmap has no capacity allocation, halt, go back and run `define-roadmap`, and start over — a backtrack that example 2 of promote writes up as the normal flow. This skill checks and fills preconditions like that before the call.

---

## Orchestrator Role

By the naming convention, an orchestrator skill **does exactly 4 things**:

1. **Detect the context**: call step 0 for its findings, then derive the mode and each step's run condition mechanically from them
2. **Chain the calls**: run the atomic skills in a fixed order
3. **halt-on-failure**: the tier decides the failure semantics (see below)
4. **Aggregate the output**: merge every step's output into a single report

**Forbidden**: assessing roadmap quality, computing capacity, deciding dependencies, setting priorities, or reimplementing the logic of any atomic skill inside this skill.

---

## Execution order (fixed)

Every step carries a tier — a **mandatory** step runs when its condition is hit and cannot be skipped, a **default** step runs when its condition is hit but the user can skip it explicitly, a **recommended** step is only surfaced and never runs on its own.

| Step | Kind | Atomic skill | Tier | Run condition |
|---|---|---|---|---|
| 0 | Health check | `review-roadmap` | mandatory | Always runs. Read-only, no side effects; its findings are the input to every condition below |
| 1 | Upstream | `design-strategic-goals` | mandatory | `strategic-goals.md` does not exist |
| 2 | Structure | `define-roadmap` | mandatory | No roadmap.md / no total capacity baseline / no capacity allocation / percentages do not sum to 100% |
| 3 | Intake | `capture-work-items` | default | Unregistered raw input exists |
| 4 | Scoring | `prioritize-backlog` | mandatory when all are unset; default when only some are | Items with `priority: unset` exist |
| 5 | Dependencies | `map-item-dependencies` | default | Promotion candidates ≥ 2 |
| 6 | Promotion | `promote-roadmap-items` | mandatory | Always runs; with no candidates it still emits the capacity usage report |
| 7 | Maintenance | `update-roadmap` | recommended | The user has an explicit status change / date shift in mind |
| 8 | Archiving | `archive-milestone` | recommended | A completed milestone that has matured enough exists |

A step whose condition does not match is skipped; the final report names which steps were skipped and why.

**The tiers are not adjustable at will**. The three tiers are a mechanical mapping of constraints the atomic skills already carry, not a domain judgement made here:

- Steps 1 and 2 are mandatory because a missing `strategic-goals.md`, a missing roadmap.md, and a missing capacity allocation are all halt conditions `promote-roadmap-items` states outright; leave them unfilled and the chain never reaches the end
- The double tier on step 4 mirrors promote's two behaviors: it halts on "all unset" and merely skips those items on "some unset"
- Step 5 is default rather than mandatory because dependency analysis is meaningless with candidates < 2
- Step 8 is recommended because `archive-milestone` removes a directory — a destructive operation — and its own `apply` defaults to `false` (dry-run)

**Step 5 must come before step 6**, one of the core reasons this orchestration exists: promote's Now-tier admission reads `depends_on`, and promoting before the dependencies are registered pulls blocked items into Now, where they hold capacity and produce nothing.

---

## Behavior

### Step 1: detect the context

Run `review-roadmap` for its findings and map them mechanically to a mode with the table below. When several signatures match at once, take the one earlier in the table, because an earlier mode corresponds to a gap further upstream.

| mode | findings signature | Effect |
|---|---|---|
| `bootstrap` | roadmap.md or strategic-goals.md missing | Steps 1 and 2 will run |
| `refresh` | No capacity baseline / no capacity allocation / percentages do not sum to 100% / strategic goals out of step with the roadmap | Step 2 will run; step 6 deals with the over-allocation first |
| `intake` | Scored items not yet promoted, with capacity left | Main path 3→4→5→6 |
| `maintain` | No capacity gap, but at-risk / blocked / overdue items exist | Step 7 rises from recommended to a default prompt |
| `healthy` | None of the findings above | Emit the health-check report and end normally; no write operation runs |

`review-roadmap` does not emit a mode itself — it emits findings only, and the mapping happens at this layer.

### Step 2: chain the calls

Call in the order of the table above, collecting each step's output. Before a call, go through that step's preconditions and fill what can be filled, to avoid a downstream halt and a backtrack.

**`milestone_slug` for step 8**: `archive-milestone` takes structured input in which `milestone_slug` is required, and this layer must supply it. The value comes from scanning the directories under `docs/process-management/milestones/` other than `_archive/` and comparing them with the completed stages in roadmap.md. With several candidates, prompt for them one at a time, never in bulk; when it cannot be determined, skip the step and say so in the report — **do not guess the slug**.

### Step 3: halt-on-failure

The tier decides the failure semantics. This is a deliberate divergence from the single halt rule in `orchestrate-code-review` — there the atomic skills are independent of one another, here the steps carry data dependencies, and one blanket rule would cut short a flow that could have continued:

| Tier | On failure |
|---|---|
| mandatory | Terminate the orchestration; emit what completed plus the failure explanation |
| default | Record it and continue. If a later step depends on its output (step 5 for step 6's dependency guardrail, say), that later step drops to recommended and the report states that the guardrail did not take effect |
| recommended | Not running it does not count as a failure |

**The special halt in step 1**: if the user rejects the candidate goals `design-strategic-goals` produces in fallback mode, this layer does not walk back level by level to fill in the vision / North Star — that is the job of `plan-next`'s goal tree traversal. Then halt and prompt to run `plan-next` first to establish the strategy layer.

### Step 4: aggregate the output

A single report, containing:

- A summary of each step's result
- The skipped steps and the reason for each
- The roadmap change list (added / promoted / demoted / status changed)
- The capacity usage report (from step 6)
- Unresolved findings (those from step 0 that this round did not handle)
- Suggestions for the next step

---

## Input & Output

**Input**: an optional scope hint and any unregistered raw input; governance document paths are discovered automatically from the project norms.

**Output**: a single aggregated report (see above).

---

## Restrictions

### Hard Boundaries

- Do not assess roadmap quality, compute capacity, decide dependencies, or set priorities inside this skill
- Do not change the execution order; above all, step 5 must not be placed after step 6
- Do not adjust the tiers; they follow from constraints the atomic skills already carry
- Do not confirm on the user's behalf: the item-by-item confirmation each atomic skill asks for goes ahead as usual, and the orchestration layer does not approve in bulk
- Do not call `plan-next` or `orchestrate-governance-step` in reverse, to avoid a call cycle
- Do not reimplement `plan-next`'s goal tree traversal

### Orthogonal boundary against the existing orchestration layers

| Skill | Coverage | Behavior | Relationship |
|---|---|---|---|
| `plan-next` | Cross-layer, read-only | Traverses the goal tree into a routing suggestion | This skill must not reimplement the traversal; it may read that state |
| `orchestrate-governance-step` | Cross-layer, executes 1 suggestion | Generic single-step executor | May call this skill as one executable action |
| `orchestrate-roadmap-planning` | The roadmap vertical slice only | Runs the fixed sequence end to end | Must not call either of the two above in reverse |

In one line: `plan-next` answers "what the whole project does next", this skill answers "the roadmap line, from strategy through promotion, in a single pass".

### Skill Boundaries

**Not done inside the orchestrator skill** (the atomic sub-skills carry it): roadmap assessment → `review-roadmap`; structure definition → `define-roadmap`; scoring → `prioritize-backlog`; dependencies → `map-item-dependencies`; promotion → `promote-roadmap-items`; status and dates → `update-roadmap`; archiving → `archive-milestone`.

---

## Self-Check

- [ ] Does only the 4 things: "detect the context / chain the calls / halt-on-failure / aggregate the output"
- [ ] No domain judgement logic was implemented inside this skill
- [ ] The mode is derived mechanically from step 0's findings; the roadmap was not assessed here
- [ ] The execution order is fixed, with step 5 ahead of step 6
- [ ] Skipped steps carry their reason in the report
- [ ] Failure semantics follow the tier; when a default step fails, the report states whether the downstream guardrail is void
- [ ] `milestone_slug` for step 8 has a definite source and was not guessed
- [ ] The report carries capacity usage and unresolved findings

---

## Examples

### Example 1: pulling in new items after capacity frees up (mainstream case)

- **Context**: `review-roadmap` findings show a complete structure with full capacity allocation, but 3 scored items are unpromoted and the Now tier has capacity left → mode = `intake`
- **Schedule**: step 0 → skip 1 and 2 (governance documents complete) → skip 3 (no unregistered input) → skip 4 (no unset items) → step 5 (3 candidates ≥ 2) → step 6 → skip 7 and 8
- **Step 5 output**: 1 candidate has an unresolved prerequisite and is marked as not admissible to Now
- **Step 6**: the other 2 are promoted to Now; the blocked one goes to Next
- **Aggregation**: capacity report + change list + a suggestion to run `capture-work-items` on the newly promoted Now items

### Example 2: cold start on a new project (edge case)

- **Context**: `docs/` holds nothing but README → findings show roadmap.md and strategic-goals.md are both missing → mode = `bootstrap`
- **Schedule**: step 0 → step 1 (`design-strategic-goals` detects the vision and North Star are missing too, switches to fallback mode on its own, and works candidate goals back from evidence in the repository) → step 2 → step 3 → step 4 → skip 5 (candidates < 2) → step 6
- **Key point**: the orchestration layer does **not** call `define-vision` just because the vision is missing. Whether the upstream is complete, and whether to run in normal or fallback mode, is `design-strategic-goals`'s own call
- **If the user rejects the fallback candidates**: halt, prompt to run `plan-next` first to establish the strategy layer, and emit the completed step 0 health-check report

### Example 3: downgrade after the dependency step fails (edge case)

- **Context**: mode = `intake`, 5 promotion candidates
- **Step 5 fails**: `map-item-dependencies` detects a dependency cycle and halts
- **Handling**: step 5 sits at the **default** tier, so the orchestration is not terminated; record the failure and carry on
- **Step 6 downgraded**: promote's Now-tier dependency guardrail cannot take effect without `depends_on` data, so the step drops from mandatory to recommended, and the user is told plainly before it runs: "the dependency guardrail is void this round; items promoted to Now have not been dependency-checked"
- **Aggregated report**: lists outright "step 5 failed: dependency cycle `#12 → #19 → #25 → #12`; step 6's dependency guardrail did not take effect", with the suggestion to break the cycle before re-running
