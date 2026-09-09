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

# Skill: Integrate Branches

## Purpose

Wrap up feature branches in bulk from the main repository: scan every active linked worktree plus the local branches that have no worktree, let the user pick which ones land, check each working tree is clean, merge + push them one after another, then clean up every successfully merged worktree in one pass. It removes the `cd` into each directory followed by a manual delivery.

---

## Core Objective

**Primary goal**: on the main repository's main branch, merge the branches the user selected (from a worktree or standalone) into main, push to origin, and clean up the worktrees that succeeded — leaving the repository in a known clean state.

**Success criteria** (all must be satisfied):

1. ✅ **Invocation context verified**: CWD is the main repository root (not inside a linked worktree), and the current branch is the main branch
2. ✅ **All candidates discovered**: both `git worktree list --porcelain` and `git branch` are parsed; the non-main entries are presented to the user as one list with type markers
3. ✅ **Pre-flight finished before any merge**: every selected worktree entry was checked for a clean working tree; every dirty entry is reported together in one block
4. ✅ **Sequential merge + push**: each selected clean branch is merged with `--no-ff` and pushed in turn; the status of each is recorded (`succeeded` / `failed`)
5. ✅ **Cleanup in one pass**: every `succeeded` worktree entry is removed together; branch-only entries skip the worktree removal; failed entries get no cleanup at all
6. ✅ **Summary report emitted**: the merge / push / cleanup / branch-deletion status of every branch is covered

**Acceptance test**: after the skill finishes, `git log --oneline <main-branch>` holds one merge commit per successful branch; `git worktree list` holds only the main repository plus the failed or skipped worktree entries; `git ls-remote origin <main-branch>` matches the local state.

---

## Scope Boundaries

**This skill does**:

- Verify the invocation context (main repository root + main branch)
- Determine the main branch (auto-detected; the user is asked only when it cannot be determined)
- Scan linked worktrees (`git worktree list --porcelain`) and local branches with no worktree (`git branch`)
- Deduplicate: a branch already covered by a worktree entry is not shown twice
- Let the user multi-select the branches to merge (`all`, or a subset by index)
- Pre-flight the working tree: worktree entries through `git -C <path> status --porcelain`; branch-only entries skip the dirty check (they have no working tree of their own)
- Run pull → `--no-ff` merge → push in turn for each selected branch
- After each failure, ask the user: continue with the remaining entries, or abort
- Clean up every successfully merged worktree entry in one pass (`git worktree remove`)
- Optional feature-branch deletion (user-confirmed, `-d` only)
- A per-branch summary report

**This skill does not do**:

- Single-worktree delivery (use `deliver-feature` from inside the worktree)
- Commit uncommitted changes (use `commit-work` inside each worktree first)
- Rebase or squash before merging
- Resolve merge conflicts (on a conflict it stops and reports to the user)
- Create or manage pull requests
- Force-push to any branch
- Parallel merge execution (execution is always sequential)

**Handoff points**:

- **→ `deliver-feature`**: the user is inside a single worktree and wants to deliver only that branch, without a `cd` back to the main repository
- **Stop and prompt the user**: invoked inside a linked worktree, or invoked on a non-main branch of the main repository
- **A branch hits a merge conflict**: stop that one, and ask whether to continue with the rest
- **A branch's push is rejected**: stop that one, and ask whether to continue with the rest

---

## Use Cases

- A developer has 2–4 feature branches (some in worktrees, some standalone) ready to land on main in one go
- End-of-sprint wrap-up in bulk: merge, push, and clean up every finished feature branch from the main repository
- A CI or automation run produced several parallel worktrees plus a handful of topic branches, and the results are now being consolidated

---

## Behavior

### Workflow (Checklist)

**Step 1 — verify the invocation context**

```bash
git rev-parse --git-dir              # main repo: <root>/.git ; linked worktree: <main-root>/.git/worktrees/<name>
git rev-parse --git-common-dir       # same value in both contexts: <main-root>/.git
git rev-parse --abbrev-ref HEAD      # current branch
git rev-parse --show-toplevel        # current repository root
```

For a linked worktree `git-dir != git-common-dir`; in the main repository the two are equal.

- If `git rev-parse --git-dir` differs from `git rev-parse --git-common-dir` (that is, CWD is inside a linked worktree) → **stop**:
  > "This skill must run from the main repository root, not from inside a worktree. Current location: `<cwd>`. To deliver the current worktree's branch, use `deliver-feature`."

- If the current branch is not the detected main branch (step 2) → **stop**:
  > "The current branch is `<current-branch>`, not `<main-branch>`. Switch to the main branch first: `git checkout <main-branch>`."

Record `<main-repo>` (= `git rev-parse --show-toplevel`). CWD stays there for every step that follows.

**Step 2 — determine the main branch**

```bash
git remote show origin | grep 'HEAD branch'
```

- The result is unambiguous (such as `HEAD branch: main`) → use it directly.
- The command fails or returns nothing → look for `origin/main` in `git branch -r`, then `origin/master`.
- Still undetermined → **ask the user**:
  > "The main branch could not be determined automatically. Enter the main branch name (main, master, develop, and so on):"

Record `<main-branch>`.

**Step 3 — scan and present the selectable branches**

```bash
# Source 1: linked worktrees
git worktree list --porcelain

# Source 2: all local branches
git branch --format='%(refname:short)'
```

Parse the porcelain output. The first worktree record is the main repository itself — skip it. Record each of the others as a `type: worktree` candidate.

Exclude from the `git branch` output:
- `<main-branch>` itself
- Branches already covered by a worktree entry (deduplicated by branch name)

Record the remaining branches as `type: branch` candidates (with no associated worktree path).

Build one list of `{path, branch, type}` tuples. Skip detached entries and mark them unavailable.

- No candidates → **stop**:
  > "No active linked worktree or local branch was found; there is nothing to integrate."

Present the list with an index, a type marker, the path where applicable, the branch name, and a hint about recent activity:

```text
Available branches to integrate:
  [1]  worktree  /repos/myapp-auth      feat/user-auth      (last commit: 2 days ago)
  [2]  worktree  /repos/myapp-api       feat/api-v2         (last commit: 5 days ago)
  [3]  branch    —                      feat/dashboard      (last commit: 14 days ago — STALE)
```

Ask:

> "Select the branches to integrate. Enter the indexes (comma-separated) or `all`:"

Record `<selected-list>`.

**Step 4 — pre-flight: check every selected entry**

For each entry `E` in `<selected-list>`:

- If `E.type == worktree`:
  ```bash
  git -C <E.path> status --porcelain
  ```
- If `E.type == branch`: it has no working tree of its own — skip the dirty check and treat it as clean.

Collect the results into `<clean-list>` and `<dirty-list>` respectively.

If `<dirty-list>` is not empty, report every dirty entry together before any merge starts:

```text
Pre-flight check — dirty worktrees (will be skipped):
  /repos/myapp-api  (feat/api-v2)    — 3 uncommitted file(s)
```

Ask:

> "The worktrees above hold uncommitted changes. Continue merging the remaining clean entries, or stop everything? [continue / halt]"

- `halt` → stop; run no merges.
- `continue` → carry on with `<clean-list>` only. If `<clean-list>` is empty → stop and report "nothing to act on".

Nothing is stashed automatically under any circumstances.

**Step 5 — bulk merge + push (sequential)**

For each entry `E` in `<clean-list>`:

```bash
# stay current across a multi-branch run
git pull origin <main-branch>

# --no-ff merge
git merge --no-ff <E.branch> -m "Merge branch '<E.branch>' into <main-branch>"

# push
git push origin <main-branch>
```

CWD stays at `<main-repo>` throughout.

When entry `E` fails:

- Merge conflict:
  > "Merging `<E.branch>` into `<main-branch>` hit a conflict. Resolve the conflict in `<main-repo>`, finish the merge by hand, then push and remove the worktree where applicable."
- Push rejected (not a fast-forward):
  > "The push after merging `<E.branch>` was rejected. Run `git reset --hard HEAD~1` in `<main-repo>` to undo the merge, then pull, merge again, and push."

In both cases mark `E` as `failed` and ask:

> "Continue with the remaining branches, or abort everything left? [continue / abort]"

- `abort` → stop; process none of the remaining entries.
- `continue` → mark `E` as `failed` and move on to the next one.

Record the result of each one: `succeeded` or `failed`.

**Step 6 — cleanup in one pass (worktree entries only)**

Once all merges are done, confirm CWD is still `<main-repo>`:

```bash
pwd   # must equal <main-repo>
```

Only for the entries in `<succeeded-list>` where `E.type == worktree`:

```bash
git worktree remove <E.path>
```

Run these in order. If one removal fails (the path no longer exists, say), record the error and move on to the next.

`type: branch` entries have no worktree path — this step skips them entirely. The worktree of a failed entry is never removed.

**Step 7 — offer the local branch deletion option**

For every entry in `<succeeded-list>`, present the branch list together:

> "The successful entries are cleaned up. Delete the local feature branches below? Enter the indexes, `all`, or `none`:"
> ```
> [1]  feat/user-auth  (was worktree)
> [2]  feat/dashboard  (was branch)
> ```

Once each one is confirmed, run:

```bash
git branch -d <E.branch>
```

Use `-d` only — never `-D`. If `-d` fails, report the error and stop deleting that branch.

**Step 8 — summary report**

```text
integrate-branches summary
──────────────────────────────────────────────────────────────────────────
Type      Branch            Merge          Push   Cleanup  Branch-Del
worktree  feat/user-auth    ✓              ✓      ✓        deleted
worktree  feat/api-v2       ✗(conflict)    —      —        —
branch    feat/dashboard    ✓              ✓      —        deleted
──────────────────────────────────────────────────────────────────────────
Main repo: /repos/myapp · Main branch: main · Remote: origin
```

Status codes: `✓` succeeded · `✗(reason)` failed · `skipped(dirty)` pre-flight failed · `—` not applicable

The `Cleanup` column of a `type: branch` entry is always `—` (there is no worktree to remove).

---

## Input & Output

### Input Requirements

| Input | Required | Note |
|---|---|---|
| Main repo + main branch context | Yes | CWD must be the main repository root, and the current branch must equal the main branch |
| Active candidates | Yes | At least one linked worktree or local branch exists, other than main |
| Branch selection | User input | `all`, or comma-separated indexes from the presented list |
| Clean working tree | Per worktree entry | A dirty worktree is reported up front and skipped; branch-only entries always pass pre-flight |
| Main branch name | Auto / ask | Detected from the remote; the user is asked when it cannot be determined |
| Network access | Yes | pull and push to `origin` need the network |

### Output Contract

| Element | Note |
|---|---|
| Merge commits | Each successful branch produces one `--no-ff` merge commit on `<main-branch>` |
| Remote push | One push per successful branch, updating `origin/<main-branch>` |
| Worktree removal | Every successful `type: worktree` entry is removed from `git worktree list` |
| Branch deletion | Optional, run after user confirmation; `git branch -d` only |
| Batch summary report | A per-branch table: type / branch / merge / push / cleanup / branch-deletion status |

---

## Restrictions

### Hard Boundaries

- **Never force-push** (`--force`, `--force-with-lease`) to any branch
- **Never remove a worktree after its merge or push failed**
- **Never stash automatically** — uncommitted changes are reported up front and that worktree is skipped
- **Never use `git branch -D`** — `-d` only (the safe delete)
- **Never start a merge before pre-flight has finished for every selected entry**
- **Never continue from inside a linked worktree, or on a non-main branch of the main repository** — stop and give the matching prompt

### Skill Boundaries

- **Single-worktree delivery**: use `deliver-feature` from inside the worktree
- **Commit pending changes**: use `commit-work` inside each worktree first
- **rebase / squash**: use `git rebase` directly, before invoking this skill
- **Create a PR**: use the platform's own PR tooling; this skill merges straight into main
- **Code review**: use `review-diff` before committing; this skill does no code review

---

## Anti-Patterns

### Invocation Context

✅ Run from the main repository root, on the main branch
❌ Do not run from inside a linked worktree — that is `deliver-feature`'s job; once the worktree is deleted the CWD goes stale and every command after it fails

### Pre-Flight Order

✅ Run the dirty check across every selected worktree entry before any merge starts
❌ Do not check an entry only just before its own merge — a dirty worktree then surfaces after some merges are already committed

### Merge Method

✅ `git merge --no-ff` keeps the branch history
❌ Do not use `git merge --squash` or a fast-forward — the history is lost

### Push Safety

✅ Standard `git push origin <main-branch>`
❌ Never use `--force` or `--force-with-lease` on main

### Cleanup Order

✅ Remove a worktree only after both the merge and the push succeeded
❌ Do not remove between the merge and the push — if the push fails the branch becomes unreachable

### Branch Deletion

✅ `git branch -d` (safe), with user confirmation
❌ Never use `git branch -D` (force) — it can delete unmerged commits

---

## Examples

### Example 1: worktree branches and standalone branches mixed (happy path)

**Scenario**: two worktree branches and one standalone branch are ready to merge into `main`.

**Execution**:

```bash
# Step 3: scan
git worktree list --porcelain
# main: /repos/myapp  +  /repos/myapp-auth feat/user-auth  +  /repos/myapp-api feat/api-v2

git branch --format='%(refname:short)'
# feat/user-auth (already in a worktree — deduplicated)
# feat/api-v2   (already in a worktree — deduplicated)
# feat/dashboard (standalone branch)

# Presented list:
#   [1]  worktree  /repos/myapp-auth  feat/user-auth  (last commit: 2 days ago)
#   [2]  worktree  /repos/myapp-api   feat/api-v2     (last commit: 5 days ago)
#   [3]  branch    —                  feat/dashboard  (last commit: 14 days ago — STALE)
# User selects: all

# Step 4: pre-flight
git -C /repos/myapp-auth status --porcelain   # (empty ✓)
git -C /repos/myapp-api  status --porcelain   # (empty ✓)
# feat/dashboard — no worktree, skipped ✓

# Step 5: sequential merge + push (3 of them)
git pull origin main
git merge --no-ff feat/user-auth -m "Merge branch 'feat/user-auth' into main"
git push origin main

git pull origin main
git merge --no-ff feat/api-v2 -m "Merge branch 'feat/api-v2' into main"
git push origin main

git pull origin main
git merge --no-ff feat/dashboard -m "Merge branch 'feat/dashboard' into main"
git push origin main

# Step 6: cleanup — worktree entries only
pwd                                       # /repos/myapp ✓
git worktree remove /repos/myapp-auth
git worktree remove /repos/myapp-api
# feat/dashboard — type: branch, skipped

# Step 7: delete branches — the user picks all
git branch -d feat/user-auth
git branch -d feat/api-v2
git branch -d feat/dashboard
```

**Summary**:

```text
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

### Example 2: the dirty worktree is skipped, the standalone branch proceeds

**Scenario**: three entries are selected, and one of the worktrees holds uncommitted changes.

**Execution**:

```bash
# Step 4: pre-flight
git -C /repos/myapp-auth  status --porcelain   # (empty ✓)
git -C /repos/myapp-api   status --porcelain   # M  src/api.ts  ← dirty
# feat/dashboard — no worktree, skipped ✓
```

**The skill reports**:

```text
Pre-flight check — dirty worktrees (will be skipped):
  /repos/myapp-api  (feat/api-v2)    — 1 uncommitted file(s)
```

The user answers `continue` → `feat/user-auth` and `feat/dashboard` carry on; `feat/api-v2` is skipped.

**Summary**:

```text
integrate-branches summary
──────────────────────────────────────────────────────────────────────────
Type      Branch            Merge          Push  Cleanup  Branch-Del
worktree  feat/user-auth    ✓              ✓     ✓        deleted
worktree  feat/api-v2       skipped(dirty) —     —        —
branch    feat/dashboard    ✓              ✓     —        deleted
──────────────────────────────────────────────────────────────────────────
```

---

### Example 3: wrong context — invoked from inside a worktree

**Scenario**: the developer is on branch `feat/api-v2` in `/repos/myapp-api`.

**Execution**:

```bash
git rev-parse --git-dir          # /repos/myapp/.git/worktrees/myapp-api
git rev-parse --git-common-dir   # /repos/myapp/.git   (differs → linked worktree)
```

**The skill stops**:

> "This skill must run from the main repository root, not from inside a worktree. Current location: `/repos/myapp-api`. To deliver the current worktree's branch, use `deliver-feature`."

---

## AI Refactor Instruction

If this skill behaves wrongly:

1. **It carried on in the wrong context**: go back to step 1 and add the git-dir vs git-common-dir comparison and the branch-equality check
2. **Pre-flight was skipped or deferred**: go back to step 4 and make sure pre-flight completes for every selected entry before any merge
3. **A failed worktree was deleted**: stop; only `type: worktree` entries in `<succeeded-list>` may be removed
4. **worktree remove ran on a branch-only entry**: a branch-only entry has no worktree path — step 6 skips it entirely
5. **A force-push was attempted**: replace it with a standard push; if that fails, stop and report
6. **pull was skipped before a merge**: rerun from the pull step
7. **A worktree branch showed up twice**: the deduplication in step 3 must exclude branches already in the worktree list from the `git branch` output

---

## Self-Check

- [ ] **Invocation context verified**: `git rev-parse --git-dir` equals `git rev-parse --git-common-dir`, and the current branch equals `<main-branch>`
- [ ] **Main branch confirmed**: auto-detected or explicitly given by the user, never assumed
- [ ] **Both sources scanned**: `git worktree list --porcelain` and `git branch` are both parsed, and the non-main entries are presented
- [ ] **Deduplication done**: a branch held in a worktree does not show up again in the branch list
- [ ] **User selection recorded**: `all` or the index subset was captured before any pre-flight
- [ ] **Pre-flight for every worktree entry finished before any merge**: `git -C <path> status --porcelain` ran for each selected worktree entry
- [ ] **Branch-only entries skipped the dirty check**: they have no working tree to check
- [ ] **Dirty worktrees reported together**: every dirty entry was listed before the continue/halt prompt
- [ ] **pull ran before every merge**: `git pull origin <main-branch>` ran immediately before each `git merge --no-ff`
- [ ] **Merged with --no-ff**: `git merge --no-ff` confirmed, with no fast-forward and no squash
- [ ] **`succeeded` marked only after the push succeeded**: an entry joins `<succeeded-list>` only after `git push` returns 0
- [ ] **Cleanup in one pass touched only successful worktree entries**: `git worktree remove` was never called on a failed, skipped, or `type: branch` entry
- [ ] **CWD confirmed before cleanup**: `pwd` equals `<main-repo>` before any `git worktree remove`
- [ ] **Branch deletion used `-d`**: no `-D` flag in any branch-deletion command; the user confirmed each branch
- [ ] **Summary report emitted**: the status code of every branch is filled in correctly
- [ ] **No force-push used**: `--force` and `--force-with-lease` show up in no command
