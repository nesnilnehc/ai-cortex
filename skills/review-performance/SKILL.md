---
name: review-performance
description: "Review code for performance: complexity, database/query efficiency, I/O and network cost, memory and allocation behavior, concurrency contention, caching, and latency/throughput regressions. Cognitive-only atomic skill; output is a findings list."
tags: [code-review, optimization]
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

Review code for **performance** concerns only. Do not define scope (diff vs codebase) or perform security/architecture/language-framework convention analysis; those are handled by other atomic skills. Emit a **findings list** in the standard format for aggregation. Focus on algorithmic complexity, query efficiency, I/O and network cost, memory behavior, contention and concurrency bottlenecks, caching strategy, and measurable regression risk.

---

## Core Objective

**Primary Goal**: Produce a performance-focused findings list covering complexity hotspots, query efficiency, I/O cost, memory behavior, concurrency contention, caching, and regression risk for the given code scope.

**Success Criteria** (ALL must be met):

1. ✅ **Performance-only scope**: Only performance dimensions are reviewed; no scope selection, security, architecture, or language/framework style review performed
2. ✅ **All eight categories assessed**: Complexity, database/query efficiency, I/O/network cost, memory/allocations, concurrency/contention, caching/reuse, load-facing behavior, and observability are evaluated where relevant
3. ✅ **Findings format compliant**: Each finding includes Location, Category (`cognitive-performance`), Severity, Title, Description, and optional Suggestion
4. ✅ **Severity accurately assigned**: Production-impacting issues marked `critical`; scalability risks marked `major`; localized optimizations marked `minor`/`suggestion`
5. ✅ **Actionable output**: Each finding has a specific location reference and a concrete fix or improvement suggestion, without claiming benchmark numbers unless measured evidence is provided

**Acceptance Test**: Does the output contain a performance findings list covering all relevant dimensions with evidence-based severity ratings and actionable, location-referenced suggestions?

---

## Scope Boundaries

**This skill handles**:

- Algorithmic complexity hotspots (O(n²)+, nested loops, repeated scans)
- Database/query efficiency (N+1, missing pagination, broad selects)
- I/O and network cost (chatty calls, missing batching, blocking on critical paths)
- Memory and allocation behavior (churn, large object retention, unbounded growth)
- Concurrency and contention (lock contention, goroutine starvation, queue backpressure)
- Caching strategy (missing caches on hot paths, invalidation risks, stampede risk)
- Load-facing behavior (missing limits/guards, expensive defaults)
- Observability for performance (missing metrics/tracing around hot paths)

**This skill does NOT handle**:

- Scope selection (deciding which files/paths to analyze) — scope is provided by the caller
- Security review — use `review-security`
- Architecture review — use `review-architecture`
- Language/framework-specific conventions — use `review-dotnet`, `review-java`, `review-go`, etc.
- Comprehensive SQL performance analysis — use `review-sql`
- Full orchestrated review — use `review-code`

**Handoff point**: When all performance findings are emitted, hand off to `review-code` orchestrator for aggregation, or deliver directly to the user for performance-focused review sessions.

---

## Use Cases

- **Orchestrated review**: Used as a cognitive step when [review-code](../review-code/SKILL.md) runs scope -> language -> framework -> library -> cognitive.
- **Performance-focused review**: When the user wants only performance dimensions checked before merge or release.
- **Regression prevention**: Validate that changes do not introduce obvious latency, throughput, or memory regressions.

**When to use**: When the task includes performance review. Scope and code range are determined by the caller or user.

---

## Behavior

### Scope of this skill

- **Analyze**: Performance dimensions in the **given code scope** (files or diff provided by the caller). Do not decide scope; accept the code range as input.
- **Do not**: Perform scope selection, security review, architecture review, or language/framework style review. Focus only on performance.

### Review checklist (performance dimension only)

1. **Complexity hotspots**: Detect unnecessary O(n^2)+ behavior, repeated scans, nested loops over large collections, and avoidable recomputation.
2. **Database and query efficiency**: N+1 access patterns, missing pagination, broad selects, inefficient joins/filters, and query frequency amplification.
3. **I/O and network cost**: Chatty remote calls, missing batching, blocking calls on critical paths, unbounded retries/timeouts, and poor backoff behavior.
4. **Memory and allocations**: Excessive allocations/churn, large object retention, unnecessary copies, unbounded growth, and avoidable buffering.
5. **Concurrency and contention**: Lock contention, serialized critical sections, thread/goroutine starvation, queue backpressure, and oversubscription risks.
6. **Caching and reuse**: Missing cache opportunities on hot read paths, invalidation correctness risks, stampede risk, and low-value cache layers.
7. **Load-facing behavior**: Missing limits/guards (batch size, page size, concurrency caps), expensive defaults, and absent degradation strategy under load.
8. **Observability for performance**: Missing metrics/tracing around hot paths that prevents regression detection and capacity planning.

### Severity guidance

- **critical**: Clear production impact likely (e.g. unbounded loop/growth, repeated expensive I/O in hot path, catastrophic query pattern).
- **major**: Strong regression or scalability risk with realistic traffic/data growth.
- **minor/suggestion**: Localized or lower-impact optimization opportunities.

### Tone and references

- **Professional and technical**: Reference specific locations (file:line or query/block).
- Emit findings with Location, Category, Severity, Title, Description, Suggestion.

---

## Input & Output

### Input

- **Code scope**: Files or directories (or diff) already selected by the user or scope skill. This skill does not decide scope; it reviews the provided code for performance only.

### Output

- Emit zero or more **findings** in the format defined in **Appendix: Output contract**.
- Category for this skill is **cognitive-performance**.

---

## Restrictions

### Hard Boundaries

- **Do not** perform scope selection, security, architecture, or language/framework style review. Stay within performance dimensions.
- **Do not** give conclusions without specific locations or actionable suggestions.
- **Do not** claim benchmark numbers unless measured evidence is provided in the input.

### Skill Boundaries

**Do NOT do these** (other skills handle them):

- Do NOT select or define the code scope — scope is determined by the caller or `review-code`
- Do NOT perform security, architecture, or language/framework review — use respective atomic skills
- Do NOT perform comprehensive SQL performance analysis — use `review-sql`
- Do NOT run or execute code to measure performance — use `run-automated-tests` for test execution

**When to stop and hand off**:

- When all performance findings are emitted, hand off to `review-code` for aggregation in an orchestrated review
- When the user needs a full review (scope + language + cognitive), redirect to `review-code`
- When SQL performance issues dominate, suggest also running `review-sql` for deeper SQL coverage

---

## Self-Check

### Core Success Criteria

- [ ] **Performance-only scope**: Only performance dimensions are reviewed; no scope selection, security, architecture, or language/framework style review performed
- [ ] **All eight categories assessed**: Complexity, database/query efficiency, I/O/network cost, memory/allocations, concurrency/contention, caching/reuse, load-facing behavior, and observability are evaluated where relevant
- [ ] **Findings format compliant**: Each finding includes Location, Category (`cognitive-performance`), Severity, Title, Description, and optional Suggestion
- [ ] **Severity accurately assigned**: Production-impacting issues marked `critical`; scalability risks marked `major`; localized optimizations marked `minor`/`suggestion`
- [ ] **Actionable output**: Each finding has a specific location reference and a concrete fix or improvement suggestion, without claiming benchmark numbers unless measured evidence is provided

### Process Quality Checks

- [ ] Was only the performance dimension reviewed (no scope/security/architecture/style)?
- [ ] Are complexity, query efficiency, I/O, memory, concurrency, caching, and load behavior covered where relevant?
- [ ] Is each finding emitted with Location, Category=cognitive-performance, Severity, Title, Description, and optional Suggestion?
- [ ] Are high-impact regression risks clearly distinguished from minor optimizations?

### Acceptance Test

Does the output contain a performance findings list covering all relevant dimensions with evidence-based severity ratings and actionable, location-referenced suggestions?

---

## Examples

### Example 1: N+1 query pattern

- **Input**: Loop fetches child records per parent with one query per iteration.
- **Expected**: Emit a major/critical finding for N+1 behavior; suggest batch query or join strategy. Category = cognitive-performance.

### Example 2: Hot-path allocation churn

- **Input**: Request handler repeatedly allocates large temporary buffers and serializes payload multiple times.
- **Expected**: Emit a major finding for allocation pressure and latency impact; suggest reuse/pooling or single-pass transform. Category = cognitive-performance.

### Edge case: No clear performance risk in small formatting diff

- **Input**: Diff includes comments/renaming only, no behavioral changes.
- **Expected**: Emit no findings or one suggestion-level note; do not invent optimization work. Category remains cognitive-performance for any emitted finding.

---

## Appendix: Output contract

Each finding MUST follow the standard findings format:

| Element | Requirement |
| :--- | :--- |
| **Location** | `path/to/file.ext` (optional line or range, or query/block identifier). |
| **Category** | `cognitive-performance`. |
| **Severity** | `critical` \| `major` \| `minor` \| `suggestion`. |
| **Title** | Short one-line summary. |
| **Description** | 1-3 sentences. |
| **Suggestion** | Concrete fix or improvement (optional). |

Example:

```markdown
- **Location**: `service/orders/handler.go:118`
- **Category**: cognitive-performance
- **Severity**: major
- **Title**: Per-item remote call inside request loop
- **Description**: The handler performs one downstream call per item, creating linear remote round-trips and latency growth.
- **Suggestion**: Batch requests or prefetch related data once per request; add timeout and bulk size guards.
```
