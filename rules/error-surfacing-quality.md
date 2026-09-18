---
artifact_type: rule
name: error-surfacing-quality
version: 1.0.0
model: RULE_MODEL_V1
rule_prefix: ERR
scope: production code that accepts input it does not control, or reports a failure to a person or an automated consumer
recommended_scope: project
status: active
created_by: ai-cortex
lifecycle: living
created_at: 2026-09-18
---

# Rule: Error Surfacing Quality

## Scope

Applies to code that reads input from outside itself — a person, a file, a network peer, configuration, another system — and to the paths by which it reports a failure. Generated code is excluded when its source schema is reviewed and regeneration is deterministic.

Three neighbouring concerns are owned elsewhere, and a finding belongs to them rather than here:

- **How the system behaves once a failure happens** — timeouts, retries, idempotency, partial failure, isolation — belongs to [reliability-quality](./reliability-quality.md).
- **What telemetry records about a failure** — the event, its correlation, who owns the alert — belongs to [observability-quality](./observability-quality.md). This Rule governs the message handed back to whoever asked; that Rule governs the event written for whoever operates.
- **What a security-relevant failure may disclose** belongs to [security-quality](./security-quality.md).

## Profiles and parameters

| Name | Kind | Provenance | Meaning |
| --- | --- | --- | --- |
| `human-facing` | profile | — | A failure reaches a person directly, through a CLI, an interface, a compiler or a form |
| `machine-consumer` | profile | — | A failure is consumed by another program, service or agent rather than read by a person |
| `error.detection_layers` | parameter | declared | The layers this project can detect a defect at, earliest first — types, lint, unit test, integration test, CI, startup, runtime |
| `error.false_positive_threshold` | parameter | declared | The share of a check's findings that may be legitimate use before the check must be narrowed |

Provenance follows [rule-modeling](../specs/rule-modeling.md) §5.4: a project writes only the `declared` values.

## Rules

### ERR-001 — Untrusted input is decided at the boundary it enters

| Field | Value |
| --- | --- |
| Level | `baseline` |
| Requirement | Input the code does not control **MUST** be checked at the boundary where it enters and carried onward in a form that cannot be misread; it **MUST NOT** be accepted tolerantly and reinterpreted by a later layer. |
| Applies when | A scope reads from a person, a file, a network peer, configuration or another system. |
| Default severity | `major` |
| Enforcement | `judgment` |
| Evidence | Each entry point, the shape or type it hands downstream, and every later site that re-checks a property the boundary already decided. |
| Pass condition | Every entry point rejects input it cannot represent, and no later layer repeats a check the boundary already made. |
| Not applicable when | The input originates inside the same deployable and already carries a checked type. |
| Remediation | Move the check to the boundary and return a value that carries the result, so downstream code cannot forget it. |

### ERR-002 — A broken invariant stops the operation

| Field | Value |
| --- | --- |
| Level | `baseline` |
| Requirement | When code detects that an invariant it depends on is broken, it **MUST** stop that operation and report; it **MUST NOT** continue with a value it has already determined to be wrong. |
| Applies when | A scope contains a check whose failure path continues execution. |
| Default severity | `major` |
| Enforcement | `judgment` |
| Evidence | Guards and assertions, and the paths where a failed check falls through to a default, an empty value, or a logged warning that execution ignores. |
| Pass condition | No detected invariant violation flows into subsequent work. |
| Not applicable when | The fallback is part of the declared contract and the caller can observe that it was taken. |
| Remediation | Fail the operation where the violation is detected, rather than at the point the wrong value finally causes damage. |

### ERR-003 — Detection sits at the earliest layer that can decide it

| Field | Value |
| --- | --- |
| Level | `project:error.detection_layers` |
| Requirement | A defect class the project can decide at an earlier declared layer **MUST NOT** be left for a later one. |
| Applies when | `error.detection_layers` is declared and the change introduces or moves a check. |
| Default severity | `minor` |
| Enforcement | `judgment` |
| Evidence | The declared layer list, the layer each check runs at, and what the check needs in order to decide. |
| Pass condition | Each check runs at the earliest declared layer that has the information to decide it, or the reason it cannot is recorded. |
| Not applicable when | The property depends on runtime state that no earlier layer can observe. |
| Remediation | Move the check left, or record why the information it needs is unavailable until later. |

### ERR-004 — A failure a person must act on says what to do next

| Field | Value |
| --- | --- |
| Level | `profile:human-facing` |
| Requirement | A failure surfaced to a person **MUST** state what failed, where, and the next action available to them; a code, a stack trace or an internal identifier **MUST NOT** stand in for any of the three. |
| Applies when | The `human-facing` profile is active and the change adds or alters a failure path a person sees. |
| Default severity | `minor` |
| Enforcement | `judgment` |
| Evidence | The message text at each human-facing failure path, and the action available at that point. |
| Pass condition | Each message carries all three. An identifier may accompany them and does not replace them. |
| Not applicable when | The only consumer of that path is a program, which ERR-005 governs. |
| Remediation | Add the missing element. Where no action exists, say what the person can do instead — retry, report, or wait. |

### ERR-005 — A failure a program consumes carries a stable identity

| Field | Value |
| --- | --- |
| Level | `profile:machine-consumer` |
| Requirement | A failure returned to an automated consumer **MUST** carry an identifier that survives rewording and releases, so the consumer is not made to match on prose. |
| Applies when | The `machine-consumer` profile is active and a failure crosses an interface another program reads. |
| Default severity | `minor` |
| Enforcement | `judgment` |
| Evidence | The failure payload or exit contract at each such interface, and whether a consumer could branch on it without reading the message text. |
| Pass condition | Every such failure carries an identifier that is stable independently of its message. |
| Not applicable when | The only consumer is a person, which ERR-004 governs. |
| Remediation | Add a stable identifier alongside the message, rather than freezing the message so consumers can keep matching it. |

### ERR-006 — A check whose findings are mostly legitimate use is narrowed

| Field | Value |
| --- | --- |
| Level | `project:error.false_positive_threshold` |
| Requirement | A check whose findings are predominantly legitimate use **MUST** be narrowed, retargeted or withdrawn; it **MUST NOT** be left for readers to filter. |
| Applies when | `error.false_positive_threshold` is declared and a check is added, or an existing one is measured. |
| Default severity | `minor` |
| Enforcement | `tool-assisted` |
| Evidence | The check's findings over the project's own population, and the share of them that a reviewer confirms as legitimate use. The count comes from the tool class that runs the check and can enumerate its own output — a linter, a static analyzer, a compiler diagnostic or a repository checker. That class decides how many findings there are and where; it cannot decide whether a finding is legitimate use, which only a reviewer sampling the findings can classify. |
| Pass condition | The share is measured, and any check above the declared threshold carries a recorded decision to narrow, retarget or withdraw it. An unmeasured check does not pass by default. |
| Not applicable when | The check has produced no findings over the population, so there is no share to measure. |
| Remediation | Narrow the applicability, sharpen the condition, or withdraw the check. Absorbing the noise is not a remedy: a report that is mostly legitimate teaches its readers to skim. |

## Severity and gate policy

Accepting input without deciding it, and continuing past a known-broken invariant, are `major`: both produce wrong behaviour now, at a distance from the code that caused it.

Every remaining item is `minor` — a check that could have run earlier, a message missing its next action, a failure a program must match on by prose, a check that cries wolf. These raise the cost of the next failure rather than causing this one. Escalate to `major` when the path is on a declared critical path, and to `critical` only where the concern is owned elsewhere: a tolerated malformed input that crosses a trust boundary is a [security](./security-quality.md) finding, not an error-surfacing one.

Grade by what happens if the finding is not fixed. A message that reads awkwardly but carries all three elements is not a defect.

## Waivers

Waivers follow [rule-modeling](../specs/rule-modeling.md). An ERR-002 waiver must name the declared fallback and the way a caller observes that it was taken; "the value is usually fine" is not a compensating control. An ERR-006 waiver must carry the measured share it is waiving, so the next reviewer inherits a number rather than an impression.

## References

- [Classic software engineering sources](../docs/references/software-engineering-classics.md) — source hierarchy and applicability boundaries
- [RFC 9413, *Maintaining Robust Protocols*](https://www.rfc-editor.org/rfc/rfc9413.html) — tolerating unexpected input causes protocol decay and is no longer best practice in all scenarios; informs ERR-001
- Jim Shore, [*Fail Fast*](https://martinfowler.com/ieeeSoftware/failFast.pdf), IEEE Software 21(5), pages 21–25, September 2004 — fail immediately and visibly, with assertions as the mechanism; informs ERR-002
- Alexis King, [*Parse, don't validate*](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/), November 2019 — decide at the boundary and return a value that preserves what was decided; informs ERR-001 and ERR-003
- Jakob Nielsen, [10 Usability Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/), heuristic 9 — plain language, precise problem, constructive solution; informs ERR-004
- George Candea and Armando Fox, [*Crash-Only Software*](https://www.usenix.org/legacy/events/hotos03/tech/full_papers/candea/candea_html/index.html), HotOS-IX, May 2003 — one way to stop and one way to recover; informs ERR-002's boundary against reliability-quality
- Barry Boehm and Victor Basili, *Software Defect Reduction Top 10 List*, IEEE Computer, January 2001 — post-delivery repair costs roughly 100 times a requirements-stage fix on large projects and about 5 times on small non-critical ones; informs ERR-003. The unattributed "100x" chart in wide circulation has no traceable data behind it and must not be cited as the basis for a finding
- [Rule Modeling Schema](../specs/rule-modeling.md)
- [Observability Quality](./observability-quality.md) — the boundary between a message returned and an event recorded
