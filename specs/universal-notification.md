---
id: UNP_SPEC_V1
name: Universal Notification Protocol
description: Channel-agnostic semantic layer defining structured notification model
version: 1.0.0
status: active
lifecycle: living
created_at: 2026-03-25
scope: >
  Applicable whenever designing or reviewing notification systems.
  All notifications MUST be expressed as UNP objects before delivery to any channel.
related: [../protocols/im-notification-delivery.md]
---

# Universal Notification Protocol (UNP)

> **语义层**：定义 WHAT（通知的结构和意图）
>
> 与 [INP](../protocols/im-notification-delivery.md) 配套：INP 定义 HOW（如何渲染和投递到 IM 渠道）

---

## 1. CORE PRINCIPLES

- All notifications MUST be structured (JSON), not plain text
- Notifications represent EVENTS, not messages
- Separate semantic layer from delivery layer
- Every notification MUST be machine-readable and human-readable

---

## 2. REQUIRED SCHEMA

### required_fields
- id
- type
- source
- timestamp
- intent
- priority
- title

### field_definitions

| 字段 | 类型 | 说明 |
|:---|:---|:---|
| `id` | string | uuid |
| `type` | string | UPPER_SNAKE_CASE event name |
| `source` | string | system name |
| `timestamp` | string | ISO8601 |
| `intent` | enum | `info` \| `action_required` \| `approval` \| `alert` |
| `priority` | enum | `P0` \| `P1` \| `P2` \| `P3` |
| `severity` | enum (optional) | `critical` \| `high` \| `medium` \| `low` |
| `title` | string | 通知标题 |
| `body` | string | 通知正文 |
| `actor` | object (optional) | `{type, id, name}` |
| `target` | object (optional) | `{type, id}` |
| `context` | object (optional) | environment / trace / metadata |
| `actions` | array | 如 priority ∈ [P0, P1]，此字段必需 |
| `actions[].type` | string | `link` \| `command` |
| `actions[].label` | string | 按钮文案 |
| `actions[].url \| command` | string | 链接或命令 |
| `extensions` | object (optional) | 扩展字段 |

---

## 3. HARD RULES (MANDATORY)

### no_plain_message
Direct string-based notification is forbidden.

**Forbidden patterns:**
```
send("...")
notify("...")
console.log("alert")
```

### must_have_event_type
Every notification MUST define a semantic event type.

### must_have_intent
Every notification MUST define intent.

### actionable_required_for_high_priority
P0 and P1 MUST include actions.

**Enforcement:**
- priority ∈ [P0, P1] → require: actions

### naming_convention
Event type must be UPPER_SNAKE_CASE.

**Example:** `BUILD_FAILED`, `DEPLOYMENT_COMPLETE`, `APPROVAL_PENDING`

---

## 4. ANTI-PATTERNS

❌ Sending raw logs as notifications
❌ Mixing rendering (markdown/text) inside business logic
❌ Hardcoding Slack/Feishu in domain code
❌ Missing priority or intent

---

## 5. AI REFACTOR INSTRUCTION

```
Refactor all notification-related code to:

1. Replace direct message sending with UNP object construction
2. Extract event types from business logic
3. Add intent and priority to each notification
4. Ensure all notifications follow the schema strictly
5. Remove any channel-specific logic from business code

Output must only use UNP objects as the notification interface.
```
