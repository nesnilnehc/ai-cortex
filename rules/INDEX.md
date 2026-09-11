# Rules Index

This document registers every passive constraint distributed by AI Cortex, the governable capability asset library for agents. Each Rule's `recommended_scope` determines whether it is long-lived user context or an on-demand project policy.

## Summary

- This file is the normative registry for passive constraints under `rules/`.
- User-scoped Rules apply across Skills as long-lived runtime constraints; project-scoped Rules are loaded only when the matched Skill or project configuration selects them.
- Governance relationship: `AGENTS.md` defines the behavioural contract and the authority boundaries; this registry enumerates the individual rule assets.
- Precedence model: where a rule conflicts with a skill's local preference, the global rule wins, unless a higher-precedence project contract overrides it explicitly.

---

## 1. Rule categories

| Category | Description |
| :--- | :--- |
| `content` | Format, tone, terminology and typography for text and documents, covering both writing and documentation. |
| `workflow` | Development process and documentation management policy. |
| `standards` | General and language-specific coding standards. |
| `architecture` | Cross-cutting architecture and design principles, such as the agentic artifact production paradigm. |
| `quality` | Versioned engineering quality criteria executed by review Skills before or after coding. |

---

## 2. Registry

Rules are listed by category and by when they apply.

| Rule | Category | Core value | When it applies |
| :--- | :--- | :--- | :--- |
| [agentic-artifact-paradigm](./agentic-artifact-paradigm.md) | architecture | The agentic artifact production paradigm: structure is scaffolding not an agenda, substance-led, extraction preferred over interrogation, the quality rule as oracle with the oracle guarded against form-filling. The higher-order principle shared by interactive and one-shot capabilities. | Designing or implementing an "input → spec artifact" agent capability |
| [architecture-quality](./architecture-quality.md) | quality | Stable architecture criteria for responsibility ownership, dependency direction, cycles, boundary leakage, contract evolution, coupling, composition and change surface. | Reviewing or designing production code with meaningful module or contract boundaries |
| [security-quality](./security-quality.md) | quality | Stable security criteria for input-to-sink safety, authorization, secrets, protected data, cryptography, dependencies, defaults and safe security telemetry. | Reviewing code or configuration that crosses a trust boundary or handles protected data |
| [reliability-quality](./reliability-quality.md) | quality | Stable reliability criteria for timeouts, retries, idempotency, partial failure, isolation, terminal background work, fault tests and release objectives. | Reviewing fallible I/O, durable workflows, background work or critical services |
| [performance-quality](./performance-quality.md) | quality | Stable performance criteria for bounded work, I/O amplification, complexity, streaming, concurrency, caching, budgets and resource ownership. | Reviewing work whose cost grows with input, data size or concurrency |
| [observability-quality](./observability-quality.md) | quality | Stable observability criteria for structured outcomes, correlation, SLIs, spans, telemetry safety, error ownership and background-work visibility. | Reviewing deployable services or production workflows that need diagnosis |
| [testing-quality](./testing-quality.md) | quality | Stable test adequacy criteria for behavior oracles, boundaries, integration assembly, contracts, critical paths, determinism, doubles and reproducible coverage. | Reviewing changed production behavior and its verification |
| [implementation-alignment-quality](./implementation-alignment-quality.md) | quality | Stable post-coding alignment criteria from approved acceptance/design/task intent to production code and verification evidence. | Reviewing an implemented change with an upstream artifact chain |
| [writing-chinese-technical](./writing-chinese-technical.md) | content | Chinese technical writing and typography, including spacing around numbers and units, and interface strings. | Any Chinese output |
| [standards-import](./standards-import.md) | standards | Keeping references in sync and ordered during refactoring, to reduce compile and runtime failures. | A code change involving module references |
| [workflow-documentation](./workflow-documentation.md) | workflow | Documentation management constraints such as minimise, DRY and naming for temporary documents. The decision tree lives in docs/guides. | Creating or maintaining a .md document |
| [workflow-rule-governance](./workflow-rule-governance.md) | workflow | Stable IDs, applicability, source hierarchy, compatibility, validation and auditable-waiver constraints for modeled engineering Rules. | Creating, changing, selecting or waiving a RULE_MODEL_V1 Rule item |
| [standards-coding](./standards-coding.md) | standards | General coding principles: organisation, comments, naming, error handling, logging, simplicity, complexity thresholds. | All code in the repository |
| [standards-shell](./standards-shell.md) | standards | Shell scripts: strict mode, log functions, trap, naming and variable quoting. | *.sh scripts |
| [standards-test-code](./standards-test-code.md) | standards | Test code standards: AAA, the three naming elements, isolation, determinism, Covers traceability, restraint with mocks. Does not cover QA business test cases. | Writing or reviewing *_test code files |
| [standards-agent-testing](./standards-agent-testing.md) | standards | Agent testing standards: separating deterministic from non-deterministic, extended oracles (contract / trajectory / rubric / golden / statistical), isolating real-model tests, regression gates on model and prompt changes. Applies on top of standards-test-code. | Testing LLM agent behaviour, in code and in contracts |
| [requirement-quality](./requirement-quality.md) | content | The 5-dimension review checklist and spec compliance for a requirement document. | Reviewing a requirement document |
| [requirement-intake-triage](./requirement-intake-triage.md) | content | The triage vocabulary for raw intake (functional / non-functional / design proposal / task / defect / insufficient information), the decision questions and the soundness lenses. The diagnostic SSOT shared by clarification and review. | Triaging or reviewing raw intake |
| [functional-design-quality](./functional-design-quality.md) | content | The 5-dimension review checklist and spec compliance for a functional design document. | Reviewing a functional design document |
| [technical-design-quality](./technical-design-quality.md) | quality | Stable pre-coding criteria for a technical design: completeness, executability, clarity, soundness, traceability and the triggered quality-attribute design. | Reviewing a technical design before tasks are derived |
| [task-quality](./task-quality.md) | quality | Stable pre-coding criteria for a task list: field completeness, dependency safety, executability, design coverage and engineering-governance annotations. | Reviewing a task list before assignment or coding |
| [roadmap-quality](./roadmap-quality.md) | content | The 5-dimension review checklist for a roadmap: core model, capacity baseline and allocation, metric triplets, dependencies mapped, change frequency. | Reviewing a roadmap document |
| [test-case-quality](./test-case-quality.md) | content | The 5-dimension review checklist and spec compliance for a QA business test case document. Does not cover code-level tests. | Reviewing a business test case document |
| [test-coverage-quality](./test-coverage-quality.md) | content | The 5-dimension review checklist for a test coverage report (completeness / truthfulness / explainability / risk alignment / currency and traceability) and spec compliance. Used when reviewing suite coverage and cross-artifact alignment. | Reviewing a coverage report — release gate, quarterly audit, upstream change |
| [doc-health-criteria](./doc-health-criteria.md) | content | The document health criteria: spec compliance, link graph, SSOT, code alignment, layer readiness. | A runtime, linter or CI checking document health |
| [repo-structure-hygiene](./repo-structure-hygiene.md) | workflow | Repository directory hygiene: misplacement, naming, empty directories, stale artifacts. | Auditing or self-checking repository structure |
| [adr-management](./adr-management.md) | workflow | ADR discipline: the two-question admission test, status field enforcement (5-value enum), the decay policy (archive at 12 months, deletable 6 months after that, ADRs themselves exempt from deletion), and the boundary with decisions. | Writing or maintaining an ADR |
| [claude-md-management](./claude-md-management.md) | workflow | CLAUDE.md discipline: length limits (≤ 300 lines at project level), expression, no-go content, revision principles, and a self-check that cites the spec item by item. | Writing or maintaining a CLAUDE.md at any level |
| [diagram-selection](./diagram-selection.md) | content | Diagram selection criteria: the relationship → diagram type → tool lookup, heuristics for choosing across tools (default Mermaid, and when to leave for PlantUML / Graphviz / flowchart.js), the rendering traps checklist, and constraints on splitting. | Drawing a technical diagram, or embedding one in a design document |

---

## 3. How to use

Rules with `recommended_scope: user` or `both` are injected as long-lived background constraints by supporting runtimes. Rules with `recommended_scope: project` are distributed but loaded on demand by the matched Skill or by explicit project configuration, preventing large concern-specific policies from consuming every session. While an atomic Skill executes, every applicable loaded Rule has precedence over the Skill's local preference.
