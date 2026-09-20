---
artifact_type: rule
name: observability-quality
version: 1.3.0
model: RULE_MODEL_V1
rule_prefix: OBS
scope: deployable services, background workloads and cross-process operations whose behavior must be diagnosed in production
recommended_scope: project
status: active
created_by: ai-cortex
lifecycle: living
created_at: 2026-09-11
---

# Rule: Observability Quality

## Scope

Applies to production operations where operators need to determine what happened, where, for whom and with what outcome. Pure in-process libraries apply only when they emit or propagate telemetry by contract.

## Profiles and parameters

| Name | Kind | Provenance | Meaning |
| --- | --- | --- | --- |
| `deployable-service` | profile | — | Independently operated request-serving process |
| `distributed-workflow` | profile | — | One operation crosses process, service or queue boundaries |
| `background-workload` | profile | — | Scheduled, queued or batch execution without an interactive caller |
| `observability.critical_operations` | parameter | declared | User journeys or jobs requiring explicit signals |
| `observability.sli_targets` | parameter | declared | Measurable success, latency, freshness or correctness indicators |
| `observability.data_policy` | parameter | declared | Allowed fields, redaction and cardinality limits |

Provenance follows [rule-modeling](../specs/rule-modeling.md) §5.4: a project writes only the `declared` values.

## Rules

### OBS-001 — Critical operations emit structured outcome events

| Field | Value |
| --- | --- |
| Level | `project:observability.critical_operations` |
| Requirement | Each critical operation **MUST** emit structured telemetry containing operation identity, outcome, duration and safe diagnostic context. |
| Applies when | The operation is listed in `observability.critical_operations`. |
| Default severity | `minor` |
| Enforcement | `tool-assisted` |
| Evidence | Structured log/event schema and representative success/failure output. |
| Pass condition | Operators can filter and aggregate outcomes and latency without parsing free-form messages. |
| Not applicable when | The operation is not declared critical and no operational contract requires telemetry. |
| Remediation | Emit a structured completion event through the shared telemetry API. |
| Tool limits | Schema validation over emitted events decides that a field is present and well typed. It cannot decide whether the operation is critical enough to owe an event, nor whether the outcome recorded is the one that matters when the operation goes wrong. |

### OBS-002 — Correlation crosses execution boundaries

| Field | Value |
| --- | --- |
| Level | `profile:distributed-workflow` |
| Requirement | Correlation or trace context **MUST** propagate across every synchronous and asynchronous process boundary. |
| Applies when | A request or job crosses two independently executing components. |
| Default severity | `major` |
| Enforcement | `tool-assisted` |
| Evidence | Header/message propagation, telemetry fields and one end-to-end trace. |
| Pass condition | One standard trace or correlation identity connects the complete representative path. |
| Not applicable when | Execution never crosses a process boundary. |
| Remediation | Propagate standard trace context in request headers and message metadata. |
| Tool limits | Inspecting one end-to-end trace decides that the correlation field survived the boundaries that trace crossed. It cannot decide whether every boundary in the system was exercised by it, so a clean trace bounds the claim to the path it took. |

### OBS-003 — User-facing behavior has measurable indicators

| Field | Value |
| --- | --- |
| Level | `project:observability.sli_targets` |
| Requirement | Each declared service-level indicator **MUST** be computed from production signals that represent user-observed success, latency, freshness or correctness. |
| Applies when | `observability.sli_targets` defines an indicator for the changed behavior. |
| Default severity | `minor` |
| Enforcement | `automated` |
| Evidence | Metric definition, labels, source events and sample query/dashboard. |
| Pass condition | The indicator can be reproduced and separates successful from failed user outcomes under its stated denominator. |
| Not applicable when | No indicator is declared for the scope. |
| Remediation | Instrument the user outcome and define a stable numerator, denominator and aggregation window. |
| Verification | `adopter`. This repository runs no service emitting user-facing indicators, so it cannot host the population this item governs. An adopting project returns the three shapes as fixtures in the format `scripts/test-rule-scenarios.py` reads, under `tests/fixtures/`, through the pull-request process in `CONTRIBUTING.md`. |

### OBS-004 — Distributed spans describe meaningful boundaries

| Field | Value |
| --- | --- |
| Level | `profile:distributed-workflow` |
| Requirement | Distributed operations **MUST** create spans at meaningful service, dependency and asynchronous-consumption boundaries with status and duration. |
| Applies when | Standard tracing is available and an operation crosses a process or dependency boundary. |
| Default severity | `minor` |
| Enforcement | `tool-assisted` |
| Evidence | Instrumentation code and representative trace topology. |
| Pass condition | The trace shows the responsible boundary, dependency latency and error status without redundant per-line spans. |
| Not applicable when | The runtime cannot support tracing and an approved equivalent correlation mechanism exists. |
| Remediation | Instrument boundary calls and consumers with standard semantic conventions. |
| Tool limits | Instrumentation inspection and trace topology decide that spans exist and nest correctly. Neither decides whether a span boundary is meaningful — a span per function is well formed and tells an operator nothing. A reviewer judges the boundaries. |

### OBS-005 — Telemetry is safe and cardinality-bounded

| Field | Value |
| --- | --- |
| Level | `baseline` |
| Requirement | Telemetry **MUST NOT** contain secrets or disallowed protected data, and metric/span attributes **MUST** have bounded cardinality. |
| Applies when | The change emits logs, metrics, traces or events. |
| Default severity | `critical` |
| Enforcement | `tool-assisted` |
| Evidence | Telemetry arguments, the redaction policy from `observability.data_policy`, attribute keys and representative values. |
| Pass condition | Sensitive values are absent/redacted and unbounded identifiers are not used as metric dimensions. |
| Not applicable when | No telemetry is emitted or changed. |
| Remediation | Redact or remove protected fields and move high-cardinality context to logs or exemplars. |
| Tool limits | Attribute inspection decides an attribute's distinct-value count over observed traffic and matches keys against the redaction policy. It cannot decide whether an unredacted value is sensitive in this system, nor whether the cardinality observed bounds the cardinality to come. |

### OBS-006 — Error signals are actionable and non-duplicative

| Field | Value |
| --- | --- |
| Level | `profile:deployable-service` |
| Requirement | A terminal failure **MUST** be recorded once at the owning boundary with stable error identity, severity and recovery context; intermediate layers **MUST NOT** duplicate the same error as separate incidents. |
| Applies when | A failure crosses layers or service boundaries. |
| Default severity | `minor` |
| Enforcement | `judgment` |
| Evidence | Catch/rethrow paths, log statements, error mapping and sample telemetry. |
| Pass condition | One owning event identifies the failure and correlation context, while lower layers preserve context without alert duplication. |
| Not applicable when | The failure is fully handled locally and has no operational consequence. |
| Remediation | Assign log ownership to the boundary, preserve error cause and remove duplicate terminal logs. |
| Worked pass | The payment boundary records one terminal `payment.failed` event carrying the stable error code, the correlation id and what was attempted. The retry layer beneath logs at debug and raises no incident of its own. |
| Worked failure | The client, the retry wrapper and the handler each raise an error event for the same failed payment. One outage pages three times and the on-call reads three stories about one fact. |

### OBS-007 — Background work exposes progress and terminal backlog

| Field | Value |
| --- | --- |
| Level | `profile:background-workload` |
| Requirement | Background processing **MUST** expose started, succeeded, retried, failed, age/backlog and dead-letter or terminal-loss signals. |
| Applies when | A scheduled, batch or queued workload can outlive one request. |
| Default severity | `major` |
| Enforcement | `tool-assisted` |
| Evidence | Job metrics/events, queue age/depth, retry counters and terminal failure path. |
| Pass condition | Operators can distinguish idle, healthy progress, retrying, stuck backlog and terminal failure. |
| Not applicable when | No background work exists. |
| Remediation | Add lifecycle counters/events and expose queue age, depth and terminal disposition. |
| Tool limits | Metric inspection decides that the counters, queue age and terminal-failure path are emitted. It cannot decide whether the backlog they expose is the one an operator must act on, nor whether the signal arrives early enough to act. |

### OBS-008 — New behavior updates its operational evidence

| Field | Value |
| --- | --- |
| Level | `baseline` |
| Requirement | A change that adds a production behavior or failure mode **MUST** add or update the telemetry needed to verify and diagnose that behavior. |
| Applies when | The change creates a new externally meaningful outcome, dependency or failure path. |
| Default severity | `minor` |
| Enforcement | `judgment` |
| Evidence | Behavior diff, failure paths and changed telemetry/tests/dashboards. |
| Pass condition | Every new production outcome and failure can be distinguished with existing or changed signals. |
| Not applicable when | The change has no production behavior or failure-mode effect. |
| Remediation | Add the smallest structured signal and verification query that closes the diagnostic gap. |
| Worked pass | The change adds a new rejection path for expired cards, and adds `payment.failed` a `reason` attribute whose values now distinguish it from the existing decline. |
| Worked failure | The rejection path ships with no signal change, so an expired card and a bank decline arrive as the same event. The first question in the incident is one nobody can answer from telemetry. |

## Severity and gate policy

Secret or protected-data exposure through telemetry is `critical` — that is a security incident, not a diagnostics gap.

Lost correlation across process boundaries and an invisible background backlog are `major`: an operator cannot diagnose, or even detect, a live incident.

Every remaining observability gap is `minor` — unstructured outcomes, an unreproducible indicator, coarse spans, duplicated error reporting, telemetry not updated for new behavior. These delay discovery rather than cause failure. Escalate to `major` when the blind spot covers a declared critical path. Signal ideas with no uncovered operation are suggestions.

## Waivers

OBS-005 secret exposure cannot be waived. A temporary tracing limitation must retain a verified correlation alternative and an expiry tied to runtime support.

## References

- [OpenTelemetry observability primer](https://opentelemetry.io/docs/concepts/observability-primer/)
- [OpenTelemetry log correlation](https://opentelemetry.io/docs/specs/otel/logs/)
- [Google SRE: alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)
- [Rule Modeling Schema](../specs/rule-modeling.md)
