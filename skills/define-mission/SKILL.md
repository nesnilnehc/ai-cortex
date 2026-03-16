---
name: define-mission
description: Define the fundamental purpose of a project or organization. Answers why the project exists; produces a single mission statement persisted to docs.
tags: [documentation, workflow, eng-standards]
version: 1.1.0
license: MIT
related_skills: [define-vision, define-north-star, design-strategic-goals, bootstrap-docs]
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [define mission, mission, why we exist]
input_schema:
  type: free-form
  description: Project or product identifier; current understanding of purpose from docs, README, or user
output_schema:
  type: document-artifact
  description: Mission statement written to docs/project-overview/mission.md (or project norms)
  artifact_type: mission
  path_pattern: docs/project-overview/mission.md
  lifecycle: living
---

# Skill: Define Mission

## Purpose

Define and document the **mission**: the enduring reason the project or organization exists. A mission statement answers "Why does this exist?" and remains stable across roadmap or feature changes. It is outcome-focused (what purpose we serve), not implementation (how we do it or what we build).

**Mission is distinct from**:

- **Vision**: Long-term future state we aim to create (use `define-vision`).
- **North Star**: Single metric representing value delivered (use `define-north-star`).
- **Strategic Goals**: 3–5 outcomes that move toward the vision (use `design-strategic-goals`).
- **Milestones**: Phase checkpoints for execution (use `define-milestones`).

---

## Core Objective

**Primary Goal**: Produce a single, user-confirmed mission statement and persist it to the project-agreed path.

**Success Criteria** (ALL must be met):

1. ✅ **Mission statement exists**: One to two sentences (three maximum) stating the fundamental purpose only — no future state, no metrics, no goals, no implementation or features.
2. ✅ **User confirmed**: User explicitly approved (e.g. "approved", "looks good", "proceed", or equivalent).
3. ✅ **Document persisted**: Written to agreed path (default `docs/project-overview/mission.md` or per project norms).
4. ✅ **Scope respected**: Statement does not describe vision, North Star metric, strategic goals, or milestones.
5. ✅ **Stable wording**: Mission is independent of features or timelines; a new reader can infer "why we exist" in under a minute.

**Acceptance Test**: Can a new team member read the mission and immediately understand why this project exists, without reading other docs?

**Handoff Point**: When mission is approved and persisted, hand off to `define-vision` to define the long-term future, or stop if only mission was requested.

---

## Scope Boundaries

### What this skill MUST do

- Identify the core purpose (why the project or organization exists).
- Identify who benefits (for whom).
- Articulate the fundamental problem or need addressed.
- Produce a concise mission statement (1–2 sentences preferred, max 3).
- Optional: capture "for whom" and "core problem addressed" in 1–2 lines in the artifact.
- Persist to project-agreed path (default `docs/project-overview/mission.md`).

### What this skill must NOT do

- Define future state (use `define-vision`).
- Define metrics or North Star (use `define-north-star`).
- Define strategic goals (use `design-strategic-goals`).
- Define milestones (use `define-milestones`).
- Describe implementation, features, or roadmap (use requirements, design, or planning skills).
- Include buzzwords, implementation language, or internal jargon in the mission statement.

---

## Mission Quality Guidelines

A strong mission statement should be:

- **Short**: 1–2 sentences preferred; maximum 3.
- **Purpose-driven**: States why we exist and what need we address, not what we build.
- **Outcome-focused**: Describes the outcome or value (e.g. "give teams a reliable way to deploy") rather than the product (e.g. "we build a deployment tool").
- **Understandable by non-experts**: No internal jargon; a new team member or stakeholder can grasp it quickly.
- **Stable over time**: Independent of current features, roadmap, or timelines; only changes when the fundamental purpose changes.

Avoid in the mission statement:

- **Buzzwords**: Vague or fashionable terms that do not clarify purpose.
- **Implementation language**: Technologies, deliverables, or "how" we do it.
- **Internal jargon**: Terms that require project-specific context to understand.

---

## Use Cases

- **New project or initiative**: Establish "why we exist" before vision or strategy.
- **Strategy refresh**: Re-anchor the project when direction is unclear.
- **Alignment discussions**: Provide a single source of truth for purpose when teams lack a clear "why".
- **Top of strategy chain**: Run first when building the full strategic hierarchy (mission → vision → north star → goals → milestones).

---

## Behavior

### Interaction Policy

- **Defaults**: Output path from project norms if present (`docs/ARTIFACT_NORMS.md` or `.ai-cortex/artifact-norms.yaml`); otherwise `docs/project-overview/mission.md`. Infer "why we exist" from README or existing docs when available.
- **Choice options**: If multiple plausible purposes exist, offer 1–3 candidate statements and ask user to pick or refine.
- **Confirm**: Before overwriting an existing mission file; before final persist.

### Execution Process

1. **Gather context**: Project/product name, domain, and current understanding of purpose (from docs, README, or user).
2. **Elicit**: Who is this for? What fundamental problem or need does it address? Why is it worth doing?
3. **Draft**: One mission statement (1–2 sentences preferred, max 3); purpose only — no future state, no metrics, no goals, no implementation or features.
4. **Validate**: Apply Mission Quality Guidelines; ask user whether the statement captures "why this project exists".
5. **Persist**: Write to project-agreed path; create `docs/project-overview/` if missing.

---

## Input & Output

**Input**:

- **Required**: Project or product identifier; access to or summary of current "why we exist" (from docs, README, or user).
- **Optional**: Existing mission draft, audience description, problem statement.

**Output**:

- **Artifact**: Single mission statement (1–2 sentences preferred, max 3).
- **Location**: `docs/project-overview/mission.md` (or per project norms).
- **Content**: Mission statement; optional 1–2 lines for "For whom", "Core problem addressed".
- **Lifecycle**: Living (update only when purpose changes).

---

## Restrictions

### Hard Boundaries

- Do NOT include vision, North Star metric, strategic goals, or milestones in the mission statement.
- Do NOT include implementation details, features, or roadmap in the mission statement.
- Do NOT overwrite an existing mission file without explicit user confirmation.
- Do NOT write more than one artifact; this skill produces only the mission document.

### Skill Boundaries (Avoid Overlap)

**Do NOT do these (other skills handle them)**:

- **Vision**: Long-term future state → Use `define-vision`.
- **North Star metric**: Single key metric → Use `define-north-star`.
- **Strategic goals**: 3–5 outcomes → Use `design-strategic-goals`.
- **Milestones**: Phase checkpoints → Use `define-milestones`.
- **Requirements or roadmap**: Use `analyze-requirements`, project planning, or `bootstrap-docs`.

**When to stop and hand off**:

- User says "approved" or equivalent → Mission complete; offer handoff to `define-vision`.
- User asks for vision or "what future" → Hand off to `define-vision`.
- User asks for metrics or goals → Hand off to `define-north-star` or `design-strategic-goals`.

---

## Self-Check

### Core Success Criteria (ALL must be met)

- [ ] **Mission statement exists**: One to two sentences (max 3), purpose only (no vision, metrics, goals, implementation).
- [ ] **User confirmed**: User said "approved", "looks good", "proceed", or equivalent.
- [ ] **Document persisted**: Written to agreed path (default `docs/project-overview/mission.md` or project norms).
- [ ] **Scope respected**: No vision, North Star, goals, or milestones in the statement.
- [ ] **Stable wording**: Mission is independent of features or timelines.

### Process Quality Checks

- [ ] **Context used**: Did I use README or existing docs to infer purpose when available?
- [ ] **One purpose**: Did I avoid mixing in future state, metrics, or implementation?
- [ ] **Quality guidelines**: Did I apply Mission Quality Guidelines (short, purpose-driven, no buzzwords/jargon)?

### Acceptance Test

**Can a new team member read the mission and immediately understand why this project exists?**

If NO: Mission is incomplete or mixed with vision/goals/features. Simplify to purpose only.
If YES: Mission is complete. Proceed to handoff or stop.

---

## Examples

### Example 1: Mission only — separate from vision

**Context**: User says "We need a mission for our deployment tool. We're also thinking about our vision later."

**Process**: Elicit purpose: who (engineering teams), what problem (manual, error-prone deploys), why it matters (reliability, safety). Draft mission: "We exist to give engineering teams a single, reliable way to deploy services from code to production with minimal manual steps and maximum safety." Do not add future state (e.g. "one-click deploy by 2027"). User confirms. Persist to `docs/project-overview/mission.md`.

**Outcome**: Mission is purpose-only; vision can be defined later with `define-vision`.

### Example 2: Purpose, not features

**Context**: Repo README says "We build a CLI that supports YAML configs, rollback, and audit logs."

**Process**: Extract purpose: the CLI exists to serve a need (reliable, auditable deployments), not to "build a CLI." Draft: "We exist to give teams a reliable, auditable way to deploy with rollback and clear history." Avoid listing features (YAML, CLI) in the mission. Ask user to confirm or refine. If mission file already exists, ask before overwriting.

**Outcome**: Mission is outcome-focused; features stay in product docs.
