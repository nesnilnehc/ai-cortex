---
artifact_type: rule
name: standards-event-driven-integration
version: 1.0.0
scope: 跨团队 / 跨独立服务的事件驱动消息通信
recommended_scope: user
status: active
created_at: 2026-05-20
---

# Rule: 事件驱动集成纪律

## 适用范围

任何跨团队 / 跨独立服务的 async 消息，无论 broker 类型（NATS、Kafka、Pulsar、RabbitMQ……）。

同一团队、同一发布周期的内部通信不适用。

## 强制触发：开工前必读

接触跨服务消息时立即加载：

- **envelope schema** → [specs/event-message-envelope.md](../specs/event-message-envelope.md)（EME_SPEC_V1）
- **完整集成流程** → [protocols/event-driven-integration.md](../protocols/event-driven-integration.md)（EDI_PROTOCOL_V1）

## 5 条致命违规

即便不读全文，以下行为**绝对禁止**：

1. **续号 ID**（`REQ-XXX-NNN`、`msg-1`、`msg-2`……）→ 使用 UUID v7 / ULID
2. **应用代码运行时建 stream / topic** → IaC 管理（Terraform / Operator / CI 脚本）
3. **自创 subject 不查契约** → Contract-first，先有书面契约再发消息
4. **跨团队消息走 Core NATS 无持久化** → 至少 at-least-once（JetStream durable）
5. **用 `in_reply_to` / `messageId` 等自定义追踪字段** → 使用 `traceparent`（W3C / OTel）或 `correlationid`

## 与其他规则的关系

- **互补 `standards-cross-team-contracts`**：该规则管契约文档（SemVer + CHANGELOG + 文件命名），本规则管运行时消息治理（envelope + QoS + DLQ）
- **实现代码遵循 `standards-coding`**：publish / consume 脚本仍须满足通用编码原则
