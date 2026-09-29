---
artifact_type: rule
name: standards-jenkins-job-naming
version: 1.0.0
scope: Jenkins jobs and folders in a Jenkins controller
recommended_scope: project
status: active
created_by: ai-cortex
lifecycle: living
created_at: 2026-09-29
---

# Rule: Jenkins Job Naming

## Scope

This Rule provides a reusable default for Jenkins controllers. Its format is a portability convention, not a description of every name Jenkins accepts. A team may adopt it as-is or record a local exception where a platform integration imposes another name. It covers folder paths and the names of Freestyle, Pipeline, and Multibranch Pipeline items. Jenkins-generated branch items are covered only where their naming can be configured by the owning job.

## Naming format

Use a folder path to express ownership or workload grouping, and use the final item name to express the job's main action and output:

```text
<workload>[/<component>]/<action>[-<artifact-or-target>]
```

Folder levels are optional when they do not add useful grouping. If the Jenkins layout is flat, use the same segments joined with hyphens:

```text
<workload>[-<component>]-<action>[-<artifact-or-target>]
```

Examples:

```text
payments/api/build-image
payments/api/test
payments/release/publish-package
customer-portal/web/build
payments-publish
```

## Constraints

1. **Case and separators**: names and folder segments **MUST** use lowercase ASCII letters and digits, with hyphens between words. Do not use spaces, underscores, characters other than letters, digits and hyphens, or repeated/leading/trailing hyphens.
2. **Stable workload identity**: a name **MUST** identify the product, service, component, or other stable workload it serves. Use the same established spelling for that workload throughout the controller.
3. **Clear action**: the final item name **MUST** state the job's primary action using a recognizable verb such as `build`, `test`, `package`, `deploy`, `release`, or `cleanup`. Add the artifact or target when needed to distinguish purpose, such as `build-image` or `publish-package`.
4. **Folder ownership**: use folders to group jobs by stable ownership, product, service, or lifecycle. A folder path **MUST NOT** repeat information already clear from its parent path or item name.
5. **Meaningful qualifiers**: a qualifier such as an environment or platform **MUST** appear in the name only when it identifies a distinct job with different behavior, permissions, or ownership. If it is only a build-time choice, represent it as a parameter instead.
6. **No run-specific data**: names **MUST NOT** include branch names, commit IDs, versions, dates, usernames, build numbers, or other values that change between runs. Multibranch jobs **MUST** use one stable parent item name and leave branch-specific identity to Jenkins.
7. **Unique and non-generic**: within a folder, sibling items **MUST** have distinct names. Names such as `job`, `pipeline`, `build`, or `test` alone **MUST NOT** be used when the folder path does not identify the workload clearly.
8. **Consistent purpose**: an item **MUST** keep the same name while its purpose remains the same. If its primary responsibility changes, rename it to match; do not preserve an obsolete name for convenience.

## Bad Patterns

- `Payments/API/Build Image` — mixed case and spaces
- `payments-api-build-image` beside the same job stored under `payments/api/` — repeated path context
- `api-build-main-20260929` — branch and date embedded in the item name
- `job1` or `pipeline` — purpose is not identifiable
- `deploy-prod` when one parameterized job deploys to several environments — a run-time choice is presented as a separate job identity

## Remediation

1. Move jobs into folders that express stable ownership or workload grouping.
2. Rename each item to use lowercase kebab-case and state its stable workload and primary action.
3. Remove run-specific values and redundant path segments; use parameters for choices made at build time.
4. Check for sibling name collisions and update links, triggers, and automation that refer to renamed jobs.

## References

- [AI Cortex terminology](../docs/architecture/terminology.md) — distinction between a checkable Rule and a structural Spec
- [Jenkins best practices](https://www.jenkins.io/doc/book/using/best-practices/) — project-name compatibility guidance and name restrictions
- [Working with Jenkins projects](https://www.jenkins.io/doc/book/using/working-with-projects/) — renaming and moving jobs, including references that need updating
