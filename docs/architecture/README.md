# Architecture

AI Cortex architecture is defined by the [Evolution Roadmap](../designs/2026-03-02-ai-cortex-evolution-roadmap.md) Layer A–E model.

## Layers

| Layer | Scope |
| :--- | :--- |
| **A** | Engineering Infrastructure — CI/CD, quality gates |
| **B** | Skill Coverage — languages, frameworks, libraries |
| **C** | Orchestration & Composition — orchestrators, skill chains |
| **D** | Ecosystem & Distribution — Plugin sync, community |
| **E** | Specification Evolution — lifecycle, testable spec |

## Canonical sources

- **[Evolution Roadmap](../designs/2026-03-02-ai-cortex-evolution-roadmap.md)** — Layer definitions, components, implementation phases
- **[skillgraph.md](../../skills/skillgraph.md)** — skill composition and dependencies
- **[spec/skill.md](../../spec/skill.md)** — skill structure and metadata spec

## ADRs

| ADR | Title | Status |
| :--- | :--- | :--- |
| [001](adrs/001-io-contract-protocol.md) | I/O Contract Protocol for Skill Chaining | Accepted |

## When to expand

Add ADRs (e.g. `docs/architecture/adrs/002-*.md`) when:

- Major design decisions need explicit rationale
- `brainstorm-design` produces approved architecture choices that warrant persistence
- Cross-skill or cross-phase dependencies need documentation
