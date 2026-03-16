---
name: refine-skill-design
description: Audit and refactor existing SKILLs to meet spec compliance and LLM best practices. Use when improving drafts, fixing quality, or aligning to spec.
tags: [writing, eng-standards, meta-skill, optimization]
related_skills: [decontextualize-text, generate-standard-readme]
version: 1.4.0
license: MIT
recommended_scope: user
metadata:
  author: ai-cortex
triggers: [refine skill, skill design]
input_schema:
  type: document-artifact
  description: Existing SKILL.md file to audit and refactor
output_schema:
  type: document-artifact
  description: Optimized SKILL written to fixed temp (SKILL.refined.md) or new-per-run path; diff summary (Section/Change/Reason) and version suggestion
---

# Skill: Refine Skill Design

## Purpose

As a "Skill for Skills," this skill **audits and refactors** AI capability definitions in draft form. It applies a senior prompt-engineering perspective to improve logic robustness, scenario coverage, and instruction adherence so each capability meets LLM best practices.

---

## Core Objective

**Primary Goal**: Produce an audited and refactored SKILL document that meets spec compliance and LLM best practices.

**Success Criteria** (ALL must be met):

1. ✅ **Structure compliant**: SKILL follows standard template (YAML, Purpose, Use Cases, Behavior, Input & Output, Restrictions, Self-Check, Examples)
2. ✅ **Logic clarity**: Input → Behavior → Output chain is clear and unambiguous
3. ✅ **Constraints defined**: Restrictions section covers common failure modes in the domain
4. ✅ **Examples comprehensive**: At least 2 examples provided, including one edge case or challenging scenario
5. ✅ **Changes documented**: Diff summary lists all changes with sections, descriptions, and reasons
6. ✅ **Version suggested**: SemVer recommendation provided with rationale

**Acceptance Test**: Can an AI agent apply this refined SKILL consistently across different contexts without ambiguity?

---

## Scope Boundaries

**This skill handles**:

- Auditing existing SKILL drafts for quality and compliance
- Refactoring SKILL structure and content to meet spec
- Improving logic clarity and instruction precision
- Adding missing sections or strengthening weak areas
- Providing diff summary and version recommendations

**This skill does NOT handle**:

- Creating new skills from scratch (use `skill-creator` from anthropics/skills)
- Running package scripts or init workflows (use skills.sh tooling)
- Planning skill assets or references (use skills.sh documentation)
- Evaluating skill quality metrics (use `curate-skills`)
- Discovering or cataloging skills (use `discover-skills`)
- Generating project documentation (use `bootstrap-docs`)

**Handoff point**: When SKILL is refined and diff summary provided, hand off to user for review and version control commit.

---

## Use Cases

- **New skill onboarding**: Expert review after an Agent has generated a new Skill draft.
- **Quality fixes**: When a Skill behaves inconsistently on newer models, align logic and strengthen examples.
- **Consistency audit**: Check that a new Skill matches the tagging system and naming in `INDEX.md`; consider adding to `skills/scenario-map.json` if the skill should be discoverable by scenario (per spec Metadata Sync).
- **Upgrade**: Turn a simple "formatting tool" into a full Agent capability with interaction policy and error handling.

**Scope**: This skill is for **auditing and refactoring existing SKILLs**, not creating from scratch. For learning how to create new skills, plan scripts/references/assets, or run init/package scripts, use skills.sh's `skill-creator` (e.g. anthropics/skills).

---

## Behavior

### Meta-audit model

1. **Intent**: Is Purpose specific enough? Avoid vague terms like "Helper," "Utilities."
2. **Logic**: Does Input → Behavior → Output form a clear chain?
3. **Constraints**: Do Restrictions cover the most common failure modes in the domain?
4. **Examples**: Do Examples progress from simple to complex and include at least one edge case?
5. **Interaction Policy** (spec §4.3): Does Behavior state defaults, choice options, and which items require user confirmation? Prefer Defaults first, Prefer choices, Context inference.
6. **Triggers** (optional): For high-discoverability skills, consider adding `triggers` (3–5 English phrases) in frontmatter for quick invocation matching.

### Optimization flow

1. **Structure**: Apply the standard template (YAML, Purpose, Use cases, Behavior, I/O, Restrictions, Self-Check, Examples).
2. **Verbs**: Use precise, unambiguous verbs (e.g. "handle" → "parse," "transform," "trim").
3. **Interaction**: For complex logic, add "confirm before proceed" or "choose among options." Align with spec Interaction Policy (defaults first, prefer choices).
4. **Metadata**: Align tags with `INDEX.md`; suggest `triggers` for high-discoverability skills; suggest sensible SemVer; remind that new skills may need `scenario-map.json` for scenario-based discovery.
5. **Apply changes**: Unless the user explicitly asks for a dry‑run / temp refinement file, write the refined content **directly回写到源 `SKILL.md`**，并在输出中同时附上 diff 摘要与版本号建议，方便审阅和审计。

---

## Input & Output

### Input

- A SKILL Markdown document to optimize, or a rough draft.

### Output

- **Optimized SKILL**: Production-grade Markdown that satisfies the spec.
- **Diff summary**: What was changed and why.
- **Version suggestion**: SemVer recommendation.

### Output Persistence (Document Handling)

**Rule**: 默认直接改进并覆盖原始 `SKILL.md`，同时提供可审计的 diff 摘要与版本号建议；只有在用户明确要求“只生成 refinement 草稿、不改源文件”时，才写入临时或新建 refinement 文件。每次运行须在以下策略中二选一：

| Strategy | Path pattern | Behavior |
| :--- | :--- | :--- |
| **Direct overwrite** (default) | `skills/<skill-name>/SKILL.md` | 直接覆盖源文件，保证 front matter `version` 已更新，且在输出中包含变更摘要，便于审计 |
| **Fixed temp** (opt‑out) | `skills/<skill-name>/SKILL.refined.md` | 在用户要求“不要改原文件，只给 refinement”时使用；每次运行覆盖同一临时文件 |
| **New per run** (opt‑out) | `skills/<skill-name>/SKILL.refined.YYYYMMDD.md` | 在用户要求“为这次 refinement 保留单独文件”时使用；每次运行创建新的 refinement 文件 |

User override: If user specifies a path or strategy, honor it. Otherwise use **Direct overwrite**。

---

## Restrictions

### Hard Boundaries

- **默认覆盖但必须可审计**：默认策略是直接覆盖源 `SKILL.md`，但必须同步更新 front matter `version`，并在输出中提供完整变更摘要，确保可审计。
- **尊重显式“草稿模式”请求**：若用户明确要求“不要改原文件”“只生成 refinement 草稿”等，则不得覆盖源 `SKILL.md`，仅写入临时或新建 refinement 文件。
- **Do not change intent**: Optimization must preserve the skill's core purpose.
- **Minimize prose**: Prefer lists and tables over long README-style text.
- **Multiple examples**: Do not keep only one "happy path" example; include at least one challenging or edge-case example.

### Skill Boundaries (Avoid Overlap)

**Do NOT do these (other skills handle them)**:

- **Creating new skills from scratch**: Generating initial SKILL structure and content → Use `skill-creator` (anthropics/skills)
- **Quality metrics evaluation**: Calculating ASQM scores, detecting overlaps → Use `curate-skills`
- **Skill discovery**: Finding skills in repositories, cataloging capabilities → Use `discover-skills`
- **Project documentation**: Generating README, AGENTS.md, or project-level docs → Use `bootstrap-docs` or `generate-standard-readme`
- **Text decontextualization**: Removing PII or sensitive information → Use `decontextualize-text`

**When to stop and hand off**:

- User says "looks good", "approved", "commit this" → Refinement complete, hand off to user for version control
- User asks "how do I create a new skill?" → Hand off to `skill-creator` documentation
- User asks "what's the quality score?" → Hand off to `curate-skills`
- User asks "what skills are available?" → Hand off to `discover-skills`

---

## Self-Check

### Core Success Criteria (ALL must be met)

- [ ] **Structure compliant**: SKILL follows standard template (YAML, Purpose, Use Cases, Behavior, Input & Output, Restrictions, Self-Check, Examples)
- [ ] **Logic clarity**: Input → Behavior → Output chain is clear and unambiguous
- [ ] **Constraints defined**: Restrictions section covers common failure modes in the domain
- [ ] **Examples comprehensive**: At least 2 examples provided, including one edge case or challenging scenario
- [ ] **Changes documented**: Diff summary lists all changes with sections, descriptions, and reasons
- [ ] **Version suggested**: SemVer recommendation provided with rationale

### Process Quality Checks

- [ ] **Self-apply**: Could this skill successfully refine itself?
- [ ] **Clarity**: Could an Agent without domain background reproduce results from Behavior?
- [ ] **Compliance**: Are all required sections and metadata fields present?
- [ ] **Intent preserved**: Does the refined SKILL maintain the original skill's core purpose?
- [ ] **Precision**: Are verbs specific and unambiguous (not vague terms like "handle")?
- [ ] **Interaction Policy** (spec §4.3): Does Behavior have Defaults or choice-based interaction where applicable?
- [ ] **Triggers** (optional): For high-discoverability skills, are `triggers` suggested?

### Acceptance Test

**Can an AI agent apply this refined SKILL consistently across different contexts without ambiguity?**

If NO: SKILL needs further refinement. Review Behavior section for clarity and add more specific instructions.

If YES: Refinement is complete. Provide diff summary and version recommendation to user.

---

## Examples

### Before

> name: spell-check
> This skill checks spelling.
> Input: multilingual text.
> Output: corrected text.

### After

> name: polish-text-spelling
> description: Context-aware spelling and terminology correction for multilingual documents.
> tags: [writing, quality-control]
> version: 1.1.0
>
> ---
>
> **Skill: Spelling and terminology**
>
> **Purpose**: Identify and fix low-level spelling errors and terminology inconsistency without changing the author's intent or tone
>
> **Behavior**
>
> 1. Detect language.
> 2. Build a term list if the text is long.
> 3. Distinguish "typos" from "intentional style."
>
> **Restrictions**: Do not change proper nouns or specific abbreviations unless clearly wrong

### Example 2: Edge case — ambiguous draft

- **Input**: A Skill draft whose Purpose is "help users handle files," with no Use Cases or Restrictions.
- **Expected**: Pin down intent (replace "handle" with concrete verbs: parse, convert, merge, etc.); add Use Cases and Restrictions (e.g. do not overwrite source; do not modify binaries); add at least one edge example (e.g. empty file, very large file, permission denied).

---

## Appendix: Output contract

When this skill produces a refinement, the output MUST satisfy this contract so that Agents and downstream tools can consume it consistently:

| Element | Requirement |
| :--- | :--- |
| **Output path** | Fixed temp `skills/<skill-name>/SKILL.refined.md` (default, overwrite each run) OR new-per-run `skills/<skill-name>/SKILL.refined.YYYYMMDD.md`. Never modify original `SKILL.md` or prior refinement files. |
| **Optimized SKILL** | Full Markdown content (or path to file). MUST satisfy [spec/skill.md](../../spec/skill.md): YAML front matter, Purpose, Use cases, Behavior, I/O, Restrictions, Self-Check, and at least one Example. |
| **Diff summary** | List of changes. Each entry MUST include **Section** (e.g. `Purpose`, `Behavior`, `metadata`), **Change** (short description of what was changed), and **Reason** (why the change was made). |
| **Version suggestion** | SemVer string `major.minor.patch`. Optionally **Rationale** (e.g. `minor: added Restrictions`). |
