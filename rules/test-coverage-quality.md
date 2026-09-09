---
artifact_type: rule
name: test-coverage-quality
version: 1.0.0
created_by: ai-cortex
lifecycle: living
created_at: 2026-05-26
recommended_scope: user
status: active
---

# Rule: Test Coverage Report Quality

> A 5-dimension review checklist plus spec compliance. Every item is independently verifiable.
>
> Applies to test coverage assessment reports that declare conformance to [specs/test-coverage-modeling.md](../specs/test-coverage-modeling.md) — the input artifact for reviewing a test suite's coverage and for cross-artifact alignment review.
>
> This rule does not review an individual test case (that belongs to [test-case-quality](./test-case-quality.md)) nor test code (that belongs to [standards-test-code](./standards-test-code.md)).

---

## 5-dimension review

### 1. Completeness — is the information all there?

- [ ] Every required frontmatter field is present (`artifact_type` / `scope` / `trigger` / `covers_artifacts` / `test_case_sources` / `tool_provenance` / `verdict`)
- [ ] All 4 body sections present (assessment summary / traceability matrix / mutation testing summary / traceability health audit)
- [ ] The assessment summary carries the three key metrics (AC coverage / mutation score / dead link count)
- [ ] A report with `verdict: conditional` has `conditional_reasons` filled in

### 2. Truthfulness — is the data credible?

- [ ] `tool_provenance` names the tools that actually produced the numbers, with versions — not empty, not a placeholder
- [ ] The mutation score comes from a real tool run; where mutation testing is not integrated, it must be marked explicitly as "not run — <reason>" and the verdict is at most `conditional`
- [ ] Traceability matrix cells are aggregated from `covers` fields, not filled in by hand
- [ ] The report's generation date agrees with the run dates of the tools it cites, avoiding stale data passing as a fresh assessment

### 3. Explainability — are gaps and waivers accounted for?

- [ ] Every row of the traceability matrix has at least 1 `✓`, or the whole row is marked `—` with a stated reason for being not applicable
- [ ] Gaps — empty rows — are listed in the gap list, each with a remedial action, an owner and a due date
- [ ] Every mutation row marked `fail` carries a "surviving mutants detail" subsection inferring which dimension is untested
- [ ] A `waived` status carries the reason for the waiver, not an empty phrase like "skipped for now"

### 4. Risk alignment — does gap severity match the verdict?

- [ ] A critical AC uncovered (a P0 requirement, anything security-related, a contract interface) → verdict = `fail`
- [ ] Mutants surviving on a critical path (`survived_critical > 0`) → verdict ≥ `conditional`
- [ ] A non-zero count of dead links or dangling guards → verdict ≥ `conditional`
- [ ] The verdict does not contradict the body: a pass report has no blocker in it, a fail report states its blocker explicitly
- [ ] Gap priorities match the upstream requirement's `priority` — a gap against a P0 requirement must not be treated the same as one against a P2

### 5. Currency and traceability — does the assessment match today's state?

- [ ] The upstream paths referenced by `covers_artifacts` resolve — no 404s
- [ ] The case documents and code directories referenced by `test_case_sources` exist
- [ ] The report's `created_at` is within 7 days of the `trigger` event; beyond that it counts as a stale assessment
- [ ] The dead link list agrees with the current state of the upstream artifacts — nothing "already fixed but not updated in the report"
- [ ] The report is comparable with the previous report of the same `scope`, so a trend can be traced

---

## Spec compliance (specs/test-coverage-modeling.md)

- [ ] Frontmatter `artifact_type: test-coverage-report`
- [ ] `lifecycle: snapshot`
- [ ] `trigger` ∈ `release-gate` / `quarterly-audit` / `requirement-change` / `contract-upgrade`
- [ ] `verdict` ∈ `pass` / `fail` / `conditional`
- [ ] Filename follows `coverage-report-<scope>-<YYYY-MM-DD>.md`
- [ ] Traceability matrix row keys follow `<REQ-ID>#AC<n> · <dimension>`
- [ ] Every mutation summary row carries the 7 required fields (module / total / killed / score / survived_critical / threshold / status)
- [ ] The traceability health audit carries 3 separate tables (dead links / bare ACs / dangling guards), not merged

---

## Anti-patterns

- ❌ Verdict contradicting the body — a pass report containing an unwaived empty row, or a fail report with no blocker explained
- ❌ A mutation score given without a tool run behind it
- ❌ Line coverage passed off as evidence of adequacy
- ❌ A gap list stating problems without remedial actions or owners
- ❌ Dead links, bare ACs and dangling guards merged into one table
- ❌ Editing the body of a snapshot report after it was generated — create a new report and record it in the CHANGELOG
- ❌ The wrong trigger — running release-gate for routine PR review, which just creates noise
- ❌ Stuffing a 5-dimension review of individual cases into this report; review types are not mixed
- ❌ A gap from the previous report going untracked in the new one, leaving no trend comparison
- ❌ `tool_provenance` left empty or filled with "various", which makes the result irreproducible

---

## Boundary with the upstream rules

| Subject of review | Owning rule | Trigger |
|---|---|---|
| One business test case | [test-case-quality](./test-case-quality.md) | A single-case PR, or a new case |
| Test code, as code | [standards-test-code](./standards-test-code.md) | A test code PR |
| A report on how a suite covers the requirements | **this rule** | Release gate / quarterly audit / upstream change impact |
| The document link graph and artifact health | [doc-health-criteria](./doc-health-criteria.md) | A repository-wide documentation audit |

---

## Related assets

- **Data contract**: [specs/test-coverage-modeling.md](../specs/test-coverage-modeling.md)
- **Data sources**: the `covers` field from [specs/test-case-modeling.md](../specs/test-case-modeling.md), and AC IDs from `requirement-modeling`
- **Sibling review rules**: [test-case-quality](./test-case-quality.md) / [standards-test-code](./standards-test-code.md) / [doc-health-criteria](./doc-health-criteria.md)
