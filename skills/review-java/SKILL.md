---
name: review-java
description: "Review Java code for language and runtime conventions: concurrency, exceptions, try-with-resources, API versioning, collections and Streams, NIO, and testability. Language-only atomic skill; output is a findings list."
description_zh: 按 Java 语言与运行时规范审查代码：并发、异常、try-with-resources、API 版本、集合与 Stream、NIO、可测性。
tags: [code-review, language]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review java]
input_schema:
  type: code-scope
  description: Source files or directories to review
output_schema:
  type: findings-list
  description: Zero or more findings with location, category, severity, and suggestion
---

# Skill: Review Java

## Purpose

Review only the **language and runtime conventions** of **Java** code. Do not define the scope (diff vs codebase) and do not run security/architecture analysis; the scope and cognitive skills handle those. Emit a **findings list** in the standard format for aggregation. Concentrate on concurrency and thread safety, exceptions and try-with-resources, API and version compatibility, collections and streams, NIO and correct closing, modules (JPMS) where they apply, and testability.

---

## Core Objective

**Primary goal**: produce a Java language/runtime findings list covering concurrency, exceptions, resource management, API compatibility, collections/streams, NIO and testability across the given code scope.

**Success criteria** (all of them must hold):

1. ✅ **Java scope only**: only Java language and runtime conventions were reviewed; no scope selection, security or architecture analysis was performed
2. ✅ **All six Java dimensions covered**: concurrency/thread safety, exceptions/resources, API/version compatibility, collections/streams, NIO/closing and testability were assessed where relevant
3. ✅ **Findings format compatible**: every finding carries location, category (`language-java`), severity, title, description and an optional suggestion
4. ✅ **file:line references**: every finding points at a specific file location with a line number
5. ✅ **Non-Java code excluded**: Java-specific rules are not applied to non-Java files unless they are explicitly in scope

**Acceptance test**: does the output carry a Java-centred findings list, with file:line references covering every relevant language/runtime dimension, and without security, architecture or scope analysis?

---

## Scope Boundary

**This skill owns**:

- Concurrency and thread safety (synchronized, volatile, concurrent collections, executor lifecycle)
- Exception handling (try-with-resources, the Throwable hierarchy, rethrow patterns)
- API stability and version compatibility (deprecated APIs, JPMS boundaries)
- Collections and the Stream API (allocation, boxing, side effects, immutability)
- NIO and resource closing (streams, channels, selectors)
- Testability (DI, singleton usage, final vs overridable design)

**This skill does not own**:

- Scope selection — the scope comes from the caller
- Security analysis — use `review-security`
- Architecture analysis — use `review-architecture`
- SQL-specific analysis — use `review-sql`
- A full orchestrated review — use `orchestrate-code-review`

**Handoff point**: once every Java finding has been emitted, hand it to `orchestrate-code-review` for aggregation. For SQL or security problems spotted in Java code, note them and suggest the appropriate cognitive skill.

---

## Use Cases

- **Orchestrated review**: used as the language step when [orchestrate-code-review](../orchestrate-code-review/SKILL.md) runs scope → language → framework → library → cognitive over a Java project.
- **Java-only review**: when the user wants to check language/runtime conventions alone.
- **Pre-PR Java checklist**: confirm that concurrency, resource management and API compatibility are correct.

**When to use**: when the code under review is Java and the task includes language/runtime quality. The scope is set by the caller or the user.

---

## Behavior

### What this skill covers

- **Analyze**: Java language and runtime conventions inside the **given code scope** (files or a diff supplied by the caller). It does not decide the scope; it takes the code scope as input.
- **Do not**: perform scope selection, a security review or an architecture review; do not check Java rules in non-Java files unless they are explicitly in scope.

### Review checklist (Java dimensions only)

1. **Concurrency and thread safety**: correct use of synchronized, volatile, locks or the concurrency API; visibility and happens-before; shared mutable state; executor usage and shutdown.
2. **Exceptions and resources**: try-with-resources for Closeable/AutoCloseable; exception handling and suppression; avoid empty catches or overly broad catches.
3. **API and version compatibility**: public API stability; backward compatibility; use of deprecated APIs and the migration path; module boundaries (JPMS) where they apply.
4. **Collections and Streams**: appropriate use of the Stream API; side effects inside streams; allocation and boxing; immutable collections where they fit.
5. **NIO and closing**: correct closing of streams, channels and selectors; avoid resource leaks; use try-with-resources.
6. **Testability**: dependency injection; static and singleton usage; overridable vs final; test doubles and mocking.

### Tone and references

- **Professional and technical**: cite a concrete location (file:line). Emit findings carrying location, category, severity, title, description, suggestion.

---

## Input and Output

### Input

- **Code scope**: files or directories (or a diff) already selected by the user or by the scope skill. This skill does not decide the scope; it checks language conventions in the Java code it is given.

### Output

- Emit zero or more **findings** in the format defined in **Appendix: Output Contract**.
- The category for this skill is **language-java**.

---

## Restrictions

### Hard Boundaries

- **Do not** perform security, architecture or scope selection. Stay inside Java language and runtime conventions.
- **Do not** land a conclusion without a concrete location or an actionable suggestion.
- **Do not** check Java-specific rules in non-Java code unless it is explicitly in scope.

### Skill Boundaries

**Do not do these** (other skills handle them):

- Do not select or define the code scope - the caller or `orchestrate-code-review` sets it
- Do not perform security analysis — use `review-security`
- Do not perform architecture analysis — use `review-architecture`
- Do not perform full SQL analysis — use `review-sql`

**When to stop and hand off**:

- Once every Java finding has been emitted, hand it to `orchestrate-code-review` for aggregation
- When the user wants a full review (scope + language + cognitive), redirect to `orchestrate-code-review`
- When a SQL or security problem turns up, note it and suggest the appropriate cognitive skill

---

## Self-Check

### Core success criteria

- [ ] **Java scope only**: only Java language and runtime conventions were reviewed; no scope selection, security or architecture analysis was performed
- [ ] **All six Java dimensions covered**: concurrency/thread safety, exceptions/resources, API/version compatibility, collections/streams, NIO/closing and testability were assessed where relevant
- [ ] **Findings format compatible**: every finding carries location, category (`language-java`), severity, title, description and an optional suggestion
- [ ] **file:line references**: every finding points at a specific file location with a line number
- [ ] **Non-Java code excluded**: Java-specific rules are not applied to non-Java files unless they are explicitly in scope

### Process quality checks

- [ ] Were only the Java language/runtime dimensions reviewed (no scope/security/architecture)?
- [ ] Were the relevant concurrency, exception, resource, collections/stream, NIO and testability aspects covered?
- [ ] Does every finding carry location, category=language-java, severity, title, description and an optional suggestion?
- [ ] Does a file:line reference point at each issue?

### Acceptance test

Does the output carry a Java-centred findings list, with file:line references covering every relevant language/runtime dimension, and without security, architecture or scope analysis?

---

## Examples

### Example 1: resources and exceptions

- **Input**: a Java method that opens an InputStream without try-with-resources.
- **Expected**: emit a resource-management finding; suggest try-with-resources. category=language-java.

### Example 2: concurrency

- **Input**: a shared mutable list reached from several threads with no synchronization and no concurrent collection.
- **Expected**: emit a thread-safety finding (for example, use CopyOnWriteArrayList or synchronization); cite the field and its usage. category=language-java.

### Edge case: mixed Java and SQL

- **Input**: a file holding JDBC or JPA alongside Java logic.
- **Expected**: review the Java conventions only (resources, exceptions, concurrency). Do not emit SQL injection findings here; those belong to review-security or review-sql.
