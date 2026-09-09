---
artifact_type: rule
name: test-case-quality
version: 1.0.0
created_by: ai-cortex
lifecycle: living
created_at: 2026-05-26
recommended_scope: user
status: active
---

# Rule: Test Case Quality

> A 5-dimension review checklist plus spec compliance. Every item is independently verifiable.
>
> Applies to QA business test case documents that declare conformance to [specs/test-case-modeling.md](../specs/test-case-modeling.md), in either form — a single case, or a collection table.
>
> **Does not apply** to code-level tests; reviewing those belongs to [rules/standards-test-code.md](./standards-test-code.md).

---

## 5-dimension review

Authors should self-check against this list before submitting for review. The checkpoints map one to one onto the 5 review dimensions: completeness, executability, clarity, soundness, traceability.

### 1. Completeness — is the information all there?

- [ ] Every required frontmatter field is present (`id` / `artifact_type` / `created_at` / `status` / `priority` / `test_type` / `covers` / `parent`)
- [ ] All 5 body sections present (scenario / preconditions / steps / expected result / traceability anchor); a collection needs the corresponding table columns
- [ ] The `covers` field carries at least 1 traceability anchor, pointing at an AC, an interface contract or a key scenario
- [ ] A case in `deprecated` status has `deprecated_at` and `deprecated_reason` filled in

### 2. Executability — can an executor follow it directly?

- [ ] Every precondition is independently verifiable — no unverifiable clause such as "the environment is fine"
- [ ] Steps are clearly numbered and each is atomic and executable — not "give it a test" or "check the related functionality"
- [ ] Steps carry concrete input data — parameter values, payloads, user identity — not "enter valid data"
- [ ] At most 10 steps; beyond that the case is too coarse and should be split
- [ ] A case with side effects includes cleanup steps, or documents them in a Teardown section

### 3. Clarity — is it unambiguous?

- [ ] The title names the subject and the key condition, not something vague like "test login"
- [ ] The expected result carries **no vague words**: "normal", "OK", "reasonable", "should", "roughly"
- [ ] The expected result is observable and decidable — an HTTP status code, a field value, a UI element appearing or disappearing
- [ ] Steps take a **black-box view** and contain no implementation code such as `await axios.post(...)`
- [ ] Terminology is consistent and does not conflict with the upstream requirement or contract

### 4. Soundness — does this case deserve to exist?

- [ ] One case verifies one kind of condition on one subject; independent scenarios are not mixed together
- [ ] Priority matches the importance of the scenario — P0 is reserved for release-blocking paths and not overused
- [ ] No duplication of an existing case; where one AC has several cases, each covers a different dimension — positive, boundary, exception
- [ ] The case is small enough to run in reasonable time — at most 5 min manual, at most 30 s automated
- [ ] `test_type` is chosen correctly (functional / contract / regression / non-functional)

### 5. Traceability — can the impact of a change be located?

- [ ] The `covers` field follows the format (`<req-id>#<AC-n>` or `<contract-path>#<endpoint>`)
- [ ] The AC or contract referenced by `covers` actually exists — no dead link to a deleted requirement
- [ ] `parent` points at the real path of the upstream requirement or contract
- [ ] The upstream requirement is at `status: approved` or beyond; formal cases are not written against a `draft` requirement
- [ ] Reverse lookup works: from a requirement's AC, at least 1 covering case can be found — no bare ACs

---

## Spec compliance (specs/test-case-modeling.md)

- [ ] Frontmatter `artifact_type` is `test-case` for a single case, or `test-cases` for a collection
- [ ] `id` follows `TC-<MODULE>-<nn>` — required for a single case, and for every row of a collection
- [ ] `lifecycle` is `snapshot` for a single case and `living` for a collection
- [ ] `status` ∈ `draft` / `active` / `deprecated`
- [ ] `priority` ∈ `P0` / `P1` / `P2`
- [ ] `test_type` ∈ `functional` / `contract` / `regression` / `non-functional`
- [ ] `covers` is non-empty and every entry follows the format
- [ ] **No execution-state field** such as `executed` / `passed` / `failed` has been introduced — results belong in a test report
- [ ] File naming follows §3: `TC-<MODULE>-<nn>.md` for a single case, `test-cases-<module>.md` for a collection

---

## Anti-patterns

- ❌ `covers` empty or filled with `TBD`
- ❌ One case covering ACs across different requirements — split it
- ❌ Vague words in the expected result ("displays normally", "returns a reasonable result")
- ❌ Implementation code in the steps, breaking the black-box view
- ❌ One case verifying several independent subjects
- ❌ A case moved to `deprecated` without the conditionally required frontmatter fields
- ❌ A case citing a `draft` requirement as its traceability anchor
- ❌ A module with ≥ 5 cases still kept as single files instead of merged into a collection table
- ❌ Mixed `id` formats inside one collection table, such as `TC-AUTH-01` next to `AUTH-002`
- ❌ Reviewing a code-level test against this rule; those belong to [standards-test-code](./standards-test-code.md)

---

## Related assets

- **Data contract**: [specs/test-case-modeling.md](../specs/test-case-modeling.md)
- **Test code standards**: [rules/standards-test-code.md](./standards-test-code.md)
- **Upstream spec**: [specs/requirement-modeling.md](../specs/requirement-modeling.md)
- **Sibling review rules**: [requirement-quality](./requirement-quality.md) / [functional-design-quality](./functional-design-quality.md) / [technical-design-quality](./technical-design-quality.md) / [task-quality](./task-quality.md)
