---
name: redeploy-local
description: Update and verify a local deployment using a source build or an existing artifact, such as a CI image, release package, or versioned binary. Use for Docker Compose, systemd, or process-manager deployments that need to run the requested code or artifact locally.
license: MIT
metadata:
  version: "3.4.1"
---

# Redeploy locally

Update one authorized local deployment and verify that the intended source build or artifact is running and ready. The target directory defaults to the current working directory. Confirm it exists and resolve its path before inspecting project files.

This skill covers Docker Compose, systemd, pm2, and supervisord. Hot-reload development servers, remote deployment, publishing, credential changes, and standalone database migrations are outside its scope. Preserve startup and migration gates already part of the authorized local workflow.

## Select the input

- Use the input requested by the user. Requests to run current working-tree changes, including a redeploy after editing code in the current task to exercise those changes, select the source path. A requested image, package, or producer build selects the existing-artifact path. Ask when the request contains incompatible inputs.
- For an otherwise unspecified redeploy, use an existing artifact only when the project explicitly defines that as the default input for the selected local entry point. A CI publication workflow or an optional image path alone is insufficient. Otherwise deploy from source.
- Keep the chosen input when resolving configuration or recovering from a failure. If a supported local path cannot consume it, report the gap before making changes.

## Bind the target and verify the plan

Use the selected input procedure below to resolve the commands and verification evidence. Complete these checks before running a build, pulling images, installing packages, or changing a service:

1. Use the project's declared local entry point when possible. Inspect the effective command, the local runtime it reaches, the named project and affected services or units, and any dependency starts, one-shot jobs, migrations or other side effects. Check the actual destinations of migrations and other writes. Ask when the intended target or a material side effect remains ambiguous. Execute only effects authorized for this run. Stop before commands that reach a remote deployment target.
2. For Compose, use the [Compose procedure](references/prebuilt.md#docker-compose) to bind the engine and effective configuration on both input paths. For systemd, pm2, or supervisord, confirm the live local manager, its scope or instance, and the exact unit or process configuration. Inspect the entry point, executable or working directory that determines what will run. Derive any elevation requirement from the actual manager and its authorization rules. Obtain explicit authorization for elevation or destructive operations outside the request.
3. Identify the expected running build or artifact, the project-defined readiness check or status criterion, and the expected terminal state of any required one-shot job. Establish how to verify each item and disclose any missing check in the plan. Record the current container, process, or job identities where they help distinguish a new run or reconcile a failure. Show the selected input, target, commands, and evidence before the first mutation. An unambiguous, authorized redeploy can proceed without a second confirmation.

## Deploy from source

1. Read the [detection and cache procedure](references/detection.md). Resolve build and deploy commands from project configuration, valid cached inference where applicable, or project evidence. An explicit configuration field overrides a cached field. Find the output path or image consumed by the resolved runtime.
2. Execute the build from the project directory. Confirm that this run produced or resolved the expected output and record its identity before deploying. A successful compile-only command, or an unchanged output of unknown origin, is insufficient evidence. The build may be subsumed by a project-backed command, such as Compose with a verified `build:` definition, when that command stops before changing the service if its build fails. Record the resulting identity and verify it after the combined command.
3. Execute the scoped deployment command using that output. Apply the shared verification below. Write or refresh source discovery cache entries only after verification passes.

## Deploy an existing artifact

Follow the [existing-artifact procedure](references/prebuilt.md#deploy-an-existing-artifact) to resolve, retrieve, and deploy the exact input through a build-free path. Skip source-build commands and the source inference cache. Apply the same verification and failure handling.

## Run commands and verify results

- Stream build and deployment output when the execution tool supports it. Use each command's actual exit status and elapsed time from the execution tool. If timing in a shell, preserve the command's own status before any logging or cleanup. A status from an enclosing logger or a pipeline's last process is insufficient.
- After a successful deployment command, verify the expected service or instance actually exists in the bound runtime. Compare what it is running with the intended output. For a host executable, inspect the active process and the executable or application-reported build identity. A file present on disk or a matching version label alone is insufficient when it could refer to another build or to a process still running old code.
- Apply the project's readiness or health check with a finite deadline. When the project explicitly defines a runtime state as its readiness criterion, verify that exact state for the intended service. Otherwise report process liveness separately. For Compose, check the named services and their expected replicas, health, and required job outcomes. For systemd use the exact unit and expected active state, for pm2 inspect structured process status for the exact app, and for supervisord check the exact program and expected state.
- Record run states as **Verified**, **Failed**, or **Verification incomplete**. Declare **Verified** only after identity, readiness, and required job outcomes match. A failed command or a demonstrated mismatch is **Failed**. Missing evidence, an unavailable check, or an unresolved timeout leaves verification incomplete or the deployment outcome unknown. Record observed failures even if another check is unavailable.

## Stop and report

On failure or an uncertain write outcome, stop further mutations. Read-only inspection of the bound target may establish which services were changed, their current identity and readiness, and whether a migration started or completed. Preserve the selected input and evidence. Follow a project-owned recovery path only when its prerequisites and scope are established. Do not retry an uncertain migration or roll back by inference.

Report the target, intended and observed running identities, readiness and job results, and the run state. Include the actual commands, exit codes and durations, and identify steps skipped or left unverified. Provide useful failure output with secrets and credential-bearing configuration redacted. A cache write error is a warning and does not change a verified deployment result.

See [worked examples](references/examples.md) for source, existing image, failure, and cache cases.

## Self-check

- The local runtime, affected services, and authorized side effects were bound before changes.
- All commands ran with the intended input, and their actual exit statuses were retained.
- The outcome reflects the observed runtime identity, readiness, and required job results.
- The report identifies partial or uncertain effects. Source inference is cached only when applicable and after verification passes.
