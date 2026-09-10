---
name: orchestrate-repair-loop
description: Iteratively review changes, run automated tests, and apply targeted fixes until issues are resolved (or a stop condition is reached).
description_zh: 迭代审查变更、运行自动化测试并实施定向修复，直至问题解决或满足停止条件。
tags: [automation, devops, optimization]
version: 1.2.1
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [repair, fix tests, delivery, stabilize, auto repair, auto fix, auto fix changes]
aliases: [orchestrate-repair-loop]
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

# Skill: Run the repair loop (review + test + fix)

## Purpose

Converge a repository, or a change set, to "clean" by running **multiple loop iterations**:

1. **Review** (catch problems early and prevent regressions),
2. **Test** (get an actionable signal),
3. **Fix** (apply the smallest correct patch),
4. Repeat until **no blocking problems remain** or a **stop condition** is reached.

---

## Core Objective

**Primary goal**: converge the repository to a "clean" state — all tests passing and no "critical"/"major" review findings — using a bounded, evidence-driven review-test-fix loop.

**Success criteria** (all must be met):

1. ✅ **Definition of done resolved**: the preflight choices (scope, test mode, max iterations, allowed actions) are confirmed before the loop starts
2. ✅ **Evidence first in every iteration**: each iteration produces at least one of a new test result, a new review signal, or a concrete code change
3. ✅ **Tests re-run after a fix**: the failing test command (or a targeted subset) is always re-run after the fix is applied, within the same iteration
4. ✅ **Bounded loop**: the loop terminates on convergence or on an explicit stop condition - no unbounded retrying
5. ✅ **Structured final report**: the output includes a repair-loop report (appendix: output contract) covering the commands run, the failures, the patches, and the remaining risk

**Acceptance** test: does the final report show either (a) tests passing with no blocking review findings, or (b) an explicit stop condition, with the remaining problems and the options open to the user stated clearly?

---

## Scope Boundaries

**This skill covers**:

- The multi-iteration review → test → fix loop
- Diff-scoped and codebase-scoped review through `review-diff` and `orchestrate-code-review`
- Test execution through `automate-tests` (fast/ci/full modes)
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
- "Run a review-test-fix loop and get the repository green."
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
  - Tests: the selected test plan passes (fast/ci/full).
  - Review: no "critical"/"major" review findings remain.
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

1. **Gather the current signals (evidence first)**
   - Scope = `diff`: run `review-diff` over the current changes, including untracked additions.
   - Scope = `codebase`: run `orchestrate-code-review`, or pick the atomic review skill for the language
     (`review-typescript` / `review-python` / …).
   - Test failures from the previous round: settle those first.
   - **Try an existing review skill first; review it yourself only when none can be invoked**. Not finding a
     skill name does not mean it is absent — different skill-listing interfaces cover different sets, and
     concluding "not installed" from a single lookup throws away a whole set of ready-made capability. When
     reviewing inline, write in the report that you "could not invoke `<skill name>`, reviewed inline", so the
     reader does not take it for the standard path.

2. **Run the tests**
   - Use `automate-tests` to discover and run the best-matching test command in the selected mode:
     - `fast` (default): unit tests only, minimal setup.
     - `ci`: stay as close to the CI steps as possible.
     - `full`: includes integration / e2e (dependencies and services need confirming first).
   - **Run the integration layer at least once before the loop ends**, even if `fast` was used throughout.
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
     - If the review found a "critical" security/correctness problem, fix it before or alongside the tests.
   - Prefer a fix that:
     - Changes the smallest surface area
     - Preserves the API/contract unless explicitly approved
     - Adds or adjusts a test when fixing a bug (where feasible)

4. **Apply the fix**
   - Implement the patch.
   - Avoid unrelated formatting or churn.
   - If the fix requires a risky change (architecture migration, authentication change, broad refactor), pause and ask.

5. **Re-run the minimal verification**
   - If the framework supports it, re-run the most relevant subset of failing tests; otherwise re-run the same test command.
   - If fixed, proceed to the next remaining failure/finding within the same iteration only if it is trivial; otherwise move to the next loop iteration.

6. **Stop early once converged**
   - Stop when the tests pass and no "critical"/"major" review findings remain.
   - **But "the tests were green from the start" is not convergence**. Green only says the existing
     assertions were not broken; it says nothing about whether this batch of changes is sound — a unit test
     verifies the behavior of a part, and it cannot see what goes wrong between parts or at real scale. When
     the repository arrives green, all of the loop's forward motion sits in the review half: **convergence
     requires at least one complete review pass (see "What to look for in review")**. Skipping it and
     declaring the repo clean turns the loop into an idle spin.

### 2b. What to look for in review (the class tests cannot see)

When the tests are green and the problem is still there, it almost always has the same shape: **every part
is correct, the assembly is wrong, and the failure is silent**. Reading file by file rarely reveals them — hunt
by the categories below, each of which gives a "how to find it" and a "why the tests miss it".

| What to look for | How to find it | Why the tests miss it |
| :--- | :--- | :--- |
| **Duplicated work on the hot path** | In a function that runs per request / per message, the same data is read twice; a newly added call is hung off an existing full load | The behavior is entirely correct, it only gets slower with scale; no assertion counts how many reads happened |
| **Written into the acceptance criteria but never implemented** | Read the acceptance items of the task / requirement against the implementation clause by clause ("with a timeout **and a cache**" — the timeout is there, where is the cache?) | The tests were written from the implementation, so whatever the implementation missed, the tests miss too |
| **A field dropped while crossing layers** | A field is computed in a lower layer; follow it up to the top layer and see which layer it disappears in | Each layer's unit tests pass on their own; not one of them crosses that seam |
| **Silent degradation from an optional dependency** | A newly added `@Optional()` / optional parameter / `?? default`: what happens when it is not supplied? | Omitting it raises no error, the behavior just falls back to the old path |
| **A capped batch job that never reports its backlog** | When a batched job fills a batch to the cap, can the log say "there is more behind this"? | The cap itself is correct, it only "looks like it finished" |
| **Built but never wired up** | Whether a new symbol has a production call site beyond itself and its tests (**import lines do not count**) | The part-level tests are all green; not one of them asks "who uses this" |
| **Configuration / wiring that only shows up in a real deployment** | Dependency injection, manifest registration, route prefixes, payload field pass-through | The unit tests `new` the object directly and never reach container assembly |

**Two disciplines for reading the results**:

- **When one criterion hits at an extremely high rate, suspect the criterion is too strict rather than the output.**
- **A zero false-positive rate means nothing without its denominator.** "Zero hits" across a batch of
  near-empty samples proves nothing — a zero false-positive rate over an inflated denominator misleads
  more easily than having no data at all.

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
    - The test command run and its result
    - The first-failure excerpt (if any)
    - The changes made (files touched + intent)
    - Remaining failures/findings
  - Final state:
    - Tests passing (under which command)
    - Remaining review items (if any) and whether they are blocking

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

- The loop converges (tests pass, no blocking findings) → present the repair-loop report and stop
- A stop condition is hit (no progress, environment blocker, flaky tests, iteration limit) → show the options and wait for the user's direction
- The user asks for a one-off code review without fixes → hand off to `orchestrate-code-review` or `review-diff`
- The user asks only to run the tests without fixing → hand off to `automate-tests`

---

## Self-Check

### Core success criteria

- [ ] **Definition of done resolved**: the preflight choices (scope, test mode, max iterations, allowed actions) are confirmed before the loop starts
- [ ] **Evidence first in every iteration**: each iteration produces at least one of a new test result, a new review signal, or a concrete code change
- [ ] **A green repo is not convergence**: when the repository arrives green, one complete review pass (§2b) is run before it is declared clean
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

Does the final report show either (a) tests passing with no blocking review findings, or (b) an explicit stop condition, with the remaining problems and the options open to the user stated clearly?

---

## Examples

### Example 1: fix a failing unit test in a Node repository

User: "Make the tests pass. Keep fixing until it is green."

Agent:

1. Preflight: scope=`diff`, test mode=`fast`, max_iterations=5; installing (`npm ci`) and network access are confirmed as allowed.
2. Iteration 1: run `npm test`, fix the first failing test, re-run `npm test`.
3. Iteration 2: run `review-diff` to catch edge cases introduced by the fix; re-run `npm test`.
4. Stop once `npm test` passes and no major review findings remain.

### Example 2 (edge case): the integration tests need Docker and secrets

User: "Mirror CI and fix the failures."

Agent:

1. Preflight: test mode=`ci` is suggested, but CI is detected to use `docker compose` and env secrets.
2. A stop condition fires: environment blocker (Docker + secrets not approved/unavailable).
3. Ask the user to choose:
   - Run only the `fast` unit tests locally, or
   - Allow Docker and provide a non-chat secrets workflow, or
   - Run only the failing CI job steps that do not need secrets.
