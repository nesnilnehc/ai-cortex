---
name: scaffold-agent-tests
description: Generate an LLM agent test suite (golden cases, mock-LLM unit tests, evaluator harness) from an agent implementation and its agent-test contract. Use when an agent has no tests, or a contract exists but the test code is missing.
description_zh: 从 agent 实现与测试契约生成测试套件（golden cases、mock LLM 单测、evaluator）；用于 agent 缺测试或契约已有但测试代码缺失时。
tags: [testing, automation]
version: 1.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [scaffold agent tests, generate agent tests, author agent tests, agent test suite]
compatibility: Requires the agent implementation source and a test contract (specs/agent-test-modeling.md instance); a shell and the repo's test toolchain.
input_schema:
  type: code-scope
  description: Path to an agent implementation plus its agent-test contract document
  defaults:
    scope: file
output_schema:
  type: code-artifact
  description: Generated test files (mock-LLM unit tests, golden dataset, evaluator harness) traceable to the contract
---

# Skill: Scaffold Agent Tests

## Purpose

Read an LLM agent's implementation and its test contract (an instance of [specs/agent-test-modeling.md](../../specs/agent-test-modeling.md)), and generate a test suite traceable to that contract — exact assertions for the deterministic parts, oracle tests for the non-deterministic parts, a golden dataset and an evaluator harness.

---

## Core Objective

**Primary goal**: produce agent test code that follows [rules/standards-agent-testing.md](../../rules/standards-agent-testing.md), with every assertion traceable to a clause of the contract.

**Success criteria** (all of them must hold):

1. ✅ **Contract located**: the agent implementation and the `agent-test-contract` document were read
2. ✅ **Test matrix generated**: capability boundary / input contract / tool boundary / write-back precondition each map onto a test
3. ✅ **Oracle chosen correctly**: deterministic behavior gets exact assertions; non-deterministic behavior gets a contract / trace / rubric / golden oracle
4. ✅ **Golden dataset on disk**: positive + boundary + error, ≥ 1 of each, carrying a `Covers` traceability anchor
5. ✅ **Real-model tests isolated**: tests that hit a real model carry the `eval` marker, and the unit pipeline uses a mock LLM
6. ✅ **Traceable**: each test's `Covers` points at a contract ID or an upstream AC

**Acceptance test**: can a developer tell what each test guards from the generated tests plus the contract alone, without reading the agent source?

---

## Scope Boundaries

**This skill owns**:

- Reading the agent implementation and the test contract, then generating the test matrix
- Generating mock-LLM unit tests, the golden dataset and the evaluator harness
- Choosing an oracle for non-deterministic behavior and writing exact assertions for deterministic behavior
- Attaching a `Covers` traceability anchor to every test

**This skill does not own**:

- **Running the tests** → use [automate-tests](../automate-tests/SKILL.md)
- **Reviewing test quality / coverage** → use [review-testing](../review-testing/SKILL.md)
- **Writing the test contract document** → a person writes the contract per [specs/agent-test-modeling.md](../../specs/agent-test-modeling.md); this skill consumes a contract, it does not author one
- **Fixing failing tests / debugging the agent** → use [orchestrate-repair-loop](../orchestrate-repair-loop/SKILL.md)

**Handoff point**: once the tests are generated → hand them to automate-tests to run, and to review-testing to review.

---

## Preconditions

- The agent implementation source is readable
- A test contract following [specs/agent-test-modeling.md](../../specs/agent-test-modeling.md) exists; **when it is missing**, prompt the user to write one per that spec rather than inventing capability boundaries

---

## Execution

### 1. Locate the contract and the implementation

- Read the `agent-test-contract` document (its frontmatter `agent_ref` points at the implementation)
- Contract missing → stop and prompt: write the contract per [specs/agent-test-modeling.md](../../specs/agent-test-modeling.md) first

### 2. Generate the test matrix

Map each section of the contract onto test entries:

| Contract section | Test type | oracle |
|---|---|---|
| Capability boundary | positive + negative behavior test | trace / contract |
| Input contract (missing-field detection) | boundary + error test | trace (assert it asks back and writes nothing) |
| Tool-call boundary | trace test | trace (the forbidden set never appears) |
| Write-back precondition | refusal test when the precondition fails | trace |
| Golden Cases | regression suite | per the contract's judgement-method column |

### 3. Choose the oracle and write the tests

- **Deterministic logic** (schema validation, tool arguments, permissions) → exact assertions (following [standards-test-code](../../rules/standards-test-code.md): AAA plus the three naming elements)
- **Non-deterministic output** → a contract / trace / rubric / golden oracle (following [standards-agent-testing §2](../../rules/standards-agent-testing.md))
- The unit pipeline uses a mock LLM / recorded replay; real-model tests carry the `eval` marker

### 4. Write the golden dataset

- Generate a versioned golden data file from the contract's Golden Cases table
- Each entry carries input / expectation / judgement method / `Covers`

### 5. Generate the evaluator harness

- For rubric / semantic / statistical judgements, generate an evaluator (LLM-as-judge or a semantic matcher)
- Emit the golden-set pass rate and compare it against the contract's `pass_threshold`

### 6. Summarize

- List the generated files, each test's `Covers`, and the unit vs eval split
- Point at what follows: automate-tests to run them, review-testing to review them

---

## Limitations

### Hard Boundaries

- Do not invent agent capability boundaries when the contract is missing (ask for the contract first)
- Do not mock the logic of the agent under test (mock the model's non-determinism only)
- Do not weaken an assertion or delete a golden case to make an eval pass
- Do not run the tests and do not modify the agent implementation (generate test artifacts only)

### Skill boundaries (avoid overlap)

- **Running the tests** → [automate-tests](../automate-tests/SKILL.md)
- **Reviewing test quality** → [review-testing](../review-testing/SKILL.md)
- **Debugging / fixing** → [orchestrate-repair-loop](../orchestrate-repair-loop/SKILL.md)

---

## Self-Check

- [ ] The agent implementation and the test contract were read
- [ ] The test matrix covers every section of the contract (capability boundary / input / tools / write-back / golden)
- [ ] Deterministic parts use exact assertions, non-deterministic parts use an oracle
- [ ] The golden set holds positive + boundary + error cases, each with a `Covers`
- [ ] Real-model tests carry the `eval` marker; unit tests use a mock LLM
- [ ] Every test traces back to the contract or to an upstream AC

---

## Examples

### Example: a requirement-clarification agent

User: "generate tests for the clarification agent."

Agent:

1. Read `agent-test-clarification.md` (the contract) and `src/agents/clarification.py`
2. Generate the matrix: missing-field detection (trace), full write-back (contract), empty input (trace), forbidden tools (trace)
3. Write the tests:
   - unit: the mock LLM returns a recorded response; assert that `ask_user` fires and `write_requirement` does not
   - eval (marked): run the golden set against the real model, with a rubric scoring how clear the follow-up wording is
4. Write `golden/clarification.jsonl` (3 entries: acceptance missing / information complete / empty input)
5. Generate the evaluator: compute the golden pass rate and compare it against `pass_threshold: 0.9`
6. Summarize: 4 unit suites plus 1 eval suite, each carrying `Covers: ACME-REQ-08#AC1/AC3`; point at automate-tests to run them
