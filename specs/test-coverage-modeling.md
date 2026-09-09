---
id: TEST_COVERAGE_MODELING_SPEC_V1
name: Test Coverage Report Schema
description: Spec defining the structural contract for test coverage assessment reports — the unified artifact carrying traceability matrix (AC × test cases), mutation test summary, and cross-artifact trace health audit. Consumed by suite-coverage and cross-artifact-alignment review services to judge sufficiency and necessity of a test case suite.
version: 1.0.0
status: active
lifecycle: living
created_at: 2026-05-25
scope: |
  Defines the structural contract for test coverage assessment reports — snapshot artifacts
  produced at release gates, audit checkpoints, or after major requirement/contract changes.
  Carries three sub-payloads: traceability matrix, mutation test summary, trace health audit.
  Does NOT define how the data is collected (tool-specific) or how individual test cases are
  structured (see test-case-modeling.md). Consumed by review services performing
  suite-coverage reviews and cross-artifact alignment reviews.
related:
  - ./spec-modeling.md
  - ./test-case-modeling.md
  - ./requirement-modeling.md
  - ../rules/test-coverage-quality.md
  - ../rules/test-case-quality.md
  - ../rules/doc-health-criteria.md
---

# Test Coverage Report Modeling Schema

> **Data contract**: defines the field structure and body skeleton of a test coverage assessment report

---

## 1. Position and scope

A test coverage report is the input artifact for a **suite-coverage review** and a **cross-artifact alignment review**. It fixes the evidence behind the judgement of "how sufficient, how necessary and how well traced a test suite is against its requirements and designs" into a snapshot that can be reviewed, compared and archived.

| Review type | The question it asks | Corresponding section here |
|---|---|---|
| Single-case review | Does this one test case hold up on its own? | **Out of this report's scope** (it belongs to [rules/test-case-quality.md](../rules/test-case-quality.md)) |
| Suite-coverage review | Is the suite both sufficient and necessary against the requirements? | §5.2 traceability matrix + §5.3 mutation test summary |
| Cross-artifact alignment review | Is the chain from the suite to the upstream requirements and contracts intact? | §5.4 trace health audit |

In scope:

- **Release gate**: take one coverage snapshot of the current suite before shipping
- **Quarterly regression-suite governance**: review the suite's redundancy and gaps on a cycle
- **Impact assessment for a requirement, contract or ADR change**: compare snapshots before and after an upstream change to judge the impact
- **Cross-team contract integration review**: produce coverage evidence when a contract is upgraded

Out of scope:

- **Reviewing an individual test case** (it belongs to [rules/test-case-quality.md](../rules/test-case-quality.md))
- **Test execution reports** (pass/fail/duration and other run results, carried by the CI report)
- **Raw code coverage data** (line/branch coverage, produced directly by the coverage tool; this artifact only cites its conclusion)

---

## 2. Mental model

> The core questions a sound coverage report has to answer.

Every report must be able to answer **3 questions**:

| Dimension | Core question | Where it lands |
|---|---|---|
| **Sufficiency** | Is the coverage there? Where are the blanks? | §5.2 traceability matrix |
| **Necessity** | How redundant is the suite? What can be pruned? | §5.3 mutation test summary |
| **Trace health** | Is the chain from the cases to the upstream artifacts intact and valid? | §5.4 trace health audit |

Leave any one of them unanswered and the report is unfit: a reviewer cannot make a release or governance decision from it.

---

## 3. Naming

```text
coverage-report-<scope>-<YYYY-MM-DD>.md
```

- `<scope>`: the identifier of the assessed scope — `<module>` or `<release>` is recommended, in kebab-case
- `<YYYY-MM-DD>`: the date the report was generated
- Examples: `coverage-report-auth-2026-05-25.md` / `coverage-report-v2.4-2026-05-25.md`
- The storage location is decided by project governance (typically `docs/test-coverage/`)

A report is a **snapshot artifact**: each run creates a new file and never overwrites an older one.

---

## 4. Frontmatter contract

```yaml
---
artifact_type: test-coverage-report
lifecycle: snapshot
created_at: YYYY-MM-DD
scope: <module-or-release-identifier>
trigger: release-gate | quarterly-audit | requirement-change | contract-upgrade
covers_artifacts:
  - <requirement-or-contract-path>
test_case_sources:
  - <test-case-doc-or-dir-path>
tool_provenance:
  matrix_generator: <tool-name@version>
  mutation_tool: <tool-name@version>
verdict: pass | fail | conditional
# conditional fields
conditional_reasons:                    # required when verdict: conditional
  - <reason>
---
```

### 4.1 Field table

| Field | Type | Required | Description |
|---|---|---|---|
| `artifact_type` | string | Yes | Fixed as `test-coverage-report` |
| `lifecycle` | enum | Yes | Fixed as `snapshot` |
| `created_at` | date | Yes | The date the report was generated |
| `scope` | string | Yes | The assessed scope (a module name, a release number, or a custom identifier) |
| `trigger` | enum | Yes | What triggered the report, which sets how strict the review is |
| `covers_artifacts` | list[path] | Yes | The upstream artifacts whose coverage this report assesses (requirements / contracts / designs) |
| `test_case_sources` | list[path] | Yes | The test case documents or code directories the data came from |
| `tool_provenance` | object | Yes | The tool and version that produced each key figure, so the data stays traceable and reproducible |
| `verdict` | enum | Yes | The overall conclusion: `pass` / `fail` / `conditional` (semantics in §4.2) |
| `conditional_reasons` | list[string] | Conditional | Required when `verdict: conditional`; lists the conditions attached |

### 4.2 verdict semantics

| Value | Meaning | Entry condition |
|---|---|---|
| `pass` | Coverage is sufficient, redundancy is under control, tracing is intact | None of the three sections (matrix / mutation / tracing) carries a blocker |
| `conditional` | A qualified pass, needing a specific waiver or later remediation | One item deviates acceptably and the condition has been recorded |
| `fail` | Not passed; cases must be added or the review redone | Any section carries a blocker (a critical AC uncovered / mutation score below the threshold / a dead trace link) |

**verdict is a conclusion field, not a process field**: it derives from the report body and must not contradict it.

---

## 5. Body structure contract

### 5.1 Required sections (4)

**H1 title**: `# Test coverage report: <scope> @ <date>`

| # | Section | Purpose | Validation |
|---|---|---|---|
| 1 | Summary | One chart or one paragraph stating the verdict and the key figures | Carries the three key metrics: coverage rate / mutation score / number of dead links |
| 2 | Traceability matrix | The AC × case × dimension matrix | See §5.2 |
| 3 | Mutation test summary | The gold-standard evidence for necessity | See §5.3 |
| 4 | Trace health audit | The integrity of the chain across artifacts | See §5.4 |

### 5.2 Traceability matrix contract

Format: a table whose rows are AC × dimension and whose columns are test case ids.

| Field | Value |
|---|---|
| Row key | `<REQ-ID>#AC<n> · <dimension>`, where dimension ∈ `positive` / `boundary` / `exception` / `non-functional` / `state-transition` / `concurrency` |
| Column key | The test case id (`TC-<MODULE>-<nn>`, or `<module>::<function>` for a code-level case) |
| Cell | `✓` covered / `—` not applicable / empty means missing |

**Hard criterion for sufficiency**: every row carries at least 1 `✓`, or the whole row is marked `—`, declaring that dimension inapplicable with a reason.
**Soft criterion for necessity**: every column has at least 1 `✓` occupying a **unique** cell; a repeat within the same dimension is a redundancy signal.

Example:

```markdown
| AC × dimension | TC-AUTH-01 | TC-AUTH-02 | TC-AUTH-03 |
| :--- | :---: | :---: | :---: |
| ACME-REQ-08#AC1 · positive | ✓ |  |  |
| ACME-REQ-08#AC1 · exception |  | ✓ |  |
| ACME-REQ-08#AC1 · boundary |  |  | ✓ |
| ACME-REQ-08#AC2 · positive | — | — | — |  ← explicitly declared inapplicable
```

**An empty row must carry its reason**: a row with missing coverage must appear in a "gap list" below the matrix, each entry carrying the planned remediation, the owner and the due date.

### 5.3 Mutation test summary contract

One row per module under test, and each row must carry these fields:

| Field | Type | Description |
|---|---|---|
| `module` | string | The module identifier, matching the code path |
| `mutants_total` | int | Total mutants injected |
| `mutants_killed` | int | Mutants caught by the suite |
| `mutation_score` | float | `killed / total`, expressed as a percentage |
| `survived_critical` | int | Surviving mutants on a critical path, labelled by the tool or by hand |
| `threshold` | float | The threshold the project agreed on (≥ 0.80 is recommended) |
| `status` | enum | `pass` (≥ threshold) / `fail` (< threshold) / `waived`, which must carry a reason |

Example:

```markdown
| Module | Total | Killed | Score | Survived (critical) | Threshold | Status |
| :--- | ---: | ---: | ---: | ---: | ---: | :--- |
| auth/token | 142 | 128 | 90.1% | 0 | 80% | pass |
| auth/session | 89 | 61 | 68.5% | 3 | 80% | fail |
```

**A `fail` row must carry a "surviving mutants detail" subsection**: list the surviving critical mutants, the untested dimension inferred from them, and the cases suggested to close the gap.

**Never fabricate figures for a mutation run that did not happen**: when no tool is integrated, write "not run — <reason> — planned integration date" in this section, and require verdict ≤ `conditional`.

### 5.4 Trace health audit contract

3 kinds of check, one table each:

**5.4.1 Dead link list** — a case whose `covers` anchor points at an upstream artifact that has been deleted or renamed:

| Case id | Dead anchor | What changed upstream | Suggested action |
|---|---|---|---|

**5.4.2 Bare AC list** — an upstream AC covered by no case at all:

| AC id | Owning requirement | Untested dimension | Remediation owner |
|---|---|---|---|

**5.4.3 Dangling guard list** — the requirement a case guards is already `deprecated`, but the case has not followed:

| Case id | Dangling guard target | Upstream deprecation date | Suggested action |
|---|---|---|---|

If **any** of the three lists is non-empty → verdict ≥ `conditional`; if **a critical AC is bare or its link is dead** → verdict = `fail`.

### 5.5 Optional sections

| Section | Triggering situation |
|---|---|
| Trends | Compared against the previous report of the same scope, covering changes in mutation score, dead link count and bare AC count |
| Risk-weighted assessment | Prioritise gaps by "frequency × impact" to drive the remediation schedule |
| Decision guard audit | Check whether the premises for rejecting an alternative in an ADR are still guarded by a case |

---

## 6. Anti-patterns

- ❌ A verdict that contradicts the body (verdict: pass while the traceability matrix has an empty row never declared inapplicable)
- ❌ A mutation score given without a mutation run — fabricated data
- ❌ A traceability matrix merging several ACs into one row, which destroys per-row judgement
- ❌ A missing `tool_provenance` field, leaving the figures irreproducible and their credibility unjudgeable
- ❌ Passing off code coverage (line coverage) as evidence of sufficiency; line coverage is not business coverage
- ❌ Generating a report for every edit to a case; a snapshot answers a meaningful trigger, not PR-level noise
- ❌ verdict: conditional with `conditional_reasons` left empty
- ❌ Merging the dead link, bare AC and dangling guard lists into one table; the 3 problems have different owners and different remedies, so they must be listed separately
- ❌ Stuffing the 5-dimension verdict on an individual case into this report; single-case review belongs to [test-case-quality](../rules/test-case-quality.md) and is not mixed with coverage review
- ❌ Editing the body after the report is generated; a snapshot freezes once published, and a correction means a new report plus a CHANGELOG entry

---

## 7. Examples

### 7.1 A minimal compliant coverage report: the auth module at a release gate

````markdown
---
artifact_type: test-coverage-report
lifecycle: snapshot
created_at: 2026-05-25
scope: auth
trigger: release-gate
covers_artifacts:
  - ../requirements/ACME-REQ-08.md
  - ../contracts/auth-contract.md
test_case_sources:
  - ../test-cases/test-cases-auth.md
  - tests/auth/
tool_provenance:
  matrix_generator: trace-matrix-cli@0.3.1
  mutation_tool: mutmut@2.4.3
verdict: conditional
conditional_reasons:
  - the auth/session module's mutation score of 68.5% is below the 80% threshold; remediation is scheduled for the next iteration
---

# Test coverage report: auth @ 2026-05-25

## Summary

- **AC coverage**: 12/13 (92.3%) — ACME-REQ-08#AC5 (the OAuth callback path) is missing
- **Mutation score**: auth/token 90.1% ✅ / auth/session 68.5% ❌
- **Dead trace links**: 0
- **Bare ACs**: 1 (remediation plan recorded)
- **Dangling guards**: 0

verdict = **conditional**: releasable, but the session module must close its mutation coverage before v2.5.

## Traceability matrix

| AC × dimension | TC-AUTH-01 | TC-AUTH-02 | TC-AUTH-03 | TC-AUTH-04 |
| :--- | :---: | :---: | :---: | :---: |
| ACME-REQ-08#AC1 · positive | ✓ |  |  |  |
| ACME-REQ-08#AC1 · exception |  | ✓ |  |  |
| ACME-REQ-08#AC2 · tampering |  |  | ✓ |  |
| ACME-REQ-08#AC4 · header format |  |  |  | ✓ |
| ACME-REQ-08#AC5 · OAuth callback |  |  |  |  | ← gap

### Gap list

| Row | Planned action | Owner | Due |
| :--- | :--- | :--- | :--- |
| ACME-REQ-08#AC5 · positive | Add TC-AUTH-05 + TC-AUTH-06 | qa-alice | v2.5 |

## Mutation test summary

| Module | Total | Killed | Score | Survived (critical) | Threshold | Status |
| :--- | ---: | ---: | ---: | ---: | ---: | :--- |
| auth/token | 142 | 128 | 90.1% | 0 | 80% | pass |
| auth/session | 89 | 61 | 68.5% | 3 | 80% | fail |

### auth/session surviving mutants detail

- The `session.expire_at` comparison `<` → `<=` survives → no boundary case for "the exact instant of expiry"
- The mutant removing the check that an old token is invalidated after `refresh_token` rotation survives → no security regression case
- The `concurrent refresh` lock-failure mutant survives → no concurrency case

## Trace health audit

### Dead link list
(empty)

### Bare AC list

| AC id | Owning requirement | Untested dimension | Remediation owner |
| :--- | :--- | :--- | :--- |
| ACME-REQ-08#AC5 | ACME-REQ-08 | positive + exception | qa-alice |

### Dangling guard list
(empty)
````

---

## 8. Relationship to other assets

- **Companion rule**: [rules/test-coverage-quality.md](../rules/test-coverage-quality.md) — the 5-dimension review checklist for a coverage assessment report
- **Downstream consumers**: the suite-coverage review service and the cross-artifact alignment review service read this artifact and produce a review decision from it
- **Data source spec**: [test-case-modeling.md](./test-case-modeling.md) — the matrix columns and the bare-AC detection both rely on a case's `covers` field
- **Upstream alignment spec**: [requirement-modeling.md](./requirement-modeling.md) — the matrix row key's `<REQ-ID>#AC<n>` anchors to that AC ID format
- **Related rule**: [doc-health-criteria.md](../rules/doc-health-criteria.md) — dead link detection reuses its link-graph health criteria
- **Recursive basis**: this spec itself follows the 8-section skeleton of [spec-modeling.md](./spec-modeling.md) v2.0.0
