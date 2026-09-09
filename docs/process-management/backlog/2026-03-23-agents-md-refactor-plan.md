---
artifact_type: backlog-item
created_by: capture-work-items
lifecycle: snapshot
created_at: 2026-03-24
status: active
---

# The AGENTS.md refactor plan

**Status**: completed  
**Created**: 2026-03-23  
**Goal**: cut AGENTS.md from about 120 lines to about 60–80, focused on the entry contract for an agent working inside this repository.

---

## 1. What was wrong

| Problem | Detail |
| :--- | :--- |
| Too long | About 120 lines, past the 60–80 that generate-agent-entry recommends |
| User-side assumptions mixed in | The discovery and loading protocol assumed intent-routing would be injected, but the design does not require injecting anything into the user's environment |
| Detail embedded inline | Match priority, the proactive suggestion table and similar detail took up space and belonged elsewhere |
| Compared with gstack | gstack's AGENTS.md is about 50 lines, mostly a skill table plus commands plus conventions, and reads better |

---

## 2. Principles for the refactor

1. **One audience**: the behavioural contract for an agent iterating inside this repository, and nothing user-facing.
2. **Terse**: keep only what an agent must know; the detail goes into linked documents.
3. **Aligned with generate-agent-entry**: keep the identity, authority, behaviour and reference structure, but shorten every section.
4. **Modelled on gstack**: a compact skill table, runnable commands, short conventions.

---

## 3. The target structure: 7 sections, about 60–80 lines

| Section | Contents | Lines, estimated |
| :--- | :--- | :---: |
| 1. Opening | One line of positioning: this file is the entry contract between an agent and AI Cortex; audience and scope are in docs/AUDIENCE_AND_SCOPE.md | 3–5 |
| 2. Project identity | One line of positioning plus the asset table (skills, directories, specs); links to mission and vision | 8–10 |
| 3. Authoritative sources | Cut to 3–4 entries: spec, INDEX/manifest, rules, principles; one line and a link each | 6–8 |
| 4. Expected behaviour | 4 numbered, actionable entries (must / should / must not); one sentence each, with a link where useful | 8–10 |
| 5. Discovery and self-reference | One summary paragraph: the asset root, discovery (read INDEX/manifest), injection (the full SKILL text), self-reference (manifest capabilities); the detail lives in a docs/ page | 6–8 |
| 6. Language and communication | One line: Chinese first, see LANGUAGE_SCHEME | 2–3 |
| 7. Reference | A table: spec, raw, conventions, directories, a trimmed self-reference task-to-skill mapping, and the local commands (verify, skill:check) | 15–20 |

---

## 4. What moved out

The following was removed from AGENTS.md and moved to the document named:

| Content | Moved to | Why |
| :--- | :--- | :--- |
| The detailed match priority (intent, triggers, semantic fallback and the like) | docs/guides/discovery-and-loading.md, newly created, or an addition to intent-routing.md | Detail does not belong in the entry point |
| The proactive suggestion table, stage to skill | skills/intent-routing.md or docs/guides/proactive-suggestions.md | The table is long and is maintained on its own |
| The invocation examples | Keep a trimmed 3-line version, or move them to INDEX or intent-routing | Decided by the final length |
| The long list of authoritative sources | Compressed to 3–4 entries, with the full list in AUDIENCE_AND_SCOPE or a new document | Avoids duplication |
| The long self-reference task-to-asset sentence in the reference table | Cut to "self-reference: see [INDEX](../../../skills/INDEX.md)" plus 2–3 representative mappings | The full mapping is in INDEX |

---

## 5. Companion documents created or revised

| Document | Action |
| :--- | :--- |
| docs/guides/discovery-and-loading.md | Created: the detail of discovery and loading — the asset root, the discovery flow, match priority, how injection works — for reference when needed |
| skills/intent-routing.md | Optional: add a "proactive suggestions" subsection or a link, or leave it as it is |
| docs/AUDIENCE_AND_SCOPE.md | Already exists; the AGENTS opening cites it |
| skills/generate-agent-entry/SKILL.md | After the refactor, confirm the output contract agrees with this plan; update the "target 60–80 lines" wording if needed |

---

## 6. Acceptance criteria

- [x] AGENTS.md is 60–80 lines in total (73 lines)
- [x] The 7-section structure is kept: opening, identity, authority, behaviour, discovery, language and communication, reference
- [x] No user-facing content, such as installation or usage instructions
- [x] The detail has moved out to docs/guides/discovery-and-loading.md and proactive-suggestions.md
- [x] The local command table keeps the commands iteration needs, verify and skill:check among them
- [x] Verification passes (verify, skill:check)
- [x] The AGENTS description in docs/AUDIENCE_AND_SCOPE.md agrees with this plan

---

## 7. Order of work

1. Create docs/guides/discovery-and-loading.md and move the discovery and loading detail into it
2. Create or update wherever the proactive suggestions live
3. Rewrite AGENTS.md to the target structure
4. Update the generate-agent-entry output contract, if it needs it
5. Run verify and skill:check, and confirm nothing regressed
6. Update the AGENTS description in AUDIENCE_AND_SCOPE, if it needs it
