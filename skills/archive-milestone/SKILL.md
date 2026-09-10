---
name: archive-milestone
description: Archive a completed milestone by generating a snapshot summary, folding the roadmap stage, and removing the stale tasks directory.
description_zh: 将已完成里程碑转为快照摘要，折叠路线图历史阶段，移除历史任务目录，减少 AI 上下文污染。
tags: [governance, lifecycle, archive, milestone]
version: 1.1.1
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
  triggers_after: [plan-next]
triggers: [archive milestone, completed milestone cleanup, milestone summary]
input_schema:
  type: structured
  fields:
    milestone_slug:
      type: string
      required: true
      description: Milestone directory name (e.g. "m3")
    apply:
      type: bool
      required: false
      default: false
      description: false = dry-run (preview only), true = write changes to disk
  defaults:
    apply: false
output_schema:
  type: document-artifact
  description: Milestone snapshot summary + roadmap fold preview + reference update list
  artifact_type: milestone-summary
  path_pattern: docs/process-management/milestones/_archive/{slug}-summary.md
  lifecycle: snapshot
---

# Skill: Archive Milestone

## Purpose

Move the historical execution detail of a completed milestone out of the active paths and produce a lean snapshot summary, so old documents stop clouding the AI's read of the project's current state.

---

## Core Objective

**Primary goal**: produce a snapshot summary for a completed milestone, fold the historical roadmap section, and move the original tasks directory into `_archive/`.

**Success criteria** (with apply=true, all of them must hold):

1. ✅ The snapshot summary was produced at `milestones/_archive/{slug}-summary.md`
2. ✅ The summary carries: completion date / key deliverables (≤5 items) / leftover gaps (pointing at later milestones) / key ADR references
3. ✅ The matching stage in `roadmap.md` was folded into a reference of ≤ 3 lines
4. ✅ Every repository-wide grep hit on the old tasks.md path was redirected to the summary
5. ✅ The `milestones/{slug}/` directory was removed (its key information is held in the summary)

**Acceptance test**: afterwards, an AI reading `milestones/_archive/m3-summary.md` understands the key outcomes of m3 accurately, without reading the original tasks.md.

---

## Maturity Test

**Any one of the following is enough to archive**; when none of them holds, the skill refuses to run and explains why:

| Condition | Basis for the decision |
|---|---|
| ≥ 60 days since the completion date | the `completed_at` field in the tasks.md frontmatter |
| The in-progress milestone index is ≥ slug + 2 | the numeric suffix of the `in-progress` milestone in roadmap.md |

For both conditions, "every task is status=done or ✅" is also required.

When maturity is not reached, emit the diagnostic `Milestone {slug} does not yet meet the archiving conditions: {specific reason}`.

---

## Behavior

### Stage 1: maturity check

Read `milestones/{slug}/tasks.md` and verify the maturity conditions. Stop when no condition is met.

### Stage 2: summary generation (always runs)

Extract from `tasks.md`:

- **Completion date**: the frontmatter `completed_at`, or the completion date of the last task
- **Key deliverables**: every `status=done` task, grouped by acceptance evidence, distilled into ≤ 5 items
- **Leftover gaps**: any entry marked "deferred" or "next iteration", or left unfinished, together with its target milestone
- **Key ADR references**: the ADR numbers mentioned in tasks.md

### Stage 3: impact analysis (always runs)

Detect:

- The stage sections in `roadmap.md` that need folding
- Every file in the repository that references `milestones/{slug}/tasks.md`

### Stage 4: output (dry-run vs apply)

**dry-run (apply=false, the default)**:

Emit a preview report, changing no file:

```text
=== dry-run preview ===

Will create:
  docs/process-management/milestones/_archive/{slug}-summary.md
  (draft summary below)

Will modify:
  roadmap.md lines N-M folded into:
    ### {stage name} (completed {date}) → see [milestones/_archive/{slug}-summary.md]

Will delete:
  docs/process-management/milestones/{slug}/ ({N} files)

Reference updates ({K} sites):
  {file path}:{line} → old path → new summary path

=== no file was modified ===
```

**apply=true**:

Perform every operation as previewed, then emit the operation log.

---

## Anti-Patterns

- ❌ Running straight through without the maturity check
- ❌ Modifying any file while apply=false
- ❌ Running apply=true while the git working tree holds uncommitted changes (commit first to preserve the state)
- ❌ A summary that omits the leftover gaps (the debt of a past decision must carry over into later milestones)
- ❌ Producing the summary without folding roadmap.md (the two must stay in step)
- ❌ Deleting the tasks directory before the repository-wide reference update is finished

---

## Self-Check

**Before running**:

- [ ] At least one maturity condition holds
- [ ] The git working tree is clean (when apply=true)
- [ ] The summary template fields are complete (completion date / deliverables / gaps / ADR)

**After running (apply=true)**:

- [ ] `_archive/{slug}-summary.md` exists and its content is complete
- [ ] The roadmap.md stage section was folded into ≤ 3 lines
- [ ] A repository-wide grep for `milestones/{slug}/tasks.md` returns nothing
- [ ] The `milestones/{slug}/` directory does not exist

---

## Examples

### Example 1: the normal case — archiving after M3 completes

**Input**:
- `docs/process-management/milestones/m3/` holds a tasks.md completed 60 days ago (all status=completed)
- The M3 stage in `roadmap.md` is marked ✅
- The next milestone, M4, has started

**Execution** (dry-run by default):
1. Maturity check: M3 completed ≥ 60 days ago ✓, the later milestone index differs by ≥ 1 ✓
2. Produce the snapshot `milestones/_archive/m3-summary.md`: completion date, 5 key deliverables, key ADR references
3. Give the impact analysis: the roadmap M3 section will fold into 3 lines; the current path `milestones/m3/` will be deleted
4. Emit the dry-run report and wait for the user to confirm

**After apply**: the roadmap.md M3 section is folded, `milestones/_archive/m3-summary.md` is produced, and `milestones/m3/` is removed.

### Example 2: edge case — the milestone just completed and is not mature enough

**Input**: M5 completed only 14 days ago, and M6 has not started.

**Execution**:
1. Maturity check: completion is < 60 days ago and the later milestone index differs by 0
2. Refuse to run: emit "the milestone is not mature yet (14 days < the 60-day threshold; no later milestone has started); suggest archiving after ≥60 days, or once M6 starts"
3. Produce no snapshot and change no roadmap

**Result**: M5 stays as it is; the user can rerun once the conditions are met.
