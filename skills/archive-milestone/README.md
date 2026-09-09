# archive-milestone

Archives a completed milestone out of the active path into a snapshot summary and folds up the roadmap's historical stage, so that stale documents do not distort the AI's read of the current project state.

## When to invoke

- The hygiene sweep of `plan-next` (step 2.3) finds a completed milestone that was never archived
- The milestone completed ≥ 60 days ago
- The index of the milestone in progress is ≥ target + 2 (with M5 in progress, m3 qualifies and m4 does not)
- tasks.md is over 300 lines and every task is done

## Default behavior: dry-run

**Without the `apply` argument, the default is dry-run** — it prints a preview and changes no file. That is the safe default.

## Examples

### Dry-run (preview, recommended first)

```text
/archive-milestone m3
```

Or state it explicitly:

```text
/archive-milestone m3 apply=false
```

Example output:

```text
=== dry-run preview ===

Will create:
  docs/process-management/milestones/_archive/m3-summary.md

  Completed on: 2026-02-15
  Key deliverables:
    - T31 QueryRouter hybrid retrieval shipped (commit abc123)
    - T32 BGE-M3 embedding wired in (ADR-006 compliant)
    ...

Will modify:
  roadmap.md lines 45-89 folded into:
    ### M3 hybrid retrieval infrastructure (completed 2026-02-15) → see [milestones/_archive/m3-summary.md]

Will delete:
  docs/process-management/milestones/m3/ (3 files, 312 lines total)

Reference updates (2):
  docs/architecture/system-architecture.md:78 → updated
  docs/calibration/planning-alignment.md:34  → updated

=== no file was modified ===
```

### Apply (execute for real)

**Once the dry-run preview checks out**, pass `apply=true`:

```text
/archive-milestone m3 apply=true
```

Precondition: the git working tree has no uncommitted changes (the skill checks this itself).

## Output files

| File | Description |
|---|---|
| `milestones/_archive/{slug}-summary.md` | Snapshot summary (lifecycle: snapshot) |

## Summary structure

```markdown
---
artifact_type: milestone-summary
created_by: archive-milestone
lifecycle: snapshot
created_at: YYYY-MM-DD
milestone_slug: {slug}
completed_at: YYYY-MM-DD
---

# {milestone name} archive summary

## Key deliverables
...

## Remaining gaps
...

## Key ADRs
...
```

## What it will not do

- Never runs by itself (it must be invoked explicitly)
- Changes no file during a dry-run
- Does not archive a milestone that fails the maturity conditions
