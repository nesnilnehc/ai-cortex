---
artifact_type: rule
name: testing-quality
version: 1.0.1
model: RULE_MODEL_V1
rule_prefix: TST
scope: automated tests and the verification strategy for changed production behavior
recommended_scope: project
status: active
created_by: ai-cortex
lifecycle: living
created_at: 2026-09-11
---

# Rule: Testing Quality

## Scope

Applies to code changes and their automated verification. These criteria complement [standards-test-code](./standards-test-code.md); they assess adequacy of the test system, not test-file style alone.

## Profiles and parameters

| Name | Kind | Provenance | Meaning |
|---|---|---|---|
| `public-contract` | profile | — | A released API, event, persisted format or CLI contract changes |
| `integration-boundary` | profile | — | Behavior depends on wiring, serialization, storage or a remote boundary |
| `critical-path` | profile | — | Failure can cause data loss, security impact or core user-journey failure |
| `testing.coverage_policy` | parameter | declared | Project-specific mutation, branch or traceability targets |

Provenance follows [rule-modeling](../specs/rule-modeling.md) §5.4: a project writes only the `declared` values.

## Rules

### TST-001 — Changed behavior has a direct oracle

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | Every changed observable behavior **MUST** have at least one automated test whose assertion would fail if that behavior were absent or wrong. |
| Applies when | Production behavior changes. |
| Default severity | `minor` |
| Enforcement | `judgment` |
| Evidence | Diff-to-test mapping and assertion behavior. |
| Pass condition | Each changed outcome maps to a test with a discriminating assertion. |
| Not applicable when | The change is documentation or non-executable metadata only. |
| Remediation | Add the smallest behavior-level test that fails under the prior or broken implementation. |

### TST-002 — Error and boundary paths are verified

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | Tests **MUST** cover applicable invalid, empty, limit, timeout, cancellation and dependency-failure paths introduced or changed by the scope. |
| Applies when | The changed behavior has one or more such paths. |
| Default severity | `minor` |
| Enforcement | `judgment` |
| Evidence | Branches and corresponding tests/assertions. |
| Pass condition | Every materially different terminal outcome is exercised and asserted. |
| Not applicable when | No error or boundary path is changed. |
| Remediation | Add focused negative and boundary tests with outcome assertions. |

### TST-003 — Integration behavior is tested at the assembly boundary

| Field | Value |
|---|---|
| Level | `profile:integration-boundary` |
| Requirement | Wiring, serialization, migration, route registration and cross-component behavior **MUST** be verified by an integration test that crosses the real assembly boundary. |
| Applies when | The change affects an integration boundary. |
| Default severity | `minor` |
| Enforcement | `tool-assisted` |
| Evidence | Integration test setup and executed production wiring or equivalent contract harness. |
| Pass condition | The test fails for a missing binding, field, route or migration and passes with the intended assembly. |
| Not applicable when | The code has no integration boundary. |
| Remediation | Add an integration or contract test using production composition and serialization. |

### TST-004 — Public contracts have compatibility tests

| Field | Value |
|---|---|
| Level | `profile:public-contract` |
| Requirement | A changed public contract **MUST** have consumer, schema-diff or compatibility tests covering existing supported consumers. |
| Applies when | A released API, event, persisted format or CLI contract changes. |
| Default severity | `major` |
| Enforcement | `automated` |
| Evidence | Consumer tests, schema compatibility output or golden contract fixtures. |
| Pass condition | Existing supported inputs and consumers remain valid, or a versioned migration is tested. |
| Not applicable when | The contract has no released or independent consumer. |
| Remediation | Restore compatibility or add a versioned contract with migration tests. |

### TST-005 — Critical paths resist implementation-shaped blind spots

| Field | Value |
|---|---|
| Level | `profile:critical-path` |
| Requirement | Critical-path tests **MUST** derive expected outcomes from the requirement or contract and **MUST NOT** merely mirror the current implementation structure. |
| Applies when | The change affects a critical path. |
| Default severity | `minor` |
| Enforcement | `judgment` |
| Evidence | Upstream acceptance/contract references and test assertions. |
| Pass condition | The oracle is independently traceable and catches omission of a required behavior. |
| Not applicable when | No critical path is affected. |
| Remediation | Reframe tests around external outcomes and add a traceability reference. |

### TST-006 — Tests are deterministic and isolated

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | Tests **MUST** control time, randomness, concurrency and external state sufficiently to produce repeatable outcomes and independent ordering. |
| Applies when | A test uses mutable global state, time, randomness, concurrency, network or shared storage. |
| Default severity | `minor` |
| Enforcement | `tool-assisted` |
| Evidence | Setup/teardown, seeded inputs, fake clock, isolated resources and repeat runs. |
| Pass condition | Reordering or repeating tests does not change outcomes under the supported environment. |
| Not applicable when | The test is purely deterministic and local. |
| Remediation | Inject controllable dependencies, isolate resources and remove order dependence. |

### TST-007 — Doubles preserve the relevant contract

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | A mock, fake or stub **MUST** preserve the contract behavior relevant to the test and **MUST NOT** replace the behavior being verified. |
| Applies when | A test uses a test double. |
| Default severity | `minor` |
| Enforcement | `judgment` |
| Evidence | Double behavior, real contract and assertion boundary. |
| Pass condition | The double isolates an external dependency while the subject's real behavior and contract remain exercised. |
| Not applicable when | No test double is used. |
| Remediation | Move the double outside the subject, use a higher-fidelity fake or add a contract test. |

### TST-008 — Declared coverage policy has reproducible evidence

| Field | Value |
|---|---|
| Level | `project:testing.coverage_policy` |
| Requirement | A declared coverage, mutation or traceability gate **MUST** be measured by a reproducible tool run and interpreted against the changed risk, not treated as a standalone quality score. |
| Applies when | `testing.coverage_policy` is declared for the scope. |
| Default severity | `minor` |
| Enforcement | `automated` |
| Evidence | Tool/version, command, report and mapping to changed requirements or code. |
| Pass condition | The configured threshold passes and no critical changed behavior is uncovered despite aggregate success. |
| Not applicable when | No coverage policy is declared. |
| Remediation | Run the configured tool, close critical gaps and record the reproducible result. |

## Severity and gate policy

Testing findings report missing **evidence**, not broken behavior. Where a production defect exists, the concern Rule for that defect owns it and carries its severity; this Rule set reports only that nothing would have caught it.

An untested change to a public contract is `major`: an incompatible contract reaches consumers undetected.

Every remaining gap is `minor` — a missing oracle, an unexercised boundary or error path, an untested assembly, an implementation-shaped critical-path test, non-determinism, an over-reaching double, an unreproduced coverage gate. Escalate to `major` when the untested behavior sits on a declared critical path, and to `critical` only when the change ships an irreversible effect that nothing can verify.

## Waivers

A critical-path or public-contract waiver must identify an alternative independent verification method and expire no later than the next release. Aggregate coverage cannot waive a specifically uncovered critical behavior.

## References

- [Classic software engineering sources](../docs/references/software-engineering-classics.md) — source hierarchy and applicability boundaries
- [Code Complete, Second Edition](https://www.microsoftpressstore.com/store/code-complete-9780735619678) — construction-time defect prevention, debugging and testing; informs TST-001, TST-002 and TST-006
- [Refactoring, Second Edition](https://martinfowler.com/books/refactoring.html) — tests as protection for behavior-preserving structural change; informs TST-001, TST-005 and TST-006
- [Programming Pearls, Second Edition](https://www.informit.com/store/programming-pearls-9780134498041) — program verification, testing, debugging and timing; informs TST-001, TST-002 and TST-007
- [Continuous Delivery](https://www.informit.com/store/continuous-delivery-reliable-software-releases-through-9780321601919) — automated acceptance and non-functional testing in a deployment pipeline; informs TST-003, TST-004 and TST-008
- [Google engineering practices: what to look for in review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
- [Test code standards](./standards-test-code.md)
- [Test coverage quality](./test-coverage-quality.md)
- [Rule Modeling Schema](../specs/rule-modeling.md)
