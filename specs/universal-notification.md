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

# 通用通知规范（UNP）

> **数据契约**：定义跨渠道通知对象的字段结构与校验规则

---

## 1. 定位与适用范围

通用通知规范（Universal Notification Protocol，UNP）是通知制品的**语义层**规范——定义"通知是什么"（字段结构与校验规则）。投递层（如何渲染、如何发到具体渠道）由 [INP](../protocols/im-notification-delivery.md) 承担，两者解耦。

### 1.1 适用与不适用

适用：

- 任何跨渠道（IM、邮件、推送、Webhook 等）的通知系统设计与评审
- 所有发往用户的通知，在投递到具体渠道前必须先表达为 UNP 对象

不适用：

- 单一渠道的私有消息格式（如 Slack block kit 完整字段）——那是投递层的事
- 系统日志、审计追踪（不是面向人的通知）

---

## 5. 正文结构契约

### 5.1 必填字段

- `id`
- `type`
- `source`
- `timestamp`
- `intent`
- `priority`
- `title`

### 5.2 字段定义表

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | string | 必 | UUID |
| `type` | string | 必 | 事件名（UPPER_SNAKE_CASE） |
| `source` | string | 必 | 来源系统名 |
| `timestamp` | string | 必 | ISO 8601 时间戳 |
| `intent` | enum | 必 | `info` / `action_required` / `approval` / `alert` |
| `priority` | enum | 必 | `P0` / `P1` / `P2` / `P3` |
| `title` | string | 必 | 通知标题 |
| `severity` | enum | 可选 | `critical` / `high` / `medium` / `low` |
| `body` | string | 可选 | 通知正文 |
| `actor` | object | 可选 | `{type, id, name}` |
| `target` | object | 可选 | `{type, id}` |
| `context` | object | 可选 | 环境 / trace / 元数据 |
| `actions` | array | 条件 | 当 `priority ∈ [P0, P1]` 时必填 |
| `actions[].type` | string | 条件 | `link` / `command` |
| `actions[].label` | string | 条件 | 按钮文案 |
| `actions[].url` / `actions[].command` | string | 条件 | 链接或命令 |
| `extensions` | object | 可选 | 扩展字段 |

### 5.3 字段约束

#### 5.3.1 必须有事件类型

每条通知必须声明语义化事件类型，`type` 字段为 UPPER_SNAKE_CASE。示例：`BUILD_FAILED`、`DEPLOYMENT_COMPLETE`、`APPROVAL_PENDING`。

#### 5.3.2 必须有 intent

每条通知必须声明 `intent`，明确"为什么通知用户"。

#### 5.3.3 高优先级必须可操作

`priority ∈ [P0, P1]` 时必须包含 `actions`——高优先级通知应给出明确动作入口。

---

## 6. 反模式

- ❌ 直接以字符串发送通知（`send("...")` / `notify("...")` / `console.log("alert")`）
- ❌ 把原始日志直接当通知发送
- ❌ 在业务逻辑里混入渲染（markdown / text）
- ❌ 在领域代码里硬编码 Slack / 飞书 / 企微等具体渠道
- ❌ 缺少 `priority` 或 `intent`
- ❌ `priority` 为 P0 / P1 但无 `actions`
- ❌ `type` 不是 UPPER_SNAKE_CASE（如 `buildFailed`）

---

## 7. 示例

### 7.1 P0 紧急通知（含 actions）

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

### 7.2 P2 普通信息（无 actions）

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

---

## 8. 与其他资产关系

- **配套 protocol**：[protocols/im-notification-delivery.md](../protocols/im-notification-delivery.md)（INP）——IM 渠道的渲染与投递流程。UNP 定义"是什么"，INP 定义"如何投递"。
- **递归基础**：本 spec 自身遵循 [spec-modeling.md](./spec-modeling.md) v2.0.0 的 8 节骨架；跳过 §2（运行时对象无 N 问框架）、§3（无文件命名）、§4（无 frontmatter）
