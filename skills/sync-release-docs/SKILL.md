---
name: sync-release-docs
description: Sync project documentation after release. Reads all docs, cross-references the diff, updates README/ARCHITECTURE/CONTRIBUTING/CLAUDE.md to match what shipped, polishes CHANGELOG voice, cleans up TODOS. Use when asked to "update the docs", "sync documentation", or "post-ship docs".
description_zh: 发版后同步项目文档：交叉引用 diff，更新 README/ARCHITECTURE/CONTRIBUTING/CLAUDE.md，润色 CHANGELOG，清理 TODOS。发版后或 PR 合并后建议使用。
tags: [documentation, workflow]
version: 1.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
  evolution:
    sources:
      - name: "document-release"
        repo: "https://github.com/nesnilnehc/gstack"
        version: "1.0.0"
        license: "MIT"
        type: "fork"
        borrowed: "Post-ship doc audit workflow, per-file heuristics, CHANGELOG polish rules, cross-doc consistency check"
    enhancements:
      - "Platform-agnostic: base_branch from CLAUDE.md or .ai-cortex/config.yaml"
      - "spec/artifact-contract.md path alignment"
      - "Removed gstack preamble, telemetry, hooks"
triggers: [sync docs, post-ship docs, update documentation, document release]
input_schema:
  type: free-form
  description: Optional base branch name; otherwise detected from project config
output_schema:
  type: side-effect
  description: Updated documentation files committed; structured doc health summary
---

# 技能 (Skill)：发版后同步文档

## 目的 (Purpose)

在代码发版或 PR 合并后，确保项目文档（README、ARCHITECTURE、CONTRIBUTING、CLAUDE.md、CHANGELOG、TODOS）与已交付变更一致，保持可发现性与跨文档一致性。

---

## 核心目标（Core Objective）

**首要目标**：产出与发版变更一致的文档更新；事实性修正自动完成，主观或风险性变更经用户确认。

**成功标准**（必须满足所有要求）：

1. ✅ **基准分支已检测**：从 CLAUDE.md、`.ai-cortex/config.yaml` 或 `gh` 推断 base branch；参见 [docs/guides/project-config.md](../../docs/guides/project-config.md)
2. ✅ **Diff 与逐文件审计**：`git diff`、`git log` 已执行；README、ARCHITECTURE、CONTRIBUTING、CLAUDE.md 已对照 diff 核对；分类为 Auto-update 或 Ask user
3. ✅ **CHANGELOG 仅润色**：不重写、不删除、不替换既有条目；VERSION 变更须经 AskUserQuestion 确认
4. ✅ **跨文档一致性**：版本号、能力列表、可发现性链接已核对
5. ✅ **变更已提交**：若有修改，单次 commit 并输出 doc health summary

**验收测试**：新贡献者能否仅凭 README/CONTRIBUTING 正确完成首次贡献流程？

---

## 范围边界（Scope Boundaries）

**本技能负责**：

- 发版后文档事实性更新（路径、计数、能力列表、示例）
- CHANGELOG 措辞润色（非重写）
- TODOS.md 已完成项标记、交叉引用
- 跨文档一致性检查与可发现性（README/CLAUDE 链接）
- 文档健康状态摘要输出

**本技能不负责**：

- 建立或更新制品规范（使用 `discover-docs-norms`）
- 文档健康评估与缺口计划（使用 `assess-docs`）
- 从零引导文档结构（使用 `bootstrap-docs`）
- 提交代码变更（本技能仅更新文档并 commit）

**转交点**：文档同步完成后，移交给后续发版流程或下一个任务。若发现规范违规，建议运行 `assess-docs`。

---

## 使用场景（Use Cases）

- 用户要求发版后更新文档、同步文档或 post-ship docs
- PR 已创建或合并，需确保文档与变更一致
- CHANGELOG 措辞需润色为面向用户的语气
- 跨文档版本号或能力列表不一致需修复

---

## 行为（Behavior）

### 前置：检测基准分支

1. 若存在 `CLAUDE.md` 或 `.ai-cortex/config.yaml`，优先读取 `base_branch`
2. 否则：`gh pr view --json baseRefName -q .baseRefName`（若有 PR）；失败则 `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`；均失败则 `main`
3. 输出检测到的 base branch

### Step 1：Pre-flight 与 Diff 分析

1. 若当前在 base branch，中止："请在 feature branch 上运行。"
2. 执行：`git diff <base>...HEAD --stat`、`git log <base>..HEAD --oneline`、`git diff <base>...HEAD --name-only`
3. 发现文档文件：`find . -maxdepth 2 -name "*.md" -not -path "./.git/*" -not -path "./node_modules/*" | sort`
4. 将变更分类：新功能、行为变更、移除、基础设施
5. 输出："分析 N 个文件变更、M 次提交，发现 K 个文档待审核。"

### Step 2：逐文件文档审计

对 README、ARCHITECTURE、CONTRIBUTING、CLAUDE.md 及项目内其他 .md：

- **README**：能力/功能列表是否与 diff 一致？安装/示例是否仍正确？
- **ARCHITECTURE**：组件与设计说明是否与代码一致？仅更新被 diff 明确否定的内容
- **CONTRIBUTING**：新贡献者按步骤能否成功？命令是否有效？
- **CLAUDE.md**：项目结构、命令是否准确？

每项更新分类为 **Auto-update**（事实性、diff 明确）或 **Ask user**（叙述性、大面积重写、安全模型、歧义）。

### Step 3：应用 Auto-update

对明确的事实性更新直接使用 Edit 工具修改。每处修改输出一行摘要（具体改了什么）。

**禁止自动更新**：README 定位、ARCHITECTURE 设计理由、安全模型、删除整节。

### Step 4：风险变更确认

对 Step 2 标记为 Ask user 的项，使用 AskUserQuestion，附 RECOMMENDATION 与选项（含 Skip）。用户确认后立即应用。

### Step 5：CHANGELOG 措辞润色

**禁止重写或替换 CHANGELOG 条目。**

- 仅修改既有条目内措辞；不删除、不重排、不整体替换
- 语气：面向用户；突出「可做什么」而非实现细节
- 若有问题，用 AskUserQuestion，不静默修复

### Step 6：跨文档一致性与可发现性

- README 能力列表与 CLAUDE.md 一致？
- ARCHITECTURE 与 CONTRIBUTING 结构一致？
- CHANGELOG 版本与 VERSION 文件一致？
- 每个文档是否可从 README 或 CLAUDE 链接到达？

### Step 7：TODOS.md 清理

若存在 TODOS.md：将 diff 明确完成的项移至 Completed；保守标记。可选：检查 diff 中的 TODO/FIXME 是否应进入 TODOS。

### Step 8：VERSION bump 确认

**禁止擅自 bump VERSION。**

- 若 VERSION 已在本 branch 修改：检查 CHANGELOG 是否覆盖全部变更
- 若未修改：AskUserQuestion（A) Bump PATCH B) Bump MINOR C) Skip）
- 推荐 C（仅文档变更通常不需 bump）

### Step 9：提交与输出

- 若无文档修改：输出 "All documentation is up to date." 并结束
- 若有修改：`git add <files>`、`git commit -m "docs: sync documentation for release"`、输出 doc health summary

**Doc health summary 格式**：

```
Documentation health:
  README.md       [Updated|Current] (description)
  ARCHITECTURE.md [Updated|Current|—] (description)
  CONTRIBUTING.md [Updated|Current|—] (description)
  CHANGELOG.md    [Voice polished|Current|—] (description)
  TODOS.md        [Updated|Current|—] (description)
  VERSION         [Not bumped|Already bumped|Skipped] (description)
```

---

## 输入与输出 (Input & Output)

### 输入

- 可选：base branch 名称；否则从项目配置或 `gh` 推断
- 包含未合并文档变更的 feature branch

### 产出

- 更新的文档文件（若有）及单次 commit
- 结构化的 doc health summary

---

## 限制（Restrictions）

### 硬边界

- 不重写、不替换、不删除 CHANGELOG 既有条目
- 不擅自 bump VERSION；始终用户确认
- 不使用 Write 覆盖 CHANGELOG；使用 Edit 精确匹配
- 不在 base branch 上运行

### 技能边界 (Skill Boundaries)

**不要做这些（其他技能可以处理它们）**：

- **建立规范**：使用 `discover-docs-norms`
- **评估文档健康**：使用 `assess-docs`
- **引导文档结构**：使用 `bootstrap-docs`

---

## 自检（Self-Check）

### 成功标准

- [ ] 基准分支已正确检测
- [ ] Diff 已分析并分类
- [ ] 逐文件审计已完成；Auto-update 已应用
- [ ] CHANGELOG 仅润色，未重写
- [ ] VERSION 变更经用户确认
- [ ] 跨文档一致性已核对
- [ ] 若有修改，已 commit 并输出 summary

### 验收测试

新贡献者能否仅凭 README/CONTRIBUTING 完成首次贡献？

---

## 示例（Examples）

### 示例 1：功能发版后同步

**场景**：新技能 `sync-release-docs` 已合并，需更新 README 能力表与 CHANGELOG。

**步骤**：检测 base branch → 分析 diff → 发现 README 缺新技能、CHANGELOG 已有条目 → Auto-update README 表 → 润色 CHANGELOG 措辞 → 确认不 bump VERSION → commit。

### 示例 2：无变更

**场景**：文档已与 diff 一致。

**输出**：`All documentation is up to date.`
