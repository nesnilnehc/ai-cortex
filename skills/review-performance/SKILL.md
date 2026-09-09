---
name: review-performance
description: "Review code for performance: complexity, database/query efficiency, I/O and network cost, memory and allocation behavior, concurrency contention, caching, and latency/throughput regressions. Cognitive-only atomic skill; output is a findings list."
description_zh: 审查性能：复杂度、数据库/查询效率、I/O 与网络成本、内存与分配、并发竞争、缓存与延迟/吞吐回归。
tags: [code-review, cognitive, optimization]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review performance, performance review]
input_schema:
  type: code-scope
  description: Source files or directories to review
output_schema:
  type: findings-list
  description: Zero or more findings with location, category, severity, and suggestion
---

# Skill: Review Performance

## Purpose

Review code for **performance** issues only. Do not define scope (diff vs codebase) or analyze security/architecture/language-framework conventions; other atomic skills handle those. Emit a **findings list** in the standard format for aggregation. Focus on algorithmic complexity, query efficiency, I/O and network cost, memory behavior, contention and concurrency bottlenecks, caching strategy, and measurable regression risk.

---

## Core Objective

**Primary goal**: produce a performance-centered findings list covering complexity hotspots, query efficiency, I/O cost, memory behavior, concurrency contention, caching, and regression risk for the given code scope.

**Success criteria** (all must hold):

1. ✅ **Performance scope only**: reviews performance dimensions only; performs no scope selection, security, architecture, or language/framework style review
2. ✅ **All eight categories assessed**: complexity, database/query efficiency, I/O and network cost, memory/allocation, concurrency/contention, caching/reuse, load-facing behavior, and observability are assessed where relevant
3. ✅ **Findings format compliant**: each finding carries location, category (`cognitive-performance`), severity, title, description, and an optional suggestion
4. ✅ **Severity assigned accurately**: production-impacting issues are marked "critical"; scalability risk is marked "major"; localized optimizations are marked "minor"/"suggestion"
5. ✅ **Actionable output**: every finding carries a concrete location reference and a specific fix or improvement suggestion, and claims no benchmark numbers unless measurement evidence is supplied

**Acceptance** test: does the output contain a performance findings list covering all relevant dimensions, with evidence-based severity ratings and actionable, location-referenced suggestions?

---

## Scope Boundaries

**This skill owns**:

- Algorithmic complexity hotspots (O(n²)+, nested loops, repeated scans)
- Database/query efficiency (N+1, missing pagination, wide selects)
- I/O and network cost (chatty calls, missing batching, blocking on the critical path)
- Memory and allocation behavior (churn, large object retention, unbounded growth)
- Concurrency and contention (lock contention, goroutine starvation, queue backpressure)
- Caching strategy (missing cache on hot paths, invalidation risk, stampede risk)
- Load-facing behavior (missing limits/guards, expensive defaults)
- Observability for performance (missing metrics/traces around hot paths)

**This skill does not own**:

- Scope selection (deciding which files/paths to analyze) — the scope is supplied by the caller
- Security review — use `review-security`
- Architecture review — use `review-architecture`
- Language/framework-specific conventions - use `review-dotnet`, `review-java`, `review-go` and so on.
- Comprehensive SQL performance analysis — use `review-sql`
- Full orchestrated review — use `orchestrate-code-review`

**Handoff point**: once all performance findings are emitted, hand them to the `orchestrate-code-review` orchestrator for aggregation, or deliver them straight to the user for a performance-centered review session.

---

## Use Cases

- **Orchestrated review**: serves as the cognitive step when [orchestrate-code-review](../orchestrate-code-review/SKILL.md) runs scope -> language -> framework -> library -> cognitive.
- **Performance-centered review**: when the user wants the performance dimensions alone checked before a merge or a release.
- **Regression prevention**: verify that a change introduces no visible latency, throughput, or memory regression.

**When to use**: when the task includes a performance review. The scope and code range are set by the caller or the user.

---

## Behavior

### What this skill covers

- **Analyze**: performance dimensions inside the **given code scope** (files or a diff supplied by the caller). Does not decide scope; takes the code scope as input.
- **Do not**: perform scope selection, security review, architecture review, or language/framework style review. Stay on performance.

### Review checklist (performance dimensions only)

1. **Complexity hotspots**: detect unnecessary O(n^2)+ behavior, repeated scans, nested loops over large collections, and avoidable recomputation.
2. **Database and query efficiency**: N+1 access patterns, missing pagination, wide selects, inefficient joins/filters, and query frequency amplification.
3. **I/O and network cost**: chatty remote calls, missing batching, blocking calls on the critical path, unbounded retries/timeouts, and poor backoff behavior.
4. **Memory and allocation**: excessive allocation/churn, large object retention, unnecessary copies, unbounded growth, and avoidable buffering.
5. **Concurrency and contention**: lock contention, serialized critical sections, thread/goroutine starvation, queue backpressure, and oversubscription risk.
6. **Caching and reuse**: missed caching opportunities on hot read paths, invalidation correctness risk, stampede risk, and low-value cache layers.
7. **Load-facing behavior**: missing limits/guards (batch size, page size, concurrency caps), expensive defaults, and no degradation strategy under load.
8. **Performance observability**: missing metrics/traces around hot paths, which blocks regression detection and capacity planning.

### Severity guidance

- **Critical**: likely to have a visible production impact (unbounded loops/growth, repeated expensive I/O in a hot path, catastrophic query patterns, for example).
- **Major**: strong regression or scalability risk under realistic traffic/data growth.
- **Minor/suggestion**: localized or lower-impact optimization opportunities.

### Tone and references

- **Professional and technical**: cite the exact location (file:line, or the query/block).
- Emit findings carrying location, category, severity, title, description, and suggestion.

---

## Input & Output

### Input

- **Code scope**: files or directories (or a diff) already selected by the user or by a scope skill. This skill does not decide scope; it only examines the code it is given for performance.

### Output

- Emit zero or more **findings** in the format defined in **Appendix: Output Contract**.
- The category for this skill is **cognitive-performance**.

---

## Restrictions

### Hard Boundaries

- **Do not** perform scope selection, security, architecture, or language/framework style review. Stay inside performance.
- **Do not** state a finding without a concrete location or an actionable suggestion.
- **Do not** claim benchmark numbers unless measurement evidence is supplied in the input.

### Skill Boundaries

**Do not do these** (other skills handle them):

- Do not select or define the code scope - it is set by the caller or by `orchestrate-code-review`
- Do not perform security, architecture, or language/framework review — use the respective atomic skills
- Do not perform comprehensive SQL performance analysis — use `review-sql`
- Do not run or execute code to measure performance - use `run-automated-tests` for test execution

**When to stop and hand off**:

- Once all performance findings are emitted, hand them to `orchestrate-code-review` for aggregation inside an orchestrated review
- When the user wants a full review (scope + language + cognitive), redirect to `orchestrate-code-review`
- When SQL performance issues dominate, suggest also running `review-sql` for deeper SQL coverage

---

## Self-Check

### Core success criteria

- [ ] **Performance scope only**: reviews performance dimensions only; performs no scope selection, security, architecture, or language/framework style review
- [ ] **All eight categories assessed**: complexity, database/query efficiency, I/O and network cost, memory/allocation, concurrency/contention, caching/reuse, load-facing behavior, and observability are assessed where relevant
- [ ] **Findings format compliant**: each finding carries location, category (`cognitive-performance`), severity, title, description, and an optional suggestion
- [ ] **Severity assigned accurately**: production-impacting issues are marked "critical"; scalability risk is marked "major"; localized optimizations are marked "minor"/"suggestion"
- [ ] **Actionable output**: every finding carries a concrete location reference and a specific fix or improvement suggestion, and claims no benchmark numbers unless measurement evidence is supplied

### Process quality checks

- [ ] Were only performance dimensions reviewed (no scope/security/architecture/style)?
- [ ] Were complexity, query efficiency, I/O, memory, concurrency, caching, and load behavior covered where relevant?
- [ ] Does every finding carry location, category = cognitive-performance, severity, title, description, and an optional suggestion?
- [ ] Is high-impact regression risk clearly separated from minor optimizations?

### Acceptance test

Does the output contain a performance findings list covering all relevant dimensions, with evidence-based severity ratings and actionable, location-referenced suggestions?

---

## Examples

### Example 1: N+1 query pattern

- **Input**: a loop that fetches the child records of each parent with one query per iteration.
- **Expected**: a major/critical finding for the N+1 behavior; the suggestion is a batched query or a join strategy. Category = cognitive-performance.

### Example 2: allocation churn on a hot path

- **Input**: a request handler that repeatedly allocates large temporary buffers and serializes the payload several times.
- **Expected**: a major finding on allocation pressure and its latency impact; the suggestion is reuse/pooling or a single-pass transformation. Category = cognitive-performance.

### Edge case: no material performance risk in a small formatting diff

- **Input**: the diff contains only comments/renames, with no behavior change.
- **Expected**: emit no findings, or a single suggestion-level note; do not invent optimization work. The category for anything emitted is still cognitive-performance.
