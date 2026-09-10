---
name: commit-work
description: Create high-quality git commits with clear messages and logical scope. Core goal - produce reviewable commits following Conventional Commits format with pre-commit quality checks.
description_zh: 创建高质量 git 提交：清晰消息与合理范围；遵循 Conventional Commits，含 pre-commit 质量检查。
tags: [git, workflow, automation]
version: 2.0.2
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
  origin: vendored-derived
  source-registry: ../SOURCES.yaml
triggers: [commit, commit work]
input_schema:
  type: free-form
  description: Staged and unstaged changes in the working tree to commit
output_schema:
  type: side-effect
  description: One or more git commits with Conventional Commits messages
---

# Skill: Commit Work

## Purpose

Produce git commits that are easy to review and safe to ship: only the intended changes, sensible commit granularity, and a message that says what was done and why. This skill is wired into the AI Cortex INDEX synchronization constraint — when a commit touches the `skills/` directory it checks that INDEX.md was updated.

The local copy is installed and updated by AI Cortex; the verifiable upstream, pinned commit, license, and local enhancements are recorded in [`../SOURCES.yaml`](../SOURCES.yaml). At runtime this skill must not be downloaded or replaced from an external registry.

---

## Core Objective

**Primary goal**: produce one or more git commits with a clear message, logical scope, and verified quality, ready to push.

**Success criteria** (all must hold):

1. ✅ **Changes reviewed**: `git diff` before staging, `git diff --cached` before every commit
2. ✅ **Logical scope**: each commit contains related changes only; unrelated changes go into separate commits
3. ✅ **Conventional Commits format**: every commit message follows the `type(scope): summary` format, with a clear body
4. ✅ **Quality verified**: the appropriate test, lint, or build command was run and every check passed
5. ✅ **No sensitive data**: no secrets, tokens, debug code, or accidental changes are included
6. ✅ **INDEX synced** (AI Cortex projects): the matching INDEX.md is updated whenever a skill / rule / spec / protocol changes

**Acceptance** test: can a reviewer tell what changed and why from the commit message alone, without reading the diff?

---

## Scope Boundaries

**This skill owns**:

- Reviewing uncommitted changes
- Splitting mixed changes into logical commits
- Staging changes with patch mode when needed
- Writing Conventional Commits messages
- Running pre-commit quality checks
- Syncing the AI Cortex registries (INDEX.md)

**This skill does not own**:

- Code review of existing commits (use the `review-diff` skill)
- Rewriting git history or rebasing (use the git rebase commands)
- Resolving merge conflicts (use the git merge/rebase workflow)
- Creating pull requests or pushing to a remote (a separate workflow)

**Handoff point**: once every change is committed and verified, hand off to the push/PR workflow or to the next development task.

## Use Cases

- The user asks to commit work, stage changes, or craft a commit message
- Mixed changes need splitting into logical, reviewable commits
- Creating commits that follow the Conventional Commits format
- Making sure commits meet the project's quality bar before pushing
- Working in an AI Cortex project, keeping skills/INDEX.md / rules/INDEX.md / specs/INDEX.md / protocols/INDEX.md in step with the corresponding assets

## Behavior

### Workflow (checklist)

If `CLAUDE.md` or `.ai-cortex/config.yaml` exists, prefer the `test_command` recorded there for quality verification; otherwise infer it from the project build configuration. See [docs/guides/project-config.md](../../docs/guides/project-config.md).

1) **Inspect the working tree before staging**
   - Run `git status`
   - Run `git diff` (unstaged changes)
   - With many changes: `git diff --stat` for an overview

2) **Suggest a pre-commit review (halt-and-suggest)**
   - Tell the user to run `/review-diff` (or `/orchestrate-code-review`) first; this skill does not call other skills itself
   - Resume staging once the user comes back with the findings
   - If the user skips this step: go straight to the next one (no blocking)

3) **Decide the commit boundaries (split if needed)**
   - Divide by logical concern:
     - Feature vs refactor
     - Backend vs frontend
     - Formatting vs logic
     - Tests vs production code
     - Dependency bumps vs behavior changes
   - If the changes are mixed inside one file, plan for patch staging

4) **Stage only what belongs in the next commit**
   - For mixed changes, prefer hunk staging: `git add -p`
   - To unstage a hunk/file: `git restore --staged -p` or `git restore --staged <path>`
   - Stage related changes together

5) **Review what will actually be committed**
   - Run `git diff --cached`
   - Sanity checks:
     - No secrets or tokens
     - No stray debug logging
     - No unrelated formatting changes
     - No commented-out code blocks

6) **Describe the staged change in 1-2 sentences**
   - Answer: "what changed?" + "why?"
   - If you cannot describe it clearly, the commit is too large or mixed; go back to step 3

7) **Write the commit message**
   - Use Conventional Commits (required):

     
```text
     type(scope): short summary
     
     body (what/why, not implementation diary)
     
     footer (BREAKING CHANGE) if needed
     ```

   - For a multi-line message, prefer the editor: `git commit -v`
   - Use `references/commit-message-template.md` if helpful
   - Keep the summary imperative and specific ("add", "fix", "remove", "refactor")

8) **Run the minimum relevant verification**
   - Run the repository's fastest meaningful check before moving on (unit tests, lint, or build)
   - Make sure the commit does not break existing functionality

9) **Sync INDEX.md (AI Cortex projects only)**
   - If the commit touches the `skills/` directory:
     - Check that `skills/INDEX.md` was updated for the added / modified / removed skill
     - Check that the INDEX entry matches the description in the target SKILL.md
   - If the commit touches the `rules/` / `specs/` / `protocols/` directories:
     - Sync the corresponding `INDEX.md`

10) **Repeat for the next commit until the working tree is clean**

### Interaction policy

- Ask the user whether they want one commit or several (default: several small commits for unrelated changes)
- Confirm the commit style requirement (this skill expects Conventional Commits)
- Ask about project-specific rules: maximum subject length, required scopes, and so on.
- For AI Cortex projects: confirm whether the corresponding INDEX.md is synced

## Input & Output

### Input requirements

- A git repository with uncommitted changes
- User intent: which work goes into the commit
- Optional: commit style preferences, scope rules

### Output contract

Deliver:

- The final commit message, with type, scope, and a clear description
- A short summary per commit explaining what changed and why
- The commands used for staging and review (at minimum: `git diff --cached`)
- Any test or verification command that was run
- For AI Cortex projects: confirmation that the corresponding INDEX.md is synced

## Restrictions

### Hard Boundaries

- Do not commit without reviewing the staged changes (`git diff --cached`)
- Do not mix unrelated changes into one commit
- Do not write vague commit messages ("fix stuff", "update", "WIP")
- Do not skip the verification step when tests or a linter are available
- Do not commit secrets, tokens, or sensitive data
- For AI Cortex projects: do not commit an asset change without syncing the corresponding INDEX.md

### Skill Boundaries (avoid overlap)

**Do not do these (other skills handle them)**:

- **Code review of existing commits**: reviewing a committed diff → use the `review-diff` skill
- **Git history rewriting**: rebase, squash, amend old commits → use the git rebase/amend commands directly
- **Merge conflict resolution**: resolving conflicts during a merge/rebase → use the git merge/rebase workflow
- **Pull request creation**: creating a PR, requesting review, running the PR workflow → use the platform-specific PR tooling
- **Code implementation**: writing the code changes being committed → use the development/implementation skills

**When to stop and hand off**:

- The user asks "can you review this commit?" → use the `review-diff` skill on the existing commit
- The user asks "can you push this?" → committing is done; hand off to the push / PR workflow
- The user asks "can you rebase these commits?" → committing is done; hand off to the git rebase workflow
- Every change committed and verified → the skill is done, ready to push or move to the next task

## Self-Check

### Core success criteria (all must hold)

- [ ] **Changes reviewed**: `git diff` before staging, `git diff --cached` before every commit
- [ ] **Logical scope**: each commit contains related changes only; unrelated changes go into separate commits
- [ ] **Conventional Commits format**: every commit message follows the "type(scope): summary" format, with a clear body
- [ ] **Quality verified**: the appropriate test, lint, or build command was run and every check passed
- [ ] **No sensitive data**: no secrets, tokens, debug code, or accidental changes are included
- [ ] **INDEX synced** (AI Cortex projects): the matching INDEX.md is updated whenever a skill / rule / spec / protocol changes

### Process quality checks

- [ ] **Pre-commit review**: ran the `review-diff` skill for AI Cortex projects, checking for unintended changes, security issues, or breaking changes
- [ ] **Patch staging used**: `git add -p` used when changes are mixed inside a single file
- [ ] **Commit boundaries clear**: the purpose of each commit can be stated in 1-2 sentences
- [ ] **Message quality**: the summary is imperative and specific; the body explains what and why (not implementation detail)
- [ ] **Breaking changes marked**: Used `!` or `BREAKING CHANGE:` footer if applicable
- [ ] **Commands recorded**: the commands used for staging, review, and verification are listed

### Acceptance test

**Can a reviewer tell what changed and why from the commit message alone, without reading the diff?**

If no: the commit message is unclear. Revise it to explain what and why.

If yes: the commit is ready to push.

## Examples

### Example 1: a simple feature addition

**Scenario**: add a new function to utils.js

**Commands**:

```bash

git status
git diff

# Review shows only the new function, no other changes

git add utils.js
git diff --cached

# Verify staged changes are correct

npm test
git commit -m "feat(utils): add formatDate helper function

Add formatDate to handle ISO 8601 date formatting consistently
across the application. Returns formatted string or null for
invalid inputs."

```markdown

**Output**:

- Commit: `feat(utils): add formatDate helper function`
- Summary: added a date formatting utility to centralize date handling logic
- Commands: `git diff`, `git diff --cached`, `npm test`

### Example 2: mixed changes that need splitting (edge case)

**Scenario**: auth.js was changed with a bug fix and a refactor, and the tests were updated

**Commands**:

```bash

git status
git diff --stat

# Shows auth.js and auth.test.js changed

# Run review-diff first (AI Cortex)

# [review-diff identifies: bug fix in line 45, refactor in lines 100-150]

# Split into logical commits

# Commit 1: Bug fix only

git add -p auth.js

# Select only the bug fix hunk

git diff --cached
npm test
git commit -m "fix(auth): prevent null pointer in token validation

Check for null token before accessing properties to avoid
runtime errors when token is missing."

# Commit 2: Refactor

git add -p auth.js

# Select refactor hunks

git diff --cached
npm test
git commit -m "refactor(auth): extract token parsing to separate function

Move token parsing logic into parseAuthToken() for better
testability and reuse across auth module."

# Commit 3: Tests

git add auth.test.js
git diff --cached
npm test
git commit -m "test(auth): add tests for token validation edge cases

Cover null token, malformed token, and expired token scenarios."

```markdown

**Output**:

- Commit 1: "fix(auth): prevent null pointer in token validation" - fixes the crash when the token is null
- Commit 2: "refactor(auth): extract token parsing to separate function" - better code organization
- Commit 3: "test(auth): add tests for token validation edge cases" - more test coverage
- Commands: `git add -p`, `git diff --cached` (×3), `npm test` (×3)

### Example 3: adding a skill to AI Cortex (with INDEX sync)

**Scenario**: add the `analyze-logs` skill to an AI Cortex project

**Commands**:

```bash

git status

# Shows: skills/analyze-logs/SKILL.md (new), skills/INDEX.md (modified)

git diff skills/INDEX.md

# Confirm the INDEX line was added and matches the SKILL.md description

git add skills/analyze-logs/ skills/INDEX.md
git diff --cached

git commit -m "feat(skills): add analyze-logs for log parsing

Add the analyze-logs skill: parses application logs by pattern matching and extracts errors.
Includes 3 examples covering common log formats.

Sync skills/INDEX.md."

```text

**Output**:

- Commit: `feat(skills): add analyze-logs for log parsing`
- Summary: new log analysis skill + INDEX sync
- Commands: `git status`, `git diff --cached`
- INDEX sync: ✓ skills/INDEX.md contains the new line
