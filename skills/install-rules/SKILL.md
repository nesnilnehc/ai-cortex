---
name: install-rules
description: Install rules from source repo into Cursor or Trae IDE with explicit confirmation and conflict detection. Core goal - install rules to editor destinations with user approval before any write.
tags: [automation, infrastructure]
version: 1.2.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
input_schema:
  type: free-form
  description: Source repo or local rules directory and target IDE (Cursor or Trae)
output_schema:
  type: side-effect
  description: Rule files written to IDE-specific destinations (.cursor/rules/ or .trae/project_rules.md)
---

# Skill: Install Rules

## Purpose

Install **rules** (passive constraints for AI behavior) from a rules source into an editor's rules destination. The primary source is this project's `rules/` directory, or a user-specified Git repository. Supported install targets: **Cursor** (`.cursor/rules/`) and **Trae IDE** (`.trae/project_rules.md` / `.trae/user_rules.md`).

---

## Core Objective

**Primary Goal**: Install rules from a source repository into Cursor or Trae IDE with explicit user confirmation and conflict detection.

**Success Criteria** (ALL must be met):

1. ✅ **Source resolved**: Rules source (this repo `rules/` or specified Git repo) is read and rule list is built from `INDEX.md` or directory listing
2. ✅ **Destination analyzed**: Existing target files are scanned and conflicts/duplicates are identified before any write
3. ✅ **Install plan presented**: Explicit plan showing per-rule actions (`create/skip/conflict/update`) and target paths is shown to user
4. ✅ **User confirmed**: User explicitly approved the plan before any file creation or modification
5. ✅ **Rules installed**: Selected rules are written to target destination (Cursor `.mdc` files or Trae managed block) with correct format
6. ✅ **Output reported**: Post-install summary includes executed actions, target paths, and any conversion notes or failures

**Acceptance Test**: Can the user verify which rules were installed, where they were installed, and whether any conflicts were detected?

---

## Scope Boundaries

**This skill handles**:

- Resolving rules source (this repo or Git repo)
- Listing available rules from source
- Analyzing destination state (existing files/conflicts)
- Building and presenting install plan
- Installing rules to Cursor (`.mdc` format) or Trae (managed block)
- Reporting installation results

**This skill does NOT handle**:

- Discovering which skills are available (use `discover-skills`)
- Creating or authoring new rules (out of scope)
- Modifying rule content (preserves source content exactly)
- Installing skills (only rules)

**Handoff point**: When rules are installed and reported, the skill is complete. If user wants to discover skills, hand off to `discover-skills`.

---

## Use Cases

- **This project**: Install all or selected rules from the current repo's `rules/` into the current project's Cursor or Trae rules.
- **Another Git repo**: User provides `owner/repo` (and optionally branch/ref and subpath); list rules from that repo and install selected ones to Cursor or Trae.
- **Bootstrap**: After cloning ai-cortex or another rule-providing repo, install its rules so the Agent respects them in the user's workspace.

---

## Behavior

1. **Resolve source**:
   - **This project**: Use the repo's `rules/` directory. Treat `rules/INDEX.md` as the authoritative list; if present, parse the registry table to get rule names and file paths. Otherwise list all `*.md` files under `rules/` (excluding `INDEX.md`).
   - **Specified Git repo**: User supplies `owner/repo` or full clone URL, and optionally branch/ref and subpath (e.g. `rules` or `docs/rules`). Discover rules by: (a) looking for an `INDEX.md` (or equivalent) in the subpath and parsing the registry, or (b) listing `*.md` files in that directory. If the repo or path does not exist or contains no rules, report clearly and do not write files.

2. **List rules**: Output a list of installable rules (name, short description or scope). Let the user choose "all" or a subset by name.

3. **Analyze destination state (required)**:
   - **Cursor**: List existing `./.cursor/rules/*.mdc` (project-level) or the user-level rules directory if selected. Identify which target filenames already exist.
   - **Trae**: Read the selected destination file (`./.trae/project_rules.md` or `./.trae/user_rules.md`, or global user-level if selected) if it exists. Detect whether a managed block already exists (see step 6).

4. **Build an install plan (required)**:
   - For each selected rule, decide one action: `create`, `skip (identical)`, `conflict (different)`, or `update (explicit overwrite approved)`.
   - The default must be conservative:
     - Existing-but-different targets are `conflict` until the user explicitly approves overwrite.
     - Existing-and-identical targets are `skip`.
   - Output the plan before any write, including the intended target path(s) and per-rule actions.

5. **Confirm before writing**:
   - Do not create, modify, or overwrite any file under `.cursor/rules/`, `.trae/`, or any target path until the user explicitly confirms the plan.
   - If overwrites are included, require explicit confirmation that lists which rule targets will be overwritten.

6. **Install to Cursor**:
   - **Target path**: Project-level is `./.cursor/rules/` (relative to repo root); user-level is platform-dependent (e.g. `~/.cursor/rules/` if applicable). Prefer project-level unless the user asks for user-level. Create the directory if it does not exist.
   - **Format**: Write one `.mdc` file per rule. Map source rule metadata into frontmatter (`description`, optional `globs`, optional `alwaysApply`), and preserve the rule body.
   - **Idempotency**: Before writing, normalize content and compare with existing target content (if any). If identical, `skip`.
   - **Conflicts**: If the target exists and differs, do not overwrite unless the plan includes `update` and the user explicitly confirmed overwrite.

7. **Install to Trae (managed block)**:
   - **Target path**: Project-level is `./.trae/project_rules.md`; user-level is `./.trae/user_rules.md` (project-scoped) or a global user-level path if Trae supports it. Prefer project-level unless the user asks for user-level. Create the `.trae/` directory if it does not exist.
   - **Managed block (required)**:
     - Only write within a managed block to avoid modifying user-authored rules.
     - Use markers like `<!-- ai-cortex:begin -->` and `<!-- ai-cortex:end -->` around the managed block.
     - If the managed block exists, replace the entire block content; if it does not, insert the block (typically appended to the end of the file).
   - **Block contents**:
     - Inside the block, render one section per rule using `## Rule: <name>` headers, in a stable order (prefer the `rules/INDEX.md` registry order when available).
     - Preserve each rule body (everything after the source frontmatter).
     - Deduplicate by rule name inside the managed block (one name → one section).
   - **Idempotency**: If the re-rendered managed block is identical to the current managed block, `skip` and do not rewrite the file.

8. **Output**: After installation, report the plan, executed actions, target path(s), and any conversion notes or failures.

---

## Input & Output

### Input

- **Source**: Default "this project" (current repo `rules/`). Or: Git repo `owner/repo` or URL, with optional branch/ref and subpath (e.g. `rules`, `docs/rules`).
- **Target**: One or both of Cursor, Trae.
- **Scope**: "All" rules or a subset (list of rule names).
- **Destination**: Project-level or user-level; default project-level.
- **Conflict policy**: Default is conservative (no overwrite); overwrites require explicit confirmation.

### Output

- **Before install**: Rule list + destination analysis summary + install plan (`create/skip/conflict/update`) with target paths.
- **After install**: Executed actions, target path(s), and any errors or conversion notes.

---

## Restrictions

### Hard Boundaries

- **No write without confirmation**: Do not create or modify files under `.cursor/rules/`, `.trae/`, or any target path without explicit user confirmation of the plan.
- **No overwrite without confirmation**: If a target already exists and differs, do not overwrite unless the user explicitly agrees and the plan includes `update` for that target.

### Skill Boundaries (Avoid Overlap)

**Do NOT do these (other skills handle them)**:

- Discovering skills → `discover-skills`
- Creating or editing rule content → out of scope
- Installing skills (SKILL.md) → out of scope

---

## Self-Check

### Core Success Criteria (ALL must be met)

- [ ] **Source resolved**: Rules source read and rule list built from `INDEX.md` or directory listing
- [ ] **Destination analyzed**: Existing target files scanned and conflicts/duplicates identified before any write
- [ ] **Install plan presented**: Plan with per-rule actions and target paths shown to user
- [ ] **User confirmed**: User explicitly approved the plan before any file creation or modification
- [ ] **Rules installed**: Selected rules written to target destination with correct format
- [ ] **Output reported**: Post-install summary includes executed actions, target paths, and any conversion notes or failures

---

## Examples

### Example 1: Install all rules from this project to Cursor

- Read `rules/INDEX.md` and build rule list.
- Analyze `.cursor/rules/` and build a conservative plan.
- Present plan, get confirmation, perform `create`/`update` actions, then report.

### Example 2: Install rules from another Git repo to Trae

- Resolve `owner/repo` and subpath.
- Discover rules, build plan for Trae managed block, confirm, then write managed block.
- Report installed rules and target file path.

