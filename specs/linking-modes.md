---
artifact_type: spec
spec_id: LINKING_MODES_SPEC_V1
created_by: spec-authoring
lifecycle: living
created_at: 2026-04-24
status: informational
version: 2.0.0
---

# 链接模式参考（Linking Modes — Descriptive Reference）

> **注意（v2.0 / 2026-04-25）**：本文档自 v2.0 起降级为**描述性参考**，不再是运行时配置对象。
>
> v1.0（随 v7.0.0 发布）曾把 6 项模式定义为 `ARTIFACT_NORMS.md` 的 `linking_mode` 枚举字段，由 `discover-docs-norms` / `define-docs-norms` / `plan-next` 协同消费。v8.0.0 回撤此设计（见 [ADR 005](../docs/architecture/adrs/005-retract-linking-mode-enum.md)）——模式描述仍对**理解项目实践**有用，但不作为需要"选择"的运行时字段。
>
> **实际实现**：项目链接约定通过 [`specs/artifact-contract.md` §8](artifact-contract.md#8-runtime-norms-resolution-protocol) 的 `path_pattern` 覆盖机制 + `upstream_ref` 可选输入表达。本文档只描述模式 taxonomy，不约束任何技能行为。

## 1. 定义（Definition）

**链接模式（Linking Mode）** 是项目在**治理制品**（requirement / design / task / code / PR）之间建立**可追溯关系**所采用的**机械约定**。

三个关键词的含义：

- **治理制品**：承载治理信息的文件或代码单元。典型类型：需求文档、设计文档、任务条目、提交 / PR。
- **可追溯关系**：从任一制品出发，能找到与之对应的上游来源或下游产物。例：从 design 文档能找到它依据的 requirement；从 task 能找到它所属的 design。
- **机械约定**：无需人工判断即可由工具自动解析的规则。"评审会口头约定"不是链接模式；"文件名共享 slug"是。

**用途（v2.0 重新定位）**：本文档为**taxonomy 参考**，用于：
- 团队沟通（"我们项目用 colocation 模式"的共识语言）
- 设计讨论（权衡不同约定的优缺点）
- 审计参考（回顾项目采用了什么约定）

**不再用于**：
- 运行时配置（v1.0 设计已废弃）
- 技能的"选择对象"（不再是 discover-docs-norms / define-docs-norms 的消费对象）
- 字段枚举值域（`linking_mode` 字段已从 `ARTIFACT_NORMS.md` schema 移除）

**非用途**：
- 不用于"该建立哪些文档"——那是 `artifact-contract.md` 的职责
- 不用于"文档该放哪里"——那是 `ARTIFACT_NORMS.md` 的 `path_pattern` 职责
- 链接模式只回答"既有文档之间**如何相互引用**"

## 2. 枚举（Enumeration）

本规范定义 **6 个固定枚举值**。`discover-docs-norms` 的识别逻辑、`define-docs-norms` 的选择 UI、`plan-next` 的消费逻辑都限定于此 6 项，不自由扩展。

下表对每个枚举值按**统一 7 维**描述，确保 LLM 与人类的理解一致：

| 维度 | 含义 |
|---|---|
| **本质** | 一句话定义 |
| **识别信号** | 扫描仓库时能观察到的具体特征（用于 discover-docs-norms） |
| **追溯方向** | 上→下 / 下→上 / 双向 |
| **维护成本** | 零 / 低 / 中 / 高（按项目团队需要付出的额外工作评估） |
| **工具要求** | 下游产出技能需支持哪些能力 |
| **适用场景** | 什么类型的项目 / 团队适用 |
| **示例** | 具体文件结构 / frontmatter 片段 |

---

### 2.1 `slug` — 共享占位符命名

| 维度 | 内容 |
|---|---|
| **本质** | 所有相关制品的文件名包含共同的 slug（主题标识符），跨目录通过同名 glob 匹配 |
| **识别信号** | 多个制品目录里的 `path_pattern` 共享 `{topic}` / `{slug}` 占位符；文件名跨目录出现同一 slug；分支 / PR 标题含同 slug |
| **追溯方向** | 双向（glob 即可正反） |
| **维护成本** | 零（文件名自然产出即完成链接） |
| **工具要求** | 下游技能 `path_pattern` 含占位符（AI Cortex 所有下游产出技能当前默认满足） |
| **适用场景** | 小中团队；目录结构稳定；避免元数据负担 |
| **示例** | `docs/requirements-planning/user-auth.md` + `docs/design-decisions/2026-04-24-user-auth.md` + `docs/process-management/tasks/2026-04-24-user-auth.md` + 分支 `feat/user-auth` + PR 标题 `[user-auth] ...` —— 共享 slug `user-auth` |

---

### 2.2 `colocation` — 同目录聚合

| 维度 | 内容 |
|---|---|
| **本质** | 所有相关制品放在同一个以 slug 命名的目录下，子文件按制品类型命名 |
| **识别信号** | 存在 `work/<slug>/` 或 `initiatives/<slug>/` 或等价模式；子目录内含 requirement / design / tasks 等类型文件 |
| **追溯方向** | 双向（`ls <dir>/` 即可） |
| **维护成本** | 零（路径隐式链接） |
| **工具要求** | 下游技能须支持输出到自定义目录（当前技能 `path_pattern` 硬编码分目录，**需 v7.x 规范驱动架构改造后方可用**） |
| **适用场景** | 团队规模稳定；强一致性；希望把某主题所有制品"打包"管理 |
| **示例** | `work/user-auth/requirement.md` + `work/user-auth/design.md` + `work/user-auth/tasks.md` + `work/user-auth/pr-links.md` |

---

### 2.3 `parent-pointer` — 显式上游指针

| 维度 | 内容 |
|---|---|
| **本质** | 每个下游制品在 frontmatter 中用单字段显式声明其直接上游 |
| **识别信号** | 下游制品 frontmatter 频繁出现 `parent:` / `implements:` / `related_to:` / `roadmap_item:` 等链接字段 |
| **追溯方向** | 下→上（单向直接；上→下需构建反向索引） |
| **维护成本** | 低（每文件 1 行 frontmatter） |
| **工具要求** | 下游技能须输出相应 frontmatter 字段（**需 v7.x 升级下游技能**） |
| **适用场景** | 合规 / 审计场景；大团队；跨目录协作；制品文件名可自由命名（不依赖 slug 约定） |
| **示例** | `docs/design-decisions/auth-session-jwt.md` frontmatter：`parent: docs/requirements-planning/user-auth.md` |

---

### 2.4 `manifest` — 中央清单登记

| 维度 | 内容 |
|---|---|
| **本质** | 每个主题或 Now tier 条目有一个清单文件，集中列出它的所有子制品链接 |
| **识别信号** | 存在 `docs/process-management/now/<slug>.md` 或等价清单文件，内含对 requirement / design / tasks / PR 的显式链接 |
| **追溯方向** | 上→下（清单→子制品直接；下→上需反向查清单） |
| **维护成本** | 中（每次新增 / 删除 / 重命名下游都要同步更新清单；有漂移风险） |
| **工具要求** | 须有清单维护者：可为 (a) 下游技能执行时自动追加 (b) 独立 `align-manifest` 技能 (c) 人工维护。v6.3 尚无任一到位 |
| **适用场景** | 需要"卡片式"登记（如验收卡、交付卡）；审计要求集中视图；团队倾向中央索引 |
| **示例** | `docs/process-management/now/user-auth.md`：<br>```- requirement: docs/requirements-planning/user-auth.md```<br>```- design: docs/design-decisions/2026-04-24-user-auth.md```<br>```- tasks: docs/process-management/tasks/2026-04-24-user-auth.md```<br>```- prs: #127, #131``` |

---

### 2.5 `mixed` — 多模式并存

| 维度 | 内容 |
|---|---|
| **本质** | 项目同时采用上述多种模式（例如主 slug + 辅 manifest） |
| **识别信号** | `discover-docs-norms` 扫描时检测到多于一种模式的强信号 |
| **追溯方向** | 视组合而定 |
| **维护成本** | 中-高（每种模式的维护成本之和，且需人工清楚声明主 / 辅关系） |
| **工具要求** | 须在 `ARTIFACT_NORMS.md` 显式声明各模式的作用域（例：主制品按 slug，Now tier 追加 manifest 作为聚合视图） |
| **适用场景** | 演化中的项目：旧约定与新约定并存；或不同资产层使用不同模式 |
| **示例** | slug（所有制品基础链接） + manifest（Now tier 另加一份 `now/<slug>.md` 汇总卡） |

---

### 2.6 `none` — 未采用

| 维度 | 内容 |
|---|---|
| **本质** | 项目未采用任何可机器识别的链接约定 |
| **识别信号** | 扫描无上述任一模式的信号；文件散布 / 命名随意 / frontmatter 无链接字段 / 无清单文件 |
| **追溯方向** | 不可机械追溯（仅人类记忆或外部文档） |
| **维护成本** | 不适用 |
| **工具要求** | 不适用 |
| **适用场景** | 新建项目未确立约定；临时性探索项目；单人项目 |
| **示例** | 仓库里有零散的 `requirements.md`、`some-design.md`、`TODO.md`，彼此无引用关系 |

**消费者行为提示**：`plan-next` 读到 `none` 时触发前置闸门路由——`discover-docs-norms` → `define-docs-norms` → 用户选定模式后再评估下游。

## 3. 识别规则（Identification Rules）— v2.0 退休

~~v1.0 由 `discover-docs-norms` 实现的识别判据已废弃~~。

v2.0 起，"项目属于哪种模式"不再是工具需要机械识别的问题——如果项目通过 `path_pattern` 覆盖或 manifest 文件表达了约定，工具直接按实际约定工作即可。本节保留为描述性参考：若需要**人工判断**项目当前属于哪种模式，可参考 §2 的"识别信号"维度。

## 4. 选择规则（Selection Rules）— v2.0 退休

~~v1.0 由 `define-docs-norms` 实现的 6 枚举选择 UI 已废弃~~。

v2.0 起，项目**不需要"选择"链接模式**。采用默认（slug 约定）则零配置；采用非默认则通过 [`specs/artifact-contract.md` §8](artifact-contract.md) 的 `path_pattern` 覆盖或建 manifest 文件表达即可——这些是具体机制，不是模式枚举。

## 5. 消费规则（Consumption Rules）— v2.0 退休

~~v1.0 由 `plan-next` 等消费者按 `linking_mode` 字段分支的逻辑已废弃~~。

v2.0 起，消费者按实际数据工作：
- 读 `path_pattern`（从 §8.2 发现顺序）决定扫描路径
- 检测 `parent:` frontmatter 字段（物理信号）
- 检测 manifest 文件存在性（物理信号）

无需查"当前是哪种模式"，直接看数据即可。

## 6. 与其他规范的关系

- **`specs/artifact-contract.md`**：定义"每种制品该有哪些字段"。链接模式 2.3（parent-pointer）使用的 `parent:` 字段若成为标准，应登记到此处。
- **`ARTIFACT_NORMS.md` schema**（`specs/artifact-norms-schema.md`）：定义项目级规范文件的字段集。`linking_mode` 字段由本规范贡献到该 schema。
- **`specs/terminology.md`**：收录"链接模式"作为核心术语的一句话定义；本规范是该术语的完整展开。

## 7. 版本与演进

- **v2.0.0**（2026-04-25）：降级为描述性参考文档；§3–§5 标注退休；顶部加 v1.0 回撤说明。运行时链接配置改由 [specs/artifact-contract.md §8](artifact-contract.md) 的 `path_pattern` 覆盖 + `upstream_ref` 输入机制处理。见 [ADR 005](../docs/architecture/adrs/005-retract-linking-mode-enum.md)。
- **v1.0.0**（2026-04-24）：初版——定义 6 枚举为运行时配置对象；由 discover/define/plan-next 协同消费。v2.0 回撤此设计。
- **演进原则（v2.0 起）**：本文档是 taxonomy 参考，新增模式描述为 MINOR；描述澄清为 PATCH；重新升级为运行时配置对象需重写决策理由（明确 v2.0 的废弃缘由已解决）。
