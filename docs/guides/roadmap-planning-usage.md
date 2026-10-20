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
| Deliverables | Roadmap views, findings, priority decisions, dependency graph, placement decisions, change summaries and archive snapshots |
| Rendering | A bundled offline Python utility produces Markdown, SVG and dated Mermaid from verified facts |
| Boundary | Inclusion does not authorize implementation or release; views do not replace detailed source records |

### One plan, three ways to look at it

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

Recommend all three views at first creation and let the user choose. Confirm the
destination before initial delivery or changing it; reuse that selection during
maintenance. Deliver once to that destination; there is no synchronization service
or second editable plan. Priority definitions explain the ordering and are linked
from the plan rather than repeated in every view.

### What is available, and what is conditional?

| Capability | Support |
| --- | --- |
| Requirement/defect arrangement, fixed status labels, evidence and source links | Provided by the roadmap skill chain |
| Optional version groups and date/relative-week schedules | Defined by the shared Spec and applied by creation/maintenance skills |
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
`roadmap.svg` and `roadmap.mmd` for generated views. Keep authoritative evidence
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

High priority does not mean it can be pulled now. Promote a P0 item whose prerequisite is still sitting in the backlog and it sits in Now while unable to progress. So entry to Now has two conditions: it ranks near the top, **and** it has no unresolved prerequisite.

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
