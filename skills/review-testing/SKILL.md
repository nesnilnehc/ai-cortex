---
name: review-testing
description: "Review code for testing: test existence, coverage adequacy, test quality and structure, edge-case and error-path coverage, and test maintainability. Cognitive-only atomic skill; output is a findings list."
description_zh: 审查测试：存在性、覆盖度、质量与结构、边界与错误路径覆盖、可维护性；认知原子技能。
tags: [code-review, cognitive]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review testing, testing review]
input_schema:
  type: code-scope
  description: Source files or directories to review
output_schema:
  type: findings-list
  description: Zero or more findings with location, category, severity, and suggestion
---

# Skill: Review Testing

## Purpose

Review code for **testing** concerns only. Do not define the scope (diff versus codebase) or perform language/framework/security/architecture analysis; those are separate atomic skills. Emit a **findings list** in the standard format for aggregation. Concentrate on test existence and coverage, test quality and structure, test types and layering, edge-case and error-path coverage, and test maintainability.

---

## Core Objective

**Primary goal**: produce a testing-centered findings list covering test existence, coverage adequacy, test quality/structure, test types/layering, edge-case coverage, and test maintainability for the given code scope.

**Success criteria** (all of them must hold):

1. ✅ **Testing scope only**: review the testing dimensions only; no scope selection, language/framework conventions, security, performance, or architecture analysis
2. ✅ **All six testing dimensions covered**: where relevant, assess test existence, coverage adequacy, quality/structure, types/layering, edge cases/error paths, and maintainability
3. ✅ **Findings format respected**: every finding carries location, category (`cognitive-testing`), severity, title, description, and an optional suggestion
4. ✅ **High-risk gaps flagged**: untested or under-tested high-risk code paths (authentication, payments, data mutation) are marked `critical` or `major`
5. ✅ **Analysis from code alone**: assess test adequacy from code structure and available artifacts, without running tests or generating coverage reports

**Acceptance** test: does the output contain a testing findings list covering every relevant dimension, with severity ratings matched to risk and actionable suggestions for raising test coverage and quality?

---

## Scope Boundaries

**This skill owns**:

- Test existence checks (missing test files for critical modules, services, public functions)
- Coverage adequacy analysis (coverage of high-risk paths: authentication, payments, data mutation)
- Test quality and structure (Arrange-Act-Assert, meaningful assertions, behavior rather than implementation)
- Test types and layering (unit, integration, e2e balance; mock/stub isolation)
- Edge-case and error-path coverage (boundary conditions, invalid input, failure modes)
- Test maintainability (DRY without sacrificing readability, fixture organization, brittle-test detection)

**This skill does not own**:

- Scope selection (deciding which files/paths to analyze) — the scope is supplied by the caller
- Running tests or generating coverage reports - use `automate-tests` for test execution
- Language/framework-specific test conventions - use `review-dotnet`, `review-java`, `review-go`, and so on.
- Security, performance, or architecture review — use the respective atomic skills
- Full orchestrated review — use `orchestrate-code-review`

**Handoff point**: once every testing finding is emitted, hand them to `orchestrate-code-review` for aggregation inside an orchestrated review. For actually running the tests, redirect to `automate-tests`.

---

## Use Cases

- **Orchestrated review**: used as the cognitive step when [orchestrate-code-review](../orchestrate-code-review/SKILL.md) runs scope → language → framework → library → cognitive.
- **Testing-centered review**: when the user only wants to assess test health and coverage (before a release, after a major refactor, or during onboarding, for instance).
- **Gap analysis**: identify untested modules, missing test types (unit/integration/e2e), or low-quality tests that give false confidence.

**When to use**: when the task includes a testing review. The scope and the code range are determined by the caller or the user.

---

## Behavior

### What this skill covers

- **Analyze**: the testing dimensions within the **given code scope** (files or a diff supplied by the caller). Do not decide the scope; take the code scope as input.
- **Do not**: perform scope selection, language/framework conventions, security, performance, or architecture review. Stay on testing alone.

### Review checklist (testing dimensions only)

1. **Do the tests exist**: do critical modules, services, and public functions have corresponding test files? Are there obvious gaps where critical logic is not exercised at all?
2. **Coverage adequacy**: is test coverage sufficient for the risk level of the code? Are the high-risk paths (authentication, payments, data mutation) tested? Note: consult coverage reports or metrics where they are available; otherwise assess structurally.
3. **Test quality and structure**: are the tests well structured (Arrange-Act-Assert, or Given-When-Then)? Do test names describe the scenario clearly? Are the assertions meaningful (not merely "does not throw")? Do the tests verify behavior rather than implementation detail?
4. **Test types and layering**: is there an appropriate mix of unit, integration, and end-to-end tests? Are unit tests isolated (mocks/stubs for external dependencies)? Do integration tests exercise real interactions where that is needed?
5. **Edge cases and error paths**: do the tests cover boundary conditions, invalid input, null/empty cases, concurrency scenarios, and expected error responses? Are failure modes tested explicitly?
6. **Test maintainability**: are the tests DRY without sacrificing readability? Are fixtures and helpers well organized? Are the tests brittle (tightly coupled to the implementation, over-mocked, or dependent on execution order)? Is test data managed cleanly (factories, builders, or fixtures rather than hard-coded magic values)?

### Tone and references

- **Professional and technical**: reference concrete locations (file:line or module). Emit findings carrying location, category, severity, title, description, and suggestion. Use severity `major` or `critical` for untested high-risk code paths.

---

## Input & Output

### Input

- **Code scope**: files or directories (or a diff) already selected by the user or by a scope skill. This skill does not decide the scope; it reviews the code it is given, for testing only.

### Output

- Emit zero or more **findings** in the format defined in **Appendix: Output Contract**.
- The category for this skill is **cognitive-testing**.

---

## Restrictions

### Hard Boundaries

- **Do not** perform scope selection, language, framework, security, performance, or architecture review. Stay inside the testing scope.
- **Do not** state a conclusion without a concrete location or an actionable suggestion.
- **Do not** require running tests or generating coverage reports. Analyze test adequacy from the code and the available artifacts (an existing coverage file, for example). For actually running the tests, use [automate-tests](../automate-tests/SKILL.md).
- **Do not** penalize the absence of tests for trivial code (plain getters, constants, generated code) unless that absence hides a real risk.

### Skill Boundaries

**Do not do these** (other skills handle them):

- Do not select or define the code scope - the scope is set by the caller or by `orchestrate-code-review`
- Do not run or execute tests - use `automate-tests` for test execution
- Do not analyze language/framework-specific test conventions - use the corresponding language skill
- Do not perform security, performance, or architecture analysis — use the respective atomic skills

**When to stop and hand off**:

- Once every testing finding is published, hand them to `orchestrate-code-review` for aggregation inside an orchestrated review
- When the user needs the tests actually run, redirect to `automate-tests`
- When the user needs a full review (scope + language + cognitive), redirect to `orchestrate-code-review`

---

## Self-Check

### Core success criteria

- [ ] **Testing scope only**: review the testing dimensions only; no scope selection, language/framework conventions, security, performance, or architecture analysis
- [ ] **All six testing dimensions covered**: where relevant, assess test existence, coverage adequacy, quality/structure, types/layering, edge cases/error paths, and maintainability
- [ ] **Findings format respected**: every finding carries location, category (`cognitive-testing`), severity, title, description, and an optional suggestion
- [ ] **High-risk gaps flagged**: untested or under-tested high-risk code paths (authentication, payments, data mutation) are marked `critical` or `major`
- [ ] **Analysis from code alone**: assess test adequacy from code structure and available artifacts, without running tests or generating coverage reports

### Process quality checks

- [ ] Were only the testing dimensions reviewed (no scope/language/security/architecture)?
- [ ] Were the relevant test existence, coverage adequacy, quality/structure, types/layering, edge cases, and maintainability covered?
- [ ] Does every finding carry location, category=cognitive-testing, severity, title, description, and an optional suggestion?
- [ ] Are the critical gaps (untested high-risk code) flagged explicitly and made actionable?

### Acceptance test

Does the output contain a testing findings list covering every relevant dimension, with severity ratings matched to risk and actionable suggestions for raising test coverage and quality?

---

## Examples

### Example 1: missing tests for a critical module

- **Input**: a payment-processing module with no test file.
- **Expected**: emit a critical finding for the missing tests on high-risk code; suggest unit tests for the core payment logic and integration tests for the gateway interaction. Category = cognitive-testing.

### Example 2: tests exist but are shallow

- **Input**: the authentication module has tests, but they cover only the happy path (a valid login) and skip invalid credentials, expired tokens, rate limiting, and account lockout.
- **Expected**: publish a major finding for insufficient edge-case coverage; list the concrete scenarios to add. Category = cognitive-testing.

### Edge case: a well-tested codebase

- **Input**: a module with comprehensive unit, integration, and end-to-end tests, clear structure, and broad coverage.
- **Expected**: emit zero findings, or suggestion-level findings for minor improvements (test-naming consistency, for example). Do not invent problems.
