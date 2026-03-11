# Registry Sync Contract

Status: MANDATORY  
Version: 1.0.0  
Scope: manifest.json, skills/INDEX.md, skills/*/SKILL.md, scenario-map, marketplace.json.

**Changelog**:

- v1.0.0 (2026-03-06): Initial contract; defines synchronization rules enforced by verify-registry.mjs.

---

## 1. Purpose

This contract specifies how the skill registry artifacts must stay consistent. `scripts/verify-registry.mjs` enforces these rules. `skills/INDEX.md` is generated from manifest and SKILL frontmatter.

---

## 2. Canonical Sources

| Artifact | Path | Role |
| :--- | :--- | :--- |
| manifest.json | repo root | Executable capability list; `capabilities[].name` and `capabilities[].path` |
| skills/INDEX.md | skills/ | Generated human-readable catalog; table rows with name, tags, version, stability, purpose |
| skills/{name}/SKILL.md | skills/ | Per-skill definition; YAML frontmatter with name, version, tags |
| skills/scenario-map.json | skills/ | Source of truth for scenario-map.md; primary/optional skill refs |
| skills/scenario-map.md | skills/ | Generated from scenario-map.json; scenario-to-skill mapping |
| .claude-plugin/marketplace.json | repo root | Claude plugin subset; `plugins[].skills[]` |

---

## 3. Sync Rules

### 3.1 manifest.json ↔ skills/

- Every `manifest.capabilities[].name` must have a directory `skills/{name}/` containing `SKILL.md`.
- Every `manifest.capabilities[].path` must equal `skills/{name}/SKILL.md`.
- Every directory `skills/{name}/` that contains `SKILL.md` must appear in `manifest.capabilities`.

### 3.2 skills/INDEX.md ↔ manifest.json

- Generated INDEX must contain every skill in manifest.json.
- Generated INDEX must not contain skills missing from manifest.json.
- No duplicate skill names in generated skills/INDEX.md.

### 3.3 skills/INDEX.md ↔ skills/{name}/SKILL.md

- For each INDEX row, the corresponding SKILL.md frontmatter must have:
  - `name` equal to the skill name (matches directory name).
  - `version` equal to the version in INDEX.
  - `tags` equal (order-independent) to the tags in INDEX.
  - `description` used as the Purpose source in INDEX.

### 3.4 scenario-map.md / scenario-map.json

- Every skill referenced in scenario-map.md (links to `./{name}/SKILL.md`) must exist in manifest and INDEX.
- Every skill referenced in scenario-map.json `scenarios[].primary` or `scenarios[].optional` must exist in manifest and INDEX.

### 3.5 marketplace.json

- Every skill path in `plugins[].skills[]` must resolve to an existing skill in manifest and INDEX.

---

## 4. Verification

Run from repo root:

```bash
node scripts/verify-registry.mjs
```

Before running, `generate-skills-docs.mjs` regenerates INDEX.md, skillgraph.md, and scenario-map.md from sources. The script exits 1 if any sync rule is violated.

---

## 5. Update Procedure

When adding a new skill:

1. Create `skills/{name}/SKILL.md` with valid frontmatter.
2. Add the capability to `manifest.json` capabilities array.
3. Regenerate `skills/INDEX.md`.
4. Optionally add to scenario-map.json and marketplace.json.
5. Run `node scripts/verify-registry.mjs` to confirm sync.
