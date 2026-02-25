---
name: bootstrap-project-documentation
description: Bootstrap or adapt project documentation using project-documentation-template. Initialize docs for empty projects, or analyze and recommend adjustments for non-empty projects. Use for lifecycle docs, ADR, version sync.
tags: [documentation, eng-standards, writing]
related_skills: [generate-standard-readme, write-agents-entry]
version: 1.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
compatibility: Requires access to https://raw.githubusercontent.com or a local clone of nesnilnehc/project-documentation-template.
---

# Skill: Bootstrap Project Documentation

## Purpose

Bootstrap or adapt project documentation using the [project-documentation-template](https://github.com/nesnilnehc/project-documentation-template) structure. This skill supports two modes: **Initialize** (empty project—copy templates and fill placeholders) and **Adjust** (non-empty project—scan, compare to template, produce a recommendation list). Both modes follow conventions from the template’s `llms.txt` and `AGENTS.md`.

---

## Use Cases

- **Empty project**: Initialize a full docs skeleton by copying template subsets and filling placeholders for small/medium/large projects.
- **Non-empty project**: Analyze existing docs, compare to the template, produce a recommendation list (missing docs, alignable templates, unfilled placeholders, broken links), then apply changes after user confirmation.
- **Shared workflows**: Generate Architecture Decision Records (ADR), update version information across docs, validate placeholders and links.

**When to use**: When a project needs structured lifecycle documentation aligned with the enterprise template, or when existing docs should be aligned with that structure.

---

## Behavior

### Mode Selection

First determine the execution mode. User override takes precedence; otherwise:

| Mode | Trigger | Behavior |
| :--- | :------ | :------- |
| **Initialize** | No `docs/` or `docs/` empty | Copy subset, fill placeholders, create `VERSION`, output docs skeleton |
| **Adjust** | `docs/` has ≥1 valid document | Scan, compare, output recommendation list; apply after user confirmation |

**Detection rules**:

- No `docs/` or `docs/` is empty → **Initialize**
- `docs/` exists and has ≥1 valid `.md` file → **Adjust**
- User explicitly specifies `--mode=initialize` or `--mode=adjust` → use that mode

### Initialize Mode Steps

1. Determine project scale: small, medium, or large (from user or context).
2. Select the document subset from the template by scale:
   - **Small**: Project Overview, Development Guide, User Guide
   - **Medium**: + Architecture, Design, Requirements & Planning
   - **Large**: + Process Management, Operations Guide, Compliance, Community & Contributing
3. Fetch templates from `https://raw.githubusercontent.com/nesnilnehc/project-documentation-template/main/` (or use a local clone).
4. Copy selected docs to the project `docs/` with preserved directory structure.
5. Fill placeholders with project metadata (name, dates, tech stack) and prompt for missing critical data.
6. Create a `VERSION` file (e.g. `1.0.0`).
7. Validate: no unreplaced placeholders, links valid, tables aligned.

### Adjust Mode Steps

1. Scan existing docs under `docs/` (structure, placeholders, links, versions).
2. Compare to the template structure and conventions.
3. Produce a **recommendation list** with:
   - Missing documents (by scale)
   - Documents alignable to template
   - Unfilled placeholders
   - Broken or outdated links
   - Version inconsistencies
4. Present the list to the user and ask for confirmation before applying changes.
5. After confirmation, apply only the approved changes.

### Conventions (from llms.txt)

- **Placeholders**: `[description]`, `[option1/option2]`, `YYYY-MM-DD`, `[number]`
- **Tables**: Preserve column alignment; `*` marks required fields
- **Version**: Use SemVer; update version history at document bottom on changes
- **References**: Internal `[Name](relative/path)`; external ` number `
- **Dates**: `YYYY-MM-DD`

---

## Input & Output

### Input

- **Project metadata**: Name, description, tech stack
- **Scale**: small | medium | large (optional; infer from context if absent)
- **Mode override** (optional): `initialize` | `adjust`

### Output

- **Initialize**: Filled docs under `docs/`, `VERSION`, and a short summary of created files
- **Adjust**: A recommendation list (markdown or structured), then—after confirmation—the applied changes and summary

---

## Restrictions

- Replace all placeholders before finalizing documents; do not leave `[description]` etc. in final output unless explicitly deferred.
- Do not add or keep broken internal links; verify relative paths.
- Use consistent dates (`YYYY-MM-DD`) and SemVer for versions.
- In Adjust mode, do not apply changes without user confirmation.
- Do not remove structural elements (sections, tables) from templates without user approval.

---

## Self-Check

- [ ] **Mode**: Was the correct mode (Initialize vs Adjust) chosen and applied?
- [ ] **Placeholders**: Are all `[...]` placeholders replaced or explicitly marked for later fill?
- [ ] **Links**: Do internal links resolve and do external links point to valid resources?
- [ ] **Version**: Is the version consistent across `VERSION` and affected documents?
- [ ] **Tables**: Is Markdown table alignment preserved?
- [ ] **Confirm**: In Adjust mode, were changes applied only after user confirmation?

---

## Examples

### Example 1: Initialize (Empty Project, Small Scale)

**Context**: New repo `my-service`, no `docs/` directory.

**Steps**: Agent selects Initialize; scale = small. Copies Project Overview, Development Guide, User Guide from template. Fills project name, dates, placeholder descriptions. Creates `VERSION` as `1.0.0`. Outputs a summary of created files.

**Output snippet**: `docs/project-overview/goals-and-vision.md`, `docs/development-guide/...`, `docs/user-guide/...`, `VERSION`. All placeholders filled with project-specific content.

### Example 2: Adjust (Non-Empty Project)

**Context**: Repo has `docs/` with `goals-and-vision.md`, `README.md` in root. Some placeholders still unfilled.

**Steps**: Agent selects Adjust. Scans `docs/`, compares to template. Produces recommendation list:

- Missing: Development Guide, User Guide (for small scale)
- Unfilled placeholders in `goals-and-vision.md`: `[project description]`, `[target date]`
- Version: No `VERSION` file

Agent presents the list and asks: "Apply these changes? (Y/n)". User confirms. Agent adds missing docs, fills placeholders, creates `VERSION`.

### Example 3: Common Workflow—Generate ADR

**Context**: Any project; user needs an Architecture Decision Record.

**Steps**: Agent fetches `docs/process-management/decisions/ADR-TEMPLATE.md` from template. Determines next ADR number (e.g. ADR-001). Fills context, options, rationale, consequences with user input. Saves as `docs/process-management/decisions/YYYYMMDD-decision-title.md` and updates the decision index if present.

---

## Appendix: Output Contract

### Initialize Mode

| Deliverable | Required |
| :--- | :--- |
| `docs/` directory with selected template subset | Yes |
| `VERSION` file | Yes |
| All placeholders replaced (or marked for later) | Yes |
| Version history table at document bottom | Per template |

### Adjust Mode Recommendation List Format

| Section | Content |
| :--- | :--- |
| Missing documents | List by template path and scale |
| Alignable documents | List existing docs that can match template |
| Unfilled placeholders | File path + placeholder text |
| Broken/outdated links | File path + link |
| Version issues | Conflicts or missing version refs |

### Template Source

- Base URL: `https://raw.githubusercontent.com/nesnilnehc/project-documentation-template/main/`
- Key files: `llms.txt`, `AGENTS.md`, `README.md`, `docs/`
