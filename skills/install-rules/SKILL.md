---
name: install-rules
description: Install rules from this project or a specified Git repo into Cursor or Trae IDE. Use when the user wants to add project/global rules to their editor from ai-cortex rules/ or another repository.
tags: [automation, infrastructure, eng-standards]
version: 1.0.0
license: MIT
related_skills: [discover-skills]
recommended_scope: both
metadata:
  author: ai-cortex
---

# Skill: Install Rules

## Purpose

Install **rules** (passive constraints for AI behavior) from a rules source into an editor’s rules directory. The primary source is this project’s `rules/` directory, or a user-specified Git repository. The only supported install target in this version is **Cursor** (`.cursor/rules/`). **Trae IDE** is not yet supported; support will be added when Trae’s rules path and file format are documented in this skill.

## Use Cases

- **This project**: Install all or selected rules from the current repo’s `rules/` into the current project’s Cursor rules (or user-level Cursor rules).
- **Another Git repo**: User provides `owner/repo` (and optionally branch/ref and subpath); list rules from that repo and install selected ones to Cursor.
- **Bootstrap**: After cloning ai-cortex or another rule-providing repo, install its rules so the Agent respects them in the user’s workspace.

## Behavior

1. **Resolve source**:
   - **This project**: Use the repo’s `rules/` directory. Treat `rules/INDEX.md` as the authoritative list; if present, parse the registry table to get rule names and file paths. Otherwise list all `*.md` files under `rules/` (excluding `INDEX.md`).
   - **Specified Git repo**: User supplies `owner/repo` or full clone URL, and optionally branch/ref and subpath (e.g. `rules` or `docs/rules`). The Agent must have network access to clone or fetch; state this before proceeding. Discover rules by: (a) looking for an `INDEX.md` (or equivalent) in the subpath and parsing the registry, or (b) listing `*.md` files in that directory. If the repo or path does not exist or contains no rules, report clearly and do not write files.

2. **List rules**: Output a list of installable rules (name, short description or scope). Let the user choose “all” or a subset by name.

3. **Confirm before writing**: Do not create or overwrite any file under `.cursor/rules/` (or any target path) until the user explicitly confirms. If a target file already exists, do not overwrite unless the user explicitly agrees.

4. **Install to Cursor**:
   - **Target path**: Project-level is `./.cursor/rules/` (relative to repo root); user-level is platform-dependent (e.g. `~/.cursor/rules/` if applicable). Prefer project-level unless the user asks for user-level. Create the directory if it does not exist.
   - **Format**: Write one `.mdc` file per rule. Cursor expects frontmatter with at least `description`. Optionally set `globs` (file pattern) or `alwaysApply: true`. Map source rule metadata: use `name` and `scope` (or equivalent) to build `description`; if scope indicates “all code” or “global”, set `alwaysApply: true`; otherwise leave `alwaysApply: false` and omit or set `globs` only when the source rule clearly implies a file type.
   - **Body**: Preserve the full rule body (everything after the source frontmatter). Do not drop content.

5. **Output**: After installation, report per the Output contract (Appendix): list of installed rule names, target directory path, and any conversion notes or failures.

## Input & Output

### Input

- **Source**: Default “this project” (current repo `rules/`). Or: Git repo `owner/repo` or URL, with optional branch/ref and subpath (e.g. `rules`, `docs/rules`).
- **Target**: One or both of Cursor, Trae. Currently only Cursor is supported; if the user asks for Trae, state that it is not yet supported and offer Cursor only.
- **Scope**: “All” rules or a subset (list of rule names).
- **Destination**: Project-level `.cursor/rules/` or user-level; default project-level.

### Output

- **Before install**: List of rules that will be installed (names and target filenames).
- **After install**: Installed rule names, target path, and any errors or conversion notes (see Appendix: Output contract).

## Restrictions

- **No write without confirmation**: Do not create or modify files under `.cursor/rules/` or any target path without explicit user confirmation.
- **No overwrite without confirmation**: If a target `.mdc` already exists, do not overwrite unless the user explicitly agrees.
- **Git and network**: Installing from a Git repo requires clone/fetch; state that network (and optionally git) is required and confirm before running clone/fetch.
- **Trae**: Do not claim Trae is supported until this skill is updated with Trae’s official rules path and format; currently state “Cursor only; Trae support to be added.”

## Self-Check

- [ ] **Source resolved**: Was the rules source (this repo `rules/` or specified Git repo + path) read correctly? Was `rules/INDEX.md` or equivalent used when present?
- [ ] **List shown**: Was the user shown the list of rules to be installed before any write?
- [ ] **Confirmation**: Was explicit user confirmation obtained before creating or overwriting any file?
- [ ] **Output contract**: Does the post-install output include installed rule names, target path, and any conversion or failure notes?
- [ ] **Restrictions**: Were overwrites and writes only done with user consent? Was Trae not claimed as supported?

## Examples

### Example 1: Install all rules from this project to Cursor

- **Scenario**: User says “install this project’s rules into Cursor.”
- **Steps**:
  1. Read `rules/INDEX.md` and build the list of rules from the registry table (or list `rules/*.md` excluding `INDEX.md`).
  2. Present the list (e.g. writing-chinese-technical, standards-import, workflow-documentation, …) and target path `./.cursor/rules/`.
  3. Ask for confirmation to create/overwrite.
  4. After confirmation, for each rule: read the `.md`, convert to `.mdc` (description from name/scope, set alwaysApply when scope is global), write to `.cursor/rules/<name>.mdc`.
  5. Output: installed rule names, path `./.cursor/rules/`, and note that Trae is not supported in this version.

### Example 2: Edge case — Git repo with no INDEX, custom subpath

- **Scenario**: User wants to install rules from `other-org/repo`, branch `main`, subpath `docs/rules`. That repo has no `docs/rules/INDEX.md`, only `docs/rules/foo.md` and `docs/rules/bar.md`.
- **Steps**:
  1. State that network access is needed to clone/fetch the repo; ask for confirmation.
  2. After confirmation, clone or fetch and list `docs/rules/*.md` (e.g. foo.md, bar.md). Do not assume an INDEX; use the directory listing as the rule list.
  3. Present the list (foo, bar) and target path; ask which rules to install (or “all”) and confirm before writing.
  4. If the user selects only “foo”, install only the file derived from `foo.md` to `.cursor/rules/foo.mdc` and report: installed [foo], path `./.cursor/rules/`, and that bar was skipped.

---

## Appendix: Output contract

After performing an install, the Agent must report:

| Element | Requirement |
| :--- | :--- |
| **Installed rules** | List of rule names (or filenames) that were written. |
| **Target path** | Absolute or repo-relative path of the rules directory (e.g. `./.cursor/rules/`). |
| **Conversion notes** | Brief note if source used a different format (e.g. .md with name/scope) and how it was mapped to Cursor .mdc. |
| **Failures** | Any rule that could not be installed (e.g. read error, write error) and reason. |
| **Trae** | If the user asked for Trae, state that only Cursor is supported in this version and Trae support will be added later. |
