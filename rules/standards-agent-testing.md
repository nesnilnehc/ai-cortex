---
artifact_type: rule
name: standards-agent-testing
version: 1.0.0
scope: LLM Agent 行为相关的测试代码与单 agent 测试契约
recommended_scope: user
status: active
---

# Rule: Agent Testing Standards

## Scope

Test code and single-agent test contract documents whose subject is LLM agent behaviour — non-deterministic behaviour that depends on model capability, model version, prompt, tool calls and retrieved context.

This rule applies on top of [standards-test-code](./standards-test-code.md). That one constrains general test coding standards (AAA, the three naming elements, isolation, determinism, Covers traceability, restraint with mocks); this one constrains only what changes because the subject under test is agent behaviour. Tests of deterministic code still belong to standards-test-code.

The data structure of a single-agent test contract is in [specs/agent-test-modeling.md](../specs/agent-test-modeling.md); this rule constrains behaviour — how to assert, isolation, regression gating, traceability.

---

## Constraints

### 1. Separate the deterministic from the non-deterministic

- **Deterministic parts** (parsers, schema validation, state machine transitions, tool argument construction, permission decisions, error handling) → assert precisely per standards-test-code, unit tested as usual
- **Non-deterministic parts** (LLM natural-language output, the model's reasoning path) → exact wording must not be the sole assertion; use an oracle from §2 instead

### 2. Extended test oracles

An assertion on non-deterministic behaviour must hit at least one of these oracles:

- **Contract assertion**: the output schema is valid, required fields are present, field types are correct
- **Trajectory assertion**: the tool call sequence is within the allowed set, forbidden calls did not occur, preconditions for a write-back were met
- **Evaluated score**: a rubric score or LLM-as-judge, with a pass threshold
- **Golden dataset**: recorded "input → expected output / expected trajectory" pairs, asserted by semantic or field matching rather than string equality
- **Statistical regression threshold**: success rate ≥ a threshold, such as a golden set pass rate ≥ 90%

### 3. Marking and isolating tests that hit a real model

- A test that hits a real model API must carry an `eval` or `e2e` marker (for example `@pytest.mark.eval`) and must stay out of the default unit pipeline
- The default unit pipeline uses a mock LLM or recorded response replay, for determinism and speed
- Mocks isolate model non-determinism only. You **must not** mock the agent's own logic — intent recognition, field validation, tool selection

### 4. Regression gate on a model or prompt change

- Any change to the model version, the prompt template or a tool definition → the full golden eval must be run
- A golden eval pass rate below the contract threshold blocks the merge
- Every such change must record a model version comparison — pass rate before against after

### 5. Maintaining the golden dataset

- Every golden case must carry: input, expected output or expected trajectory, the decision method (field / semantic / rubric), and a `Covers` traceability anchor
- The golden set is a versioned artifact living in the same repository as the agent code; a new capability must come with new golden cases
- You **must not** delete a failing golden case to make the eval pass — fix the agent, or mark it `known-failure` explicitly with a reason

### 6. Single-agent test contract

- Every agent that offers a capability externally must have a test contract document following [specs/agent-test-modeling.md](../specs/agent-test-modeling.md)
- Assertions in the test code must trace back to an item in that contract, with the `Covers` anchor pointing at a contract ID or an upstream AC

---

## Bad Patterns

```python
# ❌ exact assertion on free-form LLM text
def test_agent_reply():
    reply = agent.handle("我要提个需求")
    assert reply == "您的需求已记录"   # one wording change and it goes red for no reason
```

```python
# ❌ a real-model test with no marker, leaking into the unit pipeline
def test_clarification_flow():
    result = agent.run(real_llm_client, payload)  # slow and flaky in CI
    assert result.ok
```

```python
# ❌ mocking away the agent's own intent recognition
def test_intent():
    agent.detect_intent = Mock(return_value="create_requirement")
    assert agent.detect_intent("...") == "create_requirement"  # this tests nothing
```

```text
# ❌ merging a prompt change without running the golden eval
# ❌ an agent with no test contract, whose assertions have no Covers anchor
```

---

## Remediation

1. **Exact-wording assertion** → switch to a contract, trajectory, rubric or golden oracle (§2)
2. **Test hitting a real model** → add the `eval` marker; swap the unit pipeline to a mock LLM or recorded replay (§3)
3. **Build the golden dataset** and gate prompt and model changes on it (§4 / §5)
4. **Add a test contract for each agent** ([specs/agent-test-modeling.md](../specs/agent-test-modeling.md)) and add `Covers` anchors to the assertions (§6)

---

## Related assets

- **General test coding standards**: [standards-test-code](./standards-test-code.md) — applies on top; tests of deterministic code belong there
- **Data contract**: [specs/agent-test-modeling.md](../specs/agent-test-modeling.md) — the structure of a single-agent test contract
- **Execution capability**: [skills/scaffold-agent-tests](../skills/scaffold-agent-tests/SKILL.md) — generates a test suite from an agent implementation plus its contract
- **Terminology authority**: [docs/architecture/terminology.md](../docs/architecture/terminology.md) — the Rule / Spec / Skill boundary
