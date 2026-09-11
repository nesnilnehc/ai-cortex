---
artifact_type: rule
name: reliability-quality
version: 1.0.1
model: RULE_MODEL_V1
rule_prefix: REL
scope: deployable services, durable workflows and code that communicates with fallible external resources
recommended_scope: project
status: active
created_by: ai-cortex
lifecycle: living
created_at: 2026-09-11
---

# Rule: Reliability Quality

## Scope

Applies where dependency failure, duplication, concurrency, partial completion or process restart can affect user outcomes or durable state. Pure deterministic libraries with no external resources normally have only the baseline data-consistency and failure-test items applicable.

## Profiles and parameters

| Name | Kind | Provenance | Meaning |
|---|---|---|---|
| `remote-dependency` | profile | — | Code calls a network, process, database or cloud dependency |
| `durable-workflow` | profile | — | Work spans transactions, messages, retries or process restarts |
| `background-workload` | profile | — | Scheduled, queued or batch processing |
| `critical-service` | profile | — | Business impact requires explicit reliability targets and recovery |
| `reliability.slo` | parameter | declared | Service-level objectives and error-budget policy |
| `reliability.recovery` | parameter | declared | RTO, RPO and recovery ownership |

Provenance follows [rule-modeling](../specs/rule-modeling.md) §5.4: a project writes only the `declared` values.

## Rules

### REL-001 — Every remote attempt has a timeout and cancellation path

| Field | Value |
|---|---|
| Level | `profile:remote-dependency` |
| Requirement | Every outbound dependency attempt **MUST** have a finite timeout compatible with the end-to-end objective and a cancellation or abandonment path. |
| Applies when | Code waits for a remote service, database, process or broker. |
| Default severity | `major` |
| Enforcement | `tool-assisted` |
| Evidence | Client configuration, call context and end-to-end deadline budget. |
| Pass condition | No attempt can wait indefinitely and remaining deadline is propagated or enforced. |
| Not applicable when | The operation is a non-waiting fire-and-forget handoff with separately verified durability. |
| Remediation | Configure per-attempt timeout and propagate cancellation/deadline. |

### REL-002 — Retries are selective, bounded and budgeted

| Field | Value |
|---|---|
| Level | `profile:remote-dependency` |
| Requirement | Retries **MUST** target transient failures only, use a finite attempt/time budget and backoff with jitter, and **MUST NOT** multiply across uncoordinated layers. |
| Applies when | A client, framework, queue or caller retries an operation. |
| Default severity | `major` |
| Enforcement | `tool-assisted` |
| Evidence | Retry predicate, attempt/time limits, backoff policy, SDK defaults and call-chain ownership. |
| Pass condition | Permanent failures fail fast, aggregate retry load is bounded and one layer owns retry policy. |
| Not applicable when | The operation is never retried. |
| Remediation | Centralize retry ownership, classify errors, cap attempts/time and add exponential backoff with jitter. |

### REL-003 — Repeated operations preserve correctness

| Field | Value |
|---|---|
| Level | `profile:durable-workflow` |
| Requirement | Any operation that can be retried, redelivered or resumed **MUST** be idempotent or protected by deduplication and durable outcome recording. |
| Applies when | Delivery or response loss can cause the same logical operation to execute more than once. |
| Default severity | `critical` |
| Enforcement | `tool-assisted` |
| Evidence | Idempotency key, uniqueness constraint, inbox/outbox or durable state-transition record and duplicate tests. |
| Pass condition | Repeating the same logical operation cannot duplicate side effects or corrupt state. |
| Not applicable when | At-most-once execution is formally guaranteed and evidenced end to end. |
| Remediation | Add an idempotency key and durable uniqueness/outcome record at the side-effect owner. |

### REL-004 — Partial failure has an explicit consistency outcome

| Field | Value |
|---|---|
| Level | `profile:durable-workflow` |
| Requirement | A multi-step durable operation **MUST** define the committed state after each partial failure and a recovery, compensation or reconciliation path. |
| Applies when | One logical operation spans more than one transaction or external side effect. |
| Default severity | `critical` |
| Enforcement | `judgment` |
| Evidence | State machine, transaction boundaries, outbox/compensation/reconciliation logic, the paths named in `reliability.recovery` and failure tests. |
| Pass condition | Every interruption point leads to a valid state that can converge without lost or duplicated effects. |
| Not applicable when | The operation is atomic within one proven transaction. |
| Remediation | Make state transitions durable and add compensation or reconciliation for non-atomic effects. |

### REL-005 — Dependency failure is isolated

| Field | Value |
|---|---|
| Level | `profile:critical-service` |
| Requirement | Failure or saturation of one dependency **MUST NOT** exhaust unrelated service capacity; isolation, admission control or a bounded fallback must contain the blast radius. |
| Applies when | A critical service shares threads, connections, queues or resource pools across dependency paths. |
| Default severity | `major` |
| Enforcement | `judgment` |
| Evidence | Pool/bulkhead boundaries, circuit or admission policy, fallback semantics and load/failure test. |
| Pass condition | A representative dependency outage leaves unrelated critical operations within their declared service level or fails them predictably. |
| Not applicable when | The service has one indivisible dependency and no unrelated capacity to protect. |
| Remediation | Add bounded pools/queues, circuit breaking or fail-fast admission at the dependency boundary. |

### REL-006 — Poison and terminal background work is retained

| Field | Value |
|---|---|
| Level | `profile:background-workload` |
| Requirement | Background work that exhausts retries **MUST** enter a durable terminal state or dead-letter path with enough context for replay or resolution. |
| Applies when | A job or message can fail permanently. |
| Default severity | `major` |
| Enforcement | `tool-assisted` |
| Evidence | Max delivery count, terminal state/dead-letter configuration, payload identity and replay procedure. |
| Pass condition | Permanent failures do not loop forever or disappear, and operators can locate and safely resolve them. |
| Not applicable when | The workload has no durable input and loss is an explicitly accepted outcome. |
| Remediation | Add bounded retries and durable terminal disposition with replay identity. |

### REL-007 — Failure modes are verified at their real boundary

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | Every changed timeout, retry, transaction, concurrency or recovery behavior **MUST** have a deterministic test at the narrowest boundary that can reproduce its failure mode. |
| Applies when | Reliability behavior or a fallible dependency path changes. |
| Default severity | `minor` |
| Enforcement | `tool-assisted` |
| Evidence | Failure-injection, integration or state-transition tests and assertions on terminal state. |
| Pass condition | Tests reproduce timeout, duplicate, partial failure or restart as applicable and verify the intended outcome. |
| Not applicable when | No reliability behavior or fallible dependency path changes. |
| Remediation | Add deterministic fault injection or integration tests at the owning boundary. |

### REL-008 — Reliability targets govern release risk

| Field | Value |
|---|---|
| Level | `project:reliability.slo` |
| Requirement | A critical service **MUST** define measurable objectives and an error-budget or equivalent release policy, and releases **MUST** respect its current state. |
| Applies when | `reliability.slo` is declared. |
| Default severity | `minor` |
| Enforcement | `automated` |
| Evidence | SLI/SLO definition, current budget calculation and release-gate result. |
| Pass condition | The objective is measurable from user-facing signals and the release decision follows the declared policy. |
| Not applicable when | The project is not an operated service or has no declared SLO. |
| Remediation | Define the user-facing objective and connect its budget state to the release decision. |

## Severity and gate policy

Duplicate irreversible effects and corrupt partial state are `critical`: data ends up wrong and cannot be trusted afterwards.

A missing timeout, an unbounded or uncoordinated retry, absent dependency isolation and a lost dead letter are `major` — production fails in a way that spreads, stalls or silently drops work.

A missing failure test and an undeclared release objective are `minor`. The runtime behavior may be entirely correct; what is missing is the proof and the policy around it. Escalate to `major` when the untested failure mode is one the change itself introduced.

## Waivers

REL-003 and REL-004 cannot be waived where duplicate financial, authorization or destructive side effects remain reachable. Reliability-target waivers must be approved by the service owner and identify the temporary release-risk decision.

## References

- [Classic software engineering sources](../docs/references/software-engineering-classics.md) — source hierarchy and applicability boundaries
- [Advanced Programming in the UNIX Environment, Third Edition](https://www.informit.com/store/advanced-programming-in-the-unix-environment-9780321637734) — process, signal, I/O and thread behavior for relevant UNIX/POSIX profiles; informs REL-001, REL-005 and REL-007
- [TCP/IP Illustrated, Volume 1, Second Edition](https://www.informit.com/store/tcp-ip-illustrated-volume-1-the-protocols-9780132808217) — observable timeout, retransmission and congestion behavior; informs REL-001, REL-002 and REL-005
- [Continuous Delivery](https://www.informit.com/store/continuous-delivery-reliable-software-releases-through-9780321601919) — automated verification and low-risk release pipelines; informs REL-007 and REL-008
- [Google SRE: service-level objectives](https://sre.google/sre-book/service-level-objectives/)
- [Google SRE: example error-budget policy](https://sre.google/workbook/error-budget-policy/)
- [Microsoft transient fault handling](https://learn.microsoft.com/en-us/azure/architecture/best-practices/transient-faults)
- [Rule Modeling Schema](../specs/rule-modeling.md)
