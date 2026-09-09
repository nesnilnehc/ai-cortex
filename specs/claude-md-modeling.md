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

# CLAUDE.md Modeling Schema

> **Data contract**: defines the level structure, required sections and form requirements of a sound CLAUDE.md

---

## 1. Position and scope

CLAUDE.md is a project-level long-term memory file, loaded automatically by AI coding assistants such as Claude Code and Cursor when a session enters the repository. Its purpose is for the AI to meet the project's expectations on its first move, so the project background does not have to be re-explained every session.

CLAUDE.md does not replace the README. A README addresses human readers; CLAUDE.md addresses an AI agent. Different audiences make for different depth, form and information density.

### 1.1 Levels it applies to

| Level | Location | Enforcement |
|---|---|---|
| Project | `CLAUDE.md` at the repository root | Enforced |
| Module | `CLAUDE.md` in a subdirectory | Enforced where one exists |
| Personal | `~/.claude/CLAUDE.md` | Advisory. It lives in the user's home directory, outside any project repository, so project governance cannot enforce it; following the §5.4 form requirements is recommended |

---

## 2. Mental model

> The four core questions a sound CLAUDE.md must let the AI answer clearly.

| Question | Description |
|---|---|
| **What** | What project is this? Who is it for? What problem does it solve? |
| **With** | Which stack, runtime and dependencies does it use? |
| **How** | How is it started, built, tested and deployed? How are the directories organised? |
| **Don't** | Which directories, files or operations are off limits? Where is the boundary that requires human confirmation? |

Every section the body structure contract defines in §5 exists to answer one of these four questions.

---

## 5. Body structure contract

### 5.1 The three levels and how responsibility divides

The three levels do not overlap:

| Level | Contents |
|---|---|
| **Personal** (`~/.claude/CLAUDE.md`) | Cross-project personal collaboration preferences: language, style, references to general rules, personal shortcuts |
| **Project** (`CLAUDE.md` at the repository root) | This project's stack, key commands, directory conventions, core constraints and no-go zones |
| **Module** (`CLAUDE.md` in a subdirectory) | Local additions for one module, used only in a monorepo or multi-service layout |

No repetition across levels: the project level does not carry personal preferences, and the module level does not restate a global constraint the project level already declared.

### 5.2 Required sections at project level

A project-level CLAUDE.md must contain these sections. The order may vary, but none may be missing:

| Section | Contents |
|---|---|
| Project overview | 2-3 sentences on what the project is, who it is for and its core value. Not a restatement of the README — only what bears on the AI's decisions |
| Stack | Language, framework, runtime version, package manager — name it explicitly to avoid the AI reaching for the wrong one — plus key dependencies and version constraints |
| Key commands | The standard commands to start, build, test, lint and deploy. Prefer the higher-level command such as `make dev` over the underlying composition |
| Directory structure | Only the directories that bear on the AI's decisions, one line of responsibility each. Not a copy of `tree` output |
| Core conventions | Coding style, naming rules, commit conventions, branching strategy, testing requirements |
| No-go zones | Directories and files that must not be modified, APIs that must not be called, operations requiring human confirmation |

### 5.3 Optional sections

Add as needed:

- Domain glossary: required in a project dense with domain jargon
- Architecture constraints: cross-layer call rules, dependency direction
- Skill index: which skills this project can trigger, and on what conditions
- External integrations: how to connect to databases, message queues and third-party APIs
- Known traps: pitfalls hit in practice and how to avoid them

### 5.4 Form requirements

A sound CLAUDE.md must satisfy these:

| Requirement | Meaning |
|---|---|
| Concise | A project-level file is ≤ 300 lines; beyond that, split out a module level or trim |
| Actionable | Every rule can be followed directly by the AI, with no further explanation |
| Decision-oriented | Every line changes what the AI actually chooses; deleting it makes the AI's behaviour worse |
| Recency | Put the most easily violated and most costly constraints at the end, exploiting the model's sensitivity to what came last |

---

## 6. Anti-patterns

Unsound forms fall into two layers. The individual items and the reasons they are forbidden live in a single authority, [rules/claude-md-management.md](../rules/claude-md-management.md); this spec gives only the categorisation:

| Layer | Meaning | Authoritative list |
|---|---|---|
| Expression anti-patterns | Prose argumentation, vague wording, missing strong markers — all of which make a clear constraint hard for the AI to follow | [rules/claude-md-management.md §2 Expression](../rules/claude-md-management.md) |
| Content anti-patterns | Redundant general knowledge, volatile state, sensitive material, restatements of external documents, speculative rules — all of which pull CLAUDE.md away from being long-term memory | [rules/claude-md-management.md §3 Content no-go zones](../rules/claude-md-management.md) |

---

## 7. Examples

### 7.1 A minimally compliant project-level CLAUDE.md

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

Note: this example is a minimal skeleton. A real project adds optional sections from §5.3 — domain glossary, architecture constraints and the like.

---

## 8. Relationship to other assets

### 8.1 Paired rule

[rules/claude-md-management.md](../rules/claude-md-management.md) — CLAUDE.md discipline: length limits, expression, content no-go zones, revision principles and the self-check.

### 8.2 Boundary with other documents

CLAUDE.md does not replace the documents below; it links to them rather than copying their content:

| Document | Relationship |
|---|---|
| `README.md` | The project introduction for human readers; CLAUDE.md links to it |
| `CONTRIBUTING.md` | The contribution process; CLAUDE.md does not repeat it |
| `AGENTS.md`, where one exists | The cross-agent contract and authority boundaries; CLAUDE.md defers to its constraints |
| Architecture documents | Deep technical design; CLAUDE.md references them rather than embedding them |

### 8.3 Loading, and the recursive basis

- Loading of CLAUDE.md is built into the AI coding assistant and needs no frontmatter marker
- This spec itself follows the 8-section skeleton of [spec-modeling.md](./spec-modeling.md) v2.0.0, skipping §3 (the filename is fixed) and §4 (there is no frontmatter)
