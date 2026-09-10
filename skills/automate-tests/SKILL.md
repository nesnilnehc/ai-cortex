---
name: automate-tests
description: Discover and execute repository test commands safely with evidence-based command selection and safety guardrails.
description_zh: 安全发现并执行仓库测试命令；基于证据选择命令并设安全护栏。
tags: [automation, devops]
version: 1.0.2
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [run tests, automated tests, auto test, autotest]
compatibility: Requires git (optional), a shell, and the repo's language toolchain(s) (e.g., node, python, go, dotnet, java).
input_schema:
  type: code-scope
  description: Repository path containing test configuration and source code
  defaults:
    scope: repo
output_schema:
  type: diagnostic-report
  description: Test plan summary with commands run, results, and failure diagnostics
---

# Skill: Run Automated Tests

## Purpose

Work out how the target repository expects automated tests to be run (commands, frameworks, prerequisites, and scope), then run the best-matching test suite under a safety-first interaction policy.

---

## Core Objective

**Primary goal**: produce test execution results through evidence-based command selection and safety guardrails.

**Success criteria** (all must hold):

1. ✅ **Test plan discovered**: the evidence source is identified (documentation, CI configuration, or build manifest)
2. ✅ **Command selected**: the appropriate test command is chosen for the mode (fast/ci/full) and the constraints
3. ✅ **User confirmation obtained**: approval received before installing dependencies, using the network, or starting services
4. ✅ **Tests executed**: the command was run with its output and exit code captured
5. ✅ **Results summarized**: a test plan summary with evidence, commands, execution status, and failures (if any)

**Acceptance** test: can a developer reproduce the test execution by following the test plan summary, with no extra context?

---

## Scope Boundaries

**This skill owns**:

- Discovering the test command from repository evidence (documentation, CI, build manifests)
- Selecting the appropriate test command for the mode and the constraints
- Executing tests behind safety guardrails and user confirmation
- Summarizing test results with evidence and failure diagnostics

**This skill does not own**:

- Test quality assessment or coverage analysis (use `review-testing`)
- Fixing failing tests or debugging test failures (use `orchestrate-repair-loop`)
- Writing new tests or test infrastructure (use the development skills)
- Reviewing test code against best practices (use `review-testing`)

**Handoff point**: once the tests finish (pass or fail), hand off to `orchestrate-repair-loop` to fix the failures, or to `review-testing` for a quality assessment.

## Use Cases

- You cloned a repository and want the right test command without guessing.
- The repository has several test layers (unit/integration/e2e) and you need a safe default run plan.
- CI failed and you want to reproduce it locally by running the same commands the workflow uses.

## Behavior

1. **Establish scope and constraints (ask when unclear)**
   - With nothing specified by the user, default to a **fast, local, non-destructive** run:
     - Unit tests only, no external services, no Docker, no network-dependent setup.
   - Where it matters, have the user pick a mode:
     - `fast`: unit tests only, minimal setup.
     - `ci`: mirror the CI workflow commands as closely as possible.
     - `full`: include integration/e2e tests and service dependencies.
   - Ask whether Docker is allowed, whether network access is allowed, and whether dependency installation is allowed.

2. **Discover the test plan (evidence-based)**
   - If `CLAUDE.md` or `.ai-cortex/config.yaml` exists, prefer the `test_command` recorded there; otherwise discover it from the sources below. See [docs/guides/project-config.md](../../docs/guides/project-config.md).
   - Read these sources in order; stop early once a clear, unambiguous test command turns up:
     - `README.md`, `CONTRIBUTING.md`, `TESTING.md`, `docs/testing*`, `Makefile`
     - CI configuration: `.github/workflows/*.yml`, `.gitlab-ci.yml`, `azure-pipelines.yml`, `Jenkinsfile`
     - Build manifests: `package.json`, `pyproject.toml`, `setup.cfg`, `tox.ini`, `go.mod`, `pom.xml`, `build.gradle*`, `*.csproj`, `Cargo.toml`
   - Identify:
     - The primary test entry point (`npm test`, `pnpm test`, `yarn test`, `pytest`, `tox`, `go test`, `dotnet test`, `mvn test`, `gradle test`, `cargo test`, and so on)
     - Test layers and markers (unit, integration, e2e)
     - Environment prerequisites (DB, Redis, Docker Compose, required environment variables, secrets)
     - How CI sets up its dependencies (services, caches, artifacts)
   - Prefer an **explicit statement** in the documentation or CI over heuristic inference.

3. **Choose the execution plan**
   - In `ci` mode: derive the run sequence from the repository's CI workflow steps (closest match).
   - In `fast` mode: pick the most direct unit test command, the one with the fewest prerequisites.
   - With several stacks present (backend + frontend, say), suggest running each stack separately in a fixed order.
   - If the plan needs a dependency install or a service start, ask for confirmation before continuing.

4. **Execute with guardrails**
   - Always print the exact command you are about to run, before running it.
   - Use a working directory rooted at the target repository (default `.`).
   - Capture and summarize failures:
     - The first failing command and its exit code
     - The most relevant error excerpt
     - Next actions (missing toolchain, missing environment variable, service not running, and so on)
   - Avoid destructive operations:
     - Do not run `rm -rf`, `git clean -fdx`, `docker system prune`, or database drop/migration commands without the user's explicit approval.
   - If the repository needs secrets, do not ask the user to paste them into the chat. Use a `.env` file, a secret manager, or the documented local development flow.

## Input & Output

### Input

- Target repository path (default `.`).
- Mode: `fast` (default), `ci`, or `full`.
- Constraints: dependency install allowed (yes/no), network allowed (yes/no), Docker allowed (yes/no).

### Output

- A short "test plan summary" containing:
  - Evidence: which files/paths informed the plan
  - The selected commands (in order)
  - Assumptions and prerequisites
  - What was executed and what was skipped (and why)
- Enough of the command log to debug a failure (do not dump extremely long logs unless asked).

## Restrictions

### Hard Boundaries

- Do not invent a test command when evidence exists (documentation/CI takes precedence).
- Do not install dependencies, run Docker, or start external services without confirmation.
- Do not modify repository files unless the user explicitly asks (exception: generating a report file when the user asks for an artifact).
- Do not leak secrets; do not request sensitive credentials in the chat.

### Skill Boundaries (avoid overlap)

**Do not do these (other skills handle them)**:

- **Test quality assessment**: judging test coverage, test design, or testing best practices → use `review-testing`
- **Fixing test failures**: debugging failing tests, repairing broken test code, or root-causing → use `orchestrate-repair-loop`
- **Writing tests**: creating new test cases, test infrastructure, or a test framework → use the development/implementation skills
- **Code review**: reviewing test code for quality, maintainability, or best practices → use `review-testing`
- **Repository analysis**: full codebase structure analysis or architecture review → use `review-codebase`

**When to stop and hand off**:

- Tests fail and the user asks "why?" or "how do I fix it?" → hand off to `orchestrate-repair-loop` for debugging and repair
- The user asks "are these tests any good?" or "what is our coverage?" → hand off to `review-testing` for a quality assessment
- The user asks "can you write tests for X?" → hand off to the development workflow for test implementation
- Tests pass and the user asks "what should we test next?" → hand the test strategy suggestion to `review-testing`

## Self-Check

### Core success criteria (all must hold)

- [ ] **Test plan discovered**: the evidence source is identified (documentation, CI configuration, or build manifest)
- [ ] **Command selected**: the appropriate test command is chosen for the mode (fast/ci/full) and the constraints
- [ ] **User confirmation obtained**: approval received before installing dependencies, using the network, or starting services
- [ ] **Tests executed**: the command was run with its output and exit code captured
- [ ] **Results summarized**: a test plan summary with evidence, commands, execution status, and failures (if any)

### Process quality checks

- [ ] **Evidence-based selection**: did I identify at least one authoritative source for the test command (a doc file, a CI workflow, or a build manifest)?
- [ ] **Safety guardrails applied**: did I ask for confirmation before installing dependencies, using the network, starting Docker/services, or any state-changing action?
- [ ] **Commands printed**: did I print the exact command before running it?
- [ ] **Failures diagnosed**: when tests failed, did I give the first failing command, the exit code, and a likely root-cause category?
- [ ] **No destructive operations**: did I avoid running destructive commands (`rm -rf`, `git clean`, `docker system prune`, database drops) without explicit approval?
- [ ] **No secret leakage**: did I avoid asking for sensitive credentials in the conversation, using a `.env` file or the documented local development flow instead?

### Acceptance test

**Can a developer reproduce the test execution by following the test plan summary, with no extra context?**

If no: the test plan summary is incomplete. Add the missing evidence, commands, or prerequisites.

If yes: the skill run is complete. Continue to the handoff if one is needed.

## Examples

### Example 1: a JavaScript repo with package.json

User: "run the tests for this repository."

Agent:

1. Check the `package.json` scripts and `.github/workflows/*`.
2. Settle on `fast` mode and propose:
   - `npm test` (or `pnpm test` / `yarn test` if the repository standardizes on one)
3. Ask: "install dependencies (`npm ci`) and allow network access?"
4. Run:
   - `npm ci`
   - `npm test`
5. Summarize the results and point at the failing test output, if any.

### Example 2 (edge case): a monorepo that needs Docker for integration tests

User: "mirror CI locally."

Agent:

1. Parse `.github/workflows/ci.yml` and identify the separate jobs:
   - Backend unit tests
   - Frontend tests
   - Integration tests with `docker compose`
2. Ask for confirmation:
   - Docker allowed
   - Network allowed
   - Which jobs to run (all of them, or only the failing one)
3. Execute in a controlled order:
   - Install deps per job
   - Run unit tests first
   - Start the services for the integration tests
4. If the integration tests fail, summarize:
   - Service health/port conflicts
   - Missing environment variables
   - How the CI configuration differs from the local one
