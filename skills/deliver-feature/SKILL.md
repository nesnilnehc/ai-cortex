---
name: deliver-feature
description: From inside a linked worktree, deliver the current feature branch into main — merge with --no-ff, push, and optionally clean up the worktree, all without leaving CWD.
description_zh: 在 linked worktree 内将当前 feature 分支交付到 main——以 --no-ff 合并、推送，并可选清理本 worktree，全程不离开当前目录。
tags: [git, workflow, automation]
version: 1.1.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [deliver feature, finish feature, land feature, merge feature, ship feature, deliver this]
input_schema:
  type: free-form
  description: A linked git worktree on a non-main branch with a clean working tree.
output_schema:
  type: side-effect
  description: One --no-ff merge commit on the main branch in the main repo, pushed to origin; optional worktree removal and feature branch deletion; single-branch summary report.
---

# 技能（Skill）：交付功能（Deliver Feature）

## 目的（Purpose）

在 linked worktree 内将当前功能分支落地到 main，无需切换目录。通过 `git -C <main-repo>` 操作主仓库，用户全程保持在功能 worktree 中，直到明确选择离开为止。省去了"cd 主仓库 → 调用批量工具 → 仅选刚完成的分支 → cd 返回"的来回跳转。

---

## 核心目标（Core Objective）

**首要目标**：将当前 worktree 的功能分支（通过 `--no-ff` 合并）落地到 main，推送到 origin，并让用户决定保留还是移除该 worktree——全程不离开 worktree 目录。

**成功标准**（必须全部满足）：

1. ✅ **调用上下文已验证**：CWD 在 linked worktree 内部（而非主仓库），且当前分支不是 main 分支
2. ✅ **预检通过**：当前 worktree 无未提交变更（`git status --porcelain` 为空）
3. ✅ **在主仓库执行合并，不在 worktree 中执行**：`pull` / `merge --no-ff` / `push` 均通过 `git -C <main-repo>` 完成；合并期间 CWD 始终保持在 worktree
4. ✅ **推送成功**：`git push origin <main-branch>` 返回 0 后才提供清理选项
5. ✅ **用户控制清理**：用户明确选择保留 / 移除（可选分支删除，仅 `-d`）；不隐式移除
6. ✅ **单分支汇总**：报告 merge commit hash、推送状态与清理结果

**验收测试**：技能执行完毕后，`git -C <main-repo> log --oneline <main-branch>` 显示恰好一条新的引用该功能分支的 merge commit；`git -C <main-repo> ls-remote origin <main-branch>` 与本地一致；若用户选择移除，`git worktree list` 不再包含来源 worktree。

---

## 范围边界（Scope Boundaries）

**本技能负责**：

- 验证调用上下文（在 linked worktree 内部，非 main 分支）
- 确定 main 分支（自动检测；仅在无法确定时询问用户）
- 对当前 worktree 进行预检（工作区是否干净）
- 通过 `git worktree list --porcelain` 定位主仓库路径
- 通过 `git -C` 对主仓库执行 pull → `--no-ff` merge → push
- 遇冲突或推送被拒时移交给用户（不自动解决）
- 可选移除 worktree 及删除功能分支（用户确认，仅 `-d`）
- 单分支汇总报告

**本技能不负责**：

- 多 worktree 批量操作（请在主仓库 main 分支上使用 `integrate-branches`）
- 提交未提交的变更（请先使用 `commit-work`）
- 合并前的 rebase 或 squash
- 解决合并冲突（遇冲突则停止并提示用户）
- 创建或管理 pull request
- 向任何分支强制推送

**转交点**：

- **→ `integrate-branches`**：用户在主仓库 main 分支上，想一次性落地多个 worktree 时
- **停止并提示用户**：在主仓库（非 worktree）调用，或从处于 main 分支的 worktree 调用
- **合并冲突时**：停止并指示用户在主仓库手动解决；不处理 worktree
- **推送被拒时**：停止并指示用户在主仓库撤销合并（如 `git -C <main-repo> reset --hard HEAD~1`）、pull 后手动重试

---

## 使用场景（Use Cases）

- 开发者在 `/repos/myapp-api`（worktree，分支 `feat/api-v2`）刚完成功能，想落地到 main 但不想离开当前目录
- 在 worktree 内运行 `commit-work` 后，立即交付该单条分支
- IDE / 编辑器会话固定在某个 worktree 目录；用户想交付功能但不想中断当前会话

---

## 行为（Behavior）

### 工作流程（Checklist）

**步骤 1 — 验证调用上下文**

```bash
git rev-parse --git-dir              # 主仓库: <root>/.git ; linked worktree: <main-root>/.git/worktrees/<name>
git rev-parse --git-common-dir       # 两种上下文均返回同一值: <main-root>/.git
git rev-parse --abbrev-ref HEAD      # 当前分支
git rev-parse --show-toplevel        # 当前 worktree 根目录（CWD 所在的仓库根）
```

判断上下文：linked worktree 的 `git-dir != git-common-dir`（per-worktree 的 `.git/worktrees/<name>` 与共享的 `.git` 不同）。等价地，linked worktree 中 `<toplevel>/.git` 是普通文件（gitlink），主仓库中是目录。

- 若 `git rev-parse --git-dir` 等于 `git rev-parse --git-common-dir`（即 CWD 是主仓库而非 linked worktree）→ **停止**：
  > "本技能必须在 linked worktree 内部运行，不能在主仓库中运行。当前位置：`<cwd>`。若要从主仓库批量合并多个 worktree，请使用 `integrate-branches`。"

- 若当前分支等于检测到的 main 分支（步骤 2）→ **停止**：
  > "当前分支是 `<main-branch>`。本技能将功能分支交付到 main，而不是将 main 合并到自身。请切换到该 worktree 中的功能分支，或从主仓库使用 `integrate-branches`。"

记录 `<feature-worktree>`（= `git rev-parse --show-toplevel`）与 `<feature-branch>`（= 当前分支）。

**步骤 2 — 确定 main 分支并定位主仓库**

```bash
git remote show origin | grep 'HEAD branch'
```

- 结果无歧义（如 `HEAD branch: main`）→ 直接使用。
- 命令失败或无结果 → 检查 `git branch -r` 中的 `origin/main`，再看 `origin/master`。
- 仍无法确定 → **询问用户**：
  > "无法自动确定 main 分支，请输入 main 分支名称（如 main、master、develop）："

记录 `<main-branch>`。

从 worktree 列表定位主仓库：

```bash
git worktree list --porcelain
```

解析 porcelain 输出。第一条记录是主仓库（其 `worktree` 行给出路径）。记录 `<main-repo>`。完整性校验：`<main-repo> != <feature-worktree>`。

**步骤 3 — 预检：当前 worktree 必须干净**

```bash
git status --porcelain
```

若输出非空 → **停止**：
> "当前 worktree `<feature-worktree>` 有未提交变更。请先提交（如使用 `commit-work`）后重新调用。不自动 stash。"

**步骤 4 — Pull main、合并功能分支、推送（通过 `git -C <main-repo>` 执行）**

```bash
git -C <main-repo> checkout <main-branch>
git -C <main-repo> pull origin <main-branch>
git -C <main-repo> merge --no-ff <feature-branch> -m "Merge branch '<feature-branch>' into <main-branch>"
git -C <main-repo> push origin <main-branch>
```

**所有命令的 CWD 始终保持在 `<feature-worktree>`**——`git -C` 标志驱动主仓库操作，不改变用户位置。

合并冲突时 → **停止**：
> "合并 `<feature-branch>` 到 `<main-branch>` 时发生冲突（主仓库 `<main-repo>`）。请手动在主仓库解决冲突、完成合并，然后运行 `git -C <main-repo> push origin <main-branch>`。worktree 未受影响。"

推送被拒（非 fast-forward）时 → **停止**：
> "合并 `<feature-branch>` 后推送被拒。请在 `<main-repo>` 中运行 `git reset --hard HEAD~1` 撤销合并，然后 `git pull`，重新合并并手动推送。"

推送成功后，通过 `git -C <main-repo> rev-parse <main-branch>` 捕获 `<merge-commit-hash>`。

**步骤 5 — 询问用户清理选项**

单一提示，三个选项：

> "交付完成。worktree `<feature-worktree>` 和分支 `<feature-branch>` 如何处理？
>
> [1] 保留 worktree（保持在此，分支保留）
> [2] 移除 worktree，保留分支（cd 回主仓库）
> [3] 移除 worktree 并删除分支（`git branch -d`，安全删除）
>
> 请选择 1 / 2 / 3："

选项 2 和 3 时，技能输出最终提示，告知用户 cd 到 `<main-repo>`（技能本身无法改变用户 shell 的 CWD；仅执行 git 命令）。

选项 2 和 3 时，通过 `git -C` 执行：

```bash
git -C <main-repo> worktree remove <feature-worktree>
```

仅选项 3 时，在 worktree 移除后执行：

```bash
git -C <main-repo> branch -d <feature-branch>
```

仅用 `-d`——绝不用 `-D`。若 `-d` 失败（在成功的 `--no-ff` 合并后不应出现），上报错误并停止删除（不重试 `-D`）。

**步骤 6 — 汇总报告**

```
deliver-feature summary
──────────────────────────────────────────────────────────────────────────
Feature branch:   feat/api-v2
Worktree:         /repos/myapp-api
Main repo:        /repos/myapp
Main branch:      main

Merge commit:     a1b2c3d (--no-ff)
Push:             ✓
Worktree:         removed | kept
Branch:           deleted | kept
──────────────────────────────────────────────────────────────────────────
Next: cd /repos/myapp        （仅在 worktree 被移除时显示）
```

---

## 输入与输出（Input & Output）

### 输入要求

| 输入 | 是否必需 | 说明 |
|---|---|---|
| Worktree 上下文 | 是 | CWD 必须在 linked worktree 内部；在主仓库调用则停止 |
| 非 main 分支 | 是 | 当前分支必须不是 `<main-branch>`；否则停止 |
| 工作区干净 | 是 | `git status --porcelain` 必须为空；不自动 stash |
| 清理选项 | 用户输入 | 三选一：保留 / 移除保留分支 / 移除并删除分支 |
| main 分支名 | 自动/询问 | 从 remote 检测；无法确定时询问用户 |
| 网络访问 | 是 | pull 和 push 到 `origin` 需要网络 |

### 输出契约

产生（副作用）：

| 元素 | 说明 |
|---|---|
| Merge commit | 在主仓库 `<main-branch>` 上恰好产生一条 `--no-ff` merge commit |
| 远程推送 | `origin/<main-branch>` 更新一次 |
| Worktree 移除 | 可选，用户选择 |
| 分支删除 | 可选，用户选择；仅 `git branch -d` |
| 汇总报告 | 单分支表格，含 merge commit hash、推送状态、清理结果，及适用时的后续 cd 提示 |

---

## 约束（Restrictions）

### 硬边界（Hard Boundaries）

- **禁止改变 CWD**——所有主仓库操作通过 `git -C <main-repo>` 完成；用户 shell 始终保持在 worktree
- **禁止强制推送**（`--force`、`--force-with-lease`）到任何分支
- **禁止自动 stash** 未提交变更——停止并提示用户
- **禁止使用 `git branch -D`**——仅 `-d`
- **禁止在 merge 与 push 均成功前移除 worktree**
- **禁止在主仓库或 main 分支的 worktree 上继续执行**——停止并给出对应提示

### 技能边界（Skill Boundaries）

- **批量合并多个 worktree**：在主仓库 main 分支上使用 `integrate-branches`
- **提交待处理变更**：在调用本技能前使用 `commit-work`
- **rebase / squash**：在调用本技能前直接使用 `git rebase`
- **创建 PR**：使用平台专用 PR 工具；本技能直接合并到 main
- **代码审查**：提交前使用 `review-diff`；本技能不做代码审查

---

## 反模式（Anti-Patterns）

### 调用上下文

✅ 在 linked worktree 内部、非 main 分支上运行
❌ 不要在主仓库运行——那是 `integrate-branches` 的职责；从 main 运行时没有当前 worktree 可交付

### CWD 纪律

✅ 所有主仓库操作使用 `git -C <main-repo>`；CWD 保持在 worktree
❌ 不要在技能执行中途 `cd <main-repo>`——若用户之后移除 worktree，他们期望保持在调用时所在位置，直到选择选项 2/3

### 预检顺序

✅ 在任何合并尝试前验证工作区干净
❌ 不要先开始合并，再在中途发现脏文件

### 合并方式

✅ `git merge --no-ff` 保留分支历史
❌ 不要使用 `git merge --squash` 或 fast-forward——历史会丢失

### 清理安全性

✅ 仅在用户明确选择选项 2 或 3、且 merge+push 均成功后才移除 worktree
❌ 不要自动移除 worktree——用户可能还想在那里继续工作

### 分支删除

✅ 仅在用户明确选择选项 3 时使用 `git branch -d`（安全）
❌ 绝不使用 `git branch -D`——可能删除未合并的提交

---

## 示例（Examples）

### 示例 1：正常路径——交付并清理

**场景**：开发者在 worktree `/repos/myapp-api` 刚完成 `feat/api-v2`，想落地并清理。

**执行过程**：

```bash
# CWD: /repos/myapp-api

# 步骤 1：上下文——在 linked worktree 内部，非 main 分支 ✓
git rev-parse --git-dir            # /repos/myapp/.git/worktrees/myapp-api
git rev-parse --git-common-dir     # /repos/myapp/.git   (与 --git-dir 不同 → linked worktree ✓)
git rev-parse --abbrev-ref HEAD    # feat/api-v2
git rev-parse --show-toplevel      # /repos/myapp-api

# 步骤 2：main 分支 + 主仓库
git remote show origin | grep 'HEAD branch'   # HEAD branch: main
git worktree list --porcelain                 # 第一条记录 → /repos/myapp

# 步骤 3：预检——干净 ✓
git status --porcelain             # (empty)

# 步骤 4：pull → merge → push，全部通过 git -C；CWD 保持 /repos/myapp-api
git -C /repos/myapp checkout main
git -C /repos/myapp pull origin main
git -C /repos/myapp merge --no-ff feat/api-v2 -m "Merge branch 'feat/api-v2' into main"
git -C /repos/myapp push origin main
# merge commit: a1b2c3d

# 步骤 5：用户选择 [3] 移除 worktree 并删除分支
git -C /repos/myapp worktree remove /repos/myapp-api
git -C /repos/myapp branch -d feat/api-v2
```

**汇总**：

```
deliver-feature summary
──────────────────────────────────────────────────────────────────────────
Feature branch:   feat/api-v2
Worktree:         /repos/myapp-api
Main repo:        /repos/myapp
Main branch:      main

Merge commit:     a1b2c3d (--no-ff)
Push:             ✓
Worktree:         removed
Branch:           deleted
──────────────────────────────────────────────────────────────────────────
Next: cd /repos/myapp
```

---

### 示例 2：错误上下文——在主仓库调用

**场景**：开发者在 `/repos/myapp` 的 `main` 分支上，习惯性地运行了 `deliver-feature`。

**执行过程**：

```bash
# CWD: /repos/myapp

git rev-parse --git-dir          # /repos/myapp/.git
git rev-parse --git-common-dir   # /repos/myapp/.git   (相等 → 主仓库，而非 worktree)
```

**技能停止**：

> "本技能必须在 linked worktree 内部运行，不能在主仓库中运行。当前位置：`/repos/myapp`。若要从主仓库批量合并多个 worktree，请使用 `integrate-branches`。"

未执行任何 git 操作。

---

### 示例 3：冲突——停止，不处理 worktree

**场景**：开发者从 `/repos/myapp-api` 的 `feat/api-v2` 运行 `deliver-feature`。预检通过。合并到 main 时遇到冲突。

**执行过程**：

```bash
# CWD: /repos/myapp-api（全程保持在此）

git -C /repos/myapp pull origin main
git -C /repos/myapp merge --no-ff feat/api-v2 -m "Merge branch 'feat/api-v2' into main"
# CONFLICT (content): Merge conflict in src/api.ts
```

**技能停止**：

> "合并 `feat/api-v2` 到 `main` 时发生冲突（主仓库 `/repos/myapp`）。请手动在主仓库解决冲突、完成合并，然后运行 `git -C /repos/myapp push origin main`。worktree 未受影响。"

CWD 仍是 `/repos/myapp-api`。worktree 完好。无推送。无清理。

---

## AI 重构指引（AI Refactor Instruction）

若本技能产生错误行为：

1. **执行中 CWD 被改变**：若某步骤运行了 `cd <main-repo>` 或对主仓库使用了非 `-C` 的 git 命令 → 回退；对所有主仓库操作改用 `git -C <main-repo>`
2. **错误上下文继续执行**：若在 CWD 为主仓库时运行了技能（即 `git rev-parse --git-dir` 等于 `git rev-parse --git-common-dir`）→ 回退到步骤 1，补充 git-dir vs git-common-dir 比较校验
3. **自动 stash 被执行**：若任何位置出现了 `git stash` → 移除；按步骤 3 在脏工作区时停止
4. **在推送成功前移除了 worktree**：若 `git worktree remove` 在 `git push` 返回 0 前执行 → 停止；仅在步骤 4 完成且用户选择选项 2 或 3 后才执行清理
5. **尝试强制推送**：若任何推送命令中出现 `--force` 或 `--force-with-lease` → 替换为标准推送；若被拒，停止并上报

---

## 自检清单（Self-Check）

- [ ] **Worktree 上下文已验证**：`git rev-parse --git-dir` 与 `git rev-parse --git-common-dir` 不同
- [ ] **非 main 分支已确认**：当前分支 ≠ 检测到的 main 分支
- [ ] **main 分支已确定**：自动检测或由用户明确提供，未作假设
- [ ] **主仓库路径已定位**：从 `git worktree list --porcelain` 第一条记录解析
- [ ] **预检通过**：`git status --porcelain` 在任何合并前为空
- [ ] **CWD 从未改变**：所有主仓库命令使用 `git -C <main-repo>`；用户 shell 始终保持在 `<feature-worktree>`
- [ ] **合并前已 pull**：`git -C <main-repo> pull origin <main-branch>` 在 `git merge --no-ff` 前执行
- [ ] **使用了 --no-ff 合并**：确认使用 `git merge --no-ff`，无 fast-forward 或 squash
- [ ] **推送成功后才提供清理选项**：仅在 `git push` 返回 0 后才显示清理提示
- [ ] **清理以用户选择为前提**：worktree 移除仅在选项 2 或 3 时发生
- [ ] **分支删除使用了 `-d`**：无 `-D` 标志；仅选项 3
- [ ] **汇总报告已输出**：含 merge commit hash、推送状态、清理结果，及适用时的后续 cd 提示
- [ ] **未使用强制推送**：任何命令中未出现 `--force` 或 `--force-with-lease`
