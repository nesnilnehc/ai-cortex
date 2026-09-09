---
id: TEST_CASE_MODELING_SPEC_V1
name: Test Case Modeling Schema
description: Spec defining QA business test case document fields, naming, body sections, traceability to requirements/acceptance criteria, and execution status semantics. Scope limited to document artifacts; code-level test code is governed by rules/standards-test-code.md.
version: 1.0.1
status: active
lifecycle: living
created_at: 2026-05-25
scope: |
  Defines the structural contract for QA-owned business test case documents (markdown
  artifacts that describe black-box scenarios traceable to acceptance criteria, interface
  contracts, or key scenario lists). Does NOT cover code-level test cases written as
  test functions — those are governed by rules/standards-test-code.md as a coding standard,
  since the test function itself is the artifact (no separate document exists).
related:
  - ./spec-modeling.md
  - ./requirement-modeling.md
  - ./technical-design-modeling.md
  - ../rules/test-case-quality.md
  - ../rules/standards-test-code.md
---

# Test Case Modeling Schema

> **Data contract**: defines the field structure and body skeleton of a QA business test case document

---

## 1. Position and scope

A test case document answers what preconditions hold, what actions are taken, and what result is expected. It is the executable black-box verification record derived, within QA, from a requirement's acceptance criteria, an interface contract, or a list of key scenarios.

In scope:

- **QA business test cases**, derived from a requirement document in `approved` status, verifying that the product satisfies an AC
- **Interface contract verification cases**, derived from an upstream interface contract such as a `*-contract.md`
- **Key scenario regression cases**, the regression set for a business-critical path

Out of scope:

- **Code-level tests** (unit, integration and E2E in code) — the test function is itself the artifact and has no separate document; governed by [`rules/standards-test-code.md`](../rules/standards-test-code.md)
- **Exploratory testing notes**, an unstructured process that needs no data contract
- **Performance and load scripts**, carried by dedicated tools and scripts, out of scope here

---

## 2. Mental model

> The core questions a sound test case answers.

Every test case must be able to answer **3 questions plus 1 anchor**:

| Dimension | Core question | Field |
|---|---|---|
| **Subject** | Which object or flow is under test? | `scenario` |
| **Condition** | Under what preconditions and trigger? | `preconditions` and `steps` |
| **Expected** | What result is expected? | `expected` |
| **Trace** | Which business promise does this case guard? | `covers`, pointing at an AC, an interface contract or a scenario |

Missing any one makes the case unsound: downstream review has no way to locate why the case exists.

---

## 3. Naming

### 3.1 Single-case document form

```text
TC-<MODULE>-<nn>.md
```

- `<MODULE>`: the module abbreviation in upper case, 2-6 characters, such as `AUTH`, `PAY` or `KB`
- `<nn>`: a sequence number within the module, starting at 2 digits, monotonically increasing, and **never reused**
- Examples: `TC-AUTH-05.md`, `TC-PAY-042.md`
- Where they live is decided by project governance; typically `docs/test-cases/`

### 3.2 Collection table form

Once a module has ≥ 5 cases, merging them into a table collection is recommended:

```text
test-cases-<module>.md
```

- Example: `test-cases-auth.md`
- One case per table row, with the fields from §5.1
- Within a collection, `id` still follows `TC-<MODULE>-<nn>`

---

## 4. Frontmatter contract

### 4.1 Single-case frontmatter

```yaml
---
id: TC-<MODULE>-<nn>
artifact_type: test-case
lifecycle: snapshot
created_at: YYYY-MM-DD
status: draft | active | deprecated
priority: P0 | P1 | P2
test_type: functional | contract | regression | non-functional
covers:
  - <requirement-id>#<AC-n>
  - <contract-path>#<endpoint>
parent: <upstream requirement or contract path>
# conditional fields
deprecated_at: YYYY-MM-DD          # required when status is deprecated
deprecated_reason: <reason>         # required when status is deprecated
---
```

### 4.2 Collection frontmatter

```yaml
---
artifact_type: test-cases
lifecycle: living
created_at: YYYY-MM-DD
module: <module-name>
parent: <upstream requirement or contract path>
---
```

### 4.3 Field table

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes, for a single case | Follows `TC-<MODULE>-<nn>` |
| `artifact_type` | string | yes | `test-case` for a single case; `test-cases` for a collection |
| `lifecycle` | enum | yes | `snapshot` for a single case, frozen once stable; `living` for a collection |
| `created_at` | date | yes | The date the case landed |
| `status` | enum | yes, for a single case | `draft` / `active` / `deprecated`; semantics in §4.4 |
| `priority` | enum | yes | `P0` blocks a release / `P1` core path / `P2` edge scenario |
| `test_type` | enum | yes | `functional` / `contract` / `regression` / `non-functional` |
| `covers` | list[string] | yes | The traceability anchors, pointing at an AC, an interface contract or a key scenario; **never empty** |
| `parent` | path | yes | Path to the upstream requirement or interface contract |
| `deprecated_at` | date | conditional | Required when `status: deprecated` |
| `deprecated_reason` | string | conditional | Required when `status: deprecated`, such as "the requirement was dropped" or "replaced by TC-X-NN" |

### 4.4 状态机语义

| Status | Meaning | Entry condition |
|---|---|---|
| `draft` | Being drafted | The case has just landed and has not passed QA review |
| `active` | In force and part of regression | QA review passed; a test execution plan may reference it |
| `deprecated` | Retired | The upstream requirement was dropped, a new case replaced it, or the scenario no longer exists; `deprecated_at` and `deprecated_reason` must be filled in |

**No `executed` or `passed` status is introduced**: execution results belong to the test report, produced per version or build, and do not pollute the case's own lifecycle.

---

## 5. Body structure contract

### 5.1 The 5 required sections

Every test case must contain these 5 body sections.

**H1 title**: `# 用例：<场景一句话描述>`
- At most 80 characters
- Names the subject and the key condition, for example `# 用例：过期 token 访问受保护资源时返回 401`

| # | Section | Purpose | Validation |
|---|---|---|---|
| 1 | Scenario | One line naming the subject under test and its context | At most 120 characters; names the subject, the trigger and the direction of the expectation; a one-line Given-When-Then is recommended |
| 2 | Preconditions | The state that must be in place before execution | As a list, each independently verifiable, covering data state, system state and permission state; where there are none, say so explicitly |
| 3 | Steps | The concrete steps to execute | A numbered list; each step atomic and executable, carrying its input data; at most 10 steps, beyond which the case is split |
| 4 | Expected | The expectation per step, or the final state | Observable and decidable, carrying both positive and negative assertions, with **no** vague words such as "displays normally" or "should be OK" |
| 5 | Coverage | The business promise this case guards | Agrees with the frontmatter `covers`; each entry carries the referenced text, such as "ACME-REQ-15 AC#3: top-3 relevance precision ≥ 80%" |

### 5.2 Optional sections

| Section | When it applies |
|---|---|
| Test data | The data in the steps is complex enough to warrant listing fixtures, mock responses or boundary values separately |
| Teardown | The case has side effects — writing to a database, changing configuration, sending a message — and the cleanup needs stating |
| Notes | Known limitations, interactions with other cases, conditions for skipping |

### 5.3 Collection table format

A collection is best expressed as a table:

```markdown
| Id | Priority | Type | Scenario | Preconditions | Steps | Expected | Covers | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-AUTH-01 | P0 | functional | 过期 token 访问受保护资源 | 用户 token 已过期 ≥ 1 分钟 | 1. GET /api/profile 携带过期 token | 返回 401 + error_code=TOKEN_EXPIRED | ACME-REQ-15#AC3 | active |
```

### 5.4 Traceability semantics

- **One case, several anchors**: a case may cover several ACs where they share preconditions and results, but not ACs across different requirements
- **Several cases, one anchor**: one AC may be covered by several cases at different input boundaries, but each case states which dimension of that AC it covers
- **Broken-link detection**: when an upstream requirement or contract document is deleted or renamed, every `covers` link is validated before the case moves to `deprecated`

---

## 6. Anti-patterns

- ❌ A missing required frontmatter field (`id` / `covers` / `parent` / `priority` / `test_type`)
- ❌ `covers` empty or set to `TBD`; with no anchor the case has no review value
- ❌ A malformed `id`: lower case, missing the MODULE prefix, or a reused number
- ❌ A scenario title missing the subject or the condition, such as "test login"
- ❌ Vague words in the expected result: "normal", "OK", "reasonable", "should"
- ❌ More than 10 steps, which means the case is too coarse and needs splitting
- ❌ Implementation code in the steps; a case takes a black-box view and should not contain `await axios.post(...)`
- ❌ Verifying several independent scenarios at once; one case verifies one kind of condition on one subject
- ❌ A `deprecated` status with no `deprecated_at` or `deprecated_reason`
- ❌ Introducing an execution-state field such as `executed` / `passed` / `failed`; execution results belong to the test report
- ❌ Writing a self-check list into the spec body; review checklists belong to [rules/test-case-quality.md](../rules/test-case-quality.md)
- ❌ Using this spec to describe a code-level test; those belong to [rules/standards-test-code.md](../rules/standards-test-code.md)

---

## 7. Examples

### 7.1 A complete single-case example

````markdown
---
id: TC-KB-12
artifact_type: test-case
lifecycle: snapshot
created_at: 2026-05-20
status: active
priority: P0
test_type: functional
covers:
  - ACME-REQ-15#AC2
  - ACME-REQ-15#AC3
parent: ../requirements/ACME-REQ-15.md
---

# 用例：语义搜索在 10M 数据集上返回 top-3 结果且 p95 ≤ 500ms

## 场景

Given 知识库已向量化 10M 条目，When 客户端 POST /search/semantic 提交典型查询，Then 接口在 500ms 内返回 top-3 结果且相关性 ≥ 80%。

## 前置条件

- 知识库向量化已完成（向量库 `count` API 返回 ≥ 10_000_000）
- API Gateway 已配置 `/search/semantic` 路由
- 测试 API Key 已签发且未触发限流
- 准备 50 条标注好相关性的典型查询数据集（fixture：`fixtures/queries-50.json`）

## 操作步骤

1. 从 fixture 加载 50 条查询，逐条调用 `POST /search/semantic`，body: `{"query": "<text>", "top_k": 3}`
2. 记录每次响应时间 + 返回的 3 条文档 ID
3. 用人工标注的相关性数据计算 top-3 精度
4. 计算所有响应时间的 p95

## 预期结果

- 50 次调用全部 HTTP 200，响应体含 `results` 数组，长度 = 3
- p95 响应时间 ≤ 500ms（满足 AC2 性能指标）
- top-3 相关性精度 ≥ 80%（满足 AC3 精度指标）
- 响应体含 `query_id` 字段（用于追溯）

## 追溯锚

- **ACME-REQ-15 AC#2**：在 10M 条目数据集上响应时间 ≤ 500ms（p95）
- **ACME-REQ-15 AC#3**：top-3 相关性精度 ≥ 80%（50+ 典型查询验证）
````

### 7.2 A collection table example

````markdown
---
artifact_type: test-cases
lifecycle: living
created_at: 2026-05-20
module: AUTH
parent: ../requirements/ACME-REQ-08.md
---

# 测试用例集：认证模块

| Id | Priority | Type | Scenario | Preconditions | Steps | Expected | Covers | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-AUTH-01 | P0 | functional | 过期 token 访问受保护资源 | token 过期 ≥ 1min | GET /api/profile 带过期 token | 401 + TOKEN_EXPIRED | ACME-REQ-08#AC1 | active |
| TC-AUTH-02 | P0 | functional | 无 token 访问受保护资源 | 无 | GET /api/profile 不带 Authorization | 401 + MISSING_TOKEN | ACME-REQ-08#AC1 | active |
| TC-AUTH-03 | P1 | functional | 篡改 token 访问 | 有效 token base64 后改尾字符 | GET /api/profile 带篡改 token | 401 + INVALID_SIGNATURE | ACME-REQ-08#AC2 | active |
| TC-AUTH-04 | P2 | regression | 大小写错误的 Bearer 前缀 | 有效 token | GET /api/profile 带 "bearer xxx"（小写 b） | 401 + MALFORMED_HEADER | ACME-REQ-08#AC4 | active |
````

---

## 8. Relationship to other assets

- **Paired rule**: [rules/test-case-quality.md](../rules/test-case-quality.md) — the quality review checklist for business test case documents, 5 dimensions plus spec compliance. This spec defines the data contract only; every checklist item belongs to the rule.
- **Sibling rule**: [rules/standards-test-code.md](../rules/standards-test-code.md) — coding standards for code-level tests. **They do not overlap**: this spec governs the test case document as an artifact in its own right; that rule governs test code, which is not a document.
- **Upstream spec**: [requirement-modeling.md](./requirement-modeling.md) — `covers` cites the AC IDs of a requirement document in `approved` status, and the case's `parent` points at that document
- **Related asset**: [technical-design-modeling.md](./technical-design-modeling.md) — a `test_type: contract` case may reference an interface contract defined in a technical design document
- **Recursive basis**: this spec itself follows the 8-section skeleton of [spec-modeling.md](./spec-modeling.md) v2.0.0
