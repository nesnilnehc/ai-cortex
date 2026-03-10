---
name: discover-skills
description: Identify missing skills and recommend installations from AI Cortex or public skill catalogs. Core goal - provide top 1-3 skill matches with install commands for Agent capability gaps. Use when discovering capabilities or suggesting skills to fill gaps.
tags: [automation, infrastructure, generalization]
version: 1.3.0
license: MIT
related_skills: [refine-skill-design]
recommended_scope: user
metadata:
  author: ai-cortex
triggers: [discover skills, find skills]
input_schema:
  type: free-form
  description: Task description, capability gap, or user query about available skills
output_schema:
  type: free-form
  description: Skill recommendations with install commands and capability gap analysis
---

# Skill: Discover Skills

## Purpose

Help the Agent identify missing skills for a task and recommend concrete installation steps. This skill discovers candidates and suggests what to install, but does not install or inject skills automatically.

---

## Core Objective

**Primary Goal**: Provide the Agent with top 1-3 skill recommendations and exact installation commands to fill capability gaps.

**Success Criteria** (ALL must be met):

1. ✅ **Discovery performed**: Searched local `skills/INDEX.md` and `manifest.json`, or external catalogs if requested
2. ✅ **Best matches identified**: Selected 1-3 skills that match task requirements by name, description, and tags
3. ✅ **Recommendations explained**: Provided rationale for why each skill matches the current task
4. ✅ **Install commands provided**: Included exact installation command for each recommended skill
5. ✅ **No auto-install**: Did not execute installation commands without explicit user confirmation

**Acceptance Test**: Can the Agent or user install the recommended skills using the provided commands without additional research?

---

## Scope Boundaries

**This skill handles**:

- Discovering skills from local indexes or external catalogs
- Matching task requirements to skill capabilities
- Recommending top 1-3 skill matches with rationale
- Providing exact installation commands

**This skill does NOT handle**:

- Installing skills automatically (use `install-rules` or manual installation)
- Curating or auditing existing skills (use `curate-skills`)
- Refining or designing skills (use `refine-skill-design`)
- Injecting skill content into Agent context (handled by Agent runtime)

**Handoff point**: When recommendations are provided with install commands, hand off to user for installation decision or to `install-rules` for automated installation (with user confirmation).

---

## Use Cases

- **Initial bootstrap**: The Agent starts with only this skill, then recommends which skills to install for the current task.
- **On-demand extension**: When a task requires a Skill that is not available, suggest the best matches and how to install them.
- **Capability discovery**: Help users find relevant skills from local indexes or public catalogs.

## Behavior

1. **Discovery**: Prefer local `skills/INDEX.md` and `manifest.json` for the capability map. If the user asks for external options and network access is available, search a public catalog (e.g. SkillsMP).
2. **Matching**: Match the user task to `name`, `description`, and `tags`; select the best 1–3 skills.
3. **Recommendation**: Explain why each skill matches and whether it is local or external.
4. **Installation guidance**: Provide the exact install command for each recommended skill (e.g. `npx skills add owner/repo --skill name`).
5. **Confirmation**: If the user asks the Agent to install, request explicit confirmation before running any command.

## Input & Output

- **Input**:
  - Description of the current task.
  - Optional: list of already installed skills.
  - Optional: allowed sources (local only vs public catalogs).
- **Output**:
  - Recommended skills with rationale.
  - Install commands for each recommendation.

## Restrictions

### Hard Boundaries

- **No auto-install**: Do not execute install commands without explicit user confirmation.
- **No auto-injection**: Do not fetch or inject remote SKILL.md content automatically.
- **No bulk discovery**: Avoid listing large catalogs; return only the top 1–3 matches.

### Skill Boundaries (Avoid Overlap)

**Do NOT do these (other skills handle them)**:

- **Installing skills**: Executing installation commands or modifying skill directories → Use `install-rules` or manual installation with user confirmation
- **Curating skills**: Auditing skill quality, detecting overlaps, or scoring skills → Use `curate-skills`
- **Refining skills**: Designing, restructuring, or improving existing skill content → Use `refine-skill-design`
- **Injecting content**: Loading skill content into Agent context or runtime → Handled by Agent runtime system

**When to stop and hand off**:

- User says "install it" or "add that skill" → Provide install command, request confirmation, hand off to `install-rules` or manual installation
- User asks "how do I improve this skill?" → Hand off to `refine-skill-design`
- User asks "are my skills good quality?" → Hand off to `curate-skills`
- Recommendations provided with install commands → Discovery complete, await user decision

## Self-Check

### Core Success Criteria (ALL must be met)

- [ ] **Discovery performed**: Searched local `skills/INDEX.md` and `manifest.json`, or external catalogs if requested
- [ ] **Best matches identified**: Selected 1-3 skills that match task requirements by name, description, and tags
- [ ] **Recommendations explained**: Provided rationale for why each skill matches the current task
- [ ] **Install commands provided**: Included exact installation command for each recommended skill
- [ ] **No auto-install**: Did not execute installation commands without explicit user confirmation

### Process Quality Checks

- [ ] **Relevance**: Are the recommendations strongly related to the current task?
- [ ] **Actionable**: Are install commands concrete and correct?
- [ ] **Consent**: Did the Agent avoid running installs without explicit confirmation?
- [ ] **Source priority**: Did I prefer local indexes before searching external catalogs?
- [ ] **Conciseness**: Did I limit recommendations to top 1-3 matches, avoiding bulk catalog listings?

### Acceptance Test

**Can the Agent or user install the recommended skills using the provided commands without additional research?**

If NO: Recommendations are incomplete. Verify install commands are correct and include all necessary parameters.

If YES: Discovery is complete. Await user decision on installation.

## Examples

### Example 1: Recommend a local skill

- **Scenario**: User asks for a standardized README.
- **Steps**:
  1. Agent checks `skills/INDEX.md`.
  2. Finds `generate-standard-readme`.
  3. Recommends it and provides: `npx skills add nesnilnehc/ai-cortex --skill generate-standard-readme`.

### Example 2: Edge case - no local match

- **Scenario**: The task is niche and no local skill matches.
- **Expected**: Offer 1–3 external suggestions (if allowed) with install commands, or say "no match found" and ask for clarification. Do not install automatically.

---

## Appendix: Output contract

When this skill produces recommendations, it follows this contract:

| Element | Requirement |
| :--- | :--- |
| Count | Top 1–3 matches only; no bulk catalog listing. |
| Per skill | Name, rationale (why it matches), install command (e.g. `npx skills add owner/repo --skill name`). |
| Source | Prefer local `skills/INDEX.md` and `manifest.json`; external only when user asks and network available. |
| Interaction | Do not run install commands without explicit user confirmation. |
