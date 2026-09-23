---
id: PLAN_NEXT_PREFERENCES_SPEC_V1
name: Plan Next Preference File
description: Data contract for project-local exclusions of exact plan-next recommendation routes.
version: 1.0.0
status: active
lifecycle: living
created_at: 2026-09-23
scope: |
  Defines the persisted preference file used by plan-next to omit exact recommendation
  routes until restored. It does not define session-only skips or alter governance state.
related:
  - ./spec-modeling.md
---

# Plan Next Preference File

> **Data contract**: a project-local list of exact recommendation routes to omit until restored.

## 1. Position and scope

The file is `.ai-cortex/plan-next.yaml` in the target project. It stores only persistent recommendation preferences. Its absence means there are no persistent exclusions. It is not a task lifecycle record, roadmap decision, governance waiver, or evidence that work is complete.

Session-only skips are not represented in this file.

## 5. Body structure contract

The file is YAML with exactly these top-level fields:

| Field | Type | Constraint |
| --- | --- | --- |
| `schema_version` | integer | Required; `1` |
| `exclusions` | list | Required; empty list is valid |

Each `exclusions` entry has exactly these fields:

| Field | Type | Constraint |
| --- | --- | --- |
| `route` | string | Required, non-empty recommended skill name without `/`, or a stable action kind when no skill applies |
| `target` | string | Required, non-empty repository-relative artifact path, optionally followed by `#item-id` for an item within that artifact |

The exact `(route, target)` pair is the key. Duplicate keys, unknown fields, absolute paths, parent-directory traversal, and bare item IDs are invalid. Neither field supports wildcards. A project-specific artifact path must be used when project norms select one; a generic default path must not replace it. A target that has been renamed no longer matches the old key and must be selected again explicitly.

Entries do not encode a reason, expiry, task status, or a governance waiver. A writer preserves unrelated valid entries when adding or removing an exact key. If the last key is removed, keep `exclusions: []`. An unsupported version or malformed file must be reported, not silently ignored or overwritten.

## 6. Anti-patterns

- An ordinal or display title stored as `target` instead of the resolved artifact path.
- A wildcard or broad route category that suppresses unrelated recommendations.
- An exclusion treated as proof that its underlying task or prerequisite is satisfied.
- A malformed file silently replaced with an empty list.

## 7. Examples

```yaml
schema_version: 1
exclusions:
  - route: define-docs-norms
    target: docs/ARTIFACT_NORMS.md
```

An empty preference file is also valid:

```yaml
schema_version: 1
exclusions: []
```

## 8. Relationship to other assets

`plan-next` owns the interaction that resolves a displayed suggestion, asks for duration when unspecified, applies this file, and continues recommendation. This Spec owns only the saved file's structure and validation.
