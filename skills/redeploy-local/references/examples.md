# redeploy-local: worked examples

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

```text
Detected build:
  Source: package.json scripts.build (tsc && vite build --outDir dist)
  Cross-ref: Dockerfile copies dist/, matches output path
  Command: pnpm run build

Detected deploy:
  Source: docker-compose.yml (3 services: api, worker, db)
  Command: docker compose up -d --build
```

**With unambiguous project evidence**, the run report:

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

```text
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

**Detection**: both commands are read from `.cortex.yaml` — no heuristics or extra confirmation prompt needed.

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

```text
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

```text
Detected build:
  Source: .cortex/redeploy-local.yaml (cached 2026-05-20; 4 signal files unchanged)
  Command: pnpm run build

Detected deploy:
  Source: .cortex/redeploy-local.yaml (cached 2026-05-20; 4 signal files unchanged)
  Command: docker compose up -d --build
```

**With the validated cache**, the run report (the same commands as example 1, without the scan overhead):

```text
Step     Command                         Exit  Duration
───────  ──────────────────────────────  ────  ────────
Build    pnpm run build                    0   17.8s
Deploy   docker compose up -d --build      0    6.1s
Health   docker compose ps                 0    0.2s
```

The cache file is rewritten on success with a refreshed `written_at` and the current signal file mtimes.
