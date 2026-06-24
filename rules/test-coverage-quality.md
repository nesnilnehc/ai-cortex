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

# Rule: 测试覆盖评估报告质量（Test Coverage Report Quality）

> 5 维评审清单 + spec 合规检查。每条独立可验证。
>
> 适用于：声明遵循 [specs/test-coverage-modeling.md](../specs/test-coverage-modeling.md) 的测试覆盖评估报告（用例集覆盖评审与跨制品对齐评审的输入制品）。
>
> 本 rule 不评审单条用例（归 [test-case-quality](./test-case-quality.md)），也不评审测试代码（归 [standards-test-code](./standards-test-code.md)）。

---

## 5 维审查清单

### 1. 完整性（信息齐全吗？）

- [ ] frontmatter 必填字段齐全（`artifact_type` / `scope` / `trigger` / `covers_artifacts` / `test_case_sources` / `tool_provenance` / `verdict`）
- [ ] 4 节正文齐全（评估摘要 / 追溯矩阵 / 变异测试概要 / 追溯健康审计）
- [ ] 评估摘要含三项关键指标（AC 覆盖率 / mutation score / 死链数）
- [ ] `verdict: conditional` 报告已填 `conditional_reasons`

### 2. 真实性（数据可信吗？）

- [ ] `tool_provenance` 列出实际产出工具与版本（非空、非占位）
- [ ] mutation score 来自实际工具运行；若未集成必须显式标"未执行 — <原因>"，verdict ≤ `conditional`
- [ ] 追溯矩阵单元格来自 `covers` 字段聚合，非人工填写
- [ ] 报告生成日期与所引用工具运行日期一致（避免使用过期数据冒充新评估）

### 3. 可解释性（缺口与豁免有交代吗？）

- [ ] 追溯矩阵每行至少 1 个 `✓` 或全行标 `—` 并附"不适用"理由
- [ ] 缺口（行为空）已列入"缺口清单"，含补救动作 + 责任方 + 截止日
- [ ] 变异 `fail` 行附"存活变异详情"子节，推断缺测维度
- [ ] `waived` 状态附豁免原因（非"暂时跳过"这种空话）

### 4. 风险匹配（缺口严重度与 verdict 一致吗？）

- [ ] 关键 AC（P0 需求 / 安全相关 / 契约接口）未覆盖 → verdict = `fail`
- [ ] 关键路径变异存活（`survived_critical > 0`）→ verdict ≥ `conditional`
- [ ] 死链或悬空守护非零 → verdict ≥ `conditional`
- [ ] verdict 与正文不矛盾（pass 报告正文无 blocker；fail 报告正文有明确 blocker）
- [ ] 缺口的优先级标注与上游需求 `priority` 一致（P0 需求缺口不可与 P2 需求缺口同等对待）

### 5. 时效与可追溯性（评估对得上当下状态吗？）

- [ ] `covers_artifacts` 引用的上游路径有效（无 404）
- [ ] `test_case_sources` 引用的用例文档 / 代码目录存在
- [ ] 报告 `created_at` 距 `trigger` 事件 ≤ 7 天（否则视为过期评估）
- [ ] 死链清单与"上游制品当前状态"一致（无"已修复但报告未更新"项）
- [ ] 与上一份同 `scope` 报告可对比（趋势可追溯）

---

## Spec 合规清单（specs/test-coverage-modeling.md）

- [ ] frontmatter `artifact_type: test-coverage-report`
- [ ] `lifecycle: snapshot`
- [ ] `trigger` ∈ `release-gate` / `quarterly-audit` / `requirement-change` / `contract-upgrade`
- [ ] `verdict` ∈ `pass` / `fail` / `conditional`
- [ ] 文件命名遵循 `coverage-report-<scope>-<YYYY-MM-DD>.md`
- [ ] 追溯矩阵行键格式 `<REQ-ID>#AC<n> · <维度>`
- [ ] 变异概要每行含 7 个必填字段（module / total / killed / score / survived_critical / threshold / status）
- [ ] 追溯健康审计含 3 张独立表（死链 / 裸 AC / 悬空守护），未合并

---

## 反模式

- ❌ verdict 与正文矛盾（pass 报告含未豁免空行 / fail 报告无 blocker 解释）
- ❌ mutation score 无工具产出却给出数字
- ❌ 用 line coverage 冒充充分性证据
- ❌ 缺口清单只列问题不列补救动作 / 责任方
- ❌ 死链 / 裸 AC / 悬空守护合并为一张表
- ❌ snapshot 报告生成后修改正文（应新建报告 + CHANGELOG）
- ❌ trigger 选择不当（用 release-gate 跑日常 PR 评审，制造噪音）
- ❌ 把单用例 5 维评审塞进本报告（不同评审类型不混评）
- ❌ 上一份报告的缺口在新报告中未被跟踪（无趋势对比）
- ❌ `tool_provenance` 留空或填"various"（不可复现）

---

## 与上游 rule 的边界

| 评审对象 | 归属 rule | 触发场景 |
|---|---|---|
| 单条业务测试用例 | [test-case-quality](./test-case-quality.md) | 单用例 PR / 用例新增 |
| 测试代码（编码标准） | [standards-test-code](./standards-test-code.md) | 测试代码 PR |
| 用例集对需求的覆盖评估报告 | **本 rule** | 发布门禁 / 季度审计 / 上游变更影响 |
| 文档链接图与制品健康 | [doc-health-criteria](./doc-health-criteria.md) | 全局文档审计 |

---

## 关联资产

- **数据契约**：[specs/test-coverage-modeling.md](../specs/test-coverage-modeling.md)
- **数据来源**：[specs/test-case-modeling.md](../specs/test-case-modeling.md) 的 `covers` 字段、`requirement-modeling` 的 AC ID
- **同族评审 rule**：[test-case-quality](./test-case-quality.md) / [standards-test-code](./standards-test-code.md) / [doc-health-criteria](./doc-health-criteria.md)
