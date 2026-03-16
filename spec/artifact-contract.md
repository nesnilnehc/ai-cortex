# Artifact Contract

Status: DEFAULT (default, optional reference)
Version: 1.2.0
Scope: Skills that write Markdown artifacts under project `docs/` or repo root.

**Changelog**:

- v1.2.0 (2026-03-16): Added `requirements` artifact type; owner skill `analyze-requirements`.
- v1.1.0 (2026-03-06): Project norms first; this contract as default fallback; AI Cortex and project-documentation-template as trusted suggestions.
- v1.0.0 (2026-03-06): Initial contract; AI Cortex principles first; project-documentation-template as supplementary reference.

---

## 1. Design Principle

**Project norms first**: If a project defines its own artifact norms (see [spec/artifact-norms-schema.md](artifact-norms-schema.md)), skills MUST follow the project's norms. The project is the authority for its own documentation structure.

**Fallback**: If no project norms exist (no `docs/ARTIFACT_NORMS.md` or `.ai-cortex/artifact-norms.yaml`), skills use this contract as the default for paths, naming, and lifecycle.

**Trusted suggestions**: This contract, AI Cortex skills, and [project-documentation-template](https://github.com/nesnilnehc/project-documentation-template) are optional, trusted references. They do not override a user's existing documentation and directory structure. Users may adopt, customize, or ignore them.

**Compatibility**: Paths are designed so projects using project-documentation-template can map structure where overlap exists. Projects not using the template can still use this contract as fallback; no external dependency is required.

---

## 2. Artifact Types

| artifact_type | path_pattern | naming | lifecycle | owner_skill |
| :--- | :--- | :--- | :--- | :--- |
| requirements | `docs/requirements-planning/` | `{topic}.md` | snapshot | analyze-requirements |
| backlog-item | `docs/process-management/project-board/backlog/` | `YYYY-MM-DD-{slug}.md` | living | capture-work-items |
| backlog-item (fallback) | `docs/backlog/` | `YYYY-MM-DD-{slug}.md` | living | capture-work-items |
| adr | `docs/process-management/decisions/` | `YYYYMMDD-{slug}.md` | living | bootstrap-docs |
| design | `docs/design-decisions/` | `YYYY-MM-DD-{topic}.md` | snapshot | design-solution |
| doc-assessment | `docs/calibration/` | `YYYY-MM-DD-doc-assessment.md` | snapshot | assess-docs |

### Path Rationale

- **requirements**: `docs/requirements-planning/` groups all validated requirements; flat naming `{topic}.md` supports direct referencing from design docs. `review-requirements` uses these files as input for quality assessment.
- **backlog-item**: `project-board/backlog/` aligns with agile board semantics; single-item-per-file supports triage and traceability. Fallback `docs/backlog/` for lightweight projects without process-management.
- **adr**: `process-management/decisions/` groups architecture decisions with process docs; `YYYYMMDD` follows ADR community convention.
- **design**: `docs/design-decisions/` at top level to avoid confusion with template's `design/` (brand/UI); distinct from ADR (implementation design vs architecture decision).
- **doc-readiness**: `docs/calibration/` for governance/assessment reports; separate from content docs.

---

## 3. Path Detection (backlog-item)

For `capture-work-items`, use:

| Condition | Output path |
| :--- | :--- |
| `docs/process-management/` exists | `docs/process-management/project-board/backlog/YYYY-MM-DD-{slug}.md` |
| Otherwise | `docs/backlog/YYYY-MM-DD-{slug}.md` |

Create subdirectories if they do not exist.

---

## 4. Minimal Path Set (Lightweight Projects)

For projects with no or minimal `docs/` structure, the following paths suffice:

- `docs/backlog/` — work items
- `docs/design-decisions/` — design documents
- `docs/calibration/` — readiness/assessment reports

ADR and full process-management structure are optional for larger projects.

---

## 5. Front-Matter Requirements

Skills producing document artifacts SHOULD include in YAML front-matter:

| Field | Required | Description |
| :--- | :---: | :--- |
| `artifact_type` | Yes | One of: backlog-item, adr, design, doc-readiness |
| `created_by` | Yes | Skill name (e.g. `capture-work-items`) |
| `lifecycle` | Optional | `snapshot` or `living` |
| `created_at` | Optional | `YYYY-MM-DD` |

Progressive adoption: existing documents without these fields remain valid; new skill outputs should include required fields.

---

## 6. Naming Conventions

- **Slug**: kebab-case, lowercase letters and hyphens only; derive from title.
- **Date in filename**: `YYYY-MM-DD` for human-friendly sorting (except ADR: `YYYYMMDD` per community practice).
- **Directories**: kebab-case only.

---

## 7. Extending Artifact Types

To add a new artifact type:

1. Add row to §2 table with path_pattern, naming, lifecycle, owner_skill.
2. Document path rationale if non-obvious.
3. Update affected skill `output_schema` and Self-Check.
4. Bump contract version (PATCH for additive, MINOR for path changes).

---

## Appendix A: Machine-Readable Schema (for verify-artifact-contract)

```yaml
artifact_types:
  requirements:
    path_patterns:
      - "docs/requirements-planning/{topic}.md"
    naming: "{topic}.md"
    lifecycle: snapshot
    owner_skill: analyze-requirements
  backlog-item:
    path_patterns:
      - "docs/process-management/project-board/backlog/YYYY-MM-DD-{slug}.md"
      - "docs/backlog/YYYY-MM-DD-{slug}.md"
    naming: "YYYY-MM-DD-{slug}.md"
    lifecycle: living
    owner_skill: capture-work-items
  adr:
    path_patterns:
      - "docs/process-management/decisions/YYYYMMDD-{slug}.md"
    naming: "YYYYMMDD-{slug}.md"
    lifecycle: living
    owner_skill: bootstrap-docs
  design:
    path_patterns:
      - "docs/design-decisions/YYYY-MM-DD-{topic}.md"
    naming: "YYYY-MM-DD-{topic}.md"
    lifecycle: snapshot
    owner_skill: design-solution
  doc-readiness:
    path_patterns:
      - "docs/calibration/YYYY-MM-DD-doc-readiness.md"
    naming: "YYYY-MM-DD-doc-readiness.md"
    lifecycle: snapshot
    owner_skill: assess-docs
```
