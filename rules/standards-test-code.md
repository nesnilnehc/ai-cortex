# Rule: 测试代码编码标准 (Test Code Standards)

## 适用范围 (Scope)

所有项目中的代码级测试文件（`test_*.py` / `*.spec.ts` / `*_test.go` / `*Test.java` 等）。覆盖单元测试、集成测试、端到端测试三种分层。

代码级测试**没有独立测试用例文档**——测试函数本身即制品。本规则定义测试代码作为代码制品时的编码标准，与 [standards-coding](./standards-coding.md) 叠加生效。

QA 业务测试用例（markdown 制品）不在本规则范围，归 [specs/test-case-modeling.md](../specs/test-case-modeling.md) + [rules/test-case-quality.md](./test-case-quality.md)。

---

## 强制约束 (Constraints)

### 1. 结构（Arrange-Act-Assert）

- 每个测试函数严格按 AAA 三段组织，必要时用空行分隔
- **Act 只有 1 行**：被测行为只有一次调用；多次调用意味着用例职责不单一
- **断言聚焦该 Act 的产物**：不在同一用例混入对其他副作用的额外断言

### 2. 命名

- 测试函数名遵循 `test_<subject>_<expected>_when_<condition>` 或等价模式（如 `should_<expected>_when_<condition>`）
- 名字必须含三要素：**主体 / 期望 / 条件**；缺任一即不合格
- 反例：`test_login`、`test1`、`test_user`
- 正例：`test_returns_401_when_token_expired`、`should_throw_when_amount_negative`

### 3. 隔离性（Isolation）

- 不共享可变状态：测试间不依赖共享全局变量、单例、模块级状态
- 不依赖执行顺序：用例必须能在任意顺序、任意子集下通过
- 每用例自带 setup / teardown，或使用框架提供的 fixture 隔离机制
- 副作用（写库、写文件、发消息）必须在 teardown 清理或使用事务回滚 / 临时目录 / 嵌入式实例

### 4. 确定性（Determinism）

- **不依赖时钟**：用注入的 clock / 冻结时间（`freezegun` / `@MockBean Clock` / `vi.useFakeTimers` 等）
- **不依赖随机**：用 seeded RNG，断言基于种子产出
- **不依赖网络**：真实外部依赖必须 mock 或用本地替身（test container / 嵌入式实例）
- **不依赖并发调度**：避免裸 `sleep`；用条件等待（`await condition` / polling with timeout）
- 同样输入必然同样结果——`pytest --count=100` / 反复跑全绿

### 5. 追溯（Traceability）

- 验证业务承诺的测试在 docstring / 注释头部标注 `Covers:` 字段
- 格式：`Covers: <REQ-ID>#AC<n>` 或 `Covers: <REQ-ID>#AC<n>, ADR-<NNNN>`
- 例：
  ```python
  def test_returns_401_when_token_expired():
      """Covers: ACME-REQ-08#AC1."""
      ...
  ```
- 纯函数级单元测试可省略（如 `test_add_two_positives`）；任何验证业务规则、AC、契约的用例**必须**标注

### 6. 测真实行为，不测实现细节

- 断言公共契约（输入→输出、状态转移、外部可观察副作用）
- **禁止**断言私有方法被调用次数、内部字段值、mock 调用顺序（除非该调用顺序本身是契约的一部分）
- 重构内部不应让用例红

### 7. Mock 克制原则

- **优先用真实依赖**：数据库用嵌入式 / test container；HTTP 用本地 stub server
- Mock 只用于：外部不可控依赖（第三方 API）、慢/贵的依赖（GPU 推理）、需要触发异常路径
- **禁止** mock 数据库 ORM 层（mock 通过但生产 migration 失败的经典反模式）
- 集成测试**必须**命中真实数据库或等价的嵌入式实现

### 8. 失败信息有用

- 断言失败 message 直接说明"期望 X 实际 Y 在场景 Z"
- 优先用框架自带带 diff 的断言（`pytest` 原生断言、`assertEquals` 带 message）
- **禁止** `assert True` / `assert result`（无信息）；用 `assert result == expected` 或带 message

### 9. 性能预算

- 单元测试单条 ≤ 50ms；测试套件总时长在 CI 上 ≤ 5min（超出则分层）
- 慢用例（集成 / E2E）必须用 tag / marker 隔离（`@pytest.mark.slow` / `@Tag("integration")`），不阻塞日常反馈循环
- 网络 / DB / 文件 IO 类用例不视为单元测试，归集成层

### 10. 覆盖边界，不堆 happy path

- 每个 AC 至少覆盖：正向 1 条 + 边界 1 条 + 异常 1 条
- 边界覆盖：空值 / 零 / 负数 / 上限 / 越界 / 并发竞争 / 超时
- 每个边界一条独立用例，不堆在同一函数里

---

## 违规示例 (Bad Patterns)

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

## 修正指南 (Remediation)

1. **AAA 拆分**：每个测试函数明确分三段；Act 只有一行；多个 Act 拆成多个测试
2. **命名补三要素**：重命名为 `test_<subject>_<expected>_when_<condition>`
3. **注入时钟与随机**：把 `time.time()` / `random()` 改为可注入参数，测试中传入固定值
4. **替换 mock DB**：改用 SQLite / test container / 事务回滚 fixture
5. **补 Covers 注释**：业务规则用例 docstring 加 `Covers: <REQ-ID>#AC<n>`
6. **隔离副作用**：用框架 fixture（pytest `tmp_path` / JUnit `@TempDir`）替代手动 setup/teardown
7. **慢用例打 tag**：集成 / E2E 加 marker，CI 分管道执行

---

## 关联资产

- **同族编码标准**：[standards-coding](./standards-coding.md)（通用）、[standards-shell](./standards-shell.md)、[standards-import](./standards-import.md)
- **业务测试用例**：[specs/test-case-modeling.md](../specs/test-case-modeling.md) + [rules/test-case-quality.md](./test-case-quality.md)
- **追溯锚来源**：[specs/requirement-modeling.md](../specs/requirement-modeling.md)（AC ID 格式）
