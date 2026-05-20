---
id: EDI_PROTOCOL_V1
name: Event-Driven Integration Protocol
description: Contract-first publish/consume/evolution/DLQ flow for async messaging between independent teams and services
version: 1.0.0
status: active
lifecycle: living
created_at: 2026-05-20
scope: >
  Applicable when two or more independently-evolving teams/services exchange messages
  over a shared broker (NATS, Kafka, Pulsar, RabbitMQ, etc.). Covers the full
  lifecycle: contract definition, subject naming, QoS selection, resource governance,
  failure handling, and schema evolution.
related:
  - ../specs/event-message-envelope.md
---

# 事件驱动集成协议（EDI）

> **流程层**：定义"如何"进行合规的跨团队事件驱动集成
>
> 与 [EME](../specs/event-message-envelope.md) 配套：EME 定义消息 envelope 的"是什么"（字段结构与校验规则）

---

## 参与方

| 角色 | 职责 |
|:---|:---|
| **Producer**（事件发布方） | 维护 subject 域契约，发布合规 envelope，IaC 治理所属资源 |
| **Consumer**（事件消费方） | 自主决定升级时机，实现 Tolerant Reader，维护去重与重试逻辑 |
| **契约评审方** | Producer + Consumer 共同 review 契约 schema，签字后正式发布 |
| **IaC Owner** | 负责 broker 资源（stream / topic / DLQ）的声明式管理 |

---

## 1. Contract-First：开工前必备书面契约

跨团队消息流开始**之前**，必须存在书面契约：

1. **选择机器可读格式**：AsyncAPI spec、Protobuf `.proto`、JSON Schema、Avro schema 之一
2. **存放位置**：Provider 仓库的 `*-contract.yaml`（或 `*-contract.md`），遵循 `standards-cross-team-contracts` 规则
3. **契约内容须定义**：
   - subject / topic 命名
   - payload schema（含必填字段与类型）
   - 版本演化策略（SemVer + CHANGELOG）
   - QoS 级别与 DLQ 策略
4. **双方 review + sign**：Consumer 确认可消费后，契约正式生效

**禁止**：
- ❌ 靠 `grep` 历史消息推断对方约定（应急手段，不可常态化）
- ❌ "先发起来，schema 让对方推断"
- ❌ 口头约定，不落书面

---

## 2. Subject / Topic 命名

### 命名公式

```
<domain>.<event-type>[.<version>]
```

描述**事件本身**，不描述**发起方**。

| 示例 | 类型 |
|:---|:---|
| `clarification.session.requested` | 推荐（事件语义） |
| `orders.created.v1` | 推荐（含 MAJOR 版本） |
| `inventory.stock.depleted` | 推荐 |
| `service-zentao.events` | ❌ 按发起方前缀（禁止） |
| `team-payments.events` | ❌ 按团队前缀（禁止） |

Producer 信息写入 envelope `source` 字段，不进 subject 前缀。

### 例外：多租户 / 多团队 ACL 分治理

当需要按 producer 做 ACL / retention 分治理（≥3 团队 / 多租户 SaaS），可用：

```
<tenant>.<domain>.<event>
```

**前提**：前缀语义必须在契约里显式声明，不是隐含推断。

---

## 3. QoS 选型

按业务需求选择交付语义，**不一刀切**：

| QoS | 选型 | 典型场景 |
|:---|:---|:---|
| **At-most-once**（可丢） | Core NATS / Kafka 无 ack | telemetry、心跳、live UI 推送 |
| **At-least-once**（可重复） | JetStream durable consumer / Kafka consumer group | 业务事件、命令、跨团队请求 |
| **Exactly-once**（去重精确） | JetStream + `Nats-Msg-Id` / Kafka transactional producer | 财务、计费、库存扣减 |

**跨团队默认 at-least-once**：consumer 可能离线、broker 可能切主、网络可能抖。

降级为 at-most-once 必须在契约里显式声明并说明可丢失场景。

---

## 4. Broker 资源治理（IaC Only）

Topic / Stream / Consumer Group / DLQ 等资源**只由 IaC 管理**：

- ✅ Terraform（`mongey/kafka` provider / `nats-io/nats-server` provider）
- ✅ Operator（Strimzi Kafka Operator / NATS JetStream Operator）
- ✅ CI 阶段脚本（`kafka-topics --create` / `nats stream add`，GitOps 模式）
- ❌ 应用代码运行时 `streams.add()` / `AdminClient.createTopics()`
- ❌ 临时调试创建的资源未清理就上线

Subject 域归属方负责该域 broker 资源的 IaC 治理。应用代码应假设资源已存在，不存在即启动失败（快速失败原则）。

---

## 5. 失败处理：DLQ + 重试策略契约化

跨团队消息流必须在契约中定义失败处理路径：

### 必须声明的内容

```yaml
# 契约中的 DLQ + 重试声明示例
failure_handling:
  max_retries: 3
  backoff: exponential(1s, 30s)
  dlq_subject: clarification.session.requested.dlq
  poison_pill: isolate  # 不阻塞主流
```

### 规则

- **DLQ**：consumer 处理失败 N 次后投递到备份 subject / topic
- **重试策略**：max attempts + backoff（exponential / linear）+ retry-after 提示
- **Poison pill 隔离**：DLQ 消息单独审计，不阻塞主流
- **可观测性**：失败计数、重试分布、DLQ depth 必须作为指标暴露

**禁止**：
- ❌ Consumer 无限重试同一条消息阻塞 partition
- ❌ 处理失败静默 ACK 丢弃消息

---

## 6. Schema 演化流程

### MINOR 演化（向前兼容，consumer 无需改动）

1. Producer 在 `data` 中新增可选字段或枚举值
2. Consumer 已实现 Tolerant Reader → 自动兼容
3. 契约 MINOR bump（如 `1.0.0` → `1.1.0`）+ CHANGELOG 条目
4. 同一 subject 持续运行，无需双发

### MAJOR 演化（breaking change）

1. Provider 启动新 subject（如 `orders.created.v2`）
2. 双方协调：consumer 升级计划 + 新 subject consumer 上线
3. 新旧 subject **双发**过渡期（时长在契约中声明）
4. Consumer 全部切换到 v2 后，下线 v1 subject
5. 契约 MAJOR bump + CHANGELOG 条目（标注 BREAKING）

**字段改名标准三步走**：

```
Step 1: 双写 oldField + newField（Producer 同时发两个字段）
Step 2: Consumer 切换读 newField，Provider 发弃用通知
Step 3: 双方确认后删 oldField，契约 MINOR/MAJOR bump
```

---

## 7. 可观测性要求

每条消息 envelope 应携带完整 metadata（详见 [EME](../specs/event-message-envelope.md)）：

| 字段 | 作用 |
|:---|:---|
| `id` | idempotency / 去重 |
| `traceparent` / `correlationid` | 追踪链路 |
| `source` | producer 标识 |
| `time` | producer 时间戳 |
| `specversion` | 契约版本标识 |

推荐采用 CloudEvents v1.0 标准 envelope，OTel / 主流 broker 工具链开箱即用。

---

## 8. 执行摘要

完整集成流：

```
1. Contract-first
   ├── 选格式（AsyncAPI / Protobuf / JSON Schema）
   ├── 双方 review + sign
   └── 落 SemVer + CHANGELOG

2. IaC 建资源
   ├── Stream / Topic / Consumer Group
   └── DLQ subject + 重试策略

3. Producer 上线
   ├── 发合规 EME envelope（UUID id, source, type, time）
   ├── 注入 traceparent（OTel）
   └── 复用 id 做重试（idempotency key）

4. Consumer 上线
   ├── Tolerant Reader（忽略未知字段）
   ├── 凭 id 去重
   └── 失败 → 重试 → DLQ

5. 演化
   ├── MINOR：同 subject 加字段，CHANGELOG MINOR bump
   └── MAJOR：新 subject 版本，双发过渡，CHANGELOG MAJOR bump
```

---

## 参考工具链

| 用途 | 推荐选型 |
|:---|:---|
| 契约格式 | AsyncAPI 3.0 + Protobuf payload |
| Schema Registry | Apicurio（开源）/ Confluent（商业）|
| Broker | Kafka / NATS JetStream / Pulsar |
| 序列化 | Protobuf（强 schema）/ Avro（演化友好）|
| Trace | OpenTelemetry + Jaeger / Tempo |
| IaC | Terraform / Crossplane |
