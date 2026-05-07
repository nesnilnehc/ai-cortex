# integrate-worktrees

From the main repo on the main branch, scan all linked worktrees, let the user multi-select, then merge `--no-ff` + push them sequentially and clean up the succeeded ones together.

**Status**: validated · **Version**: 1.0.0

---

## What It Does

Closes out a batch of feature worktrees in a single invocation:

1. Verifies the skill is invoked from the main repo root on the main branch — halts if inside a worktree, or on a non-main branch
2. Determines the main branch (auto-detects from `git remote show origin`; asks the user if ambiguous)
3. Scans all active linked worktrees via `git worktree list --porcelain`; halts if none found
4. Presents the list (with last-activity hint; flags >14 days as STALE) and asks: integrate `all` or select specific ones by index?
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

**Prerequisites**: Run from the main repo root on the main branch. All changes in each worktree must be committed first — use `commit-work` per worktree before invoking this skill.

---

## When NOT to Use

- You only want to deliver a **single** worktree's branch and you're already in that worktree → use [`deliver-feature`](../deliver-feature/SKILL.md) (no need to `cd` back to main)

---

## Triggers

`integrate worktrees` · `integrate features` · `batch merge worktrees` · `merge worktrees` · `finish worktrees` · `close worktrees` · `deliver features`

---

## Inputs

| Input | Required | Description |
|---|---|---|
| Main repo + main branch | Yes | CWD must be the main repo root and current branch must equal the main branch |
| Active linked worktrees | Yes | At least one non-main linked worktree must exist; halts if none found |
| Worktree selection | User input | `all` or comma-separated index numbers from the presented list (e.g., `1,3`) |
| Clean working tree | Per-worktree | Dirty worktrees are reported upfront and skipped; no auto-stash |
| Main branch name | Auto/Ask | Detected from `git remote show origin`; user is asked if ambiguous |

---

## Outputs

| Output | Description |
|---|---|
| Merge commits | One `--no-ff` merge commit on the main branch per succeeded worktree |
| Remote push | `origin/<main-branch>` updated once per succeeded worktree |
| Worktree removal | All succeeded worktrees removed from `git worktree list` |
| Branch deletion | Optional — user selects which branches; `git branch -d` only |
| Batch summary report | Per-worktree table: branch / merge / push / cleanup / branch-deletion status |

---

## Safety Guarantees

- **Halts immediately if not in main repo on main branch** — prevents running from inside a worktree whose path may be deleted mid-execution, and prevents merging into the wrong branch
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
| [`deliver-feature`](../deliver-feature/SKILL.md) | Sibling — use from inside a single worktree to deliver only that branch without `cd`-ing back to main |
| [`commit-work`](../commit-work/SKILL.md) | Predecessor — use to commit pending changes in each worktree before invoking this skill |
| [`review-diff`](../review-diff/SKILL.md) | Optional pre-merge — review changes before committing |
