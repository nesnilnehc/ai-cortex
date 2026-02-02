# 项目定位 (Positioning)

本仓库是能力资产库本体：沉淀 Skills / Rules / Commands，并提供 Spec、测试与入口契约。除本文档外，不再维护额外的“愿景/架构/快速开始”等说明文档。

---

## 一句话定位

AI Cortex 是面向 Agent 的可治理能力资产库：用 Spec 与测试把 Skills / Rules / Commands 变成可复用、可审计、可组合的工程资产。

## 解决的问题

- **碎片化**：能力逻辑散落于零散文本与上下文，难以复用与演进。
- **不可验证**：缺少结构与质量契约，回归风险不可控。
- **不可治理**：能力边界不清，变更难审计，协作成本高。

## 核心原则

- **Contract-first**：以 `spec/` 定义结构、元数据与质量要求。
- **可验证**：以 tests 与 Self-Check 作为最低交付保障。
- **可组合**：以 Commands 与 related_skills 支持从原子能力到工作流的复用。
- **可发现**：以各类 `INDEX.md` 与 `manifest.json` 提供稳定索引与元数据。

## 边界（非目标）

- 不提供 IDE/Agent/CI 的集成与使用指南，也不提供安装或同步脚本。
- 不绑定任何 IDE 或运行时框架，不做专属适配。
- 不沉淀与单一项目强耦合、无法泛化的提示词碎片。
- 不实现模型调用、工具执行与运行时编排的基础设施。

## 资产与权威链

| 你想知道什么 | 看哪里（权威来源） |
| :--- | :--- |
| 资产怎么写、质量要求是什么 | `spec/skill.md`、`spec/rule.md`、`spec/command.md`、`spec/test.md` |
| 有哪些能力资产 | `skills/INDEX.md`、`rules/INDEX.md`、`commands/INDEX.md` |
| 可执行能力清单与元数据 | `manifest.json` |
| Agent 在本仓库内应遵守什么契约 | `AGENTS.md` |
| 给 Agent 的机器可读导航 | `llms.txt` |
