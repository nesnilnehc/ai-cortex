---
id: INP_PROTOCOL_V1
name: IM Notification Delivery Protocol
description: Rendering and delivery layer for IM channels (Feishu, WeCom, etc)
version: 1.0.0
status: active
lifecycle: living
created_at: 2026-03-25
scope: >
  Applicable when implementing notification rendering and routing for instant messaging
  channels. Takes UNP notifications as input and produces channel-specific output.
related: [../specs/universal-notification.md]
---

# IM Notification Delivery Protocol (INP)

> **Delivery layer**: defines *how* a notification is rendered and delivered to an IM channel
>
> Paired with [UNP](../specs/universal-notification.md), which defines *what* a notification is — its structure and intent

---

## Participants

| Role | Responsibility |
|:---|:---|
| **UNP producer** (the business system) | Constructs a conforming UNP notification object and hands it to the delivery layer |
| **INP delivery layer** (this protocol's executor) | Renders by priority, routes, deduplicates, throttles, and adapts to the channel's capabilities |
| **IM channel** (Feishu, WeCom and others) | Receives the channel-adapted message and presents it to the user |

---

## 1. Core principles

- Rendering must stay separate from UNP
- Notifications must be structured; free text is not allowed
- High-priority messages must be actionable
- Notification noise must be kept under control

---

## 2. Priority policy

### P0 — urgent, must interrupt

**Must include**:

- `mention_user`
- `interactive_card`
- `actionable`

**Forbidden**:

- `plain_text_only`

### P1 — important

**Must include**:

- `mention_owner`
- `actionable`

### P2 — normal

**Forbidden**:

- `mention_user`

### P3 — informational

**Forbidden**:

- `mention_user`

---

## 3. Message structure

### Required

- `header`
- `body`

### Optional

- `fields`
- `actions`
- `footer`

### Constraints

**header**：

- Must include `priority` and `emoji`

**body**：

- At most 500 characters

**actions**：

- At most 3 items

---

## 4. Rendering rules

### Priority to format mapping

| Priority | Rendered format |
|:---|:---|
| P0 | card |
| P1 | card |
| P2 | markdown |
| P3 | text |

### Rendering detail

- ❌ Must not render raw JSON directly
- ❌ Must not embed a stacktrace directly
- ✅ Use structured fields in place of long text

---

## 5. Mention rules

| Priority | Who is mentioned |
|:---|:---|
| P0 | oncall and owner |
| P1 | owner |
| P2 | nobody |
| P3 | nobody |

### Constraints

- Manual mentions are forbidden
- Mentioning everyone (@all) is forbidden

---

## 6. Routing rules

```yaml
routing:
  dynamic: true
  based_on:
    - priority
    - service
    - environment
```

---

## 7. Anti-spam policy

### Deduplication

- Required: yes
- Key: `dedup_key`

### Throttling

- Required: yes

### Rate limits

| Priority | Rate limit |
|:---|:---|
| P0 | 1 per 5 minutes |
| P1 | 1 per 10 minutes |
| P2 | Batched |

---

## 8. Channel compatibility

### Feishu

**Supports**:

- card
- button
- callback

### WeCom

**Supports**:

- markdown

**Limitations**:

- Weaker interactive capability

### Fallback rule

Where a channel does not support a capability, it must degrade gracefully.

---

## 9. Security rules

- A webhook must not be hard-coded
- Tokens must be stored securely
- Signature verification is supported

---

## 10. Execution summary

The steps that turn a UNP object into an IM message:

1. Map priority to a rendered format (card / markdown / text)
2. Inject mentions according to the routing rules
3. Ensure P0 and P1 messages are actionable
4. Apply deduplication and throttling
5. Adapt the output to the channel's capabilities

Business logic must not call the Feishu or WeCom API directly.
