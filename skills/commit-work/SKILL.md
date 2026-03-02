---
name: commit-work
description: Create high-quality git commits with AI Cortex governance - review changes, split logically, write clear messages (Conventional Commits), sync with INDEX/manifest
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
---

# Skill: Commit Work

## Purpose

Make commits that are easy to review and safe to ship by ensuring only intended changes are included, commits are logically scoped, and commit messages clearly describe what changed and why. This skill integrates AI Cortex governance standards for projects using the Skills specification.

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
     - Run `scripts/verify-registry.mjs` if present
   - If adding or moving skills, both registries must be updated together

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
- For AI Cortex projects: confirmation that INDEX.md and manifest.json are synchronized

## Restrictions

- Do not commit without reviewing staged changes (`git diff --cached`)
- Do not mix unrelated changes in a single commit
- Do not write vague commit messages ("fix stuff", "updates", "WIP")
- Do not skip verification steps if tests or linters are available
- Do not commit secrets, tokens, or sensitive data
- For AI Cortex projects: do not commit skill changes without updating both INDEX.md and manifest.json

## Self-Check

Before completing, verify:

1. **Staging review**:
   - [ ] Ran `git status` and `git diff` before staging
   - [ ] Ran `review-diff` skill (AI Cortex projects)
   - [ ] Reviewed `git diff --cached` before each commit

2. **Commit quality**:
   - [ ] Each commit has a single, clear purpose
   - [ ] No unrelated changes mixed together
   - [ ] No secrets, tokens, or debug code included

3. **Message quality**:
   - [ ] Follows Conventional Commits format: `type(scope): summary`
   - [ ] Summary is imperative and specific
   - [ ] Body explains what and why (not implementation details)
   - [ ] Breaking changes are marked with `!` or `BREAKING CHANGE:` footer

4. **Verification**:
   - [ ] Ran appropriate tests, lint, or build commands
   - [ ] All checks passed before moving to next commit

5. **Registry sync (AI Cortex projects)**:
   - [ ] If skills/ changed: INDEX.md updated
   - [ ] If skills/ changed: manifest.json updated
   - [ ] Ran verify-registry.mjs if available

6. **Deliverables**:
   - [ ] Provided final commit message(s)
   - [ ] Provided summary of what/why for each commit
   - [ ] Listed commands used for staging and review

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
