# 全局规则索引 (Rules Index)

本文档定义了 AI Cortex 中所有跨技能生效的全局行为准则（Passive Constraints）。

---

## 1. 规则分类

| 分类 | 描述 |
| :--- | :--- |
| `writing` | 定义文本输出的语调、术语和排版规范。 |
| `security` | 定义数据处理、隐私边界和合规性要求。 |
| `interaction` | 定义 Agent 与用户的交互深度与反馈机制。 |

---

## 2. 规则列表 (Registry)

| 规则名称 | 版本 | 核心价值 | 适用场景 |
| :--- | :--- | :--- | :--- |
| [chinese-technical-standard](./chinese-technical-standard.md) | `1.2.0` | 规范中文技术写作，对齐工业级排版与术语。 | 所有中文输出场景 |

---

## 3. 使用规范
规则应作为“长期背景”注入 AI 运行时。在执行任何原子技能（Skill）时，规则定义的约束具有最高优先级。
