---
artifact_type: governance
created_by: ai-cortex
lifecycle: living
created_at: 2026-03-24
status: active
---

# Artifact norms

**Source**: applies across the AI Cortex project

Language: the project's language rules are in [docs/LANGUAGE_SCHEME.md](LANGUAGE_SCHEME.md). Consumer roadmap outputs resolve and retain their own language under the [Roadmap Spec](../specs/roadmap-modeling.md#57-deliverable-language-schema-15), using existing norms or planning decisions rather than a mandatory new configuration file.

This document defines the single authoritative path for each generated artifact. Unless the user explicitly asks for a snapshot, a skill should overwrite the canonical file at the path below.

---

## The single-source-of-truth principle

The definition and canonical source of each artifact type are fixed below. Any other document touching the same information should cite and add to it rather than restating it.

### Canonical sources

| Artifact type | Canonical source | Strength | Rule |
| :--- | :--- | :--- | :--- |
| strategic-goals | `docs/project-overview/strategic-goals.md` | ★★★ | The one authoritative definition of the strategic goals; other documents cite it with a link plus a summary |
| roadmap (current results and references) | `docs/process-management/roadmap.md` | ★★★ | The active roadmap with links to planning basis and retained history |
| requirements | `docs/requirements-planning/<PROJECT>-REQ-<nn>.md` | ★★★ | The canonical source for the requirements on each topic |
| backlog-item (index) | `docs/process-management/backlog.md` | ★★ | The index and navigation for backlog work items |
| backlog-item (detail) | `docs/process-management/backlog/YYYY-MM-DD-*.md` | ★★ | The detailed definition of a work item |
| adr | `docs/adr/NNNN-{slug}.md` | ★★ | The authoritative record of an architecture decision |
| functional-design | `docs/designs/YYYY-MM-DD-*-functional-design.md` | ★★ | The authoritative definition of a functional design, from the business and product view |
| technical-design | `docs/designs/YYYY-MM-DD-*-technical-design.md` | ★★ | The authoritative definition of a technical design, from the engineering view |

### What counts as a compliant citation

- **A bare link**: the citing document carries only a link to the canonical source → ✅ **best practice**
- **A summary plus a link**: 20-30% of the original summarised, with a link to the canonical source → ✅ **compliant**
- **A full restatement** (>60% overlap, no link) → ❌ **a violation**, and it must be fixed

---

## Artifact types

| artifact_type | path_pattern | naming | lifecycle |
| :--- | :--- | :--- | :--- |
| requirements | `docs/requirements-planning/<PROJECT>-REQ-<nn>.md` | `<PROJECT>-REQ-<nn>.md` | snapshot |
| backlog-item | docs/process-management/backlog/YYYY-MM-DD-{slug}.md | YYYY-MM-DD-{slug}.md | living |
| adr | docs/adr/NNNN-{slug}.md | NNNN-{slug}.md | living |
| functional-design | docs/designs/YYYY-MM-DD-{topic}-functional-design.md | YYYY-MM-DD-{topic}-functional-design.md | snapshot |
| technical-design | docs/designs/YYYY-MM-DD-{topic}-technical-design.md | YYYY-MM-DD-{topic}-technical-design.md | snapshot |
| doc-readiness | docs/calibration/doc-readiness.md | doc-readiness.md | living |
| planning-alignment | docs/calibration/planning-alignment.md | planning-alignment.md | living |
| architecture-compliance | docs/calibration/architecture-compliance.md | architecture-compliance.md | living |
| repair-loop | docs/calibration/repair-loop.md | repair-loop.md | living |
| audit-docs | docs/calibration/audit-docs.md | audit-docs.md | living |

## Path detection for a backlog-item

| Condition | Output path |
| :--- | :--- |
| docs/process-management/ exists | docs/process-management/backlog/YYYY-MM-DD-{slug}.md |

## The backlog directory, an exception

The `backlog/` directory holds backlog-items named `YYYY-MM-DD-{slug}.md` and nothing else. Index files live directly under `docs/process-management/`.

---

## Timestamp policy

A timestamp in a filename, in YYYY-MM-DD or YYYYMMDD form, should follow the rules below, which keep unnecessary timestamps from spreading:

| Artifact type | Timestamp | Form | Why |
| :--- | :--- | :--- | :--- |
| **adr** | FORBIDDEN | `NNNN-{slug}` | An ADR uses a 4-digit sequence number so it can be referred to out loud; the decision date lives in the frontmatter `created_at` |
| **functional-design** | REQUIRED | `YYYY-MM-DD-{topic}-functional-design` | A design is a snapshot artifact, and the timestamp records the moment that version was made |
| **technical-design** | REQUIRED | `YYYY-MM-DD-{topic}-technical-design` | A design is a snapshot artifact, and the timestamp records the moment that version was made |
| **backlog-item** | REQUIRED | `YYYY-MM-DD-{slug}` | The moment a work item was created or assigned has to be recorded |
| **roadmap** | FORBIDDEN | no timestamp | A roadmap is a living document under continuous evolution, and carries no date |
| **strategic-goals** | FORBIDDEN | no timestamp | Strategic goals are a long-term direction and carry no timestamp |
| **requirements** | FORBIDDEN | `<PROJECT>-REQ-<nn>` | A requirement is a snapshot; its ID and frontmatter date identify it, and carries no date |
| **backlog (index)** | FORBIDDEN | no timestamp | The backlog index is live navigation and carries no date |
| **audit-docs** | FORBIDDEN | no timestamp | An audit report is a living document under continuous update, and carries no date |
| **detect-ssot-violations-report** | FORBIDDEN | no timestamp | An SSOT report is a living document under continuous iteration, and carries no date |

### The principle behind it

- **Sequence-numbered artifacts** (the ADR) → FORBIDDEN: a 4-digit `NNNN-{slug}` supports spoken reference, and the timestamp lives in the frontmatter `created_at`
- **Point-in-time artifacts** (designs, work items) → REQUIRED: the timestamp records the moment of the snapshot
- **ID-named snapshots and living artifacts** (requirements; roadmaps, goals and reports) → FORBIDDEN: a stable ID or canonical path identifies the current artifact without a filename timestamp

## Roadmap revision retention

Apply [the Roadmap Spec](../specs/roadmap-modeling.md#54-revision-records).
Keep material revision records in a separate document or directory and link the
history from References. Reuse decision records or archive snapshots that already
provide this history. Verify record retention and links when relocating it.

## Roadmap document family

First alignment follows the Spec's
[existing-project boundary](../specs/roadmap-modeling.md#first-alignment-of-an-existing-project).
Preserve established locations/anchors and business decisions; the default paths
below do not authorize migrating a consuming project or rerunning its planning.

Follow [Roadmap Modeling](../specs/roadmap-modeling.md#reading-order-and-document-boundaries).
The main roadmap is the entry point for direction, current priorities, blockers,
delivery expectations and events. Link the ordering rationale, policies, closure
criteria and history from References. Manage iterations in their own plan or board. Use existing supporting
documents where possible and combine related topics when they share ownership.

Each fact has one editable authority. Refresh linked or generated summaries after
a change. Keep existing project paths and knowledge-base URLs and use the Spec's
[document-family naming advice](../specs/roadmap-modeling.md#document-family-naming)
for new supporting documents.

### Roadmap selection evidence

Retain work/delivery context, intended readers, constraints, chosen primary/view
combination, layout and rationale in existing roadmap/norm/decision sources under
the [selection contract](../specs/roadmap-modeling.md#56-context-recommendations-and-retained-selection-schema-14).
Do not introduce a mandatory interview file or second configuration store. Source
facts are read before questions; existing choices and destinations survive routine
maintenance. Schema 1.4 renders this evidence, while legacy/custom plans remain valid.
