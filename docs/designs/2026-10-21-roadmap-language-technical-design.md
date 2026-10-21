---
artifact_type: technical-design
lifecycle: snapshot
created_at: 2026-10-21
parent: ../process-management/backlog/2026-10-20-roadmap-capabilities.md
status: approved
---

# Roadmap deliverable language

## 1. Goal

Select and retain a source-backed deliverable language, asking only when unresolved,
and render consistent English or Simplified Chinese without changing planning facts.

## 2. Architecture and service decomposition

| Component | Responsibility | Dependencies |
| --- | --- | --- |
| Roadmap Spec / quality Rule | Selection priority, persistence, status identity | Existing planning contract |
| Skills | Discover language evidence and prepare consistent free text | Project instructions, existing deliverables and audience |
| Language helper and catalog | Resolve supplied evidence and localize built-in presentation | Standard-library Python and local catalog |
| Renderer | Render explicit 1.5 language across Markdown, SVG and Mermaid | Language helper; existing validation/preflight |

Repository asset English is distinct from consumer artifact language. Localized
fixtures/catalog strings are narrowly exempt; no general document translation.

## 3. Components and detailed design

`resolve_language(data)` chooses user > project > existing artifact > consistent
reader/sibling-document evidence. Same-level conflict or no evidence yields focused
questions, not English fallback. `validate_language(data)` requires a settled 1.5
locale/basis/source/rationale. `ui(data, message)` translates only renderer-owned
labels; free text is never globally replaced. Timing and diagram helpers receive
locale explicitly. Existing input/enum/ID values remain unchanged. No application UI
is introduced; generated document presentation uses the existing pattern.

## 4. Database design

No database change. Retain one language decision with existing roadmap choices;
transient JSON projects it. Evidence candidates are bounded and source-referenced.
No automatic project file scanning or ongoing language configuration service.

## 5. Interface contracts

Schema 1.5 inherits 1.4 with required language: locale (en/zh-CN), basis, source and
rationale. Old schemas keep default English and ignored metadata. Read-only
--resolve-language accepts partial language_context; --recommend can include the
language result independently of view questions. Saved choice is retained absent
new evidence; changed evidence produces reconsideration without overwriting it.
Unsupported locales fail explicitly. Machine fields, filenames, IDs and enum values
remain stable; display labels have one-to-one localized mappings.

## 6. Data flow and error handling

Project evidence → missing/conflicting-language question or automatic resolution →
source decision → free text prepared by skill → validation → localized artifacts.
Unknown locale, invalid evidence/source or missing settled decision fails before
writes. Missing catalog entries fail rather than leak English into Chinese output.
The renderer does not translate arbitrary user text or certify its language; callers
review it and preserve linked original evidence. Existing I/O failure reporting stays.

## 7. Technology choices and trade-offs

| Option | Decision | Benefit / cost |
| --- | --- | --- |
| Detect language from characters/chat only | Rejected | Convenient, but overrides reader/project context and mishandles mixed sources |
| Source-backed evidence resolution | Chosen | Predictable priority and auditable reuse; skill must inspect project evidence |
| Global replacement of rendered output | Rejected | Could corrupt source text, IDs, links and XML |
| Local catalog at presentation boundaries | Chosen | Stable facts and escaping; every built-in phrase needs a reviewed translation |

## 8. Test strategy

TDD for precedence, consensus/conflict, missing evidence, retention and changed needs;
strict locales/record validation; localized labels/statuses/timing/accessibility;
source text and machine identity preservation; real CLI no-write and generation.
Paired English/Chinese examples share planning IDs/facts and reproduce all outputs.
Legacy fixtures remain byte-identical. Local Markdown/SVG inspection verifies Chinese
wrapping; no hosted rendering, machine translation or live agent interview claim.

## 9. Acceptance criteria

- AC23: User/project/existing/context priority, focused questions and retained choices agree across norms/skills.
- AC24: English/Chinese output localizes built-in labels in all selected formats without changing input facts or IDs.
- AC25: Missing/conflicting/unsupported language fails or asks explicitly; old inputs stay compatible.
- AC26: Paired source-backed examples and relevant automated/local visual checks pass.

## Quality attribute design

| Concern | rule_refs | Tactic / trade-off | Verification | Owner |
| --- | --- | --- | --- | --- |
| Identity integrity | ARC-001, TST-001 | Display mappings, no free-text replacement | Input/ID/URL equality checks | Renderer |
| Compatibility | ARC-005, TST-004 | Explicit 1.5 dispatch, old English unchanged | Legacy golden suites | Renderer |
| Boundaries | ERR-001, SEC-001, PERF-001 | Bounded evidence, strict locales and references | Malformed/conflict/limit tests | Language helper |
| Delivery | TST-003 | Real CLI and paired artifacts; caller owns natural text | CLI and example/visual checks | Skills/examples |
