---
name: define-roadmap
description: Design roadmap structure, populate source-backed content on a settled layout, or complete both stages; first-align existing plans while preserving business decisions and stable links, with optional local generation.
version: 8.0.0
license: MIT
---

# Skill: Define Roadmap

## Purpose and scope

Turn project goals and existing requirements and defects into a readable plan.
Every requirement-view row is a requirement or defect. Now / Next / Later express arrangement,
not three mandatory strategic dossiers. Tasks, implementation steps, test procedures
and release operations remain in their source documents.

This skill creates or restructures the roadmap. It does not create requirements,
rescore priorities, break down tasks or approve execution. Use `capture-work-items`
for missing requirement or defect records, `promote-roadmap-items` for tier changes,
and `update-roadmap` for status and timing maintenance.

## Inputs and output

Read project norms, goals, the existing roadmap and source requirement and defect
records. Default output is `docs/process-management/roadmap.md`; preserve a project's
established path. The output is a living roadmap with a dated summary, a compact
Now/Next/Later view, optional version and schedule views, material boundaries and a References section. Load [roadmap modeling](../../specs/roadmap-modeling.md)
for view structure and generator input; the quality rule owns evaluation criteria.

## Procedure

### Select the stage entry

Resolve the [stage contract](../../specs/roadmap-modeling.md#stage-entries-authorization-and-acceptance)
from the current request and prior authorization before reading business systems
or writing content. Keep this inside the existing skill:

- **Structure only:** run structure design and structural Self-Check, return the
  inspectable draft and stop. On an existing populated plan, repair only authorized
  organization and preserve facts; do not reset it to blank without a reset request.
- **Content on settled structure:** resume at source inventory and content planning
  below. Reuse the confirmed roles, fields, navigation and destination; do not ask
  layout questions again. Verify relevant facts, distinguish them from unresolved
  business choices, and present options before replacing settled decisions.
- **Continuous structure and content:** perform and validate structure design, then
  continue into authorized content planning without another confirmation. Stop only
  at a user-reserved boundary or a material unresolved choice; complete independent
  authorized work while that choice is pending.

Report structure acceptance separately from content acceptance using the Spec's
criteria. Empty fields are valid in structure review. Unknown facts or undecided
commitments in a content draft are gaps, never evidence of full content approval.
Keep stage reports in the response/review record rather than the reader artifact.

### Existing-project first alignment

When the request is adoption/compliance alignment of an existing plan, use the
Spec's [alignment contract](../../specs/roadmap-modeling.md#first-alignment-of-an-existing-project)
before the creation procedure below. Read review findings, the actual plan and
source records; do not assume missing `roadmap.md` means no plan. Inventory known
business facts and stable IDs/URLs/anchors, classify structural fixes versus evidence
gaps and decision changes, and apply only authorized repairs. Preserve existing
scope/order/tiers/priorities, commitments and views; do not rerun initial selection,
default tier advice or strategy creation. Existing authorization is sufficient for
reversible structural repair; ask only for missing facts or separate business choices.

Repair in place and preserve anchor compatibility. Where requirements are missing,
report registration gaps and route to capture; do not turn tasks into invented
requirements or declare the whole requirement chain compliant. Keep unmappable states
or absent planning fields explicit. Use manual Markdown/platform editing when the
generator cannot preserve the original path, anchors or unknown fields. Compare
before/after protected facts and links, then re-run review. Report repaired gaps,
unchanged decisions, remaining evidence limitations and separately proposed actions.
With no new gap, leave the plan unchanged. See the
[complete adoption example](references/existing-project/README.md).

### Settle structure before population

Apply the Spec's [structure-first contract](../../specs/roadmap-modeling.md#structure-before-content)
before creation or authorized redesign. Identify readers, entry point, enabled and
omitted views, file responsibilities, headings, columns and navigation; use an
existing choice when sufficient. Resolve material layout choices before drafting
business content, without another approval ritual for already authorized choices.
Do not translate “independent content” into a file for every field or object.

For a structure-only request, use the [clean topic-split templates](assets/structure-first/roadmap.md)
and [authoring guide and paired example](references/structure-first.md) as an optional
starting combination. Keep placeholders/empty tables; do not import prior business
material, assign sample IDs, infer cadence or invent history. Retain the user's
selected layout and omit unselected views. Generate the six-role blank combination
with `python3 <skill-dir>/scripts/render-roadmap.py --blank --output-dir DIR`
and optional `--locale en|zh-CN`; no business JSON is accepted. `--blank --check`
checks the bundled structure without writes. For another layout, author it manually
rather than inventing a tool option.
Run structure/link/format review, report only that scope, and stop before population
when the user requested confirmation. Subsequent business work resumes from the
settled structure rather than reopening it.

For populated outputs, keep authoring instructions in the guide and source-backed
reader explanations in the artifact. Existing template modules are composition
instructions, not text to copy into deliverables. Name the reference and disclose
differences whenever claiming template or example fidelity.

### Creation and authorized restructuring

1. Read project norms, existing choices and linked planning/execution/release records,
   protecting concurrent edits. Use the [scenario selection guide](references/scenario-selection.md)
   and [template combinations](assets/scenarios/README.md). Extract work mode/cadence,
   delivery mode, readers and constraints from evidence; bundle only unanswered
   questions that affect the recommendation. Do not ask known facts again.
   Propose a primary perspective, supporting/omitted views, single/split layout,
   rationale, source basis, uncertainty and maintenance cost. Recipes are starting
   advice, not mandatory framework rules. Honor an explicit choice or existing
   authorization; ask only unresolved product trade-offs. Retain the combination
   in existing norms/roadmap sources. Reuse established views/layout/destination
   during maintenance; new options alone trigger no interview or schema migration.
   When context conflicts or materially changes, retain current choices and present
   a focused reconsideration proposal rather than applying fresh defaults.
   Confirm a new destination only when not already explicit. Load
   [roadmap-quality](../../rules/roadmap-quality.md), the [base template](assets/roadmap-template.md),
   and the closest [complete scenario](references/scenarios/README.md).
2. Inventory requirements and defects with IDs, titles, source paths, priorities,
   approval states, execution evidence, project closure criteria and dependencies. Extract from existing sources before asking.
   If an input is only a task or task group, resolve its parent requirement or defect.
   Merge references to the same parent into one row. An independent defect may have
   its own row linked to the affected requirement. Never invent a parent or approval;
   report missing registration and hand off to `capture-work-items`.
3. Preserve established priorities, pauses and capacity decisions. Arrange eligible
   records using priority, readiness and existing user decisions. State blockers
   separately from priority; missing prerequisites do not make a P0 item low priority.
4. Use a concise title that names the capability or problem. Keep additional outcome
   detail in the linked source. Keep approval and execution status in separate columns. Map source evidence to exactly one execution
   label from the quality rule; report unresolved mappings outside the status cell
   without guessing. State or link the existing project closure criterion.
   Development completion, acceptance and production release remain distinct.
   Do not add or waive a project gate.
   Summarize blockers that affect placement or delivery outside the table. Link their
   sources and keep prerequisites and acceptance criteria there. Empty tiers are valid.
5. Show the direction, current arrangement, near-term outcomes and material unknowns.
   Surface unverified execution before the rows. Keep the rationale, policy and
   closure definitions, cadence, and selection/language evidence in supporting
   documents linked from References. Follow the Spec's document-family naming advice
   and preserve established URLs. Link exhaustive inventories, task lists and evidence. Add metrics or hypotheses only when they affect a real decision;
   do not fill sections or invent numbers to satisfy a template.
6. For selected iteration views, collect cadence, goals, entry scope, owners,
   timeboxes and source/board links; derive version mapping from entry membership.
   Keep far-future work directional and unallocated when not decided. For selected
   version views, group source IDs by the existing delivery decision;
   retain unassigned work and unknown owners/windows visibly. For selected schedules,
   gather known spans, milestones, timing basis and dependencies; use relative weeks
   when the start date is unknown. Do not invent dates, auto-schedule resources or
   use a group status as evidence of member acceptance. See [generation](#local-generation-and-delivery).
   Review against the quality rule. Summarize current priorities, subsequent work and
   key blockers from the main view alone. If that requires task lists or evidence
   reports, revise the main view; remove detail that does not change those answers.
7. Apply the user's authorized scope. Ask only about unresolved product tradeoffs or
   missing facts that prevent a sound plan; do not repeat an existing authorization.
   Persist the dated roadmap and report changes and evidence limitations.

## Boundaries

- Only requirements and defects are requirement entries; version groups reference them, phases scope their work, and
  independent milestones relate to entries, versions or phases (or are global). Task IDs and task groups are not requirement entries.
- Preserve source status and authorization; inclusion is not approval to implement or release.
- Link one source of truth for detailed progress and acceptance.
- State that backlog requirements and defects map to the roadmap and that items outside
  it are not done by default.
- Follow explicit project capacity decisions; introduce no default quotas or item limits.
- Template structure is presentation guidance, not a reason to pad content.

## Self-Check

Apply these checks to the requested stage. For a structure-only scope, source-dependent
business, execution, schedule and publication checks are not evaluated; passing the
structural subset does not claim the populated-plan checks passed.

- [ ] Stage entry, existing authorization and stage-specific acceptance were resolved; continuous work did not add an unnecessary confirmation, and content work reused settled structure.
- [ ] Structure was settled before population; an explicit structure-only request retained empty business fields and stopped at its requested boundary.
- [ ] Review scope and example differences are explicit; no author guidance leaked into the artifact and no unnecessary files were introduced.
- [ ] For a populated plan, project norms, goals, source records, quality rule, template and example were read.
- [ ] Every entry is a linked requirement or defect; parent references are consolidated.
- [ ] Priority, approval, pauses, prerequisites and authorized capacity are preserved.
- [ ] Tier precision is appropriate and completion or start conditions are recoverable.
- [ ] The main view explains priorities, subsequent work and blockers without task detail.
- [ ] The main shows planning results and material unknowns. References reach the supporting rationale, rules and history where applicable. Iteration plans stay separate.
- [ ] Approval and execution columns are separate; every execution cell has one fixed label.
- [ ] Material blockers are brief and linked outside the table. Closure criteria and source-backed status mappings were checked.
- [ ] Detailed progress and evidence remain in their source documents.
- [ ] Applicable quality criteria were checked; alignment with unresolved source facts reports limitations rather than a full pass, and no unverified fact was invented.
- [ ] The requested change is persisted with its update date and authorization scope respected.
- [ ] Selected views and destination are grounded in user choice; all selected views agree.
- [ ] Tool validation, SVG inspection and destination receipts or limitations are reported.
- [ ] First alignment preserved known business facts and stable links, repaired only authorized structure, and was re-reviewed without automatically running planning steps.

## Local generation and delivery

Use `python3 <skill-dir>/scripts/render-roadmap.py INPUT.json --check` to validate
temporary facts under the Spec, then pass `--output-dir DIR` and optionally
`--layout split` (legacy default `single`; schema 1.4 reuses its saved layout) for the selected local
destination. Use `--overwrite` only for confirmed replacement of reserved generated
filenames. Never overwrite authoritative evidence or treat the temporary JSON as
a second project plan. The generator emits Markdown and, when selected, SVG and
dated Mermaid; inspect the SVG in a local browser or image-capable viewer. If Python
is unavailable, prepare the same views manually and state that tool validation did
not run. No runtime dependency installation is permitted.

Read the [generator example](references/service-desk/initial/input.json). Preserve the user's
source links relative to the chosen output path; the generator does not relocate
project records. Copying a roadmap to a new directory requires rebasing relative links.

For a knowledge-base destination, discover available document read/write and image
upload tools, map them to the selected operation, read the latest target before
editing and preserve unrelated content. Verify Mermaid support with a small preview
before relying on it. Check disclosure-element support as well; if unavailable,
expand folded content or use authorized linked detail pages without hiding facts.
If native rendering is unavailable, use supported image upload
and retain source access. If upload/write is unavailable, report undelivered views
and the local output location; do not silently switch destination or claim publication.
External writes require the user's explicit destination/publication authorization.
This capability performs one delivery, never continuous or bidirectional sync.

For remote authority or migration, apply the Spec's
[remote delivery and closeout](../../specs/roadmap-modeling.md#remote-authority-and-delivery-evidence).
Read the [platform delivery guide](references/platform-delivery.md); for Yuque load
its linked adapter only when that destination is selected. Preserve rich markup,
fresh-read conflict checks and separate stored versus rendered acceptance, scoped
to affected properties rather than every editor-generated ID. Reuse unaffected
body/chart evidence for metadata-only edits and still-valid platform probe results. After
publication, account for unique local facts/history and diagram sources before any
authorized cleanup. Check recovery and inbound references; do not delete unrelated
files or create another editable local plan. Report incomplete views and evidence.

## Filled deliverable example

[Complete Service Desk deliverables](references/service-desk/README.md). This is a fictional completed output, not a template
or authorization to change the adopting project.

## Phase and milestone contract

Resolve roadmap concepts from the [Roadmap Spec](../../specs/roadmap-modeling.md).
A version groups deliverables; a phase spans work; a milestone marks an event.
Keep the delivery outlook to versions and milestones. Keep phase details in their
sources or the planning basis.
Collect milestone category, related IDs,
owner, occurrence criterion, state and evidence when these views are useful.
Do not insert events as fake requirements. Use JSON 1.1 or later for independent records;
retain 1.0 and single-view compatibility. Give version spans and approval/release
points separate IDs. Missing event dates remain unknown, never inferred.

Self-check: concepts, selected views and linked evidence agree with the source records.

## Revision history maintenance

At initial creation or structural refresh, apply the [revision contract](../../specs/roadmap-modeling.md#54-revision-records).
Resolve existing decision/history sources before writing. Keep dated entries and
source links in a separate history document or directory linked from References.
An initial baseline may have no revisions. For a legacy roadmap, disclose adoption and unknown earlier history;
do not fabricate old decisions. Use schema 1.2 or later when generating revision summaries.
Read existing history before overwrite and carry retained records forward. The
renderer presents supplied decisions; it does not discover or append them.

Self-check: material changes are traceable, retained links resolve, and repeated execution adds no duplicate revision.

## Document layout and iterations

Apply the [reading and ownership contract](../../specs/roadmap-modeling.md#reading-order-and-document-boundaries).
Show overview, priorities and selected delivery results in the main. Keep rationale,
rules and revisions in supporting documents and link them from References.
Keep the main independently useful, with near-term delivery, key events and blockers.
Split delivery detail when readership, ownership or volume justifies it. Each
supporting page links back. Keep one editable authority per fact.

Manage iteration goals, cadence, timeboxes and allocations in an independent plan
or execution board. Schema 1.3 or later can export that plan separately. Keep
iteration rows out of roadmap delivery views and charts. Single and split generation
produce a planning-basis document and a history document when revisions are supplied. Split
can also produce delivery details. Read source history before replacement and
verify all navigation/source links and stale-output cleanup within overwrite scope.
For manually split iteration/version plans, respect established paths and ownership.

Self-check: the main alone explains priorities, blockers and delivery; selected
delivery views agree, navigation resolves, and each fact has one authority.

## Scenario selection and generation

Follow the [selection contract](../../specs/roadmap-modeling.md#56-context-recommendations-and-retained-selection-schema-14).
Use the shared base plus selected modules instead of copying four complete templates.
The four recipes cover iteration products, continuous flow, staged delivery and
learning pilots; custom combinations remain valid. For flow, link project workflow,
board, WIP policy, service expectation and metrics; invent no numeric defaults.

The optional `--recommend` command consumes partial planning_context or an existing
choice and prints advice/questions only. It does not inspect project files, ask the
user interactively or apply a choice. Source discovery and tailoring remain this
skill's work. Do not convert a proposal into approval. Legacy inputs retain their
views without forced context backfill. Generate 1.4 only after a settled selection
is sourced; its primary perspective and milestone/flow views are explicit, and
its saved layout is reused. A conflicting CLI layout requires updating the source
decision first. Revision/history and destination safeguards remain in force.

Self-check: known facts were read first; missing questions were focused; recommendation
and settled choice are distinct; existing choices were reused and source-backed.

## Deliverable language

Before writing roadmap-chain deliverables, apply the [language contract](../../specs/roadmap-modeling.md#57-deliverable-language-schema-15).
Read the user instruction, consuming-project policy and existing artifact first;
retain a settled choice across handoffs. For a new artifact infer only from consistent
reader/document evidence; ask only unresolved gaps or winning-level conflicts.
Conversation language and English templates alone do not select artifact language.
Record the choice and source in existing norms/planning decisions; no new mandatory
configuration. Localize all new prose and display labels consistently while preserving
IDs, machine fields, canonical enums, source links and historical originals.

Prepare free-text names, goals, conditions, approval labels and revision summaries in
the chosen language before rendering. Use schema 1.5 or later for English/Chinese localization;
`--resolve-language` is read-only advice, not an automatic translator or interactive
interview. See the [workflow and paired examples](references/deliverable-language.md).

Self-check: language evidence and retained choice are explicit; all new display prose
is consistent, machine contracts are unchanged, and unavailable checks are reported.

## Executable topic layout and conversation regression

Use schema 1.6 with the retained `selection.layout: topic-split` for populated
main-plus-five output. Keep its established language record. The renderer fills
the selected blank scaffold without changing headings or table columns. Inspect
all six documents and schedule assets; do not treat a successful render as source
verification. Follow the Spec's ownership manifest and overwrite boundaries before
resetting or replacing generated output.

The [regression guide](references/structure-first.md#executable-generation-and-regression)
separates deterministic scripted multi-turn replay from explicit live-model eval.
Replay invokes the real renderer but does not prove model intent recognition.
Only `--eval` records live decisions; failed/timeout/provider runs are failures,
not skipped success. Neither test mode may publish or alter business sources.
