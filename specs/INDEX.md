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
| [Linking Modes Reference](./linking-modes.md) | linking | `2.0.0` | informational | 6 项链接模式 taxonomy（slug / colocation / parent-pointer / manifest / mixed / none）描述性参考；v2.0 降级为文档（团队沟通 / 审计参考用），不再是运行时配置对象——v1.0 的 discover/define/plan-next 协同消费已随 ADR 005 回撤。|
| [Artifact Contract](./artifact-contract.md) | artifact | `4.0.0` | active | 产出文档制品的契约；§8 Runtime Norms Resolution Protocol 规定技能运行时读项目规范 / 占位符语法 / 错误处理；v4.0 回撤 §8.4 linking-mode 输出真值表，保留 path_pattern 覆盖机制（ADR 005）。|
| [Artifact Norms Schema](./artifact-norms-schema.md) | artifact | `2.0.0` | active | 项目级制品规范文件字段集与语法；v2.0 废弃 §6 `linking_mode` 字段（ADR 005）；保留 path_pattern 覆盖与占位符语法。|

---

## 相关文档

- `specs/terminology.md` — 四层治理资产（Spec、Protocol、Skill、Rule）的完整定义
- `specs/protocol.md` — Protocol 规范（规范文档规范）
- `specs/skill.md` — Skill 规范
- `manifest.json` — Spec 注册和 canonical URL
