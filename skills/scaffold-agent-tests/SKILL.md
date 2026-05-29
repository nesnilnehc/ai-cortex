---
name: scaffold-agent-tests
description: Generate an LLM agent test suite (golden cases, mock-LLM unit tests, evaluator harness) from an agent implementation and its agent-test contract. Use when an agent has no tests, or a contract exists but the test code is missing.
description_zh: 从 agent 实现与测试契约生成测试套件（golden cases、mock LLM 单测、evaluator）；用于 agent 缺测试或契约已有但测试代码缺失时。
tags: [testing, automation]
version: 1.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [scaffold agent tests, generate agent tests, author agent tests, agent test suite]
compatibility: Requires the agent implementation source and a test contract (specs/agent-test-modeling.md instance); a shell and the repo's test toolchain.
input_schema:
  type: code-scope
  description: Path to an agent implementation plus its agent-test contract document
  defaults:
    scope: file
output_schema:
  type: code-artifact
  description: Generated test files (mock-LLM unit tests, golden dataset, evaluator harness) traceable to the contract
---

# 技能 (Skill)：生成 Agent 测试套件

## 目的 (Purpose)

读取一个 LLM Agent 的实现与其测试契约（[specs/agent-test-modeling.md](../../specs/agent-test-modeling.md) 实例），生成可追溯到契约的测试套件——确定性部分的精确断言、非确定性部分的 oracle 测试、golden dataset 与 evaluator harness。

---

## 核心目标（Core Objective）

**首要目标**：产出一套遵循 [rules/standards-agent-testing.md](../../rules/standards-agent-testing.md) 的 agent 测试代码，每条断言可追溯到契约的某条。

**成功标准**（必须全部满足）：

1. ✅ **契约已定位**：读取 agent 实现 + `agent-test-contract` 文档
2. ✅ **测试矩阵已生成**：能力边界 / 输入契约 / 工具边界 / 写回前置逐项映射到测试
3. ✅ **oracle 选型正确**：确定性行为用精确断言；非确定性行为用契约 / 轨迹 / rubric / golden oracle
4. ✅ **golden dataset 已落盘**：正向 + 边界 + 异常各 ≥ 1，含 `Covers` 追溯锚
5. ✅ **真实模型测试已隔离**：命中真实模型的测试打 `eval` marker，unit 管道用 mock LLM
6. ✅ **可追溯**：每个测试的 `Covers` 指向契约 ID 或上游 AC

**验收测试**：开发者能否在不读 agent 源码的情况下，仅凭生成的测试 + 契约理解每条测试守护什么？

---

## 范围边界 (Scope Boundaries)

**本技能负责**：

- 读 agent 实现 + 测试契约，生成测试矩阵
- 生成 mock LLM 单测、golden dataset、evaluator harness
- 为非确定性行为选 oracle、为确定性行为写精确断言
- 为每个测试挂 `Covers` 追溯锚

**本技能不负责**：

- **运行测试** → 用 [automate-tests](../automate-tests/SKILL.md)
- **评审测试质量 / 覆盖** → 用 [review-testing](../review-testing/SKILL.md)
- **编写测试契约文档** → 契约由人按 [specs/agent-test-modeling.md](../../specs/agent-test-modeling.md) 撰写；本技能消费契约，不创作契约
- **修复失败测试 / 调试 agent** → 用 [orchestrate-repair-loop](../orchestrate-repair-loop/SKILL.md)

**转交点**：测试生成完毕 → 交 automate-tests 运行、review-testing 评审。

---

## 前置条件

- agent 实现源码可读
- 存在遵循 [specs/agent-test-modeling.md](../../specs/agent-test-modeling.md) 的测试契约；**缺失时**先提示用户按该 spec 撰写契约，不自行编造能力边界

---

## 执行流程

### 1. 定位契约与实现

- 读 `agent-test-contract` 文档（frontmatter `agent_ref` 指向实现）
- 契约缺失 → 终止并提示：先按 [specs/agent-test-modeling.md](../../specs/agent-test-modeling.md) 撰写契约

### 2. 生成测试矩阵

将契约各章节映射为测试条目：

| 契约章节 | 测试类型 | oracle |
|---|---|---|
| 能力边界 | 正向 + 反向行为测试 | 轨迹 / 契约 |
| 输入契约（缺字段识别） | 边界 + 异常测试 | 轨迹（断言追问、不写回） |
| 工具调用边界 | 轨迹测试 | 轨迹（禁止集未出现） |
| 写回前置 | 前置不满足时的拒绝测试 | 轨迹 |
| Golden Cases | 回归测试集 | 按契约判定方式列 |

### 3. 选 oracle 并写测试

- **确定性逻辑**（schema 校验、tool 参数、权限）→ 精确断言（遵循 [standards-test-code](../../rules/standards-test-code.md) AAA + 命名三要素）
- **非确定性输出** → 契约 / 轨迹 / rubric / golden oracle（遵循 [standards-agent-testing §2](../../rules/standards-agent-testing.md)）
- unit 管道用 mock LLM / recorded replay；真实模型测试打 `eval` marker

### 4. 落 golden dataset

- 从契约 Golden Cases 表生成版本化 golden 数据文件
- 每条含输入 / 期望 / 判定方式 / `Covers`

### 5. 生成 evaluator harness

- 对 rubric / 语义 / 统计类判定，生成 evaluator（LLM-as-judge 或语义匹配器）
- 输出 golden 集通过率，对比契约 `pass_threshold`

### 6. 汇总

- 列出生成的文件、各测试的 `Covers`、unit vs eval 分层
- 提示后续：automate-tests 运行、review-testing 评审

---

## 限制 (Limitations)

### 硬边界（Hard Boundaries）

- 契约缺失时不编造 agent 能力边界（先要契约）
- 不 mock 被测 agent 自身逻辑（仅 mock 模型不确定性）
- 不为通过 eval 而弱化断言或删 golden case
- 不运行测试、不修改 agent 实现（仅生成测试制品）

### 技能边界（避免重叠）

- **运行测试** → [automate-tests](../automate-tests/SKILL.md)
- **评审测试质量** → [review-testing](../review-testing/SKILL.md)
- **调试 / 修复** → [orchestrate-repair-loop](../orchestrate-repair-loop/SKILL.md)

---

## 自检 (Self-Check)

- [ ] 读取了 agent 实现 + 测试契约
- [ ] 测试矩阵覆盖契约全部章节（能力边界 / 输入 / 工具 / 写回 / golden）
- [ ] 确定性用精确断言，非确定性用 oracle
- [ ] golden 集含正向 + 边界 + 异常，每条有 `Covers`
- [ ] 真实模型测试打 `eval` marker，unit 用 mock LLM
- [ ] 每个测试可追溯到契约或上游 AC

---

## 示例 (Examples)

### 示例：需求澄清 agent

用户："为 clarification agent 生成测试。"

代理：

1. 读 `agent-test-clarification.md`（契约）+ `src/agents/clarification.py`
2. 生成矩阵：缺字段识别（轨迹）、完整写回（契约）、空输入（轨迹）、禁止工具（轨迹）
3. 写测试：
   - unit：mock LLM 返回 recorded response，断言触发 `ask_user` 不触发 `write_requirement`
   - eval（打 marker）：真实模型跑 golden 集，rubric 评追问话术清晰度
4. 落 `golden/clarification.jsonl`（3 条：缺验收 / 信息完整 / 空输入）
5. 生成 evaluator：计算 golden 通过率，对比 `pass_threshold: 0.9`
6. 汇总：4 个 unit + 1 个 eval 套件，各挂 `Covers: ACME-REQ-08#AC1/AC3`；提示 automate-tests 运行
