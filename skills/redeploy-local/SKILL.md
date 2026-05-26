---
name: redeploy-local
description: After code changes, auto-detect the project's build system and local deployment method for a given directory, then build the project and restart its locally-deployed environment (Docker Compose / systemd / process manager). Never assumes — asks only when detection is ambiguous. Caches detected commands per project in .cortex/redeploy-local.yaml; re-invocations on the same project skip re-scanning until signal files change, the cache expires (30 days), or the skill version bumps.
description_zh: 代码修改后，自动探测目标目录的构建系统与本地部署方式，执行构建并重启本地部署环境（Docker Compose / systemd / 进程管理器）。无法确定时才询问，不盲猜。首次探测后将结果缓存至 .cortex/redeploy-local.yaml；下次同项目调用直接复用，直到信号文件变更、缓存过期（30 天）或技能版本变化。
tags: [deploy, build, local, workflow, automation, docker, systemd, pm2]
version: 3.1.0
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

# Skill: redeploy-local

## Purpose

After an Agent modifies code, execute the project's build and restart its locally-deployed environment — without requiring the user to know the project's tech stack. Covers projects that deploy locally via Docker Compose, systemd units, or process managers (pm2, supervisorctl). Intentionally excludes hot-reload dev servers; the target is a running local environment, not a development watch mode.

---

## Core Objective

**Primary goal**: Given a directory, produce one successful build and one successful local deployment restart, and report what was run.

**Success Criteria** (all must be satisfied):

1. ✅ **Directory resolved**: Target directory confirmed to exist before any command is run
2. ✅ **Build command detected or configured**: Command is traceable to a config file or detection heuristic — not invented
3. ✅ **Build succeeded**: Exit code 0; build artifacts present where expected
4. ✅ **Deploy method detected or configured**: Deployment target identified (Compose / systemd / pm2 / supervisord)
5. ✅ **Deployment restarted**: Service/container restarted and reachable (health check or status check)
6. ✅ **Run report emitted**: Table of command → exit code → duration for every step executed

**Acceptance Test**: After the skill completes, the locally deployed service reflects the latest code changes and its status check reports healthy/running.

---

## Scope Boundaries

**This skill handles**:

- Detecting build system from project files (package.json, Makefile, go.mod, Cargo.toml, pom.xml, build.gradle, *.csproj, pyproject.toml)
- Detecting local deployment from project files (docker-compose.yml / compose.yaml, systemd unit, pm2 ecosystem file, supervisord.conf)
- Reading project-level config overrides (`.cortex.yaml` `build_command` / `deploy_command`)
- Persisting successful inferences to `.cortex/redeploy-local.yaml` and reusing them on next run
- Executing build + restart in sequence
- Reporting results

**This skill does not handle**:

- Hot-reload dev servers (npm run dev, vite, next dev) — those are not "local deployed environments"
- Remote deployment (SSH, cloud, Kubernetes) — use a deploy skill targeting remote infra
- Database migrations — run those separately before invoking this skill
- Secret injection — environment variables / secrets must already be available in the deployment

**Handoff point**: When the run report shows all steps exit 0, skill is done. If any step fails, the skill reports the failure and stops — it does not auto-retry or patch the build error.

---

## Use Cases

- **Post-edit rebuild**: Agent finishes modifying code; user wants the local service to reflect the change without manually running build + restart commands
- **Multi-stack projects**: Project mixes a compiled language (Go, Rust) with a Docker Compose deployment; skill detects both automatically
- **Scripted overrides**: CI-like reproducibility via `.cortex.yaml` — same commands every time, no detection variance
- **Shared team environments**: Different team members have different local setups; skill adapts per detected signals rather than requiring identical toolchain

---

## Detection Approach

This skill does **NOT** carry a hardcoded mapping of "file X → command Y". Build and deploy commands are project-specific — two Go projects can have entirely different build conventions (custom ldflags, output paths, cross-compile targets), and a Node project's `build` script may not be what deploy needs (it might want `build:prod` instead). The agent's job is to **scan the directory, read the relevant files, and infer the project's actual commands** — then surface those inferences for user confirmation.

### Step 0: Honor config override

Check for `.cortex.yaml` in the target directory:

```yaml
build_command: make release
deploy_command: docker compose up -d --build
```

If both fields are present, use them verbatim and skip Steps 1–4 (no confirmation needed either). If only one is present, run inference for the other and still go through Step 4 for confirmation.

### Step 0.5: Honor inference cache

After Step 0 (override) but before Step 1 (full scan), check `.cortex/redeploy-local.yaml` in the target directory. If valid, reuse the cached inferences and jump to Step 4 (Present inferences for confirmation — the user still confirms the report, annotated `(from cache, scanned YYYY-MM-DD; <N> signal files unchanged)`). If absent, malformed, or stale, fall through to Step 1 — never auto-delete a stale cache file; the next successful run overwrites it.

`.cortex.yaml` override (Step 0) wins over the cache. If Step 0 set one of the two commands, that command is taken from `.cortex.yaml` and the cache supplies only the other (if its validation still passes for the remaining field).

**NEVER commit `.cortex/redeploy-local.yaml`** — it encodes host-local absolute paths and mtimes; add it (or the whole `.cortex/` directory) to `.gitignore`. The file is regenerable on first successful run.

**Cache file schema** (`.cortex/redeploy-local.yaml`):

```yaml
# Auto-generated by redeploy-local skill; do not edit by hand
skill_version: 3.1.0
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

`evidence` records only `file` + `ref` (e.g. `scripts.build`) — the command body itself is not duplicated, to keep the cache small and free of drift. `signal_files` records every file READ during inference (including cross-references), not just the file the chosen command came from.

**Validation pseudo-logic** — check in order, first failure is a cache miss:

1. File exists and parses as YAML; top-level required keys present (`skill_version`, `project_path`, `written_at`, `build`, `deploy`, `signal_files`).
2. `skill_version` string-equals the current skill's frontmatter `version` value.
3. `project_path` equals the resolved absolute target directory (symlinks resolved via `realpath`).
4. `now() - written_at` < 30 days.
5. Every entry in `signal_files`: path still exists AND current mtime equals the recorded mtime.
6. `build.command` and `deploy.command` are non-empty strings.

All pass → cache hit (jump to Step 4 with annotation). Any failure → cache miss; log `cache invalid: <reason>; falling back to full scan` and continue to Step 1.

### Step 1: Inventory signal files

Walk the target directory (depth 1, plus `deploy/`, `.github/workflows/`, `docs/`) and collect the presence of:

- **Build orchestration**: `Makefile`, `Taskfile.yml`, `justfile`, `package.json`, `scripts/build*`
- **Container**: `Dockerfile`, `docker-compose.yml`, `compose.yaml`, `compose.*.yaml`
- **Language manifests**: `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle*`, `*.csproj`, `*.sln`, `pyproject.toml`, `setup.py`
- **Local deploy**: `ecosystem.config.{js,cjs,json}`, `supervisord.conf`, `supervisor/*.conf`, `deploy/*.service`, `Procfile`
- **Documentation that often encodes commands**: `README.md`, `CONTRIBUTING.md`, `docs/development*.md`, `docs/build*.md`
- **CI as canonical reference**: `.github/workflows/*.yml`, `.gitlab-ci.yml`, `Jenkinsfile` — these often pin the team-blessed build command

### Step 2: Read & infer the build command

For each signal found, **read its contents** (do not assume defaults):

- **`Makefile`**: enumerate targets (`grep -E '^[a-zA-Z_-]+:' Makefile`); look for `build`, `release`, `compile`, `dist`, `all`. Read the body of the candidate target to confirm it actually builds (not just echoes). If multiple plausible targets exist, list them and ask the user which.
- **`package.json`**: read the `scripts` object. Look for `build`, `build:prod`, `compile`, `bundle`. If Dockerfile copies `dist/`, prefer the script that produces `dist/`. Detect package manager via lockfile (`pnpm-lock.yaml` → pnpm; `yarn.lock` → yarn; `package-lock.json` → npm).
- **`Taskfile.yml` / `justfile`**: enumerate tasks/recipes the same way as Makefile.
- **`Dockerfile`**: inspect `COPY`, `RUN`, `CMD` lines to understand what artifacts the image expects and what builds happen inside the container. Use as a **cross-reference** (e.g., `COPY dist/` means the host build must produce `dist/`) — Dockerfile is rarely the host build command itself.
- **CI workflow**: search build-like jobs/steps; the canonical command appears verbatim. Use as **cross-reference** to validate other signals.
- **`README.md` / `docs/`**: scan for "Build" / "Development" / "Getting Started" sections; look for fenced code blocks with shell commands.
- **Language manifests alone** (no Makefile, no scripts): only then fall back to the language's conventional command, and only **after** scanning README/CI to see if there's a project-specific override. Examples (only as last-resort defaults): Go → `go build ./...`; Rust → `cargo build --release`; Python → `pip install -e .`; Java/Maven → `mvn package`; Java/Gradle → `./gradlew build`; .NET → `dotnet build`.

**Priority of evidence** (highest first):
1. `Makefile` / `Taskfile` / `justfile` target with explicit build semantics
2. `package.json` script (for Node projects)
3. CI workflow's documented build step
4. README's "Build" section code block
5. Language manifest fallback (`go build`, `cargo build`, etc.) — only when above are absent

**Conflict resolution**: if Makefile says `make build` and CI says `make release`, surface both to the user with their sources and ask which to run. Never silently pick.

### Step 3: Read & infer the deploy command

Same principle — read the deploy-related files, don't assume:

- **`docker-compose.yml`**: list defined services; the standard command is `docker compose up -d --build`. If a `Makefile` has `deploy`/`up`/`run` targets that wrap Compose, prefer the Makefile target — it captures project-specific flags (profiles, env files).
- **`ecosystem.config.{js,cjs}`**: read the file and extract `apps[].name`. If `exec_mode: cluster`, prefer `pm2 reload <name>` (zero-downtime); otherwise `pm2 restart <name>`.
- **`supervisord.conf`**: enumerate `[program:<name>]` sections. If multiple programs, list them and ask which to restart (or `supervisorctl restart all` if user confirms).
- **`deploy/*.service`**: derive unit name from filename. Check file ownership vs current uid to decide if `sudo` is needed.
- **`Makefile`** with `deploy` / `restart` / `up` targets: these typically encode the project's true restart procedure (env vars, pre-hooks). Prefer them over raw `docker compose` / `systemctl`.
- **Compose-only project** (no other build orchestration found): the build step is **subsumed** by `docker compose up -d --build` — do not run a separate build, mark the build step as "skipped — subsumed by deploy".

**Priority of evidence** (highest first):
1. `Makefile` `deploy`/`restart`/`up` target (project-specific wrapper)
2. Compose / pm2 / supervisord / systemd config file (the deployment medium itself)
3. README "Deploy" / "Run" section code block

### Step 4: Present inferences for confirmation

Show the user a structured inference report **before** executing anything:

```
Detected build:
  Source: Makefile target `build` (line 12, calls `go build -ldflags ...`)
  Cross-ref: README "Building" section confirms `make build`
  Command: make build

Detected deploy:
  Source: docker-compose.yml (services: api, worker, db)
  Cross-ref: Makefile `up` target wraps it with --env-file
  Command: make up   ← Makefile wrapper preferred over raw compose
```

Proceed only after the user confirms. Skip confirmation only when both commands come from `.cortex.yaml`.

---

## Behavior

### Workflow (checklist)

1. **Resolve target directory**
   - Default: CWD
   - If user provided a path: verify it exists (`test -d <path>`)
   - Abort with clear error if the directory does not exist

2. **Read config override** (if `.cortex.yaml` present)
   - Parse `build_command` and/or `deploy_command`
   - Log which fields were overridden; skip heuristics for overridden fields

3. **Check inference cache** (Detection Approach Step 0.5)
   - Read `.cortex/redeploy-local.yaml` if present
   - Validate per the 6-step pseudo-logic in Step 0.5
   - On cache hit: skip steps 4–5 and proceed to step 6 with the report annotated `(from cache, scanned YYYY-MM-DD; <N> signal files unchanged)`
   - On cache miss / malformed / stale: continue to step 4 (do not delete the file)
   - Fields overridden by `.cortex.yaml` (step 2) are dropped from cache reuse; the cache may still supply the remaining field

4. **Infer build command** (if not overridden and not cached)
   - Run Detection Approach Steps 1–2: inventory signals, read files, cross-reference
   - Log the source(s) of evidence and the chosen command
   - If Compose-only project (no other build orchestration found): mark "build skipped — subsumed by deploy"
   - If no evidence found: stop and ask user for `build_command`
   - If evidence conflicts: surface options to user, do not silently pick

5. **Infer deploy command** (if not overridden and not cached)
   - Run Detection Approach Step 3: read deploy config files, prefer Makefile wrappers
   - Log the source and the chosen command (including extracted service/unit name)
   - If no evidence found: stop and ask user

6. **Present inferences & confirm**
   - Show the structured inference report (per Detection Approach Step 4); add cache-hit annotation if reused
   - Wait for user confirmation
   - Skip confirmation only when both commands come from `.cortex.yaml`
   - If the same directory+commands were already confirmed earlier in this conversation, skip re-confirmation

7. **Execute build** (if not skipped)
   - Run build command from the target directory
   - Stream output (do not buffer silently)
   - Record wall-clock duration with `{ start=$(date +%s); <cmd>; echo $(($(date +%s)-start))s; }`
   - On exit code ≠ 0: show last 20 lines, report failure, stop — do not run deploy

8. **Execute deployment restart**
   - Run restart command
   - Record duration the same way
   - On exit code ≠ 0: show last 20 lines, report partial state, stop

9. **Health check**
   - Docker Compose: `docker compose ps` — confirm all containers show `Up`
   - systemd: `systemctl is-active <unit>`
   - pm2: `pm2 list | grep <name>`
   - supervisord: `supervisorctl status <program>`
   - Log result; warn (but do not fail the skill run) if health check command is unavailable

10. **Emit run report**

    ```
    Step     Command                         Exit  Duration
    ───────  ──────────────────────────────  ────  ────────
    Build    pnpm run build                    0   18.2s
    Deploy   docker compose up -d --build      0    6.3s
    Health   docker compose ps                 0    0.2s
    ```

11. **Write cache on success**
    - Only when build exit 0 (or skipped-by-subsumption), deploy exit 0, AND health check passed
    - Skip the write if both commands came from `.cortex.yaml` (cache adds no value)
    - Skip on partial success (deploy 0 but health unhealthy) — do not cache a known-broken configuration
    - Create `.cortex/` (mode 0755) if missing, then write `.cortex/redeploy-local.yaml` with the `# Auto-generated by redeploy-local skill; do not edit by hand` header
    - Record current `skill_version`, resolved absolute `project_path`, ISO 8601 UTC `written_at`, the chosen commands with their evidence, and every signal file READ during inference plus its current mtime
    - On write failure (permission denied, disk full, concurrent write): log `cache write skipped: <reason>` and continue — the deploy already succeeded; the cache is only an optimization layer

### Interaction policy

- Ask only when detection is ambiguous or fails
- Never ask when `.cortex.yaml` provides both commands
- One confirmation prompt covers both build and deploy; never prompt twice for the same run
- Skip re-confirmation if the same directory and commands were already confirmed earlier in this conversation

---

## Input & Output

### Input requirements

- Target directory (explicit path or CWD)
- Optional: `.cortex.yaml` with `build_command` and/or `deploy_command`

### Output contract

Provides:

- Inference report listing every chosen command with its evidence source(s) (file + section/line + cross-references)
- Streamed build output (or "skipped" note for Compose-only projects)
- Streamed deploy output
- Health check result
- Run report table (command / exit code / duration per step)
- Inference cache written to `.cortex/redeploy-local.yaml` on fully successful run (build + deploy + health all pass)

---

## Limits

### Hard boundaries

- NEVER run `rm -rf` or destructive cleanup commands as part of build without explicit user config
- NEVER assume a service name for systemd, pm2, or supervisord — extract from config file or ask
- NEVER proceed past a failed step — report and stop
- NEVER run deployment restart without a preceding successful build (exit 0), except for Compose-only projects where deploy subsumes build
- NEVER inject or modify environment variables in the target deployment
- NEVER prepend `sudo` unless evidence justifies it (e.g., systemd unit file owned by root vs. current uid); ask the user to confirm elevation before running

### Failure modes

| Failure | Behavior |
|---|---|
| Directory not found | Abort immediately; show exact path checked |
| No build evidence found | Stop before build; ask user for `build_command` or to populate `.cortex.yaml` |
| No deploy evidence found | Stop before deploy; ask user for `deploy_command` or to populate `.cortex.yaml` |
| Evidence conflicts (e.g., Makefile vs CI disagree) | Stop; surface both options with sources; let user choose |
| Name/unit extraction fails | Stop; ask user to provide the name explicitly |
| Build exit ≠ 0 | Show last 20 lines; stop; do not run deploy |
| Deploy exit ≠ 0 | Show last 20 lines; stop; report partial state |
| Health check fails | Warn; do not fail the skill run; do not write cache |
| Cache file malformed or missing required keys | Treat as cache miss; fall through to full scan; do not delete; successful run overwrites |
| Recorded signal file deleted / mtime changed | Cache miss; re-scan |
| Cache `skill_version` differs from current | Cache miss; re-scan |
| Cache write fails (permission / disk full) | Log warning; do not fail the skill run — deploy already succeeded |

---

## Self-Check

### Core success criteria

- [ ] **Directory resolved**: Target directory verified to exist before any command runs
- [ ] **Detection traceable**: Every inferred command is attributed to specific evidence (file + line/section, ideally with a cross-reference) — never invented
- [ ] **Double-build avoided**: Compose-only projects skip the build step; `--build` in deploy command handles it
- [ ] **User confirmed**: Commands shown and confirmed before first execution (skipped only when both come from `.cortex.yaml`)
- [ ] **Build succeeded**: Exit code 0 confirmed before deploy runs (or build step legitimately skipped)
- [ ] **Deploy succeeded**: Exit code 0 confirmed before health check
- [ ] **Health check run**: Status checked and logged (warn if unavailable; do not fail)
- [ ] **Run report emitted**: Table covers every step with command / exit code / duration
- [ ] **Cache honored or refreshed**: `.cortex/redeploy-local.yaml` read before scanning; written only after a fully successful run (build + deploy + health all pass)

### Process quality checks

- [ ] **No silent buffering**: Build and deploy output streamed, not buffered
- [ ] **Duration recorded**: Wall-clock time measured for each step
- [ ] **Name/unit sourced**: pm2/supervisord/systemd name extracted from config file, not hardcoded
- [ ] **Interaction minimal**: No redundant prompts; re-confirmation skipped when already confirmed in this conversation

---

## Examples

### Example 1: Node.js app behind Docker Compose

**Directory contents**: `package.json`, `pnpm-lock.yaml`, `Dockerfile`, `docker-compose.yml`, `README.md`

**Inference process**:
- Read `package.json` `scripts`: found `build`, `build:prod`, `test`, `lint`
- Read `Dockerfile`: `COPY dist/ /app/` — image expects `dist/` to exist
- Read `package.json` `scripts.build`: `tsc && vite build --outDir dist` — produces `dist/`, matches
- `scripts.build:prod` is `NODE_ENV=production npm run build` — would also work, but `build` is the default referenced in README
- Detect package manager: `pnpm-lock.yaml` → pnpm

**Inference report shown to user**:

```
Detected build:
  Source: package.json scripts.build (tsc && vite build --outDir dist)
  Cross-ref: Dockerfile copies dist/, matches output path
  Command: pnpm run build

Detected deploy:
  Source: docker-compose.yml (3 services: api, worker, db)
  Command: docker compose up -d --build
```

**After user confirms**, run report:

```
Step     Command                         Exit  Duration
───────  ──────────────────────────────  ────  ────────
Build    pnpm run build                    0   18.2s
Deploy   docker compose up -d --build      0    6.3s
Health   docker compose ps                 0    0.2s
```

### Example 2: Go service with Makefile wrapper

**Directory contents**: `go.mod`, `Makefile`, `deploy/myapp.service`, `.github/workflows/ci.yml`

**Inference process**:
- Read `Makefile` targets: `build`, `test`, `lint`, `release`, `install`
- Read `Makefile` body of `build` target: `go build -ldflags "-X main.Version=$(VERSION)" -o bin/myapp ./cmd/myapp` — project-specific ldflags and output path; do NOT default to `go build ./...`
- Cross-ref `.github/workflows/ci.yml`: build step runs `make build` — confirms canonical
- Read `deploy/myapp.service` filename → unit `myapp`; check file owner (`root`) vs current uid → `sudo systemctl restart myapp` likely needed

**Inference report**:

```
Detected build:
  Source: Makefile target `build` (line 8)
  Cross-ref: .github/workflows/ci.yml uses `make build`
  Command: make build

Detected deploy:
  Source: deploy/myapp.service (unit name from filename)
  Note: unit file owned by root → sudo required
  Command: sudo systemctl restart myapp
```

### Example 3: Compose-only project (build step skipped)

**Directory contents**: `docker-compose.yml`, `Dockerfile` (no Makefile, no package.json, no language manifest at root)

**Inference process**:
- No build orchestration found outside the Docker context
- `Dockerfile` does the build during `docker compose up --build`
- Therefore: skip standalone build; deploy command subsumes it

**Run report**:

```
Step     Command                         Exit  Duration
───────  ──────────────────────────────  ────  ────────
Build    (skipped — subsumed by deploy)   —      —
Deploy   docker compose up -d --build      0    9.1s
Health   docker compose ps                 0    0.2s
```

### Example 4: Config override via .cortex.yaml

**`.cortex.yaml`**:

```yaml
build_command: make release GOARCH=arm64
deploy_command: supervisorctl restart api-worker
```

**Detection**: Both commands read from `.cortex.yaml` — no heuristics applied, no confirmation prompt.

**Run report**:

```
Step     Command                          Exit  Duration
───────  ───────────────────────────────  ────  ────────
Build    make release GOARCH=arm64          0   22.7s
Deploy   supervisorctl restart api-worker   0    0.8s
Health   supervisorctl status api-worker    0    0.1s
```

### Example 5: Build failure (edge case)

**Scenario**: `pnpm run build` exits with code 1

```
[build] FAILED — exit 1 after 4.2s

Last 20 lines of output:
  ...
  Error: cannot find module 'express'

Deployment step skipped.
Suggested fix: run `pnpm install` to restore dependencies, then retry.
```

### Example 6: Cache hit on a previously-deployed project

**Directory contents**: same as Example 1 (`package.json`, `pnpm-lock.yaml`, `Dockerfile`, `docker-compose.yml`, `README.md`) plus `.cortex/redeploy-local.yaml` written by a prior successful run.

**Detection process**:
- Step 0: no `.cortex.yaml` override
- Step 0.5: read `.cortex/redeploy-local.yaml`; validation passes (same skill version, same `project_path`, 2 days old, all 4 `signal_files` mtimes unchanged)
- Skip Steps 1–3 (full scan); jump to Step 4 with cache annotation

**Inference report shown to user**:

```
Detected build:
  Source: .cortex/redeploy-local.yaml (cached 2026-05-20; 4 signal files unchanged)
  Command: pnpm run build

Detected deploy:
  Source: .cortex/redeploy-local.yaml (cached 2026-05-20; 4 signal files unchanged)
  Command: docker compose up -d --build
```

**After user confirms**, run report (identical commands to Example 1, no scan overhead):

```
Step     Command                         Exit  Duration
───────  ──────────────────────────────  ────  ────────
Build    pnpm run build                    0   17.8s
Deploy   docker compose up -d --build      0    6.1s
Health   docker compose ps                 0    0.2s
```

The cache file is rewritten on success with a refreshed `written_at` and current signal-file mtimes.
