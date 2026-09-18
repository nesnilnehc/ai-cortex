---
artifact_type: rule
name: standards-coding
version: 1.1.0
scope: all code in the repository, across languages
recommended_scope: user
status: active
---

# Rule: General Coding Principles

## Scope

All code in the project, in every language. These are general principles; where a language-specific rule such as standards-shell also applies, both must be satisfied.

## Constraints

1. **Organisation**: modular, single responsibility, top-down, related functions kept near each other.
2. **Comments**: explain *why*, not *what*. Comment only what is not self-evident. A complex function must document its parameters and return value. Update comments together with the code they describe.
3. **Naming**: descriptive, consistent, avoid unestablished abbreviations, meaningful within its scope.
4. **Error handling**: one consistent error-handling mechanism; resources released correctly on the error path. Where a failure must be detected, and what the resulting message owes its reader, are defined by [error-surfacing-quality](./error-surfacing-quality.md) — cite its items rather than restating them here.
5. **Logging**: use the standard log levels and the shared log function; no echoing or printing debug output directly; enough context in each log line; verbosity controllable by a parameter.
6. **Simplicity**: follow DRY, avoid over-abstraction, and delete stale comments. Code no consumer reaches, including a commented-out former implementation, is [architecture-quality](./architecture-quality.md) ARC-010.
7. **Complexity thresholds**: a function is ≤ 50 lines; nesting is ≤ 3 levels; duplicated code must be extracted into a function; stale comments must be deleted.

## Bad Patterns

- A comment that merely restates the code — `// set variable x to 1`.
- An error path that releases no resource, or a module that raises in one style and returns codes in another.
- The same logic copied in several places instead of extracted into a function.

## Remediation

1. Extract the duplicated logic into a function; reduce nesting with early returns.
2. Replace direct echo/print calls with the shared log function; release resources on the error path.
3. Delete stale comments; add "why" comments and function documentation to complex logic.

## References

- [Classic software engineering sources](../docs/references/software-engineering-classics.md) — source hierarchy and applicability boundaries
- [Code Complete, Second Edition](https://www.microsoftpressstore.com/store/code-complete-9780735619678) — construction complexity, naming, defensive programming and collaborative construction
- [The Pragmatic Programmer, 20th Anniversary Edition](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/) — DRY knowledge, orthogonality, resource balance, feedback and deliberate testing
- [Refactoring, Second Edition](https://martinfowler.com/books/refactoring.html) — small behavior-preserving changes and code-smell-guided structural improvement
- [Error Surfacing Quality](./error-surfacing-quality.md) and [Architecture Quality](./architecture-quality.md) — obligations this document points at rather than restating
