---
name: commit-work
description: Create high-quality git commits with clear messages and logical scope. Core goal - produce reviewable commits following Conventional Commits format with pre-commit quality checks.
version: 2.2.0
license: MIT
---

# Skill: Commit Work

Produce reviewable git commits containing only the authorized work, with logical boundaries, relevant verification, and messages explaining what changed and why.

The pinned upstream, license, and local adaptations are recorded in [SOURCES.yaml](../SOURCES.yaml). Use the installed local copy; do not download or replace it at runtime.

## Inputs and Output

**Input:** a git repository and the work to commit. Infer scope from the user's request and current task; ask only when ownership or intended scope remains ambiguous. Honor a request limited to staging or drafting a message without creating a commit.

**Output:** commit hashes and messages, a short explanation per commit, staging/review and verification commands with results, and any authorized work left uncommitted or blocked. For staging or message-only requests, report that result instead.

## Workflow

1. **Inspect scope and state.** Read project commit guidance and run `git status`, `git diff`, and `git diff --cached`; use `git diff --stat` for an overview when useful. Inspect relevant untracked files separately. Preserve unrelated changes, including changes already staged by another task. If staged ownership cannot be resolved, ask before altering or committing it.
2. **Use relevant review evidence.** Reuse existing findings for the current changes and follow the project's review requirements. Obtain a required review before committing; do not add a generic pause asking the user to run another skill and return. If no review is required and no unresolved concern warrants one, continue.
3. **Choose logical commit boundaries.** Keep a behavior change and its directly supporting tests together. Split independent fixes, refactors, formatting, or dependency updates when they can be reviewed separately. For mixed files, use patch staging such as `git add -p`; otherwise stage explicit paths. Unstage only changes owned by this task, using `git restore --staged -p` or `git restore --staged <path>` when needed.
4. **Prepare and verify.** Synchronize any generated assets required by project guidance before the final check. In AI Cortex, synchronize the matching Skill, Rule, Spec, or Protocol index using its repository procedure. Select the smallest meaningful verification from project guidance and configuration; see [project configuration](../../docs/guides/project-config.md) when applicable. Reuse passing results that still cover the staged content. If verification fails or a required check is unavailable, report the cause and resolve it before committing; do not claim an unrun check passed.
5. **Review the exact staged content.** Run `git diff --cached` before every commit, including after generated changes. Check for secrets, accidental debug code, unrelated edits, and changes outside the authorized scope. Describe the staged change in one or two sentences; if its purpose is unclear, revisit the boundaries.
6. **Write the message and commit.** Use Conventional Commits and the project's scope conventions. Keep the subject imperative and specific, explain what and why in the body, and mark breaking changes with `!` or `BREAKING CHANGE:`. Use the [message template](references/commit-message-template.md) when useful. Prefer an editor or a message file for multiline text. Create the commit, then inspect its hash, summary, and remaining working-tree state.
7. **Finish the authorized scope.** Repeat for the remaining authorized commits. Completion does not require a clean working tree: leave other tasks' changes intact and report relevant remaining work.

## Boundaries

This skill prepares and creates commits. Implementation, history rewriting, conflict resolution, push, and pull requests belong to their respective workflows and require their own task authorization. Do not treat a commit request as authorization for those actions.

## Self-Check

- [ ] Each commit contains only authorized changes; unrelated staged and unstaged work is preserved.
- [ ] Commit boundaries keep related behavior and verification together, and the staged diff was reviewed before each commit.
- [ ] Messages explain what and why, follow Conventional Commits, and identify breaking changes.
- [ ] Relevant checks and required generated assets are current; failures or unavailable checks are reported accurately.
- [ ] The result includes commit identities, commands and outcomes, and remaining work within scope.

## Example: Mixed work

A repository contains an authorized authentication fix and its tests, an independent authorized refactor in the same file, and another task's documentation edits. Patch-stage the fix with its tests, verify and commit it, then stage and commit the refactor separately. Leave the documentation edits intact. Report both commits and the remaining unrelated changes.
