# Delivery Examples

## Example 1: the normal path — deliver and clean up

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

## Example 2: wrong context — invoked in the main repo

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

## Example 3: a conflict — stop, leave the worktree alone

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
