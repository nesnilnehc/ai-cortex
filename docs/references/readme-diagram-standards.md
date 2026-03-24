---
artifact_type: reference
created_by: ai-cortex
lifecycle: living
created_at: 2026-03-24
status: active
---

# README 图表设计标准

**版本**：1.0.0
**目的**：为项目 README 中的可视化沟通建立标准，确保清晰、可维护与可访问。

---

## 1. 核心原则

1. **语义优先 (Semantic-First)**：图表必须传达含义（逻辑、流程、结构），而非仅作装饰。
1. **原生渲染 (Native Rendering)**：优先使用基于代码的图表（Mermaid）而非二进制图片（PNG/SVG），以利于版本控制与可搜索性。
1. **极简 (Minimalism)**：每张图表只回答一个问题（「这是什么？」、「如何工作？」、「内部结构？」）。
1. **可访问性 (Accessibility)**：所有图表须有伴随文字说明，或通过标签自解释。

---

## 2. 图表类型与用途

| 类型 | 目的 | 回答的问题 | 推荐格式 |
| :--- | :--- | :--- | :--- |
| **概念图 (Concept Diagram)** | 高层架构、实体与关系 | 「这是什么系统？」 | Mermaid Flowchart (LR/TB) |
| **工作流图 (Workflow Diagram)** | 动态流程、用户交互、数据流 | 「如何使用？」 | Mermaid Sequence 或 Flowchart |
| **生态/拓扑图 (Ecosystem/Topology)** | 组件目录、分组与规模 | 「有哪些能力？」 | Mermaid Graph (TB) 或 Mindmap |

---

## 3. 技术标准

### 3.1 格式优先级

1. **Mermaid（`.mmd` 内嵌）**：首选。GitHub 原生渲染。*优点*：可编辑、可 diff、主题自适应（浅色/深色）。*缺点*：样式控制有限。
1. **SVG（矢量）**：次选，用于复杂品牌或非常规布局。*要求*：须在 `docs/designs/` 中包含源文件（如 `.drawio`、`.excalidraw`）。
1. **PNG/JPG（位图）**：避免用于图表；仅用于截图或照片。

### 3.2 Mermaid 风格指南

- **方向**：
  - 流程与时间线使用 `LR`（左到右）。
  - 层级与生态图使用 `TB`（上到下）。
- **节点**：标签简洁清晰，避免长文本块。
- **类**：优先使用语义类名（`classDef user`、`classDef system`）而非硬编码颜色，以支持未来主题化。

### 3.3 复杂度限制

- **最大节点数**：约 15 个/图。超出时拆分子图或使用高层抽象。
- **最大深度**：3 层嵌套（subgraphs）。

---

## 4. README 标准图表集

专业基础设施项目的 README 宜包含：

1. **「概念」图（横幅/简介）**：简单的输入-处理-输出模型。*目标*：用户在 5 秒内理解价值主张。
1. **「流程」图（用法）**：典型用户交互路径。*目标*：用户理解运行机制。
1. **「生态」图（功能/目录）**：可用能力一览。*目标*：用户看到工具广度。

---

## 5. 维护

- 图表即代码。须在与所描述功能变更相同的 PR 中更新。
- 过时图表须删除或归档。
- `docs/images/*.mmd` 为 README 中 Mermaid 块的权威来源。保持 README 与源文件同步。
- 提交前运行 `npm run verify:diagram-sync` 防止漂移。
