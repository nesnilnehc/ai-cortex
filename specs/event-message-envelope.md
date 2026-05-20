---
id: EME_SPEC_V1
name: Event Message Envelope
description: CloudEvents-aligned envelope schema for cross-service async messages — defines required fields, types, and evolution rules
version: 1.0.0
status: active
lifecycle: living
created_at: 2026-05-20
scope: >
  Applicable whenever designing or implementing async message payloads exchanged between
  independent services or teams. All cross-service messages MUST conform to this envelope
  before being published to any broker (NATS, Kafka, Pulsar, RabbitMQ, etc.).
related:
  - ../protocols/event-driven-integration.md
---

# 事件消息 Envelope 规范（EME Schema）

> **语义层**：定义"是什么"（异步消息的 envelope 字段结构、校验规则与演化约束）
>
> 与 [EDI](../protocols/event-driven-integration.md) 配套：EDI 定义"如何"发布、消费、演化与治理

---

## 1. 核心原则

- 所有跨服务消息必须结构化（JSON），不允许裸字符串
- envelope 遵循 [CloudEvents v1.0](https://github.com/cloudevents/spec) 语义，兼容 OTel / 主流 broker 工具链
- 消息 ID 全局唯一且不续号，充当 idempotency key
- Trace 关联遵循 W3C Trace Context 或 `correlationId` 字段标准
- Consumer 必须实现 Tolerant Reader，不得因未知字段失败

---

## 2. 必需结构（Schema）

### 必填字段

| 字段 | 类型 | 说明 |
|:---|:---|:---|
| `id` | string | 全局唯一 ID（UUID v7 / ULID）；重试复用同一 ID |
| `source` | string | Producer 标识，URI 或服务名（如 `zentao` / `urn:recloud:agentfabric`）|
| `type` | string | 事件类型，CloudEvents 风格（如 `orders.created.v1`）|
| `specversion` | string | CloudEvents 规范版本，固定为 `"1.0"` |
| `time` | string | Producer 时间戳，ISO 8601（如 `2026-05-20T10:30:00Z`）|
| `datacontenttype` | string | payload 序列化格式（如 `"application/json"`）|
| `data` | object | 业务 payload，嵌套在独立字段内 |

### 可选但推荐字段

| 字段 | 类型 | 说明 |
|:---|:---|:---|
| `traceparent` | string | W3C Trace Context，OTel 推荐（`00-{traceId}-{spanId}-{flags}`）|
| `correlationid` | string | 请求-响应关联 ID，指向原请求的 `id`；`traceparent` 不可用时使用 |
| `schemaurl` | string | payload schema 注册表 URL（Schema Registry）|
| `subject` | string | 事件所指向的具体资源（如 `orders/12345`）|
| `dataschema` | string | payload schema 定义路径 |

### 字段约束

- `id`：UUID v4/v7、ULID、Snowflake 均可；**禁止续号**（`REQ-001`、`msg-3` 等）
- `type`：采用 `<domain>.<event>[.<version>]` 命名（见 EDI §2）；MAJOR breaking 时通过新 type 表达
- `source`：标识 producer，不进 `type` 前缀
- `traceparent`：若使用 OpenTelemetry，producer 注入 context；consumer 提取并继续 span

---

## 3. 消息 ID 规范

### 全局唯一性要求

跨团队消息 ID 必须全局唯一，并充当 idempotency key：

- ✅ **UUID v7**（自带时间序，索引友好）—— 首选
- ✅ **ULID**（可读 prefix + 时间序）
- ✅ **Snowflake**（分布式自增，需统一发号服务）
- ✅ 可加语义 prefix：`req-clarify-01HXXXXXXXXXXXXXXXXXXXXXXXX`
- ❌ 续号（`REQ-XXX-NNN`、`msg-1`、`msg-2`）—— 分布式竞态 + retention 截断后无法续号

### Idempotency Key 语义

重试或重发时**复用同一 `id`**。Consumer 凭 `id` 去重：

- JetStream：`Nats-Msg-Id` header + `duplicate_window`
- Kafka：idempotent producer + exactly-once
- 自实现：consumer 维护已处理 ID 集合（TTL ≥ 重试窗口）

---

## 4. Trace 关联规范

### 首选：W3C Trace Context（OTel）

```json
{
  "traceparent": "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01"
}
```

- Producer 注入 OTel context；consumer 提取并继续 span
- 兼容 Jaeger / Tempo / Zipkin 等主流 exporter

### 备选：correlationId

```json
{
  "correlationid": "req-clarify-01HXXXXXXXXXXXXXXXXXXXXXXXX"
}
```

- 用于请求-响应模式：response 的 `correlationid` 指向原请求的 `id`
- **禁止**使用 `in_reply_to`、`messageId` 等自定义字段（OTel 工具链不识别）

---

## 5. Schema 演化（Tolerant Reader）

### 向前兼容（MINOR，consumer 无需改动）

| 操作 | 规则 |
|:---|:---|
| Producer 新增可选字段 | 自由新增；consumer **必须忽略未知字段** |
| Producer 新增枚举值 | consumer 遇未知枚举值须有 fallback，不得报错 |
| Producer 新增非必填嵌套字段 | 同上 |

### Breaking Change（MAJOR，需协调）

| 操作 | 规则 |
|:---|:---|
| 重命名字段 | 双写旧名 + 新名 → 弃用通知 → 删旧名（分三步） |
| 删除字段 | 同上 |
| 改变字段类型 / 语义 | 升 MAJOR，通过新 `type` version 发布（`orders.created.v2`）|
| 改变 `type` 前缀语义 | 同上 |

### Consumer 实现要求

```python
# ✅ Tolerant Reader 模式
envelope = json.loads(raw)
id_     = envelope["id"]           # 必填，取不到即快速失败
source  = envelope["source"]
type_   = envelope["type"]
extra   = {k: v for k, v in envelope.items() if k not in KNOWN_FIELDS}
# 忽略 extra，不报错
```

---

## 6. 反模式

- ❌ 用续号 ID（`REQ-XXX-NNN`）——分布式竞态 + 无法跨机房共享计数器
- ❌ `in_reply_to`、`messageId` 等自定义追踪字段——OTel 工具链不识别
- ❌ Consumer strict schema 匹配——producer 加字段就炸
- ❌ 不重用 `id` 做重试——consumer 无法去重，导致重复处理
- ❌ business payload 直接平铺到 envelope 顶层——与标准字段命名冲突

---

## 7. 合规示例

### 最小合规 envelope

```json
{
  "specversion": "1.0",
  "id": "01HXYZ-XXXXXXXXXXXXXXXXXXXXXXXX",
  "source": "zentao",
  "type": "clarification.session.requested",
  "time": "2026-05-20T10:30:00Z",
  "datacontenttype": "application/json",
  "data": {
    "sessionId": "sess-001",
    "taskId": "TASK-123"
  }
}
```

### 携带 OTel trace 的完整 envelope

```json
{
  "specversion": "1.0",
  "id": "01HXYZ-XXXXXXXXXXXXXXXXXXXXXXXX",
  "source": "urn:recloud:zentao",
  "type": "clarification.session.requested",
  "subject": "tasks/TASK-123",
  "time": "2026-05-20T10:30:00Z",
  "datacontenttype": "application/json",
  "traceparent": "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01",
  "data": {
    "sessionId": "sess-001",
    "taskId": "TASK-123",
    "requestedBy": "user-456"
  }
}
```

### 请求-响应（correlationId）

```json
{
  "specversion": "1.0",
  "id": "01HABC-YYYYYYYYYYYYYYYYYYYYYYYY",
  "source": "urn:recloud:agentfabric",
  "type": "clarification.session.responded",
  "time": "2026-05-20T10:31:00Z",
  "datacontenttype": "application/json",
  "correlationid": "01HXYZ-XXXXXXXXXXXXXXXXXXXXXXXX",
  "data": {
    "sessionId": "sess-001",
    "status": "completed",
    "result": "clarification accepted"
  }
}
```
