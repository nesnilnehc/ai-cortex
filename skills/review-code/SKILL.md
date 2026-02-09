---
name: review-code
description: Orchestrator that runs scope then language then framework then library then cognitive review skills in order and aggregates all findings into one report. Does not perform analysis itself.
tags: [eng-standards]
related_skills: [review-diff, review-codebase, review-dotnet, review-java, review-sql, review-vue, review-security, review-architecture]
version: 2.1.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
---

# Skill: Review Code (Orchestrator)

## Purpose

**This skill does not perform code analysis itself.** It is a **meta skill** that orchestrates other atomic review skills in a fixed order, then **aggregates** their findings into a single report. Use it when the user asks for a full "review code" or "code review" and you want to apply scope → language → framework → library → cognitive skills and produce one combined output. For a single-dimension review (e.g. only diff or only security), invoke the corresponding atomic skill directly ([review-diff](../review-diff/SKILL.md), [review-security](../review-security/SKILL.md), etc.).

---

## Use Cases

- **Full code review**: User asks to "review code" or "review my changes" and expects impact, language/framework conventions, security, and architecture in one pass.
- **Pre-PR or pre-commit**: Run the full pipeline (diff + stack + cognitive) and get one report.
- **Consistent pipeline**: Same execution order every time so Cursor or an agent can simulate skill chaining by following this skill's instructions.

**When to use**: When the user wants a **combined** review across scope, stack (language/framework/library), and cognitive dimensions. When the user wants only one dimension (e.g. "review my diff" or "security review"), use the atomic skill instead.

---

## Behavior

### Orchestration only

- **Do not** analyze code yourself. **Do** invoke (or simulate invoking) the following skills **in order**, then aggregate their findings.
- Execution order is fixed so that Cursor or an agent can follow it step by step.

### Interaction policy

- If the scope is not explicit (diff vs codebase), **ask the user** to choose before running any review skill.
- If language/framework is not explicit and cannot be inferred from the files in scope, **ask once**; if still unclear, skip that step and **note the skip** in the final summary.
- Always state which steps were executed and which were skipped (with reason).

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
   - [review-architecture](../review-architecture/SKILL.md): architecture findings.
   *(Reserved for future: review-reliability, review-maintainability.)*  
   Collect all findings.

6. **Aggregation**  
   Merge all collected findings into **one report**. Group by **Category** (`scope`, `language-*`, `framework-*`, `library-*`, `cognitive-*`) or by **file/location**, as best fits the report length. Use the same finding format (Location, Category, Severity, Title, Description, Suggestion). Add a short summary (e.g. counts by severity or category) at the top if useful.  
   **De-dup rule**: If multiple findings share the same **Location + Title** and represent the same issue across steps, keep the highest severity and note the other step(s) in the Description (e.g. "Also flagged by language and security").

### Summary for Cursor/Agent

- **When performing this skill, sequentially apply:**
  1. review-diff **or** review-codebase (scope)
  2. review-dotnet **or** review-java **or** review-sql (language, optional)
  3. review-vue or other framework skill (optional)
  4. Library skill (optional, when available)
  5. review-security, then review-architecture (cognitive)
- **Aggregate all findings into a single report** using the standard findings format. Do not analyze code in this skill; only orchestrate and aggregate.

---

## Input & Output

### Input

- **User intent**: What to review (e.g. "my changes" → scope = diff; "this directory" → scope = codebase) and optionally project type (e.g. .NET, Java, Vue) to select language/framework.
- **Code scope**: Diff or paths, as provided by the user when invoking the skill.

### Output

- **Single aggregated report** containing all findings from the steps above, in the standard format (Location, Category, Severity, Title, Description, Suggestion), grouped by category or location, with optional summary.

---

## Restrictions

- **Do not** perform any code analysis inside this skill. Only orchestrate other skills and aggregate.
- **Do not** change the execution order; keep scope → language → framework → library → cognitive.
- **Do not** invent findings; only include findings produced by the atomic skills you run.

---

## Self-Check

- [ ] Was the execution order followed (scope → language → framework → library → cognitive)?
- [ ] Were findings only collected from the atomic skills, not invented?
- [ ] Is the output a single report with all findings in the standard format?
- [ ] Did this skill refrain from analyzing code directly?

---

## Examples

### Example 1: Diff review for .NET project

- **Input**: User says "review my code" and provides a git diff; project is C#.
- **Expected**: Run review-diff → review-dotnet → review-security → review-architecture (skip framework/library if not Vue or other); aggregate all findings into one report with categories `scope`, `language-dotnet`, `cognitive-security`, `cognitive-architecture`.

### Example 2: Codebase review for Vue frontend

- **Input**: User says "review src/frontend" and project uses Vue 3.
- **Expected**: Run review-codebase on src/frontend → review-vue → review-security → review-architecture; aggregate into one report.

### Edge case: No language match

- **Input**: Project is Rust or another language with no atomic skill yet.
- **Expected**: Run scope (review-diff or review-codebase) → skip language and framework → run review-security and review-architecture; aggregate. Report should note that language/framework review was skipped (no matching skill).

---

## Appendix: Output contract

The aggregated report MUST use the same finding format as the atomic skills:

| Element | Requirement |
| :--- | :--- |
| **Location** | `path/to/file.ext` (optional line or range). |
| **Category** | `scope`, `language-*`, `framework-*`, `library-*`, `cognitive-*` |
| **Severity** | `critical`, `major`, `minor`, `suggestion`. |
| **Title** | Short one-line summary. |
| **Description** | 1–3 sentences. |
| **Suggestion** | Concrete fix or improvement (optional). |

Group findings by Category or by Location. Optionally include a summary table (e.g. count by severity or by category) at the top of the report.
