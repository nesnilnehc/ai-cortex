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

# IM 通知投递协议（INP）

> **投递层**：定义"如何"渲染并投递到 IM 渠道
>
> 与 [UNP](../specs/universal-notification.md) 配套：UNP 定义"是什么"（通知的结构与意图）

---

## 参与方

| 角色 | 职责 |
|:---|:---|
| **UNP 生产方**（业务系统） | 构造合规的 UNP 通知对象并提交给投递层 |
| **INP 投递层**（本协议执行者） | 按优先级渲染、路由、去重、限流，适配渠道能力 |
| **IM 渠道**（飞书 / 企微等） | 接收渠道适配后的消息并最终呈现给用户 |

---

## 1. 核心原则

- 渲染必须与 UNP 分离
- 通知必须结构化（不允许自由文本）
- 高优先级消息必须可操作
- 必须控制通知噪音

---

## 2. 优先级策略

### P0（紧急，必须打断）

**必须包含**：

- `mention_user`（@相关人）
- `interactive_card`（交互式卡片）
- `actionable`（可操作）

**禁止**：

- `plain_text_only`（纯文本）

### P1（重要）

**必须包含**：

- `mention_owner`（@责任人）
- `actionable`

### P2（普通）

**禁止**：

- `mention_user`

### P3（提示）

**禁止**：

- `mention_user`

---

## 3. 消息结构

### 必填

- `header`（标题）
- `body`（正文）

### 可选

- `fields`（字段）
- `actions`（操作）
- `footer`（页脚）

### 约束

**header**：

- 必须包含 `priority`（优先级）和 `emoji`（情绪图标）

**body**：

- 最大长度 500 字符

**actions**：

- 最多 3 项

---

## 4. 渲染规则

### 优先级 → 格式映射

| 优先级 | 渲染格式 |
|:---|:---|
| P0 | card（卡片） |
| P1 | card |
| P2 | markdown |
| P3 | text（纯文本） |

### 渲染细则

- ❌ 不得直接渲染原始 JSON
- ❌ 不得直接嵌入 stacktrace
- ✅ 使用结构化字段替代长文本

---

## 5. @人规则

| 优先级 | @ 谁 |
|:---|:---|
| P0 | oncall（值班）+ owner（责任人）|
| P1 | owner |
| P2 | 不 @ |
| P3 | 不 @ |

### 约束

- 禁止手动 @
- 禁止 @ 全员（@all）

---

## 6. 路由规则

```yaml
routing:
  dynamic: true
  based_on:
    - priority
    - service
    - environment
```

---

## 7. 反垃圾策略

### 去重（dedup）

- 必需：是
- 键：`dedup_key`

### 限流（throttle）

- 必需：是

### 限额

| 优先级 | 速率限制 |
|:---|:---|
| P0 | 每 5 分钟 1 条 |
| P1 | 每 10 分钟 1 条 |
| P2 | 批量发送 |

---

## 8. 渠道兼容性

### 飞书（Feishu）

**支持**：

- card（交互卡片）
- button（按钮）
- callback（回调）

### 企业微信（WeCom）

**支持**：

- markdown

**限制**：

- 交互能力较弱

### 兜底规则

若渠道不支持某能力，须优雅降级（graceful degradation）。

---

## 9. 安全规则

- webhook 不得硬编码
- token 必须安全存储
- 支持签名校验

---

## 10. 执行摘要

UNP → IM 消息的转换步骤：

1. 按 priority 映射渲染格式（card / markdown / text）
2. 按路由规则注入 @ 信息
3. 确保 P0 / P1 消息可操作
4. 应用去重与限流
5. 按渠道能力适配输出

业务逻辑中不得直接调用 Feishu / WeCom API。
