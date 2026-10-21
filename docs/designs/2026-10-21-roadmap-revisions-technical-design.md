---
artifact_type: technical-design
lifecycle: snapshot
created_at: 2026-10-21
parent: ../process-management/backlog/2026-10-20-roadmap-capabilities.md
status: approved
---

# Roadmap revision history

## 1. Goal

Make material planning changes understandable after the conversation ends: preserve
what changed, why, its impact and evidence without turning a roadmap into a full
activity log. User-authorized scope covers norms, skills, generator and examples.

## 2. Architecture and service decomposition

The Roadmap Spec owns structure and compatibility; the quality Rule judges
traceability. Existing planning skills own decision capture and retention. The
standard-library generator validates and presents supplied records. Existing source
records or archive snapshots retain full details; Git retains textual differences.
No new artifact type, service or planning authority is introduced.

## 3. Components and detailed design

Add separate revision validation and Markdown rendering helpers. Retain latest five
summaries and a full-history reference. SVG/Mermaid continue to show scheduling
facts. Repeated rendering is deterministic and does not append decisions. Calling
skills read retained history before changes and preserve IDs across regeneration.
No new application interface or interaction pattern is introduced; functional/UI
design records are not applicable to this document-generation extension.

## 4. Database design

No database or directory migration. JSON remains transient rendering input.
Historical decisions may mention removed objects. They are not validated against
current planning IDs and do not reintroduce objects into the active scope.

## 5. Interface contracts

Schema 1.2 adds required `revisions` (possibly empty) and optional `revision_history`.
A revision has stable ID, ISO date, before/after summary, reason, impact and source.
Dates are newest first and no later than `updated`. Equal dates retain input order.
More than five records require a resolving full-history reference upstream. Bound
input to 200 revisions independently of planning-object counts and keep text limits.
Schemas 1.0/1.1 retain their behavior, including ignored unmodeled revision metadata.
CLI flags and reserved outputs stay unchanged. Exact fields belong to the Spec.

## 6. Data flow and error handling

Source decision → durable history → current-plan summary/temporary JSON → validation
→ generated Markdown → linked-history and cross-view checks.
Missing reason/impact/source, invalid date/order/ID or absent required history link
rejects input before writes. A new baseline discloses unknown earlier history;
never synthesize records by comparing against a guessed past plan. Corrections
append linked new decisions. Moving old summaries requires preserved source links.

## 7. Technology choices and trade-offs

| Choice | Benefit | Cost |
| --- | --- | --- |
| New 1.2 interface with explicit history | Predictable output and compatible legacy rendering | Caller supplies decision evidence |
| Latest-five summary plus linked details | Readable current plan without deleting history | Links must remain valid |
| Existing source records and Git | No competing history store | No automatic business-rationale inference |

## 8. Test strategy

TDD: schema dispatch, complete summaries, bounded latest-five display, full-history
link, invalid dates/order/evidence, escaping, legacy inputs and deterministic output.
Run real CLI/JSON/output integration and source-backed initial/adjusted/delivered
casebook checks. Verify older decisions survive unchanged. SVG golden equality
checks demonstrate this extension does not alter scheduling facts. Run relevant
Markdown, links, hygiene, index, asset and Rule checks. No remote publication needed.

## 9. Acceptance criteria

- AC11: Material-change triggers and ownership are consistent across Spec, Rule and skills.
- AC12: Generated Markdown shows latest five revisions and retained-history links without changing schedule facts.
- AC13: Invalid evidence/dates/limits fail explicitly; legacy inputs remain compatible and no history is inferred.
- AC14: Source-backed examples retain the same prior revision across changed version scope and later milestone observations.

## Quality attribute design

| Concern | Tactic | Verification | Owner |
| --- | --- | --- | --- |
| Evidence integrity | Mandatory reason/impact/source, stable IDs and append-only decisions | Negative validation and casebook tests | Skills/renderer |
| Compatibility | Explicit 1.2 dispatch; unchanged legacy render behavior | Legacy regression tests | Renderer |
| Bounded work and readable output | Record/text caps; five visible rows; retained source link | Boundary and compaction tests | Renderer/calling skill |
