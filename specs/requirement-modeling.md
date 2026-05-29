---
id: REQUIREMENT_MODELING_SPEC_V4
name: Requirement Modeling Schema
description: Spec defining requirement document fields, formats, and validation rules. Covers frontmatter contract, 6 mandatory body sections (Background/Objective/Acceptance/Dependencies/Risks/Source), and conditionally-mandatory optional sections (Scope, Business Rules).
version: 4.0.0
status: active
lifecycle: living
created_at: 2026-03-25
scope: |
  Defines the structural contract for requirement documents: frontmatter fields, required body
  sections, optional sections, and field formats. Applies to functional requirements,
  non-functional requirements, bug fixes, and technical tasks.
related:
  - ./spec-modeling.md
  - ./design-modeling.md
  - ../rules/requirement-quality.md
---

# 需求建模规范

> **数据契约**：定义需求文档的字段结构与正文骨架

---

## 1. 定位与适用范围

需求文档（requirement document）回答"做什么"——通过用户故事或问题陈述、可验收的标准、依赖与风险，让团队对"要交付的东西"达成共识。它是上游目标（goal / roadmap 节点）与下游设计文档之间的桥梁。

本规范以验收标准为中心：业务规则默认内联进验收标准，不单列；实现层面的场景流程（步骤流、状态流转细节）下沉至下游设计文档。这些刻意的省略是契约的一部分——避免作者在规则与场景的归属上反复猜测。

适用：

- **功能需求**：新增功能、流程调整、体验优化
- **非功能需求**：性能、安全、可维护性、可扩展性
- **缺陷修复**：缺陷处理、性能优化、技术债偿还
- **技术任务**：架构优化、依赖升级、基础设施改造

不适用：

- 探索性研究或方案对比（属 ADR 或 RFC）
- 内部组件 API 设计（属设计文档）
- 临时性 bug fix 或代码清理（用 commit / PR 描述即可）

### 1.1 按需求类型的简化指引

| 类型 | 必填字段 | 可简化部分 |
|---|---|---|
| 功能需求 | 全部 6 节正文 | — |
| 缺陷修复 | 全部 6 节正文 | 背景（可用问题陈述形式）、风险（1 条关键风险即可） |
| 技术任务 | 全部 6 节正文 | 背景（可用问题陈述形式） |
| 非功能需求 | 全部 6 节正文 | — |

风险优先级与缓解策略**永不可选**。

---

## 3. 命名约定

```
<PROJECT>-REQ-<nn>.md
```

- `<PROJECT>`：项目缩写（大写，2-6 字符，如 `ACME` / `MYAPP`）
- `<nn>`：顺序号，2 位起步，单调递增，**不复用**
- 示例：`ACME-REQ-05.md` / `MYAPP-REQ-042.md`
- 存放位置由项目治理决定（典型：`docs/requirements/`）

---

## 4. Frontmatter 契约

```yaml
---
id: <PROJECT>-REQ-<nn>
artifact_type: requirement
lifecycle: snapshot
created_at: YYYY-MM-DD
status: draft | approved | implemented | superseded
priority: P0 | P1 | P2
parent: <upstream goal / roadmap node path>
# 条件字段
superseded_by: <new-requirement-id>   # status: superseded 时必填
implemented_at: YYYY-MM-DD             # status: implemented 时必填
---
```

### 4.1 字段表

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | string | 必 | 格式 `<PROJECT>-REQ-<nn>`（如 `ACME-REQ-05`） |
| `artifact_type` | string | 必 | 固定 `requirement` |
| `lifecycle` | enum | 必 | 固定 `snapshot`（需求批准后冻结，变更新建新需求） |
| `created_at` | date | 必 | 需求落地日期 |
| `status` | enum | 必 | `draft` / `approved` / `implemented` / `superseded`（语义见 §4.2） |
| `priority` | enum | 可选 | `P0`（阻塞路径）/ `P1`（关键路径）/ `P2`（非关键） |
| `parent` | path | 可选 | 上游目标 / roadmap 节点路径 |
| `superseded_by` | string | 条件 | `status: superseded` 时必填，指向继任需求 id |
| `implemented_at` | date | 条件 | `status: implemented` 时必填，记录实现完成日期 |

### 4.2 状态机语义

| 状态 | 含义 | 转入条件 |
|---|---|---|
| `draft` | 起草中 | 需求文档首次落地，尚未通过评审 |
| `approved` | 已批准 | 评审通过，可派生设计文档（design 的 `parent`） |
| `implemented` | 已实现 | 关联实施任务全部 `Done`，验收标准全部满足（需填 `implemented_at`） |
| `superseded` | 被新需求替代 | 业务变更导致需求重写（需填 `superseded_by`） |

---

## 5. 正文结构契约

### 5.1 必填章节（6 节）

每份需求文档必须包含以下 6 节正文（H1 标题不在统计内）。

**H1 标题**：`# 需求：[类型] 一句话描述`
- 类型示例：`[功能]` / `[缺陷]` / `[优化]` / `[非功能]` / `[技术任务]`
- 标题 ≤ 80 字符，不含技术实现细节
- 陈述需求主体（功能 / 问题 / 任务），不陈述期望结果——结果归「目标」节；词性不限（能力短语 / 问题陈述 / 约束陈述均可）

| # | 章节 | 用途 | 校验 |
|---|---|---|---|
| 1 | 背景与价值（Background & Value） | 解释问题背景与重要性 | ≤ 300 字符；**不**含解决方案 / 技术选型；推荐用户故事格式（`作为 X / 我希望 Y / 以便 Z`）或问题陈述（`背景 / 期望状态 / 影响`） |
| 2 | 目标（Objective） | 陈述本需求交付后世界发生的改变 | 单行；陈述需求级目标（区别于上游战略 / 产品目标，后者经 frontmatter `parent` 引用，不在此重复）；**不**含解决方案 / 技术选型 |
| 3 | 验收标准（Acceptance Criteria） | 定义需求完成的可验证条件 | ≥ 3 条；每条可自动或人工验证；**无**模糊形容词（"快"/"合理"/"友好"）；非功能需求含具体数值（如延迟 ≤ 500ms） |
| 4 | 依赖与前置条件（Dependencies & Prerequisites） | 依赖关系与前置条件 | 含 3 类：依赖需求 ID / 前置条件（含验证方式）/ 外部依赖；依赖图无环；无依赖时显式写"无依赖" |
| 5 | 风险、约束与假设（Risks, Constraints & Assumptions） | 风险（概率 × 影响）/ 已确认约束 / 待验证假设 | 功能 / 技术任务：≥ 1 条风险、≥ 2 条约束；缺陷修复：≥ 1 条关键风险（约束可选）；每条风险标注优先级 = 概率 × 影响；每条假设附验证方式 + 责任方 |
| 6 | 需求来源（Source） | 业务来源与决策上下文 | 含来源类型（功能请求 / 业务目标 / 故障 / 技术债）+ 来源链接 / ID + 决策背景；可追溯，不是"口头转述" |

### 5.2 可选章节

按场景需要添加：

| 章节 | 触发场景 |
|---|---|
| 范围定义（Scope） | 多系统集成、跨边界歧义、技术任务、工作量 > 5 天（满足任一时**升为必填**） |
| 业务规则（Business Rules） | 规则集本身即交付物（定价 / 资格 / 计税 / 风险评分）、单条规则被 ≥ 2 条验收标准引用、规则构成状态机 / 决策表、规则需作为下游合规审计权威来源（SSOT）被引用（满足任一时**升为必填**） |
| 待解决问题（Open Questions） | 评审中尚未解决的事项；按"阻塞 / 非阻塞"分类，附责任方与计划解决方式 |
| 完成定义（Definition of Done） | 流程与质量门（测试覆盖、文档更新、部署门），与"验收标准"区分（验收 = 功能完成；DoD = 可发布） |
| 时间表（Timeline） | 排期周期 + 预估工作量（如"Phase 2 第 3-4 周 / 4 工日"） |

### 5.3 格式细节

#### 5.3.1 风险优先级计算

```
优先级 = 概率 × 影响

- 高优先级：概率 ≥ 中 且 影响 ≥ 高
- 中优先级：（概率 = 中 且 影响 = 中）或（概率 = 高 且 影响 = 低）
- 低优先级：概率 ≤ 低 或 影响 ≤ 低
```

#### 5.3.2 验收标准推荐格式

Gherkin BDD（`Given / When / Then`）或清单（`- [ ] ...`）二选一。Gherkin 适合行为类需求，清单适合特性堆叠。

#### 5.3.3 业务规则的声明形式（升为必填时）

业务规则升为必填（§5.2 触发条件之一命中）时：

- 用声明式表达：决策表（decision table）或状态表（state table），不写过程式步骤。
- 每条规则有稳定 id（如 `R1` / `R2`），id 不复用。
- 验收标准回引规则 id（如 `覆盖 R3`），建立规则到验收的可追溯链。

#### 5.3.4 业务规则与验收标准的边界

- 业务规则 = 规范性声明（normative）：声明"什么必须为真"，一条规则可派生多条验收标准。
- 验收标准 = 规则的可验证投影（verification）：声明"如何验证它为真"，并覆盖非规则项（性能、可用性、接口存在性等）。
- 规则类验收标准回引其规则 id，闭合规则与验收的 MECE 重叠。

---

## 6. 反模式

- ❌ 缺 frontmatter 必填字段（id / artifact_type / status / created_at）
- ❌ `id` 格式不规范（小写、缺 PROJECT 前缀、复用编号）
- ❌ 背景字段含技术选型 / 实现路径 / 具体功能描述
- ❌ 标题陈述期望结果而非需求主体（与「目标」节重复）
- ❌ 缺「目标」节，或把需求级目标混入「背景与价值」
- ❌ 验收标准 < 3 条
- ❌ 验收标准含模糊词（"应当"、"合理"、"友好"、"快"）
- ❌ 非功能需求验收标准缺具体数值
- ❌ 依赖图含环
- ❌ 缺风险章节或风险无优先级标注
- ❌ 风险只列"风险描述"不附"缓解策略"
- ❌ 需求来源含糊（"某人提的"、"口头讨论"）
- ❌ `superseded` 状态未填 `superseded_by`
- ❌ `implemented` 状态未填 `implemented_at`
- ❌ 满足"范围定义升为必填"4 个条件之一但缺范围章节
- ❌ 满足"业务规则升为必填"触发条件之一但规则仍散落在验收标准内（未单列声明式规则节）
- ❌ 业务规则升为必填后用过程式步骤而非决策表 / 状态表表达
- ❌ 规则类验收标准未回引其业务规则 id（规则与验收 MECE 重叠未闭合）
- ❌ 把"自检清单"写进 spec 正文（评审清单归 [rules/requirement-quality.md](../rules/requirement-quality.md)）

---

## 7. 示例

### 7.1 功能需求完整示例

````markdown
---
id: ACME-REQ-15
artifact_type: requirement
lifecycle: snapshot
created_at: 2026-04-12
status: approved
priority: P1
parent: ../roadmap/2026-q2.md#open-integration
---

# 需求：[功能] 知识库检索的语义搜索 API

## 目标

集成方接入知识库检索的实现成本从重复造轮子降至近零，官方语义搜索 API 成为唯一权威检索入口。

## 背景与价值

作为系统集成方
我希望有 API 能对存储的规范执行语义搜索
以便外部系统能基于上下文高效检索相关文档

当前知识库仅支持关键词检索，外部 Agent 接入需自行做 embedding 与向量召回，重复造轮子。

## 验收标准

- [ ] REST API `POST /search/semantic` 已实现且能响应查询
- [ ] 在 10M 条目数据集上响应时间 ≤ 500ms（p95）
- [ ] top-3 相关性精度 ≥ 80%（50+ 典型查询验证）
- [ ] API 文档完备（OpenAPI 规范 + 5+ 用例）
- [ ] API Key 鉴权 + 限流（默认 10 QPS / key）

## 依赖与前置条件

依赖需求：
- ACME-REQ-05（向量化流水线）
- ACME-REQ-08（向量数据库部署）

前置条件：
- 知识库向量化完成（≥ 10M 向量）—— 验证方式：向量库 `count` API
- 向量数据库健康度 ≥ 99.5%（监控大盘可见）

外部依赖：
- 向量数据库（已部署，无需额外申请）
- API Gateway（已有，需新增路由）

## 风险、约束与假设

风险：
- **高并发下 API 性能退化**（概率 = 中 35% / 影响 = 高 → 高优先级）
  缓解：第 1 周完成压测，引入 Redis 查询缓存（TTL 5min）
- **embedding 模型精度不达标**（概率 = 低 15% / 影响 = 中 → 中优先级）
  缓解：第 1 周完成基准测试，准备备选模型 model-B

约束（已确认）：
- 向量数据库选型不可变（基础设施约束）
- Phase 2 末（2 周后）必须交付（与 Phase 3 串行依赖）

假设（待验证）：
- 当前 embedding 模型在 10M 数据集精度 ≥ 80% | 第 1 周基准测试 | 技术负责人

## 需求来源

- **来源类型**：业务目标
- **来源链接**：2026 Q2 OKR——"开放第三方与知识库的集成能力"
- **决策背景**：开发者社区反馈接入成本高（社区调研报告 §3）；2026 Q1 已有 3 个集成方独立实现 embedding 流程，重复工作约 40 工日

## 范围定义

In Scope:
- REST API 实现、向量数据库集成、API Key 鉴权、OpenAPI 文档
- 服务端缓存（Redis）

Out of Scope:
- OAuth 鉴权（后续需求）
- 搜索结果 UI（属前端项目）
- 实时向量更新（Phase 3 处理）

## 时间表

P1 · Phase 2 第 3-4 周 · 4 工日
````

### 7.2 业务规则升为必填示例（决策表 + 验收回引）

规则集即交付物（定价折扣），故业务规则升为必填，用决策表声明，验收标准回引规则 id。

````markdown
## 业务规则

| id | 条件 | 折扣 |
|---|---|---|
| R1 | 订单金额 < 100 | 0% |
| R2 | 100 ≤ 订单金额 < 500 | 5% |
| R3 | 订单金额 ≥ 500 且为会员 | 15% |

## 验收标准

- [ ] 订单金额 80，下单后实付 80（覆盖 R1）
- [ ] 会员订单金额 600，下单后实付 510（覆盖 R3）
````

---

## 8. 与其他资产关系

- **配套 rule**：[rules/requirement-quality.md](../rules/requirement-quality.md)——需求文档质量评审清单（5 维：完整性 / 可执行性 / 清晰性 / 合理性 / 可追溯性）。本 spec 只定义数据契约，评审清单全部归 rule。
- **下游 spec**：[design-modeling.md](./design-modeling.md)——`approved` 状态的需求才能派生设计；design 的 `parent` 指向 requirement 文档路径
- **相关行业标准**：IEEE 830（软件需求规格说明）、Gherkin / Cucumber（BDD 验收格式）、ISO 31000（风险管理）、SWEBOK（可追踪性最佳实践）
- **递归基础**：本 spec 自身遵循 [spec-modeling.md](./spec-modeling.md) v2.0.0 的 8 节骨架；跳过 §2 心智模型（需求的必答维度已在 §5.1 的 6 节中体现）
