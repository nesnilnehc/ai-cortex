---
name: generate-github-workflow
description: "GitHub Actions YAML with embedded output contract: security-first, minimal permissions, version pinning. For CI, release, PR checks. Differs from generic templates by spec compliance and auditability."
description_zh: 生成嵌有输出契约的 GitHub Actions YAML：安全优先、最小权限、版本锁定；适用于 CI、发布与 PR 检查。
tags: [devops]
version: 1.0.1
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

Generate **GitHub Actions workflow files** for software projects of every kind, satisfying this skill's **Appendix A: Workflow Output Contract**. Standardized structure, triggers, and security lower the cost of setting up CI/CD and raise maintainability and auditability, while avoiding the common security and permission problems. This skill produces workflow YAML only; it has nothing to do with the documentation or rules skills. If the user later needs a README or AGENTS.md update, invoke those skills separately.

---

## Core Objective

**Primary goal**: generate a complete, compliant, immediately runnable GitHub Actions workflow YAML file for the user's scenario, stack, and security posture — deployable as soon as the placeholders are replaced.

**Success criteria** (all requirements must be met):

1. ✅ **Appendix A satisfied**: the output meets every mandatory structural and security requirement in Appendix A (name, jobs, runs-on, steps, pinned actions, no hard-coded secrets)
2. ✅ **Narrow triggers**: the `on` block is scoped to specific branches/paths/tags - no bare `on: Push` without a filter
3. ✅ **Least privilege**: `permissions` is set at workflow or job level to the least the scenario type needs (CI: `contents: read`; release: `contents: write`, `packages: write`)
4. ✅ **Stack aligned**: runner, language version, package manager, and commands match the stack the user named
5. ✅ **User confirmation before writing**: the required notes and placeholders are listed, and the user's confirmation is obtained before writing to `.github/Workflows/`

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
- **Narrow triggers**: `on` must name branches/paths/tags; avoid firing on every push. Common pattern: `push`/`pull_request` with `branches` or `paths`. A **release** workflow must fire on version tags only (e.g. `push:tags:['v*']`) and live in a different file from CI.
- **Least privilege**: when a workflow needs repo write, PR, or secrets access, set `permissions` at workflow or job level to the least required; e.g. CI `contents: read`, release `contents: write`, `packages: write`; avoid `all`.
- **Pinned versions**: pin third-party actions (a commit SHA or a major version tag); do not use `@master` or an unpinned reference; for security and scanning actions, prefer pinning to a concrete version (Trivy, for one).

### Tone and style

- Use objective technical language; keep workflow and step `name` values short and easy to read in an operations log.
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
- **Target path**: where the file is written, defaulting to `.github/Workflows/` under the project root; for several workflows, name each file (e.g. `ci.yml`, `release.yml`).

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

- [ ] **Appendix A satisfied**: the output meets every mandatory structural and security requirement in Appendix A (name, jobs, runs-on, steps, pinned actions, no hard-coded secrets)
- [ ] **Narrow triggers**: the `on` block is scoped to specific branches/paths/tags - no bare `on：push` without a filter
- [ ] **Least privilege**: `permissions` is set at workflow or job level to the least the scenario type needs
- [ ] **Stack aligned**: runner, language version, package manager, and commands match the stack the user named
- [ ] **User confirmation before writing**: the required notes and placeholders are listed, and the user's confirmation is obtained before writing to `.github/Workflows/`

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

**Expected**: `on:push:tags:['v*']`; `permissions` including `contents: write` and `packages: write`. Steps: checkout (`fetch-depth: 0`) → set up Go (`go-version-file：go.mod`, cached) → set up QEMU (`linux/amd64`, `linux/arm64`) → set up Docker Buildx (`id：buildx`, same platforms) → log in to GHCR (`docker/login-action`, `ghcr.io`) → GoReleaser (`goreleaser/goreleaser-action` pinned, pass `GITHUB_TOKEN` and `BUILDX_BUILDER: ${{ steps.buildx.outputs.name }}`). Do not reimplement the logic defined in `.goreleaser.yaml`/Dockerfile. **See Appendix B**.

### Example 4 (edge): minimal information

**Input**: project: legacy-api. No description. Language and commands unknown. The user wants "at least a placeholder CI workflow".

**Expected**: generate structurally complete YAML that conforms to Appendix A; use placeholders for the runner and the steps (e.g. "name the runner and the install/test commands") and mark them "to be replaced"; keep `on` narrow (e.g. `pull_request:branches:[main]`); do not invent test or build commands; keep `name`, `on`, `jobs`, `runs-on`, `steps` and the recommended fields (e.g. `permissions`) for the user to fill in later.

---
