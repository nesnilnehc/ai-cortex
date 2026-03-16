# Milestones

Phase checkpoints derived from [strategic goals](../project-overview/strategic-goals.md). Each milestone maps to at least one goal. No backlog or requirements here; see backlog and roadmap for detailed work.

---

## Goal-derived milestones

### M1: Discoverability baseline

**Scope:** Scenario-first routing, INDEX, and manifest are the stable entry points for discovery.

**Success criterion:** Teams can find the right capability by task or intent; scenario-map, INDEX.md, and manifest.json are canonical and maintained.

**Maps to:** Goal 1 (Discoverability).

---

### M2: Reusability baseline

**Scope:** Skills are one-file, composable, and adoptable across projects.

**Success criterion:** Spec and related_skills support composition; skills can be installed or added to a project with minimal friction; no duplication of core capability definitions.

**Maps to:** Goal 2 (Reusability).

---

### M3: Governance baseline

**Scope:** Shared spec, quality bar, and lifecycle so agent behavior is reviewable and governable.

**Success criterion:** Spec (skill.md) defines structure and quality; ASQM/curate-skills and self-check are in use; skills have clear boundaries and handoffs.

**Maps to:** Goal 3 (Governance).

---

### M4: Ecosystem presence

**Scope:** The capability layer is available in channels and tools teams already use.

**Success criterion:** Catalog is installable or discoverable via skills.sh, SkillsMP, and at least one IDE or agent ecosystem path; adoption friction is low.

**Maps to:** Goal 4 (Ecosystem adoption).

---

## Completion status (as of assessment)

| Milestone | Status | Evidence |
| :--- | :--- | :--- |
| **M1: Discoverability baseline** | Done | `skills/scenario-map.json`, `skills/scenario-map.md`, `skills/INDEX.md`, `manifest.json` are canonical; `verify-registry.mjs` keeps them in sync; AGENTS.md describes scenario-first discovery. |
| **M2: Reusability baseline** | Done | Spec defines structure and `related_skills`; skills are one-file (`SKILL.md`); `npx skills add`, install-fallback, and per-skill install reduce adoption friction. |
| **M3: Governance baseline** | Done | `spec/skill.md` defines structure and quality; `curate-skills` and `ASQM_AUDIT.md` in use; skills have Restrictions, Scope Boundaries, and Self-Check. |
| **M4: Ecosystem presence** | Done | Catalog installable via skills.sh (`npx skills add`), documented for SkillsMP; Cursor and Trae supported via `install-rules` and rules registry; README and INDEX document channels. |

All four goal-derived milestones are met. Next step: use these as stable checkpoints for release alignment and for `align-planning` / `run-checkpoint` when assessing drift.

---

## Release alignment (reference)

Version and release milestones are tracked in [CHANGELOG](../../CHANGELOG.md) and [Evolution Roadmap](../designs/2026-03-02-ai-cortex-evolution-roadmap.md). Strategy-derived milestones above are outcome checkpoints; release milestones (e.g. v2.1.0, v2.2.x) may align to one or more of M1–M4 as they complete.
