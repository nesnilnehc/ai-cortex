# Agent Entry Point

This file is the execution contract for AI agents working inside this repository. It is the single source of truth for base facts and rules; `llms.txt` is only an outward-facing discovery pointer.

---

## 1. External resources and link policy

- An agent `MUST NOT` fetch external HTTP/HTTPS links by default. Fetching is permitted only when the current execution context explicitly sets `allow_external_fetch=true`.
- An agent `MUST NOT` load raw-content URLs by default. Permitted only when the source is trusted, pinned to a commit hash, and no local equivalent exists.
- An agent `MUST` prefer local relative paths for every load and execution dependency.
- An agent `MUST NOT` download, register or upgrade a skill from skills.sh, GitHub or any other registry at skill runtime. Externally derived capabilities enter `skills/` as reviewed local copies first.
- An agent `MUST` treat [skills/SOURCES.yaml](skills/SOURCES.yaml) as the record of pinned upstreams for externally derived skills. That file exists for maintenance and audit; it is not a runtime install instruction.

---

## 2. Project and assets

**AI Cortex** is an asset library for software delivery and project governance. See [mission](docs/project-overview/mission.md), [vision](docs/project-overview/vision.md) and [terminology](docs/architecture/terminology.md).

| Layer | Type | Registry | Authority |
|---|---|---|---|
| Active capability | Skill | [skills/INDEX.md](skills/INDEX.md) | — |
| Data structure | Spec | [specs/INDEX.md](specs/INDEX.md) | High |
| Interaction flow | Protocol | [protocols/INDEX.md](protocols/INDEX.md) | Medium |
| Passive constraint | Rule | [rules/INDEX.md](rules/INDEX.md) | Low |

**Precedence on conflict**, highest first: `AGENTS.md` > `specs/` > `protocols/` > `rules/` > `docs/`.

Skills follow the [agentskills.io](https://agentskills.io) standard format. This repository does not maintain a private skill spec.

**Canonical install path**: `${XDG_DATA_HOME:-~/.local/share}/ai-cortex`, overridable with the `CORTEX_HOME` environment variable. Agents read `specs/`, `protocols/` and `rules/` directly from that path — no install step required.

---

## 3. Expected behavior

Inside this repository, an agent `MUST`:

1. **Enumerate when asked about capabilities.** When the user asks what skills or protocols exist, read `skills/INDEX.md` and `protocols/INDEX.md` and list names with purposes. Do not answer with a URL alone.
2. **Match and use assets.** Match assets to the task semantically and inject them. Do not ignore an applicable asset.
3. **Self-check before delivering.** If a skill or protocol declares a Self-Check, it must pass before you report completion.

---

## 4. Discovery, loading and matching

**Load tiers**:

| Tier | Resource | On absence |
|---|---|---|
| MUST | `AGENTS.md` | `STOP` + `ASK` |
| SHOULD | `docs/architecture/terminology.md` | Continue, but state that it is missing; `STOP`/`ASK` if a critical decision depends on it |
| ON DEMAND | `skills/INDEX.md`, `protocols/INDEX.md`, `rules/INDEX.md` | `STOP` + `ASK` when discovery is triggered |

**Skill matching** is deterministic — never random. Match the task against each skill's `description`, `tags` and `triggers` in `skills/INDEX.md`, ranked by:

1. Exact substring match on `triggers`
2. Then number of overlapping `tags` (string equality only; no synonym inference)
3. Then semantic fit of `description`
4. On an exact tie, ascending lexicographic order of `skill_path`

**Injection**: load the selected skill's full Markdown as system or context input.
**Protocols and rules**: enumerate from their INDEX.md and inject as process baseline or long-lived background context.

---

## 5. Failure handling

- **No skill matched**: output `no skill matched` explicitly and fall back to general reasoning. You `MUST NOT` claim to have injected a skill that you did not.
- **Conflicting specifications**: resolve by the precedence order in §2 and ignore the lower-precedence source.
- **Required resource missing**: `STOP` and `ASK` the user. Do not continue inferring before the answer arrives.

---

## 6. Language

Write in English. The exceptions — existing ADRs, released changelog entries and design snapshots, all of which are immutable records — are listed in [docs/LANGUAGE_SCHEME.md](docs/LANGUAGE_SCHEME.md). Machine-consumed fields (YAML frontmatter, commands, IDs, tags) have always been English.

---

## Reference

Self-referential entry points: write an AGENTS.md with [generate-agent-entry](skills/generate-agent-entry/SKILL.md); design or refactor a skill with [refine-skill-design](skills/refine-skill-design/SKILL.md); generate a README with [generate-standard-readme](skills/generate-standard-readme/SKILL.md).
