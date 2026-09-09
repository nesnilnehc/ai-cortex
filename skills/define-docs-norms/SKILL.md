---
name: define-docs-norms
description: Create or update docs/ARTIFACT_NORMS.md from an approved proposal and establish project docs norms as canonical rules.
description_zh: 基于已确认提案创建或更新 docs/ARTIFACT_NORMS.md，建立项目文档规范的单一权威来源。
tags: [documentation, workflow]
version: 3.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [define docs norms, create docs norms, apply norms]
input_schema:
  type: free-form
  description: Approved norms proposal, optional existing ARTIFACT_NORMS.md, optional merge strategy
output_schema:
  type: document-artifact
  description: Canonical docs norms file
  artifact_type: governance
  path_pattern: docs/ARTIFACT_NORMS.md
  lifecycle: living
---

# Skill: Define Docs Norms

## Purpose

Fix a reviewed norms proposal into `docs/ARTIFACT_NORMS.md` and make it the canonical rule set for the project's documentation governance.

---

## Core Objective

**Primary goal**: create or update the project norms file safely and auditably.

**Success criteria** (all of them must hold):

1. ✅ The input proposal is unambiguous and ready to write
2. ✅ The norms file structure matches the project schema and conventions
3. ✅ The change notes are clear (rules added, modified, removed)
4. ✅ The only write target is `docs/ARTIFACT_NORMS.md`
5. ✅ The output can be consumed directly by runtime / linter / CI tooling (per `rules/doc-health-criteria.md`)

**Acceptance test**: can the norms file serve directly as the basis for path/naming/front-matter validation, and be parsed reliably by other skills?

---

## Scope Boundaries

**This skill owns**:

- Creating or updating `docs/ARTIFACT_NORMS.md`
- Merging existing norms with a new proposal (configurable strategy)
- Emitting the change summary and migration notes

**This skill does not own**:

- Discovering and deriving norms (a person or the AgentFabric runtime takes that)
- Repository tidying and file migration (per `rules/repo-structure-hygiene.md`, carried out by the AgentFabric runtime or by a person)
- Compliance audit and readiness scoring (runtime / linter / CI tooling takes that)

**Handoff point**: once the norms are written, structural cleanup and compliance checking are carried out by runtime / linter / CI tooling per `rules/repo-structure-hygiene.md` and `rules/doc-health-criteria.md`.

---

## Use Cases

- A new project establishing `ARTIFACT_NORMS` for the first time
- An existing project promoting a proposal into formal rules
- Iterating on the norms (paths, naming, field policy)

---

## Behavior

### Stage 1: confirm the input

1. Read the proposal (usually from `docs/calibration/docs-norms-proposal.md`)
2. Check whether an older `docs/ARTIFACT_NORMS.md` exists
3. Confirm the write strategy: `create | merge | replace`

### Stage 2: assemble the norms

1. Assemble the path mapping, the naming policy and the front-matter standard
2. Write a manual-confirmation note for any low-confidence rule (where there is one)
3. Validate format consistency and parseability

### Stage 3: write and summarize

1. Write `docs/ARTIFACT_NORMS.md`
2. Emit the change summary for this pass (added/modified/removed)
3. Emit the suggested next steps: the runtime tidies up per `rules/repo-structure-hygiene.md`, plus compliance checking per `rules/doc-health-criteria.md`

---

## Input and Output

### Input

- The reviewed norms proposal
- Optionally an existing `docs/ARTIFACT_NORMS.md`
- Optionally a merge strategy (`create|merge|replace`)

### Output

- `docs/ARTIFACT_NORMS.md`
- The change summary

---

## Restrictions

### Hard Boundaries

- Writing the norms file is the only write allowed; no repository restructuring is performed
- Stop and ask for confirmation when the input proposal is ambiguous
- Must not mark an unresolved conflicting rule as settled

### Skill Boundaries

**Do not do these (other skills own them)**:

- Discovery and derivation: a person or the AgentFabric runtime
- Compliance scoring: runtime / linter / CI tooling (per `rules/doc-health-criteria.md`)
- File tidying: the runtime, per `rules/repo-structure-hygiene.md`

---

## Self-Check

- [ ] A rule input ready to write was received
- [ ] `docs/ARTIFACT_NORMS.md` was written correctly
- [ ] The rule change summary was emitted
- [ ] No write outside the norms file was performed

---

## Examples

### Example 1: creating norms from a proposal

- Input: `docs/calibration/docs-norms-proposal.md`
- Behavior: `create`
- Output: `docs/ARTIFACT_NORMS.md`

### Example 2: an incremental update to existing norms

- Input: the old norms + the new proposal
- Behavior: `merge`
- Output: the updated norms file + the change summary
