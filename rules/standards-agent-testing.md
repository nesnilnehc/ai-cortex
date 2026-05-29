---
artifact_type: rule
name: standards-agent-testing
version: 1.0.0
scope: LLM Agent 行为相关的测试代码与单 agent 测试契约
recommended_scope: user
status: active
---

# Rule: LLM Agent 测试标准 (Agent Testing Standards)

## 适用范围 (Scope)

被测对象为 LLM Agent 行为（依赖模型能力、模型版本、prompt、工具调用、检索上下文的非确定性行为）的测试代码与单 agent 测试契约文档。

本 rule 与 [standards-test-code](./standards-test-code.md) 叠加生效——后者约束通用测试编码标准（AAA、命名三要素、隔离、确定性、Covers 追溯、mock 克制），本 rule 只约束"被测对象是 Agent 行为"带来的增量。确定性代码的测试仍归 standards-test-code。

单 agent 测试契约的数据结构见 [specs/agent-test-modeling.md](../specs/agent-test-modeling.md)；本 rule 约束行为面（断言方式、隔离、回归门禁、追溯）。

---

## 强制约束 (Constraints)

### 1. 确定性与非确定性分流

- **确定性部分**（parser、schema 校验、状态机转移、tool 参数构造、权限判断、错误处理）→ 按 standards-test-code 精确断言，照常 unit 测
- **非确定性部分**（LLM 自然语言输出、模型推理路径）→ 禁止用精确文案做唯一断言；改用 §2 的 oracle

### 2. 测试 oracle 扩展

非确定性行为的断言必须命中以下至少一类 oracle：

- **契约断言**：输出 schema 合法、必填字段存在、字段类型正确
- **轨迹断言**：工具调用序列在允许集合内、禁止调用未出现、写回前置条件满足
- **评估打分**：rubric 评分或 LLM-as-judge，附通过阈值
- **golden dataset**：录制"输入 → 期望输出 / 期望轨迹"对，断言基于语义匹配或字段匹配，而非字符串相等
- **统计回归阈值**：成功率 ≥ 阈值（如 golden 集通过率 ≥ 90%）

### 3. 真实模型测试的标注与隔离

- 命中真实模型 API 的测试必须打 `eval` / `e2e` marker（如 `@pytest.mark.eval`），不进默认 unit 管道
- 默认 unit 管道用 mock LLM 或 recorded response replay，保证确定性与速度
- mock 只用于隔离模型不确定性，**不得** mock 被测 agent 自身的逻辑（意图识别、字段校验、工具选择）

### 4. 模型 / prompt 变更的回归门禁

- 模型版本、prompt 模板、工具定义任一变更 → 必须跑 golden eval 全集
- golden eval 通过率低于契约阈值 → 阻断合并
- 变更需记录 model version comparison（变更前后通过率对比）

### 5. golden dataset 维护

- 每条 golden case 必须含：输入、期望输出 / 期望轨迹、判定方式（字段 / 语义 / rubric）、`Covers` 追溯锚
- golden 集是版本化制品，与 agent 代码同仓；新增能力必须补 golden case
- **不得**为让 eval 通过而删除失败的 golden case——应修 agent，或显式标 `known-failure` + 原因

### 6. 单 agent 测试契约

- 每个对外提供能力的 agent 必须有一份测试契约文档，遵循 [specs/agent-test-modeling.md](../specs/agent-test-modeling.md)
- 测试代码的断言必须可追溯到契约的某条（`Covers` 锚指向契约 ID 或上游 AC）

---

## 违规示例 (Bad Patterns)

```python
# ❌ 对 LLM 自由文本做精确断言
def test_agent_reply():
    reply = agent.handle("我要提个需求")
    assert reply == "您的需求已记录"   # 模型措辞一变即误红
```

```python
# ❌ 真实模型测试无 marker，混进 unit 管道
def test_clarification_flow():
    result = agent.run(real_llm_client, payload)  # CI 慢且 flaky
    assert result.ok
```

```python
# ❌ mock 掉 agent 自身的意图识别逻辑
def test_intent():
    agent.detect_intent = Mock(return_value="create_requirement")
    assert agent.detect_intent("...") == "create_requirement"  # 测了个寂寞
```

```text
# ❌ prompt 改了不跑 golden eval 直接合并
# ❌ agent 无测试契约，测试断言无 Covers 追溯
```

---

## 修正指南 (Remediation)

1. **精确文案断言** → 改契约 / 轨迹 / rubric / golden oracle（§2）
2. **真实模型测试** → 打 `eval` marker；unit 管道换 mock LLM 或 recorded replay（§3）
3. **建立 golden dataset**，prompt / 模型变更挂回归门禁（§4 / §5）
4. **为每个 agent 补测试契约**（[specs/agent-test-modeling.md](../specs/agent-test-modeling.md)），断言加 `Covers` 锚（§6）

---

## 关联资产

- **通用测试编码标准**：[standards-test-code](./standards-test-code.md)（叠加生效；确定性代码测试归此）
- **数据契约**：[specs/agent-test-modeling.md](../specs/agent-test-modeling.md)（单 agent 测试契约结构）
- **执行能力**：[skills/scaffold-agent-tests](../skills/scaffold-agent-tests/SKILL.md)（从 agent 实现 + 契约生成测试套件）
- **术语权威**：[docs/architecture/terminology.md](../docs/architecture/terminology.md)（Rule / Spec / Skill 边界）
