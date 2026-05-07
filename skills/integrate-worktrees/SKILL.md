---
name: integrate-worktrees
description: From the main repo on the main branch, scan all linked worktrees, let the user multi-select, then merge --no-ff + push them sequentially and clean up the succeeded ones together.
description_zh: 在主仓库 main 分支扫描所有 linked worktree，让用户多选后顺序 --no-ff 合并并推送，最后统一清理成功项。
tags: [git, workflow, automation]
version: 1.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [integrate worktrees, integrate features, batch merge worktrees, merge worktrees, finish worktrees, close worktrees, deliver features]
input_schema:
  type: free-form
  description: Main git repository on the main branch with one or more linked worktrees ready to merge.
output_schema:
  type: side-effect
  description: Selected feature branches merged into main and pushed; succeeded worktrees removed; per-worktree batch summary report.
---

# Skill: integrate-worktrees

## Purpose

Closes out a batch of worktrees from the main repo: scan all active linked worktrees, let the user pick which to land, verify all picks are clean, merge and push each in sequence, then remove all successfully-merged worktrees together. Eliminates the need to cd into each worktree directory and invoke a per-branch delivery.

---

## Core Objective

**Primary goal**: From the main repo on the main branch, land the user-selected worktree branches onto main, deliver them to origin, and clean up succeeded ones — leaving the repository in a known-clean state.

**Success Criteria** (all must be satisfied):

1. ✅ **Invocation context verified**: CWD is the main repo root (not inside a linked worktree) and current branch is the main branch
2. ✅ **All linked worktrees discovered**: `git worktree list --porcelain` parsed; non-main entries presented to user
3. ✅ **Pre-flight completed before any merge**: All selected worktrees checked for clean working tree; all dirty ones reported upfront in one block
4. ✅ **Sequential merge + push**: Each selected clean worktree merged with `--no-ff` and pushed; per-worktree status (`succeeded` / `failed`) recorded
5. ✅ **Unified cleanup**: All `succeeded` worktrees removed together; no failed worktree is removed
6. ✅ **Summary reported**: Per-worktree table covers merge / push / cleanup / branch-deletion status for every entry

**Acceptance Test**: After skill completes, `git log --oneline <main-branch>` shows one merge commit per succeeded worktree; `git worktree list` contains only the main repo plus any failed/skipped worktrees; `git ls-remote origin <main-branch>` matches local.

---

## Scope Boundaries

**This skill handles**:

- Verifying invocation context (main repo root + main branch)
- Detecting the main branch (auto-detect; ask user only if ambiguous)
- Scanning and listing all active linked worktrees
- User multi-selection of which worktrees to merge (`all` or index subset)
- Pre-flight clean-tree check for all selected worktrees before any merge begins
- Sequential pull → `--no-ff` merge → push for each selected clean worktree
- Per-failure user decision: continue with remaining or abort
- Unified cleanup of all successfully-merged worktrees
- Optional feature branch deletion (user-confirmed, `-d` only)
- Per-worktree summary report

**This skill does NOT handle**:

- Single-worktree delivery (use `deliver-feature` from inside the worktree)
- Committing uncommitted changes (use `commit-work` per worktree first)
- Rebasing or squashing commits before merge
- Resolving merge conflicts (halts and reports to user)
- Creating or managing pull requests
- Force-pushing to any branch
- Parallel merge execution (always sequential)

**Handoff points**:

- **→ `deliver-feature`**: when the user is inside a single worktree and wants to land just that branch without `cd`-ing back to the main repo
- **Halt and instruct user**: if invoked from inside a linked worktree, or from the main repo on a non-main branch
- **On merge conflict** for a worktree: halt that one; ask whether to continue with remaining
- **On push rejection** for a worktree: halt that one; ask whether to continue with remaining

---

## Use Cases

- Developer has 2–4 feature worktrees ready to land onto main and wants to handle them in one invocation
- End-of-sprint batch cleanup: merging all completed feature worktrees from the main repo
- CI / automation that spawned multiple parallel worktrees for isolated tasks, now collecting results

---

## Behavior

### Workflow (Checklist)

**Step 1 — Verify invocation context**

```bash
git rev-parse --git-dir              # main repo: <root>/.git ; linked worktree: <main-root>/.git/worktrees/<name>
git rev-parse --git-common-dir       # both contexts return the same value: <main-root>/.git
git rev-parse --abbrev-ref HEAD      # current branch
git rev-parse --show-toplevel        # current repo root
```

A linked worktree has `git-dir != git-common-dir` (the per-worktree `.git/worktrees/<name>` vs the shared `.git`); the main repo has them equal.

- If `git rev-parse --git-dir` differs from `git rev-parse --git-common-dir` (i.e., CWD is inside a linked worktree) → **halt**:
  > "This skill must be run from the main repo, not from inside a worktree. Current location: `<cwd>`. To deliver just the current worktree's branch, use `deliver-feature`."

- If current branch is not the detected main branch (Step 2) → **halt**:
  > "Current branch is `<current-branch>`, not `<main-branch>`. Switch to the main branch first: `git checkout <main-branch>`."

Record `<main-repo>` (= `git rev-parse --show-toplevel`). CWD remains here for every subsequent step.

**Step 2 — Determine main branch**

```bash
git remote show origin | grep 'HEAD branch'
```

- Unambiguous result (e.g., `HEAD branch: main`) → use it.
- Command fails or returns nothing → check `git branch -r` for `origin/main` then `origin/master`.
- Still ambiguous → **ask the user**:
  > "Could not determine the main branch automatically. What is the name of the main branch (e.g., main, master, develop)?"

Record `<main-branch>`.

**Step 3 — Scan and present active worktrees**

```bash
git worktree list --porcelain
```

Parse the porcelain output. The first record is the main repo (its `worktree` line equals `<main-repo>`). Each remaining record is a candidate. Build a list of `{path, branch}` tuples (skip detached entries; report them as ineligible).

- If no linked worktrees found → **halt**:
  > "No active linked worktrees found. Nothing to integrate."

Present the list with index, path, branch, and last-activity hint:

```
Active worktrees available to integrate:
  [1]  /repos/myapp-auth      feat/user-auth      (last commit: 2 days ago)
  [2]  /repos/myapp-api       feat/api-v2         (last commit: 5 days ago)
  [3]  /repos/myapp-ui        feat/dashboard      (last commit: 14 days ago — STALE)
```

Ask:

> "Which worktrees should be integrated? Enter numbers separated by commas, or type `all`:"

Record `<selected-list>`.

**Step 4 — Pre-flight: check all selected worktrees**

For each worktree `W` in `<selected-list>`:

```bash
git -C <W.path> status --porcelain
```

Collect all results into `<clean-list>` and `<dirty-list>`.

If `<dirty-list>` is non-empty, report all dirty entries in a single block before any merge begins:

```
Pre-flight check — dirty worktrees (will be skipped):
  /repos/myapp-api  (feat/api-v2)    — 3 uncommitted file(s)
  /repos/myapp-ui   (feat/dashboard) — 1 uncommitted file(s)
```

Ask:

> "The above worktrees have uncommitted changes. Proceed with the remaining clean worktrees, or halt all? [continue / halt]"

- `halt` → stop; no merges performed.
- `continue` → proceed with `<clean-list>` only. If `<clean-list>` is empty after filtering → halt with "Nothing left to do."

No auto-stash is performed under any condition.

**Step 5 — Batch merge + push (sequential)**

For each worktree `W` in `<clean-list>`:

```bash
# Stay current across multi-worktree run
git pull origin <main-branch>

# Merge with --no-ff
git merge --no-ff <W.branch> -m "Merge branch '<W.branch>' into <main-branch>"

# Push
git push origin <main-branch>
```

CWD remains `<main-repo>` throughout. (No `git -C` needed — this skill operates from the main repo directly.)

On failure for worktree `W`:

- If merge conflict:
  > "Merge conflict merging `<W.branch>` into `<main-branch>`. Resolve conflicts in `<main-repo>`, complete the merge manually, then push and remove the worktree."
- If push rejected (non-fast-forward):
  > "Push rejected after merging `<W.branch>`. Run `git reset --hard HEAD~1` in `<main-repo>` to undo the merge, then pull, re-merge, and push manually."

In both cases, mark `W` as `failed` and ask:

> "Continue with the remaining worktrees, or abort all remaining? [continue / abort]"

- `abort` → stop; do not touch any remaining worktrees.
- `continue` → mark `W` as `failed`, proceed to next.

Record per-worktree outcome: `succeeded` or `failed`.

**Step 6 — Unified cleanup**

After all merges complete, verify CWD is still `<main-repo>`:

```bash
pwd   # must equal <main-repo>
```

For each worktree in `<succeeded-list>` only:

```bash
git worktree remove <W.path>
```

Execute sequentially. If an individual removal fails (e.g., path already gone), log the error and continue with the next.

Never remove a worktree whose status is `failed`.

**Step 7 — Offer to delete feature branches**

For all worktrees in `<succeeded-list>`, present branches together:

> "Worktrees removed. Delete these local feature branches? Enter numbers, `all`, or `none`:"
> ```
> [1]  feat/user-auth
> [2]  feat/dashboard
> ```

For each confirmed:

```bash
git branch -d <W.branch>
```

Use `-d` only — never `-D`. If `-d` fails (unexpected after a successful `--no-ff` merge), report the error and stop deletion for that branch.

**Step 8 — Summary report**

```
integrate-worktrees summary
──────────────────────────────────────────────────────────────────────────
Worktree               Branch            Merge          Push   Cleanup  Branch
/repos/myapp-auth      feat/user-auth    ✓              ✓      ✓        deleted
/repos/myapp-api       feat/api-v2       ✗(conflict)    —      —        —
/repos/myapp-ui        feat/dashboard    skipped(dirty) —      —        —
──────────────────────────────────────────────────────────────────────────
Main repo: /repos/myapp · Main branch: main · Remote: origin
```

Status codes: `✓` succeeded · `✗(reason)` failed · `skipped(dirty)` pre-flight fail · `—` not applicable

---

## Input & Output

### Input Requirements

| Input | Required | Description |
|---|---|---|
| Main repo + main branch context | Yes | CWD must be the main repo root and current branch must equal the main branch |
| Active linked worktrees | Yes | At least one non-main linked worktree must exist |
| Worktree selection | User input | `all` or comma-separated indices from the presented list |
| Clean working tree | Per-worktree | Dirty worktrees reported upfront and skipped; no auto-stash |
| Main branch name | Auto/Ask | Detected from remote; user asked if ambiguous |
| Network access | Yes | Required to pull and push to `origin` |

### Output Contract

Produces (side-effects):

| Element | Description |
|---|---|
| Merge commits | One `--no-ff` merge commit on `<main-branch>` per succeeded worktree |
| Remote push | `origin/<main-branch>` updated once per succeeded worktree |
| Worktree removal | All succeeded worktrees removed from `git worktree list` |
| Branch deletion | Optional, user-confirmed; `git branch -d` only |
| Batch summary report | Per-worktree table: branch / merge / push / cleanup / branch-deletion status |

---

## Restrictions

### Hard Boundaries

- **MUST NOT force-push** (`--force`, `--force-with-lease`) to any branch
- **MUST NOT remove any worktree** if its merge or push failed
- **MUST NOT auto-stash** uncommitted changes — report upfront and skip the worktree
- **MUST NOT use `git branch -D`** — only `-d` (safe delete)
- **MUST NOT begin any merge** before pre-flight check completes for all selected worktrees
- **MUST NOT proceed** if invoked from inside a linked worktree, or from the main repo on a non-main branch — halt with the relevant pointer

### Skill Boundaries

**Do not do these (other skills or tools handle them)**:

- **Single-worktree delivery**: Use `deliver-feature` from inside the worktree
- **Committing pending work**: Use `commit-work` per worktree first
- **Rebasing/squashing**: Use `git rebase` directly before invoking this skill
- **Creating PRs**: Use platform-specific PR tools; this skill merges directly to main
- **Code review**: Use `review-diff` before committing; this skill does not review code

---

## Anti-Patterns

### Invocation context

✅ Run from the main repo root on the main branch
❌ Do not run from inside a linked worktree — that's `deliver-feature`'s job; the CWD becomes invalid when the worktree is later removed, causing all subsequent commands to fail

### Pre-flight order

✅ Check all selected worktrees for dirty state before starting any merge
❌ Do not check each worktree immediately before merging it — the user would discover dirty worktrees mid-batch after some merges are already committed

### Merge style

✅ `git merge --no-ff` to preserve branch history
❌ Do not use `git merge --squash` or fast-forward — history would be lost

### Push safety

✅ Standard `git push origin <main-branch>`
❌ Never use `--force` or `--force-with-lease` on main

### Cleanup order

✅ Remove worktrees only after their merge AND push both succeeded
❌ Do not remove a worktree after merge but before push — the branch would be unreachable if push fails

### Branch deletion

✅ `git branch -d` (safe) and confirm with user first
❌ Never use `git branch -D` (force) — it can delete unmerged commits

---

## Examples

### Example 1: Batch happy path

**Scenario**: Two feature worktrees are ready to merge into `main`.

**Execution**:

```bash
# Step 1: Context — main repo root, main branch ✓
git rev-parse --git-dir            # /repos/myapp/.git
git rev-parse --git-common-dir     # /repos/myapp/.git   (equal → main repo ✓)
git rev-parse --abbrev-ref HEAD    # main
git rev-parse --show-toplevel      # /repos/myapp

# Step 2: Main branch
git remote show origin | grep 'HEAD branch'   # HEAD branch: main

# Step 3: Scan
git worktree list --porcelain
# (parsed) main: /repos/myapp
#          /repos/myapp-auth   feat/user-auth
#          /repos/myapp-api    feat/api-v2
# User selects: all

# Step 4: Pre-flight
git -C /repos/myapp-auth status --porcelain   # (empty ✓)
git -C /repos/myapp-api  status --porcelain   # (empty ✓)

# Step 5: Merge + push — worktree 1
git pull origin main
git merge --no-ff feat/user-auth -m "Merge branch 'feat/user-auth' into main"
git push origin main

# Step 5: Merge + push — worktree 2
git pull origin main
git merge --no-ff feat/api-v2 -m "Merge branch 'feat/api-v2' into main"
git push origin main

# Step 6: Unified cleanup
pwd                                       # /repos/myapp ✓
git worktree remove /repos/myapp-auth
git worktree remove /repos/myapp-api

# Step 7: Branch deletion — user selects all
git branch -d feat/user-auth
git branch -d feat/api-v2
```

**Summary**:

```
integrate-worktrees summary
──────────────────────────────────────────────────────────────────────────
Worktree             Branch          Merge  Push  Cleanup  Branch
/repos/myapp-auth    feat/user-auth  ✓      ✓     ✓        deleted
/repos/myapp-api     feat/api-v2     ✓      ✓     ✓        deleted
──────────────────────────────────────────────────────────────────────────
Main repo: /repos/myapp · Main branch: main · Remote: origin
```

---

### Example 2: Pre-flight dirty detection (edge case — skip and continue)

**Scenario**: Three worktrees selected; two have uncommitted changes.

**Execution**:

```bash
# Step 4: Pre-flight
git -C /repos/myapp-auth  status --porcelain   # (empty ✓)
git -C /repos/myapp-api   status --porcelain   # M  src/api.ts
git -C /repos/myapp-ui    status --porcelain   # ?? src/temp.log
```

**Skill reports**:

```
Pre-flight check — dirty worktrees (will be skipped):
  /repos/myapp-api  (feat/api-v2)    — 1 uncommitted file(s)
  /repos/myapp-ui   (feat/dashboard) — 1 uncommitted file(s)
```

> "Proceed with the remaining clean worktrees, or halt all? [continue / halt]"

User answers `continue` → only `feat/user-auth` is merged and cleaned up. The other two are untouched.

**Summary**:

```
integrate-worktrees summary
──────────────────────────────────────────────────────────────────────────
Worktree             Branch          Merge          Push  Cleanup  Branch
/repos/myapp-auth    feat/user-auth  ✓              ✓     ✓        deleted
/repos/myapp-api     feat/api-v2     skipped(dirty) —     —        —
/repos/myapp-ui      feat/dashboard  skipped(dirty) —     —        —
──────────────────────────────────────────────────────────────────────────
```

---

### Example 3: Wrong context — invoked from inside a worktree

**Scenario**: Developer is in `/repos/myapp-api` on `feat/api-v2` and runs `integrate-worktrees` by habit.

**Execution**:

```bash
# CWD: /repos/myapp-api

git rev-parse --git-dir          # /repos/myapp/.git/worktrees/myapp-api
git rev-parse --git-common-dir   # /repos/myapp/.git   (differs from --git-dir → linked worktree, NOT main repo)
```

**Skill halts**:

> "This skill must be run from the main repo, not from inside a worktree. Current location: `/repos/myapp-api`. To deliver just the current worktree's branch, use `deliver-feature`."

No git operations performed. Exit code non-zero.

---

## AI Refactor Instruction

If this skill produces incorrect behavior:

1. **Wrong invocation context proceeded**: if the skill ran while CWD was inside a worktree (i.e., `git rev-parse --git-dir` differed from `git rev-parse --git-common-dir`), or while current branch was not main → rewind to Step 1, add the git-dir vs git-common-dir comparison + branch-equality guards
2. **Pre-flight skipped or deferred**: if `git merge` is attempted without first running `git -C <path> status --porcelain` for all selected worktrees → rewind to Step 4, complete all pre-flight checks before any merge
3. **Failed worktree deleted**: if `git worktree remove` is called for a worktree with status `failed` → halt; only the `<succeeded-list>` is eligible for removal
4. **Force-push attempted**: if `--force` or `--force-with-lease` appears in a push command → substitute standard push; if that fails, halt and report
5. **Pull skipped before merge**: if `git merge --no-ff` runs without a preceding `git pull origin <main-branch>` → re-run from the pull step

---

## Self-Check

- [ ] **Invocation context verified**: `git rev-parse --git-dir` equals `git rev-parse --git-common-dir` (main repo) AND current branch equals `<main-branch>` before proceeding
- [ ] **Main branch confirmed**: auto-detected or explicitly provided by user; not assumed
- [ ] **All linked worktrees scanned**: `git worktree list --porcelain` parsed; non-main entries presented to user
- [ ] **User selection recorded**: `all` or index-based subset captured before any pre-flight check
- [ ] **Pre-flight ran for all selected before any merge**: `git -C <path> status --porcelain` completed for every selected worktree first
- [ ] **Dirty worktrees reported upfront**: all dirty entries listed together before the continue/halt prompt
- [ ] **Pull before each merge**: `git pull origin <main-branch>` ran immediately before each `git merge --no-ff`
- [ ] **No-ff merge used**: `git merge --no-ff` confirmed; no fast-forward or squash
- [ ] **Push succeeded before worktree marked `succeeded`**: only after `git push` returned 0 is a worktree added to `<succeeded-list>`
- [ ] **Unified cleanup ran only on `<succeeded-list>`**: `git worktree remove` never called for failed or skipped entries
- [ ] **CWD confirmed before cleanup**: `pwd` matched `<main-repo>` before any `git worktree remove`
- [ ] **Branch deletion used `-d`**: no `-D` flag in any branch deletion command; user confirmed each branch
- [ ] **Summary report produced**: per-worktree table includes all entries with correct status codes
- [ ] **No force-push used**: `--force` or `--force-with-lease` never appeared in any command

---

## 附录：输出合约 (Appendix: Output Contract)

本技能产出批量集成摘要表：

| 元素 | 格式 | 必填字段 | 路径模式 |
| :--- | :--- | :--- | :--- |
| 摘要表 | 文本表格（聊天输出） | 列：Worktree / Branch / Merge / Push / Cleanup / Branch（删除状态）；每行覆盖所有用户选中的 worktree | 标准输出，不落盘 |
| 状态码 | 单元格枚举 | Merge ∈ {✓, skipped(dirty), ✗(conflict), —}；Push/Cleanup/Branch ∈ {✓, —, deleted, kept} | 摘要表每行 |
| 失败诊断 | 列表项（仅当存在失败/冲突时） | worktree_path / failure_kind（dirty / conflict / push_rejected）/ next_step | 摘要表下方 |
| 上下文标识 | 行字段 `Main repo: <path> · Main branch: <branch> · Remote: <remote>` | path / branch / remote 三字段 | 摘要表底部 |
