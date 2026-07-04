---
id: NATS_MESSAGING_SPEC_V1
name: NATS Messaging Schema
description: Spec defining the structural contract for NATS messages exchanged between independently-evolving projects — subject naming, headers, ID requirements, payload conventions, versioning, with embedded validation rules.
version: 1.1.0
status: active
lifecycle: living
created_at: 2026-05-21
scope: |
  Defines the structural contract for NATS messages exchanged between independently-evolving
  repos / teams / services over a shared broker. Covers subject naming, message ID, header
  conventions, payload shape, version evolution, and embedded behavior rules. Does not apply
  to intra-team messaging within a single release cycle.
related:
  - ./spec-modeling.md
  - ./cross-team-contract.md
---

# NATS 消息规范

> **数据契约**：定义跨项目 NATS 消息的 subject、headers、payload 与版本演化契约

---

## 1. 定位与适用范围

本规范定义跨独立 repo / team / service 通过 NATS 共享 broker 交换的消息应如何组织——subject 怎么命名、headers 必须含哪些字段、消息 ID 怎么发、payload 怎么写、版本怎么演化。

适用：

- 两个或更多独立演进的项目通过 NATS broker 交换消息
- 单一项目对外发布事件让上游/下游团队消费
- 多团队共享 broker、subject 域跨团队治理

不适用：

- 同团队、同发布周期的内部模块间消息（无需跨团队对齐成本）
- broker 自身行为（NATS protocol、JetStream 内部机制——以 <https://docs.nats.io> 为权威）
- 消息生产/消费的代码实现细节（这是应用层职责，本 spec 只规定线上契约）

本 spec 是 [cross-team-contract.md](./cross-team-contract.md) 的 NATS 特化模板——通用契约文档骨架（命名后缀、`contract_version`、CHANGELOG、扁平布局）由 cross-team-contract 承接，本 spec 只补 NATS 特有的 subject/headers/payload 细节。

实际消息收发动作由配套 Skill 通过 NATS MCP server 完成：

- [publish-nats-message](../skills/publish-nats-message/SKILL.md) — 生产侧
- [consume-nats-message](../skills/consume-nats-message/SKILL.md) — 消费侧

---

## 2. 命名约定

### 2.1 Subject 公式

```
<domain>.<event>[.<version>]
```

- **事件中心命名**，不按发起方/团队前缀
- `<domain>`：业务域名（如 `clarification` / `orders` / `inventory`）
- `<event>`：事件类型（动词过去式 / 名词，如 `created` / `session.requested` / `stock.depleted`）
- `<version>`：可选 MAJOR 版本（如 `v1`、`v2`）；MAJOR breaking 时引入新 subject 而非改旧 subject 语义

### 2.2 多租户例外

需要按 producer 做 ACL / retention 分治理（≥3 团队 / 多租户 SaaS）时允许：

```
<tenant>.<domain>.<event>
```

**前提**：前缀语义须在契约的「Subject 命名」节显式声明，不允许隐含推断。

### 2.3 契约文件命名

每个 subject 对应一份契约文件，遵循 [cross-team-contract.md §2](./cross-team-contract.md#2-命名约定) 的 `-contract.md` 后缀：

```
<event>-contract.md
```

例：`clarification-session-requested-contract.md`、`orders-created-contract.md`。

---

## 5. 正文结构契约

跨团队 NATS 消息由三个层次组成：消息 ID（idempotency anchor）、Headers（元信息）、Payload（业务数据）。本节定义每层的结构契约，以及版本演化与内嵌校验规则。

### 5.1 消息 ID 契约

跨团队消息 ID 必须全局唯一，并充当 idempotency key：

| 项 | 约束 |
|---|---|
| ID 格式 | UUID v7（推荐，自带时间序）/ ULID / Snowflake；可加语义前缀（`req-clarify-01HXXX...`） |
| 承载位置 | NATS Header `Nats-Msg-Id`（JetStream 据此做 `duplicate_window` 去重） |
| 续号 | ❌ 严格禁止（`msg-1` / `REQ-001` / `evt-0042`）——分布式竞态 + retention 截断后无法续号 |
| 重试 | 同一逻辑消息重发**必须复用同一 ID**（idempotency 前提） |

Consumer 凭 `Nats-Msg-Id` 做应用层去重（维护 TTL ≥ 重试窗口的已处理 ID 集合）。

### 5.2 Headers 契约

跨团队消息的元信息一律走 NATS Headers，不嵌进 payload JSON envelope。

#### 5.2.1 字段表

| Header | 必填 | 类型 | 说明 |
|---|---|---|---|
| `Nats-Msg-Id` | 必 | string | 消息 ID，UUID v7 / ULID（见 §5.1） |
| `X-Source` | 必 | string | Producer 服务名 / URI（如 `urn:recloud:agentfabric`），描述发起方 |
| `X-Type` | 必 | string | 事件类型字符串，与 subject 末段对齐（如 `clarification.session.requested`） |
| `Traceparent` | 推荐 | string | W3C Trace Context（`00-{traceId}-{spanId}-{flags}`），OTel 标准 |
| `X-Correlation-Id` | 条件必填 | string | 请求-响应 / 多轮会话场景必填，指向原请求的 `Nats-Msg-Id` |
| `X-Schema-Url` | 推荐 | string | payload schema 注册表 URL，consumer 可据此动态校验 |

#### 5.2.2 禁止字段

- ❌ 自创 `in_reply_to` / `messageId` / `correlationid`（混淆 OTel 标准）—— 用 `X-Correlation-Id` + `Traceparent`
- ❌ 把 producer 标识塞进 subject 前缀 —— 用 `X-Source` header
- ❌ JSON envelope 嵌 `id` / `source` / `type` / `time` 字段 —— 这些信息属 headers 层

### 5.3 Payload 约定

#### 5.3.1 序列化

- 必须结构化（JSON / Protobuf / MsgPack），**禁止裸字符串 / 二进制流**（除非走 JetStream Object Store 的对象引用）
- 默认 JSON；其他格式须在契约的「序列化」节显式声明
- 用 **binary mode**：headers 承载元信息，body 承载业务 payload；**不强制** CloudEvents structured mode（NATS Headers 已是更原生的元信息通道）

#### 5.3.2 Tolerant Reader

Consumer 必须：

- 忽略未知字段（向前兼容 producer 新增）
- 忽略未知枚举值并走 fallback 分支（不抛错退出）
- 不依赖字段顺序

#### 5.3.3 业务字段表

每份契约的字段表须含：字段名 / 类型 / 必填性 / 取值约束 / 默认值（如适用）。具体字段由各契约自行定义，本 spec 不规定业务字段。

### 5.4 版本演化

| 变更 | 版本号 | 实现方式 |
|---|---|---|
| MAJOR（breaking） | 新 subject | 引入 `<domain>.<event>.v2` 等新 subject；旧 subject 保留至所有 consumer 切换完毕 |
| MINOR（兼容新增） | `contract_version` MINOR bump | 同一 subject，新增可选字段 / 枚举值；consumer 按 Tolerant Reader 兼容 |
| PATCH（文档修订） | `contract_version` PATCH bump | 注释更正、错别字、示例补充；不影响线上行为 |

`contract_version` 与 CHANGELOG 由 [cross-team-contract.md §4-§5](./cross-team-contract.md#4-frontmatter-契约) 承接，本 spec 不重复定义。

### 5.5 内嵌校验规则

以下行为约束嵌入本 spec（terminology §四允许 Spec 内嵌 Rule）——它们是结构契约成立的前提，不是独立 rule。

#### 5.5.1 QoS 默认

- 跨团队消息**默认 at-least-once**，必须 JetStream durable consumer
- 降级 at-most-once 须在契约的「QoS」节显式声明，并说明可丢失场景
- exactly-once 要求 producer 端 `Nats-Msg-Id` + JetStream `duplicate_window` + consumer 端幂等处理三者齐备

#### 5.5.2 资源治理

- Stream / Consumer / KV / Object Store **由 IaC 管理**（Terraform / NATS Operator / CI 脚本 / GitOps）
- ❌ 应用代码运行时禁止 `streams.add()` / `KV.create()` / `AdminAPI` 操作
- Subject 域归属方负责该域 broker 资源的 IaC，所有权写进契约的「IaC 责任」节

#### 5.5.3 DLQ 与重试

- 跨团队消息的契约**必须显式定义**：
  - DLQ subject（约定 `<original>.dlq`）
  - 最大重试次数（`max_deliver`）
  - 退避算法（exponential / linear / fixed 及参数）
- consumer 处理失败的 ack 决策（`ack` / `nak` / `term`）必须按契约执行

#### 5.5.4 会话与状态

- `sessionId` / `workflowId` / `conversationId` **不是 NATS 原生概念**，是应用层叠加
- 实现方式：subject 内编码（`chat.session.<sid>.message`）+ headers 串联（`X-Correlation-Id`）+ 可选 JetStream KV 存会话状态
- ❌ 不要在契约中表述为 broker 原生能力

#### 5.5.5 服务发现 / 健康 / Schema

- 用 NATS Services API（`$SRV.*`）做服务发现 / 健康检查 / schema 查询
- ❌ 禁止在业务 subject 上自创元协议（如 `<service>.health` / `<service>.schema`）

---

## 6. 反模式

```text
❌ 消息 ID 续号
Nats-Msg-Id: msg-1 / REQ-001 / evt-0042
✅ Nats-Msg-Id: 01HX3W7K9N4PQRSTUVWXYZ0123（ULID）/ UUID v7
```

```text
❌ subject 按发起方前缀
service-zentao.events / team-payments.events
✅ clarification.session.requested / orders.created.v1
```

```text
❌ JSON payload 内嵌 CloudEvents envelope
{ "id": "...", "source": "...", "type": "...", "time": "...", "data": {...} }
✅ 元信息走 headers，payload 只放业务字段
```

```text
❌ 自创追踪字段
{ "in_reply_to": "...", "messageId": "..." }
✅ Header: X-Correlation-Id / Traceparent
```

```text
❌ 应用代码运行时建资源
await jetstreamManager.streams.add({ name: 'EVENTS', subjects: [...] });
✅ IaC（Terraform NATS provider / NATS Operator）声明式管理
```

```text
❌ 表述 sessionId 为 NATS 原生
"NATS 自动按 sessionId 路由"
✅ 应用层：subject 内编码 + X-Correlation-Id 串联 + 可选 KV 存状态
```

```text
❌ 跨团队消息用 Core NATS 不持久化
nc.publish('orders.created', payload);
✅ JetStream + durable consumer + ack policy
```

---

## 7. 示例

### 7.1 契约文件样板

```markdown
---
artifact_type: cross-team-contract
contract_version: 1.0.0
created_at: 2026-05-21
related:
  - ../../specs/nats-messaging.md
  - ../../specs/cross-team-contract.md
---

# clarification.session.requested 契约

## 契约范围

producer：urn:recloud:agentfabric（澄清服务）
consumer：urn:recloud:zentao-bridge（禅道桥接）
subject：`clarification.session.requested.v1`
QoS：at-least-once（JetStream durable consumer `zentao-bridge-clarify`）
IaC 责任：terraform/nats/clarification-stream.tf（agentfabric 团队）

## Headers

| Header | 必填 | 取值 |
|---|---|---|
| Nats-Msg-Id | 必 | UUID v7 |
| X-Source | 必 | urn:recloud:agentfabric |
| X-Type | 必 | clarification.session.requested |
| Traceparent | 推荐 | W3C Trace Context |
| X-Correlation-Id | 条件必填 | 多轮会话时关联首条 Nats-Msg-Id |

## Payload 字段

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| sessionId | string | 必 | ULID，会话标识 |
| feedbackId | string | 必 | 待澄清的反馈 ID |
| question | string | 必 | 澄清问题 |
| context | object | 可选 | 附加上下文 |

## QoS / DLQ / 重试

- max_deliver: 5
- backoff: exponential, base 1s, max 30s
- DLQ subject: clarification.session.requested.v1.dlq

## CHANGELOG

### 1.0.0 — 2026-05-21
**Initial Release**：首版发布。
```

### 7.2 项目级缓存 `.cortex/nats.yaml`

每个使用 NATS 的 repo 在根目录维护一份 `.cortex/nats.yaml`，配套 Skill 启动时直接读取，免重复询问：

```yaml
# 公共字段
broker_url: nats://nats.internal:4222
service_source: urn:recloud:agentfabric          # 本服务 X-Source 标识

# Producer 侧字段
default_stream: AGENTFABRIC_EVENTS                # JetStream stream 名（IaC 管理）
contract_dir: integrations/                       # 契约文件根目录
iac_owner: terraform/nats/                        # IaC 资源声明位置

# Consumer 侧字段
durable_name_prefix: recloud-agentfabric          # durable consumer 命名前缀
dlq_handler_dir: integrations/<producer>/dlq/     # DLQ 处理逻辑位置
vendor_contracts_dir: vendor/contracts/           # vendored 上游契约根目录

# Consumer 默认 drain 参数
consume_defaults:
  max_messages: 200                               # 单次调用最大处理数
  batch_size: 50                                  # 单次 fetch 条数
  fetch_timeout: 5s                               # 单次 fetch 超时
  idle_threshold: 2s                              # 连续空 fetch 阈值（视为 drain 完成）

# Consumer 消费范围（二选一，见下方互斥说明）
consume_subjects:                                 # 默认：显式逐 subject 列表，每个 subject 一个精确 durable
  - clarification.session.requested.v1
consume_pattern: null                             # 可选：wildcard 消费模式，如 zentao.omnireview.>；设置后优先，consume_subjects 被忽略
```

**约定**：

- 首次会话由配套 Skill 引导生成，commit 进 repo
- 后续会话 Skill 启动时直接读，免重复询问基础信息
- 不存在时 Skill 优雅降级：临时问完发送，但提示用户落盘
- `consume_pattern` 与 `consume_subjects` **互斥**：`consume_pattern` 一旦设置即优先生效，`consume_subjects` 被忽略不读——两者同时生效会导致一条消息被 wildcard consumer 和精确 consumer 各自独立收到、各自独立 ack，造成业务侧重复处理
- `consume_pattern` 启用后，只建一个 `<durable_name_prefix>-wildcard` durable，而非逐 subject 各建一个；配套 Skill 对每条消息按其实际 `subject` 动态解析对应契约（命中 `active` 契约才 ack，命中草稿或全新 subject 一律 term + DLQ 标注待确认，不会盲目 ack 未审阅过的消息）
- **已知限制**：JetStream 的 `ack_wait` / `max_deliver` 是 durable 级别配置，不能按 subject 各设各的——`consume_pattern` 模式下所有 subject 共享同一套重试参数，各契约「重试策略」字段在此模式下降级为文档性描述，不再逐 subject 强制生效

---

## 8. 与其他资产关系

- **父规范**：[cross-team-contract.md](./cross-team-contract.md)——通用跨团队契约骨架；本 spec 是其 NATS 特化模板
- **递归基础**：[spec-modeling.md](./spec-modeling.md) v2.0.0——本 spec 自身遵循 8 节骨架
- **配套 Skill**：
  - [publish-nats-message](../skills/publish-nats-message/SKILL.md)——生产侧端到端能力
  - [consume-nats-message](../skills/consume-nats-message/SKILL.md)——消费侧端到端能力（drain-style 批量）
- **broker 行为权威**：<https://docs.nats.io>——NATS protocol / JetStream / Services API 等以官方文档为准，本 spec 不复述
