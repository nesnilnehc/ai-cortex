---
name: orchestrate-repair-loop
description: Iteratively converge the sibling engineering and functional gates, apply targeted fixes, then re-review and re-verify until both pass or a stop condition is reached.
description_zh: 迭代收敛工程门禁与功能门禁，实施定向修复并重新审查、验证，直至两者通过或满足停止条件。
tags: [automation, devops, optimization]
version: 1.3.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [repair, fix tests, delivery, stabilize, auto repair, auto fix, auto fix changes]
aliases: [run-repair-loop]
compatibility: Requires a shell and the repo's toolchains to run tests (language-dependent). May require git for diff-based review.
input_schema:
  type: code-scope
  description: Repository path and scope (diff or codebase) to converge to clean state
  defaults:
    scope: diff
output_schema:
  type: diagnostic-report
  description: Repair loop report with iterations, commands, patches, and final state (persist only if explicitly requested)
---

# Skill: Run the repair loop (engineering gate + functional gate + fix)

## Purpose

Converge a repository or change set by running two sibling gates and applying the smallest targeted repair:

1. **Engineering gate** — `orchestrate-code-review` evaluates intrinsic code quality.
2. **Functional gate** — `review-implementation-alignment` compares approved intent with implementation, while `automate-tests` or the acceptance harness executes correctness evidence.
3. **Repair** — fix a blocking signal from either gate.
4. **Repeat** — rerun every gate affected by the repair until both pass or a stop condition is reached.

The gates are logically peers. They may run in either order or in parallel when the runtime supports it; passing one never substitutes for the other.

---

## Core Objective

**Primary goal**: converge the repository to a verified state — no blocking engineering findings, approved intent aligned with production code, and functional checks passing — using a bounded, evidence-driven loop.

**Success criteria** (all must be met):

1. ✅ **Definition of done resolved**: the preflight choices (scope, test mode, max iterations, allowed actions) are confirmed before the loop starts
2. ✅ **Both gates evidenced**: engineering findings and functional alignment/acceptance evidence are reported separately
3. ✅ **Affected gates re-run after a fix**: every repair is followed by the narrowest functional and engineering checks it can invalidate
4. ✅ **Bounded loop**: the loop terminates on convergence or on an explicit stop condition - no unbounded retrying
5. ✅ **Structured final report**: the output includes a repair-loop report (appendix: output contract) covering the commands run, the failures, the patches, and the remaining risk

**Acceptance** test: does the final report show either (a) both sibling gates passing with traceable evidence, or (b) an explicit stop condition with remaining engineering and functional problems separated?

---

## Scope Boundaries

**This skill covers**:

- The multi-iteration engineering-gate + functional-gate → fix loop
- Diff-scoped and codebase-scoped review through `review-diff` and `orchestrate-code-review`
- Functional alignment through `review-implementation-alignment` when approved artifacts exist
- Test and acceptance execution through `automate-tests` or the project harness
- Minimal targeted patches that preserve the API contract
- Stop-condition detection (no progress, environment blocker, flaky tests, iteration limit)
- A structured repair-loop report as output

**This skill does not cover**:

- Installing dependencies, using the network, or starting Docker/services without explicit confirmation
- Large refactors without explicit user approval
- Modifying unrelated sibling repositories
- Disabling tests, weakening assertions, or deleting coverage without explicit user approval

**Handoff point**: when the loop converges or reaches a stop condition, present the repair-loop report to the user. For a risky change (architecture migration, authentication change, broad refactor), pause and ask for explicit approval before applying it.

---

## Use Cases

- "Keep fixing until the tests pass."
- "Run engineering and functional gates, then fix until both pass."
- "Stabilize this PR/change set with iterative testing and targeted fixes."
- "Run CI-like tests, fix the failures, repeat until stable."

---

## Behavior

### 1. Preflight (must be resolved once)

If `CLAUDE.md` or `.ai-cortex/config.yaml` exists, read `test_command` and the rest from there first; otherwise fall back to discovery. See [docs/guides/project-config.md](../../docs/guides/project-config.md).

Confirm or default the following:

- **Target**: repository path (default `.`) and scope:
  - `diff` (default): focus on the current changes, preferring `review-diff`.
  - `codebase`: review the given set of paths, preferring `review-codebase` / the language skills through `orchestrate-code-review`.
- **Definition of done**:
  - Engineering: no `critical`/`major` findings remain from `orchestrate-code-review`.
  - Functional alignment: no `critical`/`major` ALN findings remain when an approved artifact chain exists.
  - Functional execution: the selected test and acceptance plan passes.
  - If only "minor"/"suggestion" findings remain, list them and ask whether to address them.
- **Loop bounds**:
  - `max_iterations` default: `5`.
  - `time_budget` default: "best effort"; if the user gives a time limit, honor it strictly.
- **Allowed actions** (ask when unclear; default to the safer choice):
  - Modify repository files: **yes** (this skill exists to repair), but keep the change minimal.
  - Install dependencies: **confirm before running** (a reasonable action, but outside the implicit authorization of "change the code").
  - Network access: **confirm before running** (only where test execution needs it; not initiated while idle).
  - Docker/services (DB/Redis/etc.): **confirm before running** (start on demand, stop once the tests finish).
  - Large refactors: **no**, not without confirmation.

### 2. The iteration loop

For `i = 1..max_iterations`:

1. **Run or refresh the engineering gate**
   - Run `orchestrate-code-review` over the selected diff or codebase scope, including untracked additions in diff mode.
   - A narrow rerun may call only the atomic reviewers whose evidence a repair changed, but the final iteration includes the complete applicable engineering gate.
   - **Try an existing review skill first; review it yourself only when none can be invoked**. Not finding a
     skill name does not mean it is absent — different skill-listing interfaces cover different sets, and
     concluding "not installed" from a single lookup throws away a whole set of ready-made capability. When
     reviewing inline, write in the report that you "could not invoke `<skill name>`, reviewed inline", so the
     reader does not take it for the standard path.

2. **Run or refresh the functional gate**
   - When approved requirements, designs or tasks exist, run `review-implementation-alignment` over that artifact chain, the implementation scope and current evidence.
   - Use `automate-tests` to discover and run the best-matching test command in the selected mode:
     - `fast` (default): unit tests only, minimal setup.
     - `ci`: stay as close to the CI steps as possible.
     - `full`: includes integration / e2e (dependencies and services need confirming first).
   - **When changed behavior crosses an integration boundary and the repository provides a runnable integration layer, run it at least once before the loop ends**, even if `fast` was used throughout. Otherwise record why it is not applicable or what environment blocks it.
     The reason is concrete: unit tests mostly `new` the object under test directly, so **they stay green
     when a constructor signature changes**, while an integration test blows up on the spot — and worse,
     that explosion often masks the real defect behind it (a missing constructor argument first yields
     `undefined.x`, and the real problem surfaces only once that is fixed). A fully green `fast` run is never
     a reason to leave integration unrun.
   - Capture:
     - The first failing command and its exit code
     - The most relevant error excerpt (do not dump large logs unless asked)

3. **Synthesize the fix plan (smallest correct patch)**
   - Pick the **one** primary problem to address first:
     - The first failing test/command usually wins (highest signal).
     - A `critical` engineering, alignment, data or security problem takes precedence over non-critical test cleanup.
   - Prefer a fix that:
     - Changes the smallest surface area
     - Preserves the API/contract unless explicitly approved
     - Adds or adjusts a test when fixing a bug (where feasible)

4. **Apply the fix**
   - Implement the patch.
   - Avoid unrelated formatting or churn.
   - If the fix requires a risky change (architecture migration, authentication change, broad refactor), pause and ask.

5. **Re-run every affected gate**
   - Re-run the most relevant failing test or acceptance subset.
   - Re-run alignment when behavior, contracts, data mapping, wiring or tests changed.
   - Re-run the affected engineering reviewers when production code, configuration or tests changed.
   - If fixed, proceed to the next remaining failure/finding within the same iteration only if it is trivial; otherwise move to the next loop iteration.

6. **Stop early once converged**
   - Stop only when both sibling gates pass: no blocking engineering or alignment findings, and all selected functional checks pass.
   - **But "the tests were green from the start" is not convergence**. Green only says the existing
     assertions were not broken; it says nothing about whether this batch of changes is sound — a unit test
     verifies the behavior of a part, and it cannot see what goes wrong between parts or at real scale. When
     the repository arrives green, all of the loop's forward motion sits in the review half: **convergence
     requires the complete engineering gate and, when artifacts exist, implementation-alignment review**. Skipping them and
     declaring the repo clean turns the loop into an idle spin.

### 2b. Criteria ownership

This Skill does not maintain another review checklist. Intrinsic quality criteria live in the canonical engineering Rule sets. Missing acceptance behavior, dropped fields, built-but-unwired code and implementation-shaped tests live in [implementation-alignment-quality](../../rules/implementation-alignment-quality.md). The loop routes to those owners and consumes their findings.

### 3. Stop conditions (must not loop forever)

Stop and ask the user for direction if any of the following happens:

- **No progress**: the same failure repeats for 2 iterations with no new information.
- **Environment blocker**: a missing toolchain, a missing secret, or an unavailable dependency (DB/Docker), with the setup it needs not yet approved by the user.
- **Flaky tests**: a nondeterministic failure is suspected (for example, a retry passes with nothing changed).
- **Iteration limit reached**: `max_iterations` is exhausted and failures remain.

When stopping, offer the shortest-path options:

- Run a different test mode (`fast` -> `ci` -> `full`)
- Allow install/network/Docker
- Narrow the scope (fix only the first failing test)
- Raise the iteration limit

### Report persistence

By default, do not write a standalone report file. If the user explicitly asks for it to be kept, write to the path resolved from the project norms, or default to `docs/calibration/repair-loop.md` and overwrite the canonical file, unless a snapshot is explicitly requested.

---

## Input & Output

### Input

- Target path (default `.`)
- Scope: `diff` (default) or `codebase` (+ paths)
- Test mode: `fast` (default), `ci`, `full`
- Constraints: install/network/Docker/services allowed (yes/no)
- `max_iterations` (default `5`)
- Optional: a time budget

### Output

- **Repair-loop report**:
  - The definition of done used
  - Evidence sources (which files/CI config informed the test plan)
  - For each iteration:
    - Engineering gate findings and coverage state
    - Functional alignment findings when an artifact chain exists
    - Test/acceptance command and result
    - The first-failure excerpt (if any)
    - The changes made (files touched + intent)
    - Remaining failures/findings
  - Final state:
    - Engineering gate: pass or remaining blocking findings
    - Functional gate: alignment state plus passing commands, or remaining failures

---

## Restrictions

### Hard Boundaries

- An action beyond modifying code (installing a dependency, a network request, starting Docker/services) needs explicit confirmation before it runs — these are reasonable repair actions, but they need the user's informed consent; do not carry them out quietly.
- Do not ask the user to paste credentials into the conversation. Prefer a local env file or the documented development workflow.
- Do not "fix" by disabling tests, weakening assertions, or deleting coverage, unless the user explicitly approves and the trade-off is recorded.
- Avoid large refactors by default; prefer the smallest patch that unblocks correctness.
- Keep the change scope inside the target repository; do not modify unrelated sibling repositories.

### Skill Boundaries (avoid overlap)

**Do not do these (other skills handle them)**:

- **Test execution only** (no review, no repair loop): use `automate-tests`
- **Test quality assessment** (coverage, structure, edge-case adequacy): use `review-testing`
- **Full code review** (no test-fix iteration): use `orchestrate-code-review`
- **Diff review only** (no test execution, no fix iteration): use `review-diff`
- **Writing new tests from scratch** (rather than fixing existing failures): use a development skill

**When to stop and hand off**:

- The loop converges (both sibling gates pass) → present the repair-loop report and stop
- A stop condition is hit (no progress, environment blocker, flaky tests, iteration limit) → show the options and wait for the user's direction
- The user asks for a one-off code review without fixes → hand off to `orchestrate-code-review` or `review-diff`
- The user asks only to run the tests without fixing → hand off to `automate-tests`

---

## Self-Check

### Core success criteria

- [ ] **Definition of done resolved**: the preflight choices (scope, test mode, max iterations, allowed actions) are confirmed before the loop starts
- [ ] **Both gates evidenced**: engineering findings and functional alignment/acceptance results are reported separately
- [ ] **Coverage preserved**: the engineering report retains Rule coverage by emitting Skill, including waived, not-applicable and evidence-limited IDs
- [ ] **A green test run is not convergence**: the complete engineering gate and applicable alignment review ran before completion
- [ ] **Prefer the existing review skills**: try to invoke one before reviewing inline; when switching to inline, say so in the report
- [ ] **Tests re-run after a fix**: once the fix is applied within an iteration, the failing test command (or a targeted subset) is always re-run
- [ ] **Bounded loop**: the loop terminates on convergence or on an explicit stop condition - no unbounded retrying
- [ ] **Structured final report**: the output includes a repair-loop report (appendix: output contract) covering the commands run, the failures, the patches, and the remaining risk

### Process quality checks

- [ ] **Minimal patch surface**: each fix touches only the files needed to solve the identified problem - no unrelated formatting or churn.
- [ ] **Flaky-test awareness**: a nondeterministic failure (for example, a retry that passes with no code change) is detected and flagged rather than blindly "fixed".
- [ ] **Risky-change pause applied**: an architecture migration, an authentication change, or a broad refactor triggered an explicit user confirmation before proceeding.
- [ ] **Progress tracked per iteration**: every iteration log shows a clear delta (a new signal or a new fix) - no empty iterations.

### Acceptance test

Does the final report show either (a) both sibling gates passing with traceable evidence, or (b) an explicit stop condition with remaining engineering and functional problems separated?

---

## Examples

### Example 1: fix a failing unit test in a Node repository

User: "Make the tests pass. Keep fixing until it is green."

Agent:

1. Preflight: scope=`diff`, test mode=`fast`, max_iterations=5; installing (`npm ci`) and network access are confirmed as allowed.
2. Iteration 1: run the engineering gate, applicable alignment review and `npm test`; select the highest-priority blocking signal.
3. Apply the smallest fix, rerun `npm test`, then rerun every engineering/alignment dimension the fix can invalidate.
4. Stop once the engineering gate, applicable alignment review and `npm test` all pass.

### Example 2 (edge case): the integration tests need Docker and secrets

User: "Mirror CI and fix the failures."

Agent:

1. Preflight: test mode=`ci` is suggested, but CI is detected to use `docker compose` and env secrets.
2. A stop condition fires: environment blocker (Docker + secrets not approved/unavailable).
3. Ask the user to choose:
   - Run only the `fast` unit tests locally, or
   - Allow Docker and provide a non-chat secrets workflow, or
   - Run only the failing CI job steps that do not need secrets.
