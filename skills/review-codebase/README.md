# Review Codebase

Runs a scope-only atomic review over a given path (file / directory / repository) across 5 dimensions: module boundaries, pattern consistency, cross-module dependencies, technical debt, and interface stability.

## Relationship to sibling skills

- `review-diff` — the either/or counterpart: this skill looks at a snapshot, review-diff looks at git changes
- `orchestrate-code-review` — the orchestrator: treats this skill as a candidate for the scope step

## When to use

- New module review: point it at `src/auth/` to see the current structure
- Legacy path audit: point it at a path to see technical debt and boundary problems
- Spot review: files or directories a colleague names, with no diff needed

## When not to use

- Reviewing git changes only → `review-diff`
- The security / performance / architecture cognitive dimensions → `review-security` / `review-performance` / `review-architecture`
- Language- or framework-specific conventions → `review-<lang>` / `review-<framework>`

## Inputs

- A path (one or more files / directories)
- Optional: a focus hint

## Outputs

- A findings list (with file:line references), grouped by file or by module

## Full definition

See [SKILL.md](./SKILL.md).
