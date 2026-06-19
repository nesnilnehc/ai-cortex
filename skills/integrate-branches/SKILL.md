---
name: integrate-branches
description: From the main repo on the main branch, scan all linked worktrees and local branches, let the user multi-select, then merge --no-ff + push them sequentially and clean up succeeded worktrees together.
description_zh: 在主仓库 main 分支扫描所有 linked worktree 与本地独立分支，让用户多选后顺序 --no-ff 合并并推送，最后统一清理成功的 worktree 条目。
tags: [git, workflow, automation]
version: 2.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [integrate branches, integrate worktrees, integrate features, batch merge, batch merge branches, batch merge worktrees, merge worktrees, finish worktrees, close worktrees, deliver features, land branches]
input_schema:
  type: free-form
  description: Main git repository on the main branch with one or more linked worktrees or local branches ready to merge.
output_schema:
  type: side-effect
  description: Selected branches merged into main and pushed; succeeded worktrees removed; per-branch batch summary report.
---

# 技能（Skill）：整合分支（Integrate Branches）

## 目的（Purpose）

在主仓库中批量收尾功能分支：扫描所有活跃的 linked worktree 以及没有 worktree 的本地分支，让用户选择哪些落地，逐一校验工作区干净，依次 merge + push，最后统一清理所有成功合并的 worktree。省去逐个 `cd` 进目录再手动交付的操作。

---

## 核心目标（Core Objective）

**首要目标**：在主仓库 main 分支上，将用户选定的分支（来自 worktree 或独立分支）合并进 main，推送到 origin，并清理成功的 worktree——使仓库处于已知干净状态。

**成功标准**（必须全部满足）：

1. ✅ **调用上下文已验证**：CWD 是主仓库根目录（而非 linked worktree 内部），且当前分支是 main 分支
2. ✅ **所有候选项已发现**：`git worktree list --porcelain` 与 `git branch` 均已解析；非 main 条目以带类型标识的统一列表呈现给用户
3. ✅ **预检在任何合并前完成**：所有选中的 worktree 条目均已检查工作区是否干净；所有脏条目在一个块中统一上报
4. ✅ **顺序 merge + push**：每条选中的干净分支依次以 `--no-ff` 合并并推送；逐条记录状态（`succeeded` / `failed`）
5. ✅ **统一清理**：所有 `succeeded` 的 worktree 条目一起移除；branch-only 条目跳过 worktree 移除；失败条目不做任何清理
6. ✅ **汇总报告已输出**：每条分支的 merge / push / cleanup / 分支删除状态均已覆盖

**验收测试**：技能执行完毕后，`git log --oneline <main-branch>` 对每条成功分支各有一条 merge commit；`git worktree list` 仅剩主仓库加上失败/跳过的 worktree 条目；`git ls-remote origin <main-branch>` 与本地一致。

---

## 范围边界（Scope Boundaries）

**本技能负责**：

- 验证调用上下文（主仓库根目录 + main 分支）
- 确定 main 分支（自动检测；仅在无法确定时询问用户）
- 扫描 linked worktree（`git worktree list --porcelain`）与无 worktree 的本地分支（`git branch`）
- 去重：已被 worktree 条目覆盖的分支不再重复展示
- 用户多选待合并分支（`all` 或按序号子集）
- 预检工作区：worktree 条目用 `git -C <path> status --porcelain`；branch-only 条目跳过脏检查（无独立工作区）
- 对每条选中分支依次执行 pull → `--no-ff` merge → push
- 每次失败后询问用户：继续剩余条目还是中止
- 统一清理所有成功合并的 worktree 条目（`git worktree remove`）
- 可选功能分支删除（用户确认，仅 `-d`）
- 逐条分支汇总报告

**本技能不负责**：

- 单 worktree 交付（请在 worktree 内使用 `deliver-feature`）
- 提交未提交的变更（请先在各 worktree 内使用 `commit-work`）
- 合并前的 rebase 或 squash
- 解决合并冲突（遇冲突则停止并上报用户）
- 创建或管理 pull request
- 向任何分支强制推送
- 并行合并执行（始终顺序执行）

**转交点**：

- **→ `deliver-feature`**：用户在单个 worktree 内，只想交付该分支而无需 `cd` 回主仓库时
- **停止并提示用户**：在 linked worktree 内部调用，或在主仓库非 main 分支上调用时
- **某条分支合并冲突时**：停止该条，询问是否继续剩余
- **某条分支推送被拒时**：停止该条，询问是否继续剩余

---

## 使用场景（Use Cases）

- 开发者有 2–4 条功能分支（部分在 worktree 中，部分为独立分支）准备一次性落地 main
- Sprint 结束批量收尾：在主仓库中合并、推送、清理所有已完成功能分支
- CI / 自动化流程生成了多个并行 worktree 加若干 topic 分支，现在汇总结果

---

## 行为（Behavior）

### 工作流程（Checklist）

**步骤 1 — 验证调用上下文**

```bash
git rev-parse --git-dir              # 主仓库: <root>/.git ; linked worktree: <main-root>/.git/worktrees/<name>
git rev-parse --git-common-dir       # 两种上下文均返回同一值: <main-root>/.git
git rev-parse --abbrev-ref HEAD      # 当前分支
git rev-parse --show-toplevel        # 当前仓库根目录
```

linked worktree 的 `git-dir != git-common-dir`；主仓库两者相等。

- 若 `git rev-parse --git-dir` 与 `git rev-parse --git-common-dir` 不同（即 CWD 在 linked worktree 内部）→ **停止**：
  > "本技能必须在主仓库根目录运行，不能在 worktree 内部运行。当前位置：`<cwd>`。若要交付当前 worktree 的分支，请使用 `deliver-feature`。"

- 若当前分支不是检测到的 main 分支（步骤 2）→ **停止**：
  > "当前分支是 `<current-branch>`，不是 `<main-branch>`。请先切换到 main 分支：`git checkout <main-branch>`。"

记录 `<main-repo>`（= `git rev-parse --show-toplevel`）。此后每一步 CWD 均保持在此。

**步骤 2 — 确定 main 分支**

```bash
git remote show origin | grep 'HEAD branch'
```

- 结果无歧义（如 `HEAD branch: main`）→ 直接使用。
- 命令失败或无结果 → 检查 `git branch -r` 中的 `origin/main`，再看 `origin/master`。
- 仍无法确定 → **询问用户**：
  > "无法自动确定 main 分支，请输入 main 分支名称（如 main、master、develop）："

记录 `<main-branch>`。

**步骤 3 — 扫描并展示可选分支**

```bash
# 来源 1：linked worktrees
git worktree list --porcelain

# 来源 2：所有本地分支
git branch --format='%(refname:short)'
```

解析 porcelain 输出。第一条 worktree 记录是主仓库本身——跳过。其余每条记为 `type: worktree` 候选项。

从 `git branch` 输出中排除：
- `<main-branch>` 本身
- 已被 worktree 条目覆盖的分支（按分支名去重）

剩余分支记为 `type: branch` 候选项（无关联 worktree 路径）。

构建 `{path, branch, type}` 元组的统一列表。跳过 detached 条目，将其标记为不可用。

- 无候选项 → **停止**：
  > "未找到活跃的 linked worktree 或本地分支，无可整合项。"

以序号、类型标识、路径（如适用）、分支名、最近活动提示展示列表：

```
Available branches to integrate:
  [1]  worktree  /repos/myapp-auth      feat/user-auth      (last commit: 2 days ago)
  [2]  worktree  /repos/myapp-api       feat/api-v2         (last commit: 5 days ago)
  [3]  branch    —                      feat/dashboard      (last commit: 14 days ago — STALE)
```

询问：

> "请选择要整合的分支，输入序号（逗号分隔）或 `all`："

记录 `<selected-list>`。

**步骤 4 — 预检：检查所有选中条目**

对 `<selected-list>` 中每条条目 `E`：

- 若 `E.type == worktree`：
  ```bash
  git -C <E.path> status --porcelain
  ```
- 若 `E.type == branch`：无独立工作区——跳过脏检查，始终视为干净。

将结果分别收集到 `<clean-list>` 和 `<dirty-list>`。

若 `<dirty-list>` 非空，在任何合并开始前统一上报所有脏条目：

```
Pre-flight check — dirty worktrees (will be skipped):
  /repos/myapp-api  (feat/api-v2)    — 3 uncommitted file(s)
```

询问：

> "以上 worktree 有未提交变更。继续合并其余干净条目，还是全部停止？[continue / halt]"

- `halt` → 停止；不执行任何合并。
- `continue` → 仅对 `<clean-list>` 继续。若 `<clean-list>` 为空 → 停止并提示"无可操作项"。

任何情况下均不自动 stash。

**步骤 5 — 批量 merge + push（顺序执行）**

对 `<clean-list>` 中每条条目 `E`：

```bash
# 多分支运行期间保持最新
git pull origin <main-branch>

# --no-ff 合并
git merge --no-ff <E.branch> -m "Merge branch '<E.branch>' into <main-branch>"

# 推送
git push origin <main-branch>
```

CWD 全程保持在 `<main-repo>`。

条目 `E` 失败时：

- 合并冲突：
  > "合并 `<E.branch>` 到 `<main-branch>` 时发生冲突。请在 `<main-repo>` 中解决冲突、手动完成合并，然后推送并移除 worktree（如适用）。"
- 推送被拒（非 fast-forward）：
  > "合并 `<E.branch>` 后推送被拒。请在 `<main-repo>` 中运行 `git reset --hard HEAD~1` 撤销合并，然后 pull、重新合并并推送。"

两种情况均将 `E` 标记为 `failed`，并询问：

> "继续处理剩余分支，还是中止所有剩余项？[continue / abort]"

- `abort` → 停止；不再处理任何剩余条目。
- `continue` → 标记 `E` 为 `failed`，继续下一条。

逐条记录结果：`succeeded` 或 `failed`。

**步骤 6 — 统一清理（仅 worktree 条目）**

所有合并完成后，确认 CWD 仍为 `<main-repo>`：

```bash
pwd   # 必须等于 <main-repo>
```

仅对 `<succeeded-list>` 中 `E.type == worktree` 的条目：

```bash
git worktree remove <E.path>
```

顺序执行。若某次移除失败（如路径已不存在），记录错误后继续下一条。

`type: branch` 条目无 worktree 路径——本步骤完全跳过。失败条目的 worktree 绝不移除。

**步骤 7 — 提供本地分支删除选项**

对 `<succeeded-list>` 中所有条目，统一展示分支列表：

> "已清理成功条目。删除以下本地功能分支？输入序号、`all` 或 `none`："
> ```
> [1]  feat/user-auth  (was worktree)
> [2]  feat/dashboard  (was branch)
> ```

每条确认后执行：

```bash
git branch -d <E.branch>
```

仅用 `-d`——绝不用 `-D`。若 `-d` 失败，上报错误并停止该分支的删除。

**步骤 8 — 汇总报告**

```
integrate-branches summary
──────────────────────────────────────────────────────────────────────────
Type      Branch            Merge          Push   Cleanup  Branch-Del
worktree  feat/user-auth    ✓              ✓      ✓        deleted
worktree  feat/api-v2       ✗(conflict)    —      —        —
branch    feat/dashboard    ✓              ✓      —        deleted
──────────────────────────────────────────────────────────────────────────
Main repo: /repos/myapp · Main branch: main · Remote: origin
```

状态码：`✓` 成功 · `✗(原因)` 失败 · `skipped(dirty)` 预检失败 · `—` 不适用

`type: branch` 条目的 `Cleanup` 列始终为 `—`（无 worktree 可移除）。

---

## 输入与输出（Input & Output）

### 输入要求

| 输入 | 是否必需 | 说明 |
|---|---|---|
| 主仓库 + main 分支上下文 | 是 | CWD 必须是主仓库根目录，当前分支必须等于 main 分支 |
| 活跃候选项 | 是 | 至少存在一个 linked worktree 或本地分支（main 除外） |
| 分支选择 | 用户输入 | `all` 或从展示列表中输入逗号分隔的序号 |
| 工作区干净 | 每个 worktree 条目 | 脏 worktree 预先上报并跳过；branch-only 条目始终通过预检 |
| main 分支名 | 自动/询问 | 从 remote 检测；无法确定时询问用户 |
| 网络访问 | 是 | pull 和 push 到 `origin` 需要网络 |

### 输出契约

| 元素 | 说明 |
|---|---|
| Merge commits | 每条成功分支在 `<main-branch>` 上产生一条 `--no-ff` merge commit |
| 远程推送 | 每条成功分支推送一次，更新 `origin/<main-branch>` |
| Worktree 移除 | 所有成功的 `type: worktree` 条目从 `git worktree list` 中移除 |
| 分支删除 | 可选，用户确认后执行；仅 `git branch -d` |
| 批量汇总报告 | 逐条分支表格：type / branch / merge / push / cleanup / 分支删除状态 |

---

## 约束（Restrictions）

### 硬边界（Hard Boundaries）

- **禁止强制推送**（`--force`、`--force-with-lease`）到任何分支
- **禁止在 merge 或 push 失败后移除该 worktree**
- **禁止自动 stash** 未提交变更——预先上报并跳过该 worktree
- **禁止使用 `git branch -D`**——仅 `-d`（安全删除）
- **禁止在所有选中条目预检完成前开始任何合并**
- **禁止在 linked worktree 内部或主仓库非 main 分支上继续执行**——停止并给出对应提示

### 技能边界（Skill Boundaries）

- **单 worktree 交付**：在 worktree 内使用 `deliver-feature`
- **提交待处理变更**：先在各 worktree 内使用 `commit-work`
- **rebase / squash**：在调用本技能前直接使用 `git rebase`
- **创建 PR**：使用平台专用 PR 工具；本技能直接合并到 main
- **代码审查**：提交前使用 `review-diff`；本技能不做代码审查

---

## 反模式（Anti-Patterns）

### 调用上下文

✅ 在主仓库根目录、main 分支上运行
❌ 不要在 linked worktree 内部运行——那是 `deliver-feature` 的职责；worktree 被删除后 CWD 会失效，导致后续所有命令失败

### 预检顺序

✅ 在开始任何合并前，对所有选中的 worktree 条目统一做脏检查
❌ 不要在合并前才检查该条目——脏 worktree 会在部分合并已提交后才被发现

### 合并方式

✅ `git merge --no-ff` 保留分支历史
❌ 不要使用 `git merge --squash` 或 fast-forward——历史会丢失

### 推送安全

✅ 标准 `git push origin <main-branch>`
❌ 绝不在 main 上使用 `--force` 或 `--force-with-lease`

### 清理顺序

✅ 仅在 merge 与 push 均成功后才移除 worktree
❌ 不要在 merge 后、push 前移除——push 失败则分支将无法访问

### 分支删除

✅ `git branch -d`（安全），且需用户确认
❌ 绝不使用 `git branch -D`（强制）——可能删除未合并的提交

---

## 示例（Examples）

### 示例 1：worktree 分支与独立分支混合（正常路径）

**场景**：两条 worktree 分支和一条独立分支准备合并进 `main`。

**执行过程**：

```bash
# 步骤 3：扫描
git worktree list --porcelain
# main: /repos/myapp  +  /repos/myapp-auth feat/user-auth  +  /repos/myapp-api feat/api-v2

git branch --format='%(refname:short)'
# feat/user-auth（已在 worktree 中——去重）
# feat/api-v2   （已在 worktree 中——去重）
# feat/dashboard（独立分支）

# 展示列表：
#   [1]  worktree  /repos/myapp-auth  feat/user-auth  (last commit: 2 days ago)
#   [2]  worktree  /repos/myapp-api   feat/api-v2     (last commit: 5 days ago)
#   [3]  branch    —                  feat/dashboard  (last commit: 14 days ago — STALE)
# 用户选择：all

# 步骤 4：预检
git -C /repos/myapp-auth status --porcelain   # (empty ✓)
git -C /repos/myapp-api  status --porcelain   # (empty ✓)
# feat/dashboard — 无 worktree，跳过 ✓

# 步骤 5：顺序 merge + push（3 条）
git pull origin main
git merge --no-ff feat/user-auth -m "Merge branch 'feat/user-auth' into main"
git push origin main

git pull origin main
git merge --no-ff feat/api-v2 -m "Merge branch 'feat/api-v2' into main"
git push origin main

git pull origin main
git merge --no-ff feat/dashboard -m "Merge branch 'feat/dashboard' into main"
git push origin main

# 步骤 6：清理——仅 worktree 条目
pwd                                       # /repos/myapp ✓
git worktree remove /repos/myapp-auth
git worktree remove /repos/myapp-api
# feat/dashboard — type: branch，跳过

# 步骤 7：删除分支——用户选 all
git branch -d feat/user-auth
git branch -d feat/api-v2
git branch -d feat/dashboard
```

**汇总**：

```
integrate-branches summary
──────────────────────────────────────────────────────────────────────────
Type      Branch            Merge  Push  Cleanup  Branch-Del
worktree  feat/user-auth    ✓      ✓     ✓        deleted
worktree  feat/api-v2       ✓      ✓     ✓        deleted
branch    feat/dashboard    ✓      ✓     —        deleted
──────────────────────────────────────────────────────────────────────────
Main repo: /repos/myapp · Main branch: main · Remote: origin
```

---

### 示例 2：脏 worktree 被跳过，独立分支正常推进

**场景**：选中三条条目，其中一个 worktree 有未提交变更。

**执行过程**：

```bash
# 步骤 4：预检
git -C /repos/myapp-auth  status --porcelain   # (empty ✓)
git -C /repos/myapp-api   status --porcelain   # M  src/api.ts  ← 脏
# feat/dashboard — 无 worktree，跳过 ✓
```

**技能上报**：

```
Pre-flight check — dirty worktrees (will be skipped):
  /repos/myapp-api  (feat/api-v2)    — 1 uncommitted file(s)
```

用户回答 `continue` → `feat/user-auth` 和 `feat/dashboard` 继续；`feat/api-v2` 跳过。

**汇总**：

```
integrate-branches summary
──────────────────────────────────────────────────────────────────────────
Type      Branch            Merge          Push  Cleanup  Branch-Del
worktree  feat/user-auth    ✓              ✓     ✓        deleted
worktree  feat/api-v2       skipped(dirty) —     —        —
branch    feat/dashboard    ✓              ✓     —        deleted
──────────────────────────────────────────────────────────────────────────
```

---

### 示例 3：错误上下文——在 worktree 内部调用

**场景**：开发者在 `/repos/myapp-api` 的 `feat/api-v2` 分支上。

**执行过程**：

```bash
git rev-parse --git-dir          # /repos/myapp/.git/worktrees/myapp-api
git rev-parse --git-common-dir   # /repos/myapp/.git   (不同 → linked worktree)
```

**技能停止**：

> "本技能必须在主仓库根目录运行，不能在 worktree 内部运行。当前位置：`/repos/myapp-api`。若要交付当前 worktree 的分支，请使用 `deliver-feature`。"

---

## AI 重构指引（AI Refactor Instruction）

若本技能产生错误行为：

1. **错误上下文继续执行**：回到步骤 1，补充 git-dir vs git-common-dir 比较及分支相等性校验
2. **预检被跳过或延后**：回到步骤 4，确保在任何合并前对所有选中条目完成预检
3. **失败 worktree 被删除**：停止；仅 `<succeeded-list>` 中 `type: worktree` 的条目可移除
4. **branch-only 条目执行了 worktree remove**：branch-only 条目无 worktree 路径——完全跳过步骤 6
5. **尝试强制推送**：替换为标准推送；若失败，停止并上报
6. **合并前跳过 pull**：从 pull 步骤重新执行
7. **worktree 分支重复出现**：步骤 3 的去重必须将已在 worktree 列表中的分支从 `git branch` 输出中排除

---

## 自检清单（Self-Check）

- [ ] **调用上下文已验证**：`git rev-parse --git-dir` 等于 `git rev-parse --git-common-dir`，且当前分支等于 `<main-branch>`
- [ ] **main 分支已确认**：自动检测或由用户明确提供，未作假设
- [ ] **两个来源均已扫描**：`git worktree list --porcelain` 和 `git branch` 均已解析，非 main 条目已展示
- [ ] **去重已执行**：worktree 中的分支未在分支列表中重复出现
- [ ] **用户选择已记录**：在任何预检前已获取 `all` 或序号子集
- [ ] **所有 worktree 条目预检在任何合并前完成**：对每个选中的 worktree 条目执行了 `git -C <path> status --porcelain`
- [ ] **branch-only 条目已跳过脏检查**：它们无工作区可检查
- [ ] **脏 worktree 已统一上报**：所有脏条目在 continue/halt 提示前一并列出
- [ ] **每次合并前已 pull**：每次 `git merge --no-ff` 前立即执行了 `git pull origin <main-branch>`
- [ ] **使用了 --no-ff 合并**：确认使用 `git merge --no-ff`，无 fast-forward 或 squash
- [ ] **push 成功后才标记 `succeeded`**：仅在 `git push` 返回 0 后才将条目加入 `<succeeded-list>`
- [ ] **统一清理仅对成功的 worktree 条目执行**：`git worktree remove` 从未对失败、跳过或 `type: branch` 条目调用
- [ ] **清理前已确认 CWD**：任何 `git worktree remove` 前 `pwd` 等于 `<main-repo>`
- [ ] **分支删除使用了 `-d`**：任何分支删除命令中无 `-D` 标志；用户已确认每条分支
- [ ] **汇总报告已输出**：每条分支的状态码均正确填写
- [ ] **未使用强制推送**：任何命令中未出现 `--force` 或 `--force-with-lease`
