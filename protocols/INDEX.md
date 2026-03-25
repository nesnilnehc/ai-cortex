# 领域协议索引 (Protocols Index)

本文档定义了 AI Cortex 中所有对外发布的领域协议规范。这些协议定义了特定问题域（如通知系统）的标准接口契约。

## 英文摘要 (English Summary)

- 本文件为 `protocols/` 下领域协议规范的规范注册表。
- 这些协议跨项目可用，在消费者系统中实现时需遵循。
- 与 UNP/INP 协议栈的关系：UNP 定义语义层（WHAT），INP 定义投递层（HOW）。

---

## 📖 快速开始

**我想...**

- **了解协议是什么**：阅读下方的 [核心概念](#1-协议分类)
- **使用通知协议**：查看 [UNP](./unp.md) 和 [INP](./inp.md)
- **在项目中集成**：按照 [完整使用指南](../../docs/guides/protocols-usage.md) 操作
- **获取示例代码**：见 [协议使用指南 §4](../../docs/guides/protocols-usage.md#4-使用场景和示例)

---

## 1. 协议分类

| 分类 | 描述 | 状态 |
| :--- | :--- | :--- |
| `notification` | 通知系统的协议栈（语义层 + 投递层） | 活跃 |

---

## 2. 协议列表 (Registry)

表中「版本」为协议内容的语义化版本。重大约束变更或结构性调整时递增主/次版本，勘误或措辞优化可仅递增修订号。

### Notification Stack

| 协议名称 | 层级 | 版本 | 核心价值 | 适用场景 |
| :--- | :--- | :--- | :--- | :--- |
| [UNP](./unp.md) | 语义层 | `1.0.0` | 定义通知的结构、意图、优先级；channel-agnostic | 所有通知系统设计与审查 |
| [INP](./inp.md) | 投递层 | `1.0.0` | 定义 UNP 通知如何渲染、路由、投递到 IM 渠道 | IM 渠道（Feishu、WeCom）的实现 |

**关系**：
- UNP 是上游（业务/应用层制造 UNP 对象）
- INP 是下游（投递层消费 UNP，转换为渠道特定格式）
- 两者通过共同的 `priority` 和 `intent` 字段耦合

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
