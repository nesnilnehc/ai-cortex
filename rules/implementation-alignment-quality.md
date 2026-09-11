---
artifact_type: rule
name: implementation-alignment-quality
version: 1.0.0
model: RULE_MODEL_V1
rule_prefix: ALN
scope: implemented changes with one or more upstream requirements, designs or tasks
recommended_scope: project
status: active
created_by: ai-cortex
lifecycle: living
created_at: 2026-09-11
---

# Rule: Implementation Alignment Quality

## Scope

Applies after coding when an artifact chain exists. It assesses whether the delivered code and verification evidence implement the approved intent. It does not assess intrinsic architecture, security or performance quality; the corresponding concern Rules own those criteria.

## Profiles and parameters

| Name | Kind | Provenance | Meaning |
|---|---|---|---|
| `artifact-chain` | profile | — | At least one requirement, design or task artifact is available |
| `public-contract` | profile | — | The artifact chain defines an externally consumed contract |
| `data-change` | profile | — | The artifact chain defines schema, migration or persisted-state behavior |
| `alignment.authoritative_artifacts` | parameter | derived | Ordered requirement, functional design, technical design and task paths |

Provenance follows [rule-modeling](../specs/rule-modeling.md) §5.4: a project writes only the `declared` values.

## Rules

### ALN-001 — Every approved acceptance item has implementation evidence

| Field | Value |
|---|---|
| Level | `profile:artifact-chain` |
| Requirement | Every approved acceptance criterion in scope **MUST** map to implemented behavior and independent verification evidence. |
| Applies when | An upstream acceptance criterion is assigned to the change. |
| Default severity | `critical` |
| Enforcement | `judgment` |
| Evidence | Acceptance-to-code-to-test traceability matrix built over `alignment.authoritative_artifacts`. |
| Pass condition | Each criterion has a reachable implementation location and a test or named manual verification that proves its outcome. |
| Not applicable when | The criterion is explicitly out of the current change scope in the approved artifact. |
| Remediation | Implement the omitted behavior and add evidence, or correct the approved scope before coding continues. |

### ALN-002 — Delivered behavior stays within approved scope

| Field | Value |
|---|---|
| Level | `profile:artifact-chain` |
| Requirement | Production behavior **MUST NOT** be added, removed or materially changed outside the approved artifact scope. |
| Applies when | The diff changes externally or operationally observable behavior. |
| Default severity | `major` |
| Enforcement | `judgment` |
| Evidence | Diff behavior map and approved in-scope/out-of-scope statements. |
| Pass condition | Every behavior change traces to an approved criterion, design decision or task. |
| Not applicable when | The change is a behavior-preserving refactor authorized by the technical design or ADR. |
| Remediation | Remove the scope addition or update and re-approve the upstream artifact. |

### ALN-003 — Design boundaries and tactics appear in production code

| Field | Value |
|---|---|
| Level | `profile:artifact-chain` |
| Requirement | Approved component boundaries, dependency directions and quality tactics **MUST** be represented in production code and composition. |
| Applies when | A technical design specifies boundaries, interfaces or quality tactics. |
| Default severity | `major` |
| Enforcement | `judgment` |
| Evidence | Technical design mapping, production modules, interfaces and composition root. |
| Pass condition | Each in-scope design element has a reachable production implementation with no contradictory shortcut. |
| Not applicable when | No technical design element is assigned to the change. |
| Remediation | Implement or wire the missing design element, or revise the design through review. |

### ALN-004 — Interface implementation matches the approved contract

| Field | Value |
|---|---|
| Level | `profile:public-contract` |
| Requirement | Implemented requests, responses, events, errors and authorization behavior **MUST** match the approved interface contract exactly. |
| Applies when | The artifact chain defines or changes a public contract. |
| Default severity | `critical` |
| Enforcement | `tool-assisted` |
| Evidence | Contract/schema diff, implementation, generated artifact and compatibility tests. |
| Pass condition | Names, types, optionality, errors and authorization agree, with no field dropped across layers. |
| Not applicable when | No public contract is in scope. |
| Remediation | Correct the implementation or return the contract change to design and consumer review. |

### ALN-005 — Persisted-state behavior matches the approved data design

| Field | Value |
|---|---|
| Level | `profile:data-change` |
| Requirement | Schema, constraints, indexes, migration order, backfill and rollback behavior **MUST** match the approved data design. |
| Applies when | The change alters persisted data or migration behavior. |
| Default severity | `critical` |
| Enforcement | `tool-assisted` |
| Evidence | Design, migration files, model/schema, dry-run result and rollback test where required. |
| Pass condition | The executable migration and runtime model preserve every designed constraint and transition. |
| Not applicable when | No persisted-state change exists. |
| Remediation | Align migration and runtime schema, then rerun forward and rollback verification. |

### ALN-006 — Completed tasks have concrete evidence

| Field | Value |
|---|---|
| Level | `profile:artifact-chain` |
| Requirement | A task marked complete **MUST** have its declared code, artifact and verification evidence present. |
| Applies when | A task in the change is marked done or equivalent. |
| Default severity | `minor` |
| Enforcement | `tool-assisted` |
| Evidence | Task status, changed paths, command/report output and acceptance reference. |
| Pass condition | Every completion claim resolves to the promised artifact and passing verification. |
| Not applicable when | No task list exists or the task is not claimed complete. |
| Remediation | Complete and verify the task or return its status to an unfinished state. |

### ALN-007 — Tests trace to intent rather than implementation inventory

| Field | Value |
|---|---|
| Level | `profile:artifact-chain` |
| Requirement | Functional verification **MUST** cover the approved acceptance and failure outcomes, including an item omitted entirely from the implementation. |
| Applies when | Automated or manual functional verification is used for completion. |
| Default severity | `minor` |
| Enforcement | `judgment` |
| Evidence | Acceptance-to-test mapping and negative/omission-sensitive assertions. |
| Pass condition | Verification derives from upstream intent and would fail when any required outcome is absent. |
| Not applicable when | No approved artifact chain exists. |
| Remediation | Derive tests from acceptance items and add missing negative or end-to-end assertions. |

## Severity and gate policy

Missing acceptance behavior, an incompatible contract and unsafe data divergence are `critical`: production does not do what was approved, or a consumer breaks.

Scope drift and an approved design element absent from production code are `major`.

An unsupported completion claim or an implementation-shaped test is `minor`. The distinction is deliberate: the delivered behavior may well be correct, and what is missing is the *evidence* for it. Escalate to `major` when the unsupported claim covers a criterion nothing else verifies.

## Waivers

An alignment waiver must be approved in the upstream artifact, not invented during code review. It must name the deferred criterion or design element and cannot convert an unimplemented requirement into a pass.

## References

- [Requirement Modeling Schema](../specs/requirement-modeling.md)
- [Technical Design Modeling Schema](../specs/technical-design-modeling.md)
- [Task Modeling Schema](../specs/task-modeling.md)
- [Testing Quality](./testing-quality.md)
- [Rule Modeling Schema](../specs/rule-modeling.md)
