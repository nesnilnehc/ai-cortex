---
artifact_type: architecture
created_by: ai-cortex
lifecycle: living
created_at: 2026-03-24
status: active
---

# 架构

AI Cortex 架构由 [Evolution Roadmap](../designs/2026-03-02-ai-cortex-evolution-roadmap.md) 的 Layer A–E 模型定义。

## 层级

| 层级 | 范围 |
| :--- | :--- |
| **A** | Engineering Infrastructure（工程基础设施）— CI/CD、质量门 |
| **B** | Skill Coverage（技能覆盖）— 语言、框架、库 |
| **C** | Orchestration & Composition（编排与组合）— 编排器、技能链 |
| **D** | Ecosystem & Distribution（生态与分发）— Plugin 同步、社区 |
| **E** | Specification Evolution（规范演进）— 生命周期、可测试 Spec |

## Canonical 来源

- **[Evolution Roadmap](../designs/2026-03-02-ai-cortex-evolution-roadmap.md)** — 层级定义、组件、实施阶段
- **[skills/INDEX.md](../../skills/INDEX.md)** — 技能目录、用途与依赖关系入口
- **[specs/skill.md](../../specs/skill.md)** — 技能结构与元数据 Spec

## ADR

| ADR | 标题 | 状态 |
| :--- | :--- | :--- |
| [001](adrs/001-io-contract-protocol.md) | I/O Contract Protocol for Skill Chaining（技能链 I/O 契约协议） | Accepted |

## 何时扩展

在以下情形添加 ADR（如 `docs/architecture/adrs/002-*.md`）：

- 重大设计决策需显式 rationale
- `design-solution` 产出经批准的、值得持久化的架构选择
- 跨技能或跨阶段依赖需文档化
