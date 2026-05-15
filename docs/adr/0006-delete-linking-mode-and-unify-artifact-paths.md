---
artifact_type: adr
created_by: decision-record
lifecycle: snapshot
created_at: 2026-04-25
status: accepted
description: 彻底删除 linking_mode 内容并统一需求/设计/任务路径
---

# ADR 0006：彻底删除 linking_mode 相关内容 + 统一需求/设计/任务路径（v9.0.0）

**上下文**：v8.0.0 回撤了 linking_mode 的运行时消费，但仍以"废弃"保留了大量引用；用户要求**彻底删除**所有 linking_mode 内容，同时指出 analyze-requirements / design-solution / breakdown-tasks 的输出路径不统一（前两个在顶级目录，tasks 嵌套在 process-management 下；前一个无日期前缀，后两个有 YYYY-MM-DD 前缀）

## 背景

v8.0.0 采用"保留废弃说明"策略——`specs/linking-modes.md` 降为描述性文档、`artifact-norms-schema.md §6` 标注废弃、各技能 Stage 0 追加"v8.0 起 linking_mode 已废弃"注释。这种软删除留下两类问题：

1. **认知负担**：读者仍需理解这个曾经存在的概念才能读懂文档；新加入者看到"xxx 不涉及 linking_mode 分支"只能困惑"所以 linking_mode 是什么？"
2. **sunk-cost 残留**：`specs/linking-modes.md` 作为 informational doc 占据 manifest 注册条目和 specs/INDEX.md 一行；各 agent.yaml 的 primary_use 仍引用此概念；累计 35+ 处 soft-deprecated 引用

同时，v7/v8 迭代过程中一直回避了一个基础问题：**三个核心产出技能的输出路径和命名不统一**：

| 技能 | 原 path_pattern |
|---|---|
| analyze-requirements | `docs/requirements-planning/{topic}.md` |
| design-solution | `docs/design-decisions/YYYY-MM-DD-{topic}.md` |
| breakdown-tasks | `docs/process-management/tasks/YYYY-MM-DD-{topic}.md` |

三类差异：
- **父目录层级不一**：requirements / designs 在 docs/ 顶级；tasks 嵌套在 process-management/ 下
- **父目录语义体系不一**：`-planning` / `-decisions` 后缀 vs 嵌套式分组
- **日期前缀规则不一**：requirements 无前缀；design / tasks 有 YYYY-MM-DD

这让 plan-next 按"共享 slug glob"扫描各下游目录时必须记住三套不同规则——本来想用"slug 统一贯通"的愿景被分散规则抵消。

## 决策

### 决策 1：彻底删除 linking_mode 相关内容

**删除**（非历史性引用全部清除）：

- `specs/linking-modes.md` 文件 → **删除**
- `manifest.json` 中 `LINKING_MODES_SPEC_V1` 注册条目 → **删除**
- `specs/INDEX.md` 中 Linking Modes Reference 行 → **删除**
- `specs/terminology.md` §6 "相关术语 / Linking Mode" 节 → **删除**
- `specs/artifact-norms-schema.md` §6 "链接模式字段（已废弃）"节 → **删除整节**
- `specs/artifact-contract.md` §8.4 中提及 linking-modes.md 的"项目自定义典型场景"段落中的 v7 残留引用 → **简化并清理**
- `specs/artifact-contract.md` §8.6 错误处理表中 `linking_mode: ...` 错误场景行 → **删除并用通用 `{parent_slug}` 缺失场景替换**
- 所有技能 SKILL.md / agent.yaml / README.md 里残留的 "v8.0 linking_mode 已废弃 / 不涉及 linking_mode 分支" 注释 → **删除**

**保留**（历史记录，accept 性质）：

- ADR 003（最早讨论 linking_mode）、ADR 004（v7.0 落地）、ADR 005（v8.0 回撤）、ADR 006（本 ADR） → **保留**
- `CHANGELOG.md` v7.0.0 / v8.0.0 / v9.0.0 条目 → **保留**（CHANGELOG 本质是变更历史）
- 各规范 v 条目里描述"本版本删除了 linking_mode"的 changelog 行 → **保留**（必须提及被删对象）

### 决策 2：统一 requirements / design / tasks 的 canonical 路径

采用**扁平并列**结构：`docs/<type>/{slug}.md`。

| artifact_type | 旧 path_pattern | 新 path_pattern |
|---|---|---|
| requirements | `docs/requirements-planning/{topic}.md` | `docs/requirements/{slug}.md` |
| design | `docs/design-decisions/YYYY-MM-DD-{topic}.md` | `docs/designs/{slug}.md` |
| tasks | `docs/process-management/tasks/YYYY-MM-DD-{topic}.md` | `docs/tasks/{slug}.md` |

**关键改动**：

- **父目录扁平化**：三类均位于 `docs/` 顶级，平级并列，简化心智模型
- **命名去后缀化**：`requirements-planning` → `requirements`；`design-decisions` → `designs`；保持纯名词复数
- **去日期前缀**：design / tasks 去掉 `YYYY-MM-DD-` 前缀；git log 已经提供时序，文件名不重复编码
- **统一占位符**：全部用 `{slug}`（不再混用 `{topic}`）

**路径理由**（新加入 artifact-contract §2 / Appendix A）：

同一主题的 requirement / design / tasks **共享 slug**，跨三个平级目录即能 glob 打通全链（如 "user-auth" 主题的三份制品均为 `docs/{requirements,designs,tasks}/user-auth.md`）。plan-next 的 Now tier 下游扫描由此变成最简单的 slug glob，不需要理解任何"模式"概念。

### 决策 3：其他制品类型保持原路径

backlog-item、adr、doc-assessment 三类保留 v4.0 路径：

- `docs/process-management/project-board/backlog/YYYY-MM-DD-{slug}.md`（backlog 看板传统）
- `docs/process-management/decisions/YYYYMMDD-{slug}.md`（ADR 社区惯例）
- `docs/calibration/doc-assessment.md`（calibration 分类）

**理由**：这三类有各自领域惯例（敏捷看板、ADR、治理报告），强行统一会破坏领域语义。只统一 requirements / design / tasks 三类产品交付主链。

### 决策 4：协同 MAJOR 发布为 v9.0.0

- `manifest.json` project version 4.0.0 → **5.0.0**
- `manifest.json` spec_version 4.0.0 → **5.0.0**
- `specs/artifact-contract.md` v4.0 → **v5.0**（§2 路径表 MAJOR 变更）
- `specs/artifact-norms-schema.md` v2.0 → **v3.0**（§6 删除 MAJOR）
- `specs/terminology.md` v1.1.1 → **v1.2.0**（§6 删除）
- `skills/analyze-requirements` v2.0 → **v3.0**（路径 MAJOR 变更）
- `skills/design-solution` v2.0 → **v3.0**（路径 MAJOR 变更）
- `skills/breakdown-tasks` v2.0 → **v3.0**（路径 MAJOR 变更）

其他技能不 bump：它们的 Stage 0 + upstream_ref 机制不变，只是消除了 linking_mode 的残留措辞。

## 替代方案（已拒绝）

1. **保留 linking_mode 为描述性文档**（v8.0 的做法）：拒。用户明确要求删除；软废弃留下的认知负担和维护成本大于收益。
2. **只统一命名不改父目录**（保留 `requirements-planning` / `design-decisions`）：拒。父目录层级不一致才是核心问题；`-planning` / `-decisions` 后缀属于 v1.0 历史痕迹，没有语义价值。
3. **保留 YYYY-MM-DD 日期前缀**：拒。git log 已经提供时序；文件名不重复编码；`{slug}.md` 更易 grep 和引用；与 requirements 已经无日期前缀的惯例对齐。
4. **用嵌套 `docs/process-management/{requirements,designs,tasks}/`**：拒。无必要的三层嵌套；顶级扁平更简单；process-management 名称本身是 v1 残留。
5. **改为聚合式 `docs/work/<slug>/{requirement,design,tasks}.md`**：拒。这是**项目自定义**选项（通过 ARTIFACT_NORMS.md 覆盖可达成），不适合作为 AI Cortex canonical；canonical 应该是 "一类制品一个目录"的最简结构。

## 后果

### 正面

- **认知负担显著降低**：不再有"废弃但保留描述"的幽灵概念；新加入者直接读当前文档就懂
- **三类产出技能路径一致**：`docs/{requirements,designs,tasks}/{slug}.md` 对称并列
- **plan-next 扫描简化**：共享 slug 跨三个平级目录，glob 即可，不需要特殊规则
- **文件名简短**：`docs/designs/user-auth.md` 比 `docs/design-decisions/2026-04-25-user-auth.md` 更易引用、更易 grep
- **git log 作为唯一时序源**：创建/修改日期由 git 管理，不重复编码进文件名
- **spec 规模减小**：删除了 `specs/linking-modes.md` 整个文件（200+ 行）

### 负面

- **第三次 MAJOR bump**（v6.3 → v7.0 → v8.0 → v9.0）：频繁版本迭代，外部消费者信心受损
- **破坏现有项目路径**：使用 `docs/requirements-planning/` 等旧路径的项目需要：
  - 迁移文件到新路径，OR
  - 在 `ARTIFACT_NORMS.md` 显式声明覆盖为旧路径
- **git rename 检测依赖**：文件重命名需要 git follow 跟踪历史（通常自动）

### 中性

- **Stage 0 机制不变**：所有产出技能的 Norms Resolution 逻辑保持——本次只改 canonical 默认值
- **upstream_ref 机制不变**：可选 frontmatter 输入 + parent: emit 逻辑保持
- **align-work-item-manifest 不变**：仍通过物理 manifest 文件 glob 检测，不依赖任何 mode 字段
- **保留的其他制品类型**：backlog-item / adr / doc-assessment 各自领域惯例保留

## 迁移

**外部项目迁移清单**：

1. 搜索仓库里 `docs/requirements-planning/`、`docs/design-decisions/`、`docs/process-management/tasks/` 路径下的文件
2. 二选一：
   - **选项 A（推荐）**：`git mv` 到新路径 `docs/{requirements,designs,tasks}/{slug}.md`（去掉日期前缀）
   - **选项 B（保留旧路径）**：在 `docs/ARTIFACT_NORMS.md` 显式覆盖：
     ```yaml
     artifact_types:
       requirements:
         path_patterns: ["docs/requirements-planning/{topic}.md"]
       design:
         path_patterns: ["docs/design-decisions/YYYY-MM-DD-{topic}.md"]
       tasks:
         path_patterns: ["docs/process-management/tasks/YYYY-MM-DD-{topic}.md"]
     ```
3. 若曾在 `ARTIFACT_NORMS.md` 声明过 `linking_mode` 字段 → 删除该字段；参考下表替换为正交机制：

| 原 linking_mode 值 | v9.0 做法 |
|---|---|
| `slug` / `none` | 什么都不用改（默认行为） |
| `colocation` | 在 `artifact_types` 覆盖各类型 `path_pattern` 为聚合式，如 `work/{parent_slug}/<type>.md` |
| `parent-pointer` | 调用下游技能时传 `upstream_ref` |
| `manifest` | 保留清单文件即可；plan-next / align-work-item-manifest 通过物理存在性检测 |
| `mixed` | 各机制独立声明 |

## 回滚

- `v8.0-lts` tag → v8.0.0 完整状态（含软废弃 linking_mode）
- `v7.0-lts` tag → v7.0.0 完整状态（含 linking_mode 运行时消费）
- `v6.3-lts` tag → pre-v7 启发式扫描状态

## 参考

- ADR 003 / 004 / 005 —— linking_mode 概念的引入、落地、回撤历程
- `specs/artifact-contract.md` v5.0 §2 / Appendix A —— 新 canonical 路径表
- `specs/artifact-norms-schema.md` v3.0 —— schema 清理后的字段集
- `skills/analyze-requirements` v3.0 / `design-solution` v3.0 / `breakdown-tasks` v3.0 —— 采用新路径的链接锚点技能
