---
id: UNIVERSAL_NOTIFICATION_SPEC_V2
name: Universal Notification Schema
description: Channel-agnostic spec defining notification object structure (fields, types, validation). All notifications MUST be expressed as UNP objects before delivery to any channel.
version: 2.0.0
status: active
lifecycle: living
created_at: 2026-03-25
scope: |
  Applicable whenever designing or reviewing notification systems.
  All notifications MUST be expressed as UNP objects before delivery to any channel.
related:
  - ./spec-modeling.md
  - ../protocols/im-notification-delivery.md
---

# Universal Notification Protocol (UNP)

> **Data contract**: defines the field structure and validation rules of a channel-agnostic notification object

---

## 1. Position and scope

The Universal Notification Protocol (UNP) is the **semantic layer** spec for notification artifacts: it defines what a notification *is* — field structure and validation rules. The delivery layer — how it is rendered and how it reaches a particular channel — is carried by [INP](../protocols/im-notification-delivery.md). The two are decoupled.

### 1.1 In scope and out of scope

In scope:

- Designing or reviewing any notification system that spans channels — IM, email, push, webhooks and the like
- Every notification sent to a user, which must be expressed as a UNP object before it reaches a particular channel

Out of scope:

- A single channel's proprietary message format, such as the full Slack block kit field set — that belongs to the delivery layer
- System logs and audit trails, which are not notifications addressed to a person

---

## 5. Body structure contract

### 5.1 Required fields

- `id`
- `type`
- `source`
- `timestamp`
- `intent`
- `priority`
- `title`

### 5.2 Field definitions

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | UUID |
| `type` | string | yes | Event name, UPPER_SNAKE_CASE |
| `source` | string | yes | Name of the originating system |
| `timestamp` | string | yes | ISO 8601 timestamp |
| `intent` | enum | yes | `info` / `action_required` / `approval` / `alert` |
| `priority` | enum | yes | `P0` / `P1` / `P2` / `P3` |
| `title` | string | yes | Notification title |
| `severity` | enum | optional | `critical` / `high` / `medium` / `low` |
| `body` | string | optional | Notification body |
| `actor` | object | optional | `{type, id, name}` |
| `target` | object | optional | `{type, id}` |
| `context` | object | optional | Environment / trace / metadata |
| `actions` | array | conditional | Required when `priority ∈ [P0, P1]` |
| `actions[].type` | string | conditional | `link` / `command` |
| `actions[].label` | string | conditional | Button text |
| `actions[].url` / `actions[].command` | string | conditional | A link or a command |
| `extensions` | object | optional | Extension fields |

### 5.3 Field constraints

#### 5.3.1 An event type is required

Every notification must declare a semantic event type, with `type` in UPPER_SNAKE_CASE. For example `BUILD_FAILED`, `DEPLOYMENT_COMPLETE`, `APPROVAL_PENDING`.

#### 5.3.2 An intent is required

Every notification must declare an `intent`, stating why the user is being notified.

#### 5.3.3 High priority must be actionable

When `priority ∈ [P0, P1]`, `actions` must be present — a high-priority notification needs a clear way to act.

---

## 6. Anti-patterns

- ❌ Sending a notification as a bare string (`send("...")` / `notify("...")` / `console.log("alert")`)
- ❌ Sending a raw log line as a notification
- ❌ Mixing rendering (markdown or text) into business logic
- ❌ Hard-coding a specific channel such as Slack, Feishu or WeCom into domain code
- ❌ Missing `priority` or `intent`
- ❌ A `priority` of P0 or P1 with no `actions`
- ❌ A `type` that is not UPPER_SNAKE_CASE, such as `buildFailed`

---

## 7. Examples

### 7.1 A P0 urgent notification, with actions

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "type": "BUILD_FAILED",
  "source": "ci-pipeline",
  "timestamp": "2026-05-09T10:30:00Z",
  "intent": "action_required",
  "priority": "P0",
  "severity": "critical",
  "title": "Trunk build failed",
  "body": "Build #1234 on main failed, blocking every downstream deployment",
  "actor": { "type": "system", "id": "ci-pipeline", "name": "CI Pipeline" },
  "target": { "type": "branch", "id": "main" },
  "actions": [
    { "type": "link",    "label": "View build log", "url": "https://ci.example.com/builds/1234" },
    { "type": "command", "label": "Retry build",   "command": "ci retry 1234" }
  ]
}
```

### 7.2 A P2 informational notification, without actions

```json
{
  "id": "660f9511-f30c-52e5-b827-557766551111",
  "type": "DEPLOYMENT_COMPLETE",
  "source": "deploy-service",
  "timestamp": "2026-05-09T11:00:00Z",
  "intent": "info",
  "priority": "P2",
  "title": "Deployment to staging complete",
  "body": "v2.3.1 deployed successfully to staging",
  "target": { "type": "environment", "id": "staging" }
}
```

---

## 8. Relationship to other assets

- **Paired protocol**: [protocols/im-notification-delivery.md](../protocols/im-notification-delivery.md), the INP — rendering and delivery for IM channels. UNP defines what a notification is; INP defines how it is delivered.
- **Recursive basis**: this spec itself follows the 8-section skeleton of [spec-modeling.md](./spec-modeling.md) v2.0.0, skipping §2 (a runtime object has no N-question framework), §3 (no file naming) and §4 (no frontmatter)
