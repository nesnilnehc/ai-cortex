---
name: deliver-feature
description: From inside a linked worktree, deliver the current feature branch into main — merge with --no-ff, push, and optionally clean up the worktree, all without leaving CWD.
description_zh: 在 linked worktree 内将当前 feature 分支交付到 main——以 --no-ff 合并、推送，并可选清理本 worktree，全程不离开当前目录。
tags: [git, workflow, automation]
version: 1.0.0
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

# Skill: deliver-feature

## Purpose

Lands the current worktree's feature branch onto main without requiring the user to switch directories. Operates the main repo via `git -C <main-repo>` so the user keeps working in their feature worktree until they explicitly choose to leave it. Eliminates the round trip: cd to main repo → invoke batch tool → select just-finished branch → cd back.

---

## Core Objective

**Primary goal**: Deliver the current worktree's feature branch onto main (via `--no-ff` merge), push to origin, and let the user decide whether to keep or remove the worktree — all without leaving the worktree directory.

**Success Criteria** (all must be satisfied):

1. ✅ **Invocation context verified**: CWD is inside a linked worktree (not the main repo), and current branch is not the main branch
2. ✅ **Pre-flight clean**: Current worktree has no uncommitted changes (`git status --porcelain` empty)
3. ✅ **Merge in main repo, not in worktree**: `git -C <main-repo>` used for `pull` / `merge --no-ff` / `push`; CWD remains the worktree throughout the merge
4. ✅ **Push succeeded**: `git push origin <main-branch>` returns 0 before any cleanup is offered
5. ✅ **User-controlled cleanup**: User explicitly chooses keep / remove (with optional branch delete via `-d` only); no implicit removal
6. ✅ **Single-branch summary**: Reports merge commit hash, push status, and cleanup outcome

**Acceptance Test**: After skill completes, `git -C <main-repo> log --oneline <main-branch>` shows exactly one new merge commit referencing the feature branch; `git -C <main-repo> ls-remote origin <main-branch>` matches local; if user chose remove, `git worktree list` no longer contains the source worktree.

---

## Scope Boundaries

**This skill handles**:

- Verifying invocation context (inside a linked worktree, on a non-main branch)
- Detecting the main branch (auto-detect; ask user only if ambiguous)
- Pre-flight clean-tree check on the current worktree
- Locating the main repo path via `git worktree list --porcelain`
- Pull → `--no-ff` merge → push, executed against the main repo via `git -C`
- Handing back to the user on conflict or push rejection (no auto-resolve)
- Optional worktree removal and feature branch deletion (user-confirmed, `-d` only)
- Single-branch summary report

**This skill does NOT handle**:

- Multiple worktrees (use `integrate-worktrees` from the main repo on the main branch)
- Committing uncommitted changes (use `commit-work` first)
- Rebasing or squashing commits before merge
- Resolving merge conflicts (halts and reports to user)
- Creating or managing pull requests
- Force-pushing to any branch

**Handoff points**:

- **→ `integrate-worktrees`**: when the user is in the main repo on the main branch and wants to land multiple worktrees in one batch
- **Halt and instruct user**: if invoked from the main repo (not a worktree), or from a worktree currently on the main branch
- **On merge conflict**: halt and instruct the user to resolve in the main repo; do not touch the worktree
- **On push rejection**: halt and instruct the user to undo the merge in the main repo (e.g., `git -C <main-repo> reset --hard HEAD~1`), pull, and retry manually

---

## Use Cases

- A developer just finished a feature in `/repos/myapp-api` (worktree on `feat/api-v2`) and wants to land it into main without leaving the worktree
- After running `commit-work` in a worktree, immediately delivering that single branch
- IDE / editor session anchored in a worktree directory; user wants to ship the feature without breaking their session

---

## Behavior

### Workflow (Checklist)

**Step 1 — Verify invocation context**

```bash
git rev-parse --git-dir              # main repo: <root>/.git ; linked worktree: <main-root>/.git/worktrees/<name>
git rev-parse --git-common-dir       # both contexts return the same value: <main-root>/.git
git rev-parse --abbrev-ref HEAD      # current branch
git rev-parse --show-toplevel        # current worktree root (CWD's repo root)
```

Determine the context: a linked worktree has `git-dir != git-common-dir` (the per-worktree `.git/worktrees/<name>` vs the shared `.git`). Equivalently, the file at `<toplevel>/.git` is a regular file (gitlink) in a linked worktree, and a directory in the main repo.

- If `git rev-parse --git-dir` equals `git rev-parse --git-common-dir` (i.e., CWD is the main repo, not a linked worktree) → **halt**:
  > "This skill must be run from inside a linked worktree, not from the main repo. Current location: `<cwd>`. To batch-merge multiple worktrees from the main repo, use `integrate-worktrees`."

- If current branch equals the detected main branch (see Step 2) → **halt**:
  > "Current branch is `<main-branch>`. This skill delivers a feature branch into main, not main into itself. Switch to a feature branch in this worktree, or use `integrate-worktrees` from the main repo."

Record `<feature-worktree>` (= `git rev-parse --show-toplevel`) and `<feature-branch>` (= current branch).

**Step 2 — Determine main branch and locate main repo**

```bash
git remote show origin | grep 'HEAD branch'
```

- Unambiguous result (e.g., `HEAD branch: main`) → use it.
- Command fails or returns nothing → check `git branch -r` for `origin/main` then `origin/master`.
- Still ambiguous → **ask the user**:
  > "Could not determine the main branch automatically. What is the name of the main branch (e.g., main, master, develop)?"

Record `<main-branch>`.

Locate the main repo from the worktree list:

```bash
git worktree list --porcelain
```

Parse the porcelain output. The first record is the main repo (its `worktree` line gives the path). Record `<main-repo>`. Sanity check: `<main-repo> != <feature-worktree>`.

**Step 3 — Pre-flight: current worktree must be clean**

```bash
git status --porcelain
```

If output is non-empty → **halt**:
> "Current worktree `<feature-worktree>` has uncommitted changes. Commit them first (e.g., via `commit-work`) and re-invoke. No auto-stash."

**Step 4 — Pull main, merge feature branch, push (executed via `git -C <main-repo>`)**

```bash
git -C <main-repo> checkout <main-branch>
git -C <main-repo> pull origin <main-branch>
git -C <main-repo> merge --no-ff <feature-branch> -m "Merge branch '<feature-branch>' into <main-branch>"
git -C <main-repo> push origin <main-branch>
```

**CWD remains `<feature-worktree>` for every command** — the `git -C` flag drives the main repo without changing the user's location.

On conflict during merge → **halt**:
> "Merge conflict merging `<feature-branch>` into `<main-branch>` (in main repo `<main-repo>`). Resolve conflicts there manually, complete the merge, then run `git -C <main-repo> push origin <main-branch>`. The worktree is untouched."

On push rejection (non-fast-forward) → **halt**:
> "Push rejected after merging `<feature-branch>`. In `<main-repo>`, run `git reset --hard HEAD~1` to undo the merge, then `git pull`, re-merge, and push manually."

After successful push, capture `<merge-commit-hash>` via `git -C <main-repo> rev-parse <main-branch>`.

**Step 5 — Ask the user about cleanup**

Present a single prompt with three options:

> "Delivery complete. What should happen to the worktree `<feature-worktree>` and branch `<feature-branch>`?
>
> [1] Keep worktree (stay here, branch kept)
> [2] Remove worktree, keep branch (cd back to main repo)
> [3] Remove worktree and delete branch (`git branch -d`, safe delete)
>
> Choose 1 / 2 / 3:"

For options 2 and 3, the skill outputs a final instruction telling the user to cd to `<main-repo>` (the skill itself cannot change the user's shell CWD; it only runs the git commands).

For options 2 and 3, execute (from `<main-repo>` via `git -C`):

```bash
git -C <main-repo> worktree remove <feature-worktree>
```

For option 3 only, after worktree removal:

```bash
git -C <main-repo> branch -d <feature-branch>
```

Use `-d` only — never `-D`. If `-d` fails (unexpected after a successful `--no-ff` merge), report the error and stop deletion (do not retry with `-D`).

**Step 6 — Summary report**

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
Next: cd /repos/myapp        (only when worktree was removed)
```

---

## Input & Output

### Input Requirements

| Input | Required | Description |
|---|---|---|
| Worktree context | Yes | CWD must be inside a linked worktree; halts if in main repo |
| Non-main branch | Yes | Current branch must not be `<main-branch>`; halts otherwise |
| Clean working tree | Yes | `git status --porcelain` must be empty; no auto-stash |
| Cleanup choice | User input | One of keep / remove-keep-branch / remove-and-delete-branch |
| Main branch name | Auto/Ask | Detected from remote; user asked if ambiguous |
| Network access | Yes | Required to pull and push to `origin` |

### Output Contract

Produces (side-effects):

| Element | Description |
|---|---|
| Merge commit | Exactly one `--no-ff` merge commit on `<main-branch>` in the main repo |
| Remote push | `origin/<main-branch>` updated once |
| Worktree removal | Optional, user-chosen |
| Branch deletion | Optional, user-chosen; `git branch -d` only |
| Summary report | Single-branch table with merge commit hash, push status, cleanup outcome, and a follow-up cd hint when applicable |

---

## Restrictions

### Hard Boundaries

- **MUST NOT change CWD** — all main-repo operations go through `git -C <main-repo>`; the user's shell stays in the worktree
- **MUST NOT force-push** (`--force`, `--force-with-lease`) to any branch
- **MUST NOT auto-stash** uncommitted changes — halt and instruct the user
- **MUST NOT use `git branch -D`** — only `-d`
- **MUST NOT remove the worktree** before merge AND push both succeed
- **MUST NOT proceed** if invoked from the main repo or from a worktree on the main branch — halt with the relevant pointer

### Skill Boundaries

**Do not do these (other skills or tools handle them)**:

- **Batch merging multiple worktrees**: Use `integrate-worktrees` from the main repo on the main branch
- **Committing pending work**: Use `commit-work` before invoking this skill
- **Rebasing/squashing**: Use `git rebase` directly before invoking this skill
- **Creating PRs**: Use platform-specific PR tools; this skill merges directly to main
- **Code review**: Use `review-diff` before committing; this skill does not review code

---

## Anti-Patterns

### Invocation context

✅ Run from inside a linked worktree on a non-main branch
❌ Do not run from the main repo — that's `integrate-worktrees`'s job; running this from main has no current worktree to deliver

### CWD discipline

✅ Use `git -C <main-repo>` for every main-repo operation; CWD stays in the worktree
❌ Do not `cd <main-repo>` mid-skill — if the user later removes the worktree, they expect to remain wherever they invoked from until they pick option 2/3

### Pre-flight order

✅ Verify clean tree before any merge attempt
❌ Do not start the merge and discover dirty files mid-flow

### Merge style

✅ `git merge --no-ff` to preserve branch history
❌ Do not use `git merge --squash` or fast-forward — history would be lost

### Cleanup safety

✅ Remove worktree only after the user explicitly chose option 2 or 3, AND merge+push succeeded
❌ Do not auto-remove the worktree — the user may want to keep working there

### Branch deletion

✅ Use `git branch -d` (safe) only on user's explicit option-3 choice
❌ Never use `git branch -D` — it can delete unmerged commits

---

## Examples

### Example 1: Happy path — deliver and remove

**Scenario**: Developer just finished `feat/api-v2` in worktree `/repos/myapp-api`. Wants to land it and clean up.

**Execution**:

```bash
# CWD: /repos/myapp-api

# Step 1: Context — in a linked worktree on a non-main branch ✓
git rev-parse --git-dir            # /repos/myapp/.git/worktrees/myapp-api
git rev-parse --git-common-dir     # /repos/myapp/.git   (differs from --git-dir → linked worktree ✓)
git rev-parse --abbrev-ref HEAD    # feat/api-v2
git rev-parse --show-toplevel      # /repos/myapp-api

# Step 2: Main branch + main repo
git remote show origin | grep 'HEAD branch'   # HEAD branch: main
git worktree list --porcelain                 # first record → /repos/myapp

# Step 3: Pre-flight — clean ✓
git status --porcelain             # (empty)

# Step 4: Pull → merge → push, all via git -C; CWD stays /repos/myapp-api
git -C /repos/myapp checkout main
git -C /repos/myapp pull origin main
git -C /repos/myapp merge --no-ff feat/api-v2 -m "Merge branch 'feat/api-v2' into main"
git -C /repos/myapp push origin main
# merge commit: a1b2c3d

# Step 5: User chooses [3] Remove worktree and delete branch
git -C /repos/myapp worktree remove /repos/myapp-api
git -C /repos/myapp branch -d feat/api-v2
```

**Summary**:

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

### Example 2: Wrong context — invoked from main repo

**Scenario**: Developer is in `/repos/myapp` on `main` and runs `deliver-feature` by habit.

**Execution**:

```bash
# CWD: /repos/myapp

git rev-parse --git-dir          # /repos/myapp/.git
git rev-parse --git-common-dir   # /repos/myapp/.git   (equal → main repo, NOT a worktree)
```

**Skill halts**:

> "This skill must be run from inside a linked worktree, not from the main repo. Current location: `/repos/myapp`. To batch-merge multiple worktrees from the main repo, use `integrate-worktrees`."

No git operations performed. Exit code non-zero.

---

### Example 3: Conflict — halt without touching the worktree

**Scenario**: Developer ran `deliver-feature` from `/repos/myapp-api` on `feat/api-v2`. Pre-flight clean. The merge into main hits a conflict.

**Execution**:

```bash
# CWD: /repos/myapp-api  (stays here throughout)

git -C /repos/myapp pull origin main
git -C /repos/myapp merge --no-ff feat/api-v2 -m "Merge branch 'feat/api-v2' into main"
# CONFLICT (content): Merge conflict in src/api.ts
```

**Skill halts**:

> "Merge conflict merging `feat/api-v2` into `main` (in main repo `/repos/myapp`). Resolve conflicts there manually, complete the merge, then run `git -C /repos/myapp push origin main`. The worktree is untouched."

CWD is still `/repos/myapp-api`. Worktree is intact. No push. No cleanup. Summary reports `Merge: ✗(conflict)`.

---

## AI Refactor Instruction

If this skill produces incorrect behavior:

1. **CWD changed during execution**: if any step ran `cd <main-repo>` or used a non-`-C` git command on the main repo → rewind; switch to `git -C <main-repo>` for all main-repo operations
2. **Wrong invocation context proceeded**: if the skill ran while CWD was the main repo (i.e., `git rev-parse --git-dir` equals `git rev-parse --git-common-dir`) → rewind to Step 1, add the git-dir vs git-common-dir comparison guard
3. **Auto-stash performed**: if `git stash` appeared anywhere → remove; halt on dirty tree per Step 3
4. **Worktree removed before push succeeded**: if `git worktree remove` ran before `git push` returned 0 → halt; only run cleanup after Step 4 completes successfully and the user picks option 2 or 3
5. **Force-push attempted**: if `--force` or `--force-with-lease` appears in any push command → substitute standard push; if rejected, halt and report

---

## Self-Check

- [ ] **Worktree context verified**: `git rev-parse --git-dir` differs from `git rev-parse --git-common-dir` before proceeding
- [ ] **Non-main branch confirmed**: current branch ≠ detected main branch
- [ ] **Main branch determined**: auto-detected or explicitly provided by user; not assumed
- [ ] **Main repo path located**: parsed from `git worktree list --porcelain` first record
- [ ] **Pre-flight clean**: `git status --porcelain` empty before any merge
- [ ] **CWD never changed**: every main-repo command used `git -C <main-repo>`; user's shell stayed in `<feature-worktree>`
- [ ] **Pull before merge**: `git -C <main-repo> pull origin <main-branch>` ran before `git merge --no-ff`
- [ ] **No-ff merge used**: `git merge --no-ff` confirmed; no fast-forward or squash
- [ ] **Push succeeded before cleanup offered**: only after `git push` returned 0 was the cleanup prompt shown
- [ ] **Cleanup gated on user choice**: worktree removal happened only on options 2 or 3
- [ ] **Branch deletion used `-d`**: no `-D` flag; option 3 only
- [ ] **Summary report produced**: includes merge commit hash, push status, cleanup outcome, and follow-up cd hint when applicable
- [ ] **No force-push used**: `--force` or `--force-with-lease` never appeared in any command
