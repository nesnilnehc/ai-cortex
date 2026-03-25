# 协议索引 (Protocols Index)

本文档是 **AI Cortex** 所有协议（Protocol）的权威注册表。

**协议（Protocol）定义**：交互流程、各步骤约束、应用哪些 Rule（"怎么做"）。

详见 [specs/terminology.md](../specs/terminology.md)。

## 相关文档

- `specs/INDEX.md` — Spec 规范索引（定义"是什么"）
- `specs/terminology.md` — 四层治理资产的完整定义
- `specs/protocol.md` — Protocol 规范本身的文档标准
- `manifest.json` — Protocol 注册和 canonical URL

---

## 📖 快速开始

### 👤 对于人类用户

- **快速 5 分钟了解**：[快速参考卡](../../docs/guides/protocols-quickstart.md)
- **深入 30 分钟学习**：[完整使用指南](../../docs/guides/protocols-usage.md)
- **查看代码示例**：[使用指南 §4](../../docs/guides/protocols-usage.md#4-使用场景和示例)

### 🤖 对于 AI Agent

- **Agent 如何自动使用协议**：[Agent 驱动指南](../../docs/guides/protocols-agent-usage.md)
  - 自动发现、加载、应用协议
  - Skill 集成和协议声明
  - 代码生成和自动验证

**推荐阅读顺序**：
- Agent Builders → 从 [Agent 驱动指南](../../docs/guides/protocols-agent-usage.md) 开始
- 项目用户 → 从 [快速参考](../../docs/guides/protocols-quickstart.md) 或 [完整指南](../../docs/guides/protocols-usage.md) 开始

---

---

## 协议列表 (Registry)

表中「版本」为内容的语义化版本。详见 [specs/protocol.md](../specs/protocol.md) §2.2。

| 协议名 | 分类 | 版本 | 状态 | 描述 |
|:---|:---|:---|:---|:---|
| [IM Notification Delivery Protocol](./im-notification-delivery.md) | notification | `1.0.0` | active | 定义通知的渲染和投递流程到 IM 渠道（Feishu、WeCom 等）。定义"怎么做"（HOW）。|

### Notification Stack

| 名称 | 类型 | 层级 | 版本 | 核心价值 | 适用场景 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [UNP](./unp.md) | Spec | 语义层 | `1.0.0` | 定义通知的结构、意图、优先级（channel-agnostic） | 所有通知系统的设计与审查 |
| [INP](./inp.md) | Protocol | 投递层 | `1.0.0` | 定义 UNP 通知如何渲染、路由、投递到 IM 渠道 | IM 渠道（Feishu、WeCom）的实现 |

**关系**：
- UNP（规范）：定义通知对象有哪些字段和结构 → **WHAT**
- INP（协议）：定义通知如何从 UNP 对象流向 IM 渠道的步骤 → **HOW**
- 两者通过共同的 `priority` 和 `intent` 字段耦合

### Requirements

| 名称 | 类型 | 适用范围 | 版本 | 核心价值 | 适用场景 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [Requirement Modeling Spec](./requirement-modeling/PROTOCOL.md) | Spec | 需求建模 | `1.0.0` | 定义 7 个必填字段、5 维度自检清单、标准验收标准格式（Gherkin BDD）和风险评估方法 | 功能需求、非功能需求、缺陷修复、技术任务的标准化建模 |

**特点**：
- 包含 7 个必填字段和可选字段的完整框架
- 提供 5 维度（完整性、可执行性、清晰性、合理性、可追踪性）的质量检查清单
- 支持不同需求类型的简化指引（缺陷修复、技术任务等）
- 包含 AI 自动化校验和重构指令

---

## 3. 使用规范

协议应作为：

1. **接口契约**（Interface Contract）：在系统设计/审查时，确保通知系统严格遵循协议定义。
2. **实现基准**（Implementation Reference）：在编码时，UNP 作为对象模型，INP 作为渲染规则。
3. **审查清单**（Review Checklist）：使用 `review-notifications` 技能审查通知相关代码/设计。

---

## 4. 生命周期

| 状态 | 含义 | 操作 |
| :--- | :--- | :--- |
| `active` | 当前活跃，新项目应采纳 | 遵循，反馈 |
| `living` | 允许有 breaking changes（需明确通知） | 关注更新 |
| `deprecated` | 不再推荐，向后兼容期 | 考虑迁移 |
| `retired` | 不再维护 | 不建议使用 |

---

## 5. 参考与工具

- **审查工具**：技能 `review-notifications` 可自动检查代码是否符合 UNP/INP 规范
- **协议演进**：协议更新时，版本号递增；`CHANGELOG.md` 记录 breaking changes
- **反馈**：发现协议缺陷或改进建议，请向本项目提 issue

---

## 参考

| 项目 | 说明 |
| :--- | :--- |
| Spec 来源 | [AI Cortex](https://github.com/nesnilnehc/ai-cortex) |
| 协议注册表 (Raw) | <https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/protocols/INDEX.md> |
