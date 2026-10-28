---
id: SKILL_SOURCE_MODELING_SPEC_V1
name: Vendored Skill Source Registry Schema
description: Defines external Skill source records and evidence-backed provenance presentation for the AI Cortex catalog.
version: 2.0.1
status: active
lifecycle: living
created_at: 2026-08-26
scope: |
  Defines the source registry for externally derived Skills and provenance markers for the Skill catalog.
  Includes creative-reference evidence and tool-lookup references needed for provenance decisions; does not model runtime dependencies.
related:
  - ../skills/SOURCES.yaml
  - ../docs/adr/0011-vendor-external-skills.md
  - ../docs/references/LICENSE_POLICY.md
  - ../docs/references/ATTRIBUTIONS.md
---

# Externally Derived Skill Source Schema

> **Data contract**: defines the source, pinned version, license, modifications and update record of a vendored externally derived skill in AI Cortex

## 1. Position and scope

`skills/SOURCES.yaml` is the machine-readable source registry for AI Cortex's externally derived skills. Every local directory that copies, adapts, forks or substantially borrows an external skill's workflow and continues to be distributed as an AI Cortex skill must be registered. Ordinary tool dependencies and deleted historical Skills are not registered as vendored copies. Creative-reference and tool-lookup sources used in provenance decisions are recorded separately under `references`; they do not assert copying or distribution rights.

At runtime only the local copies under `skills/` are loaded. The registry exists for maintenance, audit, license compliance and SPDX generation. It is not a dependency resolver, and it does not authorise an agent to install anything over the network.

## 2. Mental model

Every registry entry must answer five questions:

| Question | Fields |
| --- | --- |
| What is called locally? | `local_path`, `local_version` |
| What was it derived from? | `upstream.repository`, `upstream.path` |
| What is it pinned to? | `upstream.ref`, `tree`, `skill_digest` |
| Under what license is it distributed? | `license`, `notice` |
| What did AI Cortex change, and how is it updated? | `modifications`, `update_policy` |

Registered does not mean downloadable at runtime. An agent can call a skill only once the local directory exists, it is registered in `skills/INDEX.md`, and the canonical installer has synced it.

## 3. Naming

- The registry is always `skills/SOURCES.yaml`.
- The skill key, the `local_path` directory name and the `name` in `SKILL.md` must all match.
- Local paths in the registry are always relative to the repository root. A copy of the upstream license may live at the target skill's `LICENSE.upstream`; centralised attribution uses `docs/references/THIRD_PARTY_NOTICES.md`.

## 5. Body structure contract

### 5.1 Root structure

```yaml
schema_version: "1.0"
policy:
  distribution: vendored-only
  runtime_external_install: forbidden
  update: reviewed
skills: {}
references: {}
```

`distribution` and `runtime_external_install` are repository-wide invariants. An `on-demand`, `remote` or `auto-install` exception must not be added for an individual skill.

### 5.2 Skill entry

| Field | Type | Required | Constraint |
| --- | --- | --- | --- |
| `local_path` | path | yes | `skills/<name>`; the directory must exist |
| `local_version` | SemVer | yes | Matches the local `SKILL.md` |
| `origin` | enum | yes | Currently fixed as `vendored-derived` |
| `upstream.repository` | HTTPS Git URL | yes | The repository URL; never a raw URL |
| `upstream.path` | path | yes | The upstream skill's root directory |
| `upstream.ref` | full commit SHA | yes | A 40-character commit; must not be a branch, tag or `latest` |
| `upstream.tree` | digest | yes | Pins the upstream directory's Git tree |
| `upstream.skill_digest` | digest | yes | SHA-256 of the upstream `SKILL.md` |
| `license` | SPDX expression | yes | The verified upstream and local distribution license |
| `notice` | path | yes | Path to the local license or NOTICE, relative to the repository root; the file must exist |
| `update_policy` | enum | yes | `reviewed-merge` or `reviewed-port` |
| `modifications` | list[string] | yes | Local differences; an empty list is allowed only for a verified unchanged upstream copy |

### 5.3 Update validation

A maintenance update must first pin the new commit, compare the upstream tree against the local differences, re-verify the license and the assets, and only then update the local copy, the version, the registry, the attribution and the SPDX inputs. An update must not happen in the middle of a business skill invocation.

### 5.4 Reviewed provenance presentation (schema 2)

The distributed-file inventory includes Git-tracked and nonignored untracked files; ignored local caches are excluded. Outside a Git checkout, inventory every file. Existing contained file aliases in original/adapted Skills bind the link target text and distributed target bytes; unchanged upstream copies still require exact distribution identity.

`skills/PROVENANCE.json` owns the classification and human decision for every current Skill. The root is `{schema_version: 2, skills: {<directory-name>: <record>}}`. Missing/extra records fail full-catalogue validation. There are exactly three classification identifiers; none is an implicit default:

| Identifier | Meaning and evidence |
| --- | --- |
| `native` | Built from scratch in this repository without external creative reference. Creation commit or related requirement plus explicit maintainer confirmation are required; Git history alone is insufficient. Tool documentation consulted only for parameters or command usage does not disqualify originality. |
| `third_party_original` | All distributed files match a pinned upstream Skill byte for byte, including any local metadata/notices. Full upstream file inventory, revision, license and human-reviewed comparison are required. |
| `third_party_adapted` | Copied/modified Skill or independent writing informed by external methods, workflows or expression. Record actual sources and local adaptation, including non-Skill articles without an upstream repository. A verified unchanged distribution takes precedence over this category. |

Confirmed `native` records omit the display badge; `third_party_original` and `third_party_adapted` retain visible text badges. Evidence remains accessible in the repository index and maintenance records; the website displays no audit-material links. No unknown-source badge, hidden unresolved classification or inferred originality is accepted for delivery. Index and website use the same validated record. Individual Skill frontmatter does not repeat the display classification. Provenance is not a security or quality certification.

| Record field | Contract |
| --- | --- |
| `classification` | One of the three identifiers above |
| `version` | Current Skill frontmatter version |
| `reviewed_files` | Exact distributed relative path to lowercase SHA-256 map, including `SKILL.md`; regular files hash their bytes, contained file links hash their UTF-8 target text |
| `reviewed_links` | Optional exact link-path to relative-target-text map for native/adapted distributions; required when links exist, omitted or empty otherwise |
| `reviewed_evidence` | Exact map of all non-confirmation evidence file paths to SHA-256 bytes |
| `evidence` | Nonempty array of EvidenceReference objects, including all confirmation evidence |
| `creation` | Native only: `{kind: "commit", revision: <40-hex-commit>}` touching the Skill, or `{kind: "requirement", evidence: EvidenceReference}` |
| `sources` | Array of `{id, role, adaptation?}`; unique source IDs; roles `creative_reference`, `tool_lookup`, `copied_upstream`. Creative references and modified copies require adaptation descriptions |
| `decision` | `{maintainer, confirmed_at, action, classification, rationale, evidence, subject_digest}`. Nonempty identity/rationale, ISO date, action `confirmed` or `corrected`, matching classification, nonempty evidence array and lowercase SHA-256 subject digest |
| `upstream_ref`, `upstream_files` | Unchanged only: immutable 40-hex revision matching the source registry and full upstream file hash map matching the local distribution |

EvidenceReference is `{path: <repository-relative-file>, anchor?: <existing-heading-or-explicit-id>}`. Paths must be contained regular files without traversal or symlinks; no URL is accepted in place of a local evidence path. Confirmation evidence is a public JSON file exactly matching the decision object, never private chat text. Unknown fields, duplicate JSON keys, malformed dates, dangling source IDs and contradictory categories fail validation.

Source IDs use `skill:<name>` for the existing vendored registry, and `reference:<id>` for §5.5. Native records permit only tool-lookup references; adapted requires creative-reference or modified-copy evidence. Unchanged requires exactly one copied source and no creative adaptation. All vendored sources retain §5.2 license/notice obligations. Non-copy references do not invent upstream file comparisons or licenses for material not distributed.

The subject contains Skill ID, version, category, reviewed files, creation, ordered source objects, resolved source-registry entries, non-confirmation evidence references and their hashes; unchanged claims also include upstream revision/file maps. Include `reviewed_links` when present. Sort mapping keys, sources by ID/role and evidence by path/anchor; serialize as UTF-8 JSON with sorted keys, separators `(',', ':')`, `ensure_ascii=False`, then SHA-256. Preserve string contents. Exclude the decision and its confirmation document to avoid self-reference. Confirmation evidence cannot also be a hashed subject input. The confirmation document states the subject digest and final decision.

Any change to the Skill files, category, creation reference, sources, adaptation descriptions or non-confirmation evidence invalidates the old decision. Require a new packet and explicit confirmation; never auto-refresh a digest as a substitute for a person. Export revision changes alone do not change the subject.

Existing contained file aliases are supported for native/adapted distributions: the link target must be relative, resolve to a regular file inside the same Skill, and contain no directory-link or link-chain traversal. Both the link text and the target file are inventoried. This preserves the existing define-roadmap example alias without duplicating maintained data. Link-type or target changes invalidate the decision. Evidence references and `SKILL.md` itself cannot be symlinks; unchanged-upstream claims continue rejecting symlink distributions pending an explicitly reviewed upstream link contract.

### 5.5 Reference entries and supported registry syntax

`references.<id>` has `{url, title, accessed_at, kind, evidence}`: HTTPS URL, nonempty title, ISO access date, kind `article`, `method`, `workflow`, `skill` or `tool_documentation`, and an EvidenceReference. A `tool_lookup` role requires the last kind; a copied-upstream role requires a vendored Skill entry. Copy/license evidence remains in `skills`, not `references`.

The offline registry reader accepts two-space-indented mappings with unquoted alphanumeric/hyphen/underscore keys, string scalars, double-quoted JSON strings, single-quoted strings with doubled single quotes, scalar string lists and empty `{}`/`[]`. Blank and full-line comment lines are allowed. Tabs, aliases, tags, folded/literal blocks, nonempty flow containers, inline comments and implicit typed scalar coercion are unsupported. Unsupported or duplicate structures fail with a location rather than being guessed. Root keys are `schema_version`, `policy`, `skills`, `references`; the last collection may be omitted during migration.

### 5.6 Generation and migration boundary

Schema 1 is a migration-only reader for the existing working catalogue until all schema-2 decisions are collected. Its generic declarations/dates must not be converted into human attestations. The schema-2 validator and tests can run on isolated fixtures before that cutover. After cutover, canonical generation rejects schema 1; the maintenance review command may still inspect legacy or incomplete candidates without writing a decision or making an unresolved catalogue ready.

Formal generation validates the complete manifest, website coverage and fixed evidence commit before replacing index, public projection and managed static regions. Local preview is isolated, marked not delivery-ready, and cannot replace canonical outputs. Fixed public URLs are an export projection, not a second editable provenance authority. Maintenance validates upstream/source truth; offline generation does not fetch upstream or claim remote evidence availability.

## 6. Anti-patterns

- ❌ A skill body that asks the agent to run `npx skills add`, clone an external repository, or read a floating raw URL.
- ❌ An `upstream.ref` set to `main`, a tag, a version range, or omitting the commit.
- ❌ Copying an external skill but writing only `author: ai-cortex`, with no source and no notice.
- ❌ Registering only the entry skill while omitting sibling skills or assets that were copied into the repository.
- ❌ Registering an external CLI or API as an external skill, or using the registry to auto-install software dependencies.

## 7. Examples

```yaml
skills:
  example-skill:
    local_path: skills/example-skill
    local_version: 1.0.0
    origin: vendored-derived
    upstream:
      repository: https://github.com/example/skills.git
      path: skills/example-skill
      ref: 0123456789abcdef0123456789abcdef01234567
      tree: sha1:0123456789abcdef0123456789abcdef01234567
      skill_digest: sha256:0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
    license: MIT
    notice: docs/references/THIRD_PARTY_NOTICES.md
    update_policy: reviewed-merge
    modifications: [Adapted output contract]
```

## 8. Relationship to other assets

- [ADR 0011](../docs/adr/0011-vendor-external-skills.md) decided on the vendored-only distribution strategy.
- The [license policy](../docs/references/LICENSE_POLICY.md) governs license verification and notice retention.
- [Sources and attributions](../docs/references/ATTRIBUTIONS.md) is the human-readable view.
- A Release Package's SPDX artifact can be generated from this registry and the repository contents, but SPDX plays no part in runtime skill discovery.
