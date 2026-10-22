# Structure before roadmap content

Use this guide for a new roadmap or authorized structural redesign. Routine
maintenance reuses the settled structure. The [Spec](../../../specs/roadmap-modeling.md#structure-before-content)
owns the contract and the [quality rule](../../../rules/roadmap-quality.md#review-scope-and-structure-drafts)
owns review scope. This is authoring guidance; do not copy it into the deliverable.

## Stage entry and completion

Use the [three stage entries](../../../specs/roadmap-modeling.md#stage-entries-authorization-and-acceptance)
inside the existing skill. For example, “confirm structure first” ends at the blank
artifact; “populate the confirmed structure” resumes from source inventory; “complete
both now” validates structure and continues without another confirmation. A later
request to review only format can inspect populated files without changing facts
or claiming business acceptance. These authoring examples are not deliverable text.

## Choose the reader entry first

Identify readers, their primary questions and the existing authority for each fact.
Settle enabled/omitted views, document roles, titles, fields and navigation before
business population. A small plan can remain one document. “Independent content”
means independently useful topics, not a file for every field, empty chapter or
future iteration. Respect an already authorized layout without asking again.

If the user wants to confirm structure first, return the empty artifact and stop.
Do not fetch business systems, inherit discarded materials, insert teaching IDs or
invent a cadence, owner, release number or date to make tables look complete.
Later population uses the confirmed structure; material layout changes explain
reader benefit and affected links before they are applied.

## Optional topic-split combination

| Document | Reader purpose | Empty structure | Populated case |
| --- | --- | --- | --- |
| Roadmap | Priorities, next work, conditions and delivery outlook | [Template](../assets/structure-first/roadmap.md) | [Case](service-desk/topic-split/roadmap.md) |
| Iteration plan | Goals, timeboxes, members and version contribution | [Template](../assets/structure-first/iterations.md) | [Case](service-desk/topic-split/iterations.md) |
| Version plan | What ships together and what remains unassigned | [Template](../assets/structure-first/versions.md) | [Case](service-desk/topic-split/versions.md) |
| Milestones | Events, occurrence criteria, responsibility and evidence | [Template](../assets/structure-first/milestones.md) | [Case](service-desk/topic-split/milestones.md) |
| Planning basis | Selection, authorities, unresolved decisions and facts | [Template](../assets/structure-first/roadmap-planning-basis.md) | [Case](service-desk/topic-split/roadmap-planning-basis.md) |
| Revision history | Retained changes and completed/closed records | [Template](../assets/structure-first/roadmap-history.md) | [Case](service-desk/topic-split/roadmap-history.md) |

This combination keeps timing in the main and provides no extra index or combined
delivery document. Omit unused optional views when selected; six files are not a
universal requirement. Per-object detail files need an actual reader/ownership
reason. Blank generation uses `--blank`; populated topic rendering uses schema 1.6
with `selection.layout=topic-split`. The existing single/split contracts remain
supported. Blank and populated topic rendering retain matching headings and columns.

## Fill without leaking instructions

Use bold standalone labels and consistent placeholders in the empty structure;
keep tables empty rather than inventing object IDs. Localize reader labels using
the established language choice and preserve stable IDs and source links.

During population, resolve facts from their authority, map execution to the Rule's
single-label vocabulary, retain unknowns and distinguish business choices from
facts. A need for a fact is not permission to change a priority or promise a date.
The main retains the latest five revision summaries; detail retains durable
history. Main summaries are projections, not second independently editable plans.

Keep field-filling instructions, enum tutorials, template directives, agent work
orders and discussion process here or in their governing assets. Actual rationale,
timing conventions, closure conditions, material limitations and unknown facts
are legitimate reader content and remain in a populated plan.

## Review and claims

For structure-only review, inspect every selected document for role/field coverage,
main/detail navigation, consistent titles/formatting, empty tables and absence of
authoring guidance. Business completeness, readiness, dates and source truth are
not evaluated. Report a structural result, not a full roadmap pass. Re-review with
no new finding or evidence leaves the artifact unchanged.

- **Compatibility:** identify the Spec and Rule; custom combinations can conform.
- **Template use:** name the template and disclose selected modules and deviations.
- **Replication:** name the exact example; compare files, headings, columns, order
  and display conventions. Disclose differences instead of claiming “100%” for a
  compatible but different layout.

### Example layout decision

The paired Service Desk case uses the existing iteration-driven planning snapshot
with the same requirement IDs, priorities, tiers, states, versions, events and
revision IDs. Only presentation changes: the combined delivery page becomes
iteration/version/milestone detail pages, timing moves to the main, and planning
basis has its own page. PSEARCH remains linked to its existing source. This is an
illustrative reader-layout choice, not another business decision or revision.

### Example review result

The six empty files contain one entry, five linked details, bold placeholder
labels and empty tables. They contain no Service Desk records or authoring prose.
The paired populated files retain the selected second-level sections, link back
to the main, preserve source requirement states/version members/event states and
link unknown occurrence evidence. These checks run in `scripts/test-roadmap-examples.py`.

Structural review passes for the empty set; business criteria are not evaluated.
The populated teaching case does not establish live acceptance, production release
or external publication. Its links and source relationships are local fixtures,
not evidence of a real user interview or operational deployment.

## Executable generation and regression

Generate a clean English or Simplified Chinese structure without any business input:

```sh
python3 skills/define-roadmap/scripts/render-roadmap.py --blank --check
python3 skills/define-roadmap/scripts/render-roadmap.py --blank --locale en --output-dir /tmp/roadmap-structure
```

For population, prepare verified schema 1.6 facts with a retained `topic-split`
selection and language record, then use the normal renderer with that input.
Explicit `--overwrite` is required for existing outputs. Generated ownership
metadata protects unrelated or modified stale files during reset; it is not an
editable business plan. Keep source evidence outside reserved output paths.

The [design](../../../docs/designs/2026-10-21-roadmap-generation-workflow.md)
and [agent test contract](../../../docs/agent-tests/agent-test-roadmap-structure.md)
trace the following checks and their boundaries:

```sh
python3 scripts/test-roadmap-renderer.py
python3 scripts/test-roadmap-conversations.py
python3 scripts/test-roadmap-eval-evidence.py
python3 scripts/roadmap-conversation-eval.py --report /tmp/roadmap-replay.json
```

Replay runs ten scripted conversations through the real renderer in temporary
workspaces. It checks formatting feedback, confirmation without population, repeat
review without writes, authorized population, reset without re-import, preservation
of source states, English/Chinese feedback, missing input/source and refusal of external publication. Negative controls must fail.
Additional stage cases cover continuous authorization, scoped structural review on populated files and business options without decision replacement.
This tests deterministic tool/trajectory handling; it is not a live-model recording.

A separate explicit `--eval` mode invokes the installed Codex CLI with complete
conversation history and actual Skill/Spec/Rule context. The model proposes a JSON
action; the host executes only local renderer actions. The adapter cannot use tools
or publish. This is a bounded decision-and-generation eval, not arbitrary shell-edit
or integration testing. `--ignore-user-config` excludes user-defined tool/MCP
configuration and uses the CLI built-in provider/model defaults rather than a
custom user model selection. Authentication still uses the normal Codex account;
use this mode only when live model use is authorized.

```sh
python3 scripts/roadmap-conversation-eval.py --eval --timeout 300 --report /tmp/roadmap-live.json
python3 scripts/save-roadmap-eval-evidence.py /tmp/roadmap-live.json --overwrite
```

The report distinguishes replay/live backend, per-turn proposals, renderer execution,
violations and pass rate. Required threshold is 1.0. A provider error, timeout, missing
CLI, malformed decision or incomplete case is failure, never a skipped pass. Record
CLI/model metadata when available; do not invent a provider model ID the CLI does
not expose. Test reports belong outside the generated roadmap output directory.

The [schema 1.6 fixture](service-desk/topic-split/input.json) reproduces every populated
topic document and its diagram. The [live golden report](../../../docs/references/roadmap-conversation-eval-20261021.json)
records the evaluated conversations and actual model decisions, with its context
digest, CLI version and evaluation limitations.

The oracle also checks the confirmed section/table schema and internal navigation.
Feedback can validly lead to regeneration or a no-write review when the requested
format is already present. Tool observations describe the actual workspace, never
the expected test answer. Reports identify fixture, runner, renderer and frozen
Skill/Spec/Rule context digests. Provider failure, timeout, malformed responses and
forbidden tool attempts have isolated negative tests; those tests use a CLI double,
not live model service calls in CI.

A live run must supply a complete structured provider trace. The adapter accepts
message/reasoning items only and rejects unknown tool items rather than assuming
they are harmless. Provider-double tests include a valid-response control.

Offline CI also checks that saved live evidence matches the current instruction,
golden-case, evaluator and renderer digests. Instruction or executable changes
require fresh explicit eval evidence; an older passing report cannot certify a
new revision. Raw localized transcripts are retained under the language fixtures;
the stable report entry carries an English summary and provenance.

[Raw localized live trace](languages/conversation-eval-20261021.json).

The evidence export validates the complete live trace against current golden cases
and instruction/executable digests before writing. It saves both canonical report
paths linked above; existing files require explicit `--overwrite`. Export performs
no model calls and cannot turn stale or replay evidence into live evidence.

Content review of a blank draft retains business scope and reports its missing
basis without filling files or certifying readiness. Evidence export independently
rechecks each recorded decision and observation against the golden turn. Reports
record the per-turn timeout and fingerprint templates, locale catalog and source
fixtures in addition to instructions and executables.
