---
name: merge-worktree
description: Merge the current git worktree branch into the main branch, push to origin, and remove the worktree.
description_zh: 将当前 git worktree 分支合并到主分支，推送到 origin，并删除该 worktree。
tags: [git, workflow, automation]
version: 0.1.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [merge worktree, finish worktree, close worktree]
input_schema:
  type: free-form
  description: Current git worktree with a branch ready to merge
output_schema:
  type: side-effect
  description: Feature branch merged into main, pushed to origin, worktree removed
---

# Skill: merge-worktree

## Purpose

Automates the end-of-worktree lifecycle: merge the current worktree's branch into the project main branch, push the result to origin, and clean up the worktree directory. Eliminates the error-prone multi-step manual process of switching contexts, merging, pushing, and removing worktrees.

---

## Core Objective

**Primary goal**: Safely land the current worktree's branch onto the main branch, deliver it to origin, and remove the worktree — leaving the repository in a clean state.

**Success Criteria** (all must be satisfied):

1. ✅ **Clean working tree**: No uncommitted changes exist in the worktree before merging
2. ✅ **Main branch identified**: Main branch is known (auto-detected or confirmed by user)
3. ✅ **Merge completed**: Feature branch merged into main with `--no-ff` (history preserved)
4. ✅ **Pushed to origin**: `git push origin <main-branch>` succeeds without force-push
5. ✅ **Worktree removed**: `git worktree remove` completes; `git worktree list` no longer shows the path
6. ✅ **No data loss**: Merge and push both succeed before worktree is deleted

**Acceptance Test**: After skill completes, `git log --oneline <main>` shows the merge commit, `git worktree list` does not show the removed path, and the remote is up to date.

---

## Scope Boundaries

**This skill handles**:

- Detecting current worktree path and branch
- Determining the main branch (auto-detect or ask user)
- Verifying the working tree is clean
- Merging the feature branch into main (`--no-ff`)
- Pushing main to origin
- Removing the worktree directory
- Optionally deleting the feature branch after successful cleanup

**This skill does NOT handle**:

- Committing uncommitted changes (use `commit-work` skill first)
- Rebasing or squashing commits before merge
- Resolving merge conflicts (halts and reports to user)
- Creating or managing pull requests
- Pushing feature branches or creating remote tracking branches
- Force-pushing to any branch

**Handoff points**:
- If the working tree is dirty → halt, instruct user to run `commit-work` first
- If a merge conflict occurs → halt, provide conflict resolution instructions
- If push is rejected → halt, instruct user to pull and re-run

---

## Use Cases

- Developer finishes work in a worktree and wants to integrate it into main and clean up
- CI/automation finishing an isolated worktree task and landing the result
- After completing a `commit-work` cycle in a worktree, delivering the work end-to-end

---

## Behavior

### Workflow (Checklist)

**Step 1 — Detect current worktree**

```bash
git worktree list
git rev-parse --abbrev-ref HEAD       # current branch name
git rev-parse --show-toplevel         # worktree root path
```

Record: `<feature-branch>`, `<worktree-path>`, `<main-repo-path>` (first entry in `git worktree list`).

**Step 2 — Determine main branch**

```bash
git remote show origin | grep 'HEAD branch'
```

- If result is unambiguous (e.g., `HEAD branch: main`) → use it.
- If the command fails or returns multiple candidates → check for `main` then `master` in `git branch -r`.
- If still ambiguous → **ask the user**:
  > "Could not determine the main branch automatically. What is the name of the main branch (e.g., main, master, develop)?"

**Step 3 — Verify working tree is clean**

```bash
git status --porcelain
```

- If output is non-empty → **halt**:
  > "The working tree has uncommitted changes. Please commit or stash them first (consider using the `commit-work` skill), then re-run this skill."

**Step 4 — Merge feature branch into main**

From the main repo path (not the worktree):

```bash
cd <main-repo-path>
git checkout <main-branch>
git pull origin <main-branch>          # sync before merging
git merge --no-ff <feature-branch> -m "Merge branch '<feature-branch>' into <main-branch>"
```

- If merge conflict → **halt**, do not push, do not delete worktree:
  > "Merge conflict detected. Resolve the conflicts in `<main-repo-path>`, complete the merge manually, then push and remove the worktree."

**Step 5 — Push to origin**

```bash
git push origin <main-branch>
```

- If rejected (non-fast-forward) → **halt**, do not delete worktree:
  > "Push rejected. The remote has new commits. Run `git pull --rebase origin <main-branch>` in `<main-repo-path>`, resolve any conflicts, then push and remove the worktree manually."

**Step 6 — Remove worktree**

```bash
git worktree remove <worktree-path>
```

Only execute after both merge and push succeed.

**Step 7 — Offer to delete feature branch**

Ask the user:
> "Worktree removed. Delete the local feature branch `<feature-branch>`? (yes/no)"

If yes:
```bash
git branch -d <feature-branch>
```

Use `-d` (safe delete) only — never `-D`. If `-d` fails because the branch is not fully merged (unexpected), report the error and stop.

**Step 8 — Report outcome**

Summarize:
- Branch merged: `<feature-branch>` → `<main-branch>` ✓
- Pushed to origin: `<main-branch>` ✓
- Worktree removed: `<worktree-path>` ✓
- Feature branch deleted: yes/no

---

## Input & Output

### Input Requirements

- An active git worktree with a named branch
- A clean working tree (no uncommitted changes)
- Network access to push to `origin`

### Output Contract

Produces (side-effects):

| Element | Description |
|---|---|
| Merge commit | `--no-ff` merge commit on `<main-branch>` |
| Remote push | `origin/<main-branch>` updated |
| Worktree removal | Directory removed from `git worktree list` |
| Branch deletion | (optional, user-confirmed) local branch deleted |

Summary report includes: branch names, merge commit hash, push confirmation, worktree path removed.

---

## Restrictions

### Hard Boundaries

- **Never force-push** (`--force`, `--force-with-lease`) to any branch
- **Never delete worktree** if merge or push failed
- **Never auto-stash** uncommitted changes — halt and inform the user instead
- **Never use `-D`** (force-delete) for branch deletion
- **Never proceed** if `git status --porcelain` returns non-empty output

### Skill Boundaries

**Do not do these (other skills or tools handle them)**:

- **Committing pending work**: Use `commit-work` skill before invoking this skill
- **Rebasing/squashing**: Use `git rebase` directly before invoking this skill
- **Creating PRs**: Use platform-specific PR tools; this skill merges directly to main
- **Code review**: Use `review-diff` before committing; this skill does not review code

---

## Anti-Patterns

### Working tree check

✅ Always verify `git status --porcelain` is empty before merging
❌ Do not skip the clean-tree check and merge with uncommitted changes

### Merge style

✅ Use `git merge --no-ff` to preserve branch history
❌ Do not use `git merge --squash` or `git merge` (fast-forward only) — history would be lost

### Push safety

✅ Use `git push origin <main-branch>` (standard push)
❌ Never use `--force` or `--force-with-lease` on main

### Deletion order

✅ Delete worktree only after merge AND push both succeed
❌ Do not delete worktree after merge but before push — the branch would be unreachable if push fails

### Branch deletion

✅ Use `git branch -d` (safe) and confirm with user first
❌ Never use `git branch -D` (force) — it deletes unmerged commits

---

## Examples

### Example 1: Standard flow (happy path)

**Scenario**: Feature branch `feat/user-auth` in worktree `/repos/myapp-auth` is ready to merge into `main`.

**Execution**:

```bash
# Step 1: Detect
git worktree list
# /repos/myapp        abc1234 [main]
# /repos/myapp-auth   def5678 [feat/user-auth]

git rev-parse --abbrev-ref HEAD   # feat/user-auth
git rev-parse --show-toplevel     # /repos/myapp-auth

# Step 2: Determine main branch
git remote show origin | grep 'HEAD branch'
# HEAD branch: main

# Step 3: Verify clean
git status --porcelain
# (empty — proceed)

# Step 4: Merge
cd /repos/myapp
git checkout main
git pull origin main
git merge --no-ff feat/user-auth -m "Merge branch 'feat/user-auth' into main"

# Step 5: Push
git push origin main

# Step 6: Remove worktree
git worktree remove /repos/myapp-auth

# Step 7: Ask user about branch deletion
# User answers: yes
git branch -d feat/user-auth
```

**Outcome report**:
- Branch merged: `feat/user-auth` → `main` ✓ (commit `abc9999`)
- Pushed to origin: `main` ✓
- Worktree removed: `/repos/myapp-auth` ✓
- Feature branch deleted: yes ✓

---

### Example 2: Dirty working tree (edge case — halt)

**Scenario**: User invokes skill but has uncommitted changes in the worktree.

**Execution**:

```bash
git status --porcelain
# M  src/auth.ts
# ?? src/temp.log
```

**Skill halts**:

> "The working tree has uncommitted changes (`src/auth.ts`, `src/temp.log`). Please commit or stash them first (consider using the `commit-work` skill), then re-run `merge-worktree`."

No merge, push, or worktree removal occurs.

---

### Example 3: Ambiguous main branch (edge case — ask user)

**Scenario**: `git remote show origin` fails (no network) and both `main` and `develop` exist.

**Execution**:

```bash
git remote show origin | grep 'HEAD branch'
# (error: unable to connect to origin)

git branch -r
# origin/main
# origin/develop
# origin/feat/user-auth
```

**Skill asks**:

> "Could not determine the main branch automatically. Both `main` and `develop` exist on origin. What is the name of the main branch?"

User responds: `main` → skill continues from Step 4 using `main`.

---

## AI Refactor Instruction

If this skill produces incorrect behavior:

1. Check Step 2 (main branch detection) — ensure `git remote show origin` output is parsed correctly; add `git branch -r` fallback
2. Check Step 3 (dirty tree) — ensure `git status --porcelain` is used (not `git status`)
3. Check Step 4 (merge) — ensure `git pull origin <main>` runs before merge to avoid non-fast-forward push failure
4. Check Step 6 (worktree removal) — ensure it runs only after Step 5 (push) succeeds
5. Check Step 7 (branch deletion) — ensure `-d` not `-D` is used, and user confirmed

---

## Self-Check

- [ ] **Worktree detected**: `git worktree list` output parsed; feature branch and worktree path captured
- [ ] **Main branch confirmed**: Auto-detected or explicitly provided by user; not assumed
- [ ] **Clean tree verified**: `git status --porcelain` returned empty before any merge
- [ ] **Pull before merge**: `git pull origin <main>` ran before `git merge` to minimize push rejection
- [ ] **No-ff merge**: Used `git merge --no-ff`, not fast-forward
- [ ] **Push succeeded**: `git push origin <main>` completed without error
- [ ] **Worktree removed after push**: Deletion happened only after push confirmed
- [ ] **Branch deletion confirmed**: User was asked; `-d` (not `-D`) used
- [ ] **Outcome reported**: Summary includes merge commit, push status, worktree path, branch deletion status
- [ ] **No force-push used**: `--force` or `--force-with-lease` never appeared in any command
