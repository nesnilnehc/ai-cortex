---
id: SKILL_SOURCE_MODELING_SPEC_V1
name: Vendored Skill Source Registry Schema
description: Defines the source, pin, license, modification, and update contract for externally derived Skills vendored into AI Cortex.
version: 1.0.0
status: active
lifecycle: living
created_at: 2026-08-26
scope: |
  Applies to externally derived Skills distributed by AI Cortex and recorded in skills/SOURCES.yaml.
  It does not model ordinary software packages, CLI tools, APIs, or informational references.
related:
  - ../skills/SOURCES.yaml
  - ../docs/adr/0011-vendor-external-skills.md
  - ../docs/references/LICENSE_POLICY.md
  - ../docs/references/ATTRIBUTIONS.md
---

# Externally Derived Skill Source Schema

> **Data contract**: defines the source, pinned version, license, modifications and update record of a vendored externally derived skill in AI Cortex

## 1. Position and scope

`skills/SOURCES.yaml` is the machine-readable source registry for AI Cortex's externally derived skills. Every local directory that copies, adapts, forks or substantially borrows an external skill's workflow and continues to be distributed as an AI Cortex skill must be registered. Ordinary tool dependencies, industry standards, documentation links and historical skills that have been deleted are not registered.

At runtime only the local copies under `skills/` are loaded. The registry exists for maintenance, audit, license compliance and SPDX generation. It is not a dependency resolver, and it does not authorise an agent to install anything over the network.

## 2. Mental model

Every registry entry must answer five questions:

| Question | Fields |
|---|---|
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
```

`distribution` and `runtime_external_install` are repository-wide invariants. An `on-demand`, `remote` or `auto-install` exception must not be added for an individual skill.

### 5.2 Skill entry

| Field | Type | Required | Constraint |
|---|---|---|---|
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
| `modifications` | list[string] | yes | At least one entry, describing the local differences |

### 5.3 Update validation

A maintenance update must first pin the new commit, compare the upstream tree against the local differences, re-verify the license and the assets, and only then update the local copy, the version, the registry, the attribution and the SPDX inputs. An update must not happen in the middle of a business skill invocation.

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
