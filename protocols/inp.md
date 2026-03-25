---
id: INP_SPEC_V1
name: IM Notification Protocol
description: Rendering and delivery layer for IM channels (Feishu, WeCom, etc)
version: 1.0.0
status: active
lifecycle: living
created_at: 2026-03-25
scope: >
  Applicable when implementing notification rendering and routing for instant messaging
  channels. Takes UNP notifications as input and produces channel-specific output.
related: [./unp.md]
---

# IM Notification Protocol (INP)

> **投递层**：定义 HOW（如何渲染和投递到 IM 渠道）
>
> 与 [UNP](./unp.md) 配套：UNP 定义 WHAT（通知的结构和意图）

---

## 1. CORE PRINCIPLES

- Rendering MUST be separated from UNP
- Notification MUST be structured (no free text)
- High-priority messages MUST be actionable
- Notification noise MUST be controlled

---

## 2. PRIORITY POLICY

### P0 (Critical, must interrupt)

**MUST include:**
- mention_user
- interactive_card
- actionable

**FORBIDDEN:**
- plain_text_only

### P1 (Important)

**MUST include:**
- mention_owner
- actionable

### P2 (Normal)

**MUST NOT:**
- mention_user

### P3 (Info)

**FORBIDDEN:**
- mention_user

---

## 3. MESSAGE STRUCTURE

### required
- header
- body

### optional
- fields
- actions
- footer

### constraints

**header:**
- MUST include: `priority`, `emoji`

**body:**
- max_length: 500 characters

**actions:**
- max_items: 3

---

## 4. RENDERING RULES

### Priority → Format Mapping

| Priority | Rendering Format |
|:---|:---|
| P0 | card |
| P1 | card |
| P2 | markdown |
| P3 | text |

### Rendering Rules

- ❌ Do NOT render raw JSON
- ❌ Do NOT include stacktrace directly
- ✅ Use structured fields instead of long text

---

## 5. MENTION RULES

### P0
- oncall
- owner

### P1
- owner

### P2
- none

### P3
- none

### Constraints
- no_manual_mentions
- no_@all

---

## 6. ROUTING RULES

```
routing:
  dynamic: true
  based_on:
    - priority
    - service
    - environment
```

---

## 7. ANTI-SPAM POLICY

### dedup
- required: true
- key: dedup_key

### throttle
- required: true

### limits

| Priority | Rate Limit |
|:---|:---|
| P0 | 1 per 5 minutes |
| P1 | 1 per 10 minutes |
| P2 | batched |

---

## 8. CHANNEL COMPATIBILITY

### Feishu

**supports:**
- card
- button
- callback

### WeCom

**supports:**
- markdown

**limitations:**
- weak_interaction

### Rule
If channel does not support feature → degrade gracefully

---

## 9. SECURITY RULES

- webhook MUST NOT be hardcoded
- tokens MUST be stored securely
- support signature validation

---

## 10. AI REFACTOR INSTRUCTION

```
Transform UNP notifications into IM messages:

1. Map priority to rendering format (card/markdown/text)
2. Inject mentions based on routing rules
3. Ensure P0/P1 messages are actionable
4. Apply deduplication and throttling
5. Adapt output per channel capability

Remove any direct usage of Feishu/WeCom APIs from business logic.
```
