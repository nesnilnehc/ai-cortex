---
id: TEST_CASE_MODELING_SPEC_V1
name: Test Case Modeling Schema
description: Spec defining QA business test case document fields, naming, body sections, traceability to requirements/acceptance criteria, and execution status semantics. Scope limited to document artifacts; code-level test code is governed by rules/standards-test-code.md.
version: 1.0.0
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
  - ./design-modeling.md
  - ../rules/test-case-quality.md
  - ../rules/standards-test-code.md
---

# 测试用例建模规范

> **数据契约**：定义 QA 业务测试用例文档的字段结构与正文骨架

---

## 1. 定位与适用范围

测试用例文档（test case document）回答"在什么前提下、做什么操作、期望看到什么结果"——它是 QA 体系下从需求验收标准、接口契约或关键场景清单派生的可执行黑盒验证记录。

适用：

- **QA 业务测试用例**：从 `approved` 状态的需求文档派生，验证 AC 是否被产品满足
- **接口契约验证用例**：基于上游接口契约（如 `*-contract.md`）派生的契约级用例
- **关键场景回归用例**：业务关键路径的回归测试集合

不适用：

- **代码级测试**（unit / integration / E2E in code）——测试函数本身即制品，无独立文档；由 [`rules/standards-test-code.md`](../rules/standards-test-code.md) 约束
- **探索性测试笔记**——非结构化探索过程，不需要数据契约
- **性能压测脚本**——由专门工具与脚本承载，本 spec 不覆盖

---

## 2. 心智模型（Mental Model）

> 一份合格测试用例要回答的核心问题。

每个测试用例必须能回答 **3 问 + 1 锚**：

| 维度 | 核心问题 | 落地字段 |
|---|---|---|
| **主体（Subject）** | 在测什么对象 / 流程？ | `scenario` |
| **条件（Condition）** | 在什么前置与触发下？ | `preconditions` + `steps` |
| **期望（Expected）** | 预期看到什么结果？ | `expected` |
| **追溯锚（Trace）** | 这条用例守护哪条业务承诺？ | `covers`（指向 AC / 接口契约 / 场景） |

缺任一即视为不合格用例——下游评审无法定位"为何要这条用例"。

---

## 3. 命名约定

### 3.1 单用例文档形态

```
TC-<MODULE>-<nn>.md
```

- `<MODULE>`：所属模块缩写（大写，2-6 字符，如 `AUTH` / `PAY` / `KB`）
- `<nn>`：模块内顺序号，2 位起步，单调递增，**不复用**
- 示例：`TC-AUTH-05.md` / `TC-PAY-042.md`
- 存放位置由项目治理决定（典型：`docs/test-cases/`）

### 3.2 集合表格形态

当同一模块用例 ≥ 5 条时，推荐合并为表格集合：

```
test-cases-<module>.md
```

- 示例：`test-cases-auth.md`
- 表格每行一条用例，字段同 §5.1
- 集合内 `id` 仍遵循 `TC-<MODULE>-<nn>` 格式

---

## 4. Frontmatter 契约

### 4.1 单用例文档 frontmatter

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
# 条件字段
deprecated_at: YYYY-MM-DD          # status: deprecated 时必填
deprecated_reason: <原因>           # status: deprecated 时必填
---
```

### 4.2 集合表格 frontmatter

```yaml
---
artifact_type: test-cases
lifecycle: living
created_at: YYYY-MM-DD
module: <module-name>
parent: <upstream requirement or contract path>
---
```

### 4.3 字段表

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | string | 必（单用例） | 格式 `TC-<MODULE>-<nn>` |
| `artifact_type` | string | 必 | 单用例 `test-case`；集合 `test-cases` |
| `lifecycle` | enum | 必 | 单用例 `snapshot`（用例稳定后冻结）；集合 `living` |
| `created_at` | date | 必 | 用例落地日期 |
| `status` | enum | 必（单用例） | `draft` / `active` / `deprecated`（语义见 §4.4） |
| `priority` | enum | 必 | `P0`（阻断发布）/ `P1`（核心路径）/ `P2`（边缘场景） |
| `test_type` | enum | 必 | `functional` / `contract` / `regression` / `non-functional` |
| `covers` | list[string] | 必 | 追溯锚列表；指向 AC / 接口契约 / 关键场景；**禁空** |
| `parent` | path | 必 | 上游需求或接口契约路径 |
| `deprecated_at` | date | 条件 | `status: deprecated` 时必填 |
| `deprecated_reason` | string | 条件 | `status: deprecated` 时必填（"需求废弃" / "被 TC-X-NN 替代"等） |

### 4.4 状态机语义

| 状态 | 含义 | 转入条件 |
|---|---|---|
| `draft` | 起草中 | 用例首次落地，尚未通过 QA 评审 |
| `active` | 已生效，纳入回归 | QA 评审通过，可被测试执行计划引用 |
| `deprecated` | 已废弃 | 上游需求废弃 / 被新用例替代 / 场景不再存在（需填 `deprecated_at` + `deprecated_reason`） |

**不引入 `executed` / `passed` 状态**：执行结果是测试报告的职责（按版本/构建产出），不污染用例自身生命周期。

---

## 5. 正文结构契约

### 5.1 必填章节（5 节）

每条测试用例必须包含以下 5 节正文。

**H1 标题**：`# 用例：<场景一句话描述>`
- 标题 ≤ 80 字符
- 含主体 + 关键条件（如 `# 用例：过期 token 访问受保护资源时返回 401`）

| # | 章节 | 用途 | 校验 |
|---|---|---|---|
| 1 | 场景（Scenario） | 一句话描述被测主体 + 上下文 | ≤ 120 字符；含主体 / 触发 / 预期方向；推荐 Given-When-Then 一行式 |
| 2 | 前置条件（Preconditions） | 执行前必须就位的状态 | 清单形式；每条可独立验证；含数据状态、系统状态、权限状态；无前置时显式写"无前置条件" |
| 3 | 操作步骤（Steps） | 具体执行步骤 | 编号清单；每步原子可执行；含输入数据；步骤数 ≤ 10（超过则拆用例） |
| 4 | 预期结果（Expected） | 每步对应或终态期望 | 可观察、可判定；含正向断言与负向断言；**无**模糊词（"正常显示" / "应该 OK"） |
| 5 | 追溯锚（Coverage） | 本用例守护的业务承诺 | 与 frontmatter `covers` 一致；每条含引用文本（如 "ACME-REQ-15 AC#3：top-3 相关性精度 ≥ 80%"） |

### 5.2 可选章节

| 章节 | 触发场景 |
|---|---|
| 测试数据（Test Data） | 步骤中数据较复杂，需独立列出 fixture / mock 响应 / 边界值 |
| 清理步骤（Teardown） | 用例产生副作用（写库 / 改配置 / 发消息），需说明清理动作 |
| 备注（Notes） | 已知限制、与其他用例的交互、跳过条件 |

### 5.3 集合表格格式

集合形态推荐表格：

```markdown
| Id | Priority | Type | Scenario | Preconditions | Steps | Expected | Covers | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-AUTH-01 | P0 | functional | 过期 token 访问受保护资源 | 用户 token 已过期 ≥ 1 分钟 | 1. GET /api/profile 携带过期 token | 返回 401 + error_code=TOKEN_EXPIRED | ACME-REQ-15#AC3 | active |
```

### 5.4 追溯语义

- **单用例 ↔ 多锚**：一条用例可覆盖多个 AC（共同前置 + 共同结果时），但**不应**覆盖跨需求的 AC
- **多用例 ↔ 单锚**：一条 AC 可被多条用例覆盖（不同输入边界），但每条用例应明确"覆盖该 AC 的哪个维度"
- **追溯断链检测**：上游需求 / 契约文档被删除或重命名时，本用例进入 `deprecated` 状态前需校验所有 `covers` 链接有效

---

## 6. 反模式

- ❌ 缺 frontmatter 必填字段（`id` / `covers` / `parent` / `priority` / `test_type`）
- ❌ `covers` 字段为空或写 `TBD`（无追溯锚 = 无评审价值）
- ❌ `id` 格式不规范（小写、缺 MODULE 前缀、复用编号）
- ❌ 场景标题缺主体或缺条件（如 "测试登录"）
- ❌ 预期结果含模糊词（"正常" / "OK" / "合理" / "应该"）
- ❌ 步骤 > 10 条（说明用例粒度过粗，应拆分）
- ❌ 步骤含具体代码实现（用例是黑盒视角，不该含 `await axios.post(...)`）
- ❌ 同时验证多个独立场景（单条用例只验证一个主体的一类条件）
- ❌ `deprecated` 状态未填 `deprecated_at` 或 `deprecated_reason`
- ❌ 引入 `executed` / `passed` / `failed` 等执行态字段（执行结果归测试报告）
- ❌ 把"自检清单"写进 spec 正文（评审清单归 [rules/test-case-quality.md](../rules/test-case-quality.md)）
- ❌ 用本 spec 描述代码级测试（代码测试归 [rules/standards-test-code.md](../rules/standards-test-code.md)）

---

## 7. 示例

### 7.1 单用例完整示例

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

### 7.2 集合表格示例

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

## 8. 与其他资产关系

- **配套 rule**：[rules/test-case-quality.md](../rules/test-case-quality.md)——业务测试用例文档质量评审清单（5 维 + spec 合规）。本 spec 只定义数据契约，评审清单全部归 rule。
- **同族 rule**：[rules/standards-test-code.md](../rules/standards-test-code.md)——代码级测试的编码标准。**本 spec 与之互不重叠**：本 spec 管"测试用例文档"这一独立制品；该 rule 管"测试代码"这一非文档制品。
- **上游 spec**：[requirement-modeling.md](./requirement-modeling.md)——`covers` 字段引用 `approved` 状态需求文档的 AC ID；用例的 `parent` 指向需求文档路径
- **关联资产**：[design-modeling.md](./design-modeling.md)——`test_type: contract` 类用例可引用设计文档中定义的接口契约
- **递归基础**：本 spec 自身遵循 [spec-modeling.md](./spec-modeling.md) v2.0.0 的 8 节骨架
