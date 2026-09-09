---
name: define-mission
description: Define the fundamental purpose of a project or organization. Answers why the project exists; produces a single mission statement persisted to docs.
description_zh: 定义项目或组织的根本目的；回答项目为何存在；产出 mission 陈述并持久化到 docs。
tags: [documentation, workflow]
version: 1.4.0
license: MIT
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

> **Role**: the first layer of the strategy chain, defining the fundamental purpose behind the project
> **WHAT**: a single mission statement (1–3 sentences, stating only "why it exists")
> **HOW**: elicit the purpose from README/docs/the user, confirm it with the user, then write it to the agreed path
> **Distinction**: vision (future state) → `define-vision`; metric → `define-north-star`; goals → `design-strategic-goals`

## Purpose

Define and record the mission: the lasting reason a project or organization exists. A mission statement answers "why does this exist?", holds to the outcome (the purpose we serve) rather than the implementation (how we work or what we build), and stays stable while the roadmap or the feature set changes.

## Core Goal

**Primary goal**: produce a single, user-confirmed mission statement and persist it to the agreed path.

**Success criteria**:
1. ✅ A mission statement exists: 1–2 sentences (3 at most), stating the fundamental purpose alone
2. ✅ The user approved it explicitly ("approved", "looks good", and the like)
3. ✅ It was written to the agreed path (default `docs/project-overview/mission.md`, overridden by project norms)
4. ✅ No vision, metric, goal, milestone or implementation detail is mixed in
5. ✅ The wording is stable: independent of features or schedule

**Acceptance test**: can a new team member understand why the project exists from the mission alone?

## Scope Boundary

**This skill owns**: eliciting the fundamental purpose; drafting a 1–2 sentence mission; confirming with the user; writing to the agreed path.

**This skill does not own** (handed off to the named skill):
- Vision → `define-vision`
- North star metric → `define-north-star`
- Strategic goals → `design-strategic-goals`
- Milestones/roadmap → `define-roadmap`

**Handoff point**: once the mission is approved → `define-vision` is the suggested next step.

## When to Use

- Defining "why we exist" for a new project or a strategy refresh
- The team reads the direction differently and needs a single source
- The start of the strategy chain (mission → vision → north-star → goals → roadmap)

## Behavior

**Execution**:
1. Load context: project name, domain, the existing understanding of the purpose (README, existing docs, the user's description)
2. Elicit: for whom? what fundamental problem does it solve? why is it worth doing?
3. Draft the mission statement (1–2 sentences, purpose only, no future state/metric/goal/feature)
4. Confirm with the user; when a candidate carries buzzwords or implementation detail, prompt for a rewrite
5. Persist to the agreed path; overwriting an existing file must be confirmed first

## Input and Output

**Input**: the project identifier; the existing understanding of the purpose (from README, docs or the user).

**Output**: the mission statement as a Markdown document; the path is given by the frontmatter `output_schema.path_pattern`; lifecycle living.

## Limits

- **MUST NOT** put vision, metrics, goals, milestones, features or implementation detail into the mission statement
- **MUST NOT** overwrite an existing mission.md without user confirmation
- **MUST** apply YAGNI: the statement is the core; add an optional paragraph ("for whom", "what problem it solves") only where there is a real need

## Anti-Patterns

### ✅ Right: centred on the outcome

Input: the README says "we built a CLI with YAML configuration, rollback and audit logs"
Mission draft: "We exist to give teams a reliable, auditable way to deploy, with rollback and a clear history."

**Why it is right**: it holds to the purpose (reliable deployment) and lists no features (YAML, CLI).

### ❌ Wrong: features or future state mixed in

Bad draft: "We built a CLI with one-click deployment, and by 2027 we will have the fastest rollback in the industry."

**The problem**: it lists a feature ("one-click CLI") and a metric/future state ("fastest by 2027"). Features belong in the product documentation, future state in the vision.

## Examples

### Example 1: mission only, kept apart from the vision

**Context**: the user says "our deployment tool needs a mission; the vision can wait."

**Flow**: elicit the who (engineering teams), the problem (manual deployment is error-prone) and the why (reliability, safety). Draft: "We exist to give engineering teams one reliable way to take a service from code to production, with manual steps at a minimum and safety at a maximum." The user confirms → write to `docs/project-overview/mission.md`.

### Example 2: a mission already exists and a rewrite is requested (edge case)

**Context**: the existing mission.md carries product feature descriptions.

**Flow**: read the existing version and pick out the feature-description parts. Extract the purpose: why does the customer need this product? Draft a trimmed version (purpose only). The user must confirm before it is overwritten; the old version stays in git history for traceability.

## AI Refactoring Instructions

### Problem: the mission statement carries future state or metrics

**Detection**: the statement contains wording such as "by YYYY", "deliver an X% improvement", "become the fastest/largest".

**Correction**:
1. Identify the future-state/metric fragment
2. Tell the user: "this part belongs to the vision or the north star; suggest removing it from the mission"
3. Rewrite it as a pure purpose statement
4. Suggest running `define-vision` or `define-north-star` to take over what was removed

### Problem: the mission statement lists features

**Detection**: the statement contains wording such as "we built X", "includes features A, B, C".

**Correction**: rewrite "we built X" into "we exist to Y", turning the feature view into a purpose view.

## Self-Check

- [ ] The mission statement is 1–2 sentences (3 at most), purpose only
- [ ] The user has confirmed it
- [ ] It was written to the agreed path
- [ ] No vision/metric/goal/milestone/feature is mixed in
- [ ] The wording is independent of any schedule
