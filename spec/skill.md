# Skill Specification

Status: MANDATORY  
Scope: All files under `skills/`.

---

## 1. File Structure and Naming

- **Directory**: Must use `kebab-case` and match the YAML `name` field.
- **File name**: Must be `SKILL.md`.
- **Naming**: Use `verb-noun` (e.g. `decontextualize-text`). Avoid vague or generic terms.
- **name** (aligned with [agentskills.io](https://agentskills.io/specification)): 1–64 chars; lowercase letters, digits, hyphens only; must not start or end with `-`; no consecutive hyphens `--`; must match parent directory name.
- **Single-file and self-contained (best practice)**: A skill is typically **one SKILL.md**; the Agent loads that file for the full definition. Do not rely on other MD files in the skill directory for execution. If the skill has a fixed output format or contract (e.g. "AGENTS.md must follow a given structure"), **embed that contract in SKILL.md** (e.g. "## Appendix: Output contract") rather than a separate file, so one injection is enough.

## 2. Required YAML Metadata

Every `SKILL.md` must start with:

```yaml
---
name: [kebab-case-name]
description: [one-line summary in English; for discoverability and semantic search in agentskills / skills.sh]
tags: [at least one tag from INDEX]
version: [x.x.x]
license: MIT
related_skills: [optional list]
recommended_scope: [optional] user | project | both  # default both
metadata:
  author: ai-cortex
  # Optional evolution tracking (for forked/derived skills):
  evolution:
    sources:  # Array of source skills this skill is derived from
      - name: [original-skill-name]
        repo: [source repository URL or identifier]
        version: [version borrowed from]
        license: [source license]
        type: fork | integration | reference  # fork=main base, integration=incorporated, reference=inspired by
        borrowed: [brief description of what was borrowed]
# Optional agentskills.io fields:
# compatibility: [optional] environment requirements, ≤500 chars, e.g. "Requires git, docker"
# allowed-tools: [optional, experimental] space-separated tool whitelist
---
```

### Evolution Metadata (Optional)

When a skill is derived from, forked from, or integrates content from other skills, use `metadata.evolution.sources` to track provenance:

- **sources**: Array of source skills with attribution
  - **name**: Original skill name
  - **repo**: Source repository URL or identifier (e.g., "nesnilnehc/ai-cortex", "https://github.com/org/repo")
  - **version**: Version borrowed from
  - **license**: Source license (for compliance)
  - **type**: Relationship type
    - `fork`: This skill is primarily based on the source (main lineage)
    - `integration`: Incorporated specific components or methodology from source
    - `reference`: Inspired by or referenced the source's approach
  - **borrowed**: Brief description of what was borrowed (e.g., "Core workflow and staging approach", "Review methodology")

Example with multiple sources:

```yaml
metadata:
  author: ai-cortex
  evolution:
    sources:
      - name: "commit-work"
        repo: "https://github.com/anthropics/skills"
        version: "1.0.0"
        license: "MIT"
        type: "fork"
        borrowed: "Core workflow, Conventional Commits format"
      - name: "review-diff"
        repo: "nesnilnehc/ai-cortex"
        version: "1.3.0"
        license: "MIT"
        type: "integration"
        borrowed: "Pre-commit review methodology"
    enhancements:
      - "Added registry synchronization"
      - "Enhanced Self-Check"
```

## 3. Required Heading Structure

- `# Skill: [English title]`
- `## Purpose`
- `## Use Cases`
- `## Behavior`
- `## Input & Output`
- `## Restrictions`
- `## Self-Check`
- `## Examples`

## 4. Content Quality

- **Language**: YAML `description` must be **English** for skills.sh, SkillsMP, etc. Skill body, titles, and examples must be **English**. `name`, `tags`, and other identifiers remain English/kebab-case.
- **Tone**: Use imperative, technical language. Avoid filler or casual phrasing.
- **Examples**: Include at least 2 examples, one of which must be an edge case or complex scenario.
- **Interaction**: For non-trivial logic, define when to ask the user to confirm.

## 5. Metadata Sync

- After adding a skill, update `skills/INDEX.md` with the new entry.
- After adding or moving a skill, update `manifest.json` `capabilities` with the new path.
- **Checklist**: When adding or moving a skill, verify both `skills/INDEX.md` and `manifest.json` are updated together; run `scripts/verify-registry.mjs` (if present) to confirm they stay in sync.
- **Publish for npx skills**: `npx skills add owner/repo --skill <name>` clones the default branch from the remote. Push the commit that adds the skill (and updated INDEX + manifest) so the skill is discoverable and installable.
- Versions must follow [SemVer](https://semver.org/).

## 6. agentskills Compatibility

- This spec aligns with [agentskills.io](https://agentskills.io) and skills.sh. `license` and `metadata.author` are used for catalog and trust; `metadata.author` is `ai-cortex`.
- This spec may be stricter than agentskills.io as long as it does not conflict with the upstream requirements.
- **Optional directories** (agentskills.io): `scripts/`, `references/`, `assets/`. Use relative paths, keep depth shallow.
- **Progressive disclosure**: Keep main `SKILL.md` ≤500 lines; move detail to `references/` and load on demand.

## 7. Extension and Contribution

- New skills must satisfy this spec; use `skills/refine-skill-design` for design review.
- Version registration: update `skills/INDEX.md` with linear version bumps.
- Installation: see [README.md](../README.md).

## 8. Repo-level docs (skills directory)

- **`skills/skillgraph.md`**: Optional; describes how review and other skills compose. For human and Agent reading; INDEX and manifest do not depend on it. Update when adding or changing orchestration (e.g. review-code) or composition.
- **`skills/ASQM_AUDIT.md`**: Produced by the `curate-skills` skill; lifecycle and ASQM scores. Update by running curate-skills after adding or changing skills. It does not replace INDEX or manifest.
