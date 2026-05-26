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

# 测试覆盖评估报告建模规范

> **数据契约**：定义测试覆盖评估报告的字段结构与正文骨架

---

## 1. 定位与适用范围

测试覆盖评估报告（test coverage report）是**用例集覆盖评审**与**跨制品对齐评审**的输入制品——它把"用例集对需求/方案的充分性 + 必要性 + 追溯闭环"的判断证据，固化为可评审、可对比、可归档的快照。

| 评审类型 | 关注问题 | 本报告对应章节 |
|---|---|---|
| 单用例评审 | 单条用例本身立得住吗？ | **不在本报告范围**（归 [rules/test-case-quality.md](../rules/test-case-quality.md)） |
| 用例集覆盖评审 | 用例集对需求充分且必要吗？ | §5.2 追溯矩阵 + §5.3 变异测试概要 |
| 跨制品对齐评审 | 用例集与上游需求/契约的链路完整吗？ | §5.4 追溯健康审计 |

适用：

- **发布门禁**：发版前对当前用例集做一次覆盖快照
- **季度回归集治理**：周期性审视用例集冗余与缺口
- **需求/契约/ADR 变更影响评估**：上游变更后用快照前后对比判断影响
- **跨团队契约对接评审**：契约升级时输出覆盖证据

不适用：

- **单条用例评审**（归 [rules/test-case-quality.md](../rules/test-case-quality.md)）
- **测试执行报告**（pass/fail/duration 等运行结果，由 CI 报告承载）
- **代码覆盖率原始数据**（line/branch coverage，由覆盖工具直接产出，本制品只引用其结论）

---

## 2. 心智模型（Mental Model）

> 一份合格覆盖报告要回答的核心问题。

每份报告必须能回答 **3 问**：

| 维度 | 核心问题 | 落地章节 |
|---|---|---|
| **充分性（Sufficiency）** | 覆盖到位了吗？哪里有空白？ | §5.2 追溯矩阵 |
| **必要性（Necessity）** | 用例冗余多少？哪些可剪？ | §5.3 变异测试概要 |
| **追溯闭环（Trace Health）** | 用例与上游制品的链路是否完整有效？ | §5.4 追溯健康审计 |

任一问题无答案，报告即不合格——评审无法据此做发布/治理决策。

---

## 3. 命名约定

```
coverage-report-<scope>-<YYYY-MM-DD>.md
```

- `<scope>`：覆盖评估范围标识（推荐 `<module>` 或 `<release>`，kebab-case）
- `<YYYY-MM-DD>`：报告生成日期
- 示例：`coverage-report-auth-2026-05-25.md` / `coverage-report-v2.4-2026-05-25.md`
- 存放位置由项目治理决定（典型：`docs/test-coverage/`）

报告是 **snapshot 制品**——每次生成新文件，不在旧文件上覆盖。

---

## 4. Frontmatter 契约

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
# 条件字段
conditional_reasons:                    # verdict: conditional 时必填
  - <原因>
---
```

### 4.1 字段表

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `artifact_type` | string | 必 | 固定 `test-coverage-report` |
| `lifecycle` | enum | 必 | 固定 `snapshot` |
| `created_at` | date | 必 | 报告生成日期 |
| `scope` | string | 必 | 覆盖评估范围（模块名 / release 号 / 自定义标识） |
| `trigger` | enum | 必 | 报告生成触发场景（决定评审严苛度） |
| `covers_artifacts` | list[path] | 必 | 本报告评估覆盖的上游制品（需求 / 契约 / 设计） |
| `test_case_sources` | list[path] | 必 | 数据来源的测试用例文档 / 代码目录 |
| `tool_provenance` | object | 必 | 关键数据的产出工具与版本（保证可追溯与可复现） |
| `verdict` | enum | 必 | 总体结论：`pass` / `fail` / `conditional`（语义见 §4.2） |
| `conditional_reasons` | list[string] | 条件 | `verdict: conditional` 时必填，列出条件项 |

### 4.2 verdict 语义

| 值 | 含义 | 转入条件 |
|---|---|---|
| `pass` | 覆盖充分、冗余可控、追溯完整 | 三节（矩阵 / 变异 / 追溯）均无 blocker |
| `conditional` | 有限通过，需特定豁免或后续补救 | 单项有可接受偏离，已记录条件 |
| `fail` | 不通过，需补用例或重审 | 任一节出现 blocker（关键 AC 未覆盖 / mutation score < 阈值 / 追溯死链） |

**verdict 是结论字段，不是过程字段**——它来源于报告正文，不应与正文矛盾。

---

## 5. 正文结构契约

### 5.1 必填章节（4 节）

**H1 标题**：`# 测试覆盖评估报告：<scope> @ <date>`

| # | 章节 | 用途 | 校验 |
|---|---|---|---|
| 1 | 评估摘要（Summary） | 一图/一段说清楚 verdict + 关键数字 | 含覆盖率 / mutation score / 死链数 三项关键指标 |
| 2 | 追溯矩阵（Traceability Matrix） | AC × 用例 × 维度 矩阵 | 详见 §5.2 |
| 3 | 变异测试概要（Mutation Summary） | 必要性的金标准证据 | 详见 §5.3 |
| 4 | 追溯健康审计（Trace Health） | 跨制品链路完整性 | 详见 §5.4 |

### 5.2 追溯矩阵契约

格式：表格，行 = AC × 维度，列 = 用例 id。

| 字段 | 取值 |
|---|---|
| 行键 | `<REQ-ID>#AC<n> · <维度>`，维度 ∈ `正向` / `边界` / `异常` / `非功能` / `状态转移` / `并发` |
| 列键 | 测试用例 id（`TC-<MODULE>-<nn>` 或代码用例的 `<module>::<function>`） |
| 单元格 | `✓`（覆盖）/ `—`（不适用）/ 空（缺失） |

**充分性硬判据**：每行至少 1 个 `✓` 或全行标 `—`（声明该维度不适用并附理由）。
**必要性软判据**：每列至少 1 个 `✓` 占据**唯一**单元（同维度重复 = 冗余信号）。

示例：

```markdown
| AC × 维度 | TC-AUTH-01 | TC-AUTH-02 | TC-AUTH-03 |
| :--- | :---: | :---: | :---: |
| ACME-REQ-08#AC1 · 正向 | ✓ |  |  |
| ACME-REQ-08#AC1 · 异常 |  | ✓ |  |
| ACME-REQ-08#AC1 · 边界 |  |  | ✓ |
| ACME-REQ-08#AC2 · 正向 | — | — | — |  ← 显式声明不适用
```

**空行必标因由**：缺失覆盖的行需在矩阵下方列"缺口清单"，每条含计划补救动作 + 责任方 + 截止日。

### 5.3 变异测试概要契约

每个被测模块一行，必含字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| `module` | string | 模块标识（与代码路径对应） |
| `mutants_total` | int | 注入变异总数 |
| `mutants_killed` | int | 被用例集捕获的变异数 |
| `mutation_score` | float | `killed / total`，百分比表示 |
| `survived_critical` | int | 存活的关键路径变异数（按工具或人工标注） |
| `threshold` | float | 项目约定阈值（推荐 ≥ 0.80） |
| `status` | enum | `pass`（≥ threshold）/ `fail`（< threshold）/ `waived`（豁免，需附原因） |

示例：

```markdown
| Module | Total | Killed | Score | Survived (critical) | Threshold | Status |
| :--- | ---: | ---: | ---: | ---: | ---: | :--- |
| auth/token | 142 | 128 | 90.1% | 0 | 80% | pass |
| auth/session | 89 | 61 | 68.5% | 3 | 80% | fail |
```

**`fail` 行必附"存活变异详情"子节**：列出存活的关键变异 + 推断的缺测维度 + 补用例建议。

**没跑变异测试不得伪造数据**：若工具未集成，本节写"未执行 — <原因> — 计划接入日期"，并要求 verdict ≤ `conditional`。

### 5.4 追溯健康审计契约

3 类检查项，每项一表：

**5.4.1 死链清单**（用例 `covers` 锚指向已删/已重命名的上游制品）：

| 用例 id | 死链锚 | 上游变化 | 建议动作 |
|---|---|---|---|

**5.4.2 裸 AC 清单**（上游 AC 未被任何用例覆盖）：

| AC id | 所属需求 | 缺测维度 | 补救责任方 |
|---|---|---|---|

**5.4.3 悬空守护清单**（用例守护的需求已 `deprecated` 但用例未同步）：

| 用例 id | 悬空守护对象 | 上游 deprecated 日期 | 建议动作 |
|---|---|---|---|

三类清单**任一非空** → verdict ≥ `conditional`；**关键 AC 裸露或死链** → verdict = `fail`。

### 5.5 可选章节

| 章节 | 触发场景 |
|---|---|
| 历史趋势（Trends） | 与上一次同 scope 报告对比，含 mutation score / 死链数 / 裸 AC 数变化 |
| 风险加权评估 | 把缺口按"频率 × 影响"标注优先级，引导补救排期 |
| 决策守护审计 | 检查 ADR 中被拒方案的拒绝前提是否仍有用例守护 |

---

## 6. 反模式

- ❌ verdict 与正文矛盾（如 verdict: pass 但追溯矩阵有空行未声明不适用）
- ❌ 没跑变异测试却给出 mutation score（数据捏造）
- ❌ 追溯矩阵把多个 AC 合并到一行（破坏每行可独立判定）
- ❌ 缺 `tool_provenance` 字段（无法复现 / 无法判断数据可信度）
- ❌ 用代码覆盖率（line coverage）冒充充分性证据（line coverage 不等于业务覆盖）
- ❌ 把每次用例修改都生成一份报告（snapshot 应对应有意义的 trigger，不是 PR 级噪音）
- ❌ verdict: conditional 未填 `conditional_reasons`
- ❌ 死链/裸 AC/悬空守护清单合并为一张表（3 类问题责任方与补救动作不同，必须分列）
- ❌ 把单条用例 5 维评审结论塞进报告（单用例评审归 [test-case-quality](../rules/test-case-quality.md)，不与覆盖评审混评）
- ❌ 报告生成后修改正文（snapshot 一经发布即冻结，更正用新报告 + CHANGELOG）

---

## 7. 示例

### 7.1 最小合规覆盖报告：auth 模块发布门禁

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
  - auth/session 模块 mutation score 68.5% < 80% 阈值，已排期下个迭代补
---

# 测试覆盖评估报告：auth @ 2026-05-25

## 评估摘要

- **AC 覆盖率**：12/13（92.3%）—— 缺 ACME-REQ-08#AC5（OAuth 回调链路）
- **Mutation Score**：auth/token 90.1% ✅ / auth/session 68.5% ❌
- **追溯死链**：0
- **裸 AC**：1（已记录补救计划）
- **悬空守护**：0

verdict = **conditional**：可发布，session 模块需在 v2.5 前补齐变异覆盖。

## 追溯矩阵

| AC × 维度 | TC-AUTH-01 | TC-AUTH-02 | TC-AUTH-03 | TC-AUTH-04 |
| :--- | :---: | :---: | :---: | :---: |
| ACME-REQ-08#AC1 · 正向 | ✓ |  |  |  |
| ACME-REQ-08#AC1 · 异常 |  | ✓ |  |  |
| ACME-REQ-08#AC2 · 篡改 |  |  | ✓ |  |
| ACME-REQ-08#AC4 · header 格式 |  |  |  | ✓ |
| ACME-REQ-08#AC5 · OAuth 回调 |  |  |  |  | ← 缺口

### 缺口清单

| 行 | 计划动作 | 责任方 | 截止 |
| :--- | :--- | :--- | :--- |
| ACME-REQ-08#AC5 · 正向 | 新增 TC-AUTH-05 + TC-AUTH-06 | qa-alice | v2.5 |

## 变异测试概要

| Module | Total | Killed | Score | Survived (critical) | Threshold | Status |
| :--- | ---: | ---: | ---: | ---: | ---: | :--- |
| auth/token | 142 | 128 | 90.1% | 0 | 80% | pass |
| auth/session | 89 | 61 | 68.5% | 3 | 80% | fail |

### auth/session 存活变异详情

- `session.expire_at` 比较符 `<` → `<=` 存活 → 缺"恰好过期一刻"边界用例
- `refresh_token` 旋转后旧 token 未失效检测变异存活 → 缺安全回归用例
- `concurrent refresh` 锁失效变异存活 → 缺并发用例

## 追溯健康审计

### 死链清单
（空）

### 裸 AC 清单

| AC id | 所属需求 | 缺测维度 | 补救责任方 |
| :--- | :--- | :--- | :--- |
| ACME-REQ-08#AC5 | ACME-REQ-08 | 正向 + 异常 | qa-alice |

### 悬空守护清单
（空）
````

---

## 8. 与其他资产关系

- **配套 rule**：[rules/test-coverage-quality.md](../rules/test-coverage-quality.md)——覆盖评估报告的 5 维评审清单
- **下游消费者**：用例集覆盖评审服务、跨制品对齐评审服务读取本制品产出评审决策
- **数据来源 spec**：[test-case-modeling.md](./test-case-modeling.md)——追溯矩阵的列与裸 AC 检测依赖用例的 `covers` 字段
- **上游对齐 spec**：[requirement-modeling.md](./requirement-modeling.md)——矩阵行键的 `<REQ-ID>#AC<n>` 锚定 AC ID 格式
- **关联 rule**：[doc-health-criteria.md](../rules/doc-health-criteria.md)——死链检测复用其链接图健康判据
- **递归基础**：本 spec 自身遵循 [spec-modeling.md](./spec-modeling.md) v2.0.0 的 8 节骨架
