# Rule: 测试用例质量（Test Case Quality）

> 5 维评审清单 + spec 合规检查。每条独立可验证。
>
> 适用于：声明遵循 [specs/test-case-modeling.md](../specs/test-case-modeling.md) 的 QA 业务测试用例文档（单用例与集合表格两种形态）。
>
> **不适用**于代码级测试——代码测试的评审归 [rules/standards-test-code.md](./standards-test-code.md)。

---

## 5 维审查清单

提交评审前，作者应按本清单自检。这些检查点与 5 维审查标准（完整性、可执行性、清晰性、合理性、可追踪性）一一对应。

### 1. 完整性（信息齐全吗？）

- [ ] frontmatter 必填字段齐全（`id` / `artifact_type` / `created_at` / `status` / `priority` / `test_type` / `covers` / `parent`）
- [ ] 5 节正文齐全（场景 / 前置 / 步骤 / 预期 / 追溯锚），集合形态需对应表格列齐全
- [ ] `covers` 字段至少 1 条追溯锚（指向 AC / 接口契约 / 关键场景）
- [ ] `deprecated` 状态用例已填 `deprecated_at` + `deprecated_reason`

### 2. 可执行性（执行者能直接照做吗？）

- [ ] 前置条件每条可独立验证（无"环境正常"等不可验证条款）
- [ ] 步骤编号清晰，每步原子可执行（不含"测试一下"、"检查相关功能"）
- [ ] 步骤含具体输入数据（参数值、payload、用户身份），非"输入合法数据"
- [ ] 步骤数 ≤ 10（超过即过粗，应拆用例）
- [ ] 副作用类用例已含清理步骤或在 Teardown 节说明

### 3. 清晰性（无歧义吗？）

- [ ] 标题含主体 + 关键条件（不是"测试登录"这种泛泛之言）
- [ ] 预期结果**无模糊词**："正常" / "OK" / "合理" / "应该" / "差不多"
- [ ] 预期结果可观察、可判定（HTTP 状态码、字段值、UI 元素出现/消失等）
- [ ] 步骤是**黑盒视角**，不含具体代码实现（如 `await axios.post(...)`）
- [ ] 术语一致，与上游需求 / 契约用词不冲突

### 4. 合理性（这条用例值得存在吗？）

- [ ] 一条用例只验证一个主体的一类条件（不混测多个独立场景）
- [ ] 优先级与场景重要性匹配（P0 限"阻断发布"路径，不滥用）
- [ ] 与现有用例无重复（同一 AC 多条用例时，每条覆盖不同维度——正向 / 边界 / 异常）
- [ ] 用例粒度可在合理时间内执行（手工用例 ≤ 5min / 自动化用例 ≤ 30s）
- [ ] `test_type` 选择正确（functional / contract / regression / non-functional）

### 5. 可追溯性（能定位变更影响吗？）

- [ ] `covers` 字段格式规范（`<req-id>#<AC-n>` 或 `<contract-path>#<endpoint>`）
- [ ] `covers` 引用的 AC / 契约确实存在（无指向已删需求的死链）
- [ ] `parent` 指向上游需求或契约的实际路径
- [ ] 上游需求 `status: approved` 或更高态（不基于 `draft` 需求写正式用例）
- [ ] 反向可查：从需求 AC 能找到至少 1 条覆盖用例（无"裸 AC"）

---

## Spec 合规清单（specs/test-case-modeling.md）

- [ ] frontmatter `artifact_type` 为 `test-case`（单用例）或 `test-cases`（集合）
- [ ] `id` 格式 `TC-<MODULE>-<nn>`（单用例必填；集合内每行同样格式）
- [ ] `lifecycle` 单用例为 `snapshot`，集合为 `living`
- [ ] `status` ∈ `draft` / `active` / `deprecated`
- [ ] `priority` ∈ `P0` / `P1` / `P2`
- [ ] `test_type` ∈ `functional` / `contract` / `regression` / `non-functional`
- [ ] `covers` 非空且每条格式规范
- [ ] **未引入** `executed` / `passed` / `failed` 等执行态字段（执行结果归测试报告）
- [ ] 文件命名遵循 §3：`TC-<MODULE>-<nn>.md`（单用例）或 `test-cases-<module>.md`（集合）

---

## 反模式

- ❌ `covers` 字段为空或填 `TBD`
- ❌ 同一用例覆盖跨需求的 AC（应拆分）
- ❌ 预期结果用模糊词（"显示正常"、"返回合理结果"）
- ❌ 步骤含代码实现（破坏黑盒视角）
- ❌ 一条用例验证多个独立主体
- ❌ 用例进入 `deprecated` 但 frontmatter 未补必填条件字段
- ❌ 用例引用 `draft` 状态需求作为追溯锚
- ❌ 同一模块用例 ≥ 5 条仍用单文件形态（应合并为集合表格）
- ❌ 集合表格内 `id` 格式混用（如 `TC-AUTH-01` 与 `AUTH-002` 同存）
- ❌ 用本 rule 评审代码级测试（代码测试归 [standards-test-code](./standards-test-code.md)）

---

## 关联资产

- **数据契约**：[specs/test-case-modeling.md](../specs/test-case-modeling.md)
- **代码测试编码标准**：[rules/standards-test-code.md](./standards-test-code.md)
- **上游 spec**：[specs/requirement-modeling.md](../specs/requirement-modeling.md)
- **同族评审 rule**：[requirement-quality](./requirement-quality.md) / [design-quality](./design-quality.md) / [task-quality](./task-quality.md)
