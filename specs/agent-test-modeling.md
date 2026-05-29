---
id: AGENT_TEST_MODELING_SPEC_V1
name: Agent Test Contract Modeling Schema
description: Spec defining the per-agent test contract document — capability boundary, input contract, tool boundary, write-back preconditions, oracles, golden cases, and pass threshold. Governs the contract document; test code conventions are governed by rules/standards-agent-testing.md.
version: 1.0.0
status: active
lifecycle: living
created_at: 2026-05-29
scope: |
  Defines the structural contract for a single LLM Agent's test contract document —
  the noun that declares what the agent must accept, must reject, how correctness is
  judged, and which upstream promise it guards. Does NOT cover test code conventions
  (assertion style, mocking, regression gates) — those are governed by
  rules/standards-agent-testing.md. Does NOT cover QA business test cases (governed by
  test-case-modeling.md) or code-level test coding (governed by standards-test-code.md).
related:
  - ./spec-modeling.md
  - ./test-case-modeling.md
  - ../rules/standards-agent-testing.md
  - ../rules/standards-test-code.md
---

# Agent 测试契约建模规范

> **数据契约**：定义单个 LLM Agent 的测试契约文档的字段结构与正文骨架

---

## 1. 定位与适用范围

Agent 测试契约（agent test contract）回答"这个 agent 必须接受什么、必须拒绝什么、怎么算对、守护哪条承诺"——它是单个 LLM Agent 的可验证行为契约，是测试代码断言的追溯源。

适用：

- 对外提供能力的 LLM Agent（如需求澄清 agent、代码审查 agent）的测试契约

不适用：

- **测试代码编码方式**（断言 oracle、mock 隔离、回归门禁）——归 [rules/standards-agent-testing.md](../rules/standards-agent-testing.md)
- **QA 业务测试用例文档**——归 [test-case-modeling.md](./test-case-modeling.md)
- **代码级测试编码标准**——归 [standards-test-code.md](../rules/standards-test-code.md)

具体存放路径由各项目治理决定（典型：`docs/agent-tests/` 或与 agent 实现同目录）。

---

## 2. 心智模型（Mental Model）

> 一份合格 agent 测试契约要回答的核心问题。

每份契约必须能回答 **3 问 + 1 锚**：

| 维度 | 核心问题 | 落地章节 |
|---|---|---|
| **输入契约（Accept）** | agent 必须接受什么？缺字段如何识别？ | §5 输入契约 |
| **行为边界（Reject）** | agent 必须拒绝什么？允许 / 禁止调用什么工具？ | §5 工具调用边界 + 写回前置 |
| **判定（Judge）** | 怎么算对？用哪类 oracle？阈值多少？ | §5 判定方式 + golden cases |
| **追溯锚（Trace）** | 守护哪条业务承诺？ | `covers` |

缺任一即视为不合格契约——测试代码无法定位"为何这样断言"。

---

## 3. 命名约定

```
agent-test-<agent-slug>.md
```

- `<agent-slug>`：agent 标识（kebab-case，与 agent 实现命名对齐，如 `clarification` / `code-review`）
- 示例：`agent-test-clarification.md`
- 契约 ID（frontmatter `id`）格式 `ATC-<AGENT>`（大写，如 `ATC-CLARIFICATION`）

---

## 4. Frontmatter 契约

```yaml
---
id: ATC-<AGENT>
artifact_type: agent-test-contract
lifecycle: living
created_at: YYYY-MM-DD
status: draft | active | deprecated
agent_ref: <agent 实现的相对路径>
model_baseline: <golden 集录制时的模型 id / 版本>
pass_threshold: <golden 集通过率阈值，如 0.9>
covers:
  - <requirement-id>#<AC-n>
parent: <上游需求或设计文档路径>
# 条件字段
deprecated_at: YYYY-MM-DD          # status: deprecated 时必填
deprecated_reason: <原因>           # status: deprecated 时必填
---
```

### 4.1 字段表

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | string | 必 | 格式 `ATC-<AGENT>` |
| `artifact_type` | string | 必 | 固定 `agent-test-contract` |
| `lifecycle` | enum | 必 | 固定 `living`（契约随 agent 能力演化） |
| `created_at` | date | 必 | 契约落地日期 |
| `status` | enum | 必 | `draft` / `active` / `deprecated`（语义见 §4.2） |
| `agent_ref` | path | 必 | 被测 agent 实现的相对路径 |
| `model_baseline` | string | 必 | golden 集录制依据的模型 id / 版本（回归对比基线） |
| `pass_threshold` | number | 必 | golden 集通过率阈值（0–1） |
| `covers` | list[string] | 必 | 追溯锚列表，指向上游 AC；**禁空** |
| `parent` | path | 必 | 上游需求或设计文档路径 |
| `deprecated_at` | date | 条件 | `status: deprecated` 时必填 |
| `deprecated_reason` | string | 条件 | `status: deprecated` 时必填 |

### 4.2 状态机语义

| 状态 | 含义 | 转入条件 |
|---|---|---|
| `draft` | 起草中 | 契约首次落地，golden 集未稳定 |
| `active` | 已生效 | golden 集稳定，回归门禁已挂接 |
| `deprecated` | 已废弃 | agent 下线 / 能力合并（需填 `deprecated_at` + `deprecated_reason`） |

---

## 5. 正文结构契约

### 5.1 必填章节（7 节）

**H1 标题**：`# Agent 测试契约：<agent 名>`

| # | 章节 | 用途 | 校验 |
|---|---|---|---|
| 1 | 能力边界（Capability Boundary） | agent 做什么 / 不做什么 | 清单形式；正负各 ≥ 1 条 |
| 2 | 输入契约（Input Contract） | 必填输入字段 + 缺失字段识别规则 | 每字段含名称 / 类型 / 必填性 / 缺失时的预期行为 |
| 3 | 工具调用边界（Tool Boundary） | 允许 / 禁止的工具集 | 允许集与禁止集均显式列出；禁止集非空时每条附理由 |
| 4 | 写回前置（Write-back Preconditions） | 产生副作用前必须满足的条件 | 每条可独立验证；无副作用的 agent 显式写"无写回" |
| 5 | 判定方式（Oracles） | 各类行为用哪种 oracle | 每类行为映射到 [standards-agent-testing §2](../rules/standards-agent-testing.md) 的 oracle 类型 |
| 6 | Golden Cases | 输入 → 期望 表格 | 每行含输入 / 期望 / 判定方式 / Covers；正向 + 边界 + 异常各 ≥ 1 |
| 7 | 通过阈值与追溯锚（Threshold & Coverage） | golden 通过率阈值 + 守护的业务承诺 | 阈值与 frontmatter `pass_threshold` 一致；`covers` 引用文本可定位 |

### 5.2 Golden Cases 表格格式

```markdown
| Case | 输入 | 期望（输出 / 轨迹） | 判定方式 | Covers |
| :--- | :--- | :--- | :--- | :--- |
```

- **判定方式**取值：`字段` / `语义` / `轨迹` / `rubric` / `统计`（对应 standards-agent-testing §2 oracle 类型）

### 5.3 校验集中

所有正文章节的结构校验集中在 §5；§6 反模式只列违规形态，不重复定义规则。

---

## 6. 反模式

- ❌ 缺 frontmatter 必填字段（`id` / `agent_ref` / `model_baseline` / `pass_threshold` / `covers`）
- ❌ `covers` 为空或写 `TBD`（无追溯锚 = 测试断言无源）
- ❌ 工具调用边界只列允许集、不列禁止集（无法验证"禁止调用未出现"）
- ❌ Golden Cases 只堆正向用例，缺边界与异常
- ❌ 判定方式写"检查结果正常"等模糊词（应映射到具体 oracle 类型）
- ❌ `pass_threshold` 与正文 §7 阈值不一致
- ❌ 把测试代码的断言写法塞进契约（编码方式归 [standards-agent-testing](../rules/standards-agent-testing.md)）
- ❌ 一份契约覆盖多个 agent（应一 agent 一契约）
- ❌ `deprecated` 状态未填 `deprecated_at` / `deprecated_reason`

---

## 7. 示例

````markdown
---
id: ATC-CLARIFICATION
artifact_type: agent-test-contract
lifecycle: living
created_at: 2026-05-29
status: active
agent_ref: ../src/agents/clarification.py
model_baseline: claude-sonnet-4-6
pass_threshold: 0.9
covers:
  - ACME-REQ-08#AC1
  - ACME-REQ-08#AC3
parent: ../requirements/ACME-REQ-08.md
---

# Agent 测试契约：需求澄清

## 能力边界

- 做：从自由文本识别需求要素，缺字段时按流程追问
- 不做：信息不足时禁止写回需求系统

## 输入契约

| 字段 | 类型 | 必填 | 缺失时预期行为 |
|---|---|---|---|
| title | string | 是 | 追问标题，不写回 |
| acceptance | list | 是 | 追问验收标准，不写回 |

## 工具调用边界

- 允许：`search_requirements`、`ask_user`
- 禁止：`write_requirement`（写回前置未满足时）——防止信息不足时落库

## 写回前置

- 全部必填字段已收集且通过完整性校验

## 判定方式

| 行为 | oracle 类型 |
|---|---|
| 缺字段识别 | 轨迹（断言触发 ask_user，未触发 write_requirement） |
| 完整需求写回 | 契约（写回 payload schema 合法） |
| 追问话术质量 | rubric（清晰度评分 ≥ 4/5） |

## Golden Cases

| Case | 输入 | 期望（输出 / 轨迹） | 判定方式 | Covers |
| :--- | :--- | :--- | :--- | :--- |
| 缺验收标准 | "做个登录功能" | 触发 ask_user 追问验收；不触发 write_requirement | 轨迹 | ACME-REQ-08#AC1 |
| 信息完整 | 含标题 + 3 条验收的描述 | 触发 write_requirement，payload schema 合法 | 契约 | ACME-REQ-08#AC3 |
| 空输入 | "" | 返回引导提示；不触发任何工具 | 轨迹 | ACME-REQ-08#AC1 |

## 通过阈值与追溯锚

- golden 集通过率 ≥ 0.9（与 `pass_threshold` 一致）
- **ACME-REQ-08 AC#1**：信息不足时禁止写回
- **ACME-REQ-08 AC#3**：完整需求写回 payload 合法
````

---

## 8. 与其他资产关系

- **配套 rule**：[rules/standards-agent-testing.md](../rules/standards-agent-testing.md)——agent 测试代码的红线与方法论约束（断言 oracle、隔离、回归门禁）。本 spec 只定义契约结构，编码方式归 rule。
- **执行能力**：[skills/scaffold-agent-tests](../skills/scaffold-agent-tests/SKILL.md)——读本 spec 的契约实例 + agent 实现，生成测试套件。
- **同族 spec**：[test-case-modeling.md](./test-case-modeling.md)——QA 业务测试用例文档。**与之互不重叠**：本 spec 管单 agent 的行为契约，该 spec 管黑盒业务用例。
- **上游 spec**：[requirement-modeling.md](./requirement-modeling.md)——`covers` 引用需求 AC ID。
- **递归基础**：本 spec 自身遵循 [spec-modeling.md](./spec-modeling.md) v2.0.0 的 8 节骨架。
