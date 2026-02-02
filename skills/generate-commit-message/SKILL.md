---
name: generate-commit-message
description: 根据当前 git diff 生成符合 Conventional Commits 规范的专业 Git 提交信息（含 type/scope/subject 与可选的 body/breaking 说明）。
tags: [eng-standards, devops]
version: 1.0.0
recommended_scope: project
---

# Skill: 生成提交信息 (Generate Commit Message)

## 目的 (Purpose)

以**高级工程师对仓库质量负责**的视角，分析当前工作区的 **git diff**（含已暂存与未暂存），生成**符合 Conventional Commits** 的专业 Git 提交信息，便于历史可读、自动化与协作规范。

---

## 适用场景 (Use Cases)

- **提交前**：用户执行 `git add` 后或直接对工作区 diff 生成一条可直接使用的 commit message。
- **规范统一**：团队或项目要求使用 Conventional Commits，需由 Agent 产出标准格式。
- **CI/钩子**：作为 commit-msg 钩子或 PR 模板的参考来源。

**何时使用**：当用户触发「生成提交信息」或 `/commit` 且需要基于**当前分支的本地变更**生成提交信息时。

---

## 行为要求 (Behavior)

### 格式规范

- **第一行**：`<type>(<scope>): <subject>`
- **Type**：使用其一 — `feat` | `fix` | `refactor` | `perf` | `test` | `docs` | `chore` | `build` | `ci` | `revert`。
- **Scope**：若变更明显属于某模块、目录或服务，用其作为 scope；跨模块用 `core`；基建/配置用 `infra`；可不写。
- **Subject**：
  - 祈使语气（"fix"、"add"、"remove"，不用 "fixed"、"added"）。
  - 结尾无句号。
  - 长度 ≤ 72 字符。
  - 描述**做了什么改变**，而非**如何做**。

### 内容要求

- **Bug 修复**：在 subject 或 body 中说明「修了什么问题」。
- **行为/API/数据变更**：在 subject 或 body 中明确写出影响。
- **Body（可选）**：第一行后空一行，可用列表说明：
  - 为何需要该变更
  - 具体改了什么
  - 风险或副作用
- **Breaking Change**：若 diff 显示潜在破坏性变更，在文末追加：`BREAKING CHANGE: <说明>`。

### 输出形式

- **仅输出**：最终可直接用于 `git commit -m "..."` 或 `-F` 的**完整提交信息**，不含解释、评语或多余前缀。
- 若无法从 diff 推断意图（如无变更或仅空白），可输出简短说明并建议用户补充上下文。

---

## 输入与输出 (Input & Output)

### 输入 (Input)

- **git diff**：当前分支相对于 HEAD 的变更（staged + unstaged），由执行方在调用本技能时提供。

### 输出 (Output)

- **标准**：一段符合 Conventional Commits 的提交信息正文（可多行）。
- **无 diff 或无法推断**：一句简短说明（如「未检测到变更，请先 git add 或描述意图」），不虚构 type/scope/subject。

---

## 禁止行为 (Restrictions)

- **禁止**输出除提交信息本身以外的分析报告、建议列表或评论性文字（除非无 diff 时的说明）。
- **禁止**使用非规定的 type 或口语化、模糊的 subject。
- **禁止**在无明确证据时虚构 breaking change。

---

## 质量检查 (Self-Check)

- [ ] 第一行是否严格为 `<type>(<scope>): <subject>` 且 type 在规范列表中？
- [ ] Subject 是否祈使、≤72 字符、无句号？
- [ ] 若有行为/API/数据影响或 bug 修复，是否在 subject 或 body 中写清？
- [ ] 若存在破坏性变更，是否包含 `BREAKING CHANGE:`？
- [ ] 输出是否可直接用于 `git commit`（无多余前缀或说明）？

---

## 示例 (Examples)

### 示例一：功能新增

- **输入**：diff 显示在 `src/auth/` 下新增 JWT 校验逻辑。
- **预期输出**：

```text
feat(auth): add JWT validation for API routes

- Validate token signature and expiry before handler execution
- Return 401 with clear error when token invalid or expired
```

### 示例二：修复与破坏性变更

- **输入**：diff 显示移除某 API 的 `legacy` 查询参数，且调用方需改用新参数。
- **预期输出**：

```text
fix(api): remove legacy query param and enforce new contract

- Drop `legacy` query param; callers must use `version=v2`
- Prevents inconsistent behavior between envs

BREAKING CHANGE: `legacy` query parameter is no longer supported. Use `version=v2` instead.
```

### 边界示例：无变更

- **输入**：无 staged 且 unstaged 无有效变更（或仅空白）。
- **预期行为**：输出一句说明，如「未检测到变更，请先执行 git add 或提供变更说明。」不生成虚构的 type/scope/subject。
