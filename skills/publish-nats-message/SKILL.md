---
name: publish-nats-message
description: Publish a NATS message conforming to a cross-team contract, using NATS MCP tools. Authors the contract on first use if missing. Reads project-level cache (.cortex/nats.yaml) to avoid re-prompting basics across sessions.
description_zh: 通过 NATS MCP 工具按跨团队契约发布消息；首次缺契约时引导起草。读取项目级缓存 .cortex/nats.yaml，避免跨会话重复询问。
tags: [nats, messaging, cross-team, producer, mcp]
version: 1.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [publish nats, send nats message, 发布事件, 跨服务发消息, nats publish]
input_schema:
  type: free-form
  description: Event description (domain + type); payload data; consumer name (first time only); optional QoS hint; optional explicit contract path
output_schema:
  type: side-effect
  description: NATS message published via MCP; ack/result reported; contract file created (first time) or reused (subsequent)
---

# 技能（Skill）：发布 NATS 消息

## 目的（Purpose）

让相互协作的项目能"正确生产消息"——按跨团队契约通过 NATS MCP 工具发布一条消息，确保 subject / headers / payload / QoS 严格对齐 [specs/nats-messaging.md](../../specs/nats-messaging.md)。首次某事件无契约时，引导生成契约并落盘 producer repo。

---

## 核心目标（Core Objective）

**首要目标**：通过 NATS MCP 工具发布一条符合 contract 的消息；契约不存在时先生成契约再发送。

**成功标准**：

1. ✅ 项目缓存 `.cortex/nats.yaml` 已读取（不存在则引导生成）
2. ✅ 事件对应的 `<event>-contract.md` 已就位（存在则读取；不存在则起草并提示 commit）
3. ✅ 实际发送的 subject / headers / payload 严格符合契约定义
4. ✅ `Nats-Msg-Id` 为本次生成的 UUID v7（或同消息重试复用原 ID）
5. ✅ JetStream 发送收到 ack；at-most-once 仅做 fire-and-forget
6. ✅ 用户拿到发送结果（成功 + headers 实摘要 / 失败 + 原因）

**验收测试**：consumer 侧用 `consume-nats-message` 订阅同一 subject，能正确解码 headers + payload 且无校验失败。

---

## 范围边界

**本技能负责**：

- 读项目缓存 + 加载契约
- 首次缺契约时按 [specs/nats-messaging.md](../../specs/nats-messaging.md) + [specs/cross-team-contract.md](../../specs/cross-team-contract.md) 起草契约
- 构造合规消息（subject + headers + payload）
- 通过 NATS MCP 工具完成 publish / jetstream_publish / request
- Ack 校验与失败重试（按契约重试策略）

**本技能不负责**：

- 实际写 publisher 代码 → 不在 Skill 范畴（应用工程职责）
- 创建 / 修改 JetStream stream / consumer / KV → IaC 责任（见 spec §5.5.2）
- 订阅 / 消费消息 → 用 [consume-nats-message](../consume-nats-message/SKILL.md)

---

## 前置条件

- 已连接 NATS MCP server（提供 `mcp__nats__publish` / `mcp__nats__jetstream_publish` / `mcp__nats__request` 等工具；具体工具名以连接的 server 为准）
- 当前工作目录是 producer repo（用于读 `.cortex/nats.yaml` 与契约文件）
- 用户能授权对 broker 的发布权限

---

## 执行流程

### 阶段 0：宣告

> "我正在使用 publish-nats-message 技能发送一条 NATS 消息。"

### 阶段 1：读项目缓存

1. 读 `.cortex/nats.yaml`（producer repo 根目录）
2. 提取字段：`broker_url` / `service_source` / `default_stream` / `contract_dir` / `iac_owner`
3. **缓存不存在**：进入"缓存初始化子流程"——询问上述字段，写入 `.cortex/nats.yaml`，提示用户 review 并 commit；后续步骤复用此次填的值
4. **缓存存在但字段缺**：仅就缺字段询问，更新缓存

### 阶段 2：定位契约

1. 解析用户输入的事件描述（如"发 clarification.session.requested"）
2. Glob `<contract_dir>/**/<event>-contract.md`
3. **命中**：读取契约 → 进入阶段 4
4. **未命中**：进入阶段 3 起草契约

### 阶段 3：契约起草子流程（仅首次某 event）

询问最少必要信息（其他从缓存得到）：

- consumer 名称（一个或多个）
- QoS 选型（默认 at-least-once；用户可选 at-most-once 但须说明可丢失场景）
- 是否多轮会话场景（若是 → `X-Correlation-Id` 标条件必填，subject 内规划 sessionId 位置）
- 业务字段表（payload schema 草案；可让用户列出主要字段类型必填性）
- DLQ + 重试参数（默认值：DLQ `<subject>.dlq`、max_deliver=5、exponential backoff base 1s max 30s）

生成契约文件：

- 路径：`<contract_dir>/<consumer>/<event>-contract.md`（按 [cross-team-contract.md §3](../../specs/cross-team-contract.md) 扁平布局）
- frontmatter 含 `contract_version: 1.0.0` + CHANGELOG 首条 `### 1.0.0 — YYYY-MM-DD Initial Release`
- 正文按 [specs/nats-messaging.md §7.1](../../specs/nats-messaging.md) 样板

完成后：

- 提示用户 review + commit 契约文件
- **等待用户确认**契约 ok 后再进入阶段 4 实发送（避免按未确认契约发出污染消息）

### 阶段 4：构造消息

按契约填字段：

| 项 | 取值 |
|---|---|
| subject | 契约「契约范围」节定义的 subject |
| `Nats-Msg-Id` | 现场生成 UUID v7（重试时复用原 ID） |
| `X-Source` | 缓存 `service_source` |
| `X-Type` | 契约定义的事件类型字符串 |
| `Traceparent` | 若运行环境有 OTel context，注入；否则跳过 |
| `X-Correlation-Id` | 多轮会话场景必填，由调用方提供原 ID |
| `X-Schema-Url` | 契约定义 schema URL 时填 |
| payload | 用户提供的业务数据，按契约字段表逐字段校验（必填齐全、类型对、枚举值合法） |

校验失败 → 报错指出违规字段，**不发送**。

### 阶段 5：调用 MCP NATS 工具发送

按 QoS 选用工具：

| 场景 | MCP 工具 | 备注 |
|---|---|---|
| at-most-once（telemetry / 心跳） | `mcp__nats__publish` | 无 ack，fire-and-forget |
| at-least-once（跨团队默认） | `mcp__nats__jetstream_publish` | 必须等 ack；触发 `duplicate_window` 去重 |
| 同步请求-响应（< 5s） | `mcp__nats__request` | 含 reply subject + `X-Correlation-Id` |

具体工具名以连接的 NATS MCP server 提供为准；如工具签名不一致，Skill 自适应映射（headers 参数 / subject 参数）。

### 阶段 6：自检与回执

- **JetStream**：等 ack；超时 / 无 ack → 视为失败
- **失败重试**：按契约重试策略重发，**复用同一 `Nats-Msg-Id`**（broker 端去重）；达 max_deliver 仍失败 → 上报用户
- **成功回执**：输出
  - subject
  - headers 实际值（敏感字段如有可脱敏）
  - ack 信息（JetStream sequence / stream / domain）
  - 用时

---

## 错误处理

| 情况 | 处理 |
|---|---|
| MCP NATS server 未连接 | 提示用户检查 MCP 配置，列出期望工具名 |
| `.cortex/nats.yaml` 不存在 | 进入缓存初始化子流程（阶段 1） |
| 契约不存在 | 进入契约起草子流程（阶段 3） |
| Payload 字段校验失败 | 列出违规字段，要求修正后重发 |
| JetStream ack 超时 | 按契约 backoff 重试；最终失败上报用户 |
| Stream 不存在（Subject 域未 IaC 化） | 报错指出违反 [specs/nats-messaging.md §5.5.2](../../specs/nats-messaging.md)；提示联系 IaC 责任方 |

---

## 反模式

- ❌ 应用代码运行时建 Stream / Consumer / KV（违反 spec §5.5.2）—— 报错并指向 IaC
- ❌ 跨团队消息走 Core NATS 不持久化 —— 默认转 JetStream，需用户显式确认才降级
- ❌ 重试时换新 `Nats-Msg-Id` —— 必须复用，否则 broker 去重失效
- ❌ 元信息塞进 payload JSON envelope（`id` / `source` / `time` 等）—— 必须走 Headers
- ❌ 未读缓存就重复询问 `broker_url` / `service_source` 等基础信息
- ❌ 契约不存在就直接发 —— 必须先起草并提示 commit

---

## 与其他资产关系

- **结构契约标尺**：[specs/nats-messaging.md](../../specs/nats-messaging.md)——subject / headers / payload / QoS / 校验规则的权威
- **契约文档骨架**：[specs/cross-team-contract.md](../../specs/cross-team-contract.md)——首次起草契约时套用其 frontmatter + 章节结构
- **消费侧配套**：[consume-nats-message](../consume-nats-message/SKILL.md)——同一契约的另一端
- **broker 行为权威**：<https://docs.nats.io>——NATS protocol / JetStream / Services API 以官方为准
