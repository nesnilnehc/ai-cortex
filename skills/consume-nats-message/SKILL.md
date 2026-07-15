---
name: consume-nats-message
description: Drain pending NATS messages from a producer contract via NATS MCP tools. Discovers the available NATS tool capabilities, selects exact-subject or wildcard mode from .cortex/nats.yaml, applies Tolerant Reader semantics, executes ack/nak/term decisions, and returns aggregated stats.
description_zh: 通过 NATS MCP 工具批量拉取 producer 契约下的待处理消息。先发现并映射可用 NATS 工具能力，再根据 .cortex/nats.yaml 选择精确 subject 或 wildcard 模式，按 Tolerant Reader 处理并执行 ack/nak/term，最终返回聚合统计。
tags: [nats, messaging, cross-team, consumer, mcp]
version: 1.4.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [consume nats, subscribe nats, drain nats, 订阅事件, 跨服务收消息, nats consume]
input_schema:
  type: free-form
  description: Producer name + event type or subject; optional contract path with @version; optional consume override max_messages / batch_size / fetch_timeout / idle_threshold
output_schema:
  type: side-effect
  description: Pending messages drained via MCP; each message acked/naked/termed or isolated for contract confirmation; aggregated counts, failures, awaiting_confirmation, and exit reason reported
---

# 技能：消费 NATS 消息

## 目的

在 consumer 仓库中执行一次有限的 NATS JetStream pull-consume：读取本地配置和 producer 契约，拉取待处理消息，逐条按 Tolerant Reader 解析并调用业务 handler，然后执行正确的 `ack` / `nak` / `term + DLQ` 决策。

默认是 **drain-style**：持续 fetch，直到队列被 drain、达到消息上限，或连续空 fetch 达到 idle 阈值。

---

## 权威引用

本 Skill 只负责单次消费动作的编排，不重新定义 NATS 契约规则。

| 内容 | 权威来源 |
|---|---|
| subject / headers / payload / Tolerant Reader / DLQ / IaC 边界 | [specs/nats-messaging.md](../../specs/nats-messaging.md) |
| `contract_version` / CHANGELOG / `*-contract.md` 结构 | [specs/cross-team-contract.md](../../specs/cross-team-contract.md) |
| Skill / Spec / Protocol / Rule 边界 | [docs/architecture/terminology.md](../../docs/architecture/terminology.md) |
| 外部链接与 raw content 策略 | [AGENTS.md](../../AGENTS.md) |

若本 Skill 与上述资产冲突，按 `AGENTS.md > specs/ > protocols/ > rules/ > docs/` 的仓库权威顺序处理；Skill 正文只保留执行编排说明。

---

## 前置条件

- 当前工作目录是 consumer repo。
- consumer repo 含 `.cortex/nats.yaml`，或用户允许本次交互补齐临时配置。
- 已连接某个 NATS MCP server。工具名不要求固定，但必须能映射出 fetch / ack / nak / term / publish-DLQ 等能力。
- producer 契约优先来自本地 vendored 快照；只有当前上下文显式允许外部抓取时，才可读取外部 HTTP/HTTPS 契约或官方文档。

---

## 输入

用户可以提供以下任意组合：

- `producer`：producer 名称或服务来源。
- `event`：事件名。
- `subject`：明确的 NATS subject。
- `contract_path`：本地契约路径，建议包含 `@version` 语义。
- `max_messages` / `batch_size` / `fetch_timeout` / `idle_threshold`：覆盖 `.cortex/nats.yaml` 中的默认值。

缺少 producer / event / subject 时，先从 `.cortex/nats.yaml` 和 vendored 契约推断；仍不能唯一确定时再询问用户。

---

## 行为

### 0. 宣告

向用户说明：

> 我正在使用 consume-nats-message 技能 drain 一批待处理消息。

### 1. 读取本地上下文

1. 读取 `.cortex/nats.yaml`。
2. 提取：
   - `broker_url`
   - `service_source`
   - `durable_name_prefix`
   - `dlq_handler_dir`
   - `vendor_contracts_dir`
   - `consume_defaults`
   - `consume_subjects`（可选）
   - `consume_pattern`（可选）
3. 用用户显式参数覆盖 `consume_defaults`。
4. 若配置缺失，询问最少必要字段，并提示用户后续把配置 commit 进 repo。

### 2. 发现并映射 NATS MCP 工具

不要假设 MCP 工具名固定。先检查当前运行时暴露的 NATS 相关工具，并建立能力映射：

| 能力 | 用途 | 缺失时处理 |
|---|---|---|
| `list_streams_or_subjects` | Bootstrap 时列举 broker 拓扑 | Bootstrap 不可执行，停止并说明缺失能力 |
| `peek_message` | Bootstrap 只读样本，不 ack、不移动 durable offset | 契约缺失时停止，不能进入正式 drain |
| `attach_or_pull_consumer` | 复用既有 durable 并 fetch batch | 停止并提示检查 MCP 配置 |
| `ack` | 成功或重复消息确认 | 停止；不能安全消费 |
| `nak` | 可重试失败重投 | 停止；不能安全消费 |
| `term` | 不可恢复失败停止重投 | 停止；不能安全隔离失败消息 |
| `publish` | 发送 DLQ 副本 | term 路径不可用，停止或按用户确认降级为只 term |

若工具名与示例名不同，按能力而不是名称调用。若没有工具发现能力，则根据当前工具列表人工匹配；无法确认时停止并询问用户配置。

### 3. 选择消费模式

| 条件 | 模式 | 行为 |
|---|---|---|
| `.cortex/nats.yaml` 设置了 `consume_pattern` | wildcard | 建一个 `<durable_name_prefix>-wildcard` durable，按每条消息的实际 `subject` 动态匹配契约 |
| 未设置 `consume_pattern`，但有 `subject` / `producer + event` / `consume_subjects` | exact-subject | 每个 subject 复用一个精确 durable |
| 两者都不足以确定 | discovery | 列出本地契约和可见 subject，让用户选择 |

`consume_pattern` 与 `consume_subjects` 互斥；`consume_pattern` 一旦存在，本次调用必须忽略 `consume_subjects`，避免同一消息被多个 durable 独立处理。

### 4. 定位或引导契约

#### exact-subject 模式

按顺序定位契约：

1. `<vendor_contracts_dir>/<producer>/<event>-contract.md`
2. 用户提供的本地 `contract_path`
3. `.cortex/nats.yaml` 或 `consume_subjects` 指向的本地契约
4. 仍缺失时进入 Bootstrap

读取契约 frontmatter 和正文，至少提取 `contract_version`、`status`、`subject`、必填 headers、payload 字段、DLQ subject、`max_deliver`、backoff。字段语义以 `specs/nats-messaging.md` 和契约自身为准。

#### wildcard 模式

建 consumer 前不预先锁定单份契约。每条消息到达后，**先做两项前置过滤**，命中任一项都直接 `ack` 并跳过契约解析、去重、解码、业务 handler（步骤 2-7），两项都未命中才继续往下走：

1. **自产消息**：`headers['X-Source']` 存在且等于 `service_source`（即消息就是本服务自己发出的）→ 直接 `ack`，不解析契约、不生成草稿、不进业务 handler。

   原因：wildcard subject pattern 只按前缀匹配，不携带方向信息。当 producer/consumer 共用同一命名前缀（如双方约定 `zentao.omnireview.>` 承载两个方向的事件）时，本服务发给对方的出站消息也会匹配自己的 wildcard filter 被重新投递回来。这不是"未知契约"，是回声，照 unknown-subject 流程走会为自己的消息生成多余的草稿契约文件。

   `X-Source` 缺失时**不**判定为自产消息（不与 `undefined`/`None` 做相等比较）——直接放行进入下一项过滤和正式契约解析；真正缺失该必填 header 的消息会在步骤 3「解码 headers」被判为不可恢复，走 `term + DLQ`，而不是被这条前置过滤悄悄吞掉或让读取本身报错中断整批。

2. **DLQ 副本自我回环**：消息携带 `X-DLQ-Original-Subject` header（即消息本身就是本服务此前 `publish` 的 DLQ 副本，见"10. Ack 决策"的 DLQ 副本必带 header 列表）→ 直接 `ack`，不解析契约。

   原因：`term + publish DLQ` 产生的副本 subject 落在 `<original-subject>.dlq`，同样匹配 wildcard 前缀，会被同一个 wildcard consumer 再次收到。DLQ 副本是失败归档的终点，不是待处理的业务事件，不需要、也不应该再触发一轮契约解析或二次 DLQ。用 `X-DLQ-Original-Subject` 这一自产 header 判定，而不是裸 `.dlq` 后缀字符串匹配——后者会把恰好以 `.dlq` 结尾的正常业务 subject 误判为回环，静默丢弃真实业务消息。

两项前置过滤都未命中时，用 `msg.subject` 精确匹配 `<vendor_contracts_dir>/<producer>/*.md` 中 frontmatter 的 `subject:`：

- 命中 `status: active`：进入正常处理。
- 命中 `status: draft`：不进入业务 handler，走 awaiting-confirmation。
- 未命中：为该 subject 生成 N=1 draft 契约，然后走 awaiting-confirmation。

### 5. Bootstrap 契约草稿

仅在契约缺失时执行。Bootstrap 是只读探查阶段：

- 不 ack。
- 不 nak。
- 不 term。
- 不创建或推进正式 durable offset。
- 不修改 producer 权威契约。

步骤：

1. 用 NATS MCP 的拓扑/peek 能力列出 stream / subject / 消息计数。
2. 选择目标 subject；若无法唯一确定，询问用户。
3. peek 最近 N 条样本，默认 N=5；wildcard 未命中时 N=1。
4. 推断 headers 和 payload 字段：
   - N>1 时，出现率 100% 可标为必填，低于 100% 标为可选。
   - N=1 时，不得把出现字段自动判为必填，必填性统一标为 `待确认`。
   - QoS / max_deliver / DLQ 无法可靠推断，标为 `TBD`。
5. 写入本地 draft 契约：`<vendor_contracts_dir>/<producer>/<event>-contract.md`。
6. frontmatter 必含：

```yaml
contract_version: 0.1.0
status: draft
inferred_from: bootstrap-peek
inferred_at: <ISO 8601>
inferred_sample_size: <N>
inferred_sample_seq_range: <first>-<last>
authoritative: false
```

Bootstrap 后的分支：

| 场景 | 默认处理 |
|---|---|
| exact-subject 模式新建 draft | 展示草稿摘要并询问用户是否继续正式 drain；默认不继续 |
| wildcard 模式遇到未知 subject | 生成 draft 后直接 `term + DLQ` 当前消息，标注 `awaiting contract confirmation`，不中断整批 |
| wildcard 模式命中 draft | 直接 `term + DLQ` 当前消息，标注 `awaiting contract confirmation`，不中断整批 |

只有用户明确确认“按 draft 继续正式 drain”时，exact-subject 模式才可在 draft 契约下进入正式处理；否则停止，等待 producer owner 确认契约。

### 6. 版本与状态检查

exact-subject 模式：

1. 读取契约 `contract_version` 和 `<vendor_contracts_dir>/<producer>/.lock`。
2. `.lock` 缺失时写入当前 `<contract-name>@<version>`，视为首次对齐。
3. MINOR / PATCH 漂移：提示风险后继续。
4. MAJOR 漂移或 subject breaking 变更：停止，提示升级 vendored 契约。
5. `status: draft`：必须先获得用户确认，才能正式 ack 消息。

wildcard 模式：

- 不做逐条 SemVer 漂移检查。
- 只允许 `status: active` 的契约进入业务 handler。
- `draft` 或未知契约一律进入 awaiting-confirmation 路径。

### 7. 建立或复用 pull consumer

遵守 `specs/nats-messaging.md` 的 IaC 边界：Skill 不创建 stream 或 durable 资源。

exact-subject 模式：

- durable name: `<durable_name_prefix>-<event-slug>`
- filter subject: 契约 subject
- durable 不存在时停止，并指向 IaC owner

wildcard 模式：

- durable name: `<durable_name_prefix>-wildcard`
- filter subject: `consume_pattern`
- ack policy: `explicit`
- `ack_wait` / `max_deliver` 使用 durable 级默认值；不能按 subject 单独强制
- durable 不存在时停止，并指向 IaC owner

### 8. Drain 循环

```text
processed = 0
last_non_empty_at = now

while processed < max_messages:
    batch = fetch(batch_size, fetch_timeout)
    if batch is empty:
        if now - last_non_empty_at >= idle_threshold:
            exit_reason = "drained"
            break
        continue

    last_non_empty_at = now
    for msg in batch:
        try:
            consume_one(msg)
        except Exception as error:
            record_failure(msg, error)
        processed += 1

if processed >= max_messages:
    exit_reason = "cap_reached"
```

若 fetch 工具区分 broker timeout 和空 batch，broker timeout 计为空 fetch；不要把它当成单条消息失败。

### 9. 逐条消费

对每条消息按顺序执行：

1. **wildcard 契约门禁**：若当前模式是 wildcard，先做自产消息 / DLQ 回环前置过滤（见"定位或引导契约 > wildcard 模式"）；命中任一项，直接 `ack`，不进入步骤 2-7。均未命中时，再按 `msg.subject` 定位 active 契约；未知或 draft 走 awaiting-confirmation，同样不进入后续步骤。
2. **去重**：按 `Nats-Msg-Id` 查询应用层去重集合；命中则 `ack` 并计入 `duplicates_skipped`。
3. **解码 headers**：缺失 `Nats-Msg-Id` / `X-Source` / `X-Type` 或契约必填 header 时，判为不可恢复。
4. **解码 payload**：缺失必填字段判为不可恢复；未知字段忽略；未知枚举走业务 fallback。
5. **接续 Traceparent**：若存在且 consumer 支持 OTel，则延续 span。
6. **调用业务 handler**：只调用 consumer repo 自有 handler；本 Skill 不实现业务逻辑。
7. **执行 ack 决策**。

### 10. Ack 决策

| 结果 | 动作 |
|---|---|
| 成功 | `ack` |
| 重复消息 | `ack` |
| wildcard 自产消息回声 | `ack`，不解析契约、不进业务 handler |
| wildcard DLQ 副本回环 | `ack`，不解析契约 |
| 可重试失败，如网络瞬断、下游限流 | `nak` |
| schema 违规或业务永久失败 | `term` 原消息，并 `publish` 副本到 DLQ |
| wildcard 未知或 draft 契约 | `term` 原消息，并 `publish` 副本到 `<subject>.dlq`，`X-DLQ-Reason` 以 `awaiting contract confirmation` 开头 |

DLQ 副本至少附加：

- `X-DLQ-Original-Subject`
- `X-DLQ-Reason`
- `X-DLQ-Failed-At`
- 原始 headers（能保留则保留）

---

## 输出

输出聚合回执，不输出完整消息体，避免泄露 payload。

```yaml
exit_reason: drained
duration: 12.3s
counts:
  fetched: 87
  acked: 80
  naked: 4
  termed: 3
  dlq_sent: 3
  duplicates_skipped: 1
  self_sourced_skipped: 0
  dlq_echo_skipped: 0
failures:
  - msg_id: 01HX...A1
    subject: clarification.session.requested.v1
    decision: term
    reason: missing required payload field 'sessionId'
awaiting_confirmation:
  - subject: zentao.omnireview.some_new_event
    contract_path: .cortex/vendor-contracts/recloud-zentao/some-new-event-contract.md
    reason: newly bootstrapped draft, needs producer confirmation
backlog_hint: |
  exit_reason=drained，无需续跑。
  若 exit_reason=cap_reached，建议再次调用本 Skill 续 drain。
  若 awaiting_confirmation 非空，请先确认契约，再续跑。
```

`awaiting_confirmation` 仅在 wildcard 模式或 Bootstrap draft 未确认时出现。

---

## 错误处理

| 情况 | 处理 |
|---|---|
| NATS MCP server 未连接 | 停止并提示检查 MCP 配置 |
| 必需 MCP 能力缺失 | 停止并列出缺失能力 |
| `.cortex/nats.yaml` 缺失 | 询问最少必要字段，并提示落盘 |
| 契约缺失 | 进入 Bootstrap，不直接终止 |
| Bootstrap 缺少 peek 能力 | 停止，不能安全推断契约 |
| 用户未确认 exact-subject draft | 草稿落盘后停止，不 ack |
| durable 不存在 | 停止并指向 IaC owner |
| MAJOR 版本漂移 | 停止并提示升级 vendored 契约 |
| 单条解码失败 | `term + DLQ`，记录失败，继续整批 |
| 单条可重试失败 | `nak`，记录失败，继续整批 |
| fetch 连续为空 | 达到 `idle_threshold` 后以 `drained` 退出 |
| wildcard 命中未知或 draft 契约 | `term + DLQ`，记录 `awaiting_confirmation`，继续整批 |

---

## 反模式

- 单条失败抛错中断整批。
- 解码到未知字段就失败；Tolerant Reader 必须忽略未知字段。
- 业务成功后不 ack。
- 不可恢复失败用 nak 导致反复重投。
- DLQ 不带原 subject、失败原因和时间戳。
- Skill 运行时创建 stream / durable 等 broker 资源。
- 契约缺失时直接进入正式 ack。
- Bootstrap peek 阶段 ack / nak / term。
- wildcard 模式下对未知或 draft 契约消息直接 ack。
- wildcard 模式下把自产消息（`X-Source == service_source`）或携带 `X-DLQ-Original-Subject` 的 DLQ 回环消息当成未知契约，触发 Bootstrap 生成多余草稿。
- 用裸 `.dlq` 后缀字符串匹配判定 DLQ 回环，误吞真实以 `.dlq` 结尾的业务 subject。
- 把缺失的 `X-Source` header 当成等于 `service_source`，误判为自产消息静默 ack。
- 同时启用 `consume_pattern` 与 `consume_subjects`。
- 默认抓取外部 HTTP/HTTPS 契约或 raw URL。

---

## 自检

- [ ] 已读取 `.cortex/nats.yaml`，或已明确说明缺失字段。
- [ ] 已完成 NATS MCP 工具能力映射，且未硬编码不存在的工具名。
- [ ] 已选择 exact-subject / wildcard / discovery 模式。
- [ ] 已按本地 vendored 契约优先定位契约。
- [ ] Bootstrap 阶段未 ack、未 nak、未 term、未推进正式 durable offset。
- [ ] draft 契约在 exact-subject 模式下获得用户确认后才正式 ack。
- [ ] wildcard 模式只让 active 契约进入业务 handler。
- [ ] wildcard 自产消息 / DLQ 回环前置过滤已生效；`X-Source` 缺失未被误判为自产消息，DLQ 回环靠 `X-DLQ-Original-Subject` 而非裸 `.dlq` 后缀判定。
- [ ] 单条失败不会中断整批。
- [ ] 输出包含 counts、failures、exit_reason；必要时包含 awaiting_confirmation。
- [ ] 未默认抓取外部 HTTP/HTTPS 链接。

---

## 示例

### 示例 1：精确 subject drain

输入：

```text
consume nats producer=agentfabric event=clarification.session.requested max_messages=100
```

预期：

1. 读取 `.cortex/nats.yaml`。
2. 映射 NATS MCP fetch / ack / nak / term / publish 能力。
3. 定位 `clarification-session-requested-contract.md`。
4. 复用 `<durable_name_prefix>-clarification-session-requested`。
5. drain 至 `drained` 或 `cap_reached`。
6. 返回聚合回执。

### 示例 2：wildcard 遇到新 subject

配置：

```yaml
consume_pattern: zentao.omnireview.>
consume_subjects:
  - zentao.omnireview.task.updated.v1
```

预期：

1. 忽略 `consume_subjects`，只使用 `<durable_name_prefix>-wildcard`。
2. 收到 `zentao.omnireview.some_new_event.v1`。
3. 本地未命中 active 契约，生成 N=1 draft，字段必填性标为 `待确认`。
4. 当前消息 `term + DLQ`，原因以 `awaiting contract confirmation` 开头。
5. 继续处理同批其他消息，最终在 `awaiting_confirmation` 中列出该 subject。
