---
artifact_type: backlog-item
created_by: capture-work-items
lifecycle: living
type: requirement
date: 2026-10-20
status: done
priority: unset
strategic_goal_id: goal-2
source: user
---

# Make roadmap capabilities understandable and usable

## Problem / Need

Adopters need to understand which roadmap capabilities AI Cortex provides, what
they produce, and how requirement arrangement, version scope and scheduling fit
together. Planning must respect project priority policies and an explicitly chosen
delivery destination. Goal mapping is inferred from the governance capability
defined in [Goal 2](../../project-overview/strategic-goals.md#goal-2-governance-chain-capabilities-are-available).

## Acceptance Criteria

- [x] AC1: The public guide explains scenarios, skills, governing assets, deliverables,
  three presentation forms, formats, destinations and capability limits.
- [x] AC2: A shared roadmap contract supports optional version and schedule views,
  preserves approval/execution separation, and accepts existing single-view plans.
- [x] AC3: Priority policy application preserves settled priorities; full four-framework
  reassessment is explicit. Requirement priority vocabulary includes P3.
- [x] AC4: A standard-library local tool validates structured input and generates
  Markdown, SVG and, for dated schedules, Mermaid without automatic scheduling.
- [x] AC5: Skills agree on ownership, destination choice, source evidence and updating
  all selected views. No cross-platform synchronization or runtime downloads occur.
- [x] AC6: Behavioral tests, rendered SVG inspection and relevant repository checks
  pass, with unavailable platform checks reported explicitly.

## Delivery plan

User-authorized implementation; capture status and priority are not approval fields.
The existing project roadmap remains authoritative; this work serves its Now
governance-capability direction without rewriting unrelated milestones.

| Step | Work | Points | Progress |
| --- | --- | --- | --- |
| 1 | Publish the capability guide and navigation | 5 | Done |
| 2 | Define the shared multi-view and generator contracts | 5 | Done |
| 3 | Align priority and roadmap skills | 8 | Done |
| 4 | Build and test the local generator | 8 | Done |
| 5 | Inspect outputs and run repository checks | 5 | Done |

## Implementation boundaries

Discuss team cadence and select useful requirement, iteration/version and schedule views at creation. Confirm a new
destination; reuse an established selection during maintenance. Temporary JSON is
a generation interface, not a second planning authority. Use relative weeks when
the start date is unknown. Do not copy private reference content into examples.
No commit, push, installation update or remote publication is included.

Implementation detail: [technical design](../../designs/2026-10-20-roadmap-generation-technical-design.md).

## Verification evidence

- `python3 scripts/test-roadmap-renderer.py`: 19 tests passed. Red failures were
  observed before implementation, including XML control characters, the last
  supported date and missing direction/rationale output; targeted fixes went green.
- Browser inspection: relative-week example and dated Chinese long-label SVG opened
  successfully; spans, dependency arrows, labels and unscheduled work were inspected
  at the desktop viewport. No narrow-screen or assistive-technology audit is claimed.
- Public illustration is reproducible from the shipped JSON example.
- Markdown lint, relative links, document hygiene, asset counts, findings contract,
  cortex command documentation, skill index and whitespace checks passed.
- Modeled Rule validation, Rule scenarios and the existing mutation suite passed.
- Working-tree version comparison checked 12 changed/new versioned assets; the
  standard tag-range version check also passed, covering its declared committed range.
- Static contract walkthroughs checked policy application versus reassessment,
  single-view compatibility, tier/version separation, destination reuse and archive
  carryover. These are document reviews, not live-model behavioral evaluations.

### Capability version decisions

| Skill | Version | Changed responsibility / rationale |
| --- | --- | --- |
| `define-roadmap` | 7.1.0 | Inputs, procedure and delivery: select views/destination and render locally; additive capability. |
| `review-roadmap` | 3.2.0 | Procedure and Self-Check: evaluate selected views and destination evidence; additive checks. |
| `update-roadmap` | 3.1.0 | Scope, persistence and Self-Check: existing-version membership and cross-view refresh; additive maintenance. |
| `promote-roadmap-items` | 3.2.0 | Inputs and persistence: accept policy priorities and preserve version/time facts; additive clarification. |
| `prioritize-backlog` | 3.0.0 | Modes, procedure and references: policy application is the default and full reassessment is explicit; major behavior change. |
| `capture-work-items` | 2.2.0 | Priority handoff: suggest policy application or assessment without forcing batch scoring; additive interaction change. |
| `orchestrate-roadmap-planning` | 2.2.0 | Routing: preserve mode intent, selected views and archive target kinds; additive orchestration. |
| `archive-milestone` | 1.3.0 | Version/year route and conditional checks: preserve unfinished carryover without inventing directories; additive route. |
| `plan-next` | 15.3.0 | Diagnosis adapter: recognize version/schedule views without duplicating requirements; additive diagnosis. |

## Delivery limitations and exclusions

Yuque writes, image uploads and target-platform Mermaid rendering were not executed;
no compatible Mermaid renderer was present in this environment. Those remain
conditional destination checks, not claims of connected publication. No cross-platform
sync, resource scheduler, PNG/PDF exporter, commit, push or installation update was
performed. Existing unrelated working-tree changes were retained.

## Filled deliverable examples

- [x] Publish a single [Service Desk casebook](../../../skills/define-roadmap/references/service-desk/README.md)
  with four consistent IDs and source-backed initial, adjusted and after-delivery snapshots.
- [x] Provide filled priority, dependency, placement, review, change and archive outputs.
- [x] Separate the intentionally faulty candidate from valid generated roadmaps and
  show both correction and the independent sandbox-blocking event.
- [x] Point the input example to the casebook's canonical initial input through a
  relative compatibility symlink;
  link producing skills and the public guide to their finished outputs.
- [x] Verify regenerated Markdown/SVG, source anchors, policy/graph agreement,
  membership/timing/status, drift detection and unfinished-item destinations in CI.

Verification: 22 renderer tests and 7 casebook tests pass. Additional renderer
checks distinguish unscheduled items from unverified dependency edges and ensure
key conditions link to source evidence. Version window labels cover targets,
commitments and actual timing. These are local fictional examples; no remote
publication, live release or model-based end-to-end evaluation is claimed.

The producing skills receive minor version bumps for the worked examples and
entry links. The earlier delivery's recorded versions and test counts remain
its verification facts, rather than being rewritten as a new release record.

## Phase and milestone implementation

Design and research: [implementation design](../../designs/2026-10-20-roadmap-events-technical-design.md),
[primary-source evidence](../../references/roadmap-milestone-research.json).

| Step | Work | Points | Progress |
| --- | --- | --- | --- |
| 1 | Define roadmap, version, phase and event relations and compatibility | 5 | Done |
| 2 | Extend the offline generator with independent phase/event objects | 8 | Done |
| 3 | Align creation, maintenance, diagnosis and archive skills | 5 | Done |
| 4 | Migrate examples, inspect rendering and verify contracts | 5 | Done |

- [x] AC7: Definitions and relations are consistent; 1.0 inputs and existing single-view plans remain valid.
- [x] AC8: Version/phase spans coexist with independent approval and release events.
- [x] AC9: Event occurrence requires source evidence, with explicit unknown timing and actionable invalid-input errors.
- [x] AC10: Skills, templates, archive routes and examples share the model without directory migration or evidence loss.

### Phase/event verification

- Roadmap Spec 1.1.0 defines four concepts, optional relations, evidence and explicit
  JSON 1.0/1.1 compatibility; the quality Rule is 4.2.0.
- Extended generator tests were first run red against schema 1.0, then implemented
  and run green. Final checks cover 28 renderer tests and 8 casebook tests, including
  independent version/phase spans, multiple event points, dated Mermaid, global and
  unscheduled events, evidence/state validation, legacy compatibility and drift.
- Initial, adjusted and after-delivery examples reproduce their Markdown/SVG; the
  deliberately invalid example withholds SVG. Public illustration matches initial.
- Browser inspection of adjusted and after-delivery SVG confirms distinct lanes,
  same-time acceptance/release points and target/actual plus planned/reached labels.
  Inspection prompted moving event state out of wrapped names into timing labels.
- Definition, update, review, promotion, orchestration, diagnosis and archive skills
  follow the same model. Legacy archive maturity and cleanup stay on their existing
  work-package route; the general route preserves independent event evidence.
- No automatic input/directory migration, remote publication or source evidence
  deletion was performed. Destination-specific rendering remains unverified.

| Updated capability | Version |
| --- | --- |
| define-roadmap | 7.3.0 |
| update-roadmap | 3.3.0 |
| review-roadmap | 3.4.0 |
| promote-roadmap-items | 3.4.0 |
| orchestrate-roadmap-planning | 2.3.0 |
| plan-next | 15.4.0 |
| archive-milestone | 1.5.0 |

These are additive model/route clarifications with explicit legacy compatibility.
The earlier verification and version tables above retain their historical scope.

## Revision history implementation

Design: [revision mechanism](../../designs/2026-10-21-roadmap-revisions-technical-design.md).
User-authorized on 2026-10-21. Existing phase/event delivery evidence above remains historical.

| Step | Work | Points | Progress |
| --- | --- | --- | --- |
| 1 | Define material changes, retention, evidence and compatibility | 3 | Done |
| 2 | Extend the generator with tested 1.2 revision summaries | 5 | Done |
| 3 | Align maintenance, review, promotion, priority and archive ownership | 3 | Done |
| 4 | Verify baseline, adjusted/delivered examples and repository checks | 3 | Done |

- [x] AC11: Material-change triggers and ownership agree across norms and skills.
- [x] AC12: Latest-five summaries link retained history; schedule facts remain unchanged.
- [x] AC13: Invalid evidence/date/order/limits fail; old schemas remain compatible without invented history.
- [x] AC14: Filled examples preserve earlier decisions through version moves and milestone observations.

### Revision mechanism verification

- 41 renderer tests and 9 casebook tests pass. The new 1.2 tests first failed
  against the prior generator, then passed after validation/rendering implementation.
- Coverage includes complete summaries, latest-five compaction with retained links,
  duplicate IDs, invalid/future/out-of-order dates, missing evidence, record limits,
  escaping, no-op repeatability, legacy ignored metadata and real CLI output/failure.
- Source-backed examples show an empty initial baseline, REV1 after plan adjustment,
  and REV2 plus unchanged REV1 after delivery. Full history links resolve. Existing
  SVG outputs remain byte-for-byte identical to the generated scheduling facts.
- Spec 1.2.0 and Rule 4.3.0 own the revision mechanism. Eight related skills receive
  minor bumps for new maintenance/review/handoff steps; their purposes remain intact.
- Markdown lint, links, hygiene, findings, asset counts, CLI documentation, index,
  modeled Rule validation, changed-asset versions and whitespace checks pass.
- The active project roadmap adopts an explicit 2026-10-21 baseline without invented
  earlier planning records. No live-model, remote-publication or platform-rendering
  verification is claimed for this documentation/generator extension.

## Reading structure and iteration implementation

Design: [document layout and iterations](../../designs/2026-10-21-roadmap-document-layout-technical-design.md).
User-authorized on 2026-10-21; preserves earlier revision implementation and snapshots.

| Step | Work | Points | Progress |
| --- | --- | --- | --- |
| 1 | Define main/detail reading order and fact ownership | 3 | Done |
| 2 | Add optional 1.3 iteration validation and views with TDD | 5 | Done |
| 3 | Add safe single/split output and navigation with TDD | 5 | Done |
| 4 | Align skills, template, guide and source-backed examples | 3 | Done |
| 5 | Verify compatibility, layout, navigation and repository checks | 3 | Done |

- [x] AC15: Main/detail responsibilities and one-source ownership agree across assets.
- [x] AC16: Optional iterations map goal/scope/timebox to versions without implicit release or tier movement.
- [x] AC17: Single/split output shares facts, navigation and history; safe overwrite and legacy compatibility pass.
- [x] AC18: Filled single/split iteration examples reproduce source decisions and all relevant checks pass.

### Layout and iteration verification

- 53 renderer tests and 11 casebook tests pass. New iteration/layout cases first
  failed against the prior implementation; the output-alias regression likewise
  failed before the bounded preflight repair, then passed.
- The 1.3 iteration example and both layouts reproduce one input and independently
  recorded allocations. They preserve adjusted requirements, versions, events,
  original deadline impact and REV1. REV3 records only iteration-view adoption.
- Coverage includes carry-over, unallocated/empty/unknown scope, version mapping,
  invalid sources/members/IDs, shared limits, dated exports, full supplied history,
  navigation, source-relative links, no mutation, deterministic output and legacy
  1.0–1.2 split/default compatibility. Reserved-path hazards fail before writes;
  explicit layout switches remove only stale generated siblings.
- Local browser inspection with the installed Marked renderer confirms readable
  priority/delivery views, working main-to-detail navigation and expandable timing
  details. SVG inspection confirms separate version/event/iteration lanes and
  target/committed/actual labels. This is local preview evidence, not Yuque or Git
  host rendering verification; target support must be checked at delivery.
- The project's own main roadmap is shorter and links its retained strategic
  definitions in roadmap-strategy.md. Conflicting metric thresholds are explicit;
  no new target, cadence, date, requirement status or milestone occurrence is inferred.
- Spec 1.3.0 and Rule 4.4.0 own the additive contract; seven skills receive minor
  increments for layout/iteration selection, maintenance, review, routing and archive
  steps. The earlier priority/revision changes retain their own scope.
- No commit, push, local installation update or remote publication was performed
  during this implementation. Unrelated worktree changes remain outside its scope.

## Scenario combinations and retained choices

Design: [scenario selection](../../designs/2026-10-21-roadmap-scenarios-technical-design.md).
User-authorized on 2026-10-21. Existing revision/layout work remains intact.

| Step | Work | Points | Progress |
| --- | --- | --- | --- |
| 1 | Define sourced recipe advice and intake/retention contract | 3 | Done |
| 2 | Implement read-only recommendation and explicit 1.4 selection with TDD | 5 | Done |
| 3 | Add shared modules, four recipes and complete source-backed examples | 5 | Done |
| 4 | Align skills, norms, guide and review/diagnosis routes | 3 | Done |
| 5 | Verify CLI, compatibility, examples and document checks | 3 | Done |

- [x] AC19: Four template combinations share a base/modules with sourced advice and tailoring boundaries.
- [x] AC20: Intake reads known facts, asks material gaps, recommends with reasons and retains existing choices.
- [x] AC21: Generator validates selection, supports independent/flow views and never applies recommendation output.
- [x] AC22: Four complete examples reproduce source choices and all relevant checks pass.

### Scenario verification and delivery evidence

- 62 renderer tests and 14 example checks pass. New recommendation/selection cases,
  legacy metadata reuse and continuous-iteration tailoring first failed against
  the prior behavior, then passed after targeted implementation. Legacy 1.0–1.3
  outputs remain reproducible; no new selection metadata is required for them.
- Four scenarios include independent source tables, intake/selection records,
  transient input and generated output. Checks compare context, scope, status,
  delivery/event facts, timing, flow policy and selected views with those sources;
  deliberate context/choice/membership/evidence/scope/timing mutations are detected.
- Real CLI runs retain each choice and its saved layout, reproduce every output
  and preserve the input. Recommendation needs-input is diagnostic (exit 0), invalid
  choices fail, and neither advice path writes files. New generation rejects a
  conflicting layout rather than changing the source decision.
- The shared template has six optional modules and four recipes; examples distinguish
  actual flow policy from unknown measurements, significant acceptance events from
  releases, and learning evidence from speculative rollout commitments. WIP limits
  and participant counts in examples are fictional source facts, not defaults.
- Local installed-Marked/browser inspection confirms distinct flow and phase views,
  readable planning choice/source, and working main-to-detail navigation. This does
  not prove hosted Markdown/Yuque rendering or an actual agent-led user interview.
- Links, document hygiene, Markdown lint, findings contract, asset counts, CLI docs,
  generated index, modeled Rules, changed asset versions and whitespace checks pass.
  Generator functions remain at most 50 lines; no dependencies were installed.
- No commit/push, installation update, remote publication or unrelated-file edits
  were performed in this step. Earlier revision/layout work remains uncommitted.

| Skill | Sections / reason for change | Version |
| --- | --- | --- |
| define-roadmap | Read-first intake, scenario/template selection, explicit recommendation vs retained choice, generation handoff | 7.6.0 |
| update-roadmap | Reuse selection during status/date/flow maintenance; route changed needs without resetting choices | 3.6.0 |
| review-roadmap | Judge source/choice consistency and evidence limits; no recipe conformity gate | 3.7.0 |
| orchestrate-roadmap-planning | Carry selection/context across atomic handoffs; delegate intake and reconsideration | 2.6.0 |
| plan-next | Diagnose selection conflicts without treating legacy/custom choices as gaps | 15.7.0 |
| promote-roadmap-items | Preserve scenario/layout while refreshing tier projections | 3.7.0 |
| archive-milestone | Retain choice/context and flow evidence in history | 1.8.0 |

These are additive minor increments with unchanged capability ownership. Spec 1.4.0
owns the new explicit interface; Rule 4.5.0 owns intake/choice evaluation. Skill
frontmatter, source links, inputs/decisions/outputs, tool fallback and Self-Checks
were inspected under refine-skill-design; sources/provenance remain unchanged.

### Closeout input-boundary repair

Pre-commit scope review reproduced an unhandled TypeError for object/array schema
versions in recommendation input, and acceptance of unsupported versions. A new
regression first failed; the boundary now rejects supplied invalid versions through
the existing ValueError diagnostic. Context-only recommendation remains supported.
Define-roadmap receives patch 7.6.1 for this erratum. Final renderer count is 63;
14 example checks remain unchanged. No new planning behavior or source choice is added.

## Deliverable language adoption

Scope: [language design](../../designs/2026-10-21-roadmap-language-technical-design.md).
Resolve user > project > existing artifact > supported reader/document context;
ask only unresolved gaps/conflicts and retain the choice across planning steps.

| Work unit | Story points | Status |
| --- | --- | --- |
| Language contract, quality criteria and skill handoffs | 3 | Implemented |
| Schema 1.5 resolution and localized rendering with TDD | 5 | Implemented |
| Paired source-backed examples and workflow guidance | 3 | Implemented |
| Regression, repository checks and visual inspection | 2 | Verified |

Acceptance additions:

- AC23: all roadmap-chain skills follow the same language priority, focused-question
  and retention contract, with no mandatory new configuration or legacy migration.
- AC24: English/Chinese headings, headers, states, summaries and diagram descriptions
  agree with selected language while preserving IDs, references and planning facts.
- AC25: conflicts and unsupported locales are explicit; read-only advice changes no
  files, unresolved generation writes nothing, and legacy English outputs remain stable.
- AC26: paired complete examples are independently source-backed, reproducible and
  checked for shared facts; arbitrary prose remains a skill/reviewer responsibility.

Changed skills receive additive minor versions: define-roadmap 7.7.0,
update-roadmap 3.7.0, review-roadmap 3.8.0, orchestrate-roadmap-planning 2.7.0,
plan-next 15.8.0, promote-roadmap-items 3.8.0, archive-milestone 1.9.0,
prioritize-backlog 3.3.0, map-item-dependencies 1.2.0 and capture-work-items 2.3.0.
Each adds language resolution/retention and output verification without changing its
existing domain scope. Definition prepares localized prose; maintenance/promotion
retain choices; review/diagnosis report drift without rewriting; orchestration
passes evidence; archive preserves historical originals; intake/priority/dependencies
apply the choice to new chain records and reports. Source versions, frontmatter,
links, boundaries, tool fallback and Self-Checks are checked under refine-skill-design.

### Language verification evidence

The AGENTS language clause now links the scoped localization exception without
changing section order or other loading/authority rules. Entry-profile verification:

| Requirement | Result | Entry evidence |
| --- | --- | --- |
| Opening role | PASS | Opening paragraph |
| Project identity and asset table | PASS | Section 1 |
| Authoritative sources | PASS | Section 2 |
| Actionable behavior | PASS | Section 3 numbered MUSTs and external-resource constraints |
| Discovery/loading | PASS | Section 4 canonical path, tiers and matching/injection |
| Language and terminology | PASS | Section 5; terminology pointer in section 2 |
| Section order | PASS | Opening, sections 1–5, Reference |
| Concise pointers rather than copied contracts | PASS | Source tables and linked assets |
| Stable local references | PASS | Repository link check |
| Title and primary language | PASS | Title and English entry body |
| Tables | PASS | Identity, authority and Reference tables |
| Format reference | PASS | Reference: agents.md |
| Raw entry URL | PASS | Reference: raw.githubusercontent.com URL |
| Project-specific profile | PASS | Reference: generate-agent-entry |
| Usage and installation | PASS | Reference: README and bin/cortex |
| Asset indexes | PASS | Reference: Skills, Specs, Protocols, Rules |

No heading/section numbers changed, so existing section references remain valid.
The change is supplied as a reviewable working-tree diff; closeout is a separate step.

Final language checks: 78 renderer tests and 18 example tests pass. All legacy
fixtures remain reproducible. Link, hygiene, findings-contract, asset-count, CLI-doc,
index, modeled-Rule, Markdown-lint and whitespace checks pass; 12 changed versioned
assets have increased versions. Renderer functions remain within 50 lines.
Local installed-Marked/browser inspection confirms readable Chinese tables and
main-to-detail navigation; English and Chinese SVG timelines preserve the same
endpoints and display localized legends. Mermaid syntax/labels are tested as text;
hosted Mermaid/Yuque rendering and an actual agent-led interview were not exercised.
Unrelated working-tree changes were preserved. No local installation update, commit,
push or remote skill publication was performed for this change.

Timeline headings are selected at construction; source prose mentioning a schedule
heading is preserved in both languages. Missing/malformed bundled localization data
fails with a recovery instruction before output creation. Regressions exercise both
conditions; paired editions are also reproduced through the real CLI from a different
working directory. Existing example outputs remain unchanged by these repairs.
