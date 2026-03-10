---
name: prune-content
description: Identifies and archives obsolete project content based on user judgment or onboarding analysis. Invoke when user asks to clean up, archive, or audit repository content.
tags: [optimization, documentation, workflow, eng-standards]
version: 1.1.0
license: MIT
metadata:
  author: ai-cortex
triggers: [prune, cleanup, repository maintenance]
input_schema:
  type: free-form
  description: User request to clean up content, or context from onboard-repo/review-codebase
output_schema:
  type: free-form
  description: Report of archived files and cleanup actions
---

# Skill: Prune Content

## Purpose

Help the user maintain a clean codebase by identifying and archiving "expired" or obsolete content. Instead of relying solely on mechanical timestamps or "deprecated" tags, this skill prioritizes **contextual relevance** and **user judgment**, often leveraging insights from `onboard-repo` or project cognition.

---

## Core Objective

**Primary Goal**: Safely archive project content that the user or project context identifies as obsolete, reducing cognitive load without destroying history.

**Success Criteria** (ALL must be met):

1. ✅ **Contextually identified**: Candidates selected based on user intent ("archive the v1 docs") or project analysis ("this directory is from the legacy prototype").
2. ✅ **User confirmed**: User explicitly approved the list of files to be archived.
3. ✅ **Safely archived**: Files moved to `_archive/<original_path>` to preserve structure and history (preferred over deletion).
4. ✅ **No accidental data loss**: Critical directories (`.git`, `node_modules`, `src`) protected from broad sweeps.

**Acceptance Test**: Can a developer browse the active repository and see only relevant, current content, while still being able to find the old content in `_archive` if needed?

---

## Scope Boundaries

**This skill handles**:

- Interactively identifying obsolete content (directories, files).
- Moving content to `_archive/` with structure preservation.
- Listing candidates based on user-provided rules (e.g., "all markdown files in /temp").

**This skill does NOT handle**:

- **Automatic decision making**: Does not decide what is "old" without user or context input.
- **Code refactoring**: Does not fix broken imports after archiving (use `run-repair-loop` or `refactor-code`).
- **Git history rewriting**: Does not use `git filter-branch` or permanently purge history.

**Handoff Point**: Once files are archived, if the build breaks or docs need updating, hand off to `run-repair-loop` or `validate-document-artifacts`.

---

## Use Cases

- **Post-Onboarding Cleanup**: "The onboard-repo report says `docs/v1` is obsolete. Please archive it."
- **Contextual Archiving**: "Archive the old prototype code in `experiments/`."
- **Manual Cleanup**: "Move `README-old.md` to the archive."

---

## Behavior

### 1. Identification (Interactive)

Do not just `grep` or `find` blindly. Ask or analyze based on input.

**Scenario A: User specifies target**
User: "Archive the `legacy` folder."
Action: Verify existence of `legacy`. List contents summary.

**Scenario B: Vague request ("Clean up old stuff")**
Action:

1. **Consult Context**: Check `docs/`, `experiments/`, or `tmp/`.
2. **Ask User**: "I see a `prototypes` folder and some root markdown files from 2023. Should I check those?"
3. **Collaborate**: "Based on `onboard-repo` findings, `src/v1` seems unused. Archive?"

### 2. Proposal & Confirmation

Present a clear plan:
> "I propose to move the following to `_archive/src/v1`:
>
> - `src/v1/ (24 files)`
>
> This will preserve their path structure inside `_archive`. Proceed?"

### 3. Execution (Archive Strategy)

**Standard Action: Move to Archive**
Use `git mv` (if tracked) or `mv` to preserve history linkage where possible, but moving to `_archive` effectively hides it from daily work.

```bash
mkdir -p _archive/<parent_dir>
git mv <source> _archive/<source>
# Fallback if not git tracked:
# mv <source> _archive/<source>
```

**Note**: Mirror the directory structure inside `_archive`.

- `docs/v1/guide.md` -> `_archive/docs/v1/guide.md`

### 4. Cleanup

Check if the original parent directory is empty and remove it if so.

---

## Input & Output

- **Input**: User instruction, list of files, or context from other skills.
- **Output**: Confirmation of moved files, new locations.

---

## Restrictions

### Hard Boundaries

- **No Deletion by Default**: Always prefer **Moving to `_archive`** over `rm`. Only use `rm` if user explicitly says "delete permanently" or "remove".
- **Protect Critical Paths**: Never move/delete `.git`, `.github` (unless asked), `node_modules`, or root configuration files (`package.json`) without explicit, specific confirmation.

### Skill Boundaries

- **Refactoring**: If moving a file breaks code references, this skill identifies the move but does not rewrite the import paths.

---

## Self-Check

### Core Success Criteria (ALL must be met)

- [ ] **Contextually identified**: Candidates matched user intent or project context.
- [ ] **User confirmed**: Explicit approval received.
- [ ] **Safely archived**: Content moved to `_archive/` (not deleted).
- [ ] **Structure preserved**: Directory hierarchy mirrored in archive.

### Process Quality Checks

- [ ] **Git awareness**: Did I use `git mv` if applicable?
- [ ] **Safety**: Did I warn the user if they asked to archive something that looks active (e.g., recently modified)?

### Acceptance Test

**Can a developer browse the active repository and see only relevant, current content, while still being able to find the old content in `_archive` if needed?**

---

## Examples

### Example 1: Archiving a directory

**User**: "Archive the `experiments` folder."
**Agent**: "I found `experiments/` with 5 files. I will move it to `_archive/experiments/`. Proceed?"
**User**: "Yes."
**Agent**:

```bash
mkdir -p _archive
git mv experiments _archive/experiments
```

**Agent**: "Done. `experiments/` is now in `_archive/experiments/`."

### Example 2: Contextual cleanup

**User**: "The onboarding report mentioned `docs/drafts` is confusing. Hide it."
**Agent**: "Understood. I'll archive `docs/drafts` to remove it from the active documentation set. Moving to `_archive/docs/drafts`."
**User**: "Go ahead."
**Agent**: Executes move. "Archived."
