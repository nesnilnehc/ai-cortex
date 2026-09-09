---
artifact_type: rule
name: standards-test-code
version: 1.0.0
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

- Each test function is organised strictly into the three AAA parts, separated by blank lines where that helps
- **Act is 1 line**: the behaviour under test is invoked once. Several invocations mean the case has more than one responsibility
- **Assertions focus on what that Act produced**: do not mix in extra assertions about other side effects in the same case

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

## Bad Patterns

```python
# ❌ 命名缺三要素 + 一个函数测多件事
def test_user():
    user = create_user("alice")
    assert user.name == "alice"
    user.deactivate()
    assert not user.active
    user.delete()
    assert User.objects.count() == 0
```

```python
# ❌ 依赖系统时钟
def test_token_expires():
    token = issue_token(ttl=1)
    time.sleep(2)  # 不确定，且慢
    assert not token.is_valid()
```

```python
# ❌ Mock 数据库——通过但生产 migration 炸
def test_user_created():
    db = Mock()
    db.insert.return_value = {"id": 1}
    user = UserService(db).create("alice")
    assert user.id == 1  # 没测到真实 schema
```

```python
# ❌ 断言无信息
def test_returns_something():
    result = compute(42)
    assert result  # 失败时什么都不知道
```

```python
# ❌ 业务规则测试缺 Covers 追溯
def test_overdraft_blocked():
    # 这条测试守护哪条 AC？无人能查
    account = Account(balance=0)
    with pytest.raises(InsufficientFunds):
        account.withdraw(100)
```

---

## Remediation

1. **Split into AAA**: give each test function three clear parts; one line of Act; split multiple Acts into multiple tests
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
