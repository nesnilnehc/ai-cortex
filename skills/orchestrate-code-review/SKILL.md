---
name: orchestrate-code-review
description: Orchestrator skill — sequence atomic review-* skills into the post-coding engineering gate and aggregate their findings; functional alignment and acceptance verification remain separate.
description_zh: 编排技能——按 scope → language → framework → library → cognitive 顺序串联原子 review-* 技能，聚合 findings 为统一报告。
tags: [code-review, orchestration]
version: 1.2.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review code, code review, pr review, orchestrate code review]
input_schema:
  type: code-scope
  description: Diff or codebase path(s) to review, plus optional language/framework hint
  defaults:
    scope: diff
    untracked: include
output_schema:
  type: findings-list
  description: Aggregated findings, duplicate-group annotations and risk signals from all executed atomic skills
---

# Orchestrator Skill: Orchestrate Code Review

## Purpose

Chain the atomic review-* skills in a fixed order and aggregate their findings as the **engineering gate**. This skill orchestrates only; it runs no code analysis. Functional alignment against requirements/design/tasks and functional acceptance execution are a sibling gate handled by `review-implementation-alignment` and `automate-tests`, normally converged by `orchestrate-repair-loop`.

---

## Orchestrator Role

Under the naming convention, an orchestrator skill **does exactly 4 things**:

1. **Detect context**: determine scope (diff / codebase), language and framework from user intent and project state
2. **Chain the calls**: run the atomic review-* skills in the fixed order scope → language → framework → library → cognitive
3. **halt-on-failure**: when any atomic skill fails, stop the remaining steps and report the findings collected so far
4. **Aggregate output**: collect and sort findings without rewriting or merging them, group them by location so one defect's several concerns read as one site, and derive risk_signals mechanically

**Strictly forbidden**: running code analysis inside this skill, embedding lint rules, reimplementing the logic of a single atomic skill.

---

## Execution Order (Fixed)

| Step | Type | Candidate atomic skills | Selection rule |
|---|---|---|---|
| 1 | scope | `review-diff` or `review-codebase` | Pick one, by user intent (diff = the current changes; codebase = the given path) |
| 2 | language | `review-typescript` / `review-python` / `review-go` / `review-java` / `review-php` / `review-powershell` / `review-dotnet` / `review-sql` | 0 or 1, inferred from the dominant language in scope |
| 3 | framework | `review-react` / `review-vue` | 0 or 1, inferred from the framework in scope |
| 4 | library | `review-orm-usage` | 0 or 1, inferred from ORM usage in scope |
| 5 | cognitive | `review-security` → `review-reliability` → `review-performance` → `review-architecture` → `review-observability` → `review-testing` | All of them, in order; each atomic Skill resolves whether its profiles apply |

A step with no match is skipped; the final report names which steps were skipped and why.

---

## Behavior

### Step 1: Detect context

- Confirm the scope: when the user has not said, have them pick between `diff` and `codebase`
- diff mode includes untracked files by default
- codebase mode defaults to the repository root; a path may be given
- Language / framework inference: infer from the file extensions in scope and from dependency files (package.json, pyproject.toml and the like); when it is unclear, have the user choose from the candidate list

### Step 2: Chain the calls

Call the atomic skills in the order of the table above, collecting findings at each step (standard format: location / category / severity / title / description / suggestion).

### Step 3: halt-on-failure

Any atomic skill fails → stop the remaining steps, output the findings collected plus an account of the failure.

### Step 4: Aggregate output

- **Grouping**: preserve every atomic finding unchanged, and group them by normalized location per [findings-list](../../specs/findings-list.md) §5.4.1. One changed contract failing an architecture, a testing and an alignment item is one site with three concerns, not three defects. The group takes its highest-severity member as primary; severity counts stay computed over findings, so grouping never changes a total. A group is one site, not a claim of shared cause — never group by an inferred common root.
- **Duplicate handling**: when two findings in a group share `location + title`, additionally mark them an exact duplicate; do not merge them or discard either source.
- **Risk signals**: a **mechanical rule mapping** over the aggregated findings plus the change context (severity distribution, file spread, keyword matches), with no subjective judgement; output the empty list `[]` when no signal is clear
- **Rule coverage**: preserve each atomic Skill's Rule coverage object separately; never merge evidence-limited or not-applicable IDs into passed IDs

---

## Input and Output

### Input

- User intent (review the diff / the codebase / a given path)
- Optional: a language / framework hint

### Output

One aggregated report:

- Findings from each atomic skill (grouped by category or location)
- An account of the skipped steps
- The `risk_signals` list (each entry carries signal_name plus an optional confidence ∈ [0, 1])
- A summary at the top (counts by severity, counts by category, and the number of sites the findings group into)
- Rule coverage by emitting Skill (`passed` / `waived` / `not_applicable` / `evidence_limited`)

---

## Restrictions

### Hard boundaries

- No code analysis, lint or rule matching inside this skill (it breaks the orchestrator 4-things principle)
- No change to the execution order (scope → language → framework → library → cognitive)
- No invented findings; only what the atomic skills produced gets aggregated
- Atomic skills are not asked to emit risk_signals; risk labels are produced in the aggregation stage alone
- No code edits / no fixes applied (that goes to the developer or to `orchestrate-repair-loop`)

### Skill boundaries

**Not done inside the orchestrator skill** (an atomic sub-skill or a downstream skill should take it):

- Direct code analysis → the individual atomic review-* skills
- Single-dimension review → call the matching atomic skill directly
- Applying fixes → `orchestrate-repair-loop` or the development process
- Writing tests → the test-related skills
- Comparing implementation with approved requirements/design/tasks → `review-implementation-alignment`
- Running functional acceptance checks → `automate-tests` or the project-specific acceptance harness

---

## Self-Check

- [ ] Only the 4 things get done: detect context / chain the calls / halt-on-failure / aggregate output
- [ ] No domain detection logic was implemented inside this skill
- [ ] The scope was confirmed with the user
- [ ] The execution order is fixed (scope → language → framework → library → cognitive)
- [ ] Skipped steps are noted in the report
- [ ] Every atomic finding was preserved unchanged; findings were grouped by location only, and exact duplicates were annotated rather than merged
- [ ] Severity counts were computed over findings, not over groups
- [ ] risk_signals were derived mechanically from the aggregated findings, with no subjective judgement
- [ ] Rule coverage metadata was preserved per emitting Skill

---

## Examples

### Example 1: diff review of a .NET project

- Input: the user says "review my changes"; the project is C#
- Dispatch: `review-diff` → `review-dotnet` → `review-security` → `review-reliability` → `review-performance` → `review-architecture` → `review-observability` → `review-testing`
- Skipped: the framework / library steps (no match)
- Aggregation: one report plus risk_signals

### Example 2: codebase review of a Vue frontend

- Input: `src/frontend`; the project uses Vue 3 and an ORM
- Dispatch: `review-codebase` → `review-typescript` → `review-vue` → `review-orm-usage` → all six cognitive reviewers
- Aggregation: one report

### Example 3: edge case — no language match

- Input: a Rust project (no atomic skill covers it)
- Dispatch: `review-codebase` → skip language / framework / library → run every cognitive step
- Aggregation: the report names the skipped language / framework steps and the reason
