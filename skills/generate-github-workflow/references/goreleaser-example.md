# generate-github-workflow: goreleaser example

## Appendix B: Go + Docker + GHCR + GoReleaser

Conventions and practices for **Go + Docker + GHCR + GoReleaser** workflows; follow together with the main skill and Appendix A when generating or editing such workflows.

### B.1 Layout

- **CI and CD separate**: Two workflows.
  - **CI** (e.g. `ci.yml`): `push`/`pull_request` to main branch. Build, test, security scan only; **no release**.
  - **CD** (e.g. `release.yml`): Only on `push` of version tags (e.g. `v*`). Publish image and GitHub Release.
- Do not mix "run on every push" and "release only on tag" in one workflow.

### B.2 Permissions

- Set `permissions` explicitly. CI: `contents: read`. Release: `contents: write`, `packages: write`. Do not use `all`.

### B.3 Steps and order

#### Go

- Use `actions/setup-go@v5` with `go-version-file: go.mod`. Enable `cache: true`. For release, checkout with `fetch-depth: 0` (needed for GoReleaser); CI can use the same for consistency.

#### CI (Example Order)

1. Checkout (`fetch-depth: 0`)
2. Set up Go (go.mod + cache)
3. `go test ./...`
4. govulncheck: `go install golang.org/x/vuln/cmd/govulncheck@latest` then `govulncheck ./...`
5. Docker Buildx (setup only, single platform)
6. Build image for scanning: single arch `linux/amd64`, `push: false`, `load: true`, tag e.g. `local/your-app:ci-${{ github.sha }}`
7. Trivy on that image: `severity: HIGH,CRITICAL`, `ignore-unfixed: true`, `exit-code: 1` so CI fails on findings

Multi-arch in Release only; CI scans single arch for speed.

#### Release (Example Order)

1. Checkout (`fetch-depth: 0`)
2. Set up Go (go.mod + cache)
3. Set up QEMU: `docker/setup-qemu-action`, `platforms: linux/amd64,linux/arm64`
4. Set up Docker Buildx: `id: buildx`, `driver: docker-container`, `platforms: linux/amd64,linux/arm64`
5. Login to GHCR: `docker/login-action`, registry `ghcr.io`, password `secrets.GHCR_TOKEN || secrets.GITHUB_TOKEN`, `logout: true`
6. GoReleaser: `goreleaser/goreleaser-action@v6`, `args: release --clean`, env `GITHUB_TOKEN` and `BUILDX_BUILDER: ${{ steps.buildx.outputs.name }}`

QEMU before Buildx; Buildx `platforms` must match QEMU. GoReleaser needs the Buildx builder name for multi-arch, so set `id: buildx` and pass `BUILDX_BUILDER`.

### B.4 Relation to repo config

- **Docker image**: Shape is defined in `.goreleaser.yaml` and Dockerfile; workflow does not duplicate build logic.
- **GHCR**: Image path and tagging in GoReleaser config; workflow only logs in and passes `GITHUB_TOKEN` and Buildx builder.
- **Makefile**: Local build/test can stay; CI steps can align with Make targets but need not depend on them.

### B.5 When editing

1. **Full flow**: Changing one job may affect the whole flow; verify checkout → Go → QEMU → Buildx → login → GoReleaser order and deps.
2. **Action versions**: Use current major versions (e.g. `checkout@v4`, `setup-go@v5`, `setup-buildx-action@v3`, `goreleaser-action@v6`); check changelog for breaking changes when upgrading.
3. **Trivy**: Pin version (e.g. `@0.33.1`) to avoid CI breakage from behavior changes.
4. **YAML**: Check indent and no duplicate keys; validate with a tool after edits.

### B.6 Lessons learned

| Issue | Approach |
| :----------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------- |
| Single workflow too large | Split into **CI + Release**: CI for build/test/scan, Release only on tag via GoReleaser; clearer permissions and logic. |
| GHCR auth too complex | Use minimal login (`docker/login-action` + token); avoid heavy auth-verify that can false-fail. |
| Multi-arch manifest validation fails | Pull and validate **per platform** instead of generic manifest pull. |
| Date/version format inconsistent | Use one format (e.g. ISO8601) in workflow and Dockerfile; add `dist/` to `.gitignore` if using GoReleaser output. |
| GoReleaser multi-arch build fails | GoReleaser needs Buildx builder: set **id: buildx** on Buildx step and pass **BUILDX_BUILDER: ${{ steps.buildx.outputs.name }}**. |
| Version drift | Use reasonable version constraints and check release notes when upgrading; validate on a branch first. |

**Inspect workflow history**: `git log --oneline -- .github/workflows/`

---
