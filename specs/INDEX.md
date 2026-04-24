# 规范索引 (Specifications Index)

本文档是 **AI Cortex** 所有规范（Spec）的权威注册表。

**规范（Spec）定义**：数据结构、必需字段、接口契约（"是什么"）。

详见 [specs/terminology.md](../specs/terminology.md)。

---

## 规范列表 (Registry)

表中「版本」为内容的语义化版本。详见 [specs/protocol.md](../specs/protocol.md) §2.2。

| 规范名 | 类别 | 版本 | 状态 | 描述 |
|:---|:---|:---|:---|:---|
| [Universal Notification Protocol](./universal-notification.md) | notification | `1.0.0` | active | 定义通知的结构、必需字段、语义层（WHAT）。与 INP 协议栈配套。|
| [Requirement Modeling Spec](./requirement-modeling/SPEC.md) | requirements | `1.0.0` | active | 定义需求的 7 个必填字段、5 维审查清单、BDD 验收标准格式。|
| [Artifact Contract](./artifact-contract.md) | artifact | `5.0.0` | active | 产出文档制品的契约；§2 定义 canonical 制品类型与路径（v5.0 统一 requirements/designs/tasks 为 `docs/<type>/{slug}.md`）；§8 Runtime Norms Resolution Protocol 规定技能运行时读项目规范 / 占位符语法 / 错误处理 / 部分覆盖合并（ADR 006）。|
| [Artifact Norms Schema](./artifact-norms-schema.md) | artifact | `3.0.0` | active | 项目级制品规范文件字段集与语法；`path_pattern` 覆盖 + 占位符语法是项目定制 canonical 路径的唯一机制。|

---

## 相关文档

- `specs/terminology.md` — 四层治理资产（Spec、Protocol、Skill、Rule）的完整定义
- `specs/protocol.md` — Protocol 规范（规范文档规范）
- `specs/skill.md` — Skill 规范
- `manifest.json` — Spec 注册和 canonical URL
