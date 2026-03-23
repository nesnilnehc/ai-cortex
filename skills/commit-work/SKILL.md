---
name: commit-work
description: Create high-quality git commits with clear messages and logical scope. Core goal - produce reviewable commits following Conventional Commits format with pre-commit quality checks.
description_zh: 创建高质量 git 提交：清晰消息与合理范围；遵循 Conventional Commits，含 pre-commit 质量检查。
tags: [git, workflow, automation]
version: 2.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
  evolution:
    sources:
      - name: "commit-work"
        repo: "https://github.com/anthropics/skills (assumed)"
        version: "1.0.0"
        license: "MIT"
        type: "fork"
        borrowed: "Core workflow, Conventional Commits format, patch staging approach"
      - name: "review-diff"
        repo: "https://github.com/nesnilnehc/ai-cortex"
        version: "1.3.0"
        license: "MIT"
        type: "integration"
        borrowed: "Pre-commit review methodology"
    enhancements:
      - "Integrated review-diff for pre-commit quality checks"
      - "Added spec/skill.md compliance verification"
      - "Auto-sync with skills/INDEX.md and manifest.json"
      - "Enhanced Self-Check with AI Cortex standards"
triggers: [commit, commit work]
aliases: [cw]
input_schema:
  type: free-form
  description: Staged and unstaged changes in the working tree to commit
output_schema:
  type: side-effect
  description: One or more git commits with Conventional Commits messages
---

# 技能（Skill）：承诺工作

## 目的 (Purpose)

通过确保仅包含预期的更改、提交的逻辑范围以及提交消息清楚地描述更改的内容和原因，使提交易于审查且安全交付。该技能使用技能规范集成了项目的 AI Cortex 治理标准。

---

## 核心目标（Core Objective）

**首要目标**：生成一个或多个 git 提交，其中包含清晰的消息、逻辑范围和经过验证的质量，可供推送。

**成功标准**（必须满足所有要求）：

1. ✅ **已审查的更改**：在暂存之前运行“git diff”，在每次提交之前运行“git diff --cached”
2. ✅ **逻辑范围**：每次提交仅包含相关更改；不相关的更改分为单独的提交
3. ✅ **常规提交格式**：所有提交消息均遵循 `type(scope):summary` 格式，正文清晰
4. ✅ **质量验证**：运行适当的测试、lint 或构建命令并且所有检查均已通过
5. ✅ **无敏感数据**：不包含秘密、令牌、调试代码或意外更改
6. ✅ **注册表同步**（AI Cortex 项目）：如果技能/更改，则 INDEX.md 和 manifest.json 都会更新

**验收**测试：审阅者是否可以仅从提交消息中了解更改的内容以及原因，而无需阅读差异？

---

## 范围边界（范围边界）

**本技能负责**：

- 审查未提交的更改
- 将混合更改拆分为逻辑提交
- 需要时使用补丁模式进行暂存更改
- 编写常规提交消息
- 运行预提交质量检查
- 同步 AI Cortex 注册表（INDEX.md、manifest.json）

**本技能不负责**：

- 现有提交的代码审查（使用“review-diff”技能）
- 重写 git 历史记录或变基（使用 git rebase 命令）
- 解决合并冲突（使用 git merge/rebase 工作流）
- 创建拉取请求或推送到远程（单独的工作流）

**转交点**：当所有变更都提交并验证后，移交给推送/PR 工作流或下一个开发任务。

## 使用场景（用例）

- 用户要求提交工作、阶段更改或制作提交消息
- 需要将混合更改拆分为逻辑的、可审查的提交
- 创建遵循常规提交格式的提交
- 在推动之前确保提交符合项目质量标准
- 在AI Cortex项目中工作，其中INDEX.md和manifest.json必须保持同步

## 行为（行为）

### 工作流程（清单）

若存在 `CLAUDE.md` 或 `.ai-cortex/config.yaml`，优先读取其中的 `test_command` 用于质量验证；否则从项目构建配置推断。参见 [docs/guides/project-config.md](../../docs/guides/project-config.md)。

1) **在登台前检查工作树**
   - 运行`git status`
   - 运行“git diff”（未暂存的更改）
   - 如果有很多更改：`git diff --stat` 进行概述

2) **运行预提交审查（AI Cortex 增强）**
   - 调用“review-diff”技能来检查：
     - 意外的更改或调试代码
     - 安全问题或泄露的秘密
     - 重大更改或兼容性问题
   - 在进行分期之前解决发现的问题

3) **决定提交边界（如果需要则分割）**
   - 按逻辑问题划分：
     - 功能与重构
     - 后端与前端
     - 格式与逻辑
     - 测试与生产代码
     - 依赖性颠簸与行为改变
   - 如果更改混合在一个文件中，则计划使用补丁暂存

4) **仅暂存属于下一次提交的内容**
   - 更喜欢混合更改的补丁暂存：`git add -p`
   - 要取消暂存块/文件： `git restore --staged -p` 或 `git Restore --staged <path>`
   - 阶段相关的变化一起

5) **审查实际要提交的内容**
   - 运行“git diff --cached”
   - 健全性检查：
     - 没有秘密或代币
     - 没有意外的调试日志记录
     - 没有不相关的格式改动
     - 没有注释掉的代码块

6) **用 1-2 句话描述阶段性变化**
   - 回答：“什么改变了？” +“为什么？”
   - 如果你不能清楚地描述它，则提交可能太大或混合；返回步骤 3

7) **写入提交消息**
   - 使用常规提交（必需）：

     
```text
     type(scope): short summary
     
     body (what/why, not implementation diary)
     
     footer (BREAKING CHANGE) if needed
     ```


   - 更喜欢多行消息的编辑器：`git commit -v`
   - Use `references/commit-message-template.md` if helpful
   - 保持摘要的必要性和具体性（“添加”、“修复”、“删除”、“重构”）

8) **运行最小相关验证**
   - 在继续之前运行存储库最快的有意义的检查（单元测试、lint 或构建）
   - 确保提交不会破坏现有功能

9) **如果需要，同步注册表（仅限 AI Cortex 项目）**
   - 如果提交影响 `skills/` 目录：
     - 验证“skills/INDEX.md”是否已更新为新的/更改的技能
     - 验证“manifest.json”功能数组是否已更新
     - 如果添加、删除或重大更改了技能，则验证 manifest.json 与 INDEX 已同步
     - 运行“scripts/verify-registry.mjs”（如果存在）
   - 如果添加或移动技能，INDEX、清单和（根据需要）场景地图必须一起更新

10) **重复下一次提交，直到工作树干净**

### 交互（互动）政策

- 询问用户是否想要单个或多个提交（默认：针对不相关的更改进行多个小提交）
- 确认提交风格需求（该技能需要常规提交）
- 询问任何特定于项目的规则：最大主题长度、所需范围等。
- 对于 AI Cortex 项目：确认是否运行注册表同步检查

## 输入与输出 (Input & Output)

### 输入（输入）要求

- 包含未提交更改的 git 存储库
- 用户意图：应该致力于哪些工作
- 可选：提交样式首选项、范围规则

### 产出（Output）合约

提供：

- 最终提交消息，包含类型、范围和清晰的描述
- 每次提交的简短摘要，解释发生了什么变化以及原因
- 用于暂存和审查的命令（至少：`git diff --cached`）
- 运行任何测试或验证命令
- 对于 AI Cortex 项目：确认 INDEX.md、manifest.json 已同步

## 限制（限制）

### 硬边界（Hard Boundaries）

- 在未审查分阶段更改的情况下不要提交（`git diff --cached`）
- 不要在一次提交中混合不相关的更改
- 不要编写模糊的提交消息（“修复内容”、“更新”、“WIP”）
- 如果测试或 linter 可用，请勿跳过验证步骤
- 不要提交秘密、令牌或敏感数据
- 对于 AI Cortex 项目：在未更新 INDEX.md、manifest.json 的情况下，请勿提交技能更改

### 技能边界 (Skill Boundaries)（避免重叠）

**不要做这些（其他技能可以处理它们）**：

- **现有提交的代码审查**：审查已提交的差异 → 使用“review-diff”技能
- **Git 历史重写**：变基、压缩、修改旧提交 → 直接使用 git rebase/amend 命令
- **合并冲突解决**：解决合并/变基期间的冲突 → 使用 git merge/rebase 工作流程
- **拉取请求创建**：创建 PR、请求审查、管理 PR 工作流程 → 使用特定于平台的 PR 工具
- **代码实施**：编写正在提交的代码更改→使用开发/实施技能

**何时停止并交接**：

- 用户问“你能审查这个提交吗？” → 对现有提交使用“review-diff”技能
- 用户问“你能推这个吗？” → 提交完成，移交推送/公关工作流程
- 用户问“你可以重新调整这些提交的基础吗？” → 提交完成，移交给 git rebase 工作流程
- 提交并验证所有更改 → 技能完成，准备好推送或下一个任务

## 自检（Self-Check）

### 核心成功标准（必须满足所有标准）

- [ ] **已审查的更改**：在暂存之前运行“git diff”，在每次提交之前运行“git diff --cached”
- [ ] **逻辑范围**：每次提交仅包含相关更改；不相关的更改分为单独的提交
- [ ] **常规提交格式**：所有提交消息均遵循“类型（范围）：摘要”格式，正文清晰
- [ ] **质量验证**：运行适当的测试、lint 或构建命令并且所有检查均已通过
- [ ] **无敏感数据**：不包含秘密、令牌、调试代码或意外更改
- [ ] **注册表同步**（AI Cortex 项目）：如果技能变更，则更新 INDEX.md、manifest.json

### 流程质量检查

- [ ] **提交前审查**：为 AI Cortex 项目运行“review-diff”技能，以检查是否存在意外更改、安全问题或重大更改
- [ ] **使用补丁暂存**：当更改混合在单个文件中时使用`git add -p`
- [ ] **提交边界清晰**：可以用 1-2 句话描述每个提交的目的
- [ ] **消息质量**：摘要是必要且具体的；正文解释了内容和原因（不是实现细节）
- [ ] **Breaking changes marked**: Used `!` or `BREAKING CHANGE:` footer if applicable
- [ ] **记录的命令**：列出用于暂存、审查和验证的命令

### 验收测试

**审阅者可以仅从提交消息中了解更改的内容和原因，而不阅读差异吗？**

如果否：提交消息不清楚。修改消息以解释内容和原因。

如果是：提交已准备好推送。

## 示例（示例）

### 示例 1：简单的功能添加

**场景**：向 utils.js 添加新函数

**命令**：


```bash
git status
git diff
# Review shows only the new function, no other changes
git add utils.js
git diff --cached
# Verify staged changes are correct
npm test
git commit -m "feat(utils): add formatDate helper function

Add formatDate to handle ISO 8601 date formatting consistently
across the application. Returns formatted string or null for
invalid inputs."
```


**输出**：

- 提交：`feat(utils)：添加 formatDate 辅助函数`
- 摘要：添加了日期格式化实用程序以集中日期处理逻辑
- 命令：`git diff`、`git diff --cached`、`npm test`

### 示例 2：需要拆分的混合更改（边缘情况）

**场景**：修改了 auth.js，修复了错误并进行了重构，并更新了测试

**命令**：


```bash
git status
git diff --stat
# Shows auth.js and auth.test.js changed

# Run review-diff first (AI Cortex)
# [review-diff identifies: bug fix in line 45, refactor in lines 100-150]

# Split into logical commits
# Commit 1: Bug fix only
git add -p auth.js
# Select only the bug fix hunk
git diff --cached
npm test
git commit -m "fix(auth): prevent null pointer in token validation

Check for null token before accessing properties to avoid
runtime errors when token is missing."

# Commit 2: Refactor
git add -p auth.js
# Select refactor hunks
git diff --cached
npm test
git commit -m "refactor(auth): extract token parsing to separate function

Move token parsing logic into parseAuthToken() for better
testability and reuse across auth module."

# Commit 3: Tests
git add auth.test.js
git diff --cached
npm test
git commit -m "test(auth): add tests for token validation edge cases

Cover null token, malformed token, and expired token scenarios."
```


**输出**：

- 提交 1：“修复（auth）：在令牌验证中防止空指针” - 修复了令牌为空时的崩溃
- 提交 2：“重构（auth）：将令牌解析提取到单独的函数” - 改进的代码组织
- 提交 3：“测试（auth）：添加令牌验证边缘情况的测试” - 增加测试覆盖率
- 命令：`git add -p`、`git diff --cached` (×3)、`npm test` (×3)

### 示例 3：AI Cortex 技能添加（边缘情况）

**场景**：为 AI Cortex 项目添加新技能“analyze-logs”

**命令**：


```bash
git status
# Shows: skills/analyze-logs/SKILL.md (new), skills/INDEX.md (modified), manifest.json (modified)

git diff skills/INDEX.md
git diff manifest.json
# Verify both registries reference the new skill correctly

git add skills/analyze-logs/
git add skills/INDEX.md
git add manifest.json
git diff --cached

# Run registry verification
node scripts/verify-registry.mjs
# ✓ INDEX.md and manifest.json are synchronized

npm test
git commit -m "feat(skills): add analyze-logs skill for log parsing

Add new skill to parse and analyze application logs with pattern
matching and error extraction. Includes examples for common log
formats.

Updated INDEX.md and manifest.json to register the new skill."
```


**输出**：

- 提交：`feat(skills)：添加分析日志技能以进行日志解析`
- 摘要：添加了带有注册表同步的日志分析功能
- 命令：`git diff --cached`、`node script/verify-registry.mjs`、`npm test`
- 注册表同步：✓ INDEX.md 和 manifest.json 均已更新

---

## 附录：输出合约

该技能会产生副作用输出（git 提交）和报告。输出报告必须包括：

|元素|要求 |
| :--- | :--- |
| **提交消息** |常规提交格式：`类型（范围）：主题` + 正文 + 可选页脚 |
| **每次提交摘要** |一句话：改变了什么以及为什么改变|
| **使用的命令** |最小值：`git diff --cached`；包括暂存和验证命令 |
| **注册表同步** | 对于 AI Cortex 项目：确认 INDEX.md、manifest.json 已同步 |

报告示例：

- 提交：`feat(utils)：添加 formatDate 辅助函数`
- 摘要：添加了日期格式化实用程序以集中日期处理逻辑
- 命令：`git diff`、`git diff --cached`、`npm test`