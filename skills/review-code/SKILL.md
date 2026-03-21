---
name: review-code
description: Orchestrate comprehensive code reviews by running scope, language, framework, library, and cognitive review skills in sequence, then aggregate findings into a unified report.
tags: [code-review]
version: 2.6.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review, code review, pr review, review code]
aliases: [rc]
input_schema:
  type: code-scope
  description: Diff or codebase path(s) to review, plus optional language/framework hint
  defaults:
    scope: diff
    untracked: include
output_schema:
  type: findings-list
  description: Aggregated, deduplicated findings with risk signals from all executed atomic skills
---

# Skill: Review Code (Orchestrator)

## Purpose

**This skill does not perform code analysis itself.** It is a **meta skill** that orchestrates other atomic review skills in a fixed order, then **aggregates** their findings into a single report. Use it when the user asks for a full "review code" or "code review" and you want to apply scope → language → framework → library → cognitive skills and produce one combined output. For a single-dimension review (e.g. only diff or only security), invoke the corresponding atomic skill directly ([review-diff](../review-diff/SKILL.md), [review-security](../review-security/SKILL.md), etc.).

---

## Core Objective

**Primary Goal**: Produce a comprehensive, deduplicated code review report by orchestrating atomic review skills in a fixed sequence and aggregating their findings.

**Success Criteria** (ALL must be met):

1. ✅ **Scope confirmed**: User's review scope (diff or codebase paths) is confirmed before execution
2. ✅ **Execution order followed**: Skills run in fixed sequence (scope → language → framework → library → cognitive)
3. ✅ **All applicable skills executed**: Scope skill + language skill (if applicable) + framework skill (if applicable) + all cognitive skills (security, performance, architecture, testing) are run
4. ✅ **Findings aggregated**: All findings from atomic skills are collected and merged into a single report using standard format (Location, Category, Severity, Title, Description, Suggestion)
5. ✅ **Findings deduplicated**: Duplicate findings (same Location + Title) are merged, keeping highest severity
6. ✅ **Risk signals derived**: Risk signals are generated from final deduplicated findings and change context (not from individual skills)

**Acceptance Test**: Does the final report contain findings from all executed atomic skills, with no duplicates, and risk signals derived only at the aggregation stage?

---

## Scope Boundaries

**This skill handles**:

- Orchestrating atomic review skills in fixed order
- Confirming review scope with user (diff vs codebase, paths, language/framework)
- Collecting findings from each atomic skill
- Aggregating and deduplicating findings into single report
- Deriving risk signals from final findings

**This skill does NOT handle**:

- Direct code analysis (use atomic review skills: `review-diff`, `review-codebase`, `review-security`, etc.)
- Single-dimension reviews (use atomic skills directly: `review-diff` for diff only, `review-security` for security only, etc.)
- Implementation of fixes (use development/refactoring skills)
- Test writing (use testing skills)

**Handoff point**: When aggregated report is complete, hand off to user for review or to development workflow for implementing fixes.

---

## Use Cases

- **Full code review**: User asks to "review code" or "review my changes" and expects impact, language/framework conventions, security, performance, and architecture in one pass.
- **Pre-PR or pre-commit**: Run the full pipeline (diff + stack + cognitive) and get one report.
- **Consistent pipeline**: Same execution order every time so Cursor or an agent can simulate skill chaining by following this skill's instructions.

**When to use**: When the user wants a **combined** review across scope, stack (language/framework/library), and cognitive dimensions. When the user wants only one dimension (e.g. "review my diff" or "security review"), use the atomic skill instead.

---

## Behavior

### Orchestration only

- **Do not** analyze code yourself. **Do** invoke (or simulate invoking) the following skills **in order**, then aggregate their findings.
- Execution order is fixed so that Cursor or an agent can follow it step by step.

### Interaction policy

- **Prefer defaults and choices**: Use the defaults in the table below; present options for the user to **confirm or select** (e.g. [diff] [codebase], [Repo root] [Current dir]), and avoid asking for free-text input when a default exists.
- **Scope (diff vs codebase)**: If the user has **not** explicitly indicated (a) diff/current change (e.g. "my changes", "the diff", "what I changed") or (b) codebase/path (e.g. "this directory", "src/foo", "the repo"), **ask the user to choose**. In particular, if they said only "review", "review code", or "code review" with no scope cue, **do not assume** — offer: *Review current change (diff)* [default] *or codebase (given path(s))?* and wait for their choice before running any review skill.
- If language/framework is not explicit and cannot be inferred from the files in scope, **offer choices** ([.NET] [Java] [Go] [PHP] [PowerShell] [SQL] [Vue] [Skip]); if still unclear, skip and **note the skip** in the final summary.
- Always state which steps were executed and which were skipped (with reason).

### Defaults (prefer confirm or choose; avoid asking for free-text input)

| Item | Default | When to deviate |
| :--- | :--- | :--- |
| **Scope** | **diff** (current change) | User chooses "codebase" to review given path(s) instead. |
| **Scope = diff — untracked** | **Include** untracked files in change set | User can choose "diff only, no untracked." |
| **Scope = codebase — path(s)** | **Repo root** | User chooses one or more paths (offer: repo root / current file’s dir / list top-level dirs to pick). |
| **Scope = codebase — large** | **By layer** (output by module/dir; no single shallow pass) | User can choose a **priority subset** (e.g. one layer or named modules). |
| **Language / framework** | **Infer from files in scope** | If unclear, offer choices: [.NET] [Java] [Go] [PHP] [PowerShell] [SQL] [Vue] [Skip]; do not ask user to type. |

### Pre-flight: confirm before running

**Resolve the following with the user once, before executing any review step.** Prefer **confirm default** or **select from options**; avoid asking for free-text input when a default exists.

| Item | If unclear | Action |
| :--- | :--- | :--- |
| **Scope** | User did not say "my changes"/"diff" vs "codebase"/path (e.g. "review" or "review code" alone = unclear) | **Must ask.** Offer: *Review current change (diff)* [default] *or codebase (given path(s))?* — user chooses; do not assume. |
| **Scope = diff** | — | Confirm: *Include untracked files?* Default **Yes**. Ensure diff + untracked content available for review-diff. |
| **Scope = codebase** | Path(s) not stated | Offer: *Review repo root?* [default] *Or pick path(s): [repo root] [current file’s dir] [list top-level dirs]* — user selects, no typing. |
| **Scope = codebase, large** | Whole repo or very large dir | Default: output **by layer** (module/dir). Option: *Narrow to a priority subset?* — user can choose from listed dirs/modules. |
| **Language / framework** | Cannot infer from files | Offer: *[.NET] [Java] [Go] [PHP] [PowerShell] [SQL] [Vue] [Skip]* — user picks one; if Skip or none match, skip and note in summary. |

After pre-flight, run the pipeline without further scope questions; report which steps ran and which were skipped.

### Execution order

When performing this skill, **sequentially apply** the following steps. For each step, load and run the corresponding skill's instructions, collect its findings (in the standard format: Location, Category, Severity, Title, Description, Suggestion), then proceed to the next step.

1. **Scope**  
   Choose **one** based on user intent:
   - **review-diff**: Use when the user wants only the **current change** (git diff, staged + unstaged) reviewed. Load [review-diff](../review-diff/SKILL.md) and run it on the diff.
   - **review-codebase**: Use when the user wants the **current state** of given path(s), directory(ies), or repo reviewed. Load [review-codebase](../review-codebase/SKILL.md) and run it on the specified scope.
   Run the chosen scope skill; collect all findings.

2. **Language**  
   Choose **one or none** based on the project's primary language in scope:
   - **review-dotnet**: .NET (C#/F#). Load [review-dotnet](../review-dotnet/SKILL.md).
   - **review-java**: Java. Load [review-java](../review-java/SKILL.md).
   - **review-go**: Go. Load [review-go](../review-go/SKILL.md).
   - **review-php**: PHP. Load [review-php](../review-php/SKILL.md).
   - **review-powershell**: PowerShell (`.ps1`, `.psm1`, `.psd1`). Load [review-powershell](../review-powershell/SKILL.md).
   - **review-sql**: SQL or query-heavy code. Load [review-sql](../review-sql/SKILL.md).
   If none match, skip this step. Run the chosen language skill on the same scope; collect all findings.

3. **Framework (optional)**  
   If the project uses a known framework in scope, choose the matching skill:
   - **review-vue**: Vue 3. Load [review-vue](../review-vue/SKILL.md).
   - *(Reserved for future: review-aspnetcore, review-react, etc.)*
   If none match, skip. Run the chosen framework skill; collect all findings.

4. **Library (optional)**  
   If the project heavily uses a key library with a dedicated review skill, run it (e.g. *review-entityframework* when available). Otherwise skip. Collect all findings.

5. **Cognitive**  
   Run **in order**:
   - [review-security](../review-security/SKILL.md): security findings.
   - [review-performance](../review-performance/SKILL.md): performance findings.
   - [review-architecture](../review-architecture/SKILL.md): architecture findings.
   - [review-testing](../review-testing/SKILL.md): testing findings (existence, coverage, quality, edge cases).
   *(Reserved for future: review-reliability, review-maintainability.)*  
   Collect all findings.

6. **Aggregation**  
   Merge all collected findings into **one report**. Group by **Category** (`scope`, `language-*`, `framework-*`, `library-*`, `cognitive-*`) or by **file/location**, as best fits the report length. Use the same finding format (Location, Category, Severity, Title, Description, Suggestion). Add a short summary (e.g. counts by severity or category) at the top if useful.  
   **De-dup rule**: If multiple findings share the same **Location + Title** and represent the same issue across steps, keep the highest severity and note the other step(s) in the Description (e.g. "Also flagged by language and security").

7. **Risk signal aggregation (final stage only)**  
   Derive risk signals from the **deduplicated final findings** and from explicit change context (e.g. files or paths), not from any single atomic skill in isolation. Keep this mapping centralized in the orchestrator to avoid inconsistent or duplicated risk labels across skills.
   - Emit a compact `risk_signals` list with unique signal names.
   - Optionally include `risk_confidence` per signal (0.0-1.0).
   - If no clear signals exist, emit an empty list (`[]`), not guessed risks.

### Summary for Cursor/Agent

- **When performing this skill, sequentially apply:**
  1. review-diff **or** review-codebase (scope)
  2. review-dotnet **or** review-java **or** review-go **or** review-php **or** review-powershell **or** review-sql (language, optional)
  3. review-vue or other framework skill (optional)
  4. Library skill (optional, when available)
  5. review-security, then review-performance, then review-architecture, then review-testing (cognitive)
  6. aggregate and deduplicate findings into one report
  7. derive final `risk_signals` (and optional `risk_confidence`) from the final findings + change context
- **Aggregate all findings into a single report** using the standard findings format, then emit risk signals at final stage. Do not analyze code in this skill; only orchestrate and aggregate.

---

## Input & Output

### Input

- **User intent**: What to review (e.g. "my changes" → scope = diff; "this directory" → scope = codebase) and optionally project type (e.g. .NET, Java, Vue) to select language/framework.
- **Code scope**: Diff or paths, as provided by the user when invoking the skill.

### Output

- **Single aggregated report** containing all findings from the steps above, in the standard format (Location, Category, Severity, Title, Description, Suggestion), grouped by category or location, with optional summary.
- **Optional risk summary** derived at aggregation stage: `risk_signals` (and optional confidence), based on final deduplicated findings and change context.

---

## Restrictions

### Hard Boundaries

- **Do not** perform any code analysis inside this skill. Only orchestrate other skills and aggregate.
- **Do not** change the execution order; keep scope → language → framework → library → cognitive.
- **Do not** invent findings; only include findings produced by the atomic skills you run.
- **Do not** require each atomic skill to emit risk signals. Risk labels are orchestrator-owned and generated only at final aggregation.

### Skill Boundaries

**Do NOT do these (other skills handle them):**

- Direct code analysis or linting — use the atomic review skills (`review-diff`, `review-codebase`, `review-security`, etc.)
- Single-dimension reviews — invoke `review-diff`, `review-security`, `review-performance`, or other atomic skills directly
- Implementing fixes or refactoring code — use development/refactoring skills
- Writing or modifying tests — use testing skills or `run-automated-tests`

**When to stop and hand off:**

- When aggregated report is complete → hand off to user for review or to development workflow
- When user asks for only a specific dimension (e.g. "security review") → hand off to the corresponding atomic skill
- When findings need to be acted upon → hand off to implementation or `run-repair-loop` skill

---

## Self-Check

### Core Success Criteria

- [ ] Scope confirmed: User's review scope (diff or codebase paths) is confirmed before execution
- [ ] Execution order followed: Skills run in fixed sequence (scope → language → framework → library → cognitive)
- [ ] All applicable skills executed: Scope skill + language skill (if applicable) + framework skill (if applicable) + all cognitive skills are run
- [ ] Findings aggregated: All findings from atomic skills are collected and merged into a single report using standard format
- [ ] Findings deduplicated: Duplicate findings (same Location + Title) are merged, keeping highest severity
- [ ] Risk signals derived: Risk signals are generated from final deduplicated findings and change context (not from individual skills)

### Acceptance Test

- [ ] Does the final report contain findings from all executed atomic skills, with no duplicates, and risk signals derived only at the aggregation stage?

---

## Examples

### Example 1: Diff review for .NET project

- **Input**: User says "review my code" and provides a git diff; project is C#.
- **Expected**: Run review-diff → review-dotnet → review-security → review-performance → review-architecture → review-testing (skip framework/library if not Vue or other); aggregate all findings into one report with categories `scope`, `language-dotnet`, `cognitive-security`, `cognitive-performance`, `cognitive-architecture`, `cognitive-testing`.

### Example 2: Codebase review for Vue frontend

- **Input**: User says "review src/frontend" and project uses Vue 3.
- **Expected**: Run review-codebase on src/frontend → review-vue → review-security → review-performance → review-architecture → review-testing; aggregate into one report.

### Edge case: No language match

- **Input**: Project is Rust or another language with no atomic skill yet.
- **Expected**: Run scope (review-diff or review-codebase) → skip language and framework → run review-security, review-performance, review-architecture, and review-testing; aggregate. Report should note that language/framework review was skipped (no matching skill).

### Example 3: Diff review for PowerShell scripts

- **Input**: User asks to review changed `.ps1` files in the current diff.
- **Expected**: Run review-diff → review-powershell → review-security → review-performance → review-architecture → review-testing; aggregate findings and categorize PowerShell issues as `language-powershell`.

---

## Appendix: Output contract

The aggregated report MUST use the same finding format as the atomic skills:

| Element | Requirement |
| :--- | :--- |
| **Location** | `path/to/file.ext` (optional line or range). |
| **Category** | `scope`, `language-*`, `framework-*`, `library-*`, `cognitive-*` (including `cognitive-testing`) |
| **Severity** | `critical`, `major`, `minor`, `suggestion`. |
| **Title** | Short one-line summary. |
| **Description** | 1–3 sentences. |
| **Suggestion** | Concrete fix or improvement (optional). |
| **Risk Signals** | Optional `risk_signals: string[]`; values MUST come from the mapping in `Appendix: Risk signal mapping (aggregator-owned)`. Use `[]` when no clear signal exists. |
| **Risk Confidence** | Optional `risk_confidence: { [signal: string]: number }`; keys MUST be a subset of `risk_signals`, values MUST be in `[0.0, 1.0]`. |

Group findings by Category or by Location. Optionally include a summary table (e.g. count by severity or by category) at the top of the report.

## Appendix: Risk signal mapping (aggregator-owned)

When emitting risk signals, apply this centralized mapping from final findings/change context:

| Signal | Trigger heuristic (examples) |
| :--- | :--- |
| `auth_change` | Findings mention authentication flow, token/session handling, login logic, SSO/OAuth, or auth middleware changes. |
| `permission_change` | Findings mention authorization checks, ACL/RBAC policy changes, IDOR risk, or role/permission matrix updates. |
| `data_loss` | Findings indicate destructive data operations, irreversible mutation, unsafe deletes/truncates, migration rollback gaps, or idempotency breakage with loss risk. |
| `backward_incompatible` | Findings indicate API/contract/schema behavior breaks without versioning/deprecation handling. |
| `config_change` | Findings reference behavior-critical config/default changes (timeouts, feature flags, env settings, runtime knobs). |
| `external_api_change` | Findings indicate changed upstream/downstream API contract, request/response shape, webhook/event format, or client SDK expectations. |
| `sql_migration` | Findings involve DDL/index/constraint migration scripts or schema-evolution risk in SQL change sets. |
| `ci_script_change` | Findings touch CI/CD workflow, build/release scripts, deployment automation, or test-gating scripts. |
| `crypto_security` | Findings mention encryption/hashing/signature/key-management issues or crypto algorithm changes. |
| `performance_regression` | Findings from `language-*`, `framework-*`, `language-sql`, or `cognitive-performance` indicate measurable latency/throughput/memory regression risk. |

Notes:

- Use evidence-first mapping; do not infer a signal without at least one supporting finding or explicit changed artifact.
- Emit each signal once; keep list stable and deduplicated.
