# deliver-feature

From inside a linked worktree, deliver the current feature branch into main — merge with `--no-ff`, push, and optionally clean up the worktree, all without leaving CWD.

**Status**: validated · **Version**: 1.0.0

---

## What It Does

Lands a single feature branch into main from inside its worktree, in one invocation:

1. Verifies CWD is inside a linked worktree (not the main repo) and the current branch is not main
2. Determines the main branch (auto-detect from `git remote show origin`; ask if ambiguous)
3. Locates the main repo path from `git worktree list --porcelain`
4. Pre-flight checks the current worktree's working tree is clean — halts on dirty (no auto-stash)
5. Pull → `git merge --no-ff <feature>` → `git push`, all run via `git -C <main-repo>` so CWD stays in the worktree
6. Asks the user what to do next: keep worktree / remove worktree / remove worktree and delete branch (`-d` only)
7. Prints a single-branch summary with the merge commit hash, push status, cleanup outcome, and a `cd` hint when the worktree was removed

---

## When to Use

- You just finished a feature in a worktree and want to ship it without `cd`-ing back to the main repo
- After running `commit-work` in a worktree, immediately delivering that single branch
- Your editor / terminal session is anchored in the worktree directory and you want to keep it there until cleanup

**Prerequisites**: Run from inside a linked worktree on a non-main branch with a clean working tree. Use `commit-work` first if there are pending changes.

---

## When NOT to Use

- You want to land **multiple** worktrees in one go → use [`integrate-branches`](../integrate-branches/SKILL.md) from the main repo
- You're already on the main repo and main branch → use [`integrate-branches`](../integrate-branches/SKILL.md)

---

## Triggers

`deliver feature` · `finish feature` · `land feature` · `merge feature` · `ship feature` · `deliver this`

---

## Inputs

| Input | Required | Description |
|---|---|---|
| Worktree context | Yes | CWD must be inside a linked worktree; halts if invoked from main repo |
| Non-main branch | Yes | Current branch must not be the main branch; halts otherwise |
| Clean working tree | Yes | `git status --porcelain` empty; no auto-stash |
| Cleanup choice | User input | One of keep / remove / remove-and-delete-branch |
| Main branch name | Auto/Ask | Detected from `git remote show origin`; user is asked if ambiguous |

---

## Outputs

| Output | Description |
|---|---|
| Merge commit | Exactly one `--no-ff` merge commit on `<main-branch>` in the main repo |
| Remote push | `origin/<main-branch>` updated once |
| Worktree removal | Optional (user-chosen) |
| Branch deletion | Optional (user-chosen); `git branch -d` only |
| Summary report | Single-branch table: feature branch / worktree / main repo / merge commit hash / push status / cleanup outcome / cd hint |

---

## Safety Guarantees

- **Never changes CWD** — all main-repo operations go through `git -C <main-repo>`
- **Never force-pushes** to any branch
- **Never auto-stashes** — halts on dirty tree instead
- **Never removes the worktree** before merge AND push both succeed
- **Halts on merge conflict** with explicit recovery instructions; worktree stays intact
- **Halts on push rejection** with explicit recovery instructions
- **Uses `-d` only** for branch deletion — never `-D`
- **Halts immediately** if invoked from the main repo or from a worktree on the main branch, with a pointer to `integrate-branches`

---

## Related Skills

| Skill | Relationship |
|---|---|
| [`integrate-branches`](../integrate-branches/SKILL.md) | Sibling — use from the main repo on the main branch when batching multiple worktrees |
| [`commit-work`](../commit-work/SKILL.md) | Predecessor — use to commit pending changes in the worktree before invoking this skill |
| [`review-diff`](../review-diff/SKILL.md) | Optional pre-merge — review changes before committing |
