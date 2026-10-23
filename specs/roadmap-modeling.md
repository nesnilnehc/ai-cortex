---
id: ROADMAP_MODELING_SPEC_V1
name: Roadmap Modeling Schema
description: Roadmap views, source authority, priority vocabulary and local generation input contract.
version: 1.11.1
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
New independent phase/event records use 1.1–1.6. Revision summaries use 1.2–1.6. Their registers appear only when
records exist; no additional view or lifecycle gate is compulsory.

## 5. Body structure contract

### Structure before content

For new roadmaps and authorized structural redesigns, settle the reader entry,
selected/omitted views, document responsibilities, titles, fields and navigation
before populating business content. Reuse an established structure during routine
maintenance. Existing user choices or authorization can settle this step; do not
add a mandatory approval ceremony. If the user requests structure confirmation
first, deliver that inspectable structure and stop before business population.

A **structure draft** contains headings, consistently styled standalone field labels
(bold under the default Markdown style), placeholders, empty table headers and
necessary navigation. It has no invented
planning objects, source facts, commitments or historical revisions. Required
fields remain visible even when unknown. No fixed number of iterations, versions,
milestones or files is implied. Structure-first is sequencing, not an interview
that asks the user to fill each field.

A **populated plan** uses the settled structure and source-backed decisions.
Structure review checks roles, field coverage, naming, navigation, formatting and
absence of author guidance. Business completeness, readiness and source-dependent
claims are not evaluated on an intentionally empty draft. State the review scope;
a structure-only pass is not a complete roadmap pass.

Keep the settled structure during population. A material layout change requires
explaining its reader benefit and affected links, and resolving any new choice
before applying it; existing authorization remains sufficient for routine repair.

Conformance to this Spec, use of a template, and exact replication of a named
example are distinct claims. Identify the reference and disclose differences;
custom compatible layouts are not exact replicas. A repeated review with no new
finding or evidence leaves the artifact unchanged.

### Stage entries, authorization and acceptance

Structure design and content planning are stages of the existing roadmap capability,
not separate Skills or document statuses. Select the entry from the current request
and retained decisions, independently of whether the files already contain facts.

| Entry | Inputs and permitted work | Boundary and acceptance |
| --- | --- | --- |
| Structure only | Readers, existing layout or authorized layout choice, template and destination; settle roles, titles, fields, navigation and presentation | Deliver an inspectable empty structure for a new draft, or preserve business facts during structural repair of an existing plan. Validate all selected files and links; content is not evaluated. Stop before content work. |
| Content on settled structure | Retained structure, source records, existing business decisions and authorization to plan or populate | Reuse the layout and fill or maintain source-backed content. Check completeness, readiness, cross-view consistency and traceability; expose unknown facts and unresolved choices. Do not reopen layout without a material new issue. |
| Continuous structure and content | Authorization for both stages and sufficient evidence or already settled layout | Settle structure first, validate it, then populate and review content in the same request. No intermediate confirmation is required unless the user reserved it or an unresolved material choice blocks continuation. Report the two stage results separately. |

Review has an independent scope: structure, content, or both. A structure-only
review of a populated plan checks organization without erasing facts, fetching
business evidence or claiming content approval. Content review includes the
structural consistency needed to interpret facts but does not reopen settled
presentation choices. Read-only review never repairs files or initiates planning. If content review is
explicitly requested on an empty draft, retain that scope: report the missing
business basis and applicable checks as cannot evaluate, without population,
a full content pass or silently substituting a structural-only review.

Structure confirmation, source availability, a template example or an earlier
structure pass alone grants no content-planning authorization. Content work grants
no authority to replace settled priorities, tiers, version membership, cadence or
delivery commitments, implement work, or publish externally. Present unresolved
business changes as options with evidence and impacts; wait for the relevant
choice while completing independent authorized work. Read-only fact verification
can continue where needed for authorized content work. Separate unknown facts to
verify from decisions the user must make; neither is invented to finish a table.

Report scope, applicable checks, result, evidence limitations and the next boundary
in the response or existing review record, never as agent instructions inside the
roadmap. A structural pass does not certify content. An incomplete content plan can
be delivered with explicit gaps but cannot receive a full applicable-criteria pass.
Reuse confirmed structure on resumption; do not require a new interview, mandatory
configuration file, extra artifact or approval ritual for these stage entries.

### First alignment of an existing project

An explicit request to align an existing project's requirements/roadmap to this
contract authorizes structural and presentation repair, not replanning. Discover
the actual plan and source locations before treating a missing default filename
as a missing artifact. First review records structure gaps separately from missing
facts, conflicting sources and proposed business changes.

Preserve settled priorities and relative order, tiers, approval/execution facts,
scope, ownership, dependencies, delivery groups, dates and commitment basis, pauses,
closure criteria, selected views, destination and language. Retain stable item IDs,
page URLs, source links and inbound heading/explicit anchors. Do not infer a source
fact from a template, rename an item to manufacture compliance, apply tier defaults
again, create delivery objects or reconstruct unknown history. Preserve established
source-label meanings until any required mapping is supported. Unknown tier/priority
or execution mapping remains explicit; it is not assigned a default to fill a row.

The define capability repairs needed structure in place; maintenance handles only
separately authorized source-backed state/time corrections. Missing source requirement
registration goes to intake under its own authorization; reconciliation of conflicting
facts, priority reassessment and placement changes remain separate decisions. Missing
strategy or policy is reported as an evidence gap rather than automatically authored
to satisfy a later planning step. Adequate existing decisions need no new approval.

Existing requirement-body alignment follows the Requirement Spec's lifecycle rules:
review it through the requirement reviewer, repair authorized drafts through the
requirements repair loop, and leave frozen approved/implemented/superseded originals
intact. Alignment alone does not authorize a successor revision, new identity or
automatic approval. Do not recapture an existing requirement as a new unset item.

Compare known facts and protected links before and after the proposed repair. Retain
the actual adoption date and unknown earlier history; formatting-only repair is not
falsely recorded as a business planning change. Re-review after repair and report
remaining limitations; an aligned presentation with unresolved facts is not a full
governance pass. A repeat run with no new gaps makes no change. The JSON generator
remains optional: if it cannot preserve a nonstandard filename/anchor or unknown
planning field, repair the existing document manually instead of migrating it or
inventing facts. Established safe links are not rejected merely because this optional
rendering interface uses a narrower reference grammar.

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

1. Overview: direction, update date and a concise explanation of the current
   arrangement. Summarize known near-term outcomes and material unknowns when they
   change how the plan should be read; do not repeat the item inventory.
2. Priority arrangement: requirements/defects and their material conditions.
3. Delivery plan, when selected: iteration and/or version planning, with relevant
   phases and milestone events grouped beneath it.
4. Timeline, when selected: primary diagram, unknowns and timing exceptions;
   a detailed timing table may be folded or linked.
5. Latest revisions.
6. Planning basis and sources: priority policy, closure basis, retained view/layout
   and language evidence, and source/detail links. Use short summaries and links;
   maintenance metadata does not take precedence over the plan.

The overview is a reader summary, not a mandatory form of additional fields. Put
unverified execution evidence before the requirement table so placement is not
mistaken for actual progress. Summarize immediate decisions/unknowns there only
when supported; detailed dependency chains remain in the rows and linked sources.
The policy and closure basis remain recoverable from the main document even when
their full definitions live elsewhere. Existing plans need no automatic rewrite.

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
and events normally stay with the related delivery plan. A topic-split combination
may instead use a main roadmap plus iteration, version, milestone, planning-basis
and revision-detail documents, with the timeline in the main. This is an optional
reader-oriented combination, not six mandatory files. Do not split every field,
empty section or individual object into a file without a reader/ownership need.
Gantt is a derived view, not an additional planning authority. Every detail page links back to the main plan.

For each fact, declare one editable source (requirement, iteration board, version
plan or decision record). Main/detail summaries are linked or generated projections.
When a planning decision changes, refresh every affected projection and retain one
revision ID. Do not maintain separate editable copies of scope or dates. Detailed
iteration tasks, daily progress and individual assignments remain on execution
boards; the roadmap carries goals, scope and links. Sources are resolved relative
to their containing output document, not the temporary input file.

### Remote authority and delivery evidence

A roadmap family can live entirely in a knowledge base. Its established remote
pages are then the editable planning authority; repository pointers, exports and
temporary renderer input are not competing plans. Requirement/execution systems
retain authority over their own facts. Declare ownership per fact, including
iteration timeboxes, version members and milestone targets, in the existing planning
basis or project entry. Summaries and charts are projections refreshed for the
same authorized change, whether by an agent or an explicitly installed automation.
One publication or refresh never implies continuous synchronization or monitoring.

Remote acceptance has three distinct evidence levels: source agreement, stored
read-back integrity and rendered usability. A successful write is not evidence of
the latter two. Compare protected identities, links, anchors, rich cards, retained
history and unrelated content against the pre-edit snapshot; verify source-backed
scope/date/state assertions in every affected projection. A short display title may
change independently of its URL. Keep project names out of titles when book context
already identifies the product, unless needed to distinguish pages. Reader dates
use actual intended dates; serialization boundaries, timezone mechanics and author
instructions stay out of the reader document unless materially relevant.

Capture a fresh target immediately before writing. If its body, title or revision
differs from the read used to prepare the edit, re-read and reconcile rather than
overwrite it. Use conditional writes when supported; a read/compare fallback is not
an atomic lock. Report residual races or partial multi-page delivery and re-read
affected pages. Do not blindly retry an unknown write outcome. Retain unresolved
business decisions; do not infer completion from historic closures or expired dates.

Scope verification to affected properties. For a metadata-only title change, exact
read-back equality of the rich body can reuse unaffected body/chart evidence;
verify the new title and directory instead of rewriting content or rerunning every
renderer probe. Changes to content, assets or rendering support need corresponding
fresh observations. Reuse still-valid capability evidence; do not perform test writes
as part of a read-only review or outside authorized probe/publication scope.

Captured acceptance evidence distinguishes these records; concrete platform payloads
belong to the selected adapter, not the roadmap business schema:

| Record | Fields and meaning |
| --- | --- |
| Document snapshot | Stable document identity/URL, display title, rich body and revision; rendered source when needed to discover legacy anchors |
| Rendering observation | Meaningful section/compatibility anchors, loaded assets, and observed navigation/chart/readability results for affected content |
| Acceptance contract | Expected titles, protected source/navigation links and anchors, source-derived content assertions, historical originals and intended rich-object changes |

These are transient verification inputs, not a new persistent planning schema or
mandatory project file. The checker must reject missing/duplicate document sets,
lost protected stored/rendered anchors or required links, duplicate anchor IDs,
broken in-scope section links, unintended card/history changes and absent required
observations. Do not turn transient editor-generated block/text IDs into permanent
public anchors. Known inbound fragments and declared compatibility aliases remain
protected. Out-of-scope links are reported separately.
Text assertions supplement semantic review; they cannot establish source truth,
detect every unsupported conclusion or authenticate a screenshot/DOM observation.
Fixtures and captured evidence do not themselves establish a live integration pass.

### Migration closeout

Removing a superseded local plan requires explicit cleanup authorization and a
reviewed inventory of exactly the files being retired. Before removal, account for
all unique decisions, unknowns, exclusions, source references, complete revision
history and reproducible diagram sources at the chosen destination. Classify
differences as preserved, linked, corrected or unresolved; do not use raw byte
equality to reject valid platform presentation, or treat unexplained omissions as
migrated. Read back the destination and inspect affected page/chart behavior.
Unresolved migration gaps block removal of the affected files, not independent work.

Check inbound repository links and consumers, including README and agent entries.
Keep a verified recoverable snapshot when normal version history cannot restore
the originals, especially for untracked files. A recovery archive is a dated backup,
not an editable plan. Remove only inventoried artifacts; unrelated files remain.
Update existing pointers and remove stale pending-publication/local-draft wording
from living content. Preserve historical originals and legitimate local-deployment
facts. Verify no dangling retired-path references remain. Publication alone does
not authorize deletion, commits, source-system changes or installation.

### 5.2 Priority vocabulary

Default planning vocabulary: P0 (highest), P1, P2, P3 (lowest); `unset` is unresolved,
not a low priority. Project policy defines business meaning and exceptions.
Nonstandard source labels require an explicit mapping before comparison. Existing
P0–P2 records remain valid; do not silently reinterpret their historical meaning.
Tier placement is a separate decision based on readiness and project priorities.

### Policy, decisions and arrangement rationale

The priority policy is the reusable rule for relative treatment precedence, not
merely an importance label. It may consider value, urgency, dependencies and cost
as the project decides. Priority levels and any necessary same-level order are
decisions under that policy. An arrangement rationale explains how those decisions
and verified conditions produced the current sequence or tier placement; it is not
a second scoring policy or a requirement to reassess settled priorities.

Keep one editable policy source. The roadmap links it with only the summary needed
to understand the plan; a bare link is valid when sufficient. Reuse an existing
priority/placement decision instead of requiring another rationale document. A
policy's current application links to item/roadmap records rather than maintaining
a second live inventory. A retained decision snapshot is identified as historical.
Same-level items may be explicitly tied. Stable ID/path display order alone is not
a business decision about which item must start first. Existing tier defaults remain
overridable advice; this distinction removes neither levels nor planning tiers.

### Prerequisite readiness

For a proposed start or next step, identify the required deliverable and when it is
needed from source evidence. That deliverable must be available before the step;
the entire supplying requirement need not be complete. A dependency needed only at
a later step permits parallel work when sources establish that the current step
can proceed and expose the later condition. An unchecked dependency is unknown,
not evidence of either readiness or blockage. Neither mapping nor placement changes
execution status or automatically raises a prerequisite's priority.

### Document-family naming

These are default role-based names, not mandatory separate documents:

| Role | Suggested title | Suggested local name |
| --- | --- | --- |
| Current plan and entry point | Roadmap | `roadmap.md` |
| Reusable priority rules | Requirement Priority Policy | `priority-policy.md` |
| Planning facts and selection decisions | Roadmap Planning Basis | `roadmap-planning-basis.md` |
| Detailed delivery and timing | Delivery Plan and Timeline | `roadmap-delivery.md` |
| Retained changes and decisions | Roadmap Revision History | `roadmap-history.md` |

Names MUST distinguish policy, current plan, supporting evidence and history.
Prefer concise role names when the surrounding project/book supplies context;
rename an authorized display title without changing a stable page URL or source ID.
Combine small topics or link existing authorities; do not create a document just
to fill this table. Living titles/paths SHOULD be stable without date suffixes;
identify snapshots/drafts explicitly under project conventions. Page display titles,
URLs and local filenames are different surfaces. Preserve established titles/URLs
and inbound links; naming advice never authorizes a migration. The renderer's
reserved sibling filenames below remain a tool contract, not a platform title rule.

### 5.3 Optional local generator interface

The JSON input is a transient rendering interface, not a required project file or
a second editable source. It represents verified facts; the generator does not
infer missing priorities, owners, dates or dependencies.

| Field | Type | Requirement |
| --- | --- | --- |
| `schema_version` | string | `1.0` (legacy), `1.1`, `1.2`, `1.3`, `1.4`, `1.5` or `1.6` |
| `project`, `updated`, `direction`, `ordering`, `closure`, `priority_policy` | string | Required, nonempty; updated is an ISO date; direction states the goal served and ordering explains the sequence |
| `views` | array | Unique subset of `requirements`, `versions`, `schedule`, plus `iterations` in 1.3+ and `phases`, `milestones`, `flow` in 1.4+; requirements always included |
| `entries` | array | Requirement/defect records; may be empty |
| `versions` | array | Required when versions view selected |
| `schedule` | object | Required when schedule view selected |
| `iterations`, `cadence` | array, string | In 1.3+, required when iterations view selected; records may be empty; cadence is nonempty source-backed text |
| `revisions` | array | Required in 1.2–1.6, including an explicit empty array for an adopted baseline; not modeled in earlier schemas |
| `selection` | object | Required in 1.4+; source-backed scenario, primary perspective, layout, rationale and context; top-level views are the only enabled-view list |
| `flow` | object | In 1.4+, required only when flow selected; workflow policy, expectation, metrics and source/board links |
| `revision_history` | string or null | Optional full-history reference in 1.2–1.6; required when more than five revision records are supplied |

Unmodeled keys may be retained as input metadata but do not affect generated
views. In particular, only milestone records own the modeled event `state`;
a similarly named field on a version, phase or entry is not an event status.
The explicit 1.0 prohibition on `phases`/`milestones` still applies.

The existing `ordering` field supplies the current arrangement explanation, not a
second priority rule. In modern main output (1.3–1.6 and explicit split layout),
policy/closure/selection/language evidence follows revisions. A source-only
`priority_policy` string renders as a link; recognized forms are HTTP(S), fragments,
explicit `./` or `../` paths and bare `.md` paths with optional fragments. These
references follow the common reference contract. Other values remain escaped prose.
Legacy 1.0–1.2 single output retains its existing presentation. No new input field,
mandatory policy file or schema migration is introduced.

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

In 1.1–1.6, schedule kind `span` references entries, versions, phases or 1.3+ iterations; kind `milestone`
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
in 1.1–1.6 unscheduled milestones retain kind milestone and have no plotted marker. One missing endpoint,
an inverted span, mixed time modes, duplicate dependencies and cycles are invalid.
Finish-to-start dependencies must not overlap; unknown endpoints leave timing
unverified and are reported. This is validation, not resource scheduling.

Input is capped at 1 MiB, 200 total planning objects (including 1.3+ iterations), 200 schedule items and
200 characters per text field. Larger roadmaps must be split. Schedule horizon
is capped at 366 calendar days or 104 weeks to preserve readable output.

The original layouts are `--layout single` (default) and `--layout split`; schema 1.6
also supports the topic layout defined in §5.8. Single mode writes
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
Schema 1.3–1.6 single output uses the reading order above; legacy single outputs retain
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

JSON 1.2–1.6 revision fields: `id`, `date`, `change`, `reason`, `impact`, `source`.
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

For 1.4+, `selection` has `scenario` (iterations/flow/staged/discovery/custom), `primary`
(requirements/iterations/versions/phases/flow), `layout` (single/split; 1.6 also permits topic-split), `rationale`,
`source` and `context`. Context contains `work_mode` (iterations/flow/staged/discovery),
`delivery` (continuous/versioned/acceptance), `audience`, `constraints`, `source`.
Text/reference bounds are unchanged. Use explicit no-constraint statements when
appropriate. Sources must support the decision and facts, not merely link a guide.
`primary` MUST be in top-level `views`; requirements remains required. A custom or
hybrid choice can differ from its context's default recommendation with a rationale.
Destination stays the caller's established path/tool choice, not a duplicate JSON field.

In 1.4+, phases and milestones render only when independently selected in `views`;
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

Generation of 1.4+ requires settled context/selection and renders its source and
rationale. Layout defaults to the saved choice; a conflicting explicit `--layout`
fails before writes. Update the source selection first for an authorized layout
change. For old schemas omitted layout still means single. Schemas 1.0–1.3 remain
valid without selection records; ignored selection metadata is not a saved choice.
For valid 1.0–1.3 inputs, recommendation returns retained views without asking
for new context; primary/layout are null with an instruction to inspect the existing
roadmap. Legacy selection metadata remains ignored.
No recommendation reads project files beyond its input; calling skills perform
source discovery, ask questions and verify authorization.

### 5.7 Deliverable language (schema 1.5)

This contract governs roadmap deliverables in consuming projects, not the language
of AI Cortex's own asset instructions. Resolve language before writing new prose:

1. Follow an explicit artifact-language instruction from the user.
2. Otherwise follow the consuming project's applicable language policy.
3. Otherwise retain the existing artifact's language during maintenance.
4. For a new artifact, infer from intended readers and comparable project documents
   only when the evidence supports one language. Conversation language alone is not
   an artifact-language decision.
5. Ask a focused question when the winning level is conflicting or evidence is
   insufficient. Do independent work while waiting; do not guess or overwrite prose.

Lower-priority evidence cannot overturn a settled higher-priority instruction.
An explicit new user instruction needs no second confirmation. Show a proposed
change when new evidence differs from a retained choice; update its source decision
before regeneration. Store the locale, basis, rationale and evidence link in existing
norms or the roadmap's planning decision. No separate configuration file is required.
Pass that choice across planning skills; do not repeat the interview at every step.
Legacy documents without metadata remain valid: inspect their actual language.

Use one selected language for headings, table headers, summaries, free-text outcomes,
conditions, approval display labels, revisions, diagram labels, legends and accessible
descriptions across main/detail documents. Preserve original evidence and immutable
historical records; translate summaries without altering meaning, status or authority.
A separately requested bilingual edition uses two aligned outputs, not accidental
mixed labels. IDs, paths, URLs, commands, field names, enums and Mermaid directives
remain stable English machine values. Proper names and quoted source text may remain
in their original language. Execution display labels have the same seven meanings
as the Rule: Not started → 未开始; In progress → 进行中; Awaiting acceptance → 待验收;
Awaiting release → 待发布; Paused → 已暂停; Blocked → 受阻; Completed → 已完成.

Schema 1.5 inherits 1.4 and requires `language`:

| Field | Contract |
| --- | --- |
| `locale` | `en` or `zh-CN`; unsupported locales fail explicitly |
| `basis` | `user`, `project`, `existing` or `context` |
| `source` | Resolving relative reference, fragment or HTTP(S) URL under the common reference rules |
| `rationale` | Nonempty explanation in the selected deliverable language |

Optional `language_context` contains evidence arrays `user`, `project`, `existing`,
`audience`, `documents`, each at most 20 records with `locale` and `source`.
Unknown levels and malformed records fail explicitly. The last two levels combine
as contextual evidence. At the first populated priority level, differing locales
produce `needs-input`; a unanimous locale resolves the choice. A saved language is
retained when no new context is supplied and otherwise supplies existing-artifact
evidence when that level is empty. Diagnostic results are proposals, never mutations.

`--resolve-language` accepts partial evidence or a saved choice and prints JSON only:
`status` is `resolved`, `retained`, `change-proposed` or `needs-input`; results carry
locale, basis, source, rationale and questions as applicable. It reads only the supplied
input, asks no interactive questions and writes no files. It cannot combine with
`--recommend`, `--check`, output, layout or overwrite flags. `--recommend` includes a
nested language result only for schema 1.5 or later, or explicit language context. Calling
skills discover evidence, ask gaps and retain the decision. Generation rejects
unresolved context or context whose resolved locale differs from the saved choice,
before writing files. Keep the saved basis and source current when accepting advice.

The renderer localizes only its own display strings through the bundled catalog.
It neither translates arbitrary source text nor proves that supplied prose is in
the selected language. The calling skill prepares that prose; review checks meaning
and consistency. Missing catalog entries fail instead of silently mixing English.
CLI diagnostics and machine JSON keys remain English. Schemas 1.0–1.4 retain their
English rendering and do not acquire mandatory interviews or metadata. Adopt 1.5
explicitly for localized generation; ordinary maintenance needs no schema migration.
The define-roadmap capability provides the language workflow and paired examples.

### 5.8 Blank structures and topic layout (schema 1.6)

Schema 1.6 inherits 1.5, including language evidence, and adds `topic-split` to
`selection.layout`. Schemas 1.0–1.5 retain their original single/split contract;
passing a conflicting CLI layout still fails rather than replacing a saved choice.
The topic layout writes exactly six Markdown roles: `roadmap.md`, `iterations.md`,
`versions.md`, `milestones.md`, `roadmap-planning-basis.md`, `roadmap-history.md`.
The main carries requirement arrangement, delivery summaries, timeline and latest
five revisions. Details retain the complete supplied revisions and source links.
Selected phase/flow records remain in planning-basis source context, not silently
lost or expanded into additional files. A selected schedule also produces SVG and,
for calendar dates, Mermaid. Blank and populated topic output preserve the same
second-level headings and table columns; population does not redesign the structure.

`--blank [--locale en|zh-CN] [--layout topic-split] --output-dir DIR` needs no JSON
input and accepts no business input. It copies/localizes the clean blank topic
assets without creating IDs, dates, owners or business records. Only this layout is
supported for blank generation. `--blank --check` writes nothing and reports only
structure validity by checking emitted titles, field syntax, empty table shape and
internal navigation; reading template files alone is insufficient. Recommendation/
resolution modes cannot combine with blank mode.
For populated output, language comes from the retained input rather than `--locale`.

Blank and topic output use `.roadmap-outputs.json` as generated-file ownership
metadata, not another plan. Preflight checks all reserved topic files, graphics and
the manifest before writing; symlinks, non-files, hardlink aliases and input/output
aliases fail. Existing reserved output requires explicit `--overwrite`. Identical
writes preserve modification times. On reset, only intact stale files listed in
the manifest are removed. Unrelated files are left alone; modified stale outputs
cause failure before mutation. An invalid manifest fails closed. Without ownership metadata, legacy cleanup retains its original reserved scope;
only manifest-proven topic files can be removed during an owned layout transition.
When ownership metadata exists, transitions back to single/split use the same
intact-owned-file rule; they do not leave stale topic detail files behind. Unowned
reserved files outside the requested output set cause a pre-write refusal rather
than being deleted or silently left as a competing business draft.
I/O errors remain nonzero with a partial-output warning; atomic rollback is not promised.

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
