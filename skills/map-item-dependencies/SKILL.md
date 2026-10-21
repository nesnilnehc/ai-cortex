---
name: map-item-dependencies
description: Identify dependencies among backlog and roadmap items across five categories, record depends_on and required-deliverable evidence, and assess next-step readiness with need-by dates and reduction options before promotion.
version: 1.3.0
license: MIT
---

# Skill: Map Item Dependencies

## Purpose

Find the dependencies between backlog and roadmap items, register them on the items, and let the promotion decision see which items cannot be pulled in right now.

Priority alone does not establish next-step readiness. Apply the
[Roadmap Spec](../../specs/roadmap-modeling.md#prerequisite-readiness): distinguish
deliverables needed now, later conditions and evidence not yet verified. A supplier's
whole requirement need not finish when its needed deliverable is already available.

---

## Core Objective

**Primary goal**: identify the dependencies of the items in a given scope, write `depends_on` back, and output a dependency graph that sequencing can be based on.

**Success criteria** (all must hold):

1. ✅ Every item's dependencies are checked against all five categories (technical / team / external / knowledge / sequential); confirmed absence is `—`, while insufficient evidence remains explicitly unchecked
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

- **Before promotion**: run when candidates have missing, stale or changed dependency evidence, even for one candidate depending on existing work, another team or an external service
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
| --- | --- | --- |
| Technical | This item needs a technical capability another item produces | "needs a new data pipeline" "depends on the API refactor" |
| Team | Needs a deliverable from another team (design, platform, data) | "waiting on the design" "needs the platform team to grant access" |
| External | Waiting on a vendor, a partner, or a third-party integration | "waiting for their API to go live" |
| Knowledge | Work cannot start until research or validation reaches a conclusion | "the approach is undecided" "a POC comes first" |
| Sequential | A must ship before B can start (shared code or a shared user flow) | "registration ships before invitations" |

### Execution

1. **Fix the scope**: the promotion candidates by default; the user can name the full set or a subset.
2. **Check category by category**: for every item in scope, ask about each of the five categories in the table above, skipping none. A category with no dependency is recorded as none, never left blank.
3. **Build the graph and look for cycles**: assemble the dependencies into a directed graph and test it for cycles. **A cycle halts the run immediately**: output the cycle path and ask the user which edge to cut — this skill does not break a cycle itself.
4. **Annotate required deliverable, need-by point and owner**: identify the next intended step and the specific result it requires from source evidence. Record whether the result is available now or needed later, who supplies it, and when. Keep these details in existing item/dependency evidence; the `depends_on` shape below does not acquire mandatory fields. An unknown owner is high risk. Missing availability or step evidence stays unchecked, never guessed as none/blocked/ready.
5. **Give reduction suggestions**: for each high-risk dependency, ask four questions —
   - Can a simplified version route around this dependency?
   - Can an interface contract or a stand-in let the work proceed in parallel?
   - Can the order change so the dependency is resolved earlier?
   - Can this piece of work be absorbed into our own team, removing the cross-team coordination?
6. **Write back after confirmation**: present the dependency list, and once the user confirms, write it into the `depends_on` in each item's frontmatter.
7. **Output next-step readiness**: separate items whose next step lacks a required deliverable, those with verified independent work and a later dependency, and unchecked items. Include the required result, evidence and owner/need-by condition for promotion. A future dependency is not automatically a present blocker.

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
- Do not invent a dependency because "there ought to be one"; record none only after checking. Insufficient evidence remains unchecked and is not written as `—`.
- A dependency with no owner must be flagged explicitly as high risk; it must not be passed over in silence

### Anti-patterns (avoid)

- ❌ **Checking technical dependencies only**: team and external dependencies are what wreck a schedule most often; watching the code layer alone is not enough
- ❌ **Treating registration as the end of it**: the value of registering dependencies is feeding the promotion decision; with no blocked list the work was for nothing
- ❌ **Treating a dependency as a given**: every high-risk dependency goes through the reduction suggestions once, starting with whether the dependency can be dropped
- ❌ **Leaving it blank in place of "no dependency"**: a blank leaves downstream unable to tell "none" from "not checked"

### Skill Boundaries (avoid overlap)

| Action | Owner |
| --- | --- |
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
- [ ] Required-deliverable and next-step evidence distinguishes present blockers, later conditions and unchecked items, including a single candidate with external dependencies
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
   - #63 mobile workflow → team dependency: design is needed at the stage midpoint. Source scope confirms independently specified backend work can begin now; the design team owns the later deliverable
3. The graph has no cycle.
4. Reduction suggestion: could #51 ship read-only reporting first and route around the pipeline upgrade → the user judges it workable, recorded as the fallback plan.
5. `depends_on` is written back once the user confirms.
6. Readiness: **#51 cannot enter Now for reporting** (the required data contract from #38 is unavailable, not merely because #38 remains in backlog). #63 may enter Now for verified backend work; its later design condition remains visible. Without independent-step evidence, #63 would remain unchecked instead of passing.

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
3. Leave dependency registration unresolved instead of writing `depends_on: —`; report "this item's description is too thin to verify dependencies". Existing verified records are preserved, with any evidence gap called out.
4. Suggest the user flesh out the item description and re-run, or confirm manually at promotion time.

**Result**: nothing is fabricated where there is no evidence, and "this could not be checked" is stated to the user outright rather than silently recorded as no dependency.

## Filled deliverable example

[Filled dependency register, graph and blocked list](../define-roadmap/references/service-desk/dependencies.md). This is a fictional completed output, not a template
or authorization to change the adopting project.

## Deliverable language

Before writing roadmap-chain deliverables, apply the [language contract](../../specs/roadmap-modeling.md#57-deliverable-language-schema-15).
Read the user instruction, consuming-project policy and existing artifact first;
retain a settled choice across handoffs. For a new artifact infer only from consistent
reader/document evidence; ask only unresolved gaps or winning-level conflicts.
Conversation language and English templates alone do not select artifact language.
Record the choice and source in existing norms/planning decisions; no new mandatory
configuration. Localize all new prose and display labels consistently while preserving
IDs, machine fields, canonical enums, source links and historical originals.

Apply the retained choice to new reports, rationale, tables and diagram labels as
well as refreshed roadmap projections. Preserve existing source-record policies;
this workflow does not authorize bulk translation of unrelated documents.

Self-check: language evidence and retained choice are explicit; all new display prose
is consistent, machine contracts are unchanged, and unavailable checks are reported.
