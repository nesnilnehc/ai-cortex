# merge-worktree

Merge the current git worktree branch into the main branch, push to origin, and remove the worktree.

**Status**: experimental · **Version**: 0.1.0 · **Quality**: 16/20

---

## What It Does

Automates the end-of-worktree lifecycle in a single skill invocation:

1. Detects the current worktree path and feature branch
2. Determines the main branch (auto-detects from `git remote show origin`; asks the user if ambiguous)
3. Verifies the working tree is clean — halts if dirty
4. Pulls and merges the feature branch into main with `--no-ff`
5. Pushes main to `origin`
6. Removes the worktree directory (only after push succeeds)
7. Optionally deletes the local feature branch (user-confirmed, safe `-d` only)

---

## When to Use

- You finished work in a git worktree and want to land it on main and clean up
- After completing a `commit-work` cycle inside a worktree
- Automating the merge→push→cleanup sequence without manual context switching

**Prerequisites**: All changes must be committed before invoking this skill. Use `commit-work` first if the working tree is dirty.

---

## Triggers

`merge worktree` · `finish worktree` · `close worktree`

---

## Inputs

| Input | Required | Description |
|---|---|---|
| Active git worktree | Yes | A worktree directory with a named branch |
| Clean working tree | Yes | `git status --porcelain` must return empty |
| Main branch name | Auto/Ask | Detected from `git remote show origin`; user is asked if ambiguous |

---

## Outputs

| Output | Description |
|---|---|
| Merge commit | `--no-ff` merge commit on main branch |
| Remote push | `origin/<main-branch>` updated |
| Worktree removal | Worktree directory removed from `git worktree list` |
| Branch deletion | Optional — user confirms before `git branch -d` |
| Summary report | Branch names, commit hash, push status, worktree path |

---

## Safety Guarantees

- **Never force-pushes** to any branch
- **Never deletes the worktree** before both merge and push succeed
- **Never auto-stashes** — halts on dirty working tree instead
- **Halts on merge conflict** with resolution instructions
- **Halts on push rejection** with recovery instructions
- **Uses `-d` only** (safe delete) for branch deletion — never `-D`

---

## Related Skills

| Skill | Relationship |
|---|---|
| `commit-work` | Predecessor — use to commit pending changes before invoking this skill |
| `review-diff` | Optional pre-merge — use to review changes before committing |

---

## ASQM Scores

| Dimension | Score | Notes |
|---|---|---|
| agent_native | 4/5 | Structured YAML schema, triggers, Self-Check, Output Contract table; no formal Appendix |
| cognitive | 4/5 | 8-step checklist with exact commands, 3 decision trees, 3 examples with edge cases |
| composability | 4/5 | Explicit handoffs to commit-work; linear workflow chain |
| stance | 4/5 | All 11 spec sections, strong safety invariants, ✅/❌ Anti-Patterns |
| **total** | **16/20** | Experimental (Gate A ✓, Gate B ✓, quality < 17) |
