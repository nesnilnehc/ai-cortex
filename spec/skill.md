# Skill Specification

Status: MANDATORY  
Version: 2.7.0  
Scope: All files under `skills/`.

**Changelog**:

- v2.7.0 (2026-03-16): Added explicit Divergent (exploratory) + Convergent (decision / artifact) phase model for skills; updated naming, I/O contracts, Behavior, Restrictions, and Self-Check to support two-phase workflows and handoffs
- v2.6.0 (2026-03-16): Made "don't" (Skill Boundaries) mandatory in §4.2 Restrictions; Handoff (When to Stop) optional but recommended; added REJECT gate for missing Skill Boundaries, WARN for missing When to Stop
- v2.5.0 (2026-03-10): Added naming priority rule (§1): semantic correctness and normativity first, colloquial and memorable second
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
- **Avoid**: Pure noun-noun compounds (e.g. `documentation-readiness` → prefer `assess-docs`); abstract compound names without a clear verb.
- **Naming priority** (apply in order):
  1. **Semantic correctness and normativity first**: The verb must accurately describe what the skill does; the name must comply with verb-noun and spec. No semantic drift for colloquialism.
  2. **Colloquial and memorable second**: Prefer natural, easy-to-remember names within the above constraints.
- **Terminology consistency**: For the same semantic concept across skills, use the same term (e.g. `doc` for documentation-related skills: `assess-docs`, `bootstrap-docs`).
- **Divergent / Convergent naming** (full phase definitions and examples: §8.5):
  - **Divergent skills** (option generation, exploration) SHOULD prefer verbs like `brainstorm-`, `ideate-`, `explore-`, `generate-options-`.
  - **Convergent skills** (definition, selection, planning, artifact creation) SHOULD prefer verbs like `define-`, `design-`, `plan-`, `prioritize-`.
  - **Two-phase skills** MAY embed both phases; clearly label phases in Behavior / Execution (e.g. "Divergent phase: brainstorm-X; Convergent phase: define-X") even if implemented in a single SKILL.
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
- **Don't (mandatory)**: Every skill MUST define what it does NOT do (explicit list of responsibilities owned by other skills). This MUST appear in the `## Restrictions` section as **Skill Boundaries** (see §4.2); it may also appear in `## Scope Boundaries`.
- **Handoff (optional)**: Skills SHOULD define when to stop and hand off to other skills or workflows (e.g. in **When to Stop** under Restrictions, or as **Handoff Point** under Core Objective). Recommended for composable or chainable skills.
- **Divergent + Convergent clarity** (for exploratory / decision skills): If a skill performs both **Divergent** (option generation / exploration) and **Convergent** (selection / artifact creation) work, the SKILL MUST:
  - Explicitly describe both phases in `## Behavior` (or an `Execution` / `Execution Process` subsection), including phase names or labels.
  - Declare phase-specific inputs/outputs in `## Input & Output` and, where applicable, in `input_schema` / `output_schema`.
  - Define clear scope boundaries so that the Divergent phase does **not** commit to final decisions or persistent artifacts, and the Convergent phase does **not** reopen open-ended exploration.
  - Document handoff rules: Divergent → Convergent; Convergent → downstream skills (e.g. `define-milestones`, `align-backlog`).

### 4.1 Self-Check Requirements

The Self-Check section MUST include:

1. **Core Success Criteria**: Direct mapping from Core Objective's Success Criteria (copy them here for verification).
2. **Process Quality Checks**: Additional checks for process quality (optional but recommended).
3. **Acceptance Test**: Repeat the Acceptance Test from Core Objective for easy reference.
4. **Phase-specific checks (for Divergent + Convergent skills)**:
   - **Divergent phase**: Checklist MUST verify that multiple options or candidate artifacts were generated, that they stay within scope, and that no final decision or persistent artifact was created.
   - **Convergent phase**: Checklist MUST verify that a decision was made based on the Divergent output, a standardized artifact was produced (e.g. mission, vision, roadmap, milestones), and that persist / handoff requirements were satisfied.

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

The Restrictions section MUST include the following. **Skill Boundaries** (don't) is mandatory to avoid overlap; **When to Stop** (handoff) is optional but recommended for composable skills.

1. **Hard Boundaries**: Absolute constraints the skill must never violate.
2. **Skill Boundaries** (mandatory): Explicit list of what this skill does NOT do and which other skills or workflows handle those responsibilities. Use wording such as "Do NOT do these (other skills handle them): … → Use `skill-name`". This is the canonical don't (out-of-scope) list for the skill.
3. **When to Stop** (optional): Clear conditions for when to stop and hand off to other skills or workflows (e.g. "User says 'approved' → hand off to X", "User asks for Y → hand off to Z"). Recommended when the skill is used in chains or orchestration.
4. **Divergent vs. Convergent scope** (when applicable):
   - **Divergent phase**:
     - Only responsible for generating options, ideas, or exploratory outputs.
     - MUST NOT make final decisions, lock in a single option, or write persistent artifacts (e.g. mission, vision, roadmap documents).
     - MUST document the **handoff condition** to the Convergent phase (same SKILL or another SKILL).
   - **Convergent phase**:
     - Only responsible for selecting, evaluating, and aggregating from existing candidates.
     - MUST NOT introduce entirely new options beyond the previously generated scope (except minor refinements or synthesis).
     - MUST produce a standardized artifact or structured output that is explicitly usable by downstream skills, and document the **handoff condition** to those skills.

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

**Execution process and phases**:

- For skills that have clearly separated phases (e.g. Divergent → Convergent), `## Behavior` SHOULD describe the **execution process** in terms of:
  - **Phase names** (e.g. "Divergent phase: brainstorm-options", "Convergent phase: define-mission").
  - **Per-phase inputs** (what the Agent expects at the start of the phase).
  - **Per-phase outputs** (what is produced, and whether it is transient or persistent).
  - **Per-phase interaction** (when to ask the user to choose options, approve a selection, or trigger the next phase).
- When both phases are implemented inside the same SKILL, clearly document how the Convergent phase is triggered (e.g. "second invocation with `mode: convergent`", "user explicitly chooses 'go to definition phase'").

### 4.4 Invocation and Language

- **Triggers**: Use English only (canonical). Triggers aid exact matching; semantic matching via description/tags supports natural language in any locale.
- **Recommendation**: Prefer English invocation for stable matching. Chinese and other languages are supported via semantic understanding (best-effort).
- **No multi-language triggers**: Do not maintain parallel trigger lists per language; rely on description/tags for non-English intent.

---

## 5. Metadata Sync

- After adding a skill, update `manifest.json` and SKILL frontmatter, then regenerate `skills/INDEX.md`.
- After adding or moving a skill, update `manifest.json` `capabilities` with the new path.
- After adding, removing, or significantly changing skills, update `skills/scenario-map.json` if the skill should appear in scenario-based discovery (see §9).
- **Checklist**: When adding or moving a skill, verify `manifest.json` and (as needed) `skills/scenario-map.json` are updated; run `scripts/verify-registry.mjs` (if present) to regenerate INDEX/docs and confirm sync.
- **Publish for npx skills**: `npx skills add owner/repo --skill <name>` clones the default branch from the remote. Push the commit that adds the skill and updated manifest (INDEX is generated) so the skill is discoverable and installable.
- Versions must follow [SemVer](https://semver.org/).

## 6. agentskills Compatibility

- This spec aligns with [agentskills.io](https://agentskills.io) and skills.sh. `license` and `metadata.author` are used for catalog and trust; `metadata.author` is `ai-cortex`.
- This spec may be stricter than agentskills.io as long as it does not conflict with the upstream requirements.
- **Optional directories** (agentskills.io): `scripts/`, `references/`, `assets/`. Use relative paths, keep depth shallow.
- **Progressive disclosure**: Keep main `SKILL.md` ≤500 lines; move detail to `references/` and load on demand.

## 7. Extension and Contribution

- New skills must satisfy this spec; use `skills/refine-skill-design` for design review.
- Version registration: update SKILL frontmatter and regenerate `skills/INDEX.md` with linear version bumps.
- Installation: see [README.md](../README.md).

### 7.1 Quality Assurance Process

**For new skills**:

1. **Create draft**: Write initial SKILL.md following this spec
2. **Self-check**: Run through Self-Check section, verify all Core Success Criteria met
3. **Refine**: Use `skills/refine-skill-design` to audit and improve the skill
4. **Curate**: Run `skills/curate-skills` to evaluate ASQM score and detect overlaps
5. **Register**: Update `manifest.json`; update `skills/scenario-map.json` if the skill should be discoverable by scenario
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
- ❌ **REJECT** if Restrictions section missing **Skill Boundaries** (don't — what this skill does NOT do and which skills handle it)
- ⚠️ **WARN** if Restrictions section missing **When to Stop** (handoff conditions; recommended for composable skills)
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
  # For two-phase skills, clarify whether this is the Divergent (transient) or Convergent (persistent) output, or both
```

### 8.2 Standard Artifact Types

| Artifact type | Structure | Used by |
| :--- | :--- | :--- |
| `findings-list` | Array of {Location, Category, Severity, Title, Description, Suggestion} | All review skills |
| `document-artifact` | Markdown file written to a specified path | generate-standard-readme, generate-agent-entry, define-mission, define-vision, define-roadmap, define-milestones, design-solution. For paths and naming, see [spec/artifact-contract.md](artifact-contract.md). |
| `diagnostic-report` | Structured summary with sections (Goal, Findings, Recommendations) | review-codebase, run-checkpoint |
| `code-scope` | Files, directories, or git diff provided by the caller | review-diff, review-codebase |
| `free-form` | Unstructured text or user input | design-solution, discover-skills, brainstorm-mission, brainstorm-roadmap |

### 8.3 Document Artifact Path Contract

Skills that produce `document-artifact` outputs (e.g. capture-work-items, design-solution, assess-docs, bootstrap-docs) SHOULD align their output paths and naming with [spec/artifact-contract.md](artifact-contract.md). Declare `artifact_type`, `path_pattern`, and `lifecycle` in output_schema when applicable.

### 8.4 Orchestrator Usage

Orchestrators (meta skills) use `input_schema` and `output_schema` to:

1. **Auto-match**: Connect upstream skill output to downstream skill input by artifact type.
2. **Validate**: Ensure chained skills have compatible schemas before execution.
3. **Aggregate**: Merge multiple findings-lists into a single report.

This is backward-compatible: skills without I/O contracts continue to work as before. Orchestrators fall back to manual context passing when contracts are absent.

### 8.5 Divergent + Convergent Phase Patterns (Optional but Recommended)

To explicitly support **Divergent (exploratory)** and **Convergent (decision / artifact)** phases, skills MAY use the following patterns.

#### 8.5.1 Phase Definitions

- **Divergent phase**:
  - Purpose: Generate multiple options, ideas, scenarios, or rough candidates.
  - Inputs: Usually `free-form` context (e.g. "current product strategy", "vision draft") and constraints.
  - Outputs: Non-persistent, exploratory results such as lists of options, bullet-point candidates, sketches of missions/visions/roadmaps.
  - Scope: MUST NOT write final mission/vision/roadmap/milestones documents or commit to a single option.
  - Interaction: Encourage user / Agent to react, annotate, and narrow down preferences.
- **Convergent phase**:
  - Purpose: Select, evaluate, and aggregate from existing options into a standardized artifact.
  - Inputs: The Divergent output (options / candidates), plus user preferences or selection criteria.
  - Outputs: Persistent `document-artifact` or structured objects, such as `mission`, `vision`, `strategic-goals`, `roadmap`, `milestones`.
  - Scope: MUST NOT reopen broad exploration or introduce unrelated new options; focuses on refinement and decision.
  - Interaction: Ask for explicit confirmation before finalizing and persisting.

#### 8.5.2 Naming Patterns

- **Divergent skills** (examples):
  - `brainstorm-mission`
  - `ideate-vision`
  - `generate-options-roadmap`
  - `brainstorm-strategic-pillars`
- **Convergent skills** (examples):
  - `define-mission`
  - `define-vision`
  - `define-roadmap`
  - `design-strategic-goals`
  - `define-milestones`
- **Two-phase skills**:
  - May keep a single name (e.g. `design-solution`) but MUST document:
    - Phase labels (e.g. "Divergent mode" vs "Convergent mode").
    - How to trigger each phase (input flag, explicit user request, second invocation).
    - Which outputs are transient (Divergent) vs. persistent (Convergent).

#### 8.5.3 Input / Output Examples

**Example: Divergent-only skill (`brainstorm-mission`)**:

```yaml
name: brainstorm-mission
description: Generate multiple candidate mission statements for a product or organization.
tags: [strategy, mission, divergent]
version: 1.0.0
license: MIT
input_schema:
  type: free-form
  description: Context about the organization, users, and constraints for the mission.
output_schema:
  type: free-form
  description: List of 5–10 candidate mission statements with short rationales (Divergent, non-final).
```

- **Behavior / Execution** SHOULD state:
  - "This skill only performs a Divergent phase (option generation). It does not decide or persist a final mission."
  - "Handoff: When the user is ready to converge, hand off to `define-mission`."

**Example: Convergent-only skill (`define-mission`)**:

```yaml
name: define-mission
description: Converge from mission options to a single, approved mission statement and write it as a document artifact.
tags: [strategy, mission, convergent]
version: 1.0.0
license: MIT
input_schema:
  type: free-form
  description: Candidate mission statements from a Divergent skill (e.g. brainstorm-mission) plus selection criteria.
output_schema:
  type: document-artifact
  description: Final mission statement, persisted as a Markdown artifact.
  artifact_type: mission
  path_pattern: docs/project-overview/mission.md
  lifecycle: source-of-truth
```

- **Behavior / Execution** SHOULD state:
  - "This skill only performs a Convergent phase (selection and definition). It does not explore new, unrelated mission options."
  - "Handoff in: Expects options from `brainstorm-mission` or equivalent Divergent work."
  - "Handoff out: After writing `mission.md`, downstream skills like `define-vision` or `define-roadmap` may consume it."

**Example: Two-phase skill (Divergent + Convergent inside one SKILL)**:

```yaml
name: design-strategic-goals
description: Explore candidate strategic goals and converge on a prioritized, documented set of strategic pillars.
tags: [strategy, goals, divergent, convergent]
version: 1.0.0
license: MIT
input_schema:
  type: free-form
  description: Context about mission, vision, and constraints.
output_schema:
  type: document-artifact
  description: Final set of strategic goals / pillars, ready for downstream roadmap planning.
  artifact_type: strategic-goals
  path_pattern: docs/project-overview/strategic-goals.md
  lifecycle: source-of-truth
```

- **Behavior / Execution** MUST clarify:
  - **Divergent phase**: "Generate 10–20 candidate goals with rationale; mark this output as transient and present for review."
  - **Convergent phase**: "After user selects or refines, synthesize into 3–7 strategic pillars and write them to `strategic-goals.md`."
  - **Trigger**: e.g. `mode: divergent` vs `mode: convergent`, or "first invocation is Divergent, second (after approval) is Convergent."
  - **Handoff**: "Downstream skills like `define-roadmap` and `define-milestones` can consume `strategic-goals.md`."

#### 8.5.4 Handoff Rules

- **Divergent → Convergent**:
  - When Divergent exploration is complete (enough options, clarified preferences), the skill SHOULD:
    - Summarize options and trade-offs.
    - Ask the user whether to proceed to convergence.
    - Either:
      - Trigger its own Convergent phase (if two-phase skill), or
      - Explicitly recommend a Convergent skill (e.g. "Use `define-roadmap` with these options.").
- **Convergent → Downstream**:
  - When Convergent decision and artifact creation are complete, the skill SHOULD:
    - Confirm the persistent artifact path and type (e.g. mission, vision, roadmap, milestones).
    - Mention typical downstream skills (e.g. `define-milestones`, `align-backlog`, `capture-work-items`) that can consume the artifact.
    - Clarify that further exploration (new divergent options) is out of scope and should be handled by the Divergent skill again if needed.

---

## 9. Repo-level docs (skills directory)

- **`skills/INDEX.md`**: Auto-generated by `scripts/generate-skills-index.mjs` from manifest and SKILL frontmatter. Human-readable catalog for name, tags, version, stability, and purpose. Do not edit manually.
- **`skills/skillgraph.md`**: Auto-generated by `scripts/generate-skillgraph.mjs` from manifest and SKILL frontmatter. Describes how review and other skills compose. For human and Agent reading; INDEX and manifest do not depend on it. Do not edit manually.
- **`skills/scenario-map.json`**: Source of truth for scenario-to-skill mapping. Edit this when adding, removing, or changing scenario mappings. Every skill in primary/optional must exist in INDEX and manifest.
- **`skills/scenario-map.md`**: Auto-generated by `scripts/generate-scenario-map.mjs` from `scenario-map.json`. Task-based discovery; do not edit manually.
- **`skills/ASQM_AUDIT.md`**: Produced by the `curate-skills` skill; lifecycle and ASQM scores. Update by running curate-skills after adding or changing skills. It does not replace INDEX or manifest.

**Regeneration**: `scripts/verify-registry.mjs` runs `scripts/generate-skills-docs.mjs` first (regenerates INDEX.md, skillgraph.md, and scenario-map.md), then validates. Run `node scripts/verify-registry.mjs` after registry or scenario-map changes.
