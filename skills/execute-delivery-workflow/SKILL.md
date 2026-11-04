---
name: execute-delivery-workflow
description: Run an existing project-owned artifact delivery workflow for a specified source and destination, verifying the resulting artifact at the target. Use for one build-and-deliver operation; missing or broken workflow design belongs to establish-delivery-workflow.
version: 1.0.0
license: MIT
---

# Execute Delivery Workflow

Complete one authorized artifact delivery through the project's authoritative workflow. Delivery means required verification passed and the exact artifact is confirmed at its destination. A successful CI job, local build, or upload response alone is insufficient. Adapt to the project's environment and artifact format rather than prescribing universal commands.

## Inputs and execution contract

Require the project and component, source reference/state, exact version or project-defined version source, target destination/channel, and the applicable workflow entry point. Discover these from explicit instructions and current project configuration; honor established defaults only when their meaning is unambiguous. Do not invent a release destination, requirement scope, or version policy. A request to deliver to a named target authorizes that delivery within its stated scope; do not seek repeated approval for each stage. A request limited to a build, preview, or dry run does not authorize upload.

Read the workflow's project-owned handoff: invocation/parameters, supported targets, source-state policy, environment, verification gates, expected artifact, credential references, destination check, and recovery behavior. These may be implemented by scripts and CI configuration with linked documentation; no particular contract file or CI vendor is required.

Inspect current branch, HEAD, working-tree/staged changes, and the actual component before execution. Bind the run to an exact source state. Do not silently discard local work or deliver uncommitted changes under a commit-only identity. Follow the project's policy for dirty checkouts and record a sufficient identity for any explicitly supported working-tree build; if it cannot be represented reliably, report that gap.

## Check feasibility and scope

- Confirm required tools/versions and runner availability, dependency setup, expected parameters, destination, and non-secret credential references. Existing read access does not establish write permission.
- Inspect the invoked scripts, lifecycle hooks, and pipeline behavior for effects beyond the request. A release command may also bump, commit, tag, push, deploy, or publish to several targets. Select a documented scoped mode, or resolve the excess scope before running it.
- Before invoking an entry point that can upload, inspect how it selects, verifies, packages, and uploads the artifact. Establish that the uploaded payload will be the validated payload, including when packaging occurs again. If this cannot be established, use a documented build-only or preview mode if in scope, or stop and report the workflow gap before upload.
- Prefer a sufficient connected CI/registry/storage tool. Discover operation and status/read-back capabilities; otherwise use the project-supported CLI. A queued CI run is not a completed delivery. Identify the run created for this request and wait for its terminal outcome rather than attaching the result of an unrelated job.
- If the workflow is missing, incompatible, or incomplete, report the exact gap and hand it to `establish-delivery-workflow` when the user requests that work. Continue independent read-only assessment, but do not silently redesign infrastructure or fabricate a replacement command sequence.

## Execute the established workflow

Invoke the supported entry point with the resolved source, component, version, and destination. Reuse project entry points rather than creating a second implementation of their sequence. Track the actual stages and outputs: build, required verification, packaging, upload, and destination read-back. Stop on failed prerequisites or verification; do not weaken checks or continue to publish an unverified result.

Bind the packaged artifact to the run: record its exact name/version or immutable identifier, source state, runner/build reference, and digest where supported. Check that execution follows the inspected path and the upload consumes the validated artifact. If it deviates or identity cannot be established, stop any remaining upload steps and report the gap and any external effects.

If execution pauses at a project acceptance gate, report **awaiting acceptance** with the retained artifact identity and run reference. Do not bypass the gate or trigger another build to represent promotion of the tested artifact. A snapshot, prerelease, or stable destination has only the semantics established by the project contract.

## Verify at the destination

Query the actual target used by this run. Check the exact artifact identity and version/build, location, channel pointer if it was changed, and destination digest against the delivered payload when supported. Verify all required outputs for multi-artifact runs. Report per-artifact outcomes; partial success is not complete delivery.

For registries or directories without a comparable digest, use the project's documented alternative identity/read-back evidence and state the limitation. If the documented success criterion cannot be met, report delivery as unconfirmed rather than treating a green job as proof. Presence does not imply production deployment or independent acceptance.

A read-only artifact inspection capability can perform the destination check if available. It must query the artifact source itself; build logs may explain the run but cannot replace that observation. Do not require a particular companion skill to be installed if the necessary read-only operation is otherwise available.

## Failure, retries, and resumption

- On upload failure, retain the validated artifact, digest, source/run identity, and safe retry reference under project retention rules. Do not rebuild by default. If the runner no longer retains the artifact, state that a new build is required and creates a new candidate identity.
- After a timeout or uncertain upload outcome, inspect the destination before retrying. Avoid publishing a duplicate merely because the client did not receive confirmation.
- If the target identity already exists, compare content/immutable identity. An identical result can be reported as already delivered when the project allows it; conflicting immutable releases block the run. Mutable snapshot aliases require the explicit policy and distinguishable build identities established by the project; no implicit overwrite or deletion.
- Reuse earlier verification only while the relevant source, inputs, environment, and payload identity remain valid. Restart only affected steps; a change to the payload invalidates artifact-specific checks. Report retry history instead of implying the first attempt succeeded.
- Do not automatically reset/stash unrelated work, roll back external state, remove versions, or change credentials. Report partial external effects and the concrete next action if blocked.

## Output and completion

Lead with what was delivered and where it can be obtained, or the precise stage that stopped. Include selected source/version/target, actual run reference, verification summary, artifact identity/digest, destination evidence, retained artifacts, and material limitations as needed. Keep secrets out of logs and reports. Use natural prose; expand technical detail only when needed to evaluate the result.

Use **delivered**, **already delivered**, **awaiting acceptance**, **partially delivered**, **failed**, or **delivery unconfirmed** according to evidence. A local-only or dry-run success is **build/preview complete**, not delivered. Do not claim ready for production from a metadata check. This skill does not select requirements for a release, rewrite project policy, bump/commit/tag/push source, or deploy applications unless those actions are explicitly included in the user's scope and established workflow.
