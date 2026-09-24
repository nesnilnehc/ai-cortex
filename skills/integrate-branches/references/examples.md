# integrate-branches: examples

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
