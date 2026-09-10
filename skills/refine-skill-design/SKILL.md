---
name: refine-skill-design
description: Audit and refactor existing SKILLs to meet spec compliance, repository asset boundaries, tool adaptation requirements, and LLM best practices.
description_zh: 审计并重构既有 SKILL，使其符合规范、仓库资产边界、工具适配要求与 LLM 最佳实践。
tags: [writing, meta-skill, optimization]
version: 1.6.1
license: MIT
recommended_scope: user
metadata:
  author: ai-cortex
triggers: [refine skill, skill design, audit skill, skill refactor, skill compliance]
input_schema:
  type: document-artifact
  description: Existing SKILL.md file to audit and refactor
output_schema:
  type: document-artifact
  description: Optimized SKILL written to source SKILL.md (default) or to temp/new path when user opts out; includes diff summary and version suggestion
---

# Skill: Refine Skill Design

## Purpose

As a "meta-skill", this skill **reviews and refactors** AI capability definitions that are still in draft form. It applies an advanced prompt-engineering lens to raise logical robustness, scenario coverage, and instruction adherence, so that every capability meets LLM best practices.

---

## Core Objective

**Primary goal**: produce a reviewed and refactored skill document that meets spec compliance, the repository's asset boundaries, and LLM best practices.

**Success criteria** (all must be met):

1. ✅ **Structurally compatible**: the skill follows the standard template (YAML, purpose, use cases, behavior, input and output, restrictions, self-check, examples)
2. ✅ **Logic is clear**: the input → behavior → output chain is clear and unambiguous
3. ✅ **Constraints defined**: the restrictions section covers the failure modes common to the domain
4. ✅ **Asset boundaries clear**: the Skill embeds no authoritative definition that belongs to a Spec / Protocol / Rule; where needed it references one instead, or proposes a split
5. ✅ **Execution adaptation explicit**: external tools, MCP tools, the runtime environment, and missing capabilities all have a discovery, mapping, and failure-handling path
6. ✅ **Repository contract compliant**: obeys `AGENTS.md`, the terminology definitions, and the external-link, language, and asset-priority rules
7. ✅ **Examples are thorough**: at least 2 examples, one of them an edge case or a challenging scenario
8. ✅ **Changes recorded**: the diff summary lists every change together with its section, description, and reason
9. ✅ **Version proposed**: a SemVer proposal with its rationale

**Acceptance test**: can an AI Agent apply this refined skill consistently across different environments, with no ambiguity?

---

## Scope Boundaries

**This skill does**:

- Review an existing skill draft for quality and compliance
- Refactor the skill's structure and content to meet the spec
- Audit the Skill / Spec / Protocol / Rule boundary, to avoid burying a structural contract, an interaction protocol, or a single-point rule inside a Skill
- Audit the tool adaptation layer, so that discovery, capability mapping, and missing-tool handling for MCP / CLI / API tools are executable
- Audit the repository's local contract, so the optimised Skill obeys `AGENTS.md` and the local terminology definitions
- Raise logical clarity and instruction precision
- Add the missing sections or strengthen the weak areas
- Provide the diff summary and a version proposal

**This skill does not do**:

- Generate the full skeleton of a new Skill from scratch
- Install an external Skill or initialiser at runtime
- Decide, in the maintainer's place, the licence and vendoring scope of an externally derived Skill
- Generate the project docs/ structure (taken on by the AgentFabric runtime or a human)

**Handoff point**: once the SKILL is refined and the diff summary is delivered, hand off to the user for review and a version-control commit.

---

## Use Cases

- **New skill onboarding**: an expert review after an agent has drafted a new skill.
- **Quality repair**: when a skill behaves inconsistently on a new model, adjust the logic and strengthen the examples.
- **Consistency review**: check that a new skill matches the tag system and naming in INDEX.md; make sure `description`, `tags`, and `triggers` are enough to support semantic discovery.
- **Upgrade**: turn a plain "formatter" into a full agent capability with an interaction policy and error handling.

**Scope**: this skill is for **reviewing and refactoring an existing skill**, not for creating one from scratch. A new Skill is handled separately, through the repository contribution process and the agentskills.io spec; an external skill-creator must not be installed at runtime for that purpose.

---

## Behavior

### Meta-Audit Model

1. **Intent**: is the purpose specific enough? Avoid vague terms such as "assistant" or "utility".
2. **Logic**: do input → behavior → output form a clear chain?
3. **Constraints**: do the restrictions cover the most common failure modes in the domain?
4. **Examples**: do the examples run from simple to complex and include at least one edge case?
5. **Interaction policy** (spec §4.3): does the behavior state the defaults, the choice options, and which items need user confirmation? Defaults first, then choices, then context inference.
6. **Asset boundary**: is the Skill defining the structure of a thing (Spec), a multi-party message sequence (Protocol), or an atomic prohibition (Rule)? If so, keep the execution orchestration and turn the authoritative definition into a reference to an existing asset, or name where the split belongs.
7. **Execution adaptation**: does the Skill depend on MCP / CLI / API / an external service? If it does, does it state how to discover the available tools, build the capability mapping, handle a missing tool, and avoid hard-coding a tool name that does not exist?
8. **Repository contract**: when optimising inside the AI Cortex repository, `AGENTS.md`, `docs/architecture/terminology.md`, and `skills/SOURCES.yaml` must be read and applied; external HTTP/HTTPS links must not be fetched by default, and a Skill must not be installed at runtime. A pinned upstream version can be read only where an externally derived copy is maintained and the context explicitly declares `allow_external_fetch=true`.
9. **Triggers** (optional): for a high-discoverability skill, consider putting "triggers" (3-5 English phrases) up front, for fast invocation matching.

### Optimisation Process

1. **Structure**: apply the standard template (YAML, purpose, use cases, behavior, I/O, restrictions, self-check, examples).
2. **Verbs**: use precise, unambiguous verbs (e.g. "process" → "parse", "convert", "trim").
3. **Interaction**: for complex logic, add "confirm before continuing" or "choose an option". Keep it in line with the spec's interaction policy (defaults preferred, then choices).
4. **Boundaries**: demote authoritative structural definitions, message sequences, and atomic rules from the Skill body to references; where the asset does not yet exist, list the suggested new Spec / Protocol / Rule in the diff summary, and do not conjure unrelated assets inside this skill.
5. **Adaptation**: add "discover → map → execute → handle absence" steps for the tool dependencies; a tool name is whatever the current runtime actually exposes, and an example tool name serves only as a capability hint.
6. **Local contract**: check external links, raw URLs, language, asset priority, and the local-path-first policy; on a violation, switch to a local reference or a conditional note.
7. **Metadata**: align the tags with INDEX.md; suggest triggers for a high-discoverability skill; suggest a sensible SemVer.
8. **Apply the changes**: unless the user explicitly asks for a dry run or a temporary refined file, write the refined content **straight back to the source `SKILL.md`**, and attach both the diff summary and the version proposal to the output, so it can be reviewed and audited.

---

## Input & Output

### Input

- A SKILL Markdown document that needs optimising, or a draft.

### Output

- **Optimised skill**: production-grade Markdown that meets the spec.
- **Diff summary**: what changed, and why.
- **Version proposal**: a SemVer recommendation.

### Output Persistence (document handling)

**Rule**: by default, improve and overwrite the original `SKILL.md` in place, together with an auditable diff summary and a version proposal; only when the user explicitly asks for "a refined draft only, leave the source file alone" is a temporary or new refined file written. Every run must pick one of the two strategies below:

| Strategy | Path pattern | Behavior |
| :--- | :--- | :--- |
| **Overwrite in place** (default) | `skills/<skill-name>/SKILL.md` | Overwrite the source file directly, keep the frontmatter `version` updated, and carry the change summary in the output, which is what makes it auditable |
| **Fixed temp file** (opt-out) | `skills/<skill-name>/SKILL.refined.md` | Used when the user asks "do not touch the original, just give me the refinement"; every run overwrites the same temporary file |
| **New file per run** (opt-out) | `skills/<skill-name>/SKILL.refined.YYYYMMDD.md` | Used when the user asks "keep a separate file for this refinement"; every run creates a new refined file |

User override: if the user names a path or a strategy, follow it. Otherwise use **overwrite in place**.

---

## Restrictions

### Hard Boundaries

- **Overwrite by default, but it must stay auditable**: the default strategy overwrites the source `SKILL.md` directly, but the frontmatter `version` must be updated in step and the output carries a complete change summary, which is what keeps it auditable.
- **Respect an explicit "draft mode" request**: where the user explicitly asks "do not modify the original", "only produce a refined draft" or the like, the source `SKILL.md` must not be overwritten; write only to a temporary or new refined file.
- **Do not change the intent**: the optimisation must preserve the skill's core purpose.
- **Do not dress a split suggestion up as done**: if only the Skill's reference changed and no Spec / Protocol / Rule was actually created, the output must say "split suggested" and must not claim the asset already exists.
- **Do not route around the local contract**: in a repository that forbids external fetching by default, an external URL must not be written in as a source that execution depends on; it serves only as a reference source where conditions allow.
- **Write less prose**: prefer lists and tables over long narrative paragraphs.
- **Several examples**: do not keep only one "happy path" example; include at least one challenging or extreme case.

### Skill Boundaries (avoid overlap)

**Do not do these (other skills handle them)**:

- **Create a new skill from scratch**: generating the initial skill structure and content → handled separately through the repository contribution process; an external skill-creator must not be installed ad hoc
- **Project documentation**: generate a README → use `generate-standard-readme`; generate AGENTS.md → use `generate-agent-entry`
- **Decontextualise text**: strip PII or sensitive information → use `decontextualize-text`

**When to stop and hand off**:

- The user says "looks good", "approved", "commit this" → the refinement is done; hand off to the user for version control
- The user asks "how do I create a new skill?" → hand off to the repository contribution guide and the agentskills.io spec

---

## Self-Check

### Core Success Criteria (all must be met)

- [ ] **Structurally compatible**: the skill follows the standard template (YAML, purpose, use cases, behavior, input and output, restrictions, self-check, examples)
- [ ] **Logic is clear**: the input → behavior → output chain is clear and unambiguous
- [ ] **Constraints defined**: the restrictions section covers the failure modes common to the domain
- [ ] **Asset boundaries**: the Skill carries no authoritative definition that belongs to a Spec / Protocol / Rule; any necessary split is stated
- [ ] **Execution adaptation**: external tools and MCP tools have a discovery, capability-mapping, and missing-tool handling path
- [ ] **Repository contract**: `AGENTS.md`, the terminology definitions, and the external-link and language rules are applied
- [ ] **Examples are thorough**: at least 2 examples, one of them an edge case or a challenging scenario
- [ ] **Changes recorded**: the diff summary lists every change together with its section, description, and reason
- [ ] **Version proposed**: a SemVer proposal is given, with its rationale

### Process Quality Checks

- [ ] **Bootstrapping**: can this skill be applied to itself successfully (refine itself)?
- [ ] **Clarity**: can an agent with no domain background reproduce the behavior's result?
- [ ] **Compliance**: are all the required sections and metadata fields present?
- [ ] **Intent preserved**: does the refined skill keep the original skill's core purpose?
- [ ] **Precision**: are the verbs concrete and unambiguous (not a vague term such as "process")?
- [ ] **Interaction policy** (spec §4.3): does the behavior have default-based or choice-based interaction, where that applies?
- [ ] **Triggers** (optional): for a high-discoverability skill, are "triggers" suggested?

### Acceptance Test

**Can an AI Agent apply this refined skill consistently across different environments, with no ambiguity?**

If no: the skill needs further refinement. Go through the "Behavior" section for clarity and add more specific instructions.

If yes: the refinement is done. Give the user the diff summary and the version recommendation.

---

## Examples

### Before

> Name: spell-check
> This skill checks spelling.
> Input: multilingual text.
> Output: the corrected text.

### After

> Name: polish-text-spelling
> Description: context-aware spelling and terminology correction for multilingual documents.
> Tags: [writing, quality-control]
> Version: 1.1.0
>
> ---
>
> **Skill: Spelling and Terminology**
>
> **Purpose**: find and fix low-level spelling errors and terminology inconsistencies without changing the author's intent or tone
>
> **Behavior**
>
> 1. Detect the language.
> 2. If the text is long, build a terminology list.
> 3. Tell a "typo" apart from "deliberate style".
>
> **Restrictions**: do not change proper nouns or specific abbreviations unless they are plainly wrong

### Example 2: Edge case — an ambiguous draft

- **Input**: a skill draft whose purpose is "help users process files", with no use cases and no restrictions.
- **Expected**: pin down the intent (replace "process" with a concrete verb: parse, convert, merge, and so on); add use cases and restrictions (e.g. do not overwrite the source; do not modify binary files); add at least one edge-case example (e.g. an empty file, a very large file, permission denied).
