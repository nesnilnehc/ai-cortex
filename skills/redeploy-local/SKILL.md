---
name: redeploy-local
description: After code changes, auto-detect the project's build system and local deployment method for a given directory, then build the project and restart its locally-deployed environment (Docker Compose / systemd / process manager). Never assumes — asks only when detection is ambiguous. Caches detected commands per project in .cortex/redeploy-local.yaml; re-invocations on the same project skip re-scanning until signal files change, the cache expires (30 days), or the skill version bumps.
description_zh: 代码修改后，自动探测目标目录的构建系统与本地部署方式，执行构建并重启本地部署环境（Docker Compose / systemd / 进程管理器）。无法确定时才询问，不盲猜。首次探测后将结果缓存至 .cortex/redeploy-local.yaml；下次同项目调用直接复用，直到信号文件变更、缓存过期（30 天）或技能版本变化。
tags: [deploy, build, local, workflow, automation, docker, systemd, pm2]
version: 3.2.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [redeploy local, redeploy locally, rebuild and redeploy, update local env, rebuild local, deploy local, build and deploy, 本地重部署, 重部署本地, 更新本地环境, 重建并部署, 本地部署]
input_schema:
  type: free-form
  description: A directory path (defaults to CWD). May include an optional override for build or deploy command via .cortex.yaml. Cache at .cortex/redeploy-local.yaml is honored when valid.
output_schema:
  type: side-effect
  description: Build artifacts produced; local deployment updated (Docker Compose / systemd / process manager); inferences cached to .cortex/redeploy-local.yaml on success. Outputs (1) an inference report attributing each chosen command to its evidence source, and (2) a structured run report with command, exit code, and duration per step.
---

# Skill: Redeploy Local

## Purpose

After the agent has changed code, run the project's build and restart the locally deployed environment — the user does not need to know the project's tech stack. It applies to projects deployed locally through Docker Compose, a systemd unit, or a process manager (pm2, supervisorctl). Hot-reload development servers are deliberately out of scope; the target is a running local environment, not a development watch mode.

---

## Core Objective

**Primary goal**: given a directory, run one build and one local deployment restart successfully, and report what was run.

**Success criteria** (all must be met):

1. ✅ **Directory confirmed**: the target directory is verified to exist before any command runs
2. ✅ **Build command determined or configured**: the command traces back to a config file or a detection heuristic — never invented
3. ✅ **Build succeeded**: exit code 0; the build artifacts exist where they are expected
4. ✅ **Deployment method determined or configured**: the deployment target is identified (Compose / systemd / pm2 / supervisord)
5. ✅ **Deployment restarted**: the service/container has restarted and is reachable (a health check or status check passes)
6. ✅ **Run report emitted**: a command → exit code → duration table for every step executed

**Acceptance test**: after the skill finishes, the locally deployed service reflects the latest code changes and the status check reports healthy/running.

---

## Scope Boundaries

**This skill covers**:

- Detecting the build system from project files (package.json, Makefile, go.mod, Cargo.toml, pom.xml, build.gradle, *.csproj, pyproject.toml)
- Detecting the local deployment method from project files (docker-compose.yml / compose.yaml, a systemd unit, a pm2 ecosystem file, supervisord.conf)
- Reading project-level config overrides (`.cortex.yaml` `build_command` / `deploy_command`)
- Persisting a successful inference to `.cortex/redeploy-local.yaml` for reuse on the next run
- Running build + restart in sequence
- Reporting the result

**This skill does not cover**:

- Hot-reload development servers (npm run dev, vite, next dev) — these are not a "local deployment environment"
- Remote deployment (SSH, cloud, Kubernetes) — use a deployment skill aimed at remote infrastructure
- Database migrations — run those separately before invoking this skill
- Secret injection — environment variables / secrets must already be available in the deployment

**Handoff point**: the skill is done when the run report shows exit code 0 for every step. If any step fails, the skill reports the failure and stops — it does not retry or repair build errors on its own.

---

## Use Cases

- **Rebuild after an edit**: the agent has finished changing code; the user wants the local service to reflect the change without running build + restart commands by hand
- **Multi-stack project**: the project mixes a compiled language (Go, Rust) with a Docker Compose deployment; the skill detects both
- **Scripted override**: `.cortex.yaml` gives CI-like reproducibility — the same commands on every run, with no detection drift
- **Shared team environment**: team members have different local setups; the skill adapts to the signals it detects instead of demanding one common toolchain

---

## Detection Approach

This skill does **not** maintain a hard-coded "file X → command Y" mapping. Build and deploy commands differ from project to project — two Go projects can follow entirely different build conventions (custom ldflags, output paths, cross-compilation targets), and a Node project's `build` script is not necessarily the one the deployment needs (it may need `build:prod`). The agent's job is to **scan the directory, read the relevant files, and infer the commands the project actually uses** — and then show those inferences to the user for confirmation.

### Step 0: use the config override first

Check for `.cortex.yaml` in the target directory:

```yaml
build_command: make release
deploy_command: docker compose up -d --build
```

If both fields are present, use them directly and skip steps 1–4 (no confirmation needed either). If only one is present, run inference for the other, and still carry out the step 4 confirmation.

### Step 0.5: use the inference cache first

After step 0 (override) and before step 1 (the full scan), check for `.cortex/redeploy-local.yaml` in the target directory. If it is valid, reuse the cached inference and jump straight to step 4 (show the inference for confirmation — the user still confirms the report, annotated `(from cache, scanned YYYY-MM-DD; <N> signal files unchanged)`). If it is missing, malformed, or expired, fall back to step 1 — never delete an expired cache file automatically; the next successful run overwrites it.

The `.cortex.yaml` override (step 0) takes precedence over the cache. If step 0 set one of the commands, that command comes from `.cortex.yaml` and the cache serves only the other field, if its validation still passes.

**Never commit `.cortex/redeploy-local.yaml`** — it encodes absolute paths and mtimes local to the host machine; add it, or the whole `.cortex/` directory, to `.gitignore`. The file can be regenerated after the first successful run.

**Cache file schema** (`.cortex/redeploy-local.yaml`):

```yaml
# Auto-generated by redeploy-local skill; do not edit by hand
skill_version: 3.2.0
project_path: /Users/alice/work/api-service
written_at: 2026-05-20T14:32:11Z

build:
  command: pnpm run build
  evidence:
    - file: package.json
      ref: scripts.build
    - file: Dockerfile
      ref: "COPY dist/ (cross-ref)"

deploy:
  command: docker compose up -d --build
  evidence:
    - file: docker-compose.yml
      ref: "services: api, worker, db"

signal_files:
  - path: package.json
    mtime: 2026-05-20T11:02:44Z
  - path: pnpm-lock.yaml
    mtime: 2026-05-18T09:14:02Z
  - path: Dockerfile
    mtime: 2026-05-19T16:55:31Z
  - path: docker-compose.yml
    mtime: 2026-05-20T10:48:09Z
```

`evidence` records only `file` + `ref` (such as `scripts.build`) — the command body itself is not repeated, which keeps the cache small and free of drift. `signal_files` records every file **read** during inference, cross-references included, not only the file the chosen command came from.

**Validation pseudo-logic** — check in order; the first failure counts as a cache miss:

1. The file exists and parses as YAML; the required top-level keys are present (`skill_version`, `project_path`, `written_at`, `build`, `deploy`, `signal_files`).
2. `skill_version` as a string equals the `version` value in this skill's current frontmatter.
3. `project_path` equals the resolved absolute target directory, with symlinks resolved through `realpath`.
4. `now() - written_at` < 30 days.
5. For every entry in `signal_files`: the path still exists, and its current mtime equals the recorded mtime.
6. `build.command` and `deploy.command` are non-empty strings.

All pass → cache hit (jump to step 4 with the annotation). Any failure → cache miss; log `cache invalid: <reason>; falling back to full scan` and continue with step 1.

### Step 1: enumerate the signal files

Walk the target directory (depth 1, plus `deploy/`, `.github/workflows/`, `docs/`) and collect which of these files exist:

- **Build orchestration**: `Makefile`, `Taskfile.yml`, `justfile`, `package.json`, `scripts/build*`
- **Containers**: `Dockerfile`, `docker-compose.yml`, `compose.yaml`, `compose.*.yaml`
- **Language manifests**: `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle*`, `*.csproj`, `*.sln`, `pyproject.toml`, `setup.py`
- **Local deployment**: `ecosystem.config.{js,cjs,json}`, `supervisord.conf`, `supervisor/*.conf`, `deploy/*.service`, `Procfile`
- **Documentation, which usually encodes the commands**: `README.md`, `CONTRIBUTING.md`, `docs/development*.md`, `docs/build*.md`
- **CI as the authoritative reference**: `.github/workflows/*.yml`, `.gitlab-ci.yml`, `Jenkinsfile` — these usually pin the build command the team agreed on

### Step 2: read the files and infer the build command

For every signal found, **read its contents** — do not assume a default:

- **`Makefile`**: enumerate the targets (`grep -E '^[a-zA-Z_-]+:' Makefile`); look for `build`, `release`, `compile`, `dist`, `all`. Read the body of a candidate target to confirm that it really performs a build rather than just echoing. If several plausible targets exist, list them and ask the user which one to use.
- **`package.json`**: read the `scripts` object. Look for `build`, `build:prod`, `compile`, `bundle`. If the Dockerfile copies `dist/`, prefer the script that produces `dist/`. Detect the package manager from the lockfile (`pnpm-lock.yaml` → pnpm; `yarn.lock` → yarn; `package-lock.json` → npm).
- **`Taskfile.yml` / `justfile`**: enumerate the tasks/recipes the same way as the Makefile.
- **`Dockerfile`**: inspect the `COPY`, `RUN`, and `CMD` lines to understand which artifacts the image expects and which parts of the build happen inside the container. Use it as a **cross-reference** — a `COPY dist/` means the host build must produce `dist/` — since the Dockerfile itself is almost never the host build command.
- **CI workflow**: search for the build job/step; the authoritative command appears there verbatim. Use it as a **cross-reference** to validate the other signals.
- **`README.md` / `docs/`**: scan the "Build"/"Development"/"Getting Started" sections; look for code blocks containing shell commands.
- **Language manifest only** (no Makefile, no scripts): only in this case fall back to the language's conventional command, and only once a scan of the README and CI has confirmed there is no project-specific override. Examples (last-resort defaults only): Go → `go build ./...`; Rust → `cargo build --release`; Python → `pip install -e .`; Java/Maven → `mvn package`; Java/Gradle → `./gradlew build`; .NET → `dotnet build`.

**Evidence priority** (highest to lowest):
1. A `Makefile` / `Taskfile` / `justfile` target with clear build semantics
2. A `package.json` script (Node projects)
3. A documented build step in the CI workflow
4. A code block in the README's "Build" section
5. The language manifest fallback (`go build`, `cargo build`, and so on) — only when none of the above exists

**Conflict resolution**: if the Makefile says `make build` while CI says `make release`, show both and their sources to the user and ask which to run. Never choose silently.

### Step 3: read the files and infer the deploy command

Same principle — read the deployment files, do not assume:

- **`docker-compose.yml`**: list the services defined; the standard command is `docker compose up -d --build`. If the `Makefile` has a `deploy`/`up`/`run` target wrapping Compose, prefer the Makefile target — it carries the project-specific flags (profiles, env files).
- **`ecosystem.config.{js,cjs}`**: read the file and extract `apps[].name`. With `exec_mode: cluster`, prefer `pm2 reload <name>` (zero downtime); otherwise `pm2 restart <name>`.
- **`supervisord.conf`**: enumerate the `[program:<name>]` sections. If several programs are defined, list them and ask which to restart, or have the user confirm `supervisorctl restart all`.
- **`deploy/*.service`**: derive the unit name from the file name. Check the file ownership against the current uid to decide whether `sudo` is needed.
- **A `Makefile` with a `deploy`/`restart`/`up` target**: such a target usually encodes the project's real restart procedure (env vars, pre-hooks). Prefer it over raw `docker compose` / `systemctl`.
- **Compose-only project** (no other build orchestration): the build step is **subsumed** by `docker compose up -d --build` — do not run a separate build; mark the build step "skipped — subsumed by deploy".

**Evidence priority** (highest to lowest):
1. A `Makefile` `deploy`/`restart`/`up` target (the project-specific wrapper)
2. The Compose / pm2 / supervisord / systemd config file (the deployment medium itself)
3. A code block in the README's "Deploy"/"Run" section

### Step 4: show the inference for confirmation

Before doing anything, show the user a structured inference report:

```yaml
Detected build:
  Source: Makefile target `build` (line 12, calls `go build -ldflags ...`)
  Cross-ref: README "Building" section confirms `make build`
  Command: make build

Detected deploy:
  Source: docker-compose.yml (services: api, worker, db)
  Cross-ref: Makefile `up` target wraps it with --env-file
  Command: make up   ← Makefile wrapper preferred over raw compose
```

Proceed only after the user confirms. The confirmation is skipped when both commands come from `.cortex.yaml`.

---

## Behavior

### Workflow (Checklist)

1. **Confirm the target directory**
   - Default: CWD
   - If the user gave a path: verify it exists (`test -d <path>`)
   - Abort with a clear error when the directory does not exist

2. **Read the config override** (if `.cortex.yaml` exists)
   - Parse `build_command` and/or `deploy_command`
   - Record which fields were overridden; skip heuristic detection for those fields

3. **Check the inference cache** (Detection Approach step 0.5)
   - If it exists, read `.cortex/redeploy-local.yaml`
   - Validate it with the 6-step pseudo-logic
   - Cache hit: skip steps 4–5 and go to step 6 with the report annotated `(from cache, scanned YYYY-MM-DD; <N> signal files unchanged)`
   - Cache miss / malformed / expired: continue with step 4 (do not delete the file)
   - Fields overridden by `.cortex.yaml` (step 2) are excluded from cache reuse; the cache serves only the remaining fields, if its validation still passes

4. **Infer the build command** (when it is neither overridden nor cached)
   - Carry out Detection Approach steps 1–2: enumerate the signals, read the files, cross-reference
   - Record the evidence source and the chosen command
   - For a Compose-only project (no other build orchestration): mark "build skipped — subsumed by deploy"
   - No evidence: stop and ask the user for `build_command`, or have them fill in `.cortex.yaml`
   - Conflicting evidence: show the options to the user, do not choose silently

5. **Infer the deploy command** (when it is neither overridden nor cached)
   - Carry out Detection Approach step 3: read the deployment config files, prefer a Makefile wrapper
   - Record the source and the chosen command, including the extracted service/unit name
   - No evidence: stop and ask the user

6. **Show the inference and confirm**
   - Show the structured inference report (per Detection Approach step 4); annotate it when the cache was used
   - Wait for the user's confirmation
   - Skip the confirmation only when both commands come from `.cortex.yaml`
   - If the same directory + commands were already confirmed in this conversation, skip the repeat confirmation

7. **Run the build** (unless it was skipped)
   - Run the build command from the target directory
   - Stream the output live, without silent buffering
   - Time it with `{ start=$(date +%s); <cmd>; echo $(($(date +%s)-start))s; }`
   - On exit code ≠ 0: show the last 20 lines, report the failure, and stop — do not run the deployment

8. **Run the deployment restart**
   - Run the restart command
   - Time it the same way
   - On exit code ≠ 0: show the last 20 lines, report the partial state, and stop

9. **Health check**
   - Docker Compose: `docker compose ps` — confirm that every container shows `Up`
   - systemd: `systemctl is-active <unit>`
   - pm2: `pm2 list | grep <name>`
   - supervisord: `supervisorctl status <program>`
   - Record the result; if the health-check command is unavailable, warn, but do not mark the skill run as failed

10. **Emit the run report**

    ```
    Step     Command                         Exit  Duration
    ───────  ──────────────────────────────  ────  ────────
    Build    pnpm run build                    0   18.2s
    Deploy   docker compose up -d --build      0    6.3s
    Health   docker compose ps                 0    0.2s
    ```

11. **Write the cache on success**
    - Write only when the build exited 0 (or was skipped as subsumed), the deployment exited 0, and the health check passed
    - If both commands came from `.cortex.yaml`, skip the write (the cache adds nothing)
    - On partial success (deployment 0 but unhealthy), skip the write — do not cache a configuration known to be broken
    - If `.cortex/` does not exist, create it (mode 0755), then write `.cortex/redeploy-local.yaml` with the header `# Auto-generated by redeploy-local skill; do not edit by hand`
    - Record the current `skill_version`, the resolved absolute `project_path`, an ISO 8601 UTC `written_at`, the chosen commands with their evidence, and every signal file read during inference together with its current mtime
    - On a write failure (permission denied, disk full, concurrent write): log `cache write skipped: <reason>` and continue — the deployment already succeeded, and the cache is only an optimization layer

### Interaction policy

- Ask only when detection is ambiguous or has failed
- Do not ask when `.cortex.yaml` supplies both commands
- One confirmation prompt covers both build and deploy; do not prompt twice in the same run
- If the same directory and commands were already confirmed in this conversation, skip the re-confirmation

---

## Input & Output

### Input requirements

- The target directory (an explicit path, or CWD)
- Optional: a `.cortex.yaml` carrying `build_command` and/or `deploy_command`

### Output contract

Provide:

- An inference report listing every chosen command and its evidence source (file + section/line + cross-reference)
- The build output streamed live, or the "skipped" note for a Compose-only project
- The deployment output streamed live
- The health-check result
- The run report table (command / exit code / duration per step)
- After a fully successful run (build + deployment + health check all pass), the inference cache written to `.cortex/redeploy-local.yaml`

---

## Restrictions

### Hard Boundaries

- **Never** run `rm -rf` or a destructive cleanup command without explicit user configuration
- **Never** assume a systemd, pm2, or supervisord service name — extract it from the config file, or ask
- **Never** continue after a step fails — report and stop
- **Never** run the deployment restart without a preceding successful build (exit code 0), except for a Compose-only project, where the deployment subsumes the build
- **Never** inject or modify the target deployment's environment variables
- **Never** add `sudo` without supporting evidence, such as a systemd unit file owned by root while the current uid differs; ask the user to confirm the elevation before running

### Failure modes

| Failure | Behavior |
|---|---|
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
- [ ] **No double build**: a Compose-only project skips the build step; `--build` handles it inside the deploy command
- [ ] **User confirmed**: the commands were shown and confirmed before the first execution (skipped only when both come from `.cortex.yaml`)
- [ ] **Build succeeded**: exit code 0 was confirmed before the deployment ran, or the build step was legitimately skipped
- [ ] **Deployment succeeded**: exit code 0 was confirmed before the health check
- [ ] **Health check run**: the status was checked and recorded (warn when unavailable; do not fail)
- [ ] **Run report emitted**: the table covers command / exit code / duration for every step
- [ ] **Cache honored or refreshed**: `.cortex/redeploy-local.yaml` is read before scanning, and written only after a fully successful run (build + deployment + health check all pass)

### Process quality checks

- [ ] **No silent buffering**: build and deployment output stream live rather than being buffered
- [ ] **Durations recorded**: wall-clock time was measured for every step
- [ ] **Names/units come from the source**: pm2/supervisord/systemd names are extracted from the config file, not hard-coded
- [ ] **Interaction kept minimal**: no redundant prompts; the re-confirmation is skipped when it already happened in this conversation

---

## Examples

### Example 1: a Node.js app + Docker Compose

**Directory contents**: `package.json`, `pnpm-lock.yaml`, `Dockerfile`, `docker-compose.yml`, `README.md`

**Inference**:
- Read `package.json` `scripts`: found `build`, `build:prod`, `test`, `lint`
- Read `Dockerfile`: `COPY dist/ /app/` — the image expects `dist/` to exist
- Read `package.json` `scripts.build`: `tsc && vite build --outDir dist` — produces `dist/`, which matches
- `scripts.build:prod` is `NODE_ENV=production npm run build` — also usable, but `build` is the default the README refers to
- Detect the package manager: `pnpm-lock.yaml` → pnpm

**Inference report shown to the user**:

```yaml
Detected build:
  Source: package.json scripts.build (tsc && vite build --outDir dist)
  Cross-ref: Dockerfile copies dist/, matches output path
  Command: pnpm run build

Detected deploy:
  Source: docker-compose.yml (3 services: api, worker, db)
  Command: docker compose up -d --build
```

**After the user confirms**, the run report:

```text
Step     Command                         Exit  Duration
───────  ──────────────────────────────  ────  ────────
Build    pnpm run build                    0   18.2s
Deploy   docker compose up -d --build      0    6.3s
Health   docker compose ps                 0    0.2s
```

### Example 2: a Go service + a Makefile wrapper

**Directory contents**: `go.mod`, `Makefile`, `deploy/myapp.service`, `.github/workflows/ci.yml`

**Inference**:
- Read the `Makefile` targets: `build`, `test`, `lint`, `release`, `install`
- Read the body of the `build` target in the `Makefile`: `go build -ldflags "-X main.Version=$(VERSION)" -o bin/myapp ./cmd/myapp` — project-specific ldflags and output path; `go build ./...` is not taken as the default
- Cross-reference `.github/workflows/ci.yml`: the build step runs `make build` — confirmed as authoritative
- Read `deploy/myapp.service`: file name → unit `myapp`; the file owner (`root`) against the current uid → `sudo systemctl restart myapp` may be needed

**Inference report**:

```yaml
Detected build:
  Source: Makefile target `build` (line 8)
  Cross-ref: .github/workflows/ci.yml uses `make build`
  Command: make build

Detected deploy:
  Source: deploy/myapp.service (unit name from filename)
  Note: unit file owned by root → sudo required
  Command: sudo systemctl restart myapp
```

### Example 3: a Compose-only project (the build step is skipped)

**Directory contents**: `docker-compose.yml`, `Dockerfile` (no Makefile, package.json, or language manifest in the root)

**Inference**:
- No build orchestration found outside the Docker context
- `Dockerfile` performs the build during `docker compose up --build`
- Therefore: skip the standalone build; the deploy command subsumes it

**Run report**:

```text
Step     Command                         Exit  Duration
───────  ──────────────────────────────  ────  ────────
Build    (skipped — subsumed by deploy)   —      —
Deploy   docker compose up -d --build      0    9.1s
Health   docker compose ps                 0    0.2s
```

### Example 4: a config override through .cortex.yaml

**`.cortex.yaml`**:

```yaml
build_command: make release GOARCH=arm64
deploy_command: supervisorctl restart api-worker
```

**Detection**: both commands are read from `.cortex.yaml` — no heuristics applied, no confirmation prompt shown.

**Run report**:

```text
Step     Command                          Exit  Duration
───────  ───────────────────────────────  ────  ────────
Build    make release GOARCH=arm64          0   22.7s
Deploy   supervisorctl restart api-worker   0    0.8s
Health   supervisorctl status api-worker    0    0.1s
```

### Example 5: build failure (edge case)

**Scenario**: `pnpm run build` exits with code 1

```json
[build] FAILED — exit 1 after 4.2s

Last 20 lines of output:
  ...
  Error: cannot find module 'express'

Deployment step skipped.
Suggested fix: run `pnpm install` to restore dependencies, then retry.
```

### Example 6: a cache hit on a previously deployed project

**Directory contents**: the same as example 1 (`package.json`, `pnpm-lock.yaml`, `Dockerfile`, `docker-compose.yml`, `README.md`), plus the `.cortex/redeploy-local.yaml` written after an earlier successful run.

**Detection**:
- Step 0: no `.cortex.yaml` override
- Step 0.5: read `.cortex/redeploy-local.yaml`; validation passes (same skill version, same `project_path`, 2 days old, all 4 `signal_files` mtimes unchanged)
- Skip steps 1–3 (the full scan); go straight to step 4 with the cache annotation

**Inference report shown to the user**:

```yaml
Detected build:
  Source: .cortex/redeploy-local.yaml (cached 2026-05-20; 4 signal files unchanged)
  Command: pnpm run build

Detected deploy:
  Source: .cortex/redeploy-local.yaml (cached 2026-05-20; 4 signal files unchanged)
  Command: docker compose up -d --build
```

**After the user confirms**, the run report (the same commands as example 1, without the scan overhead):

```text
Step     Command                         Exit  Duration
───────  ──────────────────────────────  ────  ────────
Build    pnpm run build                    0   17.8s
Deploy   docker compose up -d --build      0    6.1s
Health   docker compose ps                 0    0.2s
```

The cache file is rewritten on success with a refreshed `written_at` and the current signal file mtimes.
