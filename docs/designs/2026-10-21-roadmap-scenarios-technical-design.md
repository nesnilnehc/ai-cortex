---
artifact_type: technical-design
lifecycle: snapshot
created_at: 2026-10-21
parent: ../process-management/backlog/2026-10-20-roadmap-capabilities.md
status: approved
---

# Roadmap scenario selection

## 1. Goal

Provide reusable scenario combinations and source-backed examples, with a read-first
selection workflow that recommends useful views and preserves existing choices.

## 2. Architecture and service decomposition

| Component | Responsibility | Dependencies |
| --- | --- | --- |
| Spec / Rule | Selection evidence, compatibility and consistency | Existing roadmap contract |
| Scenario guide / template modules | Context-sensitive practice recommendations | Primary Scrum, Kanban and PMI guidance |
| Planning skills | Inspect sources, ask only missing facts, recommend and retain choices | Spec, guide and project records |
| Offline generator | Read-only recommendation; validate/render explicit decisions | Python standard library |

No new service, automatic user interview or external write is introduced. Scenario
recommendations are project synthesis, not framework certification or universal rules.

## 3. Components and detailed design

`recommend(data)` consumes partial planning context and an optional existing selection.
It emits JSON with status, missing-information questions, recommended/retained views,
primary perspective, layout and rationale. Existing choices win; changed context
requires review without overwriting them. `validate_selection(data)` validates the
schema 1.4 selection against top-level views. `selection_markdown(data)` shows the
chosen combination and decision source. `flow_markdown(data)` links workflow policy,
board, service expectation and metrics without implementing a Kanban system.
No application UI changes; the existing CLI/document pattern is extended.

## 4. Database design

No database change. Keep one selection decision in existing project norms/roadmap
sources; schema 1.4 carries its rendering projection. Do not create a separate
configuration service or automatically migrate older inputs.

## 5. Interface contracts

Schema 1.4 inherits prior facts/revisions. Explicit views add phases, milestones and
flow independently. Selection holds scenario, primary perspective, layout, rationale,
source and context (work mode, delivery mode, audience, constraints, source). Views
remain top-level authority. Optional flow fields are source/board/policy/expectation/
metrics references or text. CLI `--recommend` accepts partial context and writes
nothing; generation requires a settled selection. Layout conflicts fail rather than
silently override a retained choice. Prior schema output stays compatible.

## 6. Data flow and error handling

Existing project evidence → context gaps → focused questions → reasoned proposal →
user choice within existing authorization → source selection → validation/rendering.
Missing context produces needs-input, not an invented team. Invalid existing choice
fails explicitly, not a fallback recommendation. Conflicting layout/primary/selected
records fail before writes. CLI recommendation cannot be combined with generation
flags. I/O preflight and output bounds remain unchanged.

## 7. Technology choices and trade-offs

| Option | Decision and benefit | Cost |
| --- | --- | --- |
| Copy four complete templates | Rejected; simple entry points | Repeated common sections drift |
| Base template plus modules and four recipes | Chosen; shared structure, actionable entry points | Readers follow composition links |
| Infer a team from repository heuristics in renderer | Rejected; convenient | Unsupported assumptions become decisions |
| Explicit source context and read-only recommendation | Chosen; inspectable and deterministic | Skills/users gather evidence |

## 8. Test strategy

TDD covers four recommendation recipes, incomplete context, existing/custom choice
reuse, changed-context warnings, invalid decisions, independently disabled event
views, flow rendering, saved layout and real CLI no-write/error behavior. Four filled
scenarios carry independent evidence and reproducible outputs. Verify links, lint,
registry and versions. No live-agent interview or remote rendering claim.

## 9. Acceptance criteria

- AC19: Four recipes share a base and optional modules, with sourced advice and tailoring boundaries.
- AC20: Read-first intake asks only missing facts and emits a reasoned proposal; existing selections are retained.
- AC21: Generator validates explicit selection, supports flow/independent views and writes nothing during recommendation.
- AC22: Four complete examples reproduce source decisions and all applicable checks pass.

## Quality attribute design

| Concern | rule_refs | Tactic / trade-off | Verification | Owner |
| --- | --- | --- | --- | --- |
| Decision integrity | ARC-001, ERR-001 | Single source; no heuristic approval; explicit input needed | Missing/invalid/reuse tests | Skills / renderer |
| Compatibility | ARC-005, TST-004 | Versioned 1.4 dispatch retains old outputs | Legacy regression | Renderer |
| Bounded safe output | PERF-001, SEC-001 | Common bounds and preflight; no atomic I/O guarantee | CLI failure/no-write tests | Renderer |
| Integration | TST-001, TST-003 | Independent source tables and real CLI | Scenario reproduction and link checks | Examples |
