---
name: review-diff
description: Review only git diff for impact, regression, correctness, compatibility, and side effects. Scope-only atomic skill; output is a findings list for aggregation.
description_zh: 仅审查 git diff（含未跟踪文件）的影响、回归、正确性、兼容性与副作用；scope-only 原子技能，输出 findings 列表。
tags: [code-review, scope-only]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review diff, diff review]
input_schema:
  type: code-scope
  description: Git diff (staged + unstaged, optional untracked) to review
output_schema:
  type: findings-list
  description: Scope-only findings for impact, regression, correctness, compatibility, and side effects
---

# Skill: Review Diff

## Purpose

Review the **current change** alone (git diff: staged + unstaged + optionally untracked files) across 5 dimensions: intent / impact, regression / correctness, breaking change / compatibility, side effects / idempotency, observability. Produce a scope-only findings list that feeds the scope step of `orchestrate-code-review` for aggregation.

No architecture / security / language / framework-specific analysis — those belong to the matching atomic skills.

---

## Core Objective

**Primary goal**: produce a findings list across the 5 dimensions for the diff scope alone (untracked files included).

**Success criteria** (all of them must hold):

1. ✅ **Diff scope only**: review the change set alone; do not open repository-level / architecture / security / language-specific checks
2. ✅ **All 5 dimensions covered**: intent / impact, regression / correctness, breaking change / compatibility, side effects / idempotency, observability
3. ✅ **Format conformant**: every finding carries location / category=`scope` / severity / title / description / suggestion, per [specs/findings-list.md](../../specs/findings-list.md)
4. ✅ **Precise locations**: every finding cites a concrete `file:line` or `@@` hunk
5. ✅ **Bug fix verified**: a bug-fix diff must have its fix verified for correctness, with any leftover or partial problem flagged

---

## Scope Boundaries

**This skill owns**:

- The current git diff (staged + unstaged)
- Untracked files in the change set (included by default, treated as a whole-file add)
- Analysis across 5 dimensions: intent / impact, regression / correctness, breaking / compatibility, side effects / idempotency, observability

**This skill does not own**:

- Repository-level or snapshot-level review → `review-codebase`
- The full orchestrated review → `orchestrate-code-review`
- The architecture / security / performance / testing cognitive dimensions → the matching cognitive atomic skills
- Language- / framework-specific conventions → the matching atomic skills

**Handoff point**: once the findings are out, they feed the scope step of orchestrate-code-review for aggregation, or go to `orchestrate-repair-loop` for a fix iteration.

---

## Use Cases

- **pre-commit / pre-PR gate**: a quick look at what the change introduces before committing
- **As the scope step of orchestrate-code-review**: this one or `review-codebase`, never both
- **Focused review**: the user says "look at the change only"

---

## Behavior

### Scope resolution

- **What gets analyzed**: the files in the change set — the diff (staged + unstaged) plus the untracked files included by default
- **Untracked file handling**: the caller passes the path and the full content; treat it as a whole-file add, apply the same 5-dimension checklist, and cite file:line
- **What does not get analyzed**: files that are unchanged or outside the change set

### The 5-dimension checklist

For each changed file, produce findings on these dimensions:

1. **Intent and impact**: what changed and why; the effect on callers / data / configuration / deployment
2. **Regression and correctness**: whether a new bug or a missed edge case was introduced; whether a bug-fix diff fixes the whole thing
3. **Breaking change and compatibility**: whether an API / data / configuration contract breaks; backward compatibility; versioning / deprecation
4. **Side effects and idempotency**: unintended side effects, data corruption, risk on repeated execution, idempotency problems
5. **Observability**: whether the change adds or repairs the logs, metrics and error messages needed to debug in production

### Special cases

- **A bug-fix diff**: verify the fix is correct, and record any leftover or partial problem
- **A formatting- / comment-only diff**: emit one minor finding, "formatting / comments only, no behavior change"; where a comment contradicts the code, emit a finding with a suggestion

---

## Input and Output

### Input

- **git diff**: the staged + unstaged changes of the current branch against HEAD
- **Untracked files** (included by default): path + full content

### Output

- **Findings list**: the standard format (`location` / `category=scope` / `severity` / `title` / `description` / `suggestion`)
- Every finding must carry a file:line or @@ hunk reference
- Every finding must carry an actionable suggestion (the direction of the fix + the exact location)

---

## Restrictions

### Hard boundaries

- Do not review files outside the diff
- Emit no finding that lacks a file:line reference
- Use no vague language ("might be a problem", carrying neither a type nor a direction → delete it)
- Run no security / architecture / language / framework check (stay inside the scope dimension)

### Skill boundaries

**Not done here** (other atomic skills own it):

- Repository-level / snapshot-level review → `review-codebase`
- Full-dimension orchestration → `orchestrate-code-review`
- Security → `review-security`
- Architecture → `review-architecture`
- Language / framework → the matching atomic skills

---

## Self-Check

- [ ] Only the change set was reviewed (the diff plus the untracked files included)
- [ ] All 5 dimensions are covered
- [ ] Every finding conforms to the format (all 6 fields)
- [ ] Every finding carries a file:line or @@ hunk reference
- [ ] Every finding carries an actionable suggestion
- [ ] The fix in a bug-fix diff was verified for correctness

---

## Examples

### Example 1: an API change

- **Input**: a diff that adds a query parameter and reshapes the response
- **Expected**: findings covering intent / impact (on callers), backward-compatibility risk, and a breaking-change suggestion (versioning or deprecation, say); citing the exact lines or @@ hunks; no security / architecture finding (those go to the matching atomic skills)

### Example 2: a bug fix

- **Input**: a diff that fixes a null pointer and an error code
- **Expected**: findings confirming the fix, plus a check of whether similar null pointer / error code problems remain; the observability dimension (logs / errors); citing the changed lines; category=scope

### Example 3: formatting / comments only

- **Input**: a diff carrying only indentation / whitespace / comment changes
- **Expected**: either no finding, or one minor finding, "formatting / comments only, no behavior change"; where a comment contradicts the code, emit a finding with a suggestion

### Example 4: a new (untracked) file in the change set

- **Input**: the diff plus an untracked file (path + full content)
- **Expected**: the new file is reviewed as a whole-file add; the 5-dimension checklist applies; location=the path with line references; category=scope
