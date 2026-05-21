---
artifact_type: rule
name: standards-nats-integration
version: 1.0.0
scope: 任何使用 NATS / JetStream 进行跨服务通信的代码与协作
recommended_scope: user
status: active
created_at: 2026-05-20
---

# Rule: NATS 集成纪律

## 适用范围

使用 NATS / JetStream 在独立服务之间通信的所有场景。同一团队、同一发布周期的内部消息不适用。

## 强制触发：开工前必查

- NATS 官方文档：<https://docs.nats.io>
- NATS Services API（服务发现 / 健康 / schema 查询用它，**不要自造**）
- 跨团队场景同时遵循 [standards-cross-team-contracts](./standards-cross-team-contracts.md)

## 6 条致命违规

1. **消息 ID 续号**（`msg-1` / `REQ-001`） → UUID v7 / ULID，写入 `Nats-Msg-Id` header
2. **应用代码运行时建 stream / consumer / KV** → IaC 管理（Terraform / Operator / CI 脚本）
3. **跨团队消息走 Core NATS 不持久化** → JetStream durable consumer（at-least-once）
4. **凭感觉发 subject** → 看契约，哪怕只是 markdown 列了 subject 清单
5. **元信息塞 JSON envelope** → 用 NATS Headers 承载（`Nats-Msg-Id` / `X-Source` / `X-Type` / `Traceparent` / `X-Correlation-Id`）
6. **多轮会话用 Core NATS Request-Reply** → JetStream + subject 内含 sessionId

## 反模式

- ❌ 自造服务发现 / 健康检查 / schema 查询协议 → 用 NATS Services（`$SRV.*`）
- ❌ 强制 CloudEvents structured mode → 用 binary mode（headers + 业务 payload）
- ❌ 把 SessionId / WorkflowId 表述为 NATS 原生概念 → NATS 没有，是应用层叠加（靠 subject 编码 + headers 串联 + 可选 KV 状态）
- ❌ 自创 `in_reply_to` / `messageId` 等追踪字段 → 用 `X-Correlation-Id` / `Traceparent` 标准 header

## Tolerant Reader 原则

Consumer 必须忽略未知字段与未知枚举值，不得因 producer 新增内容而失败。

## 模式选型速查

| 需求 | 选哪个 |
|---|---|
| 立即问立即答（< 5s） | Core NATS Request-Reply |
| 持久 / 至少一次 / 可回放 | JetStream Stream + durable consumer |
| 会话 / 状态 / 配置 | JetStream KV |
| 大文件 / 二进制 | JetStream Object Store |
| 服务发现 / 健康 / schema | NATS Services API |
| 工作负载分担 | Queue Group |
| 多轮异步会话 | JetStream + subject 内含 sessionId + headers 三 ID（id / X-Correlation-Id / sessionId）|

## 与其他规则关系

- 跨团队契约管理 → [standards-cross-team-contracts](./standards-cross-team-contracts.md)（与本规则正交，跨团队同时生效）
- 通用编码原则 → [standards-coding](./standards-coding.md)
