---
name: run-automated-tests
description: Discover and execute repository test commands safely with evidence-based command selection and safety guardrails.
tags: [automation, devops, eng-standards]
version: 1.0.0
license: MIT
related_skills: [review-codebase, generate-github-workflow, review-testing, run-repair-loop]
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [run tests, automated tests]
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

Determine how a target repository expects automated tests to be executed (commands, frameworks, prerequisites, and scope), then run the best matching test suite(s) with a safety-first interaction policy.

---

## Core Objective

**Primary Goal**: Produce test execution results with evidence-based command selection and safety guardrails.

**Success Criteria** (ALL must be met):

1. ✅ **Test plan discovered**: Evidence sources identified (docs, CI configs, or build manifests)
2. ✅ **Commands selected**: Appropriate test commands chosen based on mode (fast/ci/full) and constraints
3. ✅ **User confirmation obtained**: Approval received before installing dependencies, using network, or starting services
4. ✅ **Tests executed**: Commands run with captured output and exit codes
5. ✅ **Results summarized**: Test Plan Summary produced with evidence, commands, execution status, and failures (if any)

**Acceptance Test**: Can a developer reproduce the test execution by following the Test Plan Summary without additional context?

---

## Scope Boundaries

**This skill handles**:

- Discovering test commands from repository evidence (docs, CI, build manifests)
- Selecting appropriate test commands based on mode and constraints
- Executing tests with safety guardrails and user confirmation
- Summarizing test results with evidence and failure diagnostics

**This skill does NOT handle**:

- Test quality assessment or coverage analysis (use `review-testing`)
- Fixing failing tests or debugging test failures (use `run-repair-loop`)
- Writing new tests or test infrastructure (use development skills)
- Reviewing test code for best practices (use `review-testing`)

**Handoff point**: When tests complete (pass or fail), hand off to `run-repair-loop` for fixing failures or `review-testing` for quality assessment.

## Use Cases

- You cloned a repo and want the correct test command without guessing.
- A repo has multiple test layers (unit/integration/e2e) and you need a safe default run plan.
- CI is failing and you want to reproduce locally by running the same commands used in workflows.

## Behavior

1. **Establish scope and constraints (ask if ambiguous)**
   - If the user did not specify, default to a **fast, local, non-destructive** run:
     - Unit tests only, no external services, no Docker, no network-dependent setup.
   - Ask the user to choose a mode if needed:
     - `fast`: unit tests only, minimal setup.
     - `ci`: mirror CI workflow commands as closely as possible.
     - `full`: include integration/e2e tests and service dependencies.
   - Ask whether Docker is allowed, whether network access is allowed, and whether installing dependencies is allowed.

2. **Discover the test plan (evidence-based)**
   - Read these sources in order; stop early if a clear, explicit test command is found:
     - `README.md`, `CONTRIBUTING.md`, `TESTING.md`, `docs/testing*`, `Makefile`
     - CI configs: `.github/workflows/*.yml`, `.gitlab-ci.yml`, `azure-pipelines.yml`, `Jenkinsfile`
     - Build manifests: `package.json`, `pyproject.toml`, `setup.cfg`, `tox.ini`, `go.mod`, `pom.xml`, `build.gradle*`, `*.csproj`, `Cargo.toml`
   - Identify:
     - Primary test entrypoints (`npm test`, `pnpm test`, `yarn test`, `pytest`, `tox`, `go test`, `dotnet test`, `mvn test`, `gradle test`, `cargo test`, etc.)
     - Test layers and markers (unit vs integration vs e2e)
     - Environment prerequisites (DB, Redis, Docker Compose, required env vars, secrets)
     - How CI sets up dependencies (services, caches, artifacts)
   - Prefer **explicit instructions** found in docs or CI over heuristics.

3. **Select an execution plan**
   - If `ci` mode: derive the run sequence from the repo's CI workflow steps (closest match).
   - If `fast` mode: pick the most direct unit-test command with the least prerequisites.
   - If multiple stacks exist (e.g., backend + frontend), propose running each stack separately in a deterministic order.
   - If the plan requires dependency installation or service startup, request confirmation before proceeding.

4. **Execute with guardrails**
   - Always print the exact commands you will run before running them.
   - Use a working directory rooted at the target repo (default `.`).
   - Capture and summarize failures:
     - First failing command and exit code
     - The most relevant error excerpt
     - Next actions (missing toolchain, missing env var, service not running, etc.)
   - Avoid destructive operations:
     - Do not run `rm -rf`, `git clean -fdx`, `docker system prune`, or database drop/migrate commands without explicit user approval.
   - If the repo requires secrets, do not ask the user to paste secrets into chat. Prefer `.env` files, secret managers, or documented local dev flows.

## Input & Output

**Input**

- Target repository path (default `.`).
- Mode: `fast` (default), `ci`, or `full`.
- Constraints: allow dependency install (yes/no), allow network (yes/no), allow Docker (yes/no).

**Output**

- A short "Test Plan Summary" containing:
  - Evidence: which files/paths informed the plan
  - Chosen commands (in order)
  - Assumptions and prerequisites
  - What was executed and what was skipped (and why)
- Command transcript snippets sufficient to debug failures (do not dump extremely long logs unless asked).

## Restrictions

### Hard Boundaries

- Do not invent test commands when evidence exists (prefer docs/CI).
- Do not install dependencies, run Docker, or start external services without confirmation.
- Do not modify repository files unless the user explicitly requests it (exception: generating a report file if the user asked for artifacts).
- Do not exfiltrate secrets; do not request sensitive credentials in chat.

### Skill Boundaries (Avoid Overlap)

**Do NOT do these (other skills handle them)**:

- **Test quality assessment**: Evaluating test coverage, test design, or testing best practices → Use `review-testing`
- **Fixing test failures**: Debugging failing tests, repairing broken test code, or investigating root causes → Use `run-repair-loop`
- **Writing tests**: Creating new test cases, test infrastructure, or test frameworks → Use development/implementation skills
- **Code review**: Reviewing test code for quality, maintainability, or best practices → Use `review-testing`
- **Repository analysis**: Comprehensive codebase structure analysis or architecture review → Use `review-codebase`

**When to stop and hand off**:

- Tests fail and user asks "why?" or "how to fix?" → Hand off to `run-repair-loop` for debugging and repair
- User asks "are these tests good?" or "what's our coverage?" → Hand off to `review-testing` for quality assessment
- User asks "can you write tests for X?" → Hand off to development workflow for test implementation
- Tests pass and user asks "what should we test next?" → Hand off to `review-testing` for test strategy recommendations

## Self-Check

### Core Success Criteria (ALL must be met)

- [ ] **Test plan discovered**: Evidence sources identified (docs, CI configs, or build manifests)
- [ ] **Commands selected**: Appropriate test commands chosen based on mode (fast/ci/full) and constraints
- [ ] **User confirmation obtained**: Approval received before installing dependencies, using network, or starting services
- [ ] **Tests executed**: Commands run with captured output and exit codes
- [ ] **Results summarized**: Test Plan Summary produced with evidence, commands, execution status, and failures (if any)

### Process Quality Checks

- [ ] **Evidence-based selection**: Did I identify at least one authoritative test instruction source (doc file, CI workflow, or build manifest)?
- [ ] **Safety guardrails applied**: Did I ask for confirmation before any action that installs dependencies, uses network, starts Docker/services, or changes state?
- [ ] **Commands printed**: Did I print the exact commands before running them?
- [ ] **Failures diagnosed**: If tests failed, did I provide the first failing command, exit code, and likely root cause category?
- [ ] **No destructive operations**: Did I avoid running destructive commands (`rm -rf`, `git clean`, `docker system prune`, database drops) without explicit approval?
- [ ] **No secret exfiltration**: Did I avoid requesting sensitive credentials in chat and prefer `.env` files or documented local dev flows?

### Acceptance Test

**Can a developer reproduce the test execution by following the Test Plan Summary without additional context?**

If NO: Test Plan Summary is incomplete. Add missing evidence, commands, or prerequisites.

If YES: Skill execution is complete. Proceed to handoff if needed.

## Examples

**Example 1: JavaScript repo with package.json**

User: "Run tests for this repo."

Agent:

1. Inspect `package.json` scripts and `.github/workflows/*`.
2. Decide mode `fast` and propose:
   - `npm test` (or `pnpm test` / `yarn test` if the repo standardizes on it)
3. Ask: "Install dependencies (`npm ci`) and allow network?"
4. Run:
   - `npm ci`
   - `npm test`
5. Summarize results and point to failing test output if any.

**Example 2 (Edge case): Monorepo with integration tests requiring Docker**

User: "Mirror CI locally."

Agent:

1. Parse `.github/workflows/ci.yml` and identify separate jobs:
   - backend unit tests
   - frontend tests
   - integration tests with `docker compose`
2. Ask for confirmation:
   - allow Docker
   - allow network
   - which jobs to run (all vs only failing job)
3. Execute in a controlled order:
   - install deps per job
   - run unit tests first
   - bring up services for integration tests
4. If integration tests fail, summarize:
   - service health / port conflicts
   - missing env vars
    - how CI config differs from local

---

## Appendix: Output contract

Each skill execution MUST produce a **Test Plan Summary** in this exact JSON format:

```json
{
  "test_plan_summary": {
    "mode": "fast | ci | full",
    "evidence": ["path/to/source1", "path/to/source2"],
    "commands": [
      {"command": "npm test", "purpose": "run unit tests", "order": 1}
    ],
    "prerequisites": ["npm ci", "Docker running"],
    "executed": ["npm ci", "npm test"],
    "skipped": ["integration tests - require Docker"],
    "result": {
      "status": "passed | failed | blocked",
      "exit_code": 0,
      "first_failure": {
        "command": "npm test",
        "exit_code": 1,
        "error_excerpt": "FAIL src/utils.test.js"
      }
    }
  }
}
```

| Element | Type | Description |
| :--- | :--- | :--- |
| `mode` | string | Selected mode: `fast`, `ci`, or `full` |
| `evidence` | array | Source files that informed the test plan |
| `commands` | array | Selected test commands with purpose and order |
| `prerequisites` | array | Required setup steps |
| `executed` | array | Commands actually run |
| `skipped` | array | Commands skipped and reason |
| `result.status` | string | `passed`, `failed`, or `blocked` |
| `result.exit_code` | number | Exit code of test command |
| `result.first_failure` | object | First failure details (if any) |

This schema enables Agent consumption without prose parsing.
