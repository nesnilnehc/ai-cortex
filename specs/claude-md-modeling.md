---
id: CLAUDE_MD_MODELING_SPEC_V1
name: CLAUDE.md Modeling Schema
description: Spec defining the structural contract of CLAUDE.md across personal, project, and module layers — the long-term memory file auto-loaded by AI coding assistants (Claude Code, Cursor) at session start.
version: 1.0.0
status: active
lifecycle: living
created_at: 2026-05-15
scope: |
  Defines the structural contract for CLAUDE.md files at all three layers
  (~/.claude/CLAUDE.md, repo-root CLAUDE.md, subdirectory CLAUDE.md). Covers
  layer responsibilities, required sections, optional sections, form requirements,
  and relationships to README/CONTRIBUTING/AGENTS.md.
related:
  - ../rules/claude-md-management.md
  - ../docs/architecture/terminology.md
  - ../AGENTS.md
---

# CLAUDE.md 建模规范

> **数据契约**：定义合格 CLAUDE.md 的层级结构、必备章节与形态要求
>
> 配套：写作纪律见 [rules/claude-md-management.md](../rules/claude-md-management.md)

---

## 1. 定位

CLAUDE.md 是项目级长期记忆文件，由 AI 编程助手（Claude Code、Cursor 等）在会话进入仓库时自动加载。其作用是让 AI 第一次出手即符合项目期待，避免每次会话重复解释项目背景。

CLAUDE.md 不是 README 的替代品：README 面向人类读者，CLAUDE.md 面向 AI Agent。两者目标受众不同，因而详略、形态、信息密度均不同。

---

## 2. CLAUDE.md 回答的四个核心问题

每份合格 CLAUDE.md 必须使 AI 能清晰回答以下四个问题：

| 问题 | 描述 |
|---|---|
| **What** | 这是什么项目？面向谁？解决什么问题？ |
| **With** | 使用什么技术栈、运行时与依赖？ |
| **How** | 怎么启动、构建、测试、部署？目录组织如何？ |
| **Don't** | 哪些目录/文件/操作不能动？必须人工确认的边界在哪？ |

后续章节（§5 必备章节、§6 可选章节）均围绕回答这四个问题展开。

§2 是**心智模型**（为什么需要这些章节），§5 是**条目清单**（具体写哪些段），二者不互替。

---

## 3. 适用范围与强制范围

适用于所有为 AI 编程助手准备的 `CLAUDE.md` 文件。

| 层级 | 位置 | 强制范围 |
|---|---|---|
| 项目级 | 仓库根 `CLAUDE.md` | **强制** |
| 模块级 | 子目录 `CLAUDE.md` | **强制**（若存在） |
| 个人级 | `~/.claude/CLAUDE.md` | 引导性（位于用户主目录，不在任一项目仓库内，无法被项目级治理强制；建议遵循 §7 形态要求） |

---

## 4. 三层结构与职责切分

三层职责互不重叠：

| 层级 | 内容 |
|---|---|
| **个人级**（`~/.claude/CLAUDE.md`） | 跨项目的个人协作偏好：语言、风格、通用 rule 引用、个人快捷指令 |
| **项目级**（仓库根 `CLAUDE.md`） | 本项目的技术栈、关键命令、目录约定、核心约束、禁区 |
| **模块级**（子目录 `CLAUDE.md`） | 特定模块的局部补充（仅在 monorepo / 多服务结构下使用） |

跨层不重复：项目级不写"个人偏好"，模块级不重述项目级已声明的全局约束。

---

## 5. 必备章节（项目级）

项目级 CLAUDE.md 必须包含以下章节（顺序可调，但条目不可缺）：

### 5.1 项目概览

2-3 句话说明项目是什么、面向谁、核心价值。不复述 README，只提炼对 AI 决策有影响的信息。

### 5.2 技术栈

语言、框架、运行时版本、包管理器（明确指定避免 AI 用错）、关键依赖及版本约束。

### 5.3 关键命令

启动、构建、测试、lint、部署的标准命令。优先列抽象层命令（如 `make dev`），而非底层组合。

### 5.4 目录结构

仅列对 AI 决策有意义的目录，每条一行说明职责。不复制 `tree` 输出。

### 5.5 核心约定

编码风格、命名规则、Git 提交规范、分支策略、测试要求。

### 5.6 禁区

不能修改的目录/文件、不能调用的 API、必须人工确认的操作。

---

## 6. 可选章节

按需添加：

- **业务术语表**：领域黑话密集的项目必备
- **架构约束**：跨层调用规则、依赖方向
- **Skill 索引**：列出本项目可触发的 Skill 及触发条件
- **外部集成**：数据库、消息队列、第三方 API 的连接说明
- **已知陷阱**：实践中踩过的坑及规避方式

---

## 7. 形态要求

合格的 CLAUDE.md 在形态上须满足：

| 要求 | 含义 |
|---|---|
| **简洁** | 项目级总长 ≤ 300 行；超过则拆模块级或精简 |
| **可执行** | 每条规则可被 AI 直接遵循，不需要再解释 |
| **决策导向** | 每条内容都影响 AI 实际选择；删掉后 AI 行为变差 |
| **就近原则** | 最易违反、最高代价的约束放文末，利用模型对近因敏感的特性 |

---

## 8. 与其他文档的关系

CLAUDE.md 不替代以下文档，应通过链接引用而不复制其内容：

| 文档 | 关系 |
|---|---|
| `README.md` | 面向人类读者的项目介绍；CLAUDE.md 通过链接引用 |
| `CONTRIBUTING.md` | 面向贡献者的协作流程；CLAUDE.md 不重复 |
| `AGENTS.md`（若有） | 跨 Agent 的契约与权威边界；CLAUDE.md 服从其约束 |
| 架构文档 | 深度技术设计；CLAUDE.md 仅引用，不内嵌 |

---

## 9. Frontmatter

CLAUDE.md 本身不要求 frontmatter（不同于 spec/rule/skill 等资产文件）。其加载机制由 AI 编程助手内置决定，无需机器可读字段。

---

## 10. 反模式

不合格形态分为两层（具体条目与禁止理由由 Rule 单一权威承载，本 Spec 仅给出范畴划分）：

| 层 | 含义 | 权威清单 |
|---|---|---|
| **表达层反模式** | 散文化论证、模糊措辞、缺少强标注——使 AI 难以遵循明确约束 | [rules/claude-md-management.md §2 表达方式](../rules/claude-md-management.md#§2-表达方式) |
| **内容层反模式** | 通用知识冗余、易变状态、敏感信息、外部文档复述、预测性规则——使 CLAUDE.md 偏离"长期记忆"定位 | [rules/claude-md-management.md §3 内容禁区](../rules/claude-md-management.md#§3-内容禁区) |

---

## 变更记录

### 1.0.0 — 2026-05-15

**Initial Release**：定义三层结构（个人 / 项目 / 模块）、四问心智模型、6 项必备章节、形态要求与反模式清单。配套写作纪律见 [rules/claude-md-management.md](../rules/claude-md-management.md)。
