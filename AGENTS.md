# Agent Entry

This file is the **single entry and contract** for AI Agents interacting with AI Cortex. It defines **project identity**, **authoritative sources**, and **behavioral expectations** so that Agents behave consistently and predictably when working in or referencing this repository.

---

## 1. Project Identity

**AI Cortex** is an agent-first, governance-ready inventory of Skills: Specs turn Skills into reusable, composable engineering assets. See [README.md#positioning](README.md#positioning).

| Asset type | Directory | Specification |
| :--- | :--- | :--- |
| Skill | `skills/` | [spec/skill.md](spec/skill.md) |

Catalog and metadata: `skills/INDEX.md`. Executable capability list: `manifest.json` at repo root.

---

## 2. Authoritative Sources

- **Definitions**: `spec/skill.md` defines structure, metadata, and quality requirements for skills.
- **Catalogs**: `skills/INDEX.md` and `manifest.json` are the canonical capability lists.
- **Entry contract**: This file defines discovery, injection, and self-check behavior (§4).

---

## 3. Behavioral Expectations

When working in or referencing this project, Agents must:

1. **Follow the spec**: When understanding, writing, or changing skills, adhere to [spec/skill.md](spec/skill.md).
2. **Self-check before commit**: After producing content, run the Skill’s Self-Check; only then submit. If the Skill defines an interaction policy (e.g. ask user), pause and confirm before proceeding.
3. **List capabilities when asked**: When the user asks “what skills are there”, read `skills/INDEX.md`, **enumerate names and purposes**, then optionally link; do not reply with only URLs.
4. **Use assets when improving this repo**: For tasks that improve this project (e.g. writing or revising AGENTS.md, designing or refactoring Skills, generating README), consult `skills/INDEX.md`, match by task semantics, and inject the appropriate Skill; do not ignore available assets.

---

## 4. Discovery and Loading (Summary)

- **Asset root**: Current repo root, this file’s repo root, or a user-provided Raw root URL.
- **Discovery**: Read `skills/INDEX.md` and `manifest.json`; match by `description`, `tags`, and task semantics. Load SKILL `related_skills` as needed.
- **Injection**: Load the **full Markdown** of selected SKILLs as system or context; inject as atomic units.
- **Self-reference**: When working on **this repo**, discover and load assets under `skills/`; use `manifest.json` `capabilities` for paths.

---

## 5. Language and Communication

- This project’s main assets are described in **English**; aligned with [spec/skill.md](spec/skill.md) language requirements.
- Common industry terms may remain in English.

---

## Reference

| Item | Description |
| :--- | :--- |
| Spec source | [AI Cortex](https://github.com/nesnilnehc/ai-cortex) |
| skills.sh install | `npx skills add nesnilnehc/ai-cortex` |
| This entry (Raw) | <https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/AGENTS.md> |
| Specs | [spec/skill.md](spec/skill.md) |
| Usage | This file §4 |
| Entry authoring | [skills/write-agents-entry/SKILL.md](skills/write-agents-entry/SKILL.md) (includes embedded output contract for other projects) |
| Indexes | [skills/INDEX.md](skills/INDEX.md) |
| Self-reference tasks→assets | **Skill**: Write/revise AGENTS.md → [write-agents-entry](skills/write-agents-entry/SKILL.md); design/refactor Skill → [refine-skill-design](skills/refine-skill-design/SKILL.md); generate README → [generate-standard-readme](skills/generate-standard-readme/SKILL.md). Full list: [skills/INDEX.md](skills/INDEX.md). |
