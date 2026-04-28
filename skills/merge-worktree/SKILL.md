---
name: merge-worktree
description: From the main repo, scan all active worktrees, select and batch-merge branches into main, push, and clean up together.
description_zh: 从主仓库扫描所有 worktree，批量将选中分支合并到主分支、推送并统一清理。
tags: [git, workflow, automation]
version: 1.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [merge worktrees, merge all worktrees, finish worktrees, close worktrees, batch merge worktrees]
input_schema:
  type: free-form
  description: Main git repository with one or more active linked worktrees ready to merge
output_schema:
  type: side-effect
  description: Selected feature branches merged into main, pushed to origin, worktrees removed; per-worktree summary report
---

# Skill: merge-worktree

## Purpose

Automates the batch worktree lifecycle from the main repo: scan all active linked worktrees, let the user select which to merge, verify all selected are clean, merge and push each in sequence, then remove all successfully-merged worktrees together. Eliminates the need to cd into each worktree directory and invoke a merge operation separately.

---

## Core Objective

**Primary goal**: From the main repo, land all selected worktree branches onto main, deliver them to origin, and clean up — leaving the repository in a clean state.

**Success Criteria** (all must be satisfied):

1. ✅ **Invocation context verified**: CWD is the main repo root, not inside a linked worktree
2. ✅ **All linked worktrees discovered**: `git worktree list` parsed; non-main worktrees presented to user
3. ✅ **Pre-flight completed before any merge**: All selected worktrees checked for clean working tree; all dirty ones reported upfront
4. ✅ **Batch merge + push**: Each selected clean worktree merged with `--no-ff` and pushed; per-worktree status (`succeeded`/`failed`) recorded
5. ✅ **Unified cleanup**: All `succeeded` worktrees removed together; no failed worktree is deleted
6. ✅ **Summary reported**: Per-worktree table covers merge, push, cleanup, and branch-deletion status for every entry

**Acceptance Test**: After skill completes, `git log --oneline <main>` shows one merge commit per succeeded worktree; `git worktree list` shows only the main repo and any failed/skipped worktrees; remote is up to date.

---

## Scope Boundaries

**This skill handles**:

- Verifying invocation context (main repo, not a linked worktree)
- Detecting the main branch (auto-detect or ask user)
- Scanning and listing all active linked worktrees
- User selection of which worktrees to merge (`all` or subset)
- Pre-flight clean-tree check for all selected worktrees before any merge begins
- Sequential merge (`--no-ff`) + push for each selected clean worktree
- Per-failure user decision: continue with remaining or abort
- Unified cleanup of all successfully-merged worktrees
- Optional feature branch deletion (user-confirmed, `-d` only)
- Per-worktree summary report

**This skill does NOT handle**:

- Committing uncommitted changes (use `commit-work` skill first, per worktree)
- Rebasing or squashing commits before merge
- Resolving merge conflicts (halts and reports to user)
- Creating or managing pull requests
- Pushing feature branches or creating remote tracking branches
- Force-pushing to any branch
- Parallel merge execution (always sequential)

**Handoff points**:
- If any selected worktree is dirty → report all dirty ones upfront; ask user to continue with clean ones or halt all
- If a merge conflict occurs → halt that worktree; ask whether to continue with remaining
- If push is rejected → halt that worktree; ask whether to continue with remaining
- If invoked from inside a linked worktree → halt immediately

---

## Use Cases

- Developer has 2–4 feature worktrees ready to land onto main and wants to handle them in one invocation
- End-of-sprint batch cleanup: merging all completed feature worktrees from the main repo
- CI/automation that spawned multiple parallel worktrees for isolated tasks, now collecting results
- After completing `commit-work` cycles in multiple worktrees, delivering all work end-to-end

---

## Behavior

### Workflow (Checklist)

**Step 1 — Verify invocation context**

```bash
git rev-parse --show-toplevel          # current repo root
git worktree list --porcelain          # first worktree entry = main repo path
```

Parse `git worktree list --porcelain`. The first block is the main repo. Compare its `worktree` path against `git rev-parse --show-toplevel`.

- If they do NOT match (currently inside a linked worktree) → **halt**:
  > "This skill must be run from the main repo, not from inside a worktree. Current location: `<cwd>`. Main repo is at: `<main-repo-path>`. Run `cd <main-repo-path>` and re-invoke."

- If they match → record `<main-repo-path>`. CWD remains here for every subsequent step.

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
git worktree list
```

Parse output. Filter out the main repo entry (the one at `<main-repo-path>` on `<main-branch>`). Each remaining entry is a candidate.

- If no linked worktrees found → **halt**:
  > "No active linked worktrees found. Nothing to merge."

Present the list with path and branch name:

```
Active worktrees available to merge:
  [1]  /repos/myapp-auth      feat/user-auth
  [2]  /repos/myapp-api       feat/api-v2
  [3]  /repos/myapp-ui        feat/dashboard
```

Ask:
> "Which worktrees should be merged? Enter numbers separated by commas, or type `all`:"

Record `<selected-list>`.

**Step 4 — Pre-flight: check all selected worktrees**

For each worktree in `<selected-list>`:

```bash
git -C <worktree-path> status --porcelain
```

Collect all results. Build `<clean-list>` and `<dirty-list>`.

If `<dirty-list>` is non-empty, report all dirty entries in a single block before any merge begins:

```
Pre-flight check — dirty worktrees (will be skipped):
  /repos/myapp-api   (feat/api-v2)    — 3 uncommitted file(s)
  /repos/myapp-ui    (feat/dashboard) — 1 uncommitted file(s)
```

Ask:
> "The above worktrees have uncommitted changes. Proceed with the remaining clean worktrees, or halt all? [continue / halt]"

- `halt` → stop; no merges performed.
- `continue` → proceed with `<clean-list>` only. If `<clean-list>` is empty → halt, nothing to do.

No auto-stash is performed under any condition.

**Step 5 — Batch merge + push (sequential)**

For each worktree `W` in `<clean-list>`:

```bash
# Pull main to stay current across multi-worktree run
git checkout <main-branch>
git pull origin <main-branch>

# Merge with --no-ff
git merge --no-ff <W.branch> -m "Merge branch '<W.branch>' into <main-branch>"

# Push
git push origin <main-branch>
```

On failure for worktree `W`:

- If merge conflict:
  > "Merge conflict merging `<W.branch>` into `<main-branch>`. Resolve conflicts in `<main-repo-path>`, complete the merge manually, then push and remove the worktree."
- If push rejected (non-fast-forward):
  > "Push rejected after merging `<W.branch>`. Run `git reset --hard HEAD~1` in `<main-repo-path>` to undo the merge, then pull, re-merge, and push manually."

In both cases, mark `W` as `failed` and ask:
> "Continue with the remaining worktrees, or abort all remaining? [continue / abort]"

- `abort` → stop; do not touch any remaining worktrees.
- `continue` → mark `W` as `failed`, proceed to next.

Record per-worktree outcome: `succeeded` or `failed`.

**Step 6 — Unified cleanup**

After all merges complete, verify CWD is still the main repo:

```bash
pwd   # must equal <main-repo-path>
```

For each worktree in `<succeeded-list>` only:

```bash
git worktree remove <worktree-path>
```

Execute sequentially. If an individual removal fails (e.g., path already gone), log the error and continue.

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

Use `-d` only — never `-D`. If `-d` fails (unexpected after a successful `--no-ff` merge), report and stop for that branch.

**Step 8 — Summary report**

```
merge-worktree summary
──────────────────────────────────────────────────────────────────────────
Worktree               Branch            Merge         Push   Cleanup  Branch
/repos/myapp-auth      feat/user-auth    ✓             ✓      ✓        deleted
/repos/myapp-api       feat/api-v2       ✗(conflict)   —      —        —
/repos/myapp-ui        feat/dashboard    skipped(dirty) —     —        —
──────────────────────────────────────────────────────────────────────────
Main branch: main  |  Remote: origin
```

Status codes: `✓` succeeded · `✗(reason)` failed · `skipped(dirty)` pre-flight fail · `—` not applicable

---

## Input & Output

### Input Requirements

| Input | Required | Description |
|---|---|---|
| Main repo context | Yes | CWD must be the main repo root; halts if inside a linked worktree |
| Active linked worktrees | Yes | At least one non-main linked worktree must exist |
| Worktree selection | User input | `all` or comma-separated indices from the presented list |
| Clean working tree | Per-worktree | Dirty worktrees are reported upfront and skipped; no auto-stash |
| Main branch name | Auto/Ask | Detected from remote; user asked if ambiguous |
| Network access | Yes | Required to push to `origin` |

### Output Contract

Produces (side-effects):

| Element | Description |
|---|---|
| Merge commits | One `--no-ff` merge commit on `<main-branch>` per succeeded worktree |
| Remote push | `origin/<main-branch>` updated once per succeeded worktree |
| Worktree removal | All succeeded worktrees removed from `git worktree list` |
| Branch deletion | Optional, user-confirmed; `git branch -d` only |
| Batch summary report | Per-worktree table: branch, merge, push, cleanup, branch-deletion status |

---

## Restrictions

### Hard Boundaries

- **MUST NOT force-push** (`--force`, `--force-with-lease`) to any branch
- **MUST NOT remove any worktree** if its merge or push failed
- **MUST NOT auto-stash** uncommitted changes — report upfront and skip the worktree
- **MUST NOT use `git branch -D`** — only `-d` (safe delete)
- **MUST NOT begin any merge** before pre-flight check completes for all selected worktrees
- **MUST NOT proceed** if invoked from inside a linked worktree — halt immediately

### Skill Boundaries

**Do not do these (other skills or tools handle them)**:

- **Committing pending work**: Use `commit-work` skill per worktree before invoking this skill
- **Rebasing/squashing**: Use `git rebase` directly before invoking this skill
- **Creating PRs**: Use platform-specific PR tools; this skill merges directly to main
- **Code review**: Use `review-diff` before committing; this skill does not review code

---

## Anti-Patterns

### Invocation context

✅ Always run from the main repo root
❌ Do not run from inside a linked worktree — the CWD becomes invalid when the worktree is later removed, causing all subsequent commands to fail

### Pre-flight order

✅ Check all selected worktrees for dirty state before starting any merge
❌ Do not check each worktree immediately before merging it — the user would discover dirty worktrees mid-batch after some merges are already committed

### Merge style

✅ Use `git merge --no-ff` to preserve branch history
❌ Do not use `git merge --squash` or fast-forward merge — history would be lost

### Push safety

✅ Use `git push origin <main-branch>` (standard push)
❌ Never use `--force` or `--force-with-lease` on main

### Deletion order

✅ Remove worktrees only after their merge AND push both succeeded
❌ Do not remove a worktree after merge but before push — the branch would be unreachable if push fails

### Branch deletion

✅ Use `git branch -d` (safe) and confirm with user first
❌ Never use `git branch -D` (force) — it can delete unmerged commits

---

## Examples

### Example 1: Batch happy path

**Scenario**: Two feature worktrees are ready to merge into `main`.

**Execution**:

```bash
# Step 1: Guard — invoked from main repo
git rev-parse --show-toplevel   # /repos/myapp
git worktree list --porcelain   # first entry: /repos/myapp → match ✓

# Step 2: Main branch
git remote show origin | grep 'HEAD branch'
# HEAD branch: main

# Step 3: Scan
git worktree list
# /repos/myapp        abc1234 [main]
# /repos/myapp-auth   def5678 [feat/user-auth]
# /repos/myapp-api    ghi9012 [feat/api-v2]
# User selects: all

# Step 4: Pre-flight
git -C /repos/myapp-auth status --porcelain   # (empty ✓)
git -C /repos/myapp-api  status --porcelain   # (empty ✓)

# Step 5: Merge + push — worktree 1
git checkout main
git pull origin main
git merge --no-ff feat/user-auth -m "Merge branch 'feat/user-auth' into main"
git push origin main

# Step 5: Merge + push — worktree 2
git pull origin main
git merge --no-ff feat/api-v2 -m "Merge branch 'feat/api-v2' into main"
git push origin main

# Step 6: Unified cleanup
pwd                                    # /repos/myapp ✓
git worktree remove /repos/myapp-auth
git worktree remove /repos/myapp-api

# Step 7: Branch deletion — user selects all
git branch -d feat/user-auth
git branch -d feat/api-v2
```

**Summary**:

```
merge-worktree summary
──────────────────────────────────────────────────────────────────────────
Worktree             Branch          Merge  Push  Cleanup  Branch
/repos/myapp-auth    feat/user-auth  ✓      ✓     ✓        deleted
/repos/myapp-api     feat/api-v2     ✓      ✓     ✓        deleted
──────────────────────────────────────────────────────────────────────────
Main branch: main  |  Remote: origin
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
merge-worktree summary
──────────────────────────────────────────────────────────────────────────
Worktree             Branch          Merge         Push  Cleanup  Branch
/repos/myapp-auth    feat/user-auth  ✓             ✓     ✓        deleted
/repos/myapp-api     feat/api-v2     skipped(dirty) —    —        —
/repos/myapp-ui      feat/dashboard  skipped(dirty) —    —        —
──────────────────────────────────────────────────────────────────────────
```

---

### Example 3: Mid-batch merge conflict (edge case — continue past failure)

**Scenario**: Two clean worktrees; the second has a conflicting change with recent main.

**Execution**:

```bash
# Step 5: Worktree 1 — succeeds
git merge --no-ff feat/user-auth -m "Merge branch 'feat/user-auth' into main"
git push origin main
# ✓ succeeded

# Step 5: Worktree 2 — conflict
git merge --no-ff feat/api-v2 -m "Merge branch 'feat/api-v2' into main"
# CONFLICT (content): Merge conflict in src/api.ts
```

> "Merge conflict merging `feat/api-v2` into `main`. Continue with remaining worktrees, or abort? [continue / abort]"

User answers `continue` (no remaining worktrees) → proceed to cleanup.

```bash
# Step 6: Cleanup — only feat/user-auth succeeded
pwd                                    # /repos/myapp ✓
git worktree remove /repos/myapp-auth  # ✓
# /repos/myapp-api NOT removed (status = failed)
```

**Summary**:

```
merge-worktree summary
──────────────────────────────────────────────────────────────────────────
Worktree             Branch          Merge          Push  Cleanup  Branch
/repos/myapp-auth    feat/user-auth  ✓              ✓     ✓        deleted
/repos/myapp-api     feat/api-v2     ✗(conflict)    —     —        —
──────────────────────────────────────────────────────────────────────────
```

---

## AI Refactor Instruction

If this skill produces incorrect behavior:

1. **Wrong invocation context**: if the skill proceeds without verifying CWD matches the main repo → rewind to Step 1, add the invocation guard check
2. **Pre-flight skipped or deferred**: if `git merge` is attempted without first running `git -C <path> status --porcelain` for all selected worktrees → rewind to Step 4, complete all pre-flight checks before any merge
3. **Failed worktree deleted**: if `git worktree remove` is called for a worktree with status `failed` → halt; only the `<succeeded-list>` is eligible for removal
4. **Force-push attempted**: if `--force` or `--force-with-lease` appears in a push command → substitute standard push; if that fails, halt and report
5. **Pull skipped before merge**: if `git merge --no-ff` runs without a preceding `git pull origin <main-branch>` → re-run from the pull step

---

## Self-Check

- [ ] **Invocation context verified**: `git rev-parse --show-toplevel` matched main repo path before proceeding
- [ ] **Main branch confirmed**: auto-detected or explicitly provided by user; not assumed
- [ ] **All linked worktrees scanned**: `git worktree list` parsed; non-main entries presented to user
- [ ] **User selection recorded**: `all` or index-based subset captured before any pre-flight check
- [ ] **Pre-flight ran for all selected before any merge**: `git -C <path> status --porcelain` completed for every selected worktree first
- [ ] **Dirty worktrees reported upfront**: all dirty entries listed together before the continue/halt prompt
- [ ] **Pull before each merge**: `git pull origin <main-branch>` ran immediately before each `git merge --no-ff`
- [ ] **No-ff merge used**: `git merge --no-ff` confirmed; no fast-forward or squash
- [ ] **Push succeeded before worktree marked `succeeded`**: only after `git push` returns 0 is a worktree added to `<succeeded-list>`
- [ ] **Unified cleanup ran only on `<succeeded-list>`**: `git worktree remove` never called for failed or skipped entries
- [ ] **CWD confirmed before cleanup**: `pwd` matched `<main-repo-path>` before any `git worktree remove`
- [ ] **Branch deletion used `-d`**: no `-D` flag in any branch deletion command; user confirmed each branch
- [ ] **Summary report produced**: per-worktree table includes all entries with correct status codes
- [ ] **No force-push used**: `--force` or `--force-with-lease` never appeared in any command

---

## 附录：输出合约 (Appendix: Output Contract)

本技能产出批量合并摘要表：

| 元素 | 格式 | 必填字段 | 路径模式 |
| :--- | :--- | :--- | :--- |
| 摘要表 | 文本表格（聊天输出） | 列：Worktree / Branch / Merge / Push / Cleanup / Branch（删除状态）；每行覆盖所有用户选中的 worktree | 标准输出，不落盘 |
| 状态码 | 单元格枚举 | Merge ∈ {✓, skipped(dirty), ✗(conflict), —}；Push/Cleanup/Branch ∈ {✓, —, deleted, kept} | 摘要表每行 |
| 失败诊断 | 列表项（仅当存在失败/冲突时） | worktree_path / failure_kind（dirty / conflict / push_rejected）/ next_step | 摘要表下方 |
