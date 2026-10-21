---
artifact_type: technical-design
lifecycle: snapshot
created_at: 2026-10-21
parent: ../process-management/backlog/2026-10-20-roadmap-capabilities.md
status: approved
---

# Roadmap reading structure and iteration views

## 1. Goal

Make one roadmap readable at a glance, with optional iteration planning and linked
delivery/history detail, while preserving source authority and legacy inputs.

## 2. Architecture and service decomposition

| Layer | Responsibility | Dependency |
| --- | --- | --- |
| Spec and norms | Reading order, document ownership, iteration contract | Existing source records |
| Skills and quality Rule | Select layout, preserve decisions, maintain/review every affected view | Spec |
| Offline renderer | Validate supplied facts; derive single or split views | Python standard library only |
| Casebook | Demonstrate equivalent single/split plans and iteration/version mapping | Fictional source decisions |

Main document: direction, ordering, requirement arrangement, compact delivery,
key events/blockers, latest five revisions and detail links. Delivery details group
iterations/versions, phases/events and timeline. History details retain supplied
revisions and link complete durable evidence. These are views, not new asset types.

## 3. Components and detailed design

`validate_iterations(data)` checks schema 1.3 records and entry membership.
`iteration_markdown(data)` derives timeboxes from the shared schedule and version
mapping from entry membership. `documents(data, layout)` returns a fixed-name
output mapping. `preflight_outputs(...)` checks every reserved path before writes.
Single layout remains default; split layout creates delivery/history siblings only
when content exists. Flat sibling paths preserve existing relative link semantics.
Main/detail pages link both ways. New schema uses grouped headings and folds
Completed requirement rows separately; legacy renderers retain exact behavior.
No application UI or role/permission change; the functional UI trigger does not apply.

## 4. Database design

No database change. Temporary JSON is rendering input, not an editable planning
store. Existing source requirements, iteration boards and decision records remain
authoritative. No automatic source-directory migration or threshold reconciliation.

## 5. Interface contracts

Schema 1.3 adds optional iterations, selected by `views: iterations`, with cadence,
goal, owner, entry members, source and optional board link. IDs share the planning
namespace and bounds. Timeboxes use existing schedule spans; no second timing field.
An entry may contribute across iterations; version membership remains unique.
CLI adds `--layout single|split`. Reserved siblings are roadmap.md,
roadmap-delivery.md, roadmap-history.md, roadmap.svg and roadmap.mmd. Existing
1.0–1.2 schemas and default render behavior remain compatible. Invalid input/layout
or conflicting paths exits nonzero; no writes occur on validation/preflight failures.

## 6. Data flow and error handling

Project sources → verified transient facts → validation → one output mapping →
whole-set path preflight → deterministic UTF-8 files → link and view review.
Unknown iteration dates remain unscheduled; empty iteration lists and unallocated
entries are explicit. Invalid member/source/timebox rejects input before writes.
Symlink/nonregular output or input aliases reject the entire set before writes.
Explicit overwrite may remove stale reserved views when switching layouts, never
unrelated files. I/O failure reports possible partial output; no atomicity claim.

## 7. Technology choices and trade-offs

| Option | Decision | Benefit | Cost |
| --- | --- | --- | --- |
| One mandatory large document | Rejected as a universal policy | Simple storage | Grows unreadable across teams |
| One main plus optional detail views | Chosen | Main remains useful; details follow ownership/cadence | Navigation must stay valid |
| Nested generated directories | Rejected for first implementation | More customizable | Relative-link rebasing and cleanup complexity |
| Flat fixed sibling outputs | Chosen | Safe bounded writes and unchanged source links | Caller chooses one combined delivery detail page |

Hand-maintained projects may split iteration/version documents separately when
owners or update cycles differ; bundled split mode provides a bounded starting set.

## 8. Test strategy

TDD for 1.3 validation, iteration overlap/carry-over, derived version mapping,
unknown timing, grouped structure, completed rows, full-history retention and layout
switching. Real CLI checks cover both modes, stale outputs, source aliases, links,
no-write failures and dated exports. Casebook checks independently compare source
iteration decisions and reproduce every generated file. Run repository docs checks.

## 9. Acceptance criteria

- AC15: Main and detail responsibilities and one-source ownership agree across assets.
- AC16: Optional iteration goals/cadence/scope/timeboxes map to versions without implying release or tier changes.
- AC17: Single/split outputs share facts, navigation, history and safe overwrite behavior; legacy outputs remain compatible.
- AC18: Filled examples show both layouts and source-backed iteration carry-over; all relevant checks pass.

## Quality attribute design

| Concern | rule_refs | Tactic and trade-off | Verification | Owner |
| --- | --- | --- | --- | --- |
| Compatibility | ARC-005, TST-004 | Explicit 1.3 dispatch and single default; retain legacy rendering paths | Legacy and explicit split regression tests | Renderer |
| Evidence integrity | ARC-001, TST-001 | Derived mapping/timebox and one source owner; callers supply evidence | Independent casebook and no-mutation checks | Skills/renderer |
| Bounded file writes | SEC-001, REL-004, TST-002 | Fixed siblings and whole-set preflight; partial I/O remains possible and is reported | CLI alias/symlink/layout-switch tests | Renderer |
| Readability | PERF-001, TST-003 | Bounded facts, main summary and folded duplicate timing; no arbitrary planning quota | Heading/content checks and local rendered-document inspection | Creation/review skills |
