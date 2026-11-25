# Detect a source-build deployment

Use project evidence to resolve one build and one deployment command for the selected local target. Record where each command comes from and what artifact the runtime consumes.

## Read project configuration

Read `.ai-cortex/config.yaml`, legacy `.cortex.yaml`, and applicable project instructions for local deployment. Prefer a command explicitly passed by the user, then the canonical configuration field for the local target, then the legacy field. Apply precedence per field. If equally authoritative declarations select different targets or have different material side effects, resolve that choice before execution. A configured deploy command that serves a different target is not an override for this run. Use the field `deploy_command` or `build_command` only when the value applies to the intended local path. Infer any missing field from the local entry point or project evidence.

## Reuse source inference

The source-only cache is `.cortex/redeploy-local.yaml`. Use it to avoid rereading unchanged build and deployment evidence. Keep it out of version control because it contains host-local paths and times. Honor active overrides before cache lookup. Commands from active overrides need not be cached.

A cache entry has the current Skill version, real project path, original scan time, the inferred fields with evidence, and the discovery inputs. For example:

```yaml
skill_version: "3.4.1"
project_path: /work/api
written_at: 2026-11-25T01:30:00Z
build:
  mode: combined
  evidence:
    - file: compose.yaml
      ref: services.api.build
deploy:
  command: docker compose up -d --build api
  evidence:
    - file: compose.yaml
      ref: services.api
signal_files:
  - path: compose.yaml
    mtime: 2026-11-25T01:25:00Z
  - path: Dockerfile
    mtime: 2026-11-25T01:24:00Z
```

Use `build.mode: separate` and a non-empty `build.command` for a standalone build. Use `build.mode: combined` without a build command when the deployment command performs the build. Omit a field only if it was supplied by an active override. The signal inventory includes every discovered candidate and each extra file read to resolve the commands and target, including wrappers, overrides and lockfiles. Store file paths and mtimes. Keep the candidate discovery bounded to the same project roots and patterns used in the original scan.

Before reuse, check that the cache parses, the Skill version and real project path match, the scan age is from zero to less than 30 days, and every missing override has a valid cached entry. Re-enumerate candidate paths and compare them with recorded paths that match the same discovery patterns. Check all recorded signal mtimes, including any extra files outside those patterns. Check current overrides and confirm the effective deployment command, local runtime, scope, and application output still match the request. If an override changes whether the deployment builds or what it consumes, recompute the dependent field. On any failed check, treat the affected inference as missing and read project evidence. Authorization and runtime verification are evaluated on every run.

Write a new cache only after a verified source deployment with inferred fields. Write atomically in the same directory when supported. Preserve the original scan time on a cache hit so a reuse does not postpone a full rescan. Skip the cache write if both fields came from overrides, the outcome was unverified, or the path is unsafe or unwritable. Report a write error as a warning.

## Find commands and the artifact handoff

Enumerate candidate files in the chosen project or component. Inspect its root, relevant scripts, local deployment directories, CI definitions, and build or development docs:

- Build orchestration: `Makefile`, `Taskfile.yml`, `justfile`, `package.json`, and project build scripts.
- Container and local runtime configuration: `Dockerfile` and variants, `compose.yaml` and `docker-compose.yml` and their overrides, systemd units, pm2 ecosystem files, `supervisord.conf`, and included program definitions.
- Language and dependency evidence: manifests, package-manager lockfiles, and toolchain declarations.
- Documented workflows: project README or relevant local instructions, `.github/workflows/`, `.gitlab-ci.yml`, and `Jenkinsfile`.

Read the applicable files and follow includes or wrappers to the actual commands. The nearest declared local workflow and effective runtime configuration decide what the local target consumes. CI and language manifests can corroborate the build. A different CI release command does not by itself override a clear local path.

1. **Build.** Prefer a project-owned build target or package script that produces the required output. Inspect the target body or script, select the declared package manager and toolchain, and check the artifact path or image against the runtime's configuration. For example, a Dockerfile that copies `dist/` needs a build that actually produces that directory. Use a conventional language command only when project evidence identifies its exact output and the deployment consumes it. For Go, `go build ./...` may only check compilation. For Python, an editable install changes the environment and requires a project-supported path that actually uses that environment.
2. **Deploy.** Prefer a verified local wrapper that retains the intended scope and gates. For Compose, bind the runtime and explicit service set using the [Compose procedure](prebuilt.md#docker-compose). A Compose-only project can use a combined command when the selected service has a verified `build:` definition and that command builds before starting or replacing it. Where the project supports a direct restart, use `systemctl restart <unit>`, `pm2 restart <app>`, or `supervisorctl restart <program>` against the bound manager and exact live target. Use a pm2 cluster reload only when the project supports it and the active processes load the intended output. Inspect the live manager's scope and actual permissions before deciding whether elevation is required.
3. **Resolve gaps.** If multiple candidates could consume different artifacts, change different services or trigger different side effects, show the evidence and ask for the choice that matters. If an expected output or executable cannot be identified, stop before deploying. In the plan, state the chosen command, the source of each decision, and how the build output reaches and is verified in the runtime.
