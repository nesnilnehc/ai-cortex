---
id: ROADMAP_MODELING_SPEC_V1
name: Roadmap Modeling Schema
description: Roadmap views, source authority, priority vocabulary and local generation input contract.
version: 1.1.1
status: active
lifecycle: living
created_at: 2026-10-20
scope: |
  Defines roadmap presentation and the optional local generator input.
  Does not define task execution, automatic scheduling or release authorization.
related:
  - ./requirement-modeling.md
  - ./release-package.md
  - ../rules/roadmap-quality.md
---

# Roadmap Modeling Schema

> **Data contract**: defines consistent requirement, version and schedule views.

## 1. Position and scope

A roadmap presents existing planning decisions. Its source records retain detailed
requirements, defects, progress and acceptance evidence. Existing single-view
roadmaps remain valid. Optional views do not create additional planning authorities.

## 2. Mental model

| View | Question | Unit |
| --- | --- | --- |
| Requirement arrangement | What comes first, and what is its state? | Requirement or defect |
| Version delivery | What ships together? | Named delivery group referencing requirement/defect IDs |
| Schedule | When, and for how long? | Requirement/defect, version or phase span; independent event marker |

Now / Next / Later, priority, version membership, approval and execution are
independent dimensions. A version row is a grouping, not a task or a replacement
for its members' acceptance. Milestones mark events, not proof of delivery.

Presentation form (table, grouped columns, Gantt chart), encoding (Markdown,
Mermaid, SVG, PNG) and destination (repository, local folder, knowledge base) are
different choices. A dependency graph supplements these views.

## 3. Roadmap, version, phase and milestone

| Concept | Meaning | Relationship |
| --- | --- | --- |
| Roadmap | Evolving view of direction, sequence and timing | Presents requirements, versions, phases and events through selected views |
| Version | Delivery group of requirements/defects | May span several phases and have several milestones |
| Phase | Time-bearing segment of work with an exit condition | References requirements and/or versions; phases may overlap |
| Milestone | Significant event with an occurrence criterion | May relate to requirements, versions or phases, or be global |

These are not a mandatory four-level tree. A phase is a span; a milestone is a
zero-duration point even if the review meeting or work leading to it takes time.
Kickoff, approval, deadline and release are all valid events. Reaching one event
does not prove completion of its related work or authorize the next action.
A version's planned delivery window is distinct from its actual release event.
The legacy `milestones/{slug}/tasks.md` convention names historical work packages;
its directory name does not redefine a milestone as a duration-bearing task group.
No directory migration is implied by this model.

## 4. Evidence and compatibility

The model draws on the distinctions documented in the
[primary-source research record](../docs/references/roadmap-milestone-research.json).
The zero-duration event model is a deliberate project choice; tools permitting
nonzero-duration milestone tasks must map their event separately from the work span.
Existing single-view Markdown and JSON 1.0 inputs remain valid. A legacy 1.0 marker
references an entry/version directly; do not silently convert it or infer occurrence.
New independent phase/event records use 1.1. Their registers appear only when
records exist; no additional view or lifecycle gate is compulsory.

## 5. Body structure contract

### 5.1 Human-readable roadmap

Required: project direction, update date, requirement arrangement, ordering basis,
source references and declared closure criterion or an explicit unresolved notice.
Each requirement/defect carries ID, name, source, outcome, priority, tier, separate
approval and execution, and key conditions. Execution labels are owned by the
[quality rule](../rules/roadmap-quality.md#execution-status-vocabulary).

Version and schedule views are selected at creation, with all three recommended.
Only selected views are required. Version groups carry stable ID, planning name,
member references, core outcome, owner and target window; unknown values are explicit.
Formal release numbers and version types are optional project facts, never invented.
An item may remain unassigned; it is shown as such rather than silently omitted.

Schedules declare calendar dates or relative weeks and the meaning of their origin.
Target, committed and actual timing are distinguished. Unknown timing is shown as
unscheduled, not as a zero-length activity. Dates do not imply approval. Existing
release evidence is linked rather than duplicated in the roadmap.

### 5.2 Priority vocabulary

Default planning vocabulary: P0 (highest), P1, P2, P3 (lowest); `unset` is unresolved,
not a low priority. Project policy defines business meaning and exceptions.
Nonstandard source labels require an explicit mapping before comparison. Existing
P0–P2 records remain valid; do not silently reinterpret their historical meaning.
Tier placement is a separate decision based on readiness and project priorities.

### 5.3 Optional local generator interface

The JSON input is a transient rendering interface, not a required project file or
a second editable source. It represents verified facts; the generator does not
infer missing priorities, owners, dates or dependencies.

| Field | Type | Requirement |
| --- | --- | --- |
| `schema_version` | string | `1.0` (legacy) or `1.1` |
| `project`, `updated`, `direction`, `ordering`, `closure`, `priority_policy` | string | Required, nonempty; updated is an ISO date; direction states the goal served and ordering explains the sequence |
| `views` | array | Unique subset of `requirements`, `versions`, `schedule`; requirements always included |
| `entries` | array | Requirement/defect records; may be empty |
| `versions` | array | Required when versions view selected |
| `schedule` | object | Required when schedule view selected |

Unmodeled keys may be retained as input metadata but do not affect generated
views. In particular, only milestone records own the modeled event `state`;
a similarly named field on a version, phase or entry is not an event status.
The explicit 1.0 prohibition on `phases`/`milestones` still applies.

Entry fields: `id`, `name`, `source`, `outcome`, `priority` (P0–P3 or unset),
`tier` (Now/Next/Later), `approval`, `execution`, `conditions`.
All are nonempty strings except `execution`, which may be null for unverified
mapping. Null is reported separately from status, never replaced by a guessed
execution label. Entry IDs are unique ASCII letters/digits/underscores/hyphens,
starting with a letter. Source is a relative reference, fragment, or HTTP(S) URL;
absolute paths, protocol-relative URLs and other schemes are rejected.

Version fields: `id`, `name`, `members` (entry IDs), `outcome`, `owner`, `window`.
IDs are globally unique across all four record types. Unknown owner/window uses
the explicit string `Unknown`. An entry belongs to at most one version in this
snapshot; partial deliveries require distinct source records rather than duplicating
the whole entry across versions. Empty versions are permitted with empty members.

Optional 1.1 fields: `phases` and `milestones` arrays (default empty). They are
invalid in 1.0, preventing ambiguous partial upgrades.

Phase fields: `id`, `name`, `source`, `owner`, `scope`, `exit_condition`.
`scope` is a nonempty, unique array of existing entry/version IDs. Phases cannot
contain phases. Exit conditions describe the work's completion, not inferred status.

Milestone fields: `id`, `name`, `source`, `owner`, `related`, `category`, `criterion`,
`state`, `evidence`. `related` contains unique entry/version/phase IDs; an empty
array denotes a global event. Category is `achievement`, `approval`, `deadline`,
`event` or `start`. State is `planned`, `reached`, `missed` or `cancelled`.
Criterion defines what establishes occurrence; non-planned states require a linked
evidence record. Planned events may have null/omitted evidence. Sources and evidence
use the same reference syntax as entry sources. Owners and criteria are nonempty.
Dates alone never change state. A past target can remain planned pending evidence.
Actual milestone timing requires reached state and therefore evidence.

In 1.1, schedule kind `span` references entries, versions or phases; kind `milestone`
references only milestone IDs. Each record has at most one schedule item, while
multiple event IDs may reference the same version and share its boundary date.
Unsupplied phase/event timing is reported as missing when schedule is selected.

Schedule fields: `mode` (dates/weeks), `origin` (nonempty explanation),
`calendar` (exactly `calendar-days`), `items` (array).
The first renderer uses elapsed calendar days or whole weeks, not business-day
arithmetic; project working calendars must be resolved upstream.

Schedule item fields: `ref` (record ID), `kind` (span/milestone),
`basis` (target/committed/actual), `start`, `end`, `depends_on` (scheduled refs).
Each ref occurs once. Dates use ISO YYYY-MM-DD; weeks use positive integers.
Spans use an exclusive end: W1 to W3 covers W1–W2. Milestones have equal start/end.
Unscheduled items have both endpoints null. In 1.0 they must have kind span;
in 1.1 unscheduled milestones retain kind milestone and have no plotted marker. One missing endpoint,
an inverted span, mixed time modes, duplicate dependencies and cycles are invalid.
Finish-to-start dependencies must not overlap; unknown endpoints leave timing
unverified and are reported. This is validation, not resource scheduling.

Input is capped at 1 MiB, 200 total entry/version/phase/milestone records, 200 schedule items and
200 characters per text field. Larger roadmaps must be split. Schedule horizon
is capped at 366 calendar days or 104 weeks to preserve readable output.

Outputs are fixed names in the selected directory: `roadmap.md`, and for a schedule
`roadmap.svg`; dated schedules also produce `roadmap.mmd`. Relative-week schedules
produce SVG and a table, never fictitious Mermaid calendar dates. Files are
deterministic, UTF-8, and replaced only with explicit overwrite scope. Existing
unrelated files are untouched. Reserved output paths must not identify the input
file, including through a hard-link alias. Before replacing fixed outputs, remove a stale
generated SVG/Mermaid only under that same explicit overwrite scope; the generated
filenames must be reserved for this purpose, never used for source evidence.

## 6. Anti-patterns

- Using a version's aggregate completion as proof its members passed acceptance.
- Inventing dates to satisfy a renderer, or presenting targets as commitments.
- Editing temporary JSON and project records independently as competing plans.
- Treating SVG export as proof that a knowledge-base upload succeeded.

## 7. Examples

Minimal valid single-view input:

```json
{
  "schema_version": "1.0",
  "project": "Service desk",
  "updated": "2026-10-20",
  "direction": "Make request handling dependable.",
  "ordering": "Restore dependable outcomes before adding workflow shortcuts.",
  "closure": "Acceptance and production release; see the project delivery policy.",
  "priority_policy": "P0 customer blockers before P1 improvements; project policy applies.",
  "views": ["requirements"],
  "entries": []
}
```

A relative-week schedule uses `mode: weeks`, an origin such as `W1 begins when
the project starts; start date unknown`, and a span with `start: 1`, `end: 3`.
A dated span from `2026-11-02` to `2026-11-16` covers November 2–15.
