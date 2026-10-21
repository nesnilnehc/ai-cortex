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
| roadmap (views, milestones and revision summary included) | `docs/process-management/roadmap.md` | ★★★ | The active roadmap and latest revision summaries; detailed decisions and retained history are linked, not competing plans |
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

Apply [the Roadmap Spec](../specs/roadmap-modeling.md#54-revision-records). Keep the
latest five material planning summaries in the canonical roadmap. Full decisions
and older revisions stay in existing source records or archive snapshots; no new
artifact type or mandatory parallel log is introduced. Verify retention and links
before shortening summaries or removing legacy work-package directories. Git
preserves textual history; it does not replace reasons and planning impacts.

## Roadmap document family

Follow [Roadmap Modeling](../specs/roadmap-modeling.md#reading-order-and-document-boundaries).
The established main roadmap remains the entry point. Single-document delivery is
valid; split by reader, ownership, update cadence or volume when useful. Optional
iteration/version plans and history are supporting views, not new artifact types.
Keep direction, priorities, key blockers/delivery expectations/events and the latest
five revisions in the main document. Place phases/events with the related delivery
plan and link detailed tasks to execution boards. Detail pages link back.

Declare each fact's editable authority and refresh linked/generated summaries after
changes. The bundled renderer uses same-directory roadmap-delivery.md and
roadmap-history.md; hand-maintained projects may use their established paths.
No automatic migration of legacy milestone work-package directories is required.

### Roadmap selection evidence

Retain work/delivery context, intended readers, constraints, chosen primary/view
combination, layout and rationale in existing roadmap/norm/decision sources under
the [selection contract](../specs/roadmap-modeling.md#56-context-recommendations-and-retained-selection-schema-14).
Do not introduce a mandatory interview file or second configuration store. Source
facts are read before questions; existing choices and destinations survive routine
maintenance. Schema 1.4 renders this evidence, while legacy/custom plans remain valid.
