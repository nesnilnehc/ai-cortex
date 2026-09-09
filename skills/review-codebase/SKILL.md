---
name: review-codebase
description: "Review given file/dir/repo for current-state code organization: module boundaries, design patterns, cross-module dependencies, tech debt, and interface stability. Scope-only atomic skill; output is a findings list."
description_zh: 对给定路径（文件 / 目录 / 仓库）做 scope-only 原子审查，覆盖模块边界、模式一致性、跨模块依赖、技术债与接口稳定性。
tags: [code-review, scope-only]
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review codebase, codebase review]
input_schema:
  type: code-scope
  description: Files, directories, or repository path to review for current-state structure
output_schema:
  type: findings-list
  description: Findings on module boundaries, patterns, dependencies, tech debt, and interface stability
---

# Skill: Review Codebase

## Purpose

Run a scope-only atomic review of the **current state** of a **given path** (a single file / a directory / a repository). Paired with `review-diff` (which reviews git changes only), it is one of the two scope-step candidates for orchestrate-code-review — this skill looks at the snapshot, review-diff looks at the change.

**Not done here**: cognitive dimensions such as security / performance / architecture (the cognitive-step atomic skills `review-security` / `review-performance` / `review-architecture` take those), and language- or framework-specific analysis (the language / framework steps take that).

---

## Core Objective

**Primary goal**: produce a scope-only findings list that identifies the structural problems in a given path (boundaries, patterns, dependencies, tech debt, interfaces).

**Success criteria** (all of them must hold):

1. ✅ **Scope confirmed**: confirm the user's path or directory before analysis
2. ✅ **5 dimensions covered**: findings are emitted for module boundaries, pattern consistency, cross-module dependencies, tech debt and interface stability
3. ✅ **Precise locations**: every finding carries a `file:line` reference
4. ✅ **Format conformant**: findings carry location / category (`scope`) / severity / title / description / suggestion
5. ✅ **Large scopes handled**: for a repository-level scope, emit by layer (module / directory), or settle a priority subset with the user
6. ✅ **No overreach**: no security / performance / architecture / language / framework cognitive findings are emitted (they are flagged, pointing at the matching atomic skill)

---

## Scope Boundaries

**This skill owns**:

- Structural review of the current state of the given path
- Findings across 5 dimensions: module boundaries, pattern consistency, cross-module dependency and coupling, tech debt and maintainability, interface stability

**This skill does not own**:

- Reviewing git changes alone (use `review-diff`)
- The full orchestrated review (use `orchestrate-code-review`)
- Language- / framework-specific conventions (use `review-<lang>` / `review-<framework>`)
- The security / performance / architecture cognitive dimensions (use `review-security` / `review-performance` / `review-architecture`)

**Handoff point**: once the findings are out, they feed the scope step of orchestrate-code-review for aggregation, or go to the user to decide what follows (refactoring / a deeper review).

---

## Use Cases

- **New module review**: given `src/auth/`, look at the current structure and dependencies
- **Legacy path audit**: given a path, look at tech debt and boundary problems
- **Sampled review**: a file or directory a colleague names, with no diff needed
- **As the scope step of orchestrate-code-review**: one of the two, alongside `review-diff`

---

## Behavior

### Scope resolution

- **The input defines the scope**: a single file / a directory / the repository root / several paths, named by the user
- **No dependence on a diff**: analyze the current file content; a diff the user supplies is context only, not a requirement

### Defaults and pre-run confirmation

| Item | Default | How the user departs from it |
|---|---|---|
| **Path** | Repository root | Choose: [repository root] / [the current file's directory] / [list the top-level directories and pick] |
| **Large-scope handling** | Emit by layer (module / directory) | Choose a priority subset (from the top-level directory list) |

Two things must be confirmed before the run: (1) the review path; (2) for a large scope, by-layer vs priority subset.

### The 5 dimensions

For the code in scope (at the layer / subset the user chose), emit findings on these dimensions:

1. **Module boundaries**: whether module / service boundaries are clear, whether responsibilities are single, whether the dependency direction is sound
2. **Pattern consistency**: whether patterns are used aptly and match the repository's existing style
3. **Cross-module dependency and coupling**: dependency relations, cyclic dependencies, degree of coupling
4. **Tech debt and maintainability**: duplication, complexity, testability, the current state of docs and comments
5. **Interface stability**: how clear and how stable a module's outward interface is

Every finding must carry a `file:line` reference.

### Flagging out-of-scope findings

When the analysis turns up a concrete security / performance / architecture / language / framework problem: **flag it and point at the matching atomic skill**, without opening the analysis. For example:

> Potential SQL injection risk detected (user input concatenated without escaping); suggest running `review-security`

---

## Input and Output

### Input

- **Path**: one or more file / dir paths
- **Optional**: a focus hint ("concentrate on module boundaries", for example)

### Output

- **Findings list**: the standard format (location / category=scope / severity / title / description / suggestion), grouped by file or by module
- **Large-scope summary**: when organized by layer, emit the findings count and severity distribution for each layer

---

## Restrictions

### Hard boundaries

- Do not assume "the diff only" — by default this skill reviews the complete current state of the given scope
- Emit no cognitive-dimension findings (security / performance / architecture)
- Emit no language- / framework-specific findings
- Emit no finding that lacks a `file:line` reference
- Use no vague language ("might be a problem", carrying neither a type nor a direction → delete it)

### Skill boundaries

**Not done here** (other atomic skills own it):

- Reviewing git changes → `review-diff`
- Full-dimension orchestration → `orchestrate-code-review`
- Language conventions → `review-<lang>`
- Framework conventions → `review-<framework>`
- Security / performance / architecture → `review-security` / `review-performance` / `review-architecture`

---

## Self-Check

- [ ] The scope was confirmed with the user
- [ ] A large scope was emitted by layer, or a priority subset was settled
- [ ] All 5 dimensions are covered (module boundaries / patterns / dependencies / tech debt / interfaces)
- [ ] Every finding carries a file:line reference
- [ ] No cognitive / language / framework dimension finding was emitted (they are flagged only, pointing at the matching atomic skill)
- [ ] The output format conforms (location / category / severity / title / description / suggestion)

---

## Examples

### Example 1: a single directory

- Input: `src/auth/`
- Output: findings across the 5 dimensions, grouped by file, each carrying a reference of the `auth.go:42` kind; a weak crypto algorithm is flagged only, pointing at `review-security`

### Example 2: a single file

- Input: `pkg/validator/validator.go`
- Output: findings on module responsibility / interface clarity / test coverage / dependencies on upstream modules

### Example 3: the whole repository (large scope)

- Input: the repository root
- Behavior: first emit a findings summary table by layer (top-level directory), then have the user pick a priority subset to go deeper on
- Output: the layer summary plus detailed findings for the priority subset
