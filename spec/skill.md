# Skill Specification

Status: MANDATORY  
Version: 2.3.0  
Scope: All files under `skills/`.

**Changelog**:

- v2.4.0 (2026-03-10): Added Interaction Policy (§4.3), optional triggers/aliases, input_schema.defaults; Invocation UX and language strategy
- v2.3.0 (2026-03-06): Added scenario-map to Metadata Sync; expanded verb-noun naming guidance; verify-registry checks scenario-map references
- v2.2.0 (2026-03-02): Allowed `## Scope Boundaries` as an optional standalone section in heading structure (§3)
- v2.1.0 (2026-03-02): Added optional I/O contracts (input_schema/output_schema) for skill chaining and orchestration
- v2.0.0 (2026-03-02): Added mandatory Core Objective section, enhanced Self-Check and Restrictions requirements, added quality assurance process
- v1.0.0: Initial specification

---

## 1. File Structure and Naming

- **Directory**: Must use `kebab-case` and match the YAML `name` field.
- **File name**: Must be `SKILL.md`.
- **Naming**: Use `verb-noun` (e.g. `decontextualize-text`). Avoid vague or generic terms.
  - **Preferred**: `verb-noun` (e.g. `generate-readme`, `discover-skills`, `capture-work-items`), or `verb-target` for review/action families (e.g. `review-code`, `review-python`).
  - **Avoid**: Pure noun-noun compounds (e.g. `documentation-readiness` → prefer `assess-documentation-readiness`); abstract compound names without a clear verb.
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
# triggers: [optional] array of English phrases, e.g. ["review", "code review"]
# aliases: [optional] array of short aliases, e.g. ["rc"]
---
```

### Evolution Metadata (Optional)

When a skill is derived from, forked from, or integrates content from other skills, use `metadata.evolution.sources` to track provenance:

- **sources**: Array of source skills with attribution
  - **name**: Original skill name
  - **repo**: Source repository URL or identifier (e.g., "nesnilnehc/ai-cortex", "<https://github.com/org/repo>")
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

### Optional Invocation Fields

- **triggers** (optional): Array of English phrases for quick invocation matching (e.g. `["review", "code review", "pr review"]`). Prefer 3–5 phrases per skill. Use for Agent or discovery-layer exact match; does not replace description/tags semantic matching.
- **aliases** (optional): Array of short aliases (e.g. `["rc"]`). May be deferred until IDE/CLI tooling has explicit need.

## 3. Required Heading Structure

- `# Skill: [English title]`
- `## Purpose`
- `## Core Objective` (NEW - MANDATORY)
- `## Scope Boundaries` (OPTIONAL — may also appear as subsection of Core Objective; see §3.1)
- `## Use Cases`
- `## Behavior`
- `## Input & Output`
- `## Restrictions`
- `## Self-Check`
- `## Examples`

### 3.1 Core Objective Section (MANDATORY)

Every skill MUST define its core objective to prevent scope creep, skill overlap, and "brain split" (AI confusion about which skill to use).

**Required subsections**:

1. **Primary Goal**: One sentence stating what the skill produces or achieves.
2. **Success Criteria**: Measurable, verifiable conditions (3-6 items) that ALL must be met for skill completion.
3. **Acceptance Test**: A simple question or test to verify the skill achieved its goal.

**Optional subsections** (may also appear as a standalone `## Scope Boundaries` section after Core Objective):

1. **Scope Boundaries**: What this skill handles vs. what it does NOT handle.
2. **Handoff Point**: When and how to transition to other skills or workflows.

Both placements are valid: as subsections of `## Core Objective` (inline) or as a separate `## Scope Boundaries` section (standalone). Choose the form that best fits the skill's complexity.

**Example**:

```markdown
## Core Objective

**Primary Goal**: Produce a validated design document that serves as the single source of truth for implementation.

**Success Criteria** (ALL must be met):

1. ✅ **Design document exists**: Written to `docs/designs/YYYY-MM-DD-<topic>.md` and committed to version control
2. ✅ **User explicitly approved**: User said "approved", "looks good", "proceed", or equivalent confirmation
3. ✅ **Alternatives documented**: At least 2-3 approaches considered with trade-offs analysis
4. ✅ **YAGNI applied**: Design focuses on minimum viable solution, unnecessary features removed
5. ✅ **DRY applied**: Design references existing patterns/components rather than reinventing
6. ✅ **No code written**: Zero implementation code exists (design only)

**Acceptance Test**: Can a developer with zero project context implement this design without asking clarifying questions?

**Scope Boundaries**:
- This skill handles: Rough idea → Validated design document
- This skill does NOT handle: Implementation planning (use `writing-plans`), Code writing (use implementation skills)

**Handoff Point**: When design is approved and documented, hand off to implementation planning or development workflow.
```

**Why this matters**:

- **Prevents brain split**: AI knows exactly when to use this skill vs. others
- **Verifiable completion**: Clear success criteria, not vague "done"
- **Avoids scope creep**: Explicit boundaries prevent skills from doing too much
- **Clear handoffs**: Knows when to stop and transition to next skill

## 4. Content Quality

- **Language**: YAML `description` must be **English** for skills.sh, SkillsMP, etc. Skill body, titles, and examples must be **English**. `name`, `tags`, and other identifiers remain English/kebab-case.
- **Tone**: Use imperative, technical language. Avoid filler or casual phrasing.
- **Examples**: Include at least 2 examples, one of which must be an edge case or complex scenario.
- **Interaction**: For non-trivial logic, define when to ask the user to confirm.
- **Core Objective**: MUST include Core Objective section with Primary Goal, Success Criteria (3-6 items), and Acceptance Test.
- **Self-Check Alignment**: Self-Check section MUST align with Success Criteria from Core Objective.
- **Scope Boundaries**: SHOULD define what the skill handles vs. what it does NOT handle to prevent overlap with other skills.

### 4.1 Self-Check Requirements

The Self-Check section MUST include:

1. **Core Success Criteria**: Direct mapping from Core Objective's Success Criteria (copy them here for verification)
2. **Process Quality Checks**: Additional checks for process quality (optional but recommended)
3. **Acceptance Test**: Repeat the Acceptance Test from Core Objective for easy reference

**Example**:

```markdown
## Self-Check

### Core Success Criteria (ALL must be met)

- [ ] **Design document exists**: Written to `docs/designs/YYYY-MM-DD-<topic>.md` and committed
- [ ] **User explicitly approved**: User said "approved", "looks good", "proceed", or equivalent
- [ ] **Alternatives documented**: At least 2-3 approaches with trade-offs in design document
- [ ] **YAGNI applied**: Design focuses on minimum viable solution, unnecessary features removed
- [ ] **DRY applied**: Design references existing patterns/components rather than reinventing
- [ ] **No code written**: Zero implementation code exists (design only)

### Process Quality Checks

- [ ] **Context explored**: Did I examine project state, constraints, and existing patterns?
- [ ] **Questions focused**: Did I ask one question at a time?
- [ ] **Alternatives presented**: Did I propose 2-3 distinct approaches with trade-offs?

### Acceptance Test

**Can a developer with zero project context implement this design without asking clarifying questions?**

If NO: Design is incomplete. Return to clarification phase.
If YES: Design is complete. Proceed to handoff.
```

### 4.2 Restrictions Requirements

The Restrictions section SHOULD include:

1. **Hard Boundaries**: Absolute constraints the skill must never violate
2. **Skill Boundaries**: Explicit list of what other skills handle (to avoid overlap)
3. **When to Stop**: Clear conditions for when to stop and hand off to other skills

**Example**:

```markdown
## Restrictions

### Hard Boundaries

- **No premature implementation**: Do NOT write code until design is approved.
- **One question at a time**: Do not overwhelm user with multiple questions.
- **YAGNI ruthlessly**: Remove unnecessary features from all designs.

### Skill Boundaries (Avoid Overlap)

**Do NOT do these (other skills handle them)**:

- **Implementation planning**: Creating detailed task lists → Use `writing-plans`
- **Code writing**: Writing actual code → Use implementation skills
- **Code review**: Reviewing existing code → Use `review-code`
- **Debugging**: Investigating bugs → Use `systematic-debugging`

**When to stop and hand off**:

- User says "approved" → Design complete, hand off to implementation
- User asks "how do we implement?" → Hand off to `writing-plans`
- User asks "can you write code?" → Hand off to development workflow
```

**Why this matters**:

- **Prevents skill overlap**: Clear boundaries prevent multiple skills from doing the same thing
- **Reduces brain split**: AI knows which skill to use for which task
- **Enables composition**: Skills can reference each other for handoffs

### 4.3 Interaction Policy

Skills SHOULD minimize user input by applying these principles. **New skills** (registered after this spec version) MUST satisfy; **existing skills** SHOULD align in future versions.

- **Defaults first**: When a reasonable default exists, use it without asking. Do not require user input for inferable parameters.
- **Prefer choices**: Offer `[A][B][C]` options instead of free-text when possible. Avoid "please describe" unless exploration is needed.
- **Context inference**: Infer from git (status, diff, branch), currently open file, and working directory. The Agent performs inference; ask for confirmation only when inference fails or is ambiguous.
- **Progressive disclosure**: Run with defaults first, then offer follow-up options if the user wants more control.

Each skill's `## Behavior` MUST state: defaults, choice options, and which items require explicit user confirmation.

### 4.4 Invocation and Language

- **Triggers**: Use English only (canonical). Triggers aid exact matching; semantic matching via description/tags supports natural language in any locale.
- **Recommendation**: Prefer English invocation for stable matching. Chinese and other languages are supported via semantic understanding (best-effort).
- **No multi-language triggers**: Do not maintain parallel trigger lists per language; rely on description/tags for non-English intent.

---

## 5. Metadata Sync

- After adding a skill, update `skills/INDEX.md` with the new entry.
- After adding or moving a skill, update `manifest.json` `capabilities` with the new path.
- After adding, removing, or significantly changing skills, update `skills/scenario-map.json` if the skill should appear in scenario-based discovery (see §9).
- **Checklist**: When adding or moving a skill, verify `skills/INDEX.md`, `manifest.json`, and (as needed) `skills/scenario-map.json` are updated together; run `scripts/verify-registry.mjs` (if present) to regenerate docs and confirm sync.
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

### 7.1 Quality Assurance Process

**For new skills**:

1. **Create draft**: Write initial SKILL.md following this spec
2. **Self-check**: Run through Self-Check section, verify all Core Success Criteria met
3. **Refine**: Use `skills/refine-skill-design` to audit and improve the skill
4. **Curate**: Run `skills/curate-skills` to evaluate ASQM score and detect overlaps
5. **Register**: Update `skills/INDEX.md` and `manifest.json`; update `skills/scenario-map.json` if the skill should be discoverable by scenario
6. **Verify**: Run `scripts/verify-registry.mjs` to confirm sync

**For existing skills (migration to new spec)**:

1. **Add Core Objective section**: Define Primary Goal, Success Criteria (3-6 items), Acceptance Test
2. **Update Self-Check**: Align with Success Criteria from Core Objective
3. **Add Skill Boundaries**: Define what this skill does NOT handle (to avoid overlap)
4. **Refine**: Use `skills/refine-skill-design` to audit improvements
5. **Curate**: Run `skills/curate-skills` to re-evaluate ASQM score
6. **Verify**: Run `scripts/verify-registry.mjs` to confirm sync

**Quality gates**:

- ❌ **REJECT** if Core Objective section missing
- ❌ **REJECT** if Success Criteria has < 3 or > 6 items
- ❌ **REJECT** if Self-Check does not align with Success Criteria
- ⚠️ **WARN** if Skill Boundaries section missing (overlap risk)
- ⚠️ **WARN** if ASQM score < 0.7 (quality concern)

### 7.2 Automated Quality Checks

**Registry verification** (MANDATORY):

```bash
node scripts/verify-registry.mjs
```

**Skill curation** (RECOMMENDED):

```bash
# Use curate-skills to evaluate all skills
# Produces ASQM_AUDIT.md with quality scores and overlap detection
```

**Skill refinement** (RECOMMENDED for new skills):

```bash
# Use refine-skill-design to audit and improve skill quality
# Checks: structure, verbs, interaction policy, metadata alignment
```

## 8. I/O Contracts (Optional)

Skills MAY declare structured input and output contracts to support orchestration, chaining, and automated schema matching.

### 8.1 YAML Fields

Add these optional fields to the YAML front-matter:

```yaml
input_schema:
  type: [artifact type]   # findings-list | document-artifact | diagnostic-report | code-scope | free-form
  description: [what this skill consumes]
  defaults:               # optional; for "zero-arg launch" and orchestration
    [param]: [value]      # e.g. scope: diff, untracked: include
output_schema:
  type: [artifact type]
  description: [what this skill produces]
  # For document-artifact: optionally add artifact_type, path_pattern, lifecycle per spec/artifact-contract.md
```

### 8.2 Standard Artifact Types

| Artifact type | Structure | Used by |
| :--- | :--- | :--- |
| `findings-list` | Array of {Location, Category, Severity, Title, Description, Suggestion} | All review skills |
| `document-artifact` | Markdown file written to a specified path | generate-standard-readme, write-agents-entry, brainstorm-design. For paths and naming, see [spec/artifact-contract.md](artifact-contract.md). |
| `diagnostic-report` | Structured summary with sections (Goal, Findings, Recommendations) | review-codebase, onboard-repo |
| `code-scope` | Files, directories, or git diff provided by the caller | review-diff, review-codebase |
| `free-form` | Unstructured text or user input | brainstorm-design, discover-skills |

### 8.3 Document Artifact Path Contract

Skills that produce `document-artifact` outputs (e.g. capture-work-items, brainstorm-design, documentation-readiness, bootstrap-project-documentation) SHOULD align their output paths and naming with [spec/artifact-contract.md](artifact-contract.md). Declare `artifact_type`, `path_pattern`, and `lifecycle` in output_schema when applicable.

### 8.4 Orchestrator Usage

Orchestrators (meta skills) use `input_schema` and `output_schema` to:

1. **Auto-match**: Connect upstream skill output to downstream skill input by artifact type.
2. **Validate**: Ensure chained skills have compatible schemas before execution.
3. **Aggregate**: Merge multiple findings-lists into a single report.

This is backward-compatible: skills without I/O contracts continue to work as before. Orchestrators fall back to manual context passing when contracts are absent.

---

## 9. Repo-level docs (skills directory)

- **`skills/skillgraph.md`**: Auto-generated by `scripts/generate-skillgraph.mjs` from manifest and SKILL frontmatter. Describes how review and other skills compose. For human and Agent reading; INDEX and manifest do not depend on it. Do not edit manually.
- **`skills/scenario-map.json`**: Source of truth for scenario-to-skill mapping. Edit this when adding, removing, or changing scenario mappings. Every skill in primary/optional must exist in INDEX and manifest.
- **`skills/scenario-map.md`**: Auto-generated by `scripts/generate-scenario-map.mjs` from `scenario-map.json`. Task-based discovery; do not edit manually.
- **`skills/ASQM_AUDIT.md`**: Produced by the `curate-skills` skill; lifecycle and ASQM scores. Update by running curate-skills after adding or changing skills. It does not replace INDEX or manifest.

**Regeneration**: `scripts/verify-registry.mjs` runs `scripts/generate-skills-docs.mjs` first (regenerates skillgraph.md and scenario-map.md), then validates. Run `node scripts/verify-registry.mjs` after registry or scenario-map changes.
