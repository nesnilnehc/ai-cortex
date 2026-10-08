---
artifact_type: rule
name: standards-test-code
version: 1.1.0
created_by: ai-cortex
lifecycle: living
created_at: 2026-05-26
recommended_scope: user
status: active
---

# Rule: Test Code Standards

## Scope

Every code-level test file in a project (`test_*.py`, `*.spec.ts`, `*_test.go`, `*Test.java`), across all three layers — unit, integration and end-to-end.

Code-level tests have **no separate test case document**; the test function is the artifact. This rule defines coding standards for test code as a code artifact, and applies on top of [standards-coding](./standards-coding.md).

QA business test cases, which are Markdown artifacts, are out of scope here and belong to [specs/test-case-modeling.md](../specs/test-case-modeling.md) plus [rules/test-case-quality.md](./test-case-quality.md).

---

## Constraints

### 1. Structure (Arrange-Act-Assert)

- **One case verifies one explicit objective**: judge responsibility by the behavior being proved, not by line count, invocation count or assertion count. Name the objective and the condition that makes it meaningful
- Keep Arrange, Act and Assert identifiable with blank lines or comments. A multi-step case may interleave actions and intermediate assertions when they establish the same objective; AAA does not require all actions to precede all assertions
- Unit tests usually invoke the behavior once. Necessary repeated invocations are allowed to verify idempotency, retry counts or state transitions; control time and failures explicitly
- Integration and end-to-end tests may perform multiple operations and intermediate assertions when they jointly prove one explicit objective, such as a confirmed operation remaining idempotent after a lost reply and retry
- Assertions must provide evidence for that objective, including relevant outputs, state transitions and externally observable side effects. Several assertions about the same contract are allowed
- Split unrelated objectives and independent scenarios into separate cases. Sharing setup, a subject or a broad name such as "user lifecycle" does not make independent checks one objective
- Do not wrap several operations in a helper merely to make Act look like one call. Helpers may express readable domain steps, but the operations and evidence needed for the objective must remain visible in the case
- Do not replace a causal sequence under verification with pre-seeded state. Fixtures may prepare unrelated preconditions; if the objective concerns how execution, failure and retry interact, exercise that sequence through the actual behavior under test

### 2. Naming

- Test function names follow `test_<subject>_<expected>_when_<condition>` or an equivalent such as `should_<expected>_when_<condition>`
- A name must carry three elements — **subject / expected / condition**. Missing any one fails the check
- Counter-examples: `test_login`, `test1`, `test_user`
- Good examples: `test_returns_401_when_token_expired`, `should_throw_when_amount_negative`

### 3. Isolation

- No shared mutable state: tests do not depend on shared globals, singletons or module-level state
- No dependence on execution order: a case must pass in any order and in any subset
- Each case brings its own setup and teardown, or uses the framework's fixture isolation
- Side effects (writing to a database, a file, a message queue) must be cleaned up in teardown, or contained by a transaction rollback, a temporary directory or an embedded instance

### 4. Determinism

- **No dependence on the clock**: inject a clock or freeze time (`freezegun`, `@MockBean Clock`, `vi.useFakeTimers`)
- **No dependence on randomness**: use a seeded RNG and assert against what that seed produces
- **No dependence on the network**: a real external dependency must be mocked or replaced by a local stand-in — a test container or an embedded instance
- **No dependence on concurrent scheduling**: avoid a bare `sleep`; wait on a condition instead (`await condition`, polling with timeout)
- The same input always gives the same result — `pytest --count=100`, run repeatedly, all green

### 5. Traceability

- A test that verifies a business promise carries a `Covers:` field at the top of its docstring or comment
- Format: `Covers: <REQ-ID>#AC<n>` or `Covers: <REQ-ID>#AC<n>, ADR-<NNNN>`
- For example:

  ```python
  def test_returns_401_when_token_expired():
      """Covers: ACME-REQ-08#AC1."""
      ...
  ```

- A purely functional unit test may omit it (`test_add_two_positives`); any case verifying a business rule, an AC or a contract **must** carry it

### 6. Test real behaviour, not implementation detail

- Assert the public contract — input to output, state transitions, externally observable side effects
- **Never** assert how many times a private method was called, the value of an internal field, or the order of mock calls, unless that order is itself part of the contract
- Refactoring the internals does not turn a case red

### 7. Restraint with mocks

- **Prefer a real dependency**: an embedded database or test container; a local stub server for HTTP
- Mocks are for: external dependencies outside your control (a third-party API), slow or expensive ones (GPU inference), and triggering an error path
- **Never** mock the database ORM layer — the classic anti-pattern where mocks pass and the production migration fails
- Integration tests **must** hit a real database or an equivalent embedded implementation

### 8. Useful failure messages

- The assertion failure message states directly "expected X, got Y, in scenario Z"
- Prefer the framework's diff-carrying assertions (`pytest`'s native assert, `assertEquals` with a message)
- **Never** write `assert True` or `assert result` — they carry no information. Use `assert result == expected`, or add a message

### 9. Performance budget

- A unit test takes ≤ 50ms; the whole suite takes ≤ 5min in CI, and is split into layers beyond that
- Slow cases (integration, E2E) must be isolated behind a tag or marker (`@pytest.mark.slow`, `@Tag("integration")`) so they do not block the daily feedback loop
- A case touching the network, a database or file IO is not a unit test; it belongs to the integration layer

### 10. Cover the boundaries, do not pile up happy paths

- Each AC is covered by at least 1 positive case, 1 boundary case and 1 exception case
- Boundary coverage: empty, zero, negative, upper limit, out of range, concurrent contention, timeout
- One independent case per boundary, not several piled into one function

---

## Good Patterns

These are illustrative pytest-style cases; fixture and API names represent a project's public contract. Fixtures isolate resources and replace external services with local stand-ins, while the production behavior under test runs for real. `Covers:` IDs stand for the corresponding approved acceptance criteria.

```python
def test_retry_policy_stops_when_attempt_limit_reached(retry_policy, dependency):
    """Covers: RETRY-REQ-01#AC1."""
    # Arrange: a controllable external dependency always fails.
    retry_policy.set_attempt_limit(3)  # fixture uses a controlled clock
    dependency.fail_with(TemporaryUnavailable)

    # Act: one public operation triggers the real retry policy.
    with pytest.raises(RetryExhausted):
        retry_policy.run(dependency.request)

    # Assert: attempts at the external boundary are part of the retry contract.
    assert dependency.request_count == 3
```

```python
def test_confirmed_write_occurs_once_when_reply_is_lost_and_request_retried(
    client, external_store, reply_transport
):
    """Covers: WRITE-REQ-01#AC2."""
    # Arrange: isolated storage and deterministic loss after a committed write.
    request = WriteRequest(key="operation-42", value="hello")
    assert external_store.committed_write_count(request.key) == 0

    # Act / Assert: confirmation is the real prerequisite for execution.
    confirmation = client.confirm(request)
    assert confirmation.status == "confirmed"

    # Act / Assert: execute for real, then lose the reply after the write commits.
    reply_transport.drop_next_reply_after_commit()
    with pytest.raises(ReplyLost):
        client.execute(confirmation.id, request)
    assert external_store.committed_write_count(request.key) == 1

    # Act: retry the same confirmed operation with the same idempotency key.
    result = client.execute(confirmation.id, request)

    # Assert: recovery returns the result without another external write.
    assert result.status == "completed"
    assert external_store.read(request.key) == "hello"
    assert external_store.committed_write_count(request.key) == 1
```

The second case has one objective: retrying a confirmed operation after reply loss causes exactly one committed external write. Confirmation and the intermediate assertion establish the causal path. The local store records committed write events, not only the final row count: two overwrites of one row would fail the count assertion. The transport loses the reply only after actual execution commits; it does not fake the execution result. Removing deduplication must make the final write-count assertion fail.

A unit case may likewise call a public operation twice to prove idempotency, or drive a required sequence of state transitions to prove one transition contract. Repetition is evidence when removing a necessary step would stop the case from proving its stated objective.

## Bad Patterns

```python
# ❌ independent creation, deactivation and deletion checks share only a subject;
# no assertion proves a contract connecting these steps
def test_user():
    user = create_user("alice")
    assert user.name == "alice"
    user.deactivate()
    assert not user.active
    user.delete()
    assert User.objects.count() == 0
```

```python
# ❌ depends on the system clock
def test_token_expires():
    token = issue_token(ttl=1)
    time.sleep(2)  # non-deterministic, and slow
    assert not token.is_valid()
```

```python
# ❌ mocking the database: it passes, then the production migration blows up
def test_user_created():
    db = Mock()
    db.insert.return_value = {"id": 1}
    user = UserService(db).create("alice")
    assert user.id == 1  # the real schema was never exercised
```

```python
# ❌ the assertion carries no information
def test_returns_something():
    result = compute(42)
    assert result  # on failure you learn nothing
```

```python
# ❌ a business rule test with no Covers trace
def test_overdraft_blocked():
    # which AC does this test guard? nobody can find out
    account = Account(balance=0)
    with pytest.raises(InsufficientFunds):
        account.withdraw(100)
```

The following shortcuts do not prove the causal objective above:

```python
# ❌ hiding the sequence does not make it a single Act or expose its evidence
def test_confirmed_write_occurs_once_when_reply_is_lost_and_request_retried():
    result = confirm_execute_lose_reply_and_retry()
    assert result.status == "completed"  # no evidence of external write count
```

```python
# ❌ seeding a completed operation bypasses the execution / reply-loss sequence
# This setup can test replay of an existing result, but cannot prove recovery
# after the real first execution commits and its reply is lost.
def test_confirmed_write_occurs_once_when_reply_is_lost_and_request_retried(
    client, external_store, operation_repository
):
    operation_repository.seed_completed(key="operation-42", value="hello")
    result = client.execute("seeded-confirmation", WriteRequest(
        key="operation-42", value="hello"
    ))
    assert result.status == "completed"
    assert external_store.committed_write_count("operation-42") == 0
```

---

## Remediation

1. **Identify the objective and expose AAA**: name the single behavior being proved; make setup, actions and assertions identifiable. Keep necessary repeated calls, causal steps and intermediate assertions together; split independent objectives. Expose operations hidden only to satisfy a line count, and replace seeded state with real execution when that causal path is the objective
2. **Add the three naming elements**: rename to `test_<subject>_<expected>_when_<condition>`
3. **Inject the clock and the randomness**: turn `time.time()` and `random()` into injectable parameters and pass fixed values in tests
4. **Replace the mocked DB**: use SQLite, a test container, or a transaction-rollback fixture
5. **Add the Covers comment**: put `Covers: <REQ-ID>#AC<n>` in the docstring of a business-rule case
6. **Isolate side effects**: use framework fixtures (pytest `tmp_path`, JUnit `@TempDir`) instead of hand-written setup and teardown
7. **Tag the slow cases**: mark integration and E2E, and run them in a separate CI pipeline

---

## Related assets

- **Sibling coding standards**: [standards-coding](./standards-coding.md) for the general case, plus [standards-shell](./standards-shell.md) and [standards-import](./standards-import.md)
- **Business test cases**: [specs/test-case-modeling.md](../specs/test-case-modeling.md) plus [rules/test-case-quality.md](./test-case-quality.md)
- **Source of traceability anchors**: [specs/requirement-modeling.md](../specs/requirement-modeling.md), for the AC ID format
