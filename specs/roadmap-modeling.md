---
id: ROADMAP_MODELING_SPEC_V1
name: Roadmap Modeling Schema
description: Roadmap views, source authority, priority vocabulary and local generation input contract.
version: 1.4.0
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

> **Data contract**: defines consistent requirement, iteration/version and schedule views.

## 1. Position and scope

A roadmap presents existing planning decisions. Its source records retain detailed
requirements, defects, progress and acceptance evidence. Existing single-view
roadmaps remain valid. Optional views do not create additional planning authorities.

## 2. Mental model

| View | Question | Unit |
| --- | --- | --- |
| Requirement arrangement | What comes first, and what is its state? | Requirement or defect |
| Iteration cadence (optional) | What near-term goal fits each timebox? | Timebox referencing requirement/defect IDs |
| Version delivery | What ships together? | Named delivery group referencing requirement/defect IDs |
| Schedule | When, and for how long? | Requirement/defect, version or phase span; independent event marker |

Now / Next / Later, priority, version membership, approval and execution are
independent dimensions. A version row is a grouping, not a task or a replacement
for its members' acceptance. Milestones mark events, not proof of delivery.

Presentation form (table, grouped columns, Gantt chart), encoding (Markdown,
Mermaid, SVG, PNG) and destination (repository, local folder, knowledge base) are
different choices. A dependency graph supplements these views.

## 3. Roadmap, version, iteration, phase and milestone

| Concept | Meaning | Relationship |
| --- | --- | --- |
| Roadmap | Evolving view of direction, sequence and timing | Presents requirements, versions, phases and events through selected views |
| Version | Delivery group of requirements/defects | May span several phases and have several milestones |
| Iteration | Recurring timebox with a goal | Can touch multiple versions; one version can span multiple iterations |
| Phase | Time-bearing segment of work with an exit condition | References requirements and/or versions; phases may overlap |
| Milestone | Significant event with an occurrence criterion | May relate to requirements, versions or phases, or be global |

These are independent planning concepts, not a mandatory containment tree. A phase is a span; a milestone is a
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
New independent phase/event records use 1.1–1.4. Revision summaries use 1.2–1.4. Their registers appear only when
records exist; no additional view or lifecycle gate is compulsory.

## 5. Body structure contract

### 5.1 Human-readable roadmap

Required: project direction, update date, requirement arrangement, ordering basis,
source references and declared closure criterion or an explicit unresolved notice.
Each requirement/defect carries ID, name, source, outcome, priority, tier, separate
approval and execution, and key conditions. Execution labels are owned by the
[quality rule](../rules/roadmap-quality.md#execution-status-vocabulary).

Version, iteration and schedule views are selected when useful. Discuss delivery cadence
and recommend appropriate delivery/schedule views at creation; no view is mandatory
merely because a template supports it.
Only selected views are required. Version groups carry stable ID, planning name,
member references, core outcome, owner and target window; unknown values are explicit.
Formal release numbers and version types are optional project facts, never invented.
An item may remain unassigned; it is shown as such rather than silently omitted.

Schedules declare calendar dates or relative weeks and the meaning of their origin.
Target, committed and actual timing are distinguished. Unknown timing is shown as
unscheduled, not as a zero-length activity. Dates do not imply approval. Existing
release evidence is linked rather than duplicated in the roadmap.

### Reading order and document boundaries

Use this reading order rather than a separate top-level chapter per data type:

1. Overview: direction, update date, ordering rationale, policy and closure basis.
2. Priority arrangement: requirements/defects and their material conditions.
3. Delivery plan, when selected: iteration and/or version planning, with relevant
   phases and milestone events grouped beneath it.
4. Timeline, when selected: primary diagram, unknowns and timing exceptions;
   a detailed timing table may be folded or linked.
5. Latest revisions and source/detail links.

Keep completed work separate from active priorities (folded or linked archive),
without changing its source status or tier. Do not replicate a priority table in
several narrative sections. Definitions and author instructions belong in guides,
not filled deliverables. Omit empty optional chapters rather than padding them.

A small roadmap MAY remain one document. Split when readership, ownership, update
cadence or volume makes separate maintenance useful, not at an invented page limit.
The main roadmap MUST independently explain current priorities, next work, blockers,
near-term delivery expectations and key events where known. It retains the latest
five revision summaries. It MUST NOT become a link-only index.

Optional detail documents hold iteration plans, version scope, schedule detail or
retained history. Separate iteration and version documents only when useful; phases
and events normally stay with the related delivery plan. Gantt is a derived view,
not an additional planning authority. Every detail page links back to the main plan.

For each fact, declare one editable source (requirement, iteration board, version
plan or decision record). Main/detail summaries are linked or generated projections.
When a planning decision changes, refresh every affected projection and retain one
revision ID. Do not maintain separate editable copies of scope or dates. Detailed
iteration tasks, daily progress and individual assignments remain on execution
boards; the roadmap carries goals, scope and links. Sources are resolved relative
to their containing output document, not the temporary input file.

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
| `schema_version` | string | `1.0` (legacy), `1.1`, `1.2`, `1.3` or `1.4` |
| `project`, `updated`, `direction`, `ordering`, `closure`, `priority_policy` | string | Required, nonempty; updated is an ISO date; direction states the goal served and ordering explains the sequence |
| `views` | array | Unique subset of `requirements`, `versions`, `schedule`, plus `iterations` in 1.3+ and `phases`, `milestones`, `flow` in 1.4; requirements always included |
| `entries` | array | Requirement/defect records; may be empty |
| `versions` | array | Required when versions view selected |
| `schedule` | object | Required when schedule view selected |
| `iterations`, `cadence` | array, string | In 1.3+, required when iterations view selected; records may be empty; cadence is nonempty source-backed text |
| `revisions` | array | Required in 1.2–1.4, including an explicit empty array for an adopted baseline; not modeled in earlier schemas |
| `selection` | object | Required in 1.4; source-backed scenario, primary perspective, layout, rationale and context; top-level views are the only enabled-view list |
| `flow` | object | In 1.4, required only when flow selected; workflow policy, expectation, metrics and source/board links |
| `revision_history` | string or null | Optional full-history reference in 1.2–1.4; required when more than five revision records are supplied |

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
IDs are globally unique across entry/version/phase/milestone records and 1.3+ iterations. Unknown owner/window uses
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

In 1.1–1.4, schedule kind `span` references entries, versions, phases or 1.3+ iterations; kind `milestone`
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
in 1.1–1.4 unscheduled milestones retain kind milestone and have no plotted marker. One missing endpoint,
an inverted span, mixed time modes, duplicate dependencies and cycles are invalid.
Finish-to-start dependencies must not overlap; unknown endpoints leave timing
unverified and are reported. This is validation, not resource scheduling.

Input is capped at 1 MiB, 200 total planning objects (including 1.3+ iterations), 200 schedule items and
200 characters per text field. Larger roadmaps must be split. Schedule horizon
is capped at 366 calendar days or 104 weeks to preserve readable output.

The CLI selects `--layout single` (default) or `--layout split`. Single mode writes
`roadmap.md`; split mode writes that main document plus `roadmap-delivery.md` when
selected delivery/schedule content exists and `roadmap-history.md` when revision
records exist. Delivery detail groups iterations/versions, phases/events and the
timeline; separate per-iteration/per-version files are not generated by this tool.
The main document retains compact delivery/event summaries and latest-five revisions,
with links to detail pages. History detail renders every supplied record and links
retained source history; supplied records need not contain all historical decisions.
Split mode does not move or edit authoritative source documents.

Selected schedules produce `roadmap.svg`; dated schedules also produce `roadmap.mmd`.
Relative weeks produce SVG and a timing table, never fictitious calendar dates.
Schema 1.3/1.4 single output uses the reading order above; legacy single outputs retain
their established structure. Explicit split rendering may reorganize older input.

All five fixed sibling filenames are reserved generated views. Source references
are already relative to the selected output directory; sibling layouts need no
rebasing. Files are deterministic UTF-8. Preflight every reserved path before
writing: reject symlink/nonregular paths, existing files without `--overwrite`,
aliases of the input (including hard links), and aliases between reserved outputs. Explicit overwrite also removes
stale reserved views when changing layout/selection; unrelated files are untouched.
Never place authoritative evidence at a reserved output path. I/O failures may leave
partial output and must be reported; generation is not a transactional filesystem.

### 5.4 Revision records

A material planning change MUST leave a durable revision summary when the roadmap
is created or maintained under this contract. Triggers are priority or tier changes,
version scope changes, phase additions/removals, dates or commitment changes,
material exclusions and milestone cancellation, missed or reached states. A
source-backed milestone event is not itself permission to change related work.
Routine wording, formatting and link corrections may remain in Git history.

Keep the latest five summaries, newest first, in the roadmap. Each contains a stable
revision ID, calendar date, before/after change, reason, impact and details/source
link. One coherent decision can cover several affected objects; do not log a
separate revision for every generated view or every tool invocation. A repeated
render or retry of the same decision reuses its ID. A correction appends a new
revision referencing the earlier decision rather than erasing its original facts.

Detailed evidence and complete history stay in existing decision/change records,
source documents or linked archive snapshots. Git preserves textual differences;
it does not replace the reader-facing reason and impact. Before shortening the
summary table, retain older decisions and verify their history link. A history
record can name an object removed from the current plan. History is neither a
current-scope declaration nor implementation/release approval.

For existing roadmaps, adopt a baseline on the actual adoption date and link known
history. Do not reconstruct unknown decisions, dates or owners from a current
snapshot. Earlier unverified history remains explicitly unknown. Existing single-view
plans and older generator schemas remain valid without automatic migration.

JSON 1.2–1.4 revision fields: `id`, `date`, `change`, `reason`, `impact`, `source`.
All are required strings. IDs use the entry identifier syntax, unique within revision
history, independent of current planning IDs. Date is ISO YYYY-MM-DD and must not
exceed the roadmap `updated` date. Records are newest first; equal dates preserve
explicit input order. Change summarizes before/after; source supplies the detailed
decision and actor/authorization evidence where applicable. Historical names do not
need to resolve to current records. Text/reference bounds and source-link validation
are the same as other records. At most 200 revisions may be supplied, separately
from the 200 planning-object cap. `revision_history` uses the source-reference syntax.
An empty revisions array states no material revisions were supplied, not that none
ever occurred. A linked history can still be supplied with an empty summary.

The generator renders only the latest five records and a full-history link; it does
not infer changes, append decisions or edit linked source history. Calling skills
must preserve durable history and carry the appropriate revision records forward
when regenerating. JSON 1.0/1.1 continue to ignore these unmodeled metadata keys.
SVG and Mermaid remain schedule views; the revision table is in roadmap Markdown,
not another set of Gantt activities.

### 5.5 Optional iteration view (schema 1.3)

Iterations express delivery cadence (for example, every two to four weeks), not
priority tiers. Record a source-backed cadence and near-term goals without forcing
a universal duration. Distant work may remain directional and unallocated. Version
membership says what ships together; iteration membership says where work contributes.
An iteration can deliver zero, one or several versions. A version or phase can span
iterations. Iteration end does not imply acceptance, phase exit, a reached milestone
or production release. Now/Next/Later are never aliases for iteration 1/2/3.

Fields: `id`, `name`, `goal`, `owner`, `members`, `source`, optional `board` (reference
or null). All text is nonempty and bounded by the common limits. Owner may be
`Unknown`. Members are a unique array of existing entry IDs; empty is permitted.
The same entry MAY contribute across iterations; this does not clone the requirement,
change its execution status or alter its unique version membership. Decompose a
partial deliverable in source records when independent acceptance is needed.
Source/board use the common reference syntax. Source holds decision/results evidence;
board links execution detail, not a competing roadmap. Do not invent actual results.

Timebox/basis derives from the existing schedule span for that iteration ID; absent
or null timing is Unscheduled. No duplicate iteration start/end or version field
is accepted as an authoritative timing/mapping source. Versions touched are derived
from entry membership. Iteration IDs participate in the shared object cap, schedule
validation and span exports, but phase scope/event relations retain their existing
entry/version/phase contracts. Relate an iteration-end approval event to its actual
work scope rather than inventing automatic lifecycle coupling.

Schema 1.3 inherits 1.2 revision requirements. Iteration goal/scope/cadence/timebox
changes are material planning changes and use the same revision mechanism. Rendering
never generates a decision. Schemas 1.0–1.2 ignore unmodeled iteration metadata and
reject selecting the iterations view; there is no silent upgrade.

### 5.6 Context, recommendations and retained selection (schema 1.4)

A new plan MUST first inspect existing norms, roadmap choices and linked execution/
release records. Extract known facts and their sources. Ask only unresolved facts
that change the recommendation; bundle questions about work cadence, delivery mode,
audience and constraints instead of presenting a blank menu of four concepts.
A source-location gap is resolved by inspecting records or retaining the user's
explicit statement in the existing decision record, not demanding a new document.

Give a concrete recommendation: primary perspective, enabled/supporting views,
omitted views and why, single/split layout, source basis and uncertainty. Scenario
recipes are context-sensitive project advice informed by primary guides, not
mandatory framework rules or certification. Teams may combine or tailor them.
A clear user choice or prior authorization counts; never repeat a settled approval.
Record the selected combination and rationale in existing norms or the roadmap's
source. Do not require another ongoing configuration file.

On maintenance, reuse existing views, primary perspective, layout and destination.
New optional features do not require a fresh interview or schema migration. If
choices exist only in old Markdown/input, infer no new context: retain the actual
selection, disclose uncertainty and use the compatible format. If sources conflict
or team/delivery needs materially change, retain current choices while presenting
a focused reconsideration proposal. Do not overwrite them from a fresh default.
A material selection/cadence/scope change uses one revision with its source decision.

For 1.4, `selection` has `scenario` (iterations/flow/staged/discovery/custom), `primary`
(requirements/iterations/versions/phases/flow), `layout` (single/split), `rationale`,
`source` and `context`. Context contains `work_mode` (iterations/flow/staged/discovery),
`delivery` (continuous/versioned/acceptance), `audience`, `constraints`, `source`.
Text/reference bounds are unchanged. Use explicit no-constraint statements when
appropriate. Sources must support the decision and facts, not merely link a guide.
`primary` MUST be in top-level `views`; requirements remains required. A custom or
hybrid choice can differ from its context's default recommendation with a rationale.
Destination stays the caller's established path/tool choice, not a duplicate JSON field.

In 1.4, phases and milestones render only when independently selected in `views`;
selected arrays must be present (empty is allowed). Unselected record metadata may
remain for traceability but does not enable a register. A selected schedule may
still plot supplied phase/event timing independently of its detail register.
No occurrence, approval or completion is inferred from selection. Older schemas
retain automatic optional registers and do not gain 1.4 behavior implicitly.

The `flow` view links workflow/board and summarizes source-backed `policy`,
`expectation` and `metrics`; `source` and `board` are required references. It is a
roadmap summary, not a new task board or a flow-metrics calculator. WIP limits,
service expectations and baseline values come from project records; unknowns are
explicit, never default numeric targets. Flow adds no fake iteration or version.

CLI `--recommend` reads partial `planning_context` and optional existing `selection`
plus top-level `views`. It writes JSON to stdout and creates/modifies no files;
it does not generate source facts or apply recommendations. Missing/unknown context
returns `needs-input`, `missing` field names and focused `questions`, with no view
proposal. With complete new context it returns `proposal`, scenario/primary/views,
single layout, rationale, source, optional schedule and a non-application notice.
The simple recommendation uses declared work/delivery modes; audience/constraints
remain evidence for human/skill tailoring rather than keyword heuristics.

With an existing valid choice, recommendation returns `retained` with its exact
views/primary/layout, even for custom combinations. Different supplied context returns
`retained-review-needed`, the unchanged choices and remaining questions. Malformed
choices/context fail explicitly; they never fall back to a fresh default. These
results are advice, not plan approval. `--recommend` cannot combine with `--check`,
output, overwrite or layout flags. Missing information is a valid diagnostic result
(exit 0); malformed input exits nonzero. All normal input-size bounds apply.

Generation of 1.4 requires settled context/selection and renders its source and
rationale. Layout defaults to the saved choice; a conflicting explicit `--layout`
fails before writes. Update the source selection first for an authorized layout
change. For old schemas omitted layout still means single. Schemas 1.0–1.3 remain
valid without selection records; ignored selection metadata is not a saved choice.
For valid 1.0–1.3 inputs, recommendation returns retained views without asking
for new context; primary/layout are null with an instruction to inspect the existing
roadmap. Legacy selection metadata remains ignored.
No recommendation reads project files beyond its input; calling skills perform
source discovery, ask questions and verify authorization.

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
