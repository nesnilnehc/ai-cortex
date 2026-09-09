---
id: AGENT_TEST_MODELING_SPEC_V1
name: Agent Test Contract Modeling Schema
description: Spec defining the per-agent test contract document — capability boundary, input contract, tool boundary, write-back preconditions, oracles, golden cases, and pass threshold. Governs the contract document; test code conventions are governed by rules/standards-agent-testing.md.
version: 1.0.1
status: active
lifecycle: living
created_at: 2026-05-29
scope: |
  Defines the structural contract for a single LLM Agent's test contract document —
  the noun that declares what the agent must accept, must reject, how correctness is
  judged, and which upstream promise it guards. Does NOT cover test code conventions
  (assertion style, mocking, regression gates) — those are governed by
  rules/standards-agent-testing.md. Does NOT cover QA business test cases (governed by
  test-case-modeling.md) or code-level test coding (governed by standards-test-code.md).
related:
  - ./spec-modeling.md
  - ./test-case-modeling.md
  - ../rules/standards-agent-testing.md
  - ../rules/standards-test-code.md
---

# Agent Test Contract Schema

> **Data contract**: defines the field structure and body skeleton of the test contract document for a single LLM agent

---

## 1. Position and scope

An agent test contract answers what this agent must accept, what it must reject, what counts as correct, and which promise it guards. It is the verifiable behavioural contract for a single LLM agent, and the source that assertions in test code trace back to.

In scope:

- The test contract of an LLM agent that offers a capability externally, such as a requirement clarification agent or a code review agent

Out of scope:

- **How test code is written** — assertion oracles, mock isolation, regression gates — which belongs to [rules/standards-agent-testing.md](../rules/standards-agent-testing.md)
- **QA business test case documents**, which belong to [test-case-modeling.md](./test-case-modeling.md)
- **Code-level test coding standards**, which belong to [standards-test-code.md](../rules/standards-test-code.md)

Where these documents live is decided by each project's governance; typically `docs/agent-tests/` or the directory holding the agent implementation.

---

## 2. Mental model

> The core questions a sound agent test contract answers.

Every contract must be able to answer **3 questions plus 1 anchor**:

| Dimension | Core question | Section |
|---|---|---|
| **Input contract (Accept)** | What must the agent accept? How does it recognise a missing field? | §5 Input contract |
| **Behavioural boundary (Reject)** | What must the agent reject? Which tools may it call, and which are forbidden? | §5 Tool boundary and write-back preconditions |
| **Judgement (Judge)** | What counts as correct? Which oracle, at what threshold? | §5 Oracles and golden cases |
| **Traceability anchor (Trace)** | Which business promise does it guard? | `covers` |

Missing any one makes the contract unsound: the test code has no way to locate why an assertion is written the way it is.

---

## 3. Naming

```text
agent-test-<agent-slug>.md
```

- `<agent-slug>`: the agent identifier in kebab-case, aligned with the agent implementation's name, such as `clarification` or `code-review`
- Example: `agent-test-clarification.md`
- The contract ID in the frontmatter `id` follows `ATC-<AGENT>` in upper case, such as `ATC-CLARIFICATION`

---

## 4. Frontmatter contract

```yaml
---
id: ATC-<AGENT>
artifact_type: agent-test-contract
lifecycle: living
created_at: YYYY-MM-DD
status: draft | active | deprecated
agent_ref: <relative path to the agent implementation>
model_baseline: <model id and version the golden set was recorded against>
pass_threshold: <golden set pass rate threshold, for example 0.9>
covers:
  - <requirement-id>#<AC-n>
parent: <path to the upstream requirement or design document>
# conditional fields
deprecated_at: YYYY-MM-DD          # required when status is deprecated
deprecated_reason: <reason>         # required when status is deprecated
---
```

### 4.1 Field table

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Follows `ATC-<AGENT>` |
| `artifact_type` | string | yes | Fixed as `agent-test-contract` |
| `lifecycle` | enum | yes | Fixed as `living` — the contract evolves with the agent's capability |
| `created_at` | date | yes | The date the contract landed |
| `status` | enum | yes | `draft` / `active` / `deprecated`; semantics in §4.2 |
| `agent_ref` | path | yes | Relative path to the agent implementation under test |
| `model_baseline` | string | yes | The model id and version the golden set was recorded against, as the regression comparison baseline |
| `pass_threshold` | number | yes | The golden set pass rate threshold, 0–1 |
| `covers` | list[string] | yes | The list of traceability anchors pointing at upstream ACs; **never empty** |
| `parent` | path | yes | Path to the upstream requirement or design document |
| `deprecated_at` | date | conditional | Required when `status: deprecated` |
| `deprecated_reason` | string | conditional | Required when `status: deprecated` |

### 4.2 State machine semantics

| Status | Meaning | Entry condition |
|---|---|---|
| `draft` | Being drafted | The contract has just landed and the golden set is not yet stable |
| `active` | In force | The golden set is stable and the regression gate is wired up |
| `deprecated` | Retired | The agent was decommissioned or its capability merged; `deprecated_at` and `deprecated_reason` must be filled in |

---

## 5. Body structure contract

### 5.1 The 7 required sections

**H1 title**: `# Agent test contract: <agent name>`

| # | Section | Purpose | Validation |
|---|---|---|---|
| 1 | Capability boundary | What the agent does and does not do | As a list; at least 1 item on each side |
| 2 | Input contract | Required input fields, and how a missing field is recognised | Each field carries name, type, whether it is required, and the expected behaviour when absent |
| 3 | Tool call boundary | The allowed and forbidden tool sets | Both sets listed explicitly; where the forbidden set is non-empty, each entry carries its reason |
| 4 | Write-back preconditions | What must hold before a side effect occurs | Each independently verifiable; an agent with no side effects writes "no write-back" |
| 5 | Oracles | Which oracle each kind of behaviour uses | Each kind maps to an oracle type in [standards-agent-testing §2](../rules/standards-agent-testing.md) |
| 6 | Golden cases | An input-to-expectation table | Each row carries input, expectation, oracle and Covers; at least 1 each of positive, boundary and exception |
| 7 | Pass threshold and coverage | The golden pass rate threshold and the business promises guarded | The threshold matches the frontmatter `pass_threshold`; the text each `covers` entry cites can be located |

### 5.2 Golden cases table format

```markdown
| Case | Input | Expected (output / trajectory) | Oracle | Covers |
| :--- | :--- | :--- | :--- | :--- |
```

- The oracle column takes `contract` / `trajectory` / `rubric` / `field` / `semantic` / `statistical`, corresponding to the oracle types in standards-agent-testing §2

### 5.3 Validation is centralised

Structural validation for every body section lives in §5. The anti-patterns in §6 only name the violating shapes; they do not restate the rules.

---

## 6. Anti-patterns

- ❌ A missing required frontmatter field (`id` / `agent_ref` / `model_baseline` / `pass_threshold` / `covers`)
- ❌ `covers` empty or set to `TBD`; no anchor means the assertions have no source
- ❌ A tool boundary listing only the allowed set, leaving no way to verify that a forbidden call did not occur
- ❌ Golden cases piled up on positive paths, with no boundary or exception cases
- ❌ An oracle written as a vague phrase such as "check the result is normal", rather than mapping to a concrete oracle type
- ❌ `pass_threshold` disagreeing with the threshold in §7 of the body
- ❌ Stuffing the assertion style of test code into the contract; how code is written belongs to [standards-agent-testing](../rules/standards-agent-testing.md)
- ❌ One contract covering several agents; it is one contract per agent
- ❌ A `deprecated` status with no `deprecated_at` or `deprecated_reason`

---

## 7. Examples

````markdown
---
id: ATC-CLARIFICATION
artifact_type: agent-test-contract
lifecycle: living
created_at: 2026-05-29
status: active
agent_ref: ../src/agents/clarification.py
model_baseline: claude-sonnet-4-6
pass_threshold: 0.9
covers:
  - ACME-REQ-08#AC1
  - ACME-REQ-08#AC3
parent: ../requirements/ACME-REQ-08.md
---

# Agent test contract: requirement clarification

## Capability boundary

- Does: identify the elements of a requirement from free text, and follow up on missing fields through the flow
- Does not: write back to the requirement system when information is insufficient — that is forbidden

## Input contract

| Field | Type | Required | Expected behaviour when missing |
|---|---|---|---|
| title | string | Yes | Ask for the title; do not write back |
| acceptance | list | Yes | Ask for the acceptance criteria; do not write back |

## Tool call boundary

- Allowed: `search_requirements`, `ask_user`
- Forbidden: `write_requirement` while the write-back precondition is unmet — this keeps insufficient information out of the store

## Write-back preconditions

- Every required field has been collected and passes the completeness check

## Oracles

| Behaviour | Oracle type |
|---|---|
| Recognising a missing field | trajectory (assert ask_user fired and write_requirement did not) |
| Writing back a complete requirement | contract (the write-back payload schema is valid) |
| Quality of the follow-up wording | rubric (clarity score ≥ 4/5) |

## Golden Cases

| Case | Input | Expected (output / trajectory) | Oracle | Covers |
| :--- | :--- | :--- | :--- | :--- |
| Missing acceptance criteria | "build me a login feature" | ask_user fires asking for acceptance; write_requirement does not fire | trajectory | ACME-REQ-08#AC1 |
| Complete information | a description carrying a title plus 3 acceptance criteria | write_requirement fires with a valid payload schema | contract | ACME-REQ-08#AC3 |
| Empty input | "" | returns a guiding prompt; fires no tool at all | trajectory | ACME-REQ-08#AC1 |

## Pass threshold and coverage

- Golden suite pass rate ≥ 0.9, matching `pass_threshold`
- **ACME-REQ-08 AC#1**: writing back is forbidden when information is insufficient
- **ACME-REQ-08 AC#3**: a complete requirement writes back a valid payload
````

---

## 8. Relationship to other assets

- **Paired rule**: [rules/standards-agent-testing.md](../rules/standards-agent-testing.md) — the red lines and methodology for agent test code: assertion oracles, isolation, regression gates. This spec defines the contract structure only; how code is written belongs to the rule.
- **Execution capability**: [skills/scaffold-agent-tests](../skills/scaffold-agent-tests/SKILL.md) — reads a contract instance of this spec plus the agent implementation and generates a test suite.
- **Sibling spec**: [test-case-modeling.md](./test-case-modeling.md) — QA business test case documents. **They do not overlap**: this spec governs one agent's behavioural contract, that one governs black-box business cases.
- **Upstream spec**: [requirement-modeling.md](./requirement-modeling.md) — `covers` cites requirement AC IDs.
- **Recursive basis**: this spec itself follows the 8-section skeleton of [spec-modeling.md](./spec-modeling.md) v2.0.0.
