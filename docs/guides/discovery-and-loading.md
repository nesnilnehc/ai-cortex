---
artifact_type: guide
created_by: ai-cortex
lifecycle: living
created_at: 2026-03-24
status: active
---

# 技能发现与加载细则

本文档描述 Agent 在本仓库内发现与加载**技能**时的细则，供需要时查阅。AGENTS.md 仅保留摘要。

> **注**：协议（Protocols）与规则（Rules）的发现加载见 [protocols-registry.md](protocols-registry.md) 与 AGENTS.md §4。

---

## 1. 资产根

当前仓库根、本文件所在仓库根，或显式提供的 Raw 根 URL。

---

## 2. 发现流程

1. 阅读 `skills/INDEX.md` 与 `manifest.json` 获取能力清单与路径。
2. 按任务语义匹配技能（参考 SKILL 的 `description`、`tags`、`triggers`）。
3. 使用需求、设计、报告等显式制品传递上下文，避免隐式上下文；链式调用时遵循各技能 prose 中的 Handoff Point 与 Scope Boundaries。

---

## 3. 匹配优先级（多源同时适用时）

1. SKILL 的 `triggers`（frontmatter）精确匹配
2. `description` / `tags` 语义匹配

---

## 4. 路由规则

- 主技能优先：每个请求先路由到主技能；仅当主技能输出暴露明确缺口时再调用可选技能。
- 升级规则：一周期内多意图活跃时，将编排升级至 `plan-next`。
- 制品移交：使用需求、设计、对齐、文档就绪报告等显式制品传递上下文，避免隐式上下文。
- 默认值：若存在 `input_schema.defaults` 且用户未显式输入，使用该默认值。

---

## 5. 注入

将所选 SKILL 的**完整 Markdown** 作为系统或上下文加载；按原子单元注入。

---

## 6. 自引用

在本仓库工作时，用 `manifest.json` 的 `capabilities` 获取技能路径；发现并加载 `skills/` 下资产。
