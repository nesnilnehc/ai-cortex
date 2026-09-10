---
name: deliver-feature
description: From inside a linked worktree, deliver the current feature branch into main — merge with --no-ff, push, and optionally clean up the worktree, all without leaving CWD.
description_zh: 在 linked worktree 内将当前 feature 分支交付到 main——以 --no-ff 合并、推送，并可选清理本 worktree，全程不离开当前目录。
tags: [git, workflow, automation]
version: 1.1.1
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

# Skill: Deliver Feature

## Purpose

Land the current feature branch onto main from inside a linked worktree, with no directory switching. The main repo is driven through `git -C <main-repo>`, so the user stays in the feature worktree the whole way, until they explicitly choose to leave. It cuts out the round trip of "cd to the main repo → invoke the batch tool → pick only the branch just finished → cd back".

---

## Core Objective

**Primary goal**: land the current worktree's feature branch onto main (through a `--no-ff` merge), push it to origin, and let the user decide whether to keep or remove that worktree — without ever leaving the worktree directory.

**Success criteria** (all of them must hold):

1. ✅ **Invocation context verified**: CWD is inside a linked worktree (not the main repo), and the current branch is not the main branch
2. ✅ **Pre-flight passed**: the current worktree has no uncommitted changes (`git status --porcelain` is empty)
3. ✅ **The merge runs in the main repo, not in the worktree**: `pull` / `merge --no-ff` / `push` all go through `git -C <main-repo>`; CWD stays in the worktree for the whole merge
4. ✅ **Push succeeded**: the cleanup options are offered only once `git push origin <main-branch>` returns 0
5. ✅ **The user controls cleanup**: the user explicitly picks keep or remove (with optional branch deletion, `-d` only); nothing is removed implicitly
6. ✅ **Single-branch summary**: report the merge commit hash, the push status, and the cleanup outcome

**Acceptance test**: once the skill finishes, `git -C <main-repo> log --oneline <main-branch>` shows exactly one new merge commit referencing that feature branch; `git -C <main-repo> ls-remote origin <main-branch>` agrees with local; and where the user chose removal, `git worktree list` no longer holds the source worktree.

---

## Scope Boundaries

**This skill owns**:

- Verifying the invocation context (inside a linked worktree, not on the main branch)
- Determining the main branch (auto-detected; the user is asked only when it cannot be determined)
- Pre-flighting the current worktree (is the working tree clean)
- Locating the main repo path via `git worktree list --porcelain`
- Running pull → `--no-ff` merge → push against the main repo via `git -C`
- Handing over to the user on a conflict or a rejected push (nothing is resolved automatically)
- Optionally removing the worktree and deleting the feature branch (on the user's confirmation, `-d` only)
- The single-branch summary report

**This skill does not own**:

- Batch operations across several worktrees (use `integrate-branches` from the main branch of the main repo)
- Committing uncommitted changes (use `commit-work` first)
- Rebasing or squashing before the merge
- Resolving merge conflicts (on a conflict it stops and prompts the user)
- Creating or managing pull requests
- Force-pushing to any branch

**Handoff points**:

- **→ `integrate-branches`**: the user is on the main branch of the main repo and wants to land several worktrees in one go
- **Stop and prompt the user**: invoked in the main repo (not a worktree), or from a worktree sitting on the main branch
- **On a merge conflict**: stop, and direct the user to resolve it by hand in the main repo; the worktree is left alone
- **On a rejected push**: stop, and direct the user to undo the merge in the main repo (`git -C <main-repo> reset --hard HEAD~1`, say), pull, and retry by hand

---

## Use Cases

- A developer has just finished a feature in `/repos/myapp-api` (a worktree on branch `feat/api-v2`) and wants to land it on main without leaving the current directory
- Delivering that single branch immediately after running `commit-work` inside the worktree
- An IDE or editor session is pinned to one worktree directory; the user wants to deliver the feature without interrupting that session

---

## Behavior

### Workflow (checklist)

**Step 1 — verify the invocation context**

```bash
git rev-parse --git-dir              # main repo: <root>/.git ; linked worktree: <main-root>/.git/worktrees/<name>
git rev-parse --git-common-dir       # same value in both contexts: <main-root>/.git
git rev-parse --abbrev-ref HEAD      # current branch
git rev-parse --show-toplevel        # current worktree root (the repo root CWD sits in)
```

Deciding the context: in a linked worktree, `git-dir != git-common-dir` (the per-worktree `.git/worktrees/<name>` differs from the shared `.git`). Equivalently, `<toplevel>/.git` is a plain file (a gitlink) in a linked worktree, and a directory in the main repo.

- If `git rev-parse --git-dir` equals `git rev-parse --git-common-dir` (that is, CWD is the main repo rather than a linked worktree) → **stop**:
  > "This skill must run inside a linked worktree, not in the main repo. Current location: `<cwd>`. To batch-merge several worktrees from the main repo, use `integrate-branches`."

- If the current branch equals the detected main branch (Step 2) → **stop**:
  > "The current branch is `<main-branch>`. This skill delivers a feature branch into main; it does not merge main into itself. Switch to the feature branch in this worktree, or use `integrate-branches` from the main repo."

Record `<feature-worktree>` (= `git rev-parse --show-toplevel`) and `<feature-branch>` (= the current branch).

**Step 2 — determine the main branch and locate the main repo**

```bash
git remote show origin | grep 'HEAD branch'
```

- The result is unambiguous (`HEAD branch: main`, say) → use it directly.
- The command fails or returns nothing → check for `origin/main` in `git branch -r`, then `origin/master`.
- Still undetermined → **ask the user**:
  > "The main branch could not be determined automatically. Enter the main branch name (main, master, develop, and so on):"

Record `<main-branch>`.

Locate the main repo from the worktree list:

```bash
git worktree list --porcelain
```

Parse the porcelain output. The first record is the main repo (its `worktree` line gives the path). Record `<main-repo>`. Sanity check: `<main-repo> != <feature-worktree>`.

**Step 3 — pre-flight: the current worktree must be clean**

```bash
git status --porcelain
```

If the output is non-empty → **stop**:
> "The current worktree `<feature-worktree>` has uncommitted changes. Commit them first (with `commit-work`, say) and invoke again. Nothing is stashed automatically."

**Step 4 — pull main, merge the feature branch, push (all through `git -C <main-repo>`)**

```bash
git -C <main-repo> checkout <main-branch>
git -C <main-repo> pull origin <main-branch>
git -C <main-repo> merge --no-ff <feature-branch> -m "Merge branch '<feature-branch>' into <main-branch>"
git -C <main-repo> push origin <main-branch>
```

**CWD stays at `<feature-worktree>` for every command** — the `git -C` flag drives the main repo operations without moving the user.

On a merge conflict → **stop**:
> "Merging `<feature-branch>` into `<main-branch>` hit a conflict (main repo `<main-repo>`). Resolve the conflict by hand in the main repo, finish the merge, then run `git -C <main-repo> push origin <main-branch>`. The worktree is untouched."

On a rejected push (not a fast-forward) → **stop**:
> "The push after merging `<feature-branch>` was rejected. In `<main-repo>`, run `git reset --hard HEAD~1` to undo the merge, then `git pull`, merge again, and push by hand."

Once the push succeeds, capture `<merge-commit-hash>` with `git -C <main-repo> rev-parse <main-branch>`.

**Step 5 — ask the user about cleanup**

One prompt, three options:

> "Delivery complete. What do you want done with worktree `<feature-worktree>` and branch `<feature-branch>`?
>
> [1] Keep the worktree (stay here, keep the branch)
> [2] Remove the worktree, keep the branch (cd back to the main repo)
> [3] Remove the worktree and delete the branch (`git branch -d`, the safe delete)
>
> Choose 1 / 2 / 3:"

For options 2 and 3, the skill prints a closing hint telling the user to cd to `<main-repo>` (the skill cannot change the user's shell CWD; it only runs git commands).

For options 2 and 3, run through `git -C`:

```bash
git -C <main-repo> worktree remove <feature-worktree>
```

For option 3 only, after the worktree has been removed:

```bash
git -C <main-repo> branch -d <feature-branch>
```

`-d` only — never `-D`. If `-d` fails (which should not happen after a successful `--no-ff` merge), report the error and stop the deletion (do not retry with `-D`).

**Step 6 — summary report**

```yaml
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
Next: cd /repos/myapp        (shown only when the worktree was removed)
```

---

## Input & Output

### Input requirements

| Input | Required | Notes |
|---|---|---|
| Worktree context | Yes | CWD must be inside a linked worktree; invoked in the main repo, it stops |
| Non-main branch | Yes | The current branch must not be `<main-branch>`; otherwise it stops |
| Clean working tree | Yes | `git status --porcelain` must be empty; nothing is stashed automatically |
| Cleanup choice | User input | One of three: keep / remove and keep the branch / remove and delete the branch |
| Main branch name | Auto/ask | Detected from the remote; the user is asked when it cannot be determined |
| Network access | Yes | pull and push to `origin` need the network |

### Output contract

Produced (as side effects):

| Element | Notes |
|---|---|
| Merge commit | Exactly one `--no-ff` merge commit on `<main-branch>` in the main repo |
| Remote push | `origin/<main-branch>` updated once |
| Worktree removal | Optional, the user's choice |
| Branch deletion | Optional, the user's choice; `git branch -d` only |
| Summary report | A single-branch table with the merge commit hash, the push status, the cleanup outcome, and where applicable the follow-up cd hint |

---

## Restrictions

### Hard Boundaries

- **Changing CWD is forbidden** — every main-repo operation goes through `git -C <main-repo>`; the user's shell stays in the worktree
- **Force-pushing is forbidden** (`--force`, `--force-with-lease`) to any branch
- **Auto-stashing uncommitted changes is forbidden** — stop and prompt the user
- **Using `git branch -D` is forbidden** — `-d` only
- **Removing the worktree before both the merge and the push have succeeded is forbidden**
- **Carrying on in the main repo, or in a worktree on the main branch, is forbidden** — stop and give the matching prompt

### Skill Boundaries

- **Batch-merging several worktrees**: use `integrate-branches` from the main branch of the main repo
- **Committing pending changes**: use `commit-work` before invoking this skill
- **rebase / squash**: use `git rebase` directly before invoking this skill
- **Creating a PR**: use the platform's own PR tooling; this skill merges into main directly
- **Code review**: use `review-diff` before committing; this skill performs no code review

---

## Anti-Patterns

### Invocation context

✅ Run inside a linked worktree, on a branch that is not main
❌ Do not run in the main repo — that is `integrate-branches`'s job; run from main and there is no current worktree to deliver

### CWD discipline

✅ Use `git -C <main-repo>` for every main-repo operation; CWD stays in the worktree
❌ Do not `cd <main-repo>` midway through the skill — if the user removes the worktree afterwards, they expect to be left where they invoked it, until they pick option 2/3

### Pre-flight order

✅ Verify the working tree is clean before any merge attempt
❌ Do not start the merge first and find dirty files halfway through

### Merge method

✅ `git merge --no-ff` keeps the branch history
❌ Do not use `git merge --squash` or a fast-forward — the history is lost

### Cleanup safety

✅ Remove the worktree only after the user explicitly picks option 2 or 3 and both the merge and the push have succeeded
❌ Do not remove the worktree automatically — the user may still want to work there

### Branch deletion

✅ Use `git branch -d` (the safe form) only when the user explicitly picks option 3
❌ Never use `git branch -D` — it can delete unmerged commits

---

## Examples

### Example 1: the normal path — deliver and clean up

**Scenario**: a developer has just finished `feat/api-v2` in worktree `/repos/myapp-api` and wants to land it and clean up.

**What runs**:

```bash
# CWD: /repos/myapp-api

# Step 1: context — inside a linked worktree, not the main branch ✓
git rev-parse --git-dir            # /repos/myapp/.git/worktrees/myapp-api
git rev-parse --git-common-dir     # /repos/myapp/.git   (differs from --git-dir → linked worktree ✓)
git rev-parse --abbrev-ref HEAD    # feat/api-v2
git rev-parse --show-toplevel      # /repos/myapp-api

# Step 2: main branch + main repo
git remote show origin | grep 'HEAD branch'   # HEAD branch: main
git worktree list --porcelain                 # first record → /repos/myapp

# Step 3: pre-flight — clean ✓
git status --porcelain             # (empty)

# Step 4: pull → merge → push, all through git -C; CWD stays at /repos/myapp-api
git -C /repos/myapp checkout main
git -C /repos/myapp pull origin main
git -C /repos/myapp merge --no-ff feat/api-v2 -m "Merge branch 'feat/api-v2' into main"
git -C /repos/myapp push origin main
# merge commit: a1b2c3d

# Step 5: the user picks [3] remove the worktree and delete the branch
git -C /repos/myapp worktree remove /repos/myapp-api
git -C /repos/myapp branch -d feat/api-v2
```

**Summary**:

```yaml
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

### Example 2: wrong context — invoked in the main repo

**Scenario**: a developer on branch `main` in `/repos/myapp` runs `deliver-feature` out of habit.

**What runs**:

```bash
# CWD: /repos/myapp

git rev-parse --git-dir          # /repos/myapp/.git
git rev-parse --git-common-dir   # /repos/myapp/.git   (equal → the main repo, not a worktree)
```

**The skill stops**:

> "This skill must run inside a linked worktree, not in the main repo. Current location: `/repos/myapp`. To batch-merge several worktrees from the main repo, use `integrate-branches`."

No git operation ran.

---

### Example 3: a conflict — stop, leave the worktree alone

**Scenario**: a developer runs `deliver-feature` from `feat/api-v2` in `/repos/myapp-api`. Pre-flight passes. Merging into main hits a conflict.

**What runs**:

```bash
# CWD: /repos/myapp-api (stays here throughout)

git -C /repos/myapp pull origin main
git -C /repos/myapp merge --no-ff feat/api-v2 -m "Merge branch 'feat/api-v2' into main"
# CONFLICT (content): Merge conflict in src/api.ts
```

**The skill stops**:

> "Merging `feat/api-v2` into `main` hit a conflict (main repo `/repos/myapp`). Resolve the conflict by hand in the main repo, finish the merge, then run `git -C /repos/myapp push origin main`. The worktree is untouched."

CWD is still `/repos/myapp-api`. The worktree is intact. No push. No cleanup.

---

## AI Refactor Instruction

If this skill behaves wrongly:

1. **CWD changed mid-run**: if a step ran `cd <main-repo>`, or used a git command against the main repo without `-C` → roll it back; switch every main-repo operation to `git -C <main-repo>`
2. **Kept running in the wrong context**: if the skill ran with CWD in the main repo (that is, `git rev-parse --git-dir` equals `git rev-parse --git-common-dir`) → go back to Step 1 and add the git-dir vs git-common-dir comparison check
3. **An auto-stash happened**: if `git stash` appears anywhere → remove it; stop on a dirty working tree, as Step 3 states
4. **The worktree was removed before the push succeeded**: if `git worktree remove` ran before `git push` returned 0 → stop; clean up only once Step 4 has completed and the user has picked option 2 or 3
5. **A force push was attempted**: if `--force` or `--force-with-lease` appears in any push command → replace it with a plain push; if that is rejected, stop and report

---

## Self-Check

- [ ] **Worktree context verified**: `git rev-parse --git-dir` differs from `git rev-parse --git-common-dir`
- [ ] **Non-main branch confirmed**: the current branch ≠ the detected main branch
- [ ] **Main branch determined**: auto-detected or supplied explicitly by the user, never assumed
- [ ] **Main repo path located**: parsed from the first record of `git worktree list --porcelain`
- [ ] **Pre-flight passed**: `git status --porcelain` was empty before any merge
- [ ] **CWD never changed**: every main-repo command used `git -C <main-repo>`; the user's shell stayed at `<feature-worktree>`
- [ ] **Pulled before merging**: `git -C <main-repo> pull origin <main-branch>` ran before `git merge --no-ff`
- [ ] **Merged with --no-ff**: `git merge --no-ff` confirmed, with no fast-forward and no squash
- [ ] **Cleanup offered only after the push succeeded**: the cleanup prompt appears only once `git push` returns 0
- [ ] **Cleanup is conditional on the user's choice**: the worktree is removed only under option 2 or 3
- [ ] **Branch deletion used `-d`**: no `-D` flag; option 3 only
- [ ] **Summary report emitted**: with the merge commit hash, the push status, the cleanup outcome, and where applicable the follow-up cd hint
- [ ] **No force push used**: neither `--force` nor `--force-with-lease` appears in any command
