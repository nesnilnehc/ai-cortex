---
name: generate-github-workflow
description: "GitHub Actions YAML with embedded output contract: security-first, minimal permissions, version pinning. For CI, release, PR checks. Differs from generic templates by spec compliance and auditability."
description_zh: 生成嵌有输出契约的 GitHub Actions YAML：安全优先、最小权限、版本锁定；适用于 CI、发布与 PR 检查。
tags: [devops]
version: 1.1.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [github workflow, generate workflow]
input_schema:
  type: free-form
  description: Workflow requirements (CI, release, PR checks) and project context
output_schema:
  type: document-artifact
  description: GitHub Actions YAML workflow file(s) written to .github/workflows/
---

# Skill: Generate GitHub Workflow

## Purpose

Generate **GitHub Actions workflow files** for software projects of every kind, satisfying this skill's **Appendix A: Workflow Output Contract**. Standardized structure, triggers, and security lower the cost of setting up CI/CD and raise maintainability and auditability, while avoiding the common security and permission problems. This skill produces workflow YAML only; it does not chain to the documentation or rule skills. If the user later needs a README or AGENTS.md update, invoke those skills separately.

---

## Core Objective

**Primary goal**: generate a complete, compliant, immediately runnable GitHub Actions workflow YAML file for the user's scenario, stack, and security posture — deployable as soon as the placeholders are replaced.

**Success criteria** (all requirements must be met):

1. ✅ **Appendix A satisfied**: the output meets every mandatory structural and security requirement in Appendix A (name, on, jobs, runs-on, steps, pinned actions, no hard-coded secrets)
2. ✅ **Narrow triggers**: the `on` block is scoped to specific branches/paths/tags - no bare `on: push` without a filter
3. ✅ **Least privilege**: `permissions` is set at workflow or job level to the least the scenario type needs (CI: `contents: read`; release: `contents: write`, `packages: write`)
4. ✅ **Stack aligned**: runner, language version, package manager, and commands match the stack the user named
5. ✅ **User confirmation before writing**: the required notes and placeholders are listed, and the user's confirmation is obtained before writing to `.github/workflows/`

**Acceptance** test: once the user replaces the placeholders, can the workflow run in the target repository with no further modification beyond secret names and environment-specific values?

---

## Scope Boundaries

**This skill owns**:

- Generating complete GitHub Actions workflow YAML for CI, PR check, release, and scheduled scenarios
- Security hardening (pinned actions, least privilege, no hard-coded secrets)
- Stack alignment (Node/Python/Go/Rust runners, package managers, build commands)
- Multi-workflow generation (CI + Release split into separate files)
- Conflict detection against existing workflows
- The Go + Docker + GHCR + GoReleaser pattern (see Appendix B)

**This skill does not own**:

- Chaining into the documentation skills (README, AGENTS.md updates) — invoke those separately once the workflow is generated
- Writing to `.github/workflows/` without user confirmation
- Overwriting an existing workflow without warning
- Implementing build/release logic already defined in `.goreleaser.yaml` or a Dockerfile
- Generating non-GitHub CI/CD (GitLab CI, Jenkins, and the like)

**Handoff point**: once the workflow YAML is generated and confirmed, write the file to `.github/workflows/` with the user's approval. For documentation updates a new workflow triggers, use the documentation skills separately.

---

## Use Cases

- **New project setup**: add a CI (build, test, lint) or PR check workflow to a new repository.
- **Unified standards**: harmonize workflow style and naming across repositories, for operations and audit.
- **Filling gaps**: add the missing CI/release/scheduled workflow to a legacy project, with least privilege and pinned versions.
- **Scenario-driven**: generate YAML for a given scenario (e.g. "run tests on PRs only", "build and release on tags").

**When to use**: when the user or the project needs to "create or add a GitHub workflow for the current or a named project".

**Scope**: this skill's output follows the **embedded Appendix A** (narrow triggers, least privilege, pinned versions, auditable). Generic GitHub Actions templates cover more ground; this skill stresses security and maintainability.

---

## Behavior

### Principles

- **Appendix A is authoritative**: the YAML produced must satisfy Appendix A (structure, naming, security, maintainability).
- **Narrow triggers**: `on` must name branches/paths/tags; avoid firing on every push. Common pattern: `push`/`pull_request` with `branches` or `paths`. A **release** workflow must fire on version tags only (e.g. `push: tags: ['v*']`) and live in a different file from CI.
- **Least privilege**: when a workflow needs repo write, PR, or secrets access, set `permissions` at workflow or job level to the least required; e.g. CI `contents: read`, release `contents: write`, `packages: write`; avoid `all`.
- **Pinned versions**: pin third-party actions (a commit SHA or a major version tag); do not use `@master` or an unpinned reference; for security and scanning actions, prefer pinning to a concrete version (Trivy, for one).

### Tone and style

- Use objective technical language; keep workflow and step `name` values short and readable for the Actions log.
- Match the project stack: pick the runner, package manager, and build commands by project type (Node/Python/Go/Rust) and existing convention; where the project already has workflows, align naming and style with them.

### Input-driven

- Where `CLAUDE.md` or `.ai-cortex/config.yaml` exists, prefer reading `test_command`, `base_branch`, and the rest from it; otherwise infer them from user input or from the project. See [docs/guides/project-config.md](../../docs/guides/project-config.md).
- Use the user's **scenario** (e.g. "CI: run tests on PRs", "release: build and upload on tags") and **stack** (language, package manager, test/build commands) to generate the workflow; where information is missing, use sensible placeholders and mark them for replacement; do not invent commands or paths.

### Interaction policy

- **Confirm before writing**: once the YAML is generated, list the **required notes** (placeholders, branch names, secret names the user must set), then ask for confirmation; do not write to `.github/workflows/` or commit without the user's confirmation.
- **Multiple files / release**: when generating several workflows (CI + Release, say) or using write permissions (`contents: write`, `packages: write`), list the files to be created or overwritten and the permission scope, then confirm before writing.
- **Conflicts**: where the target path already holds a workflow with the same or an overlapping purpose, warn and ask whether to overwrite or save elsewhere; do not overwrite silently.

---

## Input & Output

### Input

- **Scenario**: the purpose (CI, PR check, release, schedule, matrix).
- **Stack**: language and version (e.g. Node 20, Python 3.11, Go 1.21), package manager (npm/pnpm/yarn, pip, cargo), test/build/release commands.
- **Triggers**: branches (e.g. `main`, `develop`), path filters, an optional `workflow_dispatch`.
- **Target path**: where the file is written, defaulting to `.github/workflows/` under the project root; for several workflows, name each file (e.g. `ci.yml`, `release.yml`).

### Output

- **Workflow YAML**: complete file content conforming to Appendix A, ready to be written to `.github/workflows/<name>.yml`.
- **Notes**: list the placeholders (e.g. `npm run test`, the branch `main`), the secret names, and anything else the user must configure.

---

## Restrictions

### Hard Boundaries

- **Do not violate Appendix A**: the output must have `name`, `on`, and `jobs`, and every job must have `runs-on` and `steps`; do not use unpinned third-party actions or hard-coded secrets.
- **Do not over-trigger**: unless the user asks for it explicitly, do not use a bare `on:push` with no branch/path filter.
- **Do not invent commands**: use a placeholder for an unknown test/build/release command and mark it "replace with the real command"; do not invent scripts or paths.
- **Do not ignore existing workflows**: where the project already has `.github/workflows/`, align naming and style, and avoid duplication or conflict.
- **Do not duplicate build logic**: where the project builds and shapes images with GoReleaser, a Dockerfile, and the like, the workflow only fires, logs in, and passes parameters (e.g. `GITHUB_TOKEN`, `BUILDX_BUILDER`); do not reimplement that logic.

### Skill Boundaries

**Do not do these** (other skills handle them):

- Do not chain into the documentation or README skills - invoke them separately
- Do not write to `.github/workflows/` without user confirmation
- Do not silently overwrite an existing workflow
- Do not reimplement build/release logic already defined in `.goreleaser.yaml` or Dockerfiles
- Do not generate CI/CD for non-GitHub platforms (GitLab CI, Jenkins, and the like)

**When to stop and hand off**:

- Once the workflow file is written and confirmed, hand off to the documentation skills if a README/AGENTS.md update is needed
- When the user needs registry or secret configuration, give guidance but do not automate the external service setup

---

## Self-Check

### Core success criteria

- [ ] **Appendix A satisfied**: the output meets every mandatory structural and security requirement in Appendix A (name, on, jobs, runs-on, steps, pinned actions, no hard-coded secrets)
- [ ] **Narrow triggers**: the `on` block is scoped to specific branches/paths/tags - no bare `on: push` without a filter
- [ ] **Least privilege**: `permissions` is set at workflow or job level to the least the scenario type needs
- [ ] **Stack aligned**: runner, language version, package manager, and commands match the stack the user named
- [ ] **User confirmation before writing**: the required notes and placeholders are listed, and the user's confirmation is obtained before writing to `.github/workflows/`

### Process quality checks

- [ ] **Appendix A**: does the output meet the mandatory structure and security of Appendix A?
- [ ] **Triggers**: is `on` narrowed to specific branches/paths/tags?
- [ ] **Permissions and security**: is a minimal `permissions` set? Are third-party actions pinned? Are there no hard-coded secrets?
- [ ] **Runnable**: once the user replaces the placeholders, can the workflow run in the target repository?
- [ ] **Stack aligned**: do the runner, language version, package manager, and commands match the user's stack?
- [ ] **Step order and dependencies**: for a multi-step job (e.g. QEMU → Buildx → login → GoReleaser), is the order right, and are the ids/env variables passed through? See **Appendix B** for Go + Docker + GoReleaser.

### Acceptance test

Once the user replaces the placeholders, can the workflow run in the target repository with no further modification beyond secret names and environment-specific values?

---

## Examples

### Example 1: Node CI (test + lint on PRs)

**Input**: scenario: CI. Stack: Node 20, pnpm, test `pnpm test`, lint `pnpm lint`. Trigger: `pull_request` onto `main`. File: `ci.yml`.

**Expected**: a single `ci.yml` with a `name` such as `CI`; `on: pull_request: branches: [main]`; a job on `ubuntu-latest` covering checkout, Node/pnpm setup, install, lint, and test; using pinned official `actions/checkout` and `pnpm/action-setup` (or equivalents); no hard-coded secrets; read-only if `permissions` is set.

### Example 2: PR check with path filters

**Input**: scenario: PR check. Stack: Go 1.21, test `go test ./...`. Fires only when `go.mod` or `*.go` changes. File: `pr-check.yml`.

**Expected**: `on.pull_request` plus `paths: ['**.go', 'go.mod']`; a job with a pinned `actions/setup-go`, with steps for checkout, Go setup, and test; omit `permissions`, or use `contents: read`, when no write access is needed.

### Example 3: Go release (Docker + GHCR + GoReleaser)

**Input**: scenario: CD/release. Stack: Go, multi-architecture Docker (amd64/arm64), GoReleaser for the image and the GitHub Release. Trigger: `push` on `v*` tags only. File: `release.yml`.

**Expected**: `on: push: tags: ['v*']`; `permissions` including `contents: write` and `packages: write`. Steps: checkout (`fetch-depth: 0`) → set up Go (`go-version-file: go.mod`, cached) → set up QEMU (`linux/amd64`, `linux/arm64`) → set up Docker Buildx (`id: buildx`, same platforms) → log in to GHCR (`docker/login-action`, `ghcr.io`) → GoReleaser (`goreleaser/goreleaser-action` pinned, pass `GITHUB_TOKEN` and `BUILDX_BUILDER: ${{ steps.buildx.outputs.name }}`). Do not reimplement the logic defined in `.goreleaser.yaml`/Dockerfile. **See Appendix B**.

### Example 4 (edge): minimal information

**Input**: project: legacy-api. No description. Language and commands unknown. The user wants "at least a placeholder CI workflow".

**Expected**: generate structurally complete YAML that conforms to Appendix A; use placeholders for the runner and the steps (e.g. "name the runner and the install/test commands") and mark them "to be replaced"; keep `on` narrow (e.g. `pull_request: branches: [main]`); do not invent test or build commands; keep `name`, `on`, `jobs`, `runs-on`, `steps` and the recommended fields (e.g. `permissions`) for the user to fill in later.

---

## Appendix A: Workflow output contract

The following are **mandatory** for workflow files produced by this skill; use this appendix for self-check.

**Scope**: YAML workflow files produced by this skill for a project's `.github/workflows/`.

### A.1 File and path

- **Location**: Must live under the target project's `.github/workflows/`.
- **Naming**: `kebab-case`, extension `.yml` or `.yaml`; name should reflect purpose (e.g. `ci.yml`, `pr-check.yml`, `release.yml`).
- **One file, one workflow**: One file defines one workflow; split into multiple files for complex cases; avoid many unrelated jobs in one file.

### A.2 Required structure

Each workflow YAML must contain (order recommended):

| Field               | Required | Description                                                                                                                      |
| :------------------ | :------- | :------------------------------------------------------------------------------------------------------------------------------- |
| `name`              | Yes      | Display name in GitHub UI; short and readable (e.g. "CI", "PR check", "Release").                                                |
| `on`                | Yes      | Triggers: `push`, `pull_request`, `workflow_dispatch`, etc.; must narrow branch/path/tag; avoid broad `on: push` with no filter. |
| `jobs`              | Yes      | At least one job; each job must have `runs-on` and `steps`.                                                                      |
| `jobs.<id>.runs-on` | Yes      | Runner (e.g. `ubuntu-latest`).                                                                                                   |
| `jobs.<id>.steps`   | Yes      | List of steps; each step has `name` (human-readable) and `uses` or `run`.                                                        |

Optional but recommended: `permissions`, `concurrency`, `env`.

### A.3 Naming and readability

- **Job id**: `kebab-case`, clear meaning (e.g. `build`, `test`, `lint`, `deploy-preview`).
- **Step name**: Short, scannable description for the Actions log.
- **Workflow name**: Align with filename and other workflows in the repo.

### A.4 Security and minimal permissions

- **Permissions**: If `permissions` is not set, GitHub uses default `GITHUB_TOKEN` permissions. For sensitive operations, set `permissions` at workflow or job level to the minimum needed. **By type**: CI (build/test/scan only) → `contents: read`; release (Release, GHCR push) → explicit `contents: write`, `packages: write`; avoid default or `all`.
- **Secrets**: Inject secrets via Secrets; never hardcode keys, tokens, or passwords in YAML.
- **Third-party actions**: Prefer official or widely used actions; pin version (commit SHA or major-version tag); do not use `@master` or unpinned; use specific versions for security/scan actions to reduce drift.

### A.5 Maintainability

- **CI vs CD (recommended)**: CI only builds, tests, and scans; **no release**. CD (image push, GitHub Release) runs only on version tags (e.g. `v*`). Use separate files (e.g. `ci.yml`, `release.yml`); do not mix "run on every push" and "release only on tag" in one workflow.
- **Reuse**: Extract common logic into Composite Actions or reusable workflows.
- **Comments**: Briefly comment non-obvious triggers, matrix strategy, or env usage; keep comments short.
- **Project alignment**: Runner, language version, package manager, and commands must match the target project; if the project has existing workflows, align style and naming.

### A.6 Self-check (producer)

After producing the workflow:

- [ ] File is under `.github/workflows/` with a kebab-case name.
- [ ] Contains `name`, `on`, `jobs`; each job has `runs-on` and `steps`.
- [ ] `on` is narrowed to specific branches/paths/tags.
- [ ] No hardcoded secrets; third-party actions pinned (specific version for security/scan).
- [ ] Step and job names are clear; consistent with project stack and existing workflow style.
- [ ] YAML is valid (indent, no duplicate keys); step order and dependencies are correct.

---

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

| Issue                                | Approach                                                                                                                          |
| :----------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------- |
| Single workflow too large            | Split into **CI + Release**: CI for build/test/scan, Release only on tag via GoReleaser; clearer permissions and logic.           |
| GHCR auth too complex                | Use minimal login (`docker/login-action` + token); avoid heavy auth-verify that can false-fail.                                   |
| Multi-arch manifest validation fails | Pull and validate **per platform** instead of generic manifest pull.                                                              |
| Date/version format inconsistent     | Use one format (e.g. ISO8601) in workflow and Dockerfile; add `dist/` to `.gitignore` if using GoReleaser output.                 |
| GoReleaser multi-arch build fails    | GoReleaser needs Buildx builder: set **id: buildx** on Buildx step and pass **BUILDX_BUILDER: ${{ steps.buildx.outputs.name }}**. |
| Version drift                        | Use reasonable version constraints and check release notes when upgrading; validate on a branch first.                            |

**Inspect workflow history**: `git log --oneline -- .github/workflows/`

---

## References

- [GitHub Actions docs](https://docs.github.com/en/actions)
- [Workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Security hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
