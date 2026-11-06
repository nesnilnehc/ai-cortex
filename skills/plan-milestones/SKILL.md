---
name: plan-milestones
description: Create or revise a project milestone plan from delivery goals, commitments, review or acceptance criteria, and dependencies. Use for milestone planning or rescheduling, including projects without a roadmap. Produce a Markdown plan with an optional calendar-scale SVG.
version: 0.2.1
license: MIT
---

# Plan Milestones

Apply the [Roadmap Modeling Spec](../../specs/roadmap-modeling.md#milestone-planning-achievement-and-comparison)
and the [phase and event integrity rule](../../rules/roadmap-quality.md#phase-and-event-integrity).
Plan significant events with observable occurrence criteria. Select events that
matter to a decision, commitment or handoff. The project's delivery approach
determines granularity and timing precision.

## Create or revise the plan

1. Read project norms and the existing plan or proposed events, along with the
   relevant goals, commitments, dependencies and decisions. Use the project's
   chosen destination, language and document structure. Resolve the editable
   source using the Spec's
   [ownership contract](../../specs/roadmap-modeling.md#reading-order-and-document-boundaries).
   If the source or destination is unclear, return a reviewable draft and state
   what needs to be resolved before applying it.
2. **Create:** select key events from the available facts. Give each event a stable
   ID, a testable occurrence criterion and a source. Record the responsible party
   and timing with the precision the source supports. Distinguish target dates or
   windows from confirmed commitments. Keep unknown dates and prerequisites
   explicit. Mark an event with no established owner or criterion as proposed
   and state the missing decision.
3. **Revise:** match by existing ID and retain the event identity while the scope
   and criterion remain comparable. If either changes materially, record the
   change explicitly and identify comparisons or downstream plans affected by it.
   Apply the [revision contract](../../specs/roadmap-modeling.md#54-revision-records)
   for material decisions. Separate confirmed impact from dependencies still to
   check. Preserve historical commitments and apply downstream date changes only
   when supported and authorized.
4. Apply authorized decisions to the owning source and read back the edited
   entries. For a tracker or other external destination, use an available project
   connector or CLI with access to read and update the selected record. If that
   capability is unavailable, return the draft and identify the access gap. Report
   what was saved, any unverified updates and which projections need refreshing.

## Deliverables

Use a Markdown plan or an equivalent structure in the project's selected system.
A Markdown row can carry ID, event, occurrence criterion, owner, timing, timing
basis and source. Use the project's existing fields to distinguish these roles
where applicable. Cite stable IDs and link to the source records where possible.

- **Related work:** the requirement, version or phase the event concerns. For a
  version or phase, link its scope record for the full list of requirements.
- **Key prerequisites:** conditions that directly affect occurrence or timing.
  For each prerequisite, state what must happen. Keep unresolved prerequisites
  visible as open decisions.

Preserve established fields and links, including the material revision or a link
to it. A formally selected baseline remains identifiable in the source history.

### Optional SVG calendar

When requested or already selected, derive the calendar from the same records
under the [SVG contract](../../specs/roadmap-modeling.md#milestone-plan-svg).
Project the plan into temporary UTF-8 JSON with a `title` and `milestones` array.
Set `locale` to `en` (the default) or `zh-CN` for chart labels. Keep plan order
and use each entry's `id`, `name` and `timing`. The renderer accepts up to 200
rows and 1 MiB of JSON. Its IDs must be unique and match
`[A-Za-z][A-Za-z0-9_-]*`. Keep the readable plan if its IDs are incompatible.

Use `null` when the entry has no renderable timing. Preserve any known dates or
wording in the readable plan if the timing basis is unresolved. For a known
`basis` (`target` or `committed`), use one of these shapes:

- `date` for a single ISO date (`YYYY-MM-DD`).
- `start` and `end` for ISO calendar bounds. `start` is inclusive and `end` is
  exclusive. For a known quarter, use the first day of that quarter and the
  first day of the next quarter. An optional `label` preserves the source wording.
- `label` alone for a known target or commitment without defensible calendar
  bounds. The row shows the label without a plotted mark.

Use an available Python interpreter and check its version with `--version`
(3.10 or later). Resolve the [milestone renderer](scripts/render-plan.py) and its
[roadmap renderer dependency](../define-roadmap/scripts/render-roadmap.py) from
the same local AI Cortex checkout. Run the milestone renderer with the temporary
JSON and capture its standard output at a new temporary SVG path. In a POSIX shell:

```sh
python3 "$renderer" "$input" > "$preview"
```

After a successful exit, check that the preview opens and matches the plan before
saving or replacing the SVG at the authorized destination. Link the current SVG
from the readable plan if the destination can display it. If a dependency is
missing, rendering fails or the destination lacks SVG support, deliver the
readable plan and report the limitation. Preserve any existing SVG and identify
it as stale when it no longer matches the plan.

## Roadmap handoff

- `plan-milestones` owns a request limited to defining or changing milestone plan
  facts. A roadmap is optional input.
- For a mixed request, update the owning source first. Route view selection to
  [`define-roadmap`](../define-roadmap/SKILL.md) and refreshes of existing views to
  [`update-roadmap`](../update-roadmap/SKILL.md). Apply the Spec's
  [reference and conflict rules](../../specs/roadmap-modeling.md#roadmap-references-and-conflicts)
  so views retain the source link, milestone ID, timing basis and revision reference.
- [`review-roadmap`](../review-roadmap/SKILL.md) reviews roadmap consistency.
  Actual achievement, plan-versus-actual analysis and archival are separate
  activities governed by the applicable source and workflow.

## Self-Check

- Each milestone has a stable ID, observable occurrence criterion and traceable
  source. Targets, commitments and unknowns retain their meaning.
- Related work and key prerequisites retain their distinct roles and source links.
- The authorized plan source and any material revision are identifiable. A repeat
  of the same decision does not create another record or silently move dependent dates.
- When requested, the SVG agrees with the plan and preserves date precision.
  If it could not be delivered, the readable plan and the reason are available.
