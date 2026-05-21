---
name: consume-nats-message
description: Drain pending NATS messages from a producer contract via NATS MCP tools (default batch / drain-style). Applies Tolerant Reader semantics and per-message ack/nak/term, returning aggregated stats. Reads project-level cache (.cortex/nats.yaml) to avoid re-prompting.
description_zh: 通过 NATS MCP 工具批量拉取并处理 producer 契约下的待处理消息（默认 drain-style：拉至空或达上限）。逐条按 Tolerant Reader 处理 + ack/nak/term，返回聚合结果。读取项目级缓存 .cortex/nats.yaml 免重复询问。
tags: [nats, messaging, cross-team, consumer, mcp]
version: 1.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [consume nats, subscribe nats, drain nats, 订阅事件, 跨服务收消息, nats consume]
input_schema:
  type: free-form
  description: Producer name + event type (or subject); optional contract path/URL with @version; optional override of consume_defaults (max_messages / batch_size / fetch_timeout)
output_schema:
  type: side-effect
  description: Messages drained and processed via MCP; per-message ack/nak/term applied; aggregated stats reported (counts + failure list + exit reason)
---

# 技能（Skill）：消费 NATS 消息

## 目的（Purpose）

让相互协作的项目能"正确消费消息"——按 producer 契约通过 NATS MCP 工具批量拉取待处理消息，逐条按 Tolerant Reader 处理并正确 ack。默认 **drain-style**：一次调用拉至队列空或达上限，单条失败不阻断整批，最终返回聚合结果。

---

## 核心目标（Core Objective）

**首要目标**：drain producer 契约对应 subject 的待处理消息，每条按 Tolerant Reader 解码 → 业务处理 → 正确 ack / nak / term，输出聚合统计。

**成功标准**：

1. ✅ 项目缓存 `.cortex/nats.yaml` 已读取
2. ✅ producer 契约已定位（本地 vendored 优先）并通过 `contract_version` 兼容性检查
3. ✅ pull consumer 建立 / 复用（durable name 按缓存前缀命名）
4. ✅ 循环 fetch 至 `drained` / `cap_reached` / `idle_timeout` 之一
5. ✅ 每条消息：Tolerant Reader 解码 → 业务处理 → ack 决策正确执行
6. ✅ 单条失败不中断整批，写入失败清单
7. ✅ 返回聚合回执（计数 + 失败详情 + 退出原因 + 续跑建议）

**验收测试**：consumer 处理一批含 1 条新增可选字段的消息时，不抛错并正确 ack；含 1 条业务不可恢复错误的消息时，term + DLQ 投递；含 1 条临时失败的消息时，nak 让 broker 重投。

---

## 范围边界

**本技能负责**：

- 读项目缓存 + 加载 producer 契约
- 通过 NATS MCP 建立 / 复用 JetStream pull consumer
- Drain 循环 + 逐条处理 + 逐条 ack 决策
- Tolerant Reader 解码
- 失败容错（单条不阻断整批）+ DLQ 投递（term 路径）
- 聚合回执

**本技能不负责**：

- 修改 producer 契约 → consumer 不写 producer 文件
- 创建 broker 资源（stream / durable）→ IaC 责任（首次缺则报错指向 IaC owner）
- 实际业务处理逻辑 → consumer repo 自有代码 / handler；本 Skill 仅协调消息与 ack
- 长连续 push 订阅 → 不在 Skill 调用模型中（应用层 worker 职责）

---

## 前置条件

- 已连接 NATS MCP server（提供 `mcp__nats__jetstream_pull_consumer` / `mcp__nats__ack` / `mcp__nats__nak` / `mcp__nats__term` / `mcp__nats__publish` 等工具；具体工具名以连接的 server 为准）
- 当前工作目录是 consumer repo
- producer 契约的冻结快照已 vendor 到 consumer repo（推荐）或可访问的契约路径

---

## 执行流程

### 阶段 0：宣告

> "我正在使用 consume-nats-message 技能 drain 一批待处理消息。"

### 阶段 1：读项目缓存

1. 读 `.cortex/nats.yaml`（consumer repo 根目录）
2. 提取字段：`broker_url` / `service_source` / `durable_name_prefix` / `dlq_handler_dir` / `vendor_contracts_dir` / `consume_defaults`
3. 用户参数可覆盖 `consume_defaults`（`max_messages` / `batch_size` / `fetch_timeout` / `idle_threshold`）
4. 缓存缺失或字段缺 → 引导补齐并提示 commit

### 阶段 2：定位 producer 契约

按优先级：

1. `<vendor_contracts_dir>/<producer>/<event>-contract.md`（冻结快照，含 `@version` 锚定）
2. 用户显式提供的契约路径或 URL（含 `@version`）
3. 都缺 → 提示用户先 vendor 一份冻结快照（违反 [cross-team-contract.md §7 跨 repo 引用约定](../../specs/cross-team-contract.md)），终止

读取契约：

- subject（含 MAJOR 版本段，如 `clarification.session.requested.v1`）
- 必填 headers 清单
- payload 字段表
- QoS / DLQ subject / max_deliver / backoff

### 阶段 3：版本兼容检查

1. 读契约 frontmatter `contract_version`
2. 与 consumer 自身已对齐版本对照（`<vendor_contracts_dir>/<producer>/.lock` 记录 `<contract-name>@<version>`）
3. **不匹配**：提示版本漂移
   - MINOR/PATCH 漂移：Tolerant Reader 通常可兼容，警告后继续
   - MAJOR 漂移（新 subject）：consumer 实际订阅的 subject 已变 → 终止并提示升级 vendor 快照
4. **未记录 .lock**：首次对齐，写入 `.lock` 后继续

### 阶段 4：建立 / 复用 pull consumer

通过 MCP NATS 工具：

- durable name: `<durable_name_prefix>-<event-slug>`
- 若 durable 不存在 → 报错指向 IaC（违反 spec §5.5.2 "不在应用代码运行时建资源"）
- 若存在 → 直接 attach
- ack policy: 契约约定（默认 `explicit`）
- max_deliver: 契约约定

### 阶段 5：Drain 循环

```text
processed = 0
last_non_empty_at = now
while True:
    if processed >= max_messages:
        exit_reason = "cap_reached"; break
    batch = fetch(batch_size, fetch_timeout)
    if batch is empty:
        if now - last_non_empty_at >= idle_threshold:
            exit_reason = "drained"; break
        continue
    last_non_empty_at = now
    for msg in batch:
        try:
            process_one(msg)        # 阶段 6
        except Exception as e:
            record_failure(msg, e)  # 不中断整批
        processed += 1
```

退出原因取值：`drained` / `cap_reached` / `idle_timeout`（连续空 fetch + 未达上限）。

### 阶段 6：逐条处理（Tolerant Reader）

每条消息：

1. **去重**：检查应用层去重集合（按 `Nats-Msg-Id`，TTL ≥ broker `duplicate_window`）；命中 → 直接 ack 跳过
2. **解码 headers**：读必填 headers；缺失 `Nats-Msg-Id` / `X-Source` / `X-Type` → 视为违规消息（业务不可恢复，走 term 路径）；未知 headers 忽略
3. **解码 payload**：
   - 缺失必填字段 → 业务不可恢复 → term + DLQ
   - 未知字段 → 忽略不报错
   - 未知枚举值 → 走 fallback 分支（业务定义）
4. **OTel 接续**：提取 `Traceparent` 继续 span（如适用）
5. **调用业务 handler**：consumer repo 自有处理逻辑；handler 返回结果决定 ack 路径
6. **决策 ack**：进入阶段 7

### 阶段 7：Ack 决策

| 业务结果 | MCP 工具 | 副作用 |
|---|---|---|
| 成功 | `mcp__nats__ack` | broker 确认消费 |
| 可重试错误（网络瞬时 / 下游限流） | `mcp__nats__nak` | broker 按 backoff 重投；最终达 max_deliver 自动 term |
| 不可恢复错误（schema 违规 / 业务永久失败） | `mcp__nats__term` + `mcp__nats__publish` 投 DLQ | 不再重投；原消息复制到 `<original>.dlq` 含失败原因 header |

DLQ 消息 headers 附加：

- `X-DLQ-Original-Subject`：原 subject
- `X-DLQ-Reason`：失败摘要
- `X-DLQ-Failed-At`：ISO 8601 时间戳

### 阶段 8：聚合回执

输出：

```yaml
exit_reason: drained                    # drained / cap_reached / idle_timeout
duration: 12.3s
counts:
  fetched: 87
  acked: 80
  naked: 4
  termed: 3
  dlq_sent: 3
  duplicates_skipped: 1
failures:
  - msg_id: 01HX...A1
    subject: clarification.session.requested.v1
    decision: term
    reason: missing required payload field 'sessionId'
  - msg_id: 01HX...A2
    subject: ...
    decision: nak
    reason: downstream timeout (retry will be attempted)
backlog_hint: |
  exit_reason=drained，无需续跑。
  （若为 cap_reached，建议再次调用本 Skill 续 drain。）
```

---

## 错误处理

| 情况 | 处理 |
|---|---|
| MCP NATS server 未连接 | 提示检查 MCP 配置 |
| `.cortex/nats.yaml` 缺失 | 引导补齐 |
| 契约缺失 / 未 vendor | 终止并提示 vendor 流程 |
| Durable consumer 不存在 | 报错指向 IaC owner（违反 spec §5.5.2） |
| MAJOR 版本漂移 | 终止并提示升级 vendor 快照 |
| 单条解码失败 | term + DLQ + 写入失败清单，**不中断整批** |
| 单条业务可重试失败 | nak，broker 自然重投 |
| Fetch 超时（broker 端无可用消息） | 计入空 fetch 计数，触发 idle_threshold 退出 |

---

## 反模式

- ❌ 单条失败抛错中断整批 —— 必须 try/catch 单条，记入失败清单继续
- ❌ 解码到未知字段抛错 —— Tolerant Reader 要求忽略
- ❌ 处理成功不 ack —— 消息会被 broker 重投，造成幂等假死
- ❌ 业务不可恢复失败用 nak —— 会持续重投直到 max_deliver；应直接 term + DLQ
- ❌ DLQ 投递不带原 headers / 失败原因 —— 失去运营可见性
- ❌ 修改 producer 契约 —— consumer 不写 producer 文件；用 backlog 跟踪升级
- ❌ 持续 push 订阅占据 Skill 调用 —— Skill 是一次性调用，长连续应用层 worker 实现

---

## 与其他资产关系

- **结构契约标尺**：[specs/nats-messaging.md](../../specs/nats-messaging.md)——subject / headers / payload / QoS / Tolerant Reader / DLQ 规则的权威
- **契约文档骨架**：[specs/cross-team-contract.md](../../specs/cross-team-contract.md)——vendor 上游契约时遵循其版本号锚定约定
- **生产侧配套**：[publish-nats-message](../publish-nats-message/SKILL.md)——同一契约的另一端
- **broker 行为权威**：<https://docs.nats.io>——NATS pull consumer / ack policy / Services API 以官方为准
