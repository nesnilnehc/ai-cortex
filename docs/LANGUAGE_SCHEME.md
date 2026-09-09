---
artifact_type: governance
created_by: ai-cortex
lifecycle: living
created_at: 2026-03-24
status: active
---

# Language Scheme

**Authority**: this document defines which language each asset in AI Cortex is written in. When any other document disagrees with it, this one wins.

---

## 1. Principle

**English is the default. Write English unless this document names an exception.**

AI Cortex is consumed by AI agents and by developers worldwide. Its skills are indexed by open ecosystems (skills.sh, agentskills.io) and installed into Claude Code, Cursor, Codex and other agents. English keeps the contributor pool and the user base unbounded.

---

## 2. Exceptions

Three categories stay in Chinese. All of them are **immutable records**, not living documentation.

| Category | Why it is not translated |
| :--- | :--- |
| `docs/adr/*.md` (existing records) | An ADR is a snapshot of a decision at a point in time. `rules/adr-management.md` forbids editing anything but `status`. Rewriting the prose would falsify the record. |
| `CHANGELOG.md` (existing entries) | Same reasoning: released entries describe what shipped, in the words used at the time. |
| `docs/designs/*.md` (snapshots) | `lifecycle: snapshot` artifacts record a design as it stood. |

**New** ADRs, changelog entries and design documents are written in English.

Everything else — README, AGENTS.md, CONTRIBUTING, `docs/`, `specs/`, `protocols/`, `rules/`, and every `SKILL.md` and skill `README.md` — is English.

---

## 3. Machine-consumed fields

These were always English and are unaffected by this scheme:

| Field | Where |
| :--- | :--- |
| `name`, `tags`, `triggers`, `description` | SKILL frontmatter |
| File and directory names | kebab-case, no exceptions |
| `skills/INDEX.md`, `rules/INDEX.md`, `specs/INDEX.md` | Registries |
| `.claude-plugin/marketplace.json` | Plugin manifest |

`description` must remain English regardless of anything else here: skills.sh and agentskills.io parse it, and `AGENTS.md` §4 matches skills against it.

---

## 4. `description_zh`

An optional SKILL frontmatter field carrying a Chinese translation of `description`. It is a convenience for Chinese-reading users, never the source of truth. Adding it is optional; omitting it is not a defect.

---

## 5. Writing standards

- **English prose**: plain, direct, active voice. State the conclusion first, then the reasoning. Define a term the first time it appears.
- **Chinese prose** (the exceptions in §2, and `description_zh`): follows [rules/writing-chinese-technical.md](../rules/writing-chinese-technical.md) — spacing between Chinese and Latin characters, full-width punctuation, consistent terminology.
- **Terminology**: the four asset types are Skill, Spec, Protocol and Rule. Defined in [docs/architecture/terminology.md](architecture/terminology.md).

---

## 6. Translation quality bar

Machine translation is not acceptable for this repository. It has already cost the project once: a prior pass left 164 duplicated-translation headings and 27 mistranslated technical terms (`preflight` rendered as "flight before", `flaky tests` as "flake-shaped tests", `happy path` as "road of happiness"), all of which had to be cleaned up by hand.

When converting an existing Chinese document:

- **Rewrite, do not translate.** Read the paragraph, understand what it asserts, then write that assertion in English.
- Keep technical terms in their standard English form. Do not invent renderings.
- Preserve the document's structure, IDs and cross-references exactly; only the prose changes.
- A converted document must read as though it was written in English, not as though it passed through a translator.

---

## 7. Migration status

Conversion from Chinese-first to English-first, in descending order of reader impact:

| Stage | Assets | Status |
| :--- | :--- | :--- |
| E0 | This document | done |
| E1 | `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md` | |
| E2 | `rules/*.md` | |
| E3 | `specs/*.md`, `protocols/*.md` | |
| E4 | `docs/**` (excluding `adr/` and `designs/`) | |
| E5 | `skills/*/README.md` | |
| E6 | `skills/*/SKILL.md` bodies | |

Stages are independently shippable. A partially migrated repository is expected during the transition; `skills/INDEX.md` and all frontmatter stay English throughout, so discovery and skill matching are unaffected at every point.
