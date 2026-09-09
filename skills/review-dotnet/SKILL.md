---
name: review-dotnet
description: "Review .NET (C#/F#) code for language and runtime conventions: async/await, nullable, API versioning, IDisposable, LINQ, and testability. Language-only atomic skill; output is a findings list."
description_zh: 按 .NET (C#/F#) 语言与运行时规范审查代码：async/await、nullable、API 版本、IDisposable、LINQ、可测性。
tags: [code-review, language]
version: 1.0.1
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review dotnet, review csharp]
input_schema:
  type: code-scope
  description: Source files or directories to review
output_schema:
  type: findings-list
  description: Zero or more findings with location, category, severity, and suggestion
---

# Skill: Review .NET

## Purpose

Review only the **language and runtime conventions** of code in the **.NET** ecosystem (C#, F#). Do not define the scope (diff vs codebase) and do not run security/architecture analysis; the scope and cognitive skills handle those. Emit a **findings list** in the standard format for aggregation. Concentrate on async/await and ConfigureAwait, nullable reference types and avoiding NREs, API and versioning, resources and IDisposable, collections and LINQ, and testability.

---

## Core Objective

**Primary goal**: produce a .NET language/runtime findings list covering async/await, nullable types, API stability, resource management, LINQ usage and testability across the given code scope.

**Success criteria** (all of them must hold):

1. ✅ **.NET scope only**: only .NET (C#/F#) language and runtime conventions were reviewed; no scope selection, security or architecture analysis was performed
2. ✅ **All six .NET dimensions covered**: async/await, nullable reference types, API/versioning, resources/IDisposable, collections/LINQ and testability where relevant
3. ✅ **Findings format compatible**: every finding carries location, category (`language-dotnet`), severity, title, description and an optional suggestion
4. ✅ **file:line references**: every finding points at a specific file location with a line number
5. ✅ **Non-.NET code excluded**: .NET-specific rules are not applied to non-.NET files unless they are explicitly in scope

**Acceptance** test: does the output carry a .NET-centred findings list whose file:line references cover every relevant language/runtime dimension, and without security, architecture or scope analysis?

---

## Scope Boundary

**This skill owns**:

- async/await correctness and ConfigureAwait usage (library vs application code)
- Nullable reference types and avoiding NREs
- Public API stability and the versioning policy
- IDisposable, IAsyncDisposable and using-statement patterns
- Collection and LINQ efficiency (multiple enumeration, allocation, Span/Memory)
- Testability (DI, sealed vs overridable, static usage)

**This skill does not own**:

- Scope selection — the scope comes from the caller
- Security analysis (injection, auth, cryptography) — use `review-security`
- Architecture analysis — use `review-architecture`
- A performance deep dive — use `review-performance`
- A full orchestrated review — use `orchestrate-code-review`
- Codebase state review — use `review-codebase`

**Handoff point**: once every .NET finding has been emitted, hand it to `orchestrate-code-review` for aggregation. For security or architecture problems spotted in .NET code, note them and suggest running the appropriate cognitive skill.

---

## Use Cases

- **Orchestrated review**: used as the language step when [orchestrate-code-review](../orchestrate-code-review/SKILL.md) runs scope → language → framework → library → cognitive over a .NET project.
- **.NET-only review**: when the user wants to check language/runtime conventions alone (after adding new C# files, for example).
- **Pre-PR .NET checklist**: confirm that the async, nullable and resource patterns are correct.

**When to use**: when the code under review is .NET (C#/F#) and the task includes language/runtime quality. The scope (diff vs path) is set by the caller or the user.

---

## Behavior

### What this skill covers

- **Analyze**: .NET language and runtime conventions inside the **given code scope** (files or a diff supplied by the caller). It does not decide the scope; it takes the code scope as input.
- **Do not**: perform scope selection (diff vs codebase), a security review or an architecture review; do not look at non-.NET files unless asked to disregard the language.

### Review checklist (.NET dimensions only)

1. **async/await and ConfigureAwait**: correct use of async; ConfigureAwait(false) where appropriate (library code); cancellation-token propagation; avoid async void outside event handlers.
2. **Nullable reference types and NREs**: nullable annotations; null checks and null-forgiving where justified; avoid needless null-forgiving.
3. **API and versioning**: public API surface stability; breaking changes; the versioning or deprecation policy for a library.
4. **Resources and IDisposable**: correct use of IDisposable, the using statement, IAsyncDisposable; no leaked handles or streams.
5. **Collections and LINQ**: appropriate use of LINQ; allocation and enumeration; avoid multiple enumeration; Span/Memory where relevant.
6. **Testability**: dependency injection and testability; static usage; sealed vs overridable where it affects tests.

### Tone and references

- **Professional and technical**: cite a concrete location (file:line). Emit findings carrying location, category, severity, title, description, suggestion.

---

## Input and Output

### Input

- **Code scope**: files or directories (or a diff) already selected by the user or by the scope skill. This skill does not decide the scope; it checks language conventions in the .NET code it is given.

### Output

- Emit zero or more **findings** in the format defined in [specs/findings-list.md](../../specs/findings-list.md), with **Category** `language-dotnet`.
- The category for this skill is **language-dotnet**.

---

## Restrictions

### Hard Boundaries

- **Do not** perform security, architecture or scope selection. Stay inside .NET language and runtime conventions.
- **Do not** land a conclusion without a concrete location or an actionable suggestion.
- **Do not** check .NET-specific rules in non-.NET code unless the user explicitly includes it (an embedded script, for example).

### Skill Boundaries

**Do not do these** (other skills handle them):

- Do not select or define the code scope - the caller or `orchestrate-code-review` sets it
- Do not perform security analysis — use `review-security`
- Do not perform architecture analysis — use `review-architecture`
- Do not review non-.NET code against .NET conventions

**When to stop and hand off**:

- Once every .NET finding has been emitted, hand it to `orchestrate-code-review` for aggregation
- When the user wants a full review (scope + language + cognitive), redirect to `orchestrate-code-review`
- When a security problem turns up in .NET code, note it and suggest `review-security`

---

## Self-Check

### Core success criteria

- [ ] **.NET scope only**: only .NET (C#/F#) language and runtime conventions were reviewed; no scope selection, security or architecture analysis was performed
- [ ] **All six .NET dimensions covered**: async/await, nullable reference types, API/versioning, resources/IDisposable, collections/LINQ and testability where relevant
- [ ] **Findings format conformant**: every finding carries location, category (`language-dotnet`), severity, title, description and an optional suggestion
- [ ] **file:line references**: every finding points at a specific file location with a line number
- [ ] **Non-.NET code excluded**: .NET-specific rules are not applied to non-.NET files unless they are explicitly in scope

### Process quality checks

- [ ] Were only the .NET language/runtime dimensions reviewed (no scope/security/architecture)?
- [ ] Were the relevant async, nullable, IDisposable, LINQ and testability aspects covered?
- [ ] Does every finding carry location, category=language-dotnet, severity, title, description and an optional suggestion?
- [ ] Does a file:line reference point at each issue?

### Acceptance test

Does the output carry a .NET-centred findings list with file:line references covering every relevant language/runtime dimension, and without security, architecture or scope analysis?

---

## Examples

### Example 1: an async method

- **Input**: an async C# method that calls other async methods without passing a CancellationToken.
- **Expected**: emit a finding on CancellationToken propagation (minor/suggestion, say); cite the method and its parameter list. category = language-dotnet.

### Example 2: nullable and disposal

- **Input**: a C# class that holds an IDisposable but neither implements IDisposable nor uses using.
- **Expected**: emit a finding on resource disposal, and possibly on nullability if the field can be null. category = language-dotnet.

### Edge case: mixed C# and SQL

- **Input**: a file containing C# alongside embedded SQL strings.
- **Expected**: review only the C# part against .NET conventions (async, nullable, disposal, say). Do not emit SQL injection findings; those belong to review-security or review-sql.
