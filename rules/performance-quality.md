---
artifact_type: rule
name: performance-quality
version: 1.0.1
model: RULE_MODEL_V1
rule_prefix: PERF
scope: code paths whose work, latency, throughput, memory, storage or downstream load can grow with input or concurrency
recommended_scope: project
status: active
created_by: ai-cortex
lifecycle: living
created_at: 2026-09-11
---

# Rule: Performance Quality

## Scope

Applies to production request paths, batch jobs, queries, message consumers and resource-intensive libraries. It does not require premature optimization of bounded local code; it requires explicit bounds and evidence where cost can grow.

## Profiles and parameters

| Name | Kind | Provenance | Meaning |
|---|---|---|---|
| `high-volume-data` | profile | — | Input, result or retained data can exceed safe in-memory or single-query size |
| `concurrent-workload` | profile | — | Multiple requests or jobs contend for resources |
| `performance.budgets` | parameter | declared | Latency, throughput, memory, query-count or cost targets |
| `performance.load_model` | parameter | declared | Representative volume, concurrency and data distribution |

Provenance follows [rule-modeling](../specs/rule-modeling.md) §5.4: a project writes only the `declared` values.

## Rules

### PERF-001 — Work is bounded by explicit limits

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | Work that grows with input, data size, retries or concurrency **MUST** have an explicit upper bound, pagination, backpressure or streaming strategy. |
| Applies when | A loop, query, queue, collection, recursion or fan-out is controlled by non-constant input. |
| Default severity | `major` |
| Enforcement | `tool-assisted` |
| Evidence | Loop/query bounds, page size, queue capacity, recursion limit and cancellation behavior. |
| Pass condition | Worst-case work and retained data are finite and compatible with the execution context. |
| Not applicable when | The input is structurally bounded to a small constant. |
| Remediation | Add limits, pagination, streaming, admission control or backpressure. |

### PERF-002 — Repeated remote and storage work is eliminated

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | A hot path **MUST NOT** perform N+1, duplicate or avoidably serial database, filesystem or network operations. |
| Applies when | A request or job performs I/O inside iteration or repeats an equivalent read/call. |
| Default severity | `major` |
| Enforcement | `tool-assisted` |
| Evidence | Query/call trace, loop structure, ORM loading plan and request count. |
| Pass condition | Operations are batched, joined, cached with valid ownership, or proven necessary and bounded. |
| Not applicable when | The repeated count is a small fixed constant and batching would increase risk or cost. |
| Remediation | Batch, join, prefetch, parallelize safely or reuse the existing result. |

### PERF-003 — Algorithmic growth matches the load model

| Field | Value |
|---|---|
| Level | `profile:high-volume-data` |
| Requirement | Algorithmic time and space growth **MUST** remain within the declared load model and performance budget. |
| Applies when | Input cardinality can materially grow or a nested scan/sort/copy is introduced. |
| Default severity | `major` |
| Enforcement | `tool-assisted` |
| Evidence | Complexity analysis, representative benchmark and the input-size distribution from `performance.load_model`. |
| Pass condition | Measured and asymptotic costs meet the largest supported representative input. |
| Not applicable when | Input is bounded to a documented small constant. |
| Remediation | Use a more appropriate data structure or algorithm, reduce copies, index access, or constrain input. |

### PERF-004 — Large data is streamed or chunked

| Field | Value |
|---|---|
| Level | `profile:high-volume-data` |
| Requirement | Large or unbounded payloads and result sets **MUST** be streamed, paged or processed in bounded chunks rather than materialized repeatedly in memory. |
| Applies when | Data size can exceed the project's safe single-allocation or request limit. |
| Default severity | `major` |
| Enforcement | `tool-assisted` |
| Evidence | Allocation behavior, serializer/query API, chunk size and memory benchmark. |
| Pass condition | Peak retained memory stays within budget as total data grows. |
| Not applicable when | The format or protocol guarantees a small maximum payload. |
| Remediation | Introduce streaming, cursor pagination, chunked processing or spill-to-disk with cleanup. |

### PERF-005 — Concurrency is bounded and non-blocking where required

| Field | Value |
|---|---|
| Level | `profile:concurrent-workload` |
| Requirement | Concurrent work **MUST** have a bounded degree of parallelism and **MUST NOT** block an asynchronous execution resource on avoidable synchronous I/O or locks. |
| Applies when | The code creates tasks, threads, workers, goroutines or concurrent callbacks. |
| Default severity | `major` |
| Enforcement | `tool-assisted` |
| Evidence | Worker/task creation, semaphore/pool limits, blocking calls, lock scope and contention profile. |
| Pass condition | Concurrency has a configured cap, cancellation and no avoidable blocking on the hot execution resource. |
| Not applicable when | Execution is intentionally single-threaded and bounded. |
| Remediation | Add a pool or semaphore, use asynchronous I/O, shrink lock scope or serialize the critical section. |

### PERF-006 — Caches have ownership and invalidation semantics

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | A cache **MUST** declare its key, owner, freshness/invalidation rule, capacity bound and failure behavior. |
| Applies when | The change adds or changes cached data or memoization. |
| Default severity | `major` |
| Enforcement | `judgment` |
| Evidence | Cache API, key composition, TTL/invalidation events, size policy and fallback path. |
| Pass condition | Stale or cross-tenant reads are prevented, growth is bounded and cache failure preserves correctness. |
| Not applicable when | No cached state is introduced or changed. |
| Remediation | Define invalidation and capacity, include ownership dimensions in keys, and make fallback explicit. |

### PERF-007 — Performance-sensitive changes carry representative evidence

| Field | Value |
|---|---|
| Level | `project:performance.budgets` |
| Requirement | A change affecting a declared performance budget **MUST** provide a reproducible measurement under the declared load model. |
| Applies when | The changed path is covered by `performance.budgets`. |
| Default severity | `minor` |
| Enforcement | `automated` |
| Evidence | Benchmark/load-test command, environment, data volume, concurrency and before/after results. |
| Pass condition | The result meets every applicable budget without shifting unacceptable cost to another resource. |
| Not applicable when | No declared budget or affected performance-sensitive path exists. |
| Remediation | Optimize or revise the design; change a budget only through the owning requirement or decision. |

### PERF-008 — Resource ownership prevents accumulation

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | Connections, streams, buffers, subscriptions, timers and temporary files **MUST** have bounded lifetimes and deterministic release on success, failure and cancellation paths. |
| Applies when | The scope acquires or retains a finite runtime resource. |
| Default severity | `major` |
| Enforcement | `tool-assisted` |
| Evidence | Acquire/release paths, context/disposal construct, cancellation and failure tests. |
| Pass condition | Every acquired resource is released exactly once on every terminal path and retained collections are bounded. |
| Not applicable when | No resource is acquired or retained. |
| Remediation | Use the language's scoped resource construct and add failure/cancellation cleanup. |

## Severity and gate policy

Bounded-work, amplification, complexity, memory, concurrency, cache-correctness and resource-release defects are `major`: they degrade or break production under real load.

Escalate to `critical` when the unbounded work can exhaust a shared resource and take the service down, or when a cache defect can serve one tenant's data to another.

A missing reproducible measurement is `minor`. The change may be perfectly fast; what is absent is the proof. Measurement ideas with no demonstrated defect are suggestions.

## Waivers

A budget waiver must name the affected target, measured result, business impact, owner and expiry. “No benchmark environment” is an evidence limitation, not a pass and not a permanent waiver.

## References

- [Classic software engineering sources](../docs/references/software-engineering-classics.md) — source hierarchy and applicability boundaries
- [Introduction to Algorithms, Fourth Edition](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/) — rigorous time/space analysis; informs PERF-003
- [Algorithms, Fourth Edition](https://algs4.cs.princeton.edu/home/) — practical data structures and empirical comparison; informs PERF-003 and PERF-007
- [Programming Pearls, Second Edition](https://www.informit.com/store/programming-pearls-9780134498041) — cost models, estimation, testing and timing; informs PERF-001, PERF-003 and PERF-007
- [Computer Systems: A Programmer's Perspective, Third Edition](https://csapp.cs.cmu.edu/) — memory hierarchy, I/O, concurrency and performance measurement; informs PERF-003, PERF-005 and PERF-008
- [Google engineering practices: small changes](https://google.github.io/eng-practices/review/developer/small-cls.html)
- [Microsoft transient fault handling](https://learn.microsoft.com/en-us/azure/architecture/best-practices/transient-faults)
- [Rule Modeling Schema](../specs/rule-modeling.md)
