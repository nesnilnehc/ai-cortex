# integrate-branches

From the main repo on the main branch, scan all linked worktrees and local branches, let the user multi-select, then merge `--no-ff` + push them sequentially and clean up succeeded worktrees together.

**Status**: validated · **Version**: 2.0.0

---

## What It Does

Closes out a batch of feature branches in a single invocation:

1. Verifies the skill is invoked from the main repo root on the main branch — halts if inside a worktree, or on a non-main branch
2. Determines the main branch (auto-detects from `git remote show origin`; asks the user if ambiguous)
3. Scans both sources: linked worktrees via `git worktree list --porcelain` and standalone local branches via `git branch`; deduplicates; halts if no candidates found
4. Presents a unified list (with type indicator and last-activity hint; flags >14 days as STALE) and asks: integrate `all` or select specific ones by index?
5. Pre-flight checks all selected worktree entries for clean working tree — reports all dirty ones upfront before any merge begins; branch-only entries always pass pre-flight
6. For each selected clean branch sequentially: `git pull` → `git merge --no-ff` → `git push`; on failure asks whether to continue with remaining or abort
7. Removes all successfully-merged worktree entries together (branch-only entries skip this step)
8. Asks which local feature branches to delete (safe `-d` only)
9. Prints a per-branch summary: type / merge / push / cleanup / branch-deletion status

---

## When to Use

- You have 2 or more feature branches (in worktrees or standalone) ready to land onto main in one invocation
- After completing `commit-work` cycles in multiple worktrees or branches across a sprint
- Batch end-of-iteration cleanup: merge, push, and remove all completed feature branches from the main repo

**Prerequisites**: Run from the main repo root on the main branch. All changes in each worktree must be committed first — use `commit-work` per worktree before invoking this skill.

---

## When NOT to Use

- You only want to deliver a **single** worktree's branch and you're already in that worktree → use [`deliver-feature`](../deliver-feature/SKILL.md) (no need to `cd` back to main)

---

## Triggers

`integrate branches` · `integrate worktrees` · `integrate features` · `batch merge` · `batch merge branches` · `batch merge worktrees` · `merge worktrees` · `finish worktrees` · `close worktrees` · `deliver features` · `land branches`

---

## Inputs

| Input | Required | Description |
|---|---|---|
| Main repo + main branch | Yes | CWD must be the main repo root and current branch must equal the main branch |
| Active candidates | Yes | At least one linked worktree or local branch (excluding main) must exist |
| Branch selection | User input | `all` or comma-separated index numbers from the presented list (e.g., `1,3`) |
| Clean working tree | Per-worktree-entry | Dirty worktrees are reported upfront and skipped; branch-only entries always pass |
| Main branch name | Auto/Ask | Detected from `git remote show origin`; user is asked if ambiguous |

---

## Outputs

| Output | Description |
|---|---|
| Merge commits | One `--no-ff` merge commit on the main branch per succeeded branch |
| Remote push | `origin/<main-branch>` updated once per succeeded branch |
| Worktree removal | All succeeded `type: worktree` entries removed from `git worktree list` |
| Branch deletion | Optional — user selects which branches; `git branch -d` only |
| Batch summary report | Per-branch table: type / merge / push / cleanup / branch-deletion status |

---

## Safety Guarantees

- **Halts immediately if not in main repo on main branch** — prevents running from inside a worktree whose path may be deleted mid-execution, and prevents merging into the wrong branch
- **Pre-flight checks ALL selected worktree entries before starting any merge** — user sees the full picture of dirty worktrees before any irreversible action
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
