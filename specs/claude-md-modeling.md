---
id: CLAUDE_MD_MODELING_SPEC_V2
name: CLAUDE.md Modeling Schema
description: Spec defining the structural contract of CLAUDE.md across personal, project, and module layers — the long-term memory file auto-loaded by AI coding assistants at session start.
version: 2.0.0
status: active
lifecycle: living
created_at: 2026-05-15
scope: |
  Defines the structural contract for CLAUDE.md files at all three layers
  (~/.claude/CLAUDE.md, repo-root CLAUDE.md, subdirectory CLAUDE.md). Covers
  layer responsibilities, required sections, optional sections, and form requirements.
related:
  - ./spec-modeling.md
  - ../rules/claude-md-management.md
---

# CLAUDE.md 建模规范

> **数据契约**：定义合格 CLAUDE.md 的层级结构、必备章节与形态要求

---

## 1. 定位与适用范围

CLAUDE.md 是项目级长期记忆文件，由 AI 编程助手（Claude Code、Cursor 等）在会话进入仓库时自动加载。其作用是让 AI 第一次出手即符合项目期待，避免每次会话重复解释项目背景。

CLAUDE.md 不是 README 的替代品：README 面向人类读者，CLAUDE.md 面向 AI Agent。两者目标受众不同，因而详略、形态、信息密度均不同。

### 1.1 适用层级

| 层级 | 位置 | 强制范围 |
|---|---|---|
| 项目级 | 仓库根 `CLAUDE.md` | 强制 |
| 模块级 | 子目录 `CLAUDE.md` | 强制（若存在） |
| 个人级 | `~/.claude/CLAUDE.md` | 引导性（位于用户主目录，不在任一项目仓库内，无法被项目级治理强制；建议遵循 §5.4 形态要求） |

---

## 2. 心智模型（Mental Model）

> 一份合格 CLAUDE.md 必使 AI 能清晰回答的四个核心问题。

| 问题 | 描述 |
|---|---|
| **What** | 这是什么项目？面向谁？解决什么问题？ |
| **With** | 使用什么技术栈、运行时与依赖？ |
| **How** | 怎么启动、构建、测试、部署？目录组织如何？ |
| **Don't** | 哪些目录 / 文件 / 操作不能动？必须人工确认的边界在哪？ |

§5 正文结构契约定义的章节均围绕回答这四个问题展开。

---

## 5. 正文结构契约

### 5.1 三层结构与职责切分

三层职责互不重叠：

| 层级 | 内容 |
|---|---|
| **个人级**（`~/.claude/CLAUDE.md`） | 跨项目的个人协作偏好：语言、风格、通用 rule 引用、个人快捷指令 |
| **项目级**（仓库根 `CLAUDE.md`） | 本项目的技术栈、关键命令、目录约定、核心约束、禁区 |
| **模块级**（子目录 `CLAUDE.md`） | 特定模块的局部补充（仅在 monorepo / 多服务结构下使用） |

跨层不重复：项目级不写"个人偏好"，模块级不重述项目级已声明的全局约束。

### 5.2 必备章节（项目级）

项目级 CLAUDE.md 必须包含以下章节（顺序可调，但条目不可缺）：

| 章节 | 内容 |
|---|---|
| 项目概览 | 2-3 句话说明项目是什么、面向谁、核心价值。不复述 README，只提炼对 AI 决策有影响的信息 |
| 技术栈 | 语言、框架、运行时版本、包管理器（明确指定避免 AI 用错）、关键依赖及版本约束 |
| 关键命令 | 启动、构建、测试、lint、部署的标准命令。优先列抽象层命令（如 `make dev`），而非底层组合 |
| 目录结构 | 仅列对 AI 决策有意义的目录，每条一行说明职责。不复制 `tree` 输出 |
| 核心约定 | 编码风格、命名规则、Git 提交规范、分支策略、测试要求 |
| 禁区 | 不能修改的目录 / 文件、不能调用的 API、必须人工确认的操作 |

### 5.3 可选章节

按需添加：

- 业务术语表：领域黑话密集的项目必备
- 架构约束：跨层调用规则、依赖方向
- Skill 索引：列出本项目可触发的 Skill 及触发条件
- 外部集成：数据库、消息队列、第三方 API 的连接说明
- 已知陷阱：实践中踩过的坑及规避方式

### 5.4 形态要求

合格的 CLAUDE.md 在形态上须满足：

| 要求 | 含义 |
|---|---|
| 简洁 | 项目级总长 ≤ 300 行；超过则拆模块级或精简 |
| 可执行 | 每条规则可被 AI 直接遵循，不需要再解释 |
| 决策导向 | 每条内容都影响 AI 实际选择；删掉后 AI 行为变差 |
| 就近原则 | 最易违反、最高代价的约束放文末，利用模型对近因敏感的特性 |

---

## 6. 反模式

不合格形态分为两层（具体条目与禁止理由由 [rules/claude-md-management.md](../rules/claude-md-management.md) 单一权威承载，本 spec 仅给出范畴划分）：

| 层 | 含义 | 权威清单 |
|---|---|---|
| 表达层反模式 | 散文化论证、模糊措辞、缺少强标注——使 AI 难以遵循明确约束 | [rules/claude-md-management.md §2 表达方式](../rules/claude-md-management.md) |
| 内容层反模式 | 通用知识冗余、易变状态、敏感信息、外部文档复述、预测性规则——使 CLAUDE.md 偏离"长期记忆"定位 | [rules/claude-md-management.md §3 内容禁区](../rules/claude-md-management.md) |

---

## 7. 示例

### 7.1 最小合规项目级 CLAUDE.md

````markdown
# CLAUDE.md

Claude Code 在本仓库工作时的简报。

## 项目概览

跨平台日志聚合工具，面向 SRE 团队，将多源日志归一并提供查询 UI。

## 技术栈

- Node.js 20 + TypeScript 5
- pnpm（**NEVER** 用 npm 或 yarn——锁文件不兼容）
- Vitest 测试 / Biome lint

## 关键命令

- `pnpm dev` — 启动开发服务器（localhost:3000）
- `pnpm test` — 运行全部测试
- `pnpm lint` — Biome 检查

## 目录结构

- `src/agents/` — 日志采集器（与具体平台对接）
- `src/aggregator/` — 聚合逻辑
- `src/api/` — REST endpoints
- `db/migrations/` — Drizzle schema

## 核心约定

- 提交格式：Conventional Commits（`feat:` / `fix:` / `refactor:`）
- 新功能必须含测试；覆盖率 ≥ 80%
- 数据库迁移用 `pnpm db:gen` 生成，**NEVER** 手写 SQL

## 禁区

- **NEVER**：直接修改 `db/migrations/*.sql`——总是用 Drizzle 重新生成
- **NEVER**：在 `src/agents/` 内引入第三方 SDK——agents 必须保持极小依赖面
- **ALWAYS**：修改 `src/api/auth/` 前人工确认（涉及鉴权敏感路径）
````

注：本示例为最小骨架，实际项目可按 §5.3 增加可选章节（业务术语、架构约束等）。

---

## 8. 与其他资产关系

### 8.1 配套 rule

[rules/claude-md-management.md](../rules/claude-md-management.md)——CLAUDE.md 写作纪律（篇幅控制、表达方式、内容禁区、修订原则、自检清单）。

### 8.2 与其他文档的边界

CLAUDE.md 不替代以下文档，应通过链接引用而不复制其内容：

| 文档 | 关系 |
|---|---|
| `README.md` | 面向人类读者的项目介绍；CLAUDE.md 通过链接引用 |
| `CONTRIBUTING.md` | 面向贡献者的协作流程；CLAUDE.md 不重复 |
| `AGENTS.md`（若有） | 跨 Agent 的契约与权威边界；CLAUDE.md 服从其约束 |
| 架构文档 | 深度技术设计；CLAUDE.md 仅引用，不内嵌 |

### 8.3 加载与递归基础

- CLAUDE.md 的加载由 AI 编程助手内置决定，无需 frontmatter 标记
- 本 spec 自身遵循 [spec-modeling.md](./spec-modeling.md) v2.0.0 的 8 节骨架；跳过 §3（固定文件名）与 §4（无 frontmatter）
