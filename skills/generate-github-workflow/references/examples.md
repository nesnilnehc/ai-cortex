# generate-github-workflow: examples

## Examples

### Example 1: Node CI (test + lint on PRs)

**Input**: scenario: CI. Stack: Node 20, pnpm, test `pnpm test`, lint `pnpm lint`. Trigger: `pull_request` onto `main`. File: `ci.yml`.

**Expected**: a single `ci.yml` with a `name` such as `CI`; `on: pull_request: branches: [main]`; a job on `ubuntu-latest` covering checkout, Node/pnpm setup, install, lint, and test; using pinned official `actions/checkout` and `pnpm/action-setup` (or equivalents); no hard-coded secrets; read-only if `permissions` is set.

### Example 2: PR check with path filters

**Input**: scenario: PR check. Stack: Go 1.21, test `go test ./...`. Fires only when `go.mod` or `*.go` changes. File: `pr-check.yml`.

**Expected**: `on.pull_request` plus `paths: ['**.go', 'go.mod']`; a job with a pinned `actions/setup-go`, with steps for checkout, Go setup, and test; omit `permissions`, or use `contents: read`, when no write access is needed.

### Example 3: Go release (Docker + GHCR + GoReleaser)

**Input**: scenario: CD/release. Stack: Go, multi-architecture Docker (amd64/arm64), GoReleaser for the image and the GitHub Release. Trigger: `push` on `v*` tags only. File: `release.yml`.

**Expected**: `on: push: tags: ['v*']`; `permissions` including `contents: write` and `packages: write`. Steps: checkout (`fetch-depth: 0`) → set up Go (`go-version-file: go.mod`, cached) → set up QEMU (`linux/amd64`, `linux/arm64`) → set up Docker Buildx (`id: buildx`, same platforms) → log in to GHCR (`docker/login-action`, `ghcr.io`) → GoReleaser (`goreleaser/goreleaser-action` pinned, pass `GITHUB_TOKEN` and `BUILDX_BUILDER: ${{ steps.buildx.outputs.name }}`). Do not reimplement the logic defined in `.goreleaser.yaml`/Dockerfile. See the [worked configuration](goreleaser-example.md).

### Example 4 (edge): minimal information

**Input**: project: legacy-api. No description. Language and commands unknown. The user wants "at least a placeholder CI workflow".

**Expected**: generate structurally complete YAML that conforms to Appendix A; use placeholders for the runner and the steps (e.g. "name the runner and the install/test commands") and mark them "to be replaced"; keep `on` narrow (e.g. `pull_request: branches: [main]`); do not invent test or build commands; keep `name`, `on`, `jobs`, `runs-on`, `steps` and the recommended fields (e.g. `permissions`) for the user to fill in later.

---
