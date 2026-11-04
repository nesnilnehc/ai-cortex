---
name: establish-delivery-workflow
description: Establish or repair a project's artifact delivery workflow by reusing its build, verification, packaging, and upload capabilities and filling evidenced gaps. Use when delivery is missing, incomplete, or needs redesign; an existing delivery run belongs to execute-delivery-workflow.
version: 2.0.0
license: MIT
---

# Establish Delivery Workflow

Make the selected project capable of delivering an identified artifact to a defined destination through a repeatable project-owned workflow. Delivery covers building, required verification, packaging, upload, and destination read-back. Projects own their environments, commands, artifact formats, and release policy; this skill does not prescribe npm, a CI vendor, or a universal manifest format.

## Inputs

Require a project/repository, selected component(s), and delivery intent, such as a candidate package for testing or an approved stable release. Discover existing configuration before asking for missing inputs. Accept explicit constraints on runtime, CI, artifact format, version/channel, storage, or changes allowed.

Infer technical implementation from authoritative project evidence. Product decisions such as intended audience, test versus official channel, acceptance gates, or a new publication destination need an established policy or the user's decision. Do not invent them to complete a workflow. Ask only about unresolved choices and continue independent work meanwhile.

Accept target version and delivery scope decided offline or recorded by the project. Do not require a version-planning skill. Preparation of version change descriptions is a separate capability; this workflow consumes the result only when the selected target requires it.

## Discover and assess

1. Read project instructions and delivery documentation. Inspect branch, HEAD, staged/unstaged changes, existing analogous workflows, and concurrent work. Preserve unrelated edits.
2. Locate build/test/package scripts, lockfiles, runtime/container definitions, CI configuration, artifact manifests, and registry/storage settings. Inspect actual script behavior rather than trusting command names. Distinguish documented defaults from verified execution.
3. Determine the selected component, artifact identity, version source, destination, and current authorization. In a monorepo, do not assume the root package is the deliverable.
4. Classify the gap: a complete workflow can be retained with an evidence-backed invocation; existing parts may need wiring or repair; a project with no usable parts needs a minimal design before implementation.

Use relevant connected CI/registry/storage capabilities when available; discover them by operation rather than assuming tool names. Otherwise use project-supported local tools. Missing access is a specific gap, not permission to install global tools, change credentials, replace a CI system, or choose a different registry.

## Establish the project workflow

For a missing or partial workflow, describe the minimal design and affected files before changing them. Reuse authoritative scripts and pipeline definitions. Keep commands in their actual executable source rather than copying them into a second parallel configuration. Persist only the invocation and policies not already represented elsewhere, using the project's existing documentation structure.

Resolve these execution requirements for each supported delivery target:

| Requirement | Project-owned decision or evidence |
| --- | --- |
| Source and component | Which ref/commit/component is built; clean-checkout or working-tree policy; generated/untracked input treatment |
| Source and version identity | Exact resolved commit SHA for permitted branch/tag inputs; consistency among tags, version files, build parameters and package version under project rules; isolated build-time injection and its recorded inputs |
| Environment | Required tools and versions, dependency resolution, runner/container, and any platform constraints |
| Build and verification | Actual entry points, required checks, explicit pass/fail criteria, and stop conditions |
| Change description | Whether this target requires notes; existing changelog/release notes/list location, component/version, comparison purpose and baseline/source association, target source, identifiable note revision/digest and unresolved issues when needed |
| Artifact | Format, exact identity/version source, output selection, storage/retention, and digest method |
| Destination | Registry/directory and channel/stage mapping; credential reference without a secret value |
| Success check | Read back the exact artifact at the destination and verify identity and digest where the format permits; otherwise document alternative identity evidence, the read-back method, and its limits |
| Recovery | Retained artifact location, upload retry, conflict handling, and evidence needed to resume |

Keep build, verification, packaging, upload, and read-back in one coherent invocation when appropriate. Reuse a verified package for upload and retry rather than rebuilding it implicitly. If acceptance and promotion are separate project stages, record the required artifact identity and gate; do not implement an unrequested approval service or assume a channel label proves acceptance. Snapshot/release semantics come from the project and repository format, not hardcoded names.

Set change-description prerequisites per project and target, not for every build: ordinary branch/test builds may omit them; candidate/formal releases follow the project's requirements. Reuse existing documents without requiring a new JSON handoff. Version-reference checks, description fact/scope/target checks, project code/build/package verification, and reviewed commits remain separate responsibilities. The project may commit versions and descriptions together; do not require a commit after each capability.

Support main, feature and defect branch inputs when project rules allow; do not require a tag. Establish execution modes that preserve tracked source, project configuration, version files and descriptions by default while allowing normal outputs, caches, temporary files and authorized upload. If existing scripts edit source, bump, commit, tag or deploy, document those effects and a supported scoped mode or the authorization stop. Build-time version injection may generate files in an isolated build directory; record source, parameters and final artifact identity without representing modified inputs as a pure commit snapshot. Promotion requiring the same artifact must preserve its bytes and version rather than rebuild or relabel it.

For upload conflicts, preserve immutable release versions. Snapshot aliases or other mutable channels require an explicit project policy, distinguishable build identities, and recorded digest/history semantics; never silently overwrite an unrelated payload. Do not use a version label alone as evidence that two artifacts are equal.

Implement the agreed scope in project scripts/configuration. Establishing a workflow permits appropriate repository edits and local validation within the request; it does not independently authorize a real publish, external infrastructure changes, credential rotation, or production deployment. Reuse existing authorization if those operations are already explicitly included. Do not ask again for authorized work.

## Verify and hand off

Run relevant syntax/configuration checks and meaningful tests for new logic under project rules. Exercise the local build/verification/package path or supported dry-run where feasible; inspect the actual package selection and metadata. Never report a dry run as an upload or an end-to-end verification. If a live destination check is authorized, verify the actual uploaded artifact there. Preserve inspectable edits on failure and report the failed step and environment gap; do not weaken checks to pass.

The project must provide a durable handoff that another agent can discover without this conversation. It may be an existing pipeline plus a short documentation entry, not a new mandatory file. Identify:

- The authoritative workflow/script and invocation, with required parameters.
- Supported components, source-state policy, version source, and delivery targets/channels.
- Required environment, credential references, and permission prerequisites.
- Produced artifact identity/location/digest and the destination success check.
- Recovery instructions and which steps were actually verified versus still untested.

Classify the result as **ready for the selected target**, **implemented but unverified/blocked**, or **design awaiting a specific decision**. Readiness is per target: a working candidate upload does not prove stable publication works. Missing critical inputs cannot be hidden behind a "complete" label.

## Output and boundary

Explain what the project can now deliver, through which entry point, and what remains unresolved. Link changed authoritative files and summarize checks. Do not automatically commit, push, publish, or deploy unless separately authorized by the task. Keep secrets out of source, logs, and handoff records.

Execution of a ready workflow belongs to `execute-delivery-workflow`. This skill may repair a discovered gap when authorized, but it does not assign requirements to versions, choose release scope, or treat a local build as a successful delivery.
