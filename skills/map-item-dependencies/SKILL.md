---
name: map-item-dependencies
description: Identify dependencies among backlog and roadmap items across five categories, record them in each item's depends_on field, and produce a dependency graph with need-by dates and reduction options. Runs before promotion so blocked items are not pulled into Now.
description_zh: 识别 backlog 与 roadmap 条目间的五类依赖，写入条目 depends_on 字段，产出依赖图、需解决时点与削减建议；在晋升前运行，避免被阻塞条目被拉进 Now。
tags: [workflow, planning, dependencies]
version: 1.0.0
license: MIT
recommended_scope: project
cognitive_mode: interpretive
metadata:
  author: ai-cortex
triggers: [map dependencies, dependency graph, item dependencies, blocked by, sequencing]
input_schema:
  type: free-form
  description: Backlog items (any priority state) and current roadmap; optional scope limited to promotion candidates
output_schema:
  type: chat
  description: Dependency graph + need-by table + reduction options; depends_on written back to each item's frontmatter
---

# Skill: Map Item Dependencies

## Purpose

Find the dependencies between backlog and roadmap items, register them on the items, and let the promotion decision see which items cannot be pulled in right now.

Dependencies are the highest-risk factor on a roadmap: they show up neither in the priority nor in the capacity, yet they leave a high-priority item stuck in place once it enters Now.

---

## Core Objective

**Primary goal**: identify the dependencies of the items in a given scope, write `depends_on` back, and output a dependency graph that sequencing can be based on.

**Success criteria** (all must hold):

1. ✅ Every item's dependencies are checked one by one against the five categories (technical / team / external / knowledge / sequential), with `—` recorded explicitly where there are none
2. ✅ The dependency graph is acyclic; on finding a cycle, halt and name the cycle path instead of breaking it here
3. ✅ Each dependency is annotated with "resolve by when" and its owner
4. ✅ `depends_on` is written back into the item frontmatter, with cross-document dependencies marked by a path prefix
5. ✅ High-risk dependencies come with reduction suggestions
6. ✅ A blocked list is output in a form `promote-roadmap-items` can consume directly (which items cannot enter Now at present)

**Acceptance test**: with the output in hand, can you answer "can this item enter Now, and if not, who is it stuck behind" straight away?

**Handoff point**: once the dependencies are registered, hand off to `promote-roadmap-items` for the promotion.

---

## Scope Boundaries

**This skill owns**:

- Identifying dependencies between items and classifying them
- Writing the `depends_on` field back
- Producing the dependency graph, the resolve-by dates, and reduction suggestions
- Outputting the blocked list

**This skill does not own**:

- Promotion / demotion decisions (`promote-roadmap-items`)
- Item scoring (`prioritize-backlog`)
- Creating items (`capture-work-items`)
- Resolving the dependencies themselves (that belongs to the execution layer; this skill only registers and flags them)
- Task-level dependency breakdown (carried by a runtime such as AgentFabric)

---

## Use Cases

- **Before promotion**: with candidate items ≥ 2, run this skill first to avoid pulling blocked items into Now
- **Scheduling review**: when it matters which items must run in series and which can run in parallel
- **Retrospective when stuck**: a Now-tier item is not moving, so check for an unregistered prerequisite

---

## Behavior

### Interaction policy

- **Default**: the scope is the current promotion candidates; the user can widen it to the whole backlog or to a named set of items
- **Inference and confirmation**: prefer to infer a dependency from the item body, `strategic_goal_id`, and the existing roadmap order; an inferred dependency must be confirmed by the user before it is written back, and is never persisted automatically
- **halt**: on finding a dependency cycle, stop and report it; the user decides how to break it

### The five dependency categories

| Category | Meaning | Typical signal |
|---|---|---|
| Technical | This item needs a technical capability another item produces | "needs a new data pipeline" "depends on the API refactor" |
| Team | Needs a deliverable from another team (design, platform, data) | "waiting on the design" "needs the platform team to grant access" |
| External | Waiting on a vendor, a partner, or a third-party integration | "waiting for their API to go live" |
| Knowledge | Work cannot start until research or validation reaches a conclusion | "the approach is undecided" "a POC comes first" |
| Sequential | A must ship before B can start (shared code or a shared user flow) | "registration ships before invitations" |

### Execution

1. **Fix the scope**: the promotion candidates by default; the user can name the full set or a subset.
2. **Check category by category**: for every item in scope, ask about each of the five categories in the table above, skipping none. A category with no dependency is recorded as none, never left blank.
3. **Build the graph and look for cycles**: assemble the dependencies into a directed graph and test it for cycles. **A cycle halts the run immediately**: output the cycle path and ask the user which edge to cut — this skill does not break a cycle itself.
4. **Annotate the resolve-by date and the owner**: record "who resolves it" and "by when it needs resolving" for each dependency. A dependency with no owner counts as high risk and is called out on its own.
5. **Give reduction suggestions**: for each high-risk dependency, ask four questions —
   - Can a simplified version route around this dependency?
   - Can an interface contract or a stand-in let the work proceed in parallel?
   - Can the order change so the dependency is resolved earlier?
   - Can this piece of work be absorbed into our own team, removing the cross-team coordination?
6. **Write back after confirmation**: present the dependency list, and once the user confirms, write it into the `depends_on` in each item's frontmatter.
7. **Output the blocked list**: list the items with an unresolved prerequisite, for `promote-roadmap-items` to use as the Now-tier admission criterion.

### The `depends_on` field

```yaml
depends_on:
  - ref: <item ID or relative-path#anchor>
    kind: technical | team | external | knowledge | sequential
    need_by: <ISO date | stage name>
    owner: <owner>
```

With no dependency, write `depends_on: —`, never blank — a blank cannot separate "no dependency" from "not checked yet".

**Where the field semantics come from**: this follows the existing convention for `depends_on` in [rules/task-quality.md](../../rules/task-quality.md) (acyclic dependency graph, `—` where there is no dependency, cross-document dependencies marked by a path prefix). That rule was written to constrain tasks; here the same semantics are borrowed for the backlog item.

> **Known debt**: backlog-item has no spec of its own; its structure is defined only implicitly by the output template of `capture-work-items`. This skill adds a field to an artifact that has no spec, which is semantic borrowing. If the backlog-item fields keep growing, add `specs/backlog-item-modeling.md` to bring the structure back under a spec. This is booked here as debt, not as something resolved.

---

## Input & Output

**Input**: backlog items (any priority state) + the current roadmap; an optional scope restriction.

**Output**: the dependency graph in chat + the resolve-by table + reduction suggestions + the blocked list; the `depends_on` in each item's frontmatter is updated.

---

## Restrictions

### Hard Boundaries

- On finding a dependency cycle, must halt; must not pick an edge and break it here
- An inferred dependency must not be written back without the user's confirmation
- Do not change an item's `priority` / `status` / tier
- Do not invent a dependency because "there ought to be one"; with no evidence, record none
- A dependency with no owner must be flagged explicitly as high risk; it must not be passed over in silence

### Anti-patterns (avoid)

- ❌ **Checking technical dependencies only**: team and external dependencies are what wreck a schedule most often; watching the code layer alone is not enough
- ❌ **Treating registration as the end of it**: the value of registering dependencies is feeding the promotion decision; with no blocked list the work was for nothing
- ❌ **Treating a dependency as a given**: every high-risk dependency goes through the reduction suggestions once, starting with whether the dependency can be dropped
- ❌ **Leaving it blank in place of "no dependency"**: a blank leaves downstream unable to tell "none" from "not checked"

### Skill Boundaries (avoid overlap)

| Action | Owner |
|---|---|
| Promotion / demotion | `promote-roadmap-items` |
| Scoring | `prioritize-backlog` |
| Creating items | `capture-work-items` |
| Status change / date shift | `update-roadmap` |
| Task-level dependencies | AgentFabric runtime (outside AI Cortex) |

---

## Self-Check

- [ ] The scope was confirmed with the user
- [ ] Every item was checked against all five categories, and categories with no dependency were recorded as none explicitly
- [ ] Cycle detection was run; a cycle led to a halt and the cycle path was output
- [ ] Every dependency carries kind / need_by / owner; those without an owner are flagged as high risk
- [ ] Each high-risk dependency went through the four reduction suggestion questions
- [ ] `depends_on` was written back only after the user confirmed the dependency list
- [ ] The blocked list was output and can be consumed directly by `promote-roadmap-items`
- [ ] No item's priority / status / tier was changed

---

## Examples

### Example 1: checking before promotion (mainstream case)

**Background**: 4 promotion candidates, lined up for Now.

**Flow**:

1. The scope is these 4 candidates.
2. Check category by category:
   - #42 payment optimization → no dependency
   - #51 advanced reporting → technical dependency on #38 data pipeline upgrade (in the backlog, not promoted)
   - #17 auth refactor → no dependency
   - #63 mobile workflow → team dependency: waiting on the design team's deliverable, need_by the midpoint of this stage, owner the design team
3. The graph has no cycle.
4. Reduction suggestion: could #51 ship read-only reporting first and route around the pipeline upgrade → the user judges it workable, recorded as the fallback plan.
5. `depends_on` is written back once the user confirms.
6. Blocked list: **#51 cannot enter Now at present** (its prerequisite #38 is still in the backlog); #63 can enter, but the design deliverable needs watching.

**Result**: at promotion #51 went to Next instead, which avoided an item that would have stalled inside Now.

### Example 2: a dependency cycle turns up (edge case)

**Background**: three items reference each other — #12 says it waits on #19's API, #19 says it waits on #25's auth model, and #25 says it waits on #12's data structure.

**Flow**:

1. Building the graph detects a cycle: `#12 → #19 → #25 → #12`.
2. **halt**, output the cycle path and the evidence behind each of the three edges.
3. State that this skill does not break the cycle itself — which edge to cut is a scope and design decision, beyond what dependency registration covers.
4. Offer two common ways out for the user to judge: downgrade one edge to "interface contract first, implementation later", or merge the three into a single item done in one pass.
5. The user decides to turn `#25 → #12` into interface-contract-first.
6. The rebuilt graph has no cycle, and the normal flow continues.

**Result**: the cycle was cut explicitly by the user, with the reasoning left on record; the skill made no scope decision on the user's behalf.

### Example 3: not enough evidence (edge case)

**Background**: the item body is one line, "optimize search", giving no sign of whether it depends on anything else.

**Flow**:

1. All five categories are checked; none of them produces a usable signal.
2. **No invented dependency** — nothing is added out of thin air because "search usually depends on an index".
3. Record `depends_on: —`, and note in the report: "this item's description is too thin for the dependency check to have evidence".
4. Suggest the user flesh out the item description and re-run, or confirm manually at promotion time.

**Result**: nothing is fabricated where there is no evidence, and "this could not be checked" is stated to the user outright rather than silently recorded as no dependency.
