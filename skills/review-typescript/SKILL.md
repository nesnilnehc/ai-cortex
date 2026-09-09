---
name: review-typescript
description: Review TypeScript/JavaScript code for type safety, async patterns, error handling, and module design. Atomic skill; output is a findings list.
description_zh: 审查 TypeScript/JavaScript 代码：类型安全、异步模式、错误处理与模块设计；原子技能。
tags: [code-review, language]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review typescript, review ts]
input_schema:
  type: code-scope
  description: Source files or directories to review
output_schema:
  type: findings-list
  description: Zero or more findings with location, category, severity, and suggestion
---

# Skill: Review TypeScript

## Purpose

Review **TypeScript and JavaScript** code for **language and runtime conventions** only. Do not define scope (diff vs codebase) or perform security/architecture analysis; those are handled by the scope and cognitive skills. Emit a **findings list** in the standard format for aggregation. Focus on type safety and type system usage, async patterns and Promise handling, error handling, module design, runtime correctness, API and interface design, and performance and memory considerations.

---

## Core Objective

**Primary goal**: produce a TypeScript/JavaScript language findings list covering type safety, async patterns, error handling, module design, runtime correctness, API/interface design, and performance/memory for the given code scope.

**Success criteria** (all must hold):

1. ✅ **TypeScript/JavaScript language scope only**: reviews TypeScript and JavaScript language and runtime conventions only; performs no scope selection, security, or architecture analysis
2. ✅ **All seven language dimensions covered**: type safety, async patterns, error handling, module design, runtime correctness, API/interface design, and performance/memory are assessed where relevant
3. ✅ **Findings format compliant**: each finding carries location, category (`language-typescript`), severity, title, description, and an optional suggestion
4. ✅ **File/line references**: every finding cites a specific file:line or symbol name
5. ✅ **Non-TS/JS code excluded**: non-TypeScript/JavaScript files are not analyzed against TS/JS-specific rules unless they are explicitly in scope

**Acceptance** test: does the output contain a TypeScript/JavaScript-centered findings list with file/line references covering all relevant language dimensions, without performing security, architecture, or scope analysis?

---

## Scope Boundaries

**This skill owns**:

- Type safety and type system usage (strict mode, precise types, `any` avoidance, discriminated unions, type guards, generics)
- Async patterns (async/await, Promise handling, error propagation, race conditions, unhandled rejections)
- Error handling (try/catch patterns, custom error types, error boundaries, exhaustive error handling)
- Module design (ESM vs CJS, barrel exports, circular dependencies, tree-shaking, side effects)
- Runtime correctness (null/undefined handling, equality checks, coercion pitfalls, prototype pollution)
- API and interface design (function signatures, overloads, branded types, readonly correctness)
- Performance and memory (closure leaks, event listener cleanup, WeakRef/WeakMap usage, bundle size impact)

**This skill does not own**:

- Scope selection — the scope is supplied by the caller
- Security analysis (injection, secrets, XSS) — use `review-security`
- Architecture analysis — use `review-architecture`
- Framework conventions (Vue, React, Angular) — use the framework-specific skill (for example `review-vue`)
- Full orchestrated review — use `orchestrate-code-review`

**Handoff point**: once all TypeScript/JavaScript findings are emitted, hand them to `orchestrate-code-review` for aggregation. For injection risks or secrets in the code, note them and point at `review-security`.

---

## Use Cases

- **Orchestrated review**: serves as the language step when [orchestrate-code-review](../orchestrate-code-review/SKILL.md) runs scope → language → framework → library → cognitive on a TypeScript/JavaScript project.
- **TypeScript-only review**: when the user wants nothing but TypeScript/JavaScript language conventions checked.
- **Pre-PR language checklist**: confirm type safety, async correctness, and sound module design before merging.

**When to use**: when the code under review is TypeScript or JavaScript and the task includes language quality. Scope is set by the caller or the user.

---

## Behavior

### What this skill covers

- **Analyse**: TypeScript and JavaScript language and runtime conventions inside the **given code scope** (files or a diff supplied by the caller). Does not decide scope; takes the code scope as input.
- **Do not**: perform scope selection, security review, or architecture review; do not check non-TS/JS files against TS/JS rules unless they are in scope.

### Review checklist (TypeScript/JavaScript language only)

1. **Type safety and type system usage**: enforce `strict` mode; prefer explicit types over `any`; model state with discriminated unions; apply type guards and narrowing; use generics for reuse without giving up type information; avoid type assertions (`as`) where narrowing would do.
2. **Async patterns**: ensure correct async/await usage and Promise chaining; verify error propagation across async boundaries; detect race conditions and unhandled Promise rejections; check for dangling Promises (missing `await`); verify concurrency patterns (`Promise.all`, `Promise.allSettled`).
3. **Error handling**: verify try/catch placement and specificity; prefer custom error types over bare strings or a raw Error; ensure exhaustive error handling (switch/if-else covering every case); check that errors carry enough context; verify cleanup in finally blocks.
4. **Module design**: prefer ESM (`import` / `export`) over CJS (`require` / `module.exports`); audit barrel exports for tree-shaking impact; detect circular dependencies; check for unintended side effects at module scope; verify consistent module resolution.
5. **Runtime correctness**: check null/undefined handling (optional chaining, nullish coalescing); enforce strict equality (`===`/`!==`); detect coercion pitfalls (implicit type conversion); check prototype pollution risk; verify iterator/generator correctness.
6. **API and interface design**: check function signatures for clarity and consistency; verify overloads are ordered correctly and unambiguous; check branded/opaque types for domain safety; enforce `readonly` where mutation would be unintended; verify index signatures and mapped types.
7. **Performance and memory**: detect closure-based memory leaks; verify event listener and subscription cleanup; check WeakRef/WeakMap usage for caching patterns; assess the bundle size impact of imports; identify hot-path inefficiencies (for example unnecessary allocations inside a loop).

### Tone and references

- **Professional and technical**: cite the exact location (file:line or symbol name). Emit findings carrying location, category, severity, title, description, and suggestion.

---

## Input & Output

### Input

- **Code scope**: files or directories (or a diff) containing TypeScript or JavaScript code (.ts, .tsx, .js, .jsx, .mts, .mjs, .cts, .cjs). Supplied by the user or by a scope skill.

### Output

- Emit zero or more **findings** in the format defined in **Appendix: Output Contract**.
- The category for this skill is **language-typescript**.

---

## Restrictions

### Hard Boundaries

- **Do not** perform scope selection, security, or architecture review. Stay inside TypeScript/JavaScript language and runtime conventions.
- **Do not** state a finding without a concrete location or an actionable suggestion.
- **Do not** review non-TS/JS code against TS/JS-specific rules unless it is explicitly in scope.

### Skill Boundaries

**Do not do these** (other skills handle them):

- Do not select or define the code scope - it is set by the caller or by `orchestrate-code-review`
- Do not perform security analysis (injection, secrets) — use `review-security`
- Do not perform architecture analysis — use `review-architecture`
- Do not review framework-specific conventions (Vue, React, Angular) — use the corresponding framework skill

**When to stop and hand off**:

- Once all TypeScript/JavaScript findings are emitted, hand them to `orchestrate-code-review` for aggregation
- When injection risks or secrets turn up, note them and point at `review-security`
- When the user wants a full review (scope + language + cognitive), redirect to `orchestrate-code-review`

---

## Self-Check

### Core success criteria

- [ ] **TypeScript/JavaScript language scope only**: reviews TypeScript and JavaScript language and runtime conventions only; performs no scope selection, security, or architecture analysis
- [ ] **All seven language dimensions covered**: type safety, async patterns, error handling, module design, runtime correctness, API/interface design, and performance/memory are assessed where relevant
- [ ] **Findings format compliant**: each finding carries location, category (`language-typescript`), severity, title, description, and an optional suggestion
- [ ] **File/line references**: every finding cites a specific file:line or symbol name
- [ ] **Non-TS/JS code excluded**: non-TypeScript/JavaScript files are not analyzed against TS/JS-specific rules unless they are explicitly in scope

### Process quality checks

- [ ] Were only TypeScript/JavaScript language dimensions reviewed (no scope/security/architecture)?
- [ ] Were type safety, async patterns, error handling, module design, runtime correctness, API design, and performance covered where relevant?
- [ ] Does every finding carry location, category = language-typescript, severity, title, description, and an optional suggestion?
- [ ] Is each issue referenced by file:line or symbol name?

### Acceptance test

Does the output contain a TypeScript/JavaScript-centered findings list with file/line references covering all relevant language dimensions, without performing security, architecture, or scope analysis?

---

## Examples

### Example 1: unsafe use of `any`

- **Input**: a module whose function parameters are typed `any` with no runtime validation.
- **Expected**: one finding (major) for the unsafe `any` usage; the suggestion is to replace it with a proper type, a generic, or `unknown` plus narrowing. Category = language-typescript.

### Example 2: missing `await` on an async call

- **Input**: an async function calls another async function without `await`, discarding the Promise.
- **Expected**: one finding (critical/major) for the dangling Promise; the suggestion is to add `await` or handle the returned Promise explicitly. Category = language-typescript.

### Edge case: ESM and CJS mixed in one project

- **Input**: a project where some files use `import`/`export` and others use `require`/`module.exports`.
- **Expected**: a finding for inconsistent module system usage; the suggestion is to migrate to a single module system (preferably ESM) or to document why the mix exists. Category = language-typescript.
