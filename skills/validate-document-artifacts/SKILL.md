---
name: validate-document-artifacts
description: Validate docs under project against artifact norms. Check paths, naming, front-matter for compliance. Output findings list for remediation.
tags: [documentation, eng-standards, workflow]
version: 1.0.0
license: MIT
related_skills: [assess-documentation-readiness, curate-skills]
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [validate docs, validate documents]
input_schema:
  type: free-form
  description: Project path, optional docs root, optional scope (all vs specific artifact types)
output_schema:
  type: findings-list
  description: Findings list with Location, Category, Severity, Title, Description, Suggestion
---

# Skill: Validate Document Artifacts

## Purpose

Check that documents under `docs/` conform to the project's artifact norms (or default [spec/artifact-contract.md](../../spec/artifact-contract.md)). Emit a findings list for path, naming, and front-matter violations so users can remediate.

---

## Core Objective

**Primary Goal**: Produce a findings list of documents that violate artifact norms, with Location, Severity, Title, Description, and Suggestion for each finding.

**Success Criteria** (ALL must be met):

1. ✅ **Norms resolved**: Project norms read from `docs/ARTIFACT_NORMS.md` or `.ai-cortex/artifact-norms.yaml`; fallback to spec/artifact-contract.md
2. ✅ **Docs scanned**: All relevant Markdown under `docs/` (or specified scope) enumerated
3. ✅ **Artifact type inferred**: Per file, inferred from path pattern or front-matter `artifact_type`
4. ✅ **Compliance checked**: Path, naming, front-matter validated against norms
5. ✅ **Findings emitted**: Each violation as a finding with Location, Category, Severity, Title, Description, Suggestion

**Acceptance Test**: Can a user apply the suggestions to fix all reported violations?

---

## Scope Boundaries

**This skill handles**:

- Resolving project norms per [spec/artifact-norms-schema.md](../../spec/artifact-norms-schema.md)
- Scanning `docs/` for Markdown files
- Inferring artifact type from path or front-matter
- Checking path, naming, and front-matter against norms
- Emitting findings list in standard format

**This skill does NOT handle**:

- Auto-fixing violations (user or other tools apply suggestions)
- Readiness assessment (use `assess-documentation-readiness`)
- Establishing norms (use `discover-document-norms`)

**Handoff point**: When findings are delivered, hand off to user for remediation or to `discover-document-norms` if norms need to be created or updated.

---

## Use Cases

- **Pre-commit check**: Ensure new docs comply before commit
- **Audit**: Identify existing docs that violate norms
- **After norms change**: Re-validate after updating ARTIFACT_NORMS.md

---

## Behavior

### Phase 1: Resolve Norms

1. Check `.ai-cortex/artifact-norms.yaml` then `docs/ARTIFACT_NORMS.md`
2. If found, parse path_pattern and naming per [spec/artifact-norms-schema.md](../../spec/artifact-norms-schema.md)
3. If not found, use [spec/artifact-contract.md](../../spec/artifact-contract.md) defaults

### Phase 2: Scan and Infer

1. Enumerate Markdown under `docs/` (or user-specified root)
2. For each file: read front-matter for `artifact_type`; if absent, infer from path (e.g. `backlog/` → backlog-item, `design-decisions/` → design)
3. Map each file to expected path_pattern and naming from norms

### Phase 3: Validate and Emit

1. For each file: compare actual path and filename to expected pattern
2. Check front-matter for required fields (`artifact_type`, `created_by` when applicable)
3. Emit finding for each violation: Location (path), Category (`artifact-norms`), Severity (`major` or `minor`), Title, Description, Suggestion

### Findings Format

Each finding MUST follow:

| Field | Content |
| :--- | :--- |
| Location | `path/to/file.md` |
| Category | `artifact-norms` |
| Severity | `critical` \| `major` \| `minor` \| `suggestion` |
| Title | Short violation summary |
| Description | What is wrong |
| Suggestion | How to fix (e.g. move to X, add front-matter Y) |

---

## Input & Output

### Input

- Project path (default: workspace root)
- Optional: docs root (default `docs/`)
- Optional: scope (all, or specific artifact_type)

### Output

- Findings list (array of findings)
- Summary: total files scanned, violations count by severity

---

## Restrictions

### Hard Boundaries

- **Read-only**: Do not modify files; only report findings.
- **Schema compliance**: Findings MUST follow standard format for aggregation.

### Skill Boundaries (Avoid Overlap)

**Do NOT do these**:

- Create or update norms → `discover-document-norms`
- Assess doc readiness → `assess-documentation-readiness`
- Auto-fix → User applies suggestions

---

## Self-Check

### Core Success Criteria (ALL must be met)

- [ ] **Norms resolved**: Project or default norms used
- [ ] **Docs scanned**: Relevant Markdown enumerated
- [ ] **Compliance checked**: Each file validated
- [ ] **Findings emitted**: Standard format, actionable suggestions

### Acceptance Test

**Can a user apply the suggestions to fix all reported violations?**

If NO: Suggestions unclear or incomplete. Refine findings.
If YES: Validation complete.

---

## Examples

### Example 1: Path Mismatch

**File**: `docs/designs/2026-03-06-auth.md` (project norm: `docs/design-decisions/`)

**Finding**: Location `docs/designs/2026-03-06-auth.md`, Category `artifact-norms`, Severity `major`, Title "Design doc in non-standard path", Description "File is under docs/designs/ but norms specify docs/design-decisions/", Suggestion "Move to docs/design-decisions/2026-03-06-auth.md"

### Example 2: Missing Front-Matter

**File**: `docs/backlog/2026-03-06-bug.md` (no `artifact_type` or `created_by`)

**Finding**: Location `docs/backlog/2026-03-06-bug.md`, Category `artifact-norms`, Severity `minor`, Title "Missing artifact front-matter", Description "File lacks artifact_type and created_by", Suggestion "Add front-matter: artifact_type: backlog-item, created_by: capture-work-items"

---

## Appendix: Output contract

This skill emits a **findings-list** compatible with aggregation. Each finding MUST follow:

| Element | Requirement |
| :--- | :--- |
| **Location** | File path (e.g. `docs/backlog/2026-03-06-bug.md`) |
| **Category** | `artifact-norms` \| `path` \| `naming` \| `front-matter` |
| **Severity** | `critical` \| `major` \| `minor` \| `suggestion` |
| **Title** | Short one-line summary |
| **Description** | What is wrong and why it matters |
| **Suggestion** | Concrete fix or remediation step |
