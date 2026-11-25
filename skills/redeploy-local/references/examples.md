# Local deployment examples

## Source build after an edit

The user wants to run a working-tree change in the local API. The project also documents an optional CI image route. The working-tree request selects source. The project uses pnpm to build `dist/`, and the API Dockerfile copies it. The existing local Compose project names the API and its required database. Bind the local engine and Compose inputs. Confirm the project-supported command can update only the API while its existing database satisfies the dependency requirements.

Show a plan with the evidence for `pnpm run build`, the observed `dist/` output, the scoped Compose command, and the checks for the resulting container image, code mounts, and API readiness. Record the build and deployment separately because they produce different outputs. If the image build fails, the selected services must remain untouched. Report a verification failure if a stale host mount overrides the built code.

## One combined source build and deployment

The repository defines `services.api.build` and has no separate host build. The project-supported `docker compose up -d --build api` performs the build before service changes. Use it with the same local engine and Compose arguments verified during planning. Record a single command and identify the resulting image. Confirm the selected container uses that image and passes its readiness check. Cache `build.mode: combined` after verification when detection was required.

## Package and binary deployments with a process manager

A Makefile builds the Go executable referenced by the live local systemd unit. Read the target body and the unit's effective settings, including drop-ins and its system or user scope. Check that the build produces the exact executable the unit consumes. Restart the identified unit through the project's entry point, then verify that the active process uses the expected executable and that the agreed readiness check passes.

For a release package, use the project's supported install or version switch, verify the package checksum and installed executable association, then restart the exact unit. If the unit still points to an earlier version after installation, stop before declaring a verified deployment. A root-owned unit file alone does not determine the credentials needed for the restart.

## Existing image from a CI build

The user selects a build record with an API image digest and a migration job using the same image. The local project defines both services and requires the migration to complete before the API is ready. Bind the local engine, project, configuration and expected service instances. Pin both services to the recorded digest through the project's image parameter or an image-only override. Check the effective image references and mount targets, pull the selected image, and use the project-supported scoped, build-free invocation. Preserve the migration gate.

Verify the migration run for this deployment and the API container's image ID for the intended platform. If the migration has completed and every API replica is running but the readiness check fails, report **Failed**. Include the current image ID and migration outcome. Do not repeat the migration while diagnosing the readiness failure. An unavailable readiness check with no observed failure leaves **Verification incomplete**.

## A failed build leaves the deployment untouched

The build command exits with code 1. Stream its output and preserve that code even if the tool records elapsed time separately. Report **Failed**, include useful redacted error output, and record the deployment as skipped. If the deployment command itself fails after updating part of the stack, inspect the bound target read-only and report each observed change and any unknown outcome.

| Step | Command | Exit | Duration |
| --- | --- | --- | --- |
| Build | `pnpm run build` | 1 | 4.2 s |
| Deploy | Skipped after build failure | — | — |

## Cache reuse and overrides

The project defines `deploy_command` in `.ai-cortex/config.yaml`; legacy `.cortex.yaml` supplies `build_command`. Use both fields because they apply to the requested local path and neither canonical field overrides the legacy build value. Neither needs caching.

When one field is inferred, store that finding and its evidence after a verified deployment. On the next run, reuse it only while the scan is current, the candidate file list and recorded mtimes match, and the current override still agrees with what the inferred command produces or consumes. Adding a project build wrapper triggers fresh inference even if the previous files have unchanged mtimes.
