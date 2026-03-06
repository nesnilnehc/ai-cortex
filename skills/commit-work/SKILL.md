---
name: commit-work
description: Create high-quality git commits with clear messages and logical scope. Core goal - produce reviewable commits following Conventional Commits format with pre-commit quality checks.
tags: [git, workflow, eng-standards, automation]
version: 2.0.0
license: MIT
related_skills: [review-diff]
recommended_scope: both
metadata:
  author: ai-cortex
  evolution:
    sources:
      - name: "commit-work"
        repo: "https://github.com/anthropics/skills (assumed)"
        version: "1.0.0"
        license: "MIT"
        type: "fork"
        borrowed: "Core workflow, Conventional Commits format, patch staging approach"
      - name: "review-diff"
        repo: "nesnilnehc/ai-cortex"
        version: "1.3.0"
        license: "MIT"
        type: "integration"
        borrowed: "Pre-commit review methodology"
    enhancements:
      - "Integrated review-diff for pre-commit quality checks"
      - "Added spec/skill.md compliance verification"
      - "Auto-sync with skills/INDEX.md and manifest.json"
      - "Enhanced Self-Check with AI Cortex standards"
input_schema:
  type: free-form
  description: Staged and unstaged changes in the working tree to commit
output_schema:
  type: side-effect
  description: One or more git commits with Conventional Commits messages
---

# Skill: Commit Work

## Purpose

Make commits that are easy to review and safe to ship by ensuring only intended changes are included, commits are logically scoped, and commit messages clearly describe what changed and why. This skill integrates AI Cortex governance standards for projects using the Skills specification.

---

## Core Objective

**Primary Goal**: Produce one or more git commits with clear messages, logical scope, and verified quality that are ready to push.

**Success Criteria** (ALL must be met):

1. ✅ **Changes reviewed**: Ran `git diff` before staging and `git diff --cached` before each commit
2. ✅ **Logical scope**: Each commit contains related changes only; unrelated changes split into separate commits
3. ✅ **Conventional Commits format**: All commit messages follow `type(scope): summary` format with clear body
4. ✅ **Quality verified**: Ran appropriate tests, lint, or build commands and all checks passed
5. ✅ **No sensitive data**: No secrets, tokens, debug code, or unintended changes included
6. ✅ **Registry synchronized** (AI Cortex projects): If skills/ changed, both INDEX.md and manifest.json updated

**Acceptance Test**: Can a reviewer understand what changed and why from the commit message alone, without reading the diff?

---

## Scope Boundaries

**This skill handles**:
- Reviewing uncommitted changes
- Splitting mixed changes into logical commits
- Staging changes with patch mode when needed
- Writing Conventional Commits messages
- Running pre-commit quality checks
- Syncing AI Cortex registries (INDEX.md, manifest.json)

**This skill does NOT handle**:
- Code review of existing commits (use `review-diff` skill)
- Rewriting git history or rebasing (use git rebase commands)
- Resolving merge conflicts (use git merge/rebase workflows)
- Creating pull requests or pushing to remote (separate workflow)

**Handoff point**: When all changes are committed and verified, hand off to push/PR workflow or next development task.

## Use Cases

- User asks to commit work, stage changes, or craft commit messages
- Need to split mixed changes into logical, reviewable commits
- Creating commits that follow Conventional Commits format
- Ensuring commits meet project quality standards before pushing
- Working in AI Cortex projects where INDEX.md and manifest.json must stay synchronized

## Behavior

### Workflow (checklist)

1) **Inspect the working tree before staging**
   - Run `git status`
   - Run `git diff` (unstaged changes)
   - If many changes: `git diff --stat` for overview

2) **Run pre-commit review (AI Cortex enhancement)**
   - Invoke `review-diff` skill to check for:
     - Unintended changes or debug code
     - Security issues or exposed secrets
     - Breaking changes or compatibility issues
   - Address findings before proceeding to staging

3) **Decide commit boundaries (split if needed)**
   - Split by logical concerns:
     - Feature vs refactor
     - Backend vs frontend
     - Formatting vs logic
     - Tests vs production code
     - Dependency bumps vs behavior changes
   - If changes are mixed in one file, plan to use patch staging

4) **Stage only what belongs in the next commit**
   - Prefer patch staging for mixed changes: `git add -p`
   - To unstage a hunk/file: `git restore --staged -p` or `git restore --staged <path>`
   - Stage related changes together

5) **Review what will actually be committed**
   - Run `git diff --cached`
   - Sanity checks:
     - No secrets or tokens
     - No accidental debug logging
     - No unrelated formatting churn
     - No commented-out code blocks

6) **Describe the staged change in 1-2 sentences**
   - Answer: "What changed?" + "Why?"
   - If you cannot describe it cleanly, the commit is probably too big or mixed; go back to step 3

7) **Write the commit message**
   - Use Conventional Commits (required):

     ```text
     type(scope): short summary
     
     body (what/why, not implementation diary)
     
     footer (BREAKING CHANGE) if needed
     ```

   - Prefer an editor for multi-line messages: `git commit -v`
   - Use `references/commit-message-template.md` if helpful
   - Keep summary imperative and specific ("Add", "Fix", "Remove", "Refactor")

8) **Run the smallest relevant verification**
   - Run the repo's fastest meaningful check (unit tests, lint, or build) before moving on
   - Ensure the commit doesn't break existing functionality

9) **Sync registry if needed (AI Cortex projects only)**
   - If commit affects `skills/` directory:
     - Verify `skills/INDEX.md` is updated with new/changed skills
     - Verify `manifest.json` capabilities array is updated
     - Verify `skills/scenario-map.json` is updated if skills were added, removed, or materially changed (per spec Metadata Sync)
     - Run `scripts/verify-registry.mjs` if present
   - If adding or moving skills, INDEX, manifest, and (as needed) scenario-map must be updated together

10) **Repeat for the next commit until the working tree is clean**

### Interaction Policy

- Ask user if they want single or multiple commits (default: multiple small commits for unrelated changes)
- Confirm commit style requirements (Conventional Commits are required by this skill)
- Ask about any project-specific rules: max subject length, required scopes, etc.
- For AI Cortex projects: confirm whether to run registry sync checks

## Input & Output

### Input Requirements

- A git repository with uncommitted changes
- User intent: what work should be committed
- Optional: commit style preferences, scoping rules

### Output Contract

Provide:

- The final commit message(s) with type, scope, and clear description
- A short summary per commit explaining what changed and why
- The commands used to stage and review (minimum: `git diff --cached`)
- Any test or verification commands run
- For AI Cortex projects: confirmation that INDEX.md, manifest.json, and (as needed) scenario-map.json are synchronized

## Restrictions

### Hard Boundaries

- Do not commit without reviewing staged changes (`git diff --cached`)
- Do not mix unrelated changes in a single commit
- Do not write vague commit messages ("fix stuff", "updates", "WIP")
- Do not skip verification steps if tests or linters are available
- Do not commit secrets, tokens, or sensitive data
- For AI Cortex projects: do not commit skill changes without updating INDEX.md, manifest.json, and (as needed) scenario-map.json

### Skill Boundaries (Avoid Overlap)

**Do NOT do these (other skills handle them)**:

- **Code review of existing commits**: Reviewing diffs that are already committed → Use `review-diff` skill
- **Git history rewriting**: Rebasing, squashing, amending old commits → Use git rebase/amend commands directly
- **Merge conflict resolution**: Resolving conflicts during merge/rebase → Use git merge/rebase workflows
- **Pull request creation**: Creating PRs, requesting reviews, managing PR workflow → Use platform-specific PR tools
- **Code implementation**: Writing the code changes being committed → Use development/implementation skills

**When to stop and hand off**:

- User asks "can you review this commit?" → Use `review-diff` skill for existing commits
- User asks "can you push this?" → Commits complete, hand off to push/PR workflow
- User asks "can you rebase these commits?" → Commits complete, hand off to git rebase workflow
- All changes committed and verified → Skill complete, ready for push or next task

## Self-Check

### Core Success Criteria (ALL must be met)

- [ ] **Changes reviewed**: Ran `git diff` before staging and `git diff --cached` before each commit
- [ ] **Logical scope**: Each commit contains related changes only; unrelated changes split into separate commits
- [ ] **Conventional Commits format**: All commit messages follow `type(scope): summary` format with clear body
- [ ] **Quality verified**: Ran appropriate tests, lint, or build commands and all checks passed
- [ ] **No sensitive data**: No secrets, tokens, debug code, or unintended changes included
- [ ] **Registry synchronized** (AI Cortex projects): If skills/ changed, INDEX.md, manifest.json, and (as needed) scenario-map.json updated

### Process Quality Checks

- [ ] **Pre-commit review**: Ran `review-diff` skill for AI Cortex projects to check for unintended changes, security issues, or breaking changes
- [ ] **Patch staging used**: Used `git add -p` when changes were mixed in single files
- [ ] **Commit boundaries clear**: Can describe each commit's purpose in 1-2 sentences
- [ ] **Message quality**: Summary is imperative and specific; body explains what and why (not implementation details)
- [ ] **Breaking changes marked**: Used `!` or `BREAKING CHANGE:` footer if applicable
- [ ] **Commands documented**: Listed commands used for staging, review, and verification

### Acceptance Test

**Can a reviewer understand what changed and why from the commit message alone, without reading the diff?**

If NO: Commit message is unclear. Revise message to explain what and why.

If YES: Commit is ready to push.

## Examples

### Example 1: Simple feature addition

**Scenario**: Added a new function to utils.js

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
```

**Output**:

- Commit: `feat(utils): add formatDate helper function`
- Summary: Added date formatting utility to centralize date handling logic
- Commands: `git diff`, `git diff --cached`, `npm test`

### Example 2: Mixed changes requiring split (edge case)

**Scenario**: Modified auth.js with both a bug fix and a refactor, plus updated tests

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
```

**Output**:

- Commit 1: `fix(auth): prevent null pointer in token validation` - Fixed crash when token is null
- Commit 2: `refactor(auth): extract token parsing to separate function` - Improved code organization
- Commit 3: `test(auth): add tests for token validation edge cases` - Increased test coverage
- Commands: `git add -p`, `git diff --cached` (×3), `npm test` (×3)

### Example 3: AI Cortex skill addition (edge case)

**Scenario**: Added new skill `analyze-logs` to AI Cortex project

**Commands**:

```bash
git status
# Shows: skills/analyze-logs/SKILL.md (new), skills/INDEX.md (modified), manifest.json (modified)

git diff skills/INDEX.md
git diff manifest.json
# Verify both registries reference the new skill correctly

git add skills/analyze-logs/
git add skills/INDEX.md
git add manifest.json
git diff --cached

# Run registry verification
node scripts/verify-registry.mjs
# ✓ INDEX.md and manifest.json are synchronized

npm test
git commit -m "feat(skills): add analyze-logs skill for log parsing

Add new skill to parse and analyze application logs with pattern
matching and error extraction. Includes examples for common log
formats.

Updated INDEX.md and manifest.json to register the new skill."
```

**Output**:

- Commit: `feat(skills): add analyze-logs skill for log parsing`
- Summary: Added log analysis capability with registry synchronization
- Commands: `git diff --cached`, `node scripts/verify-registry.mjs`, `npm test`
- Registry sync: ✓ Both INDEX.md and manifest.json updated
