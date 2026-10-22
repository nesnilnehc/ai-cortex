---
artifact_type: guide
created_by: ai-cortex
lifecycle: living
created_at: 2026-09-09
status: active
---

# Using the roadmap planning chain

For users: this is the capability map for roadmap planning. It shows what the
tools do, which assets govern them, what they produce and which presentation
forms are available. The roadmap is a plan; the skills are tools for maintaining it.

## Settle structure before content

For a new roadmap or authorized redesign, first settle the reader entry, views,
document roles, fields and navigation. Reuse existing choices during maintenance.
If structure confirmation is requested, deliver the clean empty files and stop
before business population. The [structure-first guide](../../skills/define-roadmap/references/structure-first.md)
connects blank templates, a populated case and stage-specific review evidence.
A structure-only pass does not certify a complete plan. Reader deliverables exclude
author guidance while retaining useful business explanations and actual constraints.

### Three entries, one capability

| Request | Existing skill route | Result |
| --- | --- | --- |
| Design structure first; wait before filling | define-roadmap → structure-scoped review-roadmap | Inspectable structure; business checks not evaluated |
| Fill the confirmed structure from verified sources | define-roadmap content stage → content-scoped review-roadmap | Source-backed plan using the retained layout; gaps and choices visible |
| Complete structure and content in this request | Structure stage/review → content stage/review | Separate acceptance results without a redundant confirmation |

`orchestrate-roadmap-planning` selects the route; no new standalone skill or stage
configuration is needed. Structure approval alone does not authorize content work.
Content authorization does not replace existing business decisions or permit
publication. An explicit structure-only review is also valid on populated files;
it preserves their facts and makes no content approval claim. See the
[stage contract](../../specs/roadmap-modeling.md#stage-entries-authorization-and-acceptance).

## Start from your team's delivery practice

Choose a [template combination](../../skills/define-roadmap/assets/scenarios/README.md)
and inspect the [four complete scenario examples](../../skills/define-roadmap/references/scenarios/README.md).
They share a base; optional modules provide iteration/version/phase/event/flow and
timeline views. These are supported combinations, not mandatory lifecycle layers.

| Your context | Recommended anchor | Supporting views |
| --- | --- | --- |
| Fixed-cycle product team | Iteration goals and requirements | Versions for real batches; significant release/acceptance events |
| Continuous arrivals / service work | Workflow, pull policy and flow evidence | Actual release groups or external events only when useful |
| Contract or implementation delivery | Phase deliverables and exit conditions | Significant customer acceptance points; useful timing |
| Exploration or pilot | Learning goals and evidence/exit decisions | Evidence-review events; near-term windows, not speculative rollout commitments |

The skill first reads existing norms, roadmap, boards and release records. It asks
only gaps about cadence/work mode, delivery, readers and constraints, then proposes
a primary perspective, supporting/omitted views and layout with reasons. Explicit
choices already made need no repeated confirmation. Routine updates reuse views,
layout and destination; new options alone trigger no migration or interview.
Changed context gets a focused reconsideration while current choices remain intact.

The [selection guide](../../skills/define-roadmap/references/scenario-selection.md#practice-basis)
records primary-source Scrum/Kanban/PMI principles and distinguishes our contextual
recommendations. Existing single-view and custom plans are valid. Do not invent
iterations, phase boundaries, release numbers, WIP limits or service expectations.

### Read-only recommendation

For a new proposal, prepare a partial context document from project evidence:

```json
{
  "planning_context": {
    "work_mode": "iterations",
    "delivery": "versioned",
    "audience": "Product team and customer",
    "constraints": "Two-week planning; monthly releases; no hard external deadline",
    "source": "planning-decisions.md#team-context"
  }
}
```

```sh
python3 skills/define-roadmap/scripts/render-roadmap.py context.json --recommend
```

This command prints a proposal or focused missing-information questions, writes no
files and makes no team decision. For a retained input, it returns existing choices;
changed context yields retained-review-needed. It performs no repository discovery
or live interview; the skill does that work. Legacy inputs retain views without new
metadata. New schema 1.4 generation validates a settled selection and reuses saved
layout. An explicit conflicting layout fails: update the authorized source choice
first. Recommendations are project advice, not proof of framework compliance.

## Roadmap capability map

For finished outputs rather than templates, open the
[Service Desk casebook](../../skills/define-roadmap/references/service-desk/README.md).
It connects policy decisions, dependency analysis, placement, a three-view roadmap,
an intentionally faulty candidate and its review, a blocking/delay adjustment,
after-delivery evidence and a version archive. Every snapshot uses the same IDs.

| Angle | What AI Cortex provides |
| --- | --- |
| User need | Create, inspect, prioritize, check dependencies, arrange, maintain and archive a roadmap |
| Tools | The atomic skills listed below; the planning orchestrator connects them |
| Instructions | [Roadmap modeling](../../specs/roadmap-modeling.md) defines structure; [roadmap quality](../../rules/roadmap-quality.md) judges it; templates and examples show usable presentations |
| Deliverables | Roadmap views, findings, priority decisions, dependency graph, placement decisions, retained revision summaries, change details and archive snapshots |
| Rendering | A bundled offline Python utility produces Markdown, SVG and dated Mermaid from verified facts |
| Boundary | Inclusion does not authorize implementation or release; views do not replace detailed source records |

### One plan, selected views

These fictional examples describe the same work. Their weeks are illustrative,
not project commitments. Select the useful views; an existing single-view plan
does not require expansion.

**Requirement arrangement — what comes first?**

| Now | Next | Later |
| --- | --- | --- |
| BUG1 Duplicate submission · P0 | R1 Search · P1; R2 Export · P1 | R3 Reminders · P2 |

The full requirement table also carries source, outcome, approval, execution and
key conditions. Priority and readiness explain placement; dates do not define it.

**Version delivery — what ships together?**

| Planning version | Members / core outcome | Target window |
| --- | --- | --- |
| V1 Dependable submission | BUG1, R1 · Submit once and find requests | W1–W2 |
| V2 Export delivery | R2 · Reuse exported records | W3–W4 |
| Unassigned | R3 · Remember follow-ups | Unknown |

**Schedule — when, and for how long?**

| Delivery | W1 | W2 | W3 | W4 |
| --- | --- | --- | --- | --- |
| V1 | Repair + search | Repair + search | | |
| V2 | | | Export | Export |

![Illustrative relative-week schedule, with dependency and unscheduled work](../images/roadmap-schedule.svg)

This illustration reproduces the [initial casebook snapshot](../../skills/define-roadmap/references/service-desk/initial/roadmap.md).
It shows initial targets, not later delivery facts. The SVG Gantt
output turns those filled cells into continuous bars and can show
dependency arrows and milestone diamonds. W1 begins at the project start, whose
calendar date is unknown. R3 remains visibly unscheduled. Bars encode elapsed time,
not percentage complete. Target, committed and actual timing are labeled separately.

### Form, format and destination are separate choices

| Choice | Examples |
| --- | --- |
| Form: how the plan is organized | Requirement table, version table, Gantt chart; dependency graph as a supplement |
| Format: how the view is encoded | Markdown table, Mermaid source, SVG; PNG only through an available exporter |
| Destination: where it is delivered | Repository path, local folder, or authorized knowledge-base document |

Discuss team cadence and select useful requirement, iteration/version and schedule
views at creation. Preserve established choices. Confirm the
destination before initial delivery or changing it; reuse that selection during
maintenance. Deliver once to that destination; there is no synchronization service
or second editable plan. Priority definitions explain the ordering and are linked
from the plan rather than repeated in every view.

### Policy, decisions and their explanation

Use one priority policy for relative treatment precedence. It may consider value,
urgency, dependencies and cost under the project's choices. P0–P3 and any necessary
same-level precedence are decisions made under that policy. The roadmap's current
arrangement explanation states how those decisions and verified conditions produced
this plan; it is not another scoring policy. Reuse a decision link when it already
explains the choice. Stable ID display order does not decide which tied item starts.

When a policy already has a document, link it with only the summary readers need;
a bare link is sufficient when clear. Keep the full rule and system-label mapping
there, current results in item/roadmap records, and historical application snapshots
explicitly dated. Do not maintain the current priority inventory in both places.

### Read the plan before its maintenance evidence

The overview highlights direction, current arrangement, known near-term delivery
focus and material unknowns. It is not a fixed questionnaire or a second item list.
Show unverified execution before rows; placement and draft approval do not prove
whether work started. Requirements, selected delivery/timeline views and revisions
follow. The later planning basis keeps priority/closure references and retained
view/layout/language evidence inspectable without occupying the first screen.

New supporting documents use the Spec's
[role-based naming advice](../../specs/roadmap-modeling.md#document-family-naming):
Roadmap, Requirement Priority Policy, Roadmap Planning Basis, Delivery Plan and
Timeline, and Roadmap Revision History. These are optional roles, not a required
five-document set. A local `priority-policy.md` or `roadmap-planning-basis.md` is a
suggested name, while the renderer's generated sibling names are fixed. Preserve
existing project conventions and URLs; readable page titles need no slug migration.
For a worked refinement and its compatibility boundaries, see the
[reading design](../designs/2026-10-21-roadmap-reading-technical-design.md).

### First alignment of an existing project

Say: "Align this existing project's requirements and roadmap to AI Cortex. Repair
necessary structure, preserve settled business decisions and stable links, and list
missing facts separately; do not replan." The orchestrator selects `align-existing`
before normal planning routes. Review first, use define-roadmap for structural
repair, and review again. Use update-roadmap only for a separately requested,
source-backed state/time correction when the structure is already adequate.

Preserve source priorities/order/tiers, scope, ownership, dates/commitments, approval,
execution, dependencies, pauses and closure criteria, plus views, language, IDs,
paths, URLs and anchors. Missing goals, unset priorities, unregistered requirements
or unpromoted items are gaps to report, not permission to create strategy, run
assessment, move tiers or archive. Request those follow-ups separately when needed.
Existing adequate decisions need no repeat approval. Mixed requests identify exactly
which business changes are additionally authorized.

If requirement bodies are also in scope, use review-requirements and then the
existing requirements repair loop for authorized draft repairs. Do not recapture
an existing requirement or reset its priority. Approved/implemented/superseded
originals remain frozen under the Requirement Spec; a successor revision requires
its own authorized destination and identity. Missing decisions are not invented
to fill mandatory sections, and structural roadmap repair alone proves no full
requirement-quality pass.

Repair at the established location. Use manual editing when the optional generator
cannot preserve a legacy filename/anchor or unknown field; no schema upgrade or
five-document family is required. Record an actual adoption baseline without
inventing earlier history. Remaining source gaps prevent a full governance pass;
repeating alignment with no new gap produces no changes. See the
[complete existing-project example](../../skills/define-roadmap/references/existing-project/README.md).
The [alignment design](../designs/2026-10-21-roadmap-alignment-technical-design.md)
records implementation and test boundaries.

### What is available, and what is conditional?

| Capability | Support |
| --- | --- |
| Requirement/defect arrangement, fixed status labels, evidence and source links | Provided by the roadmap skill chain |
| Optional iteration/version groups and date/relative-week schedules | Defined by the shared Spec and applied by creation/maintenance skills |
| Markdown, standalone SVG and dated Mermaid generation | Bundled standard-library Python tool; validated by its behavioral suite |
| Relative weeks without inventing calendar dates | SVG and schedule table; no dated Mermaid export |
| Knowledge-base delivery | Depends on the runtime's authorized document/image tools; verify rendering and read back writes |
| Automatic resource scheduling, working-calendar calculations, PNG/PDF export, drag editing or cross-platform sync | Not provided by the bundled generator |

### Generate local views

The callable utility lives inside `define-roadmap`; no new plotting skill is needed.
After choosing the output location, prepare temporary JSON from project records
using the [input example](../../skills/define-roadmap/references/service-desk/initial/input.json)
and the [contract](../../specs/roadmap-modeling.md#53-optional-local-generator-interface).
From the AI Cortex clone:

```sh
python3 skills/define-roadmap/scripts/render-roadmap.py input.json --check
python3 skills/define-roadmap/scripts/render-roadmap.py input.json --output-dir chosen-directory
```

Installed users substitute the resolved skill directory for the relative skill
path above. Explicit replacement uses `--overwrite` and reserves `roadmap.md`,
`roadmap.svg`, `roadmap.mmd`, `roadmap-delivery.md` and `roadmap-history.md`
for generated views. Keep authoritative evidence
elsewhere; rebase relative source links for the selected output directory.
The input is not a new ongoing planning database. Inspect the generated SVG before
claiming visual delivery. A tool exit does not verify a remote upload or platform
rendering. Missing Python or connector support is reported without installing tools.

Each skill is defined authoritatively in its own `SKILL.md`, and the execution order and tiering in [orchestrate-roadmap-planning](../../skills/orchestrate-roadmap-planning/SKILL.md). This page restates neither; it only tells you how to get in the door.

---

## 1. Almost always: one line

```text
/orchestrate-roadmap-planning
```

It checks the roadmap's health first, works out which link in the chain you are stuck on, then runs only the steps that need running; whatever it skips, the report says why. **You do not have to work out which skill to call** — that is exactly why it exists.

You can skip the slash command and just say "run a round of roadmap planning".

---

## 2. Finding the entry point from where you are

When you know exactly what you want, naming a single skill is faster.

| Where you are | What to use |
| :--- | :--- |
| You want to know what is wrong with this roadmap | [`review-roadmap`](../../skills/review-roadmap/SKILL.md) |
| There are no strategic goals yet | [`design-strategic-goals`](../../skills/design-strategic-goals/SKILL.md) |
| You want to build a roadmap from the strategic goals | [`define-roadmap`](../../skills/define-roadmap/SKILL.md) |
| You have a requirement or a defect to write down | [`capture-work-items`](../../skills/capture-work-items/SKILL.md) |
| The backlog needs re-prioritising | [`prioritize-backlog`](../../skills/prioritize-backlog/SKILL.md) |
| You want to see which items block which | [`map-item-dependencies`](../../skills/map-item-dependencies/SKILL.md) |
| You want to pull items into Now | [`promote-roadmap-items`](../../skills/promote-roadmap-items/SKILL.md) |
| Something is stuck, or the dates have to move | [`update-roadmap`](../../skills/update-roadmap/SKILL.md) |
| A milestone is finished and needs archiving | [`archive-milestone`](../../skills/archive-milestone/SKILL.md) |

The skill descriptions in [skills/INDEX.md](../../skills/INDEX.md) support discovery; [AGENTS.md](../../AGENTS.md) §4 describes matching.

---

## 3. Two places that will stop you

Both are by design, not a fault.

### 3.1 Promotion says priorities are missing

`promote-roadmap-items` reads settled priorities rather than requiring numeric scores.
`prioritize-backlog` applies an existing project policy to unresolved items by default.
Without a policy it offers four-framework assessment; an explicit full reassessment
can replace settled priorities. If every eligible item is unset, promotion stops
for that decision; if only some are unset, it continues with the settled items.

Candidates are compared across strategic goals in priority order. P0/P1 default to Now, P2 to Next, and P3 to Later, subject to prerequisite readiness and stage promotion criteria. An explicit user decision can change a proposed tier with its reason recorded. Goal mapping preserves traceability; it does not create resource quotas or separate promotion queues.

### 3.2 With the governance documents empty, it does not interrogate you from scratch

Run `design-strategic-goals` on a new project with no vision and no North Star, and it does not ask you for answers one field at a time. It works candidate goals back out of the evidence in the repository: README and AGENTS.md for intent, CHANGELOG and git log for where effort actually went, the code structure for the boundaries of what exists, the backlog for needs not yet met.

**The output is marked as such**: every candidate goal carries the evidence it was inferred from, pointing at a specific file, and one with no evidence is not written at all; nothing lands on disk until you confirm it item by item; and the document's header carries a note that it lacks upstream backing and is a temporary anchor. Once the vision and North Star exist, it should be run again.

The reason is blunt: a goal reasoned back out of evidence reads smoothly and hangs together, and that is precisely what makes it most likely to be invention filling a gap. Attaching the evidence and asking you to confirm is what lets you falsify it on the spot.

---

## 4. Why dependencies are mapped before promotion

Putting `map-item-dependencies` ahead of `promote-roadmap-items` is the most important ordering decision on the whole chain.

High priority alone does not establish next-step readiness. Check the specific
deliverable required for the next intended step, not the supplying item's tier or
whole-item completion. A later dependency permits source-backed independent work
now with a visible need-by condition; missing evidence remains unchecked. Run mapping
when evidence is missing, stale or changed, even for one candidate depending on
existing work or an external provider. Reuse sufficient current evidence.

Where an item has no dependencies recorded, `promote-roadmap-items` does not wave it through silently: it tells you to record dependencies first, and if you press on regardless, the candidate table marks it "dependencies not checked".

---

## 5. Where the criteria live

The [roadmap Spec](../../specs/roadmap-modeling.md) owns structure; the
[quality rule](../../rules/roadmap-quality.md) owns evaluation. Creation,
diagnosis and review reference both. Change a shared contract or criterion at
its authority rather than copying it into skills.

---

## 6. How this differs from plan-next

Both tell you what to do next, but they cover different ground:

- [`plan-next`](../../skills/plan-next/SKILL.md) answers "what does the whole project do next", across every layer from mission to task. It reads; it does not execute.
- `orchestrate-roadmap-planning` answers "take the roadmap line from strategy through to promotion in one pass". It covers only that vertical slice, and it does execute.

When you are unsure where governance goes next, run `plan-next` first; when you have decided to move the roadmap forward, use `orchestrate-roadmap-planning`.

## Concise roadmap presentation

Requirement-view entries are requirements and defects, never tasks or task groups.
Version groups and schedule milestones are additional views, not violations of that
granularity. Use the
[template](../../skills/define-roadmap/assets/roadmap-template.md) and
[completed example](../../skills/define-roadmap/references/roadmap-example.md).
Now / Next / Later express arrangement. Keep source links, outcomes, priorities and
separate approval and execution status columns plus a separate key conditions column
in the main view. Use the fixed execution vocabulary in the quality rule and link
the project closure criterion; development complete, acceptance passed and production
release remain distinct. Keep conditions short and linked; keep execution and acceptance detail in
source records. Explicit project capacity decisions remain in force. A concise view
need not reproduce hypotheses or metrics per tier to pass review.

## Roadmap, version, phase and milestone

Think of planning a journey: the roadmap shows the route; a version groups what
will be delivered together; a phase is a stretch of work; a milestone marks an event.
The [Roadmap Spec](../../specs/roadmap-modeling.md) owns the exact model.

| Object | Service Desk example | How to show it |
| --- | --- | --- |
| Roadmap | Restore reliability, then search, then export | Requirement arrangement plus selected views |
| Version | V2 delivers R1 after the plan changes | Member table and delivery span |
| Phase | PSEARCH carries search work through acceptance and release | Span with scope, owner and exit condition |
| Milestone | M0 kickoff, M2 acceptance approval, M3 production release | Separate event rows and zero-duration markers |

A version can have several phases and events; an event can relate to several
objects or be global. This is not a mandatory hierarchy. In the adjusted example,
V2 and PSEARCH both span W4–W5; M2 and M3 are separate target points at W6. After
delivery those events have reached state and linked evidence. Dates never prove
occurrence. Work on a review takes time even though its approval is a point event.

JSON 1.1 adds optional independent phase/event registers. Existing 1.0 input and
single-view Markdown continue to work. New milestones reference their own IDs;
legacy 1.0 markers still reference entries/versions without automatic conversion.
Use Markdown tables for reviewable facts, SVG for portable local/knowledge-base
presentation, and dated Mermaid where the destination supports it. All formats
come from the same verified facts. Legacy `milestones/` task directories remain
work-package conventions; no directory migration is required.

The [research record](../references/roadmap-milestone-research.json) records the
primary-source basis and compatibility choices.

## Keep a readable revision history

A roadmap changes. Readers need to see what changed, why and what it affects after
the discussion ends. [The revision contract](../../specs/roadmap-modeling.md#54-revision-records)
provides two linked levels:

| Level | Content | Where it stays |
| --- | --- | --- |
| Main roadmap | Latest five dated summaries: ID, before/after, reason, impact and details link | Revision history section, newest first |
| Durable history | Complete decisions, actors, evidence and older revisions | Existing change/decision records or retained archive snapshots |

Record changes to priorities/tiers, version scope, phases, dates/commitments,
material exclusions and milestone cancellation, missed or reached states. Routine
wording, formatting and link corrections can stay in Git. Git retains text changes;
it does not replace the business rationale. No-op rendering adds no decision.

The [adjusted example](../../skills/define-roadmap/references/service-desk/adjusted/roadmap.md)
retains REV1: search/export change versions, event targets move and export breaches
its original deadline by three weeks. The
[after-delivery example](../../skills/define-roadmap/references/service-desk/after-delivery/roadmap.md)
adds REV2 for source-backed acceptance/release observations and retains REV1 unchanged.
Its [full register](../../skills/define-roadmap/references/service-desk/change-record.md#revision-register)
keeps both decisions and their details.

`define-roadmap` establishes or adopts the baseline; `update-roadmap` retains
material maintenance decisions; promotion records confirmed tier decisions.
Priority assessment hands its source decision to roadmap maintenance when the
roadmap changes. Review checks traceability; archiving preserves decisions and
links. One decision shared across these steps uses one ID. A correction adds a
linked revision rather than erasing an inconvenient deadline or earlier commitment.

Generator schema 1.2 renders supplied revision records. It never reconstructs
history, appends decisions automatically or edits linked evidence. More than five
supplied records require a full-history reference; only the main display is shortened.
Carry retained records forward when regenerating. Schemas 1.0/1.1 and existing
single-view roadmaps remain compatible. Adopt a legacy baseline explicitly and
mark unknown earlier history rather than manufacturing dates or decisions.

## One main roadmap, detail when useful

Start with one document. Keep it understandable on its own; split when different
readers, owners, update rhythms or content volume justify separate maintenance.
Splitting is not an obligation to produce more files.

| Document | Reader question | Content |
| --- | --- | --- |
| Main roadmap | Where are we going and what matters next? | Direction, ordering, active priorities, blockers, near-term delivery, key events, latest five revisions |
| Optional delivery detail | How is delivery arranged? | Iteration goals/timeboxes, version membership, relevant phases/events and timeline |
| Optional history detail | Why did the plan change? | Supplied revision records and links to complete decisions/evidence |
| Existing execution board | What does each person do? | Tasks, daily progress, assignments and detailed results |

Reading order is overview → priorities → selected delivery plan → timeline →
revisions/sources. Completed work can be folded separately without changing its
tier. Phases and milestones normally stay with their delivery plan; Gantt is a
view of its timing. Author instructions and conceptual definitions stay in guides.

Each fact has one editable source. The main may contain a generated summary of
iteration/version dates; it does not become a second independently maintained
schedule. A change refreshes all affected views under one revision ID. Detail pages
link back. Hand-maintained projects can separate iteration and version documents
when their ownership/cadence differs; existing paths remain valid.

### Teams working in iterations

An iteration answers “what goal do we pursue in this timebox?” A version answers
“what ships together?” Neither is a mandatory parent of the other. A version can
cross iterations; an iteration can touch several versions or publish none. A phase
may cross either boundary, and a milestone remains an independent event.

Include source-backed cadence (such as two to four weeks), near-term iteration
goals, requirement/defect IDs, timeboxes/basis, owner and execution-board links.
Keep distant work broad and unallocated until decided. Now/Next/Later express
priority/readiness, not iteration numbers. Carry-over does not duplicate the
requirement or change its tier, and iteration end proves no acceptance or release.

The [single-document iteration example](../../skills/define-roadmap/references/service-desk/iteration-driven/roadmap.md)
and [split main roadmap](../../skills/define-roadmap/references/service-desk/iteration-driven-split/roadmap.md)
render the same [source iteration decisions](../../skills/define-roadmap/references/service-desk/iterations.md).
BUG1 contributes to I1 and I2 while staying in V1. I2 touches both V1 and V2;
R1 contributes across I2/I3 while staying in V2. R2/R3 remain unallocated, and
milestone acceptance/release criteria remain independent of timebox ends.

### Generate either layout

```sh
python3 skills/define-roadmap/scripts/render-roadmap.py input.json --output-dir chosen-directory
python3 skills/define-roadmap/scripts/render-roadmap.py input.json --layout split --output-dir chosen-directory --overwrite
```

Use schema 1.3 for optional iterations and the grouped reading structure. The
first command defaults to single output. Split mode adds delivery/history sibling
pages only when content exists; both layouts share SVG/Mermaid schedule facts.
The main retains delivery/event summaries and latest-five revisions. History detail
contains supplied records and links retained sources; it does not reconstruct history.
All five fixed filenames are reserved. Explicit overwrite removes stale generated
children when returning to single mode and leaves unrelated source files alone.
Source links are relative to the output folder; moving the entire bundle elsewhere
requires rebasing or preserving its relative source layout. Schemas 1.0–1.2 keep
legacy default output. No existing project is automatically migrated.

Some destinations do not preserve Markdown disclosure elements. Verify rendering;
expand folded content or use linked detail pages when unsupported. Local preview
is not proof of Yuque/Git host rendering or successful remote delivery.

## Deliverable language follows the consuming project

The English used in these asset instructions is not a default imposed on every
team's roadmap. Follow explicit artifact-language instructions, then project policy,
then the existing artifact. For a new roadmap, consistent reader and sibling-document
evidence can settle the choice; ask only when it cannot. Conversation language alone
is insufficient. Retain the decision with the planning choice and pass it across
skills so ordinary updates do not repeat the language interview.

The [language workflow](../../skills/define-roadmap/references/deliverable-language.md)
explains read-only resolution and schema 1.5. The [paired complete examples](../../skills/define-roadmap/references/languages/README.md)
show English and Simplified Chinese main/detail/history documents, SVG and dated
Mermaid from the same planning facts. One language per edition covers headings,
status labels, free prose and chart descriptions; IDs, URLs and canonical machine
states remain unchanged. The generator localizes built-in labels; the skill prepares
project prose and review checks its meaning. Legacy schemas retain English output.
