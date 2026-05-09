---
id: UNP_SPEC_V1
name: Universal Notification Schema
description: Channel-agnostic spec defining notification object structure (fields, types, validation)
version: 1.0.0
status: active
lifecycle: living
created_at: 2026-03-25
scope: >
  Applicable whenever designing or reviewing notification systems.
  All notifications MUST be expressed as UNP objects before delivery to any channel.
related: [../protocols/im-notification-delivery.md]
---

# 通用通知规范（UNP Schema）

> **语义层**：定义"是什么"（通知对象的字段结构与校验规则）
>
> 与 [INP](../protocols/im-notification-delivery.md) 配套：INP 定义"如何"渲染并投递到 IM 渠道

---

## 1. 核心原则

- 所有通知必须结构化（JSON），不允许纯文本
- 通知表达**事件**，而非消息
- 语义层与投递层必须分离
- 每条通知必须既机器可读又人可读

---

## 2. 必需结构（Schema）

### 必填字段

- `id`
- `type`
- `source`
- `timestamp`
- `intent`
- `priority`
- `title`

### 字段定义

| 字段 | 类型 | 说明 |
|:---|:---|:---|
| `id` | string | UUID |
| `type` | string | 事件名（UPPER_SNAKE_CASE） |
| `source` | string | 来源系统名 |
| `timestamp` | string | ISO 8601 时间戳 |
| `intent` | enum | `info` \| `action_required` \| `approval` \| `alert` |
| `priority` | enum | `P0` \| `P1` \| `P2` \| `P3` |
| `severity` | enum（可选） | `critical` \| `high` \| `medium` \| `low` |
| `title` | string | 通知标题 |
| `body` | string | 通知正文 |
| `actor` | object（可选） | `{type, id, name}` |
| `target` | object（可选） | `{type, id}` |
| `context` | object（可选） | 环境 / trace / 元数据 |
| `actions` | array | 当 priority ∈ [P0, P1] 时必填 |
| `actions[].type` | string | `link` \| `command` |
| `actions[].label` | string | 按钮文案 |
| `actions[].url \| command` | string | 链接或命令 |
| `extensions` | object（可选） | 扩展字段 |

---

## 3. 字段约束

### 禁止纯字符串通知

直接以字符串发送的通知一律禁止。

**禁止的模式**：

```
send("...")
notify("...")
console.log("alert")
```

### 必须有事件类型

每条通知必须声明语义化事件类型。

### 必须有 intent

每条通知必须声明 `intent`。

### 高优先级必须可操作

P0 和 P1 必须包含 `actions`。

**约束**：

- priority ∈ [P0, P1] → 必须包含 `actions`

### 命名规范

事件类型必须为 UPPER_SNAKE_CASE。

**示例**：`BUILD_FAILED`、`DEPLOYMENT_COMPLETE`、`APPROVAL_PENDING`

---

## 4. 反模式

- ❌ 把原始日志直接当通知发送
- ❌ 在业务逻辑里混入渲染（markdown / text）
- ❌ 在领域代码里硬编码 Slack / 飞书 / 企微
- ❌ 缺少 `priority` 或 `intent`

---

## 5. 合规示例

### P0（紧急，含 actions）

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "type": "BUILD_FAILED",
  "source": "ci-pipeline",
  "timestamp": "2026-05-09T10:30:00Z",
  "intent": "action_required",
  "priority": "P0",
  "severity": "critical",
  "title": "主干构建失败",
  "body": "main 分支构建 #1234 失败，影响所有下游部署",
  "actor": { "type": "system", "id": "ci-pipeline", "name": "CI Pipeline" },
  "target": { "type": "branch", "id": "main" },
  "actions": [
    { "type": "link",    "label": "查看构建日志", "url": "https://ci.example.com/builds/1234" },
    { "type": "command", "label": "重试构建",     "command": "ci retry 1234" }
  ]
}
```

### P2（普通信息，无 actions）

```json
{
  "id": "660f9511-f30c-52e5-b827-557766551111",
  "type": "DEPLOYMENT_COMPLETE",
  "source": "deploy-service",
  "timestamp": "2026-05-09T11:00:00Z",
  "intent": "info",
  "priority": "P2",
  "title": "staging 环境部署完成",
  "body": "v2.3.1 已成功部署到 staging 环境",
  "target": { "type": "environment", "id": "staging" }
}
```