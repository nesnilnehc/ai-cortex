---
name: review-orm-usage
description: Review ORM usage patterns for N+1 queries, connection management, migration safety, transaction handling, and query efficiency. Library-level atomic skill; output is a findings list.
description_zh: 审查 ORM 使用：N+1 查询、连接管理、迁移安全、事务与查询效率；库级原子技能。
tags: [code-review, library, optimization]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review orm, orm review]
input_schema:
  type: code-scope
  description: Source files or directories to review
output_schema:
  type: findings-list
  description: Zero or more findings with location, category, severity, and suggestion
---

# Skill: Review ORM Usage

## Purpose

Look at **ORM usage patterns** at the **library level** only. Do not define scope (diff vs. codebase) or perform security/architecture analysis; those are handled by the scope and cognitive skills. Emit a **findings list** in the standard format for aggregation. Focus on N+1 query detection, connection management, migration safety, transaction handling, query efficiency, and model design across ORM libraries (Prisma, Entity Framework, SQLAlchemy, Sequelize, TypeORM, Hibernate, Django ORM, ActiveRecord, and so on).

---

## Core Objective

**Primary goal**: produce an ORM usage findings list covering N+1 queries, connection management, migration safety, transaction handling, query efficiency, and model design for the given code scope.

**Success criteria** (all must be met):

1. ✅ **ORM-library scope only**: only ORM usage patterns reviewed; no scope selection, security, or architecture analysis performed
2. ✅ **All six ORM dimensions covered**: N+1, connections, migrations, transactions, query efficiency, and model design assessed where relevant
3. ✅ **Findings format compatible**: every finding includes location, category (`library-orm`), severity, title, description, and an optional suggestion
4. ✅ **File/model references**: every finding cites a specific file:line or model/entity name
5. ✅ **ORM-agnostic**: findings hold across ORM libraries; a specific library is cited only for context

**Acceptance** test: does the output contain an ORM-focused findings list, with file/model references covering every relevant library dimension, and without performing security, architecture, or scope analysis?

---

## Scope Boundaries

**This skill owns**:

- N+1 query detection (eager vs. lazy loading, include/join patterns, batch loading, dataloader patterns)
- Connection management (pool configuration, connection leaks, timeout handling, connection reuse)
- Migration safety (backward-compatible migrations, zero-downtime deploys, data vs. schema migrations, rollback strategy)
- Transaction handling (transaction scope, isolation levels, nested transactions, deadlock prevention)
- Query efficiency (unnecessary SELECT *, missing indexes implied by query patterns, raw-query fallbacks, query complexity)
- Model design (appropriate relationships, cascade behavior, soft-delete patterns, audit columns, index declarations)

**This skill does not own**:

- Scope selection — the scope is supplied by the caller
- Security analysis (SQL injection, sensitive data exposure) — use `review-security`
- Architecture analysis (module boundaries, coupling) — use `review-architecture`
- Raw SQL quality (syntax, portability, parameterization) — use `review-sql`
- General performance analysis (algorithmic complexity, I/O cost) — use `review-performance`
- Full orchestrated review — use `orchestrate-code-review`

**Handoff**: once all ORM findings are emitted, hand them to `orchestrate-code-review` for aggregation. For SQL injection risks (unsanitized raw queries), note them and point at `review-security`. For complex raw SQL quality, note it and point at `review-sql`.

---

## Use Cases

- **Orchestrated review**: used as the library step when [orchestrate-code-review](../orchestrate-code-review/SKILL.md) runs scope → language → framework → library → cognitive for a project that uses an ORM.
- **ORM-only review**: when the user wants only the ORM usage patterns in their data layer checked.
- **Pre-PR ORM checklist**: confirming N+1 queries, transaction handling, and migration safety are correct before merging.
- **Migration review**: a focused pass over migration files for backward compatibility and rollback safety.

**When to use**: when the code under review uses an ORM library and the task includes library-level quality. The scope is determined by the caller or the user.

---

## Behavior

### What this skill covers

- **Analyze**: ORM usage patterns within the **given code scope** (files or a diff supplied by the caller). Does not decide the scope; takes the code scope as input.
- **Do not**: perform scope selection, security review, or architecture review; do not check ORM rules in non-ORM files unless they are in scope.

### Review checklist (ORM library only)

1. **N+1 query detection**: identify lazy-loading patterns that trigger N+1 queries; check for eager loading (include/join), batch loading, or dataloader patterns; flag loops that issue a separate query per iteration.
2. **Connection management**: verify pool configuration (min/max, idle timeout); detect potential connection leaks (connections never returned, missing dispose/close); check timeout and retry settings; confirm connection reuse within a request-scoped context.
3. **Migration safety**: assess backward compatibility (additive-only vs. breaking changes); check zero-downtime deploy readiness (no table locks on large tables, no NOT NULL without a default); verify data migrations are kept separate from schema migrations; confirm a rollback strategy exists.
4. **Transaction handling**: assess transaction scope (too wide or too narrow); check isolation levels for correctness; detect nested-transaction misuse (savepoints vs. flat); flag potential deadlock patterns (inconsistent lock ordering, long-held locks).
5. **Query efficiency**: flag unnecessary `SELECT *` or over-fetched columns; identify query patterns that imply a missing index (unindexed WHERE/ORDER BY columns); assess whether raw-query fallbacks are appropriate; assess query complexity (deep joins, subqueries inside loops).
6. **Model design**: verify correct relationship declarations (one-to-many, many-to-many, polymorphic); check cascade behavior (accidental cascade deletes); review the soft-delete implementation; confirm the expected audit columns (createdAt, updatedAt); check index declarations on frequently queried fields.

### Tone and references

- **Professional and technical**: cite concrete locations (file:line or model/entity name). Emit findings carrying location, category, severity, title, description, suggestion.

---

## Input & Output

### Input

- **Code scope**: files or directories (or a diff) containing ORM code (models, migrations, repositories, queries). Supplied by the user or by a scope skill.

### Output

- Emit zero or more **findings** in the format defined in **Appendix: Output Contract**.
- The category for this skill is **library-orm**.

---

## Restrictions

### Hard Boundaries

- **Do not** perform scope selection, security, or architecture review. Stay on ORM library usage patterns.
- **Do not** state a conclusion without a concrete location or an actionable fix.
- **Do not** review non-ORM code against ORM-specific rules unless it is explicitly in scope.
- **Do not** duplicate the raw SQL analysis that belongs to `review-sql`; flag only ORM-generated query problems.

### Skill Boundaries

**Do not do these** (other skills handle them):

- Do not select or define the code scope — the scope is set by the caller or by `orchestrate-code-review`
- Do not perform security analysis (SQL injection, data exposure) — use `review-security`
- Do not perform architecture analysis (module boundaries, coupling) — use `review-architecture`
- Do not perform raw SQL syntax or portability review — use `review-sql`
- Do not perform general algorithmic performance analysis — use `review-performance`

**When to stop and hand off**:

- Once all ORM findings are emitted, hand them to `orchestrate-code-review` for aggregation
- When SQL injection risks turn up (for example unsanitized interpolation in a raw query), note them and point at `review-security`
- When raw SQL quality problems (syntax, portability) turn up, note them and point at `review-sql`
- When the user wants a full review (scope + language + cognitive), redirect to `orchestrate-code-review`

---

## Self-Check

### Core success criteria

- [ ] **ORM library scope only**: only ORM usage patterns reviewed; no scope selection, security, or architecture analysis performed
- [ ] **All six ORM dimensions covered**: N+1, connections, migrations, transactions, query efficiency, and model design assessed where relevant
- [ ] **Findings format compatible**: every finding includes location, category (`library-orm`), severity, title, description, and an optional suggestion
- [ ] **File/model references**: every finding cites a specific file:line or model/entity name
- [ ] **ORM-agnostic**: findings hold across ORM libraries; a specific library is cited only for context

### Process quality checks

- [ ] Were only ORM library dimensions reviewed (no scope/security/architecture)?
- [ ] Were the relevant N+1, connection, migration, transaction, query efficiency, and model design dimensions covered?
- [ ] Does every emitted finding include location, category=library-orm, severity, title, description, and an optional suggestion?
- [ ] Is each issue referenced by file:line or model/entity name?

### Acceptance test

Does the output contain an ORM-focused findings list, with file/model references covering every relevant library dimension, and without performing security, architecture, or scope analysis?

---

## Examples

### Example 1: N+1 queries in a loop

- **Input**: a controller or service that fetches a list of orders and then iterates over them accessing `order.customer` without eager loading.
- **Expected**: emit a finding for the N+1 query pattern (major); suggest eager loading via include/join (for example Prisma `include`, EF `Include`, SQLAlchemy `joinedload`, Hibernate `@EntityGraph`). category=library-orm.

### Example 2: destructive migration with no rollback

- **Input**: a migration that drops a column or renames a table, with no matching down/rollback migration and no data-preservation step.
- **Expected**: emit a finding for a destructive migration with no rollback strategy (critical); suggest the additive migration pattern (add new column → backfill → switch reads → drop old column). category=library-orm.

### Edge case: raw query fallback in an ORM context

- **Input**: a repository method that queries with raw SQL (`prisma.$queryRaw`, `DbContext.Database.ExecuteSqlRaw`, `session.execute(text(...))`) where the query could be expressed with the ORM query builder.
- **Expected**: emit a finding (suggestion) noting that raw queries bypass ORM type safety and migration tracking; where the query is expressible, suggest the ORM query builder. Where the raw query is justified (performance, an unsupported feature), accept it, but flag missing parameterization if present and point at `review-security` for the injection risk. category=library-orm.
