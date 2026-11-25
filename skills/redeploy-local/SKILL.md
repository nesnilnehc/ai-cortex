---
name: redeploy-local
description: Update and verify a local deployment using a source build or an existing artifact, such as a CI image, release package, or versioned binary. Use for Docker Compose, systemd, or process-manager deployments that need to run the requested code or artifact locally.
version: 3.4.0
license: MIT
---

# Skill: Redeploy Local

## Purpose

Update the project's local deployment from the requested source build or existing artifact. It applies to projects deployed locally through Docker Compose, a systemd unit, or a process manager (pm2, supervisorctl). Hot-reload development servers are out of scope.

---

## Core Objective

**Primary goal**: update one local deployment and verify that it runs the requested build or artifact.

**Success criteria** (all must be met):

1. ✅ **Directory confirmed**: the target directory is verified to exist before any command runs
2. ✅ **Input selected.** Identify a project-backed build command or a specific existing artifact.
3. ✅ **Input verified.** Confirm the build output or retrieve the existing artifact and verify its identity.
4. ✅ **Deployment method determined or configured**: the deployment target is identified (Compose / systemd / pm2 / supervisord)
5. ✅ **Deployment restarted**: the service/container has restarted and is reachable (a health check or status check passes)
6. ✅ **Run report emitted**: a command → exit code → duration table for every step executed

**Acceptance test**: after the skill finishes, the locally deployed service runs the requested build or artifact and the status check reports healthy/running.

---

## Scope Boundaries

**This skill covers**:

- Detecting the build system from project files (package.json, Makefile, go.mod, Cargo.toml, pom.xml, build.gradle, *.csproj, pyproject.toml)
- Detecting the local deployment method from project files (docker-compose.yml / compose.yaml, a systemd unit, a pm2 ecosystem file, supervisord.conf)
- Reading project-level config overrides (`.cortex.yaml` `build_command` / `deploy_command`)
- Persisting a successful inference to `.cortex/redeploy-local.yaml` for reuse on the next run
- Running build + restart in sequence
- Deploying a verified existing artifact without rebuilding it
- Reporting the result

**This skill does not cover**:

- Hot-reload development servers (npm run dev, vite, next dev) — these are not a "local deployment environment"
- Remote deployment (SSH, cloud, Kubernetes) — use a deployment skill aimed at remote infrastructure
- Planning or executing standalone database migrations. Retain migration gates already part of the project's local deployment workflow.
- Secret injection — environment variables / secrets must already be available in the deployment

**Handoff point**: the skill is done when the run report shows exit code 0 for every step. If any step fails, the skill reports the failure and stops — it does not retry or repair build errors on its own.

---

## Use Cases

- **Rebuild after an edit**: the agent has finished changing code; the user wants the local service to reflect the change without running build + restart commands by hand
- **Test a CI artifact locally** by running the same image or package that the existing build produced.
- **Multi-stack project**: the project mixes a compiled language (Go, Rust) with a Docker Compose deployment; the skill detects both
- **Scripted override**: `.cortex.yaml` gives CI-like reproducibility — the same commands on every run, with no detection drift
- **Shared team environment**: team members have different local setups; the skill adapts to the signals it detects instead of demanding one common toolchain

---

## Detection Approach

Prefer explicit `.cortex.yaml` commands, then a valid project cache. When either command is missing, read the [detection procedure](references/detection.md): inspect project files, choose a command supported by the project, and stop for a choice if evidence conflicts. Never invent a build or deployment target.

---

## Behavior

### Workflow (Checklist)

1. **Confirm the target directory**
   - Default: CWD
   - If the user gave a path: verify it exists (`test -d <path>`)
   - Abort with a clear error when the directory does not exist

#### Choose the deployment input

Check the user request and the project's declared local deployment workflow before reading the source-build cache.

- Honor an explicit request to use an existing artifact or to build from source.
- When the request leaves the input open, use a project-declared artifact workflow for this local target if one applies. Otherwise use the source-build steps below. A remote deployment workflow alone does not select an artifact for the local target.
- For an existing artifact, follow [Deploy an existing artifact](references/prebuilt.md) and bypass source-build detection, commands, and cache.
- If the requested input and documented local workflow conflict, look for a supported local path that consumes the requested input. Ask only if a remaining choice affects what will run. Preserve the selected input if deployment or verification fails.

#### Deploy from source

1. **Read the config override** (if `.cortex.yaml` exists)
   - Parse `build_command` and/or `deploy_command`
   - Record which fields were overridden; skip heuristic detection for those fields

2. **Check the inference cache** (Detection Approach step 0.5)
   - If it exists, read `.cortex/redeploy-local.yaml`
   - Validate it with the 6-step pseudo-logic
   - Cache hit: skip steps 3–4 and go to step 5 with the report annotated `(from cache, scanned YYYY-MM-DD; <N> signal files unchanged)`
   - Cache miss / malformed / expired: continue with step 3 (do not delete the file)
   - Fields overridden by `.cortex.yaml` (step 1) are excluded from cache reuse; the cache serves only the remaining fields, if its validation still passes

3. **Infer the build command** (when it is neither overridden nor cached)
   - Carry out Detection Approach steps 1–2: enumerate the signals, read the files, cross-reference
   - Record the evidence source and the chosen command
   - For a Compose-only project (no other build orchestration): mark "build skipped — subsumed by deploy"
   - No evidence: stop and ask the user for `build_command`, or have them fill in `.cortex.yaml`
   - Conflicting evidence: show the options to the user, do not choose silently

4. **Infer the deploy command** (when it is neither overridden nor cached)
   - Carry out Detection Approach step 3: read the deployment config files, prefer a Makefile wrapper
   - Record the source and the chosen command, including the extracted service/unit name
   - No evidence: stop and ask the user

5. **Resolve and show the inference**
   - Show the structured inference report (per Detection Approach step 4); annotate it when the cache was used
   - Ask only for missing choices when the evidence supports more than one command or deployment target
   - When the user's request already authorizes this local redeploy, continue without a second confirmation

6. **Run the build** (unless it was skipped)
   - Run the build command from the target directory
   - Stream the output live, without silent buffering
   - Time it with `{ start=$(date +%s); <cmd>; echo $(($(date +%s)-start))s; }`
   - On exit code ≠ 0: show the last 20 lines, report the failure, and stop — do not run the deployment

7. **Run the deployment restart**
   - Run the restart command
   - Time it the same way
   - On exit code ≠ 0: show the last 20 lines, report the partial state, and stop

8. **Health check**
   - Docker Compose: `docker compose ps` — confirm that every container shows `Up`
   - systemd: `systemctl is-active <unit>`
   - pm2: `pm2 list | grep <name>`
   - supervisord: `supervisorctl status <program>`
   - Record the result; if the health-check command is unavailable, warn, but do not mark the skill run as failed

9. **Emit the run report**

    ```text
    Step     Command                         Exit  Duration
    ───────  ──────────────────────────────  ────  ────────
    Build    pnpm run build                    0   18.2s
    Deploy   docker compose up -d --build      0    6.3s
    Health   docker compose ps                 0    0.2s
    ```

10. **Write the cache on success**
    - Write only when the build exited 0 (or was skipped as subsumed), the deployment exited 0, and the health check passed
    - If both commands came from `.cortex.yaml`, skip the write (the cache adds nothing)
    - On partial success (deployment 0 but unhealthy), skip the write — do not cache a configuration known to be broken
    - If `.cortex/` does not exist, create it (mode 0755), then write `.cortex/redeploy-local.yaml` with the header `# Auto-generated by redeploy-local skill; do not edit by hand`
    - Record the current `skill_version`, the resolved absolute `project_path`, an ISO 8601 UTC `written_at`, the chosen commands with their evidence, and every signal file read during inference together with its current mtime
    - On a write failure (permission denied, disk full, concurrent write): log `cache write skipped: <reason>` and continue — the deployment already succeeded, and the cache is only an optimization layer

### Interaction policy

- Ask only when detection is ambiguous or has failed
- Do not ask when `.cortex.yaml` supplies both commands
- If several choices remain, present them together in one question

---

## Input & Output

### Input requirements

- The target directory (an explicit path, or CWD)
- Optional: a `.cortex.yaml` carrying `build_command` and/or `deploy_command`
- For an existing artifact: a local package, image reference, version, or build reference resolvable to the intended artifact through project evidence

### Output contract

Provide:

- An inference report listing every chosen command and its evidence source (file + section/line + cross-reference)
- The build output streamed live, or the "skipped" note for a Compose-only project
- The deployment output streamed live
- The health-check result
- The run report table (command / exit code / duration per step)
- After a fully successful source-build run, the inference cache written to `.cortex/redeploy-local.yaml` when applicable
- For an existing artifact, its immutable identity, the local deployment target, and the observed running identity and health

---

## Restrictions

### Hard Boundaries

- **Never** run `rm -rf` or a destructive cleanup command without explicit user configuration
- **Never** assume a systemd, pm2, or supervisord service name — extract it from the config file, or ask
- **Never** continue after a step fails — report and stop
- **Never** restart a deployment before validating its input. Source deployments require a successful build, either separately or within the deployment command. Existing-artifact deployments require the exact artifact and a deployment command that cannot rebuild it.
- **Never** edit the target deployment's environment or secrets. Pass the selected artifact through a documented artifact parameter or a temporary deployment override.
- **Never** add `sudo` without supporting evidence, such as a systemd unit file owned by root while the current uid differs; ask the user to confirm the elevation before running

### Failure modes

| Failure | Behavior |
| --- | --- |
| Directory not found | Abort immediately; show the exact path that was checked |
| No build evidence | Stop before the build; ask the user for `build_command`, or have them fill in `.cortex.yaml` |
| No deploy evidence | Stop before the deployment; ask the user for `deploy_command`, or have them fill in `.cortex.yaml` |
| Conflicting evidence, such as a Makefile that disagrees with CI | Stop; show both options and their sources to the user; let the user choose |
| Name/unit extraction failed | Stop; ask the user to supply the name explicitly |
| Build exit code ≠ 0 | Show the last 20 lines; stop; do not run the deployment |
| Deployment exit code ≠ 0 | Show the last 20 lines; stop; report the partial state |
| Health check failed | Warn; do not mark the skill run as failed; do not write the cache |
| Cache file malformed, or missing a required key | Treat as a cache miss; fall back to a full scan; do not delete it; overwrite it after a successful run |
| A recorded signal file was deleted, or its mtime changed | Cache miss; rescan |
| Cached `skill_version` differs from the current one | Cache miss; rescan |
| Cache write failed (permissions / disk full) | Log a warning; do not mark the skill run as failed — the deployment already succeeded |

---

## Self-Check

### Core success criteria

- [ ] **Directory confirmed**: the target directory was verified to exist before any command ran
- [ ] **Detection traceable**: every inferred command is attributed to concrete evidence (file + line/section, ideally with a cross-reference) — not invented
- [ ] **Input preserved**: a combined source deployment builds once. An existing-artifact deployment skips building and verifies the running artifact identity.
- [ ] **Commands grounded**: build and deployment commands were traced to project evidence or an explicit override; remaining ambiguity was resolved before execution
- [ ] **Build succeeded**: exit code 0 was confirmed before the deployment ran, or the build step was legitimately skipped
- [ ] **Deployment succeeded**: exit code 0 was confirmed before the health check
- [ ] **Health check run**: the status was checked and recorded (warn when unavailable; do not fail)
- [ ] **Run report emitted**: the table covers command / exit code / duration for every step
- [ ] **Cache honored or refreshed**: source builds read `.cortex/redeploy-local.yaml` before inference and write it only after successful build, deployment, and health checks when applicable. Existing-artifact deployments bypass it.

### Process quality checks

- [ ] **No silent buffering**: build and deployment output stream live rather than being buffered
- [ ] **Durations recorded**: wall-clock time was measured for every step
- [ ] **Names/units come from the source**: pm2/supervisord/systemd names are extracted from the config file, not hard-coded
- [ ] **Interaction kept minimal**: a clear, authorized local redeploy proceeds without a redundant confirmation

---

## Examples

Consult [worked examples](references/examples.md) when detection or recovery is ambiguous.
