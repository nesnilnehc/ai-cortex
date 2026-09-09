---
name: standards-coding
version: 1.0.0
scope: all code in the repository, across languages
recommended_scope: user
---

# Rule: General Coding Principles

## Scope

All code in the project, in every language. These are general principles; where a language-specific rule such as standards-shell also applies, both must be satisfied.

## Constraints

1. **Organisation**: modular, single responsibility, top-down, related functions kept near each other.
2. **Comments**: explain *why*, not *what*. Comment only what is not self-evident. A complex function must document its parameters and return value. Update comments together with the code they describe.
3. **Naming**: descriptive, consistent, avoid unestablished abbreviations, meaningful within its scope.
4. **Error handling**: fail fast; error messages carry context and a suggested resolution; one consistent error-handling mechanism; resources released correctly on the error path.
5. **Logging**: use the standard log levels and the shared log function; no echoing or printing debug output directly; enough context in each log line; verbosity controllable by a parameter.
6. **Simplicity**: follow DRY, avoid over-abstraction, and keep neither commented-out dead code nor stale comments.
7. **Complexity thresholds**: a function is ≤ 50 lines; nesting is ≤ 3 levels; duplicated code must be extracted into a function; stale comments must be deleted.

## Bad Patterns

- A comment that merely restates the code — `// set variable x to 1`.
- An error swallowed, or printed without context.
- The same logic copied in several places instead of extracted into a function.
- Large blocks of commented-out former implementation left in place.

## Remediation

1. Extract the duplicated logic into a function; reduce nesting with early returns.
2. Replace direct echo/print calls with the shared log function; add context and cleanup to the error path.
3. Delete dead code and stale comments; add "why" comments and function documentation to complex logic.
