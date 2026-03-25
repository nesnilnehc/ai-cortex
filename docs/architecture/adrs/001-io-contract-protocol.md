---
artifact_type: adr
created_by: decision-record
lifecycle: snapshot
created_at: 2026-03-24
status: active
---

# ADR 001：技能链 I/O 契约协议

**状态**：Accepted
**日期**：2026-03-06
**上下文**：specs/skill.md v2.1.0，roadmap Layer C（Orchestration & Composition）

## 背景

技能产出可能被其他技能或编排器消费的输出（findings、报告、文档）。若无标准方式描述输入与输出类型，编排器与技能链须依赖隐式知识将上游输出与下游输入匹配。

## 决策

在 specs/skill.md 的 YAML frontmatter 中采用可选 `input_schema` 与 `output_schema`。Artifact 类型包括：`findings-list`、`document-artifact`、`diagnostic-report`、`code-scope`、`free-form`。

编排器使用这些 schema 以：

1. 自动将上游 output 类型与下游 input 类型匹配
2. 在执行前校验 handoff 兼容性
3. 在不阅读各技能正文的情况下文档化数据流

## 后果

- **正面**：编排器（run-checkpoint、review-code）可按类型路由；新技能声明 I/O 以提升可发现性
- **负面**：需额外维护元数据；schema 粒度可能随时间需细化
- **中性**：可选 —— 无 I/O schema 的技能仍有效；向后兼容

## 参考

- specs/skill.md § I/O contracts
- [Evolution Roadmap](../../designs/2026-03-02-ai-cortex-evolution-roadmap.md) C8 Skill Chain & Workflow Protocol
