# Select a roadmap combination

Use this reference for creation or an explicitly requested structural refresh.
Ordinary maintenance reuses established choices. The [Roadmap Spec](../../../specs/roadmap-modeling.md#56-context-recommendations-and-retained-selection-schema-14)
owns the contract; this reference supplies the interview and contextual advice.

## Read first, ask gaps, recommend, retain

1. Inspect project norms, current roadmap/main-detail links, source requirements,
   iteration/flow boards and release/acceptance records. Record known facts and
   sources. Do not ask the user to repeat facts already established in the session.
2. Resolve work mode/cadence, delivery mode, readers and constraints. Bundle only
   unanswered questions. Source locations are normally discovered, not another
   user questionnaire. Record explicit user statements in an existing decision source.
3. Propose one primary perspective and supporting views; name omitted views and
   why, layout, uncertainty and maintenance cost. Use the closest recipe as a starting
   point, not a verdict. Add a timing view when dates or useful relative windows exist.
4. Accept an explicit choice or already authorized direction without another approval
   ritual. For missing product trade-offs, ask a focused question and continue other
   work. Retain the decision in existing norms/roadmap sources; JSON is a projection.
5. During maintenance, reuse views, primary perspective, layout and destination.
   New fields or recipes alone trigger no migration/interview. If context changes
   materially or sources conflict, present the difference and suggested adjustment
   while retaining the existing choice until the trade-off is resolved. One material
   decision gets one revision across affected documents and diagrams.

## Questions, only when unanswered

| Evidence needed | Focused question | Why it changes the recommendation |
| --- | --- | --- |
| Work organization | Fixed cycles (how long), continuous flow, stages or discovery? | Chooses the primary planning perspective |
| Delivery | Continuous delivery, named release batches or customer acceptance? | Determines whether versions and acceptance/release events help |
| Readers | Team, management, customer or downstream collaborators? | Determines summary emphasis and useful detail separation |
| Constraints | Dates, dependencies, approval/acceptance conditions, or explicitly none? | Determines meaningful events, timing basis and exceptions |

Do not turn these into a mandatory interview. If facts already answer them, show
the recommendation directly. If an unknown matters, disclose it; do not fill a
missing cadence, WIP limit, release number or deadline from the recipe.

## Recommended starting combinations

| Scenario | Primary | Supporting views | Omit unless needed |
| --- | --- | --- | --- |
| Iteration product | Iteration goals and requirement arrangement | Versions for named batches; significant release/acceptance events; useful timeline | Phases without distinct purpose/risk/exit criteria |
| Continuous flow | Workflow/pull policy and flow evidence | Versions for actual batches; events for external commitments | Artificial iterations, fake release groups or default numeric WIP/SLE |
| Staged delivery | Phase deliverables and exit conditions | Significant acceptance/coordination events; timeline | Iterations absent from team practice; versions absent from delivery |
| Discovery pilot | Learning goals, evidence and exit decisions | Evidence-review events; near-term windows | Committed long-term feature batches and speculative rollout dates |

Requirements, priorities, blockers, source evidence and revisions remain common.
The generator's deterministic recommendation uses declared work/delivery modes;
readers/constraints require skill/user tailoring rather than keyword inference.
Default a new small plan to one document. Split by ownership/readership/update
rhythm when it improves use; keep the main independently useful. Teams can make
custom combinations and retain their own vocabulary and existing numbering.

## Practice basis

Primary sources accessed 2026-10-21. These guides support principles; the recipe
combinations and default layout above are AI Cortex synthesis, not industry mandates.

| Source | Verified principle | Application / limitation |
| --- | --- | --- |
| [Scrum Guide, November 2020](https://scrumguides.org/scrum-guide.html) | Sprints organize goals and usable increments; an increment can be delivered before Sprint end; review is not a release gate | Use iteration goals without equating iteration end and publication; recipes do not establish Scrum compliance |
| [Kanban Guide, May 2025](https://kanbanguides.org/the-kanban-guide/2025.5/) | Visualize/manage/improve workflow; track WIP, throughput, work-item age and cycle time | Flow can be the primary view without invented sprints; numeric policies and service expectations require project evidence |
| [PMI, What is a Project?](https://www.pmi.org/about/what-is-a-project) | Lifecycle phases group related activities culminating in deliverables | Use phases when they clarify real delivery boundaries; this page does not prescribe the discovery recipe or a universal phase sequence |

General advice: connect work to outcomes; detail the near term and preserve distant
uncertainty; distinguish forecasts/commitments/actuals; use verifiable event criteria;
keep one editable source and reconsider views that no longer support a decision.
Do not create phases mechanically from every design/development/test activity.
Do not measure discovery success solely by shipped feature count. These are project
recommendations to tailor, not extra acceptance gates for all consumers.

## Artifacts and tool handoff

Start from the [template combinations](../assets/scenarios/README.md) and compare
[four complete examples](scenarios/README.md). Retain the choice in an existing
project document. A generator input using schema 1.4 carries the settled `selection`
and top-level `views`; its `context` records work/delivery/readers/constraints/source.

```sh
python3 skills/define-roadmap/scripts/render-roadmap.py context.json --recommend
python3 skills/define-roadmap/scripts/render-roadmap.py input.json --check
python3 skills/define-roadmap/scripts/render-roadmap.py input.json --output-dir chosen-directory
```

Recommendation JSON statuses are proposal, needs-input, retained or
retained-review-needed. It writes nothing and applies no choices. A valid legacy
input retains its existing views without requiring new context; unknown primary/
layout stay null and must be read from the existing roadmap. New 1.4 generation
uses saved layout; a conflicting explicit layout fails. Change its source decision
before regenerating an authorized layout change. Keep the same destination unless
the user requests another; no remote writes occur through recommendation.
