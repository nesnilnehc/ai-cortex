---
name: generate-agent-entry
description: Write or revise AGENTS.md per embedded output contract to establish project identity, authoritative sources, and behavioral expectations. Use when creating Agent entry for new projects, auditing existing AGENTS.md, or adopting the AI Cortex entry format.
version: 1.1.0
license: MIT
---

# Skill: Generate Agent Entry

## Purpose

Write or revise **AGENTS.md** at the repository root according to the "Output Contract" section below, so that when an agent meets the project it holds an explicit **project identity**, **authoritative sources**, and **behavioural expectations**, and acts consistently and predictably. The output contract is embedded in this SKILL.md, so a single load supplies the whole spec and the steps.

---

## Core Objective

**Primary goal**: produce a compliant AGENTS.md that establishes project identity, authoritative sources, and behavioural expectations for AI agents.

**Success criteria** (all applicable items must be met):

1. ✅ **Authoring only — AGENTS.md exists**: the file is written to the repository root and committed to version control; an audit leaves the file unchanged
2. ✅ **The three core elements are present**: the project identity, authoritative sources, and behavioural expectations sections all exist
3. ✅ **Seven sections complete**: opening, project identity, authoritative sources, behaviour, discovery/loading summary, language/communication, reference table
4. ✅ **Actionable behaviour**: the behavioural expectations pair "must", "should", or "must not" with actionable items
5. ✅ **Reference table complete**: covers the AGENTS.md format source, the entry raw URL and project-specific entry contract where available, usage/installation, and the entry index
6. ✅ **Contract compliance**: the output follows the embedded output contract's structure and content requirements

**Acceptance** test: can an AI agent read this AGENTS.md and learn what the project is, where the authoritative sources are, and how to act when using the project?

---

## Scope Boundaries

**This skill does**:

- Write a new AGENTS.md from scratch
- Revise an existing AGENTS.md into compliance
- Review AGENTS.md against the output contract
- Generate AGENTS.md from the embedded contract spec

**This skill does not do**:

- Write the README (use "generate-standard-readme")
- Bootstrap a full project docs/ structure (taken on by the AgentFabric runtime or a human, per `docs/ARTIFACT_NORMS.md`)
- Refine skill design (use "refine-skill-design")
- Write other document types (out of scope)

**Handoff point**: after authoring, commit AGENTS.md once it passes the self-check; after an audit, return the evidence matrix and revision suggestions without changing the file.

---

## Use Cases

- **New project**: add an Agent entry to a repository that has no AGENTS.md; draft the first version from the output contract's recommended structure and sections.
- **Revise an existing entry**: audit and complete an existing AGENTS.md (add the missing sections, such as authoritative sources, behaviour, reference table) or fix wording that does not match the contract.
- **Adopt the format elsewhere**: another project can use this skill's output contract to generate an AGENTS.md carrying identity, authority, and behaviour, then swap in its own asset types and paths.
- **Compliance check**: review an existing AGENTS.md against the contract (§3 sections, §4 content, §6 reference table) and output the revision suggestions.

---

## Behavior

1. **Read the contract first**: before acting, read this file's "Output Contract" section and treat it as the single source of truth; do not invent sections or drop recommended elements.
2. **Gather verified inputs**: read the repository's README, asset registries and language policy for the one-line positioning, asset types and directories, usage path, and primary description language. Check whether a raw URL is available from the repository remote. Do not infer commands, paths or policies from names alone; ask only when a required fact cannot be established locally.
3. **Generate section by section**: produce or revise AGENTS.md in the order of the contract's §3: opening → project identity → authoritative sources → behavioural expectations → discovery and loading (summary) → language and communication → reference table. Section titles can be adjusted, but keep the order: identity → authority → behaviour → operations summary → language → reference.
4. **Actionable behaviour**: use "must", "should", "must not" (or equivalents) so that every expectation is actionable; each item can cite a spec or a document. Do not paste whole specs or documents into AGENTS.md; index and summarise only.
5. **Complete reference table**: include the AGENTS.md format source, this entry's raw URL (where applicable), the project-specific entry contract (where one exists), usage and installation, and the entry index; use relative paths or resolvable URLs. Mark an unavailable project-specific source `N/A` with a reason instead of inventing it.
6. **Verify item by item**: give each applicable requirement in the Output Contract's §3–§6 its own `PASS`, `FAIL` or `N/A` row with the exact AGENTS.md line or section that supports the verdict. Check substance as well as headings: project identity, authoritative links, actionable expectations, section order, language, and every reference-table row. Explain each `N/A`; do not mark a missing item as passed from an overall impression. Check local relative links against the filesystem and run available repository documentation checks. If a check cannot run, report which item remains unverified.
7. **Check change impact and finish**: when editing, inspect the diff and search living repository documents for references to changed AGENTS.md section numbers or headings, including text that mentions `AGENTS.md` with `§` or a heading anchor; update stale references, leaving immutable records intact. Re-run the item-by-item check after repairs. For an audit-only request, return the evidence matrix and revision suggestions without editing. For authoring, commit only after every applicable item and check passes.

---

## Input & Output

### Input

- **One-line positioning**: what the project is (e.g. "an agent-first, governance-ready capability inventory").
- **Top-level assets and directories**: asset types (e.g. skills), directories, spec paths; where a type does not exist, say "none" or leave it out.
- **Optional**: the AGENTS.md raw URL, an excerpt of an existing AGENTS.md or README (for a revision), the primary description language (e.g. English).

### Output

- **Authoring**: a complete AGENTS.md that satisfies the output contract (or a diff / the full revised text), the verification matrix, and the checks run.
- **Audit**: a verification matrix against each applicable requirement in the contract's §3–§6, plus revision suggestions; do not edit the file. Use `Requirement | Status | Evidence | Action`, citing file lines or sections for each verdict and explaining every `N/A`.

---

## Restrictions

### Hard Boundaries

- **Do not leave the contract**: do not mark a section the contract does not call for as "required", and do not drop any of the seven recommended section types without good reason.
- **Do not paste whole specs**: do not paste whole spec content into AGENTS.md; summarise and link only.
- **No vague behaviour**: do not use "if possible", "as appropriate", and the like; use "must", "should", "must not" (or equivalents).
- **Do not omit the reference table**: the table must carry the AGENTS.md format source, usage/installation, and applicable project-specific entry contract and index; mark unavailable project-specific sources `N/A` rather than inventing them.

### Skill Boundaries (avoid overlap)

**Do not do these (other skills handle them)**:

- **Write the README file**: create or update README.md → use `generate-standard-readme`
- **Bootstrap the full project documentation**: set up the complete documentation structure → stood up by the AgentFabric runtime or a human, per `docs/ARTIFACT_NORMS.md`
- **Refine skill design**: review or refactor SKILL.md files → use `refine-skill-design`
- **Write other document types**: API docs, user guides, tutorials → out of scope

**When to stop and hand off**:

- The user says "AGENTS.md looks good" or "approved" → the skill is done; hand off to the next documentation task
- The user asks "can you write the README too?" → hand off to "generate-standard-readme"
- The user asks "can you set up all the project documentation?" → hand off to the AgentFabric runtime (which acts per `docs/ARTIFACT_NORMS.md`)
- The user asks "can you review this skill?" → hand to "refine-skill-design"

---

## Self-Check

### Core Success Criteria (all applicable items must be met)

- [ ] **Authoring only — AGENTS.md exists**: the file is written to the repository root and committed to version control; skip this item for an audit-only request
- [ ] **The three core elements are present**: the project identity, authoritative sources, and behavioural expectations sections all exist
- [ ] **Seven sections complete**: opening, project identity, authoritative sources, behaviour, discovery/loading summary, language/communication, and reference table
- [ ] **Actionable behaviour**: the behavioural expectations use "must", "should", or "must not" on actionable items
- [ ] **Reference table complete**: covers the AGENTS.md format source, the entry raw URL and project-specific entry contract where available, usage/installation, and the entry index
- [ ] **Contract compliance**: the output follows the embedded output contract structure and content requirements
- [ ] **Item evidence**: every applicable §3–§6 requirement has a `PASS` or `FAIL` with a locator; each `N/A` has a reason

### Process Quality Checks

- [ ] **Contract read**: did I read the output contract section before acting?
- [ ] **Inputs gathered**: did I gather every required input (positioning, asset types, directories), or ask when one was missing?
- [ ] **Section order**: did I generate AGENTS.md in the contract's §3 order (identity → authority → behaviour → operations → language → reference)?
- [ ] **No spec duplication**: did I avoid pasting whole spec or document content, indexing and summarising instead?
- [ ] **Actionable language**: did I use "must" / "should" / "must not" for the behavioural expectations?
- [ ] **Reference table**: did I include every required element (format source, raw URL where applicable, entry contract, usage/installation, index)?
- [ ] **Links and checks**: did I resolve local relative links and run relevant repository documentation checks, or report which check was unavailable?
- [ ] **Cross-references after edits**: did I inspect the diff and repair stale references to changed AGENTS.md section numbers or headings in living documents?

### Acceptance Test

**Can an AI agent read this AGENTS.md and learn what the project is, where the authoritative sources are, and how to act when using the project?**

If no: AGENTS.md is incomplete. Go back to gather input or to revise the sections.

If yes: in authoring mode, commit and hand off; in audit mode, return the verification matrix without editing.

---

## Examples

### Example 1: New project (minimal information)

**Input**: project: my-cli. One line: a CLI for renaming files locally in batches. Assets: no skills, only a README and source code. Wants an agent entry; primary language English.

**Expected**: generate an AGENTS.md covering: opening (this file is the agent entry and contract), project identity (one line + asset table; can collapse to "docs/source" and the like), authoritative sources (the definitions and directories in the README or in docs/), behavioural expectations (a few "must" items), discovery and loading (a summary where an INDEX or equivalent exists, otherwise how the agent is to make sense of the project), language and communication (English), reference table (format source, this entry raw where applicable, links to the docs and the entry). Do not invent specs or paths that do not exist.

### Example 2: Edge case — an incomplete AGENTS.md

**Input**: the existing AGENTS.md holds only "this project is XX" and "read INDEX" — no authoritative sources, no behaviour, no reference table. The project has docs/ and a README, no skills. Complete it per the output contract.

**Expected**: keep the existing "project identity"; add authoritative sources (where the definitions and directories live), behavioural expectations (at least 2-3 actionable items, e.g. "follow the README and the docs", "when listing capabilities, read the index then enumerate"), discovery and loading (summary), language and communication, and the reference table. Do not delete correct user wording; where the project has no INDEX, the reference table can say "N/A" or list README/docs. Output the full revised text or a diff, and state which sections were added.

---

## Output Contract: AGENTS.md Authoring Standard

Below is AI Cortex's project-specific authoring profile for AGENTS.md, embedded in this SKILL.md. It is not a required template of the open [agents.md](https://agents.md/) format, which permits arbitrary Markdown headings. Other projects can adapt the profile; this repository's [AGENTS.md](../../AGENTS.md) follows it.

### 1. Purpose and Role

- **AGENTS.md** is the **single entry and contract** through which an AI agent interacts with the project; it usually sits at the repo root.
- **Purpose**: when an agent meets the project, define the **project identity**, the **authoritative sources**, and the **behavioural expectations**, so the agent acts consistently and predictably whenever it references the repository.
- **Audience**: agents that can read files (e.g. IDE agents, CLI agents); also usable by consumer repositories that reference it through a raw URL.

### 2. Primary Goal

The primary goal of AGENTS.md is not to "teach the Agent how to use skills" but to establish the **entry and the behaviour**. That means three things:

| Goal | Description |
| :--- | :--- |
| **Project identity** | One sentence on what the project is; lists the top-level asset types (e.g. skills), their directories, and the defining spec. |
| **Authoritative sources** | Where the "definitions" and the "directory/listing" live; the agent treats these as fact, not hearsay or scattered documents. |
| **Behavioural expectations** | What the agent **must or must not** do when referencing the project (e.g. follow the spec, self-check before committing, read the index then enumerate when listing capabilities). |

### 3. Recommended Structure and Sections

Both agents and humans work from this order:

| Order | Section | Content |
| :--- | :--- | :--- |
| 1 | **Opening** | One sentence: this file is the Agent's entry and contract; its purpose (identity + authority + behaviour). |
| 2 | **Project identity** | One-line positioning + a table of asset types / directories / specs + the directory and inventory, where present. |
| 3 | **Authoritative sources** | Where the definitions, the directory/listing, and the usage contract live; pointers only, no elaboration. |
| 4 | **Behavioural expectations** | Numbered expectations the agent must follow; each can cite a spec or a document. |
| 5 | **Discovery and loading (summary)** | The asset root and how discovery and injection work; link to a detailed guide when the procedure is too long for the entry file. |
| 6 | **Language and communication** | The primary description language and terminology; kept consistent with specs/skills or the equivalent. |
| 7 | **Reference** | A table: AGENTS.md format source, this entry's raw URL and project-specific entry contract where available, usage and installation, the entry index. |

Section titles and levels can follow the project's style, but keep the order: identity → authority → behaviour → operations summary → language → reference.

### 4. Content Requirements

- **Actionable expectations**: use "must", "should", "must not" (or equivalents) so the agent can parse and follow them.
- **Do not duplicate specs and docs**: AGENTS.md indexes and summarises; point at "specs/" or "docs/" for the full definitions and for installation.
- **Stable references**: use relative paths or resolvable URLs for the specs and indexes inside the repository; where the project can be referenced through a raw URL, give the canonical raw URL of AGENTS.md in the reference table.

### 5. Format and Style

- **Title**: short and parseable; prefer a project name and role (e.g. "AI Cortex — Agent Entry Point"). This is a project preference, not an agents.md requirement.
- **Length**: aim for roughly one page (e.g. 60-80 lines) so the agent can load and parse it in one pass.
- **Language**: match the project's primary asset language.
- **Tables**: use Markdown tables for project identity, authoritative sources, and the reference, so they parse structurally.

### 6. Reference Table

- End with a **reference table** listing at least: the format source, this entry's raw URL (where raw references are supported), the project-specific entry contract (where one exists), usage and installation, and the entry index (e.g. skills/INDEX.md). The table lets agents and tools jump to the authoritative document without crawling the repository.

### 7. Relationship to Other Specs

- **Usage**: runtime behaviour for self-check, discovery and injection lives in AGENTS.md's behavioural expectations and discovery sections; AGENTS.md is the single entry and contract.
- **Language**: the description and communication expectations in AGENTS.md should stay in line with the project's primary asset language.

### 8. Adapting to Other Projects

Another project adopting this contract can: keep the three elements (identity, authority, behaviour) and the recommended section order; replace "project identity" with its own one-line positioning and asset table; replace the paths and spec names in "authoritative sources", "behaviour", and "discovery and loading" with "specs/" or the equivalent; and where the project has no skills or index, leave those out or substitute the project's own top-level assets and directories, adjusting the reference table to match.
