# merge-worktree

From the main repo, scan all active worktrees, select and batch-merge branches into main, push, and clean up together.

**Status**: validated · **Version**: 1.0.0 · **Quality**: 19/20

---

## What It Does

Automates the batch worktree lifecycle in a single skill invocation:

1. Verifies the skill is invoked from the main repo root — halts if inside a linked worktree
2. Determines the main branch (auto-detects from `git remote show origin`; asks the user if ambiguous)
3. Scans all active linked worktrees via `git worktree list`; halts if none found
4. Presents the list and asks: merge `all` or select specific ones by index?
5. Pre-flight checks all selected worktrees for clean working tree — reports all dirty ones upfront before any merge begins
6. For each selected clean worktree sequentially: `git pull` → `git merge --no-ff` → `git push`; on failure asks whether to continue with remaining or abort
7. Removes all successfully-merged worktrees together (unified cleanup)
8. Asks which local feature branches to delete (safe `-d` only)
9. Prints a per-worktree summary: merge / push / cleanup / branch-deletion status

---

## When to Use

- You have 2 or more feature worktrees ready to land onto main and want to handle them in one invocation
- After completing `commit-work` cycles in multiple worktrees across a sprint
- Batch end-of-iteration cleanup: merge, push, and remove all completed feature worktrees from the main repo

**Prerequisites**: Must be run from the main repo root. All changes in each worktree must be committed first — use `commit-work` per worktree before invoking this skill.

---

## Triggers

`merge worktrees` · `merge all worktrees` · `finish worktrees` · `close worktrees` · `batch merge worktrees`

---

## Inputs

| Input | Required | Description |
|---|---|---|
| Main repo context | Yes | CWD must be the main repo root; halts if inside a linked worktree |
| Active linked worktrees | Yes | At least one non-main linked worktree must exist; halts if none found |
| Worktree selection | User input | `all` or comma-separated index numbers from the presented list (e.g., `1,3`) |
| Clean working tree | Per-worktree | Dirty worktrees are reported upfront and skipped; no auto-stash |
| Main branch name | Auto/Ask | Detected from `git remote show origin`; user is asked if ambiguous |

---

## Outputs

| Output | Description |
|---|---|
| Merge commits | One `--no-ff` merge commit on main per succeeded worktree |
| Remote push | `origin/<main-branch>` updated once per succeeded worktree |
| Worktree removal | All succeeded worktrees removed from `git worktree list` |
| Branch deletion | Optional — user selects which branches; `git branch -d` only |
| Batch summary report | Per-worktree table: branch, merge status, push status, cleanup status, branch deletion |

---

## Safety Guarantees

- **Halts immediately if not in main repo** — prevents running from inside a worktree whose path may be deleted mid-execution
- **Pre-flight checks ALL selected worktrees before starting any merge** — user sees the full picture of dirty worktrees before any irreversible action
- **Never force-pushes** to any branch
- **Never removes a worktree** before its merge and push both succeed
- **Never auto-stashes** — halts on dirty working tree instead
- **Halts on merge conflict** with resolution instructions
- **Halts on push rejection** with recovery instructions
- **Uses `-d` only** (safe delete) for branch deletion — never `-D`

---

## Related Skills

| Skill | Relationship |
|---|---|
| `commit-work` | Predecessor — use to commit pending changes in each worktree before invoking this skill |
| `review-diff` | Optional pre-merge — use to review changes before committing |

