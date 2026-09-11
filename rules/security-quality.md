---
artifact_type: rule
name: security-quality
version: 1.0.0
model: RULE_MODEL_V1
rule_prefix: SEC
scope: production code, configuration and dependency changes that cross a trust boundary or handle protected data
recommended_scope: project
status: active
created_by: ai-cortex
lifecycle: living
created_at: 2026-09-11
---

# Rule: Security Quality

## Scope

Applies to code and configuration that accepts input, performs privileged operations, handles credentials or protected data, invokes interpreters, or changes dependencies. Test-only fixtures are excluded only when they cannot enter production artifacts or logs.

## Profiles and parameters

| Name | Kind | Provenance | Meaning |
|---|---|---|---|
| `public-entrypoint` | profile | — | Untrusted callers can reach an API, command, file importer or message consumer |
| `authenticated-system` | profile | — | Identity or authorization controls access to operations or objects |
| `sensitive-data` | profile | — | The workload handles secrets, credentials, personal, financial or regulated data |
| `software-supply-chain` | profile | — | The change adds or updates executable dependencies or build inputs |
| `security.approved_crypto` | parameter | derived | Approved algorithms and libraries |
| `security.protected_data` | parameter | declared | Data classes and handling requirements |

Provenance follows [rule-modeling](../specs/rule-modeling.md) §5.4: a project writes only the `declared` values.

## Rules

### SEC-001 — Untrusted input is constrained before a dangerous sink

| Field | Value |
|---|---|
| Level | `profile:public-entrypoint` |
| Requirement | Untrusted input **MUST** be validated for the intended domain and parameterized or contextually encoded before reaching a query, command, template, path, parser or interpreter sink. |
| Applies when | Caller-controlled data can influence a dangerous sink. |
| Default severity | `critical` |
| Enforcement | `tool-assisted` |
| Evidence | Source-to-sink data flow, validators, parameter binding and encoding at the final context. |
| Pass condition | Every reachable source-to-sink path has domain validation and sink-appropriate neutralization. |
| Not applicable when | The value is constant or proven unreachable from untrusted input. |
| Remediation | Use typed validation and the sink's parameterized API; remove string-built commands or queries. |

### SEC-002 — Authorization is enforced at the protected operation

| Field | Value |
|---|---|
| Level | `profile:authenticated-system` |
| Requirement | Every protected operation and object access **MUST** enforce authorization server-side at or below the operation boundary, using deny-by-default behavior. |
| Applies when | An operation or object has role, tenant, ownership or policy restrictions. |
| Default severity | `critical` |
| Enforcement | `tool-assisted` |
| Evidence | Route/handler policy, service guard, object-level filter and negative authorization tests. |
| Pass condition | Unauthorized identities and cross-tenant or cross-owner identifiers cannot reach the protected action or data. |
| Not applicable when | The operation and data are intentionally public and documented as such. |
| Remediation | Add centralized policy enforcement and object-level checks; add negative tests. |

### SEC-003 — Secrets never enter source, artifacts or telemetry

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | Credentials, private keys, tokens and production secrets **MUST NOT** be hardcoded, committed, returned to clients or emitted to telemetry. |
| Applies when | Code, configuration, examples or logs contain credential-shaped values or secret-bearing objects. |
| Default severity | `critical` |
| Enforcement | `automated` |
| Evidence | Secret scan, configuration sources, serialization paths and logging arguments. |
| Pass condition | No live secret is present and secret values are loaded through an approved runtime mechanism and redacted from output. |
| Not applicable when | A clearly non-secret placeholder cannot authenticate and is excluded from production configuration. |
| Remediation | Revoke exposed credentials, remove them from artifacts, use secret storage and add redaction. |

### SEC-004 — Protected data is minimized and purpose-bound

| Field | Value |
|---|---|
| Level | `profile:sensitive-data` |
| Requirement | Protected data **MUST** be collected, stored, transmitted, cached and logged only to the minimum extent required by its declared purpose and retention policy. |
| Applies when | A field is classified under `security.protected_data` or is evidently credential, personal, financial or regulated data. |
| Default severity | `major` |
| Enforcement | `judgment` |
| Evidence | Data flow, schemas, response models, logs, cache keys, retention and deletion paths. |
| Pass condition | Every protected field has a necessary purpose, bounded exposure, approved protection and deletion behavior. |
| Not applicable when | No protected data enters the scope. |
| Remediation | Remove the field, narrow access, encrypt where required, redact telemetry and define retention/deletion. |

### SEC-005 — Cryptography uses approved primitives and key handling

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | Security-sensitive encryption, signing, hashing and random generation **MUST** use approved maintained libraries, algorithms and key-management mechanisms; custom cryptography is forbidden. |
| Applies when | The change performs a cryptographic security function. |
| Default severity | `critical` |
| Enforcement | `tool-assisted` |
| Evidence | Library calls, algorithm parameters, key source, nonce/IV handling and rotation path, checked against `security.approved_crypto` where a project narrows it and against the cited authority otherwise. |
| Pass condition | Every operation uses an approved primitive for its purpose and keys never enter source or insecure storage. |
| Not applicable when | Hashing is explicitly non-security data partitioning and cannot be mistaken for protection. |
| Remediation | Replace custom or deprecated primitives with an approved library and migrate affected data or tokens safely. |

### SEC-006 — Executable dependencies are trusted, pinned and reviewed

| Field | Value |
|---|---|
| Level | `profile:software-supply-chain` |
| Requirement | A new or updated executable dependency **MUST** have a traceable source, compatible license, integrity pin, vulnerability assessment and demonstrated need. |
| Applies when | A manifest, lockfile, build action, container base or downloaded executable changes. |
| Default severity | `major` |
| Enforcement | `tool-assisted` |
| Evidence | Manifest and lock diff, source provenance, digest, license and advisory scan. |
| Pass condition | Provenance and integrity resolve, no unaccepted critical vulnerability exists, and existing capabilities cannot meet the need at lower risk. |
| Not applicable when | The change removes a dependency without replacing it. |
| Remediation | Pin and verify the dependency, replace it, or remove the unnecessary addition. |

### SEC-007 — Production defaults fail closed

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | Missing or invalid security configuration **MUST** fail closed, and production defaults **MUST NOT** enable debug access, broad permissions or insecure transport. |
| Applies when | Configuration controls authentication, authorization, transport, origins, diagnostics or privileged features. |
| Default severity | `major` |
| Enforcement | `tool-assisted` |
| Evidence | Default values, environment parsing, startup validation and production configuration tests. |
| Pass condition | Absent/invalid values deny access or stop startup safely, and shipped production defaults are restrictive. |
| Not applicable when | The configuration has no security effect. |
| Remediation | Validate at startup, remove permissive fallback and require an explicit secure value. |

### SEC-008 — Security failures are observable without disclosure

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | Authentication, authorization, validation and integrity failures **MUST** produce actionable security telemetry while responses and logs **MUST NOT** disclose secrets or exploitable internals. |
| Applies when | A security control rejects or detects an operation. |
| Default severity | `major` |
| Enforcement | `tool-assisted` |
| Evidence | Error responses, audit/security events, redaction and correlation fields. |
| Pass condition | Operators can identify the control, outcome and correlation context without protected values or stack internals being exposed. |
| Not applicable when | No security control or failure path exists in scope. |
| Remediation | Add structured security events, stable public errors and central redaction. |

## Severity and gate policy

Exploit paths, access-control bypass, live secret exposure and broken cryptography are `critical`.

Excess protected-data exposure, untrusted or unpinned dependencies, permissive production defaults and unsafe failure reporting are `major`. Escalate any of these to `critical` once a concrete reachable exploit path is demonstrated.

Hardening with bounded present risk is `minor`; a preference with no demonstrated risk is a suggestion.

## Waivers

SEC-001, SEC-002, SEC-003 and SEC-005 cannot be waived for a known reachable exploit or live credential. A temporary migration waiver may cover legacy code only when exposure is blocked by a verified compensating control and a security owner approves it.

## References

- [OWASP Application Security Verification Standard 5.0](https://owasp.org/www-project-application-security-verification-standard/)
- [NIST Secure Software Development Framework](https://csrc.nist.gov/projects/ssdf)
- [Rule Modeling Schema](../specs/rule-modeling.md)
