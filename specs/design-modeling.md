---
id: DESIGN_MODELING_SPEC_V1
name: Design Modeling Schema
description: Spec defining design document fields, formats, and validation rules. Covers required structural sections, frontmatter contract, and traceability to requirements.
version: 1.0.0
status: active
lifecycle: living
created_at: 2026-05-09
scope: |
  Defines the structural contract for design documents: required sections, optional sections,
  field formats, and frontmatter. Applies to architectural designs, component designs,
  data flow specifications, and trade-off analyses derived from validated requirements.
related:
  - ./requirement-modeling.md
  - ./task-modeling.md
  - ../rules/design-quality.md
---

# 设计建模规范

> **数据契约**：定义设计文档的结构与字段
>
> 配套：质量评审见 [rules/design-quality.md](../rules/design-quality.md)；任务派生见 [specs/task-modeling.md](./task-modeling.md)

---

## 适用范围

适用于以下设计建模：

1. **架构设计**：系统层、组件层、模块层架构
2. **组件设计**：单一组件的接口、数据流、状态
3. **变更设计**：现有系统的修改方案
4. **集成设计**：跨服务 / 跨系统集成方案

---

## 必填结构（8 节）

### 1. 目标（Goal）

**用途**：陈述设计要解决的问题与成功状态。

**校验**：

- 不超过 200 字符
- 不含实现细节
- 与上游 requirement 的目标一致

### 2. 架构（Architecture）

**用途**：描述系统 / 组件的层次、边界、职责划分。

**典型形式**：分层图、C4 模型、模块依赖图。

**校验**：

- 含至少一种结构化表达（图、表、列表）
- 标注外部依赖与内部依赖

### 3. 组件（Components）

**用途**：列出设计中的关键组件及其职责。

**字段**（每个组件）：名称、职责、依赖、对外接口。

**校验**：

- 至少 1 个组件
- 每个组件职责单一可述

### 4. 数据流（Data Flow）

**用途**：描述数据如何在组件间流动。

**典型形式**：序列图、流程图、状态图。

**校验**：

- 关键路径数据流必须标注
- 错误路径与正常路径分开

### 5. 错误处理策略（Error Handling Strategy）

**用途**：列出关键失败路径与处理方法。

**校验**：

- 至少 2 条关键失败路径
- 每条标注：失败条件、检测方式、恢复策略

### 6. 测试策略（Test Strategy）

**用途**：声明验证方法（**不写测试代码**）。

**校验**：

- 含测试层次（单元 / 集成 / 端到端 之一或多个）
- 含验收方式（自动化 / 人工）
- 不含具体测试代码

### 7. 权衡分析（Trade-offs）

**用途**：记录考虑过的替代方案与选择理由。

**校验**：

- 至少 2 种替代方案
- 每种方案含：优点 / 缺点 / 是否选用 + 理由

### 8. 验收标准（Acceptance Criteria）

**用途**：定义设计完成的可验证条件，可追溯到需求。

**格式**：Gherkin BDD 或清单。

**校验**：

- 每条可追溯至上游 requirement 的某条 acceptance criteria
- ≥ 3 条

---

## 可选结构

### 9. 范围定义（Scope）

明确设计覆盖与不覆盖的边界。

### 10. 风险与假设（Risks & Assumptions）

设计层面的技术风险与依赖假设。

### 11. 关联文档（References）

相关 ADR、外部规范、参考资料链接。

---

## Frontmatter 契约

```yaml
---
artifact_type: design
lifecycle: snapshot
created_at: YYYY-MM-DD
parent: <path to upstream requirement document>
status: draft | approved | superseded
---
```

**字段**：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `artifact_type` | string | 必 | 固定 `design` |
| `lifecycle` | enum | 必 | `snapshot`（设计是时点决策） |
| `created_at` | date | 必 | 设计完成日期 |
| `parent` | path | 必 | 上游 requirement 文档路径 |
| `status` | enum | 必 | `draft` / `approved` / `superseded` |

---

## 反模式

- ❌ 含代码或脚手架（设计不写实现）
- ❌ 单一方案不做权衡
- ❌ 无验收标准（无法追溯到需求）
- ❌ 测试策略写测试代码而非验证方法
- ❌ 无 `parent` frontmatter（孤立设计）

---

## 关联标准

- **IEEE 1016**：Software Design Description Standard
- **C4 Model**：Context / Container / Component / Code 分层
- **ADR**：Architecture Decision Record（设计中决策可派生为 ADR）
