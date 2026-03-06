---
name: refine-skill-design
description: Audit and refactor existing SKILLs to meet spec compliance and LLM best practices. Use when improving drafts, fixing quality, or aligning to spec.
tags: [writing, eng-standards, meta-skill, optimization]
related_skills: [decontextualize-text, generate-standard-readme]
version: 1.3.0
license: MIT
recommended_scope: user
metadata:
  author: ai-cortex
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
- Generating project documentation (use `bootstrap-project-documentation`)

**Handoff point**: When SKILL is refined and diff summary provided, hand off to user for review and version control commit.

---

## Use Cases

- **New skill onboarding**: Expert review after an Agent has generated a new Skill draft.
- **Quality fixes**: When a Skill behaves inconsistently on newer models, align logic and strengthen examples.
- **Consistency audit**: Check that a new Skill matches the tagging system and naming in `INDEX.md`.
- **Upgrade**: Turn a simple "formatting tool" into a full Agent capability with interaction policy and error handling.

**Scope**: This skill is for **auditing and refactoring existing SKILLs**, not creating from scratch. For learning how to create new skills, plan scripts/references/assets, or run init/package scripts, use skills.sh's `skill-creator` (e.g. anthropics/skills).

---

## Behavior

### Meta-audit model

1. **Intent**: Is Purpose specific enough? Avoid vague terms like "Helper," "Utilities."
2. **Logic**: Does Input → Behavior → Output form a clear chain?
3. **Constraints**: Do Restrictions cover the most common failure modes in the domain?
4. **Examples**: Do Examples progress from simple to complex and include at least one edge case?

### Optimization flow

1. **Structure**: Apply the standard template (YAML, Purpose, Use cases, Behavior, I/O, Restrictions, Self-Check, Examples).
2. **Verbs**: Use precise, unambiguous verbs (e.g. "handle" → "parse," "transform," "trim").
3. **Interaction**: For complex logic, add "confirm before proceed" or "choose among options."
4. **Metadata**: Align tags with `INDEX.md` and suggest a sensible SemVer version.

---

## Input & Output

### Input

- A SKILL Markdown document to optimize, or a rough draft.

### Output

- **Optimized SKILL**: Production-grade Markdown that satisfies the spec.
- **Diff summary**: What was changed and why.
- **Version suggestion**: SemVer recommendation.

### Output Persistence (Document Handling)

**Rule**: Do not modify the original SKILL or any prior refinement output. Choose one strategy per run:

| Strategy | Path pattern | Behavior |
| :--- | :--- | :--- |
| **Fixed temp** (default) | `skills/<skill-name>/SKILL.refined.md` | Overwrite this single temp file each run; never touch original `SKILL.md` or prior outputs |
| **New per run** | `skills/<skill-name>/SKILL.refined.YYYYMMDD.md` | Create a new file each run; never overwrite previous refinements |

User override: If user specifies a path or strategy, honor it. Otherwise use **fixed temp**.

---

## Restrictions

### Hard Boundaries

- **Do not modify original or prior outputs**: Write only to the configured output path (fixed temp or new-per-run); never overwrite the source `SKILL.md` or previous refinement files.
- **Do not change intent**: Optimization must preserve the skill's core purpose.
- **Minimize prose**: Prefer lists and tables over long README-style text.
- **Multiple examples**: Do not keep only one "happy path" example; include at least one challenging or edge-case example.

### Skill Boundaries (Avoid Overlap)

**Do NOT do these (other skills handle them)**:

- **Creating new skills from scratch**: Generating initial SKILL structure and content → Use `skill-creator` (anthropics/skills)
- **Quality metrics evaluation**: Calculating ASQM scores, detecting overlaps → Use `curate-skills`
- **Skill discovery**: Finding skills in repositories, cataloging capabilities → Use `discover-skills`
- **Project documentation**: Generating README, AGENTS.md, or project-level docs → Use `bootstrap-project-documentation` or `generate-standard-readme`
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
> ---
> # Skill: Spelling and terminology
> ## Purpose: Identify and fix low-level spelling errors and terminology inconsistency without changing the author's intent or tone.
> ## Behavior:
> 1. Detect language.
> 2. Build a term list if the text is long.
> 3. Distinguish "typos" from "intentional style."
> ## Restrictions: Do not change proper nouns or specific abbreviations unless clearly wrong.

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
