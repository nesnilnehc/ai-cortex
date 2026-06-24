---
artifact_type: rule
name: diagram-selection
version: 1.0.0
created_by: ai-cortex
lifecycle: living
created_at: 2026-06-24
recommended_scope: user
status: active
---

# Rule: 图表选型（Diagram Selection）

> 画技术图表时的判据：先判关系类型选图，再跨工具选型，最后避渲染坑、按需拆多图。
>
> **定位**：本 rule 管「判断」（选哪种图 / 哪个工具 / 能否渲染 / 该不该拆），不管「形状」（设计文档必须含哪种图归 [specs/functional-design-modeling.md](../specs/functional-design-modeling.md) 与 [specs/technical-design-modeling.md](../specs/technical-design-modeling.md)），也不教语法（PlantUML / Mermaid / Graphviz 语法属通用知识）。
>
> **生效时机**：任何画图动作——设计文档内嵌流程图 / 状态图、或临时出一张图——都援引本判据。

---

## 1. 适用范围

用文本绘图工具（PlantUML / Mermaid / Graphviz / flowchart.js）产出技术图表的任何场景。聚焦选型与可渲染性，不约束图的业务内容正确性。

---

## 2. 第一步：按关系类型选图

一张好图只回答一个主要问题。先判断「要表达哪类关系」，再定图类型——不要让一张图同时承担多个解释任务。

| 要表达的关系 | 图类型 | 首选工具 |
| :--- | :--- | :--- |
| 顺序（一步步怎么发生） | 流程图、活动图、用户旅程图 | Mermaid、PlantUML |
| 交互（谁和谁按什么顺序） | 时序图 | PlantUML、Mermaid |
| 状态（对象有哪些态、怎么迁移） | 状态图 | PlantUML、Mermaid |
| 结构（系统由哪些部分组成） | C4 图、组件图、类图、ER 图 | PlantUML、Mermaid |
| 部署与网络 | 部署图、拓扑图、依赖图 | PlantUML、Graphviz |
| 时间计划 | 甘特图、时间线 | Mermaid、PlantUML |
| 拆解（任务 / 知识层级） | WBS、Mindmap、树形 | PlantUML、Mermaid |
| 复杂关系（多节点多边） | 有向图、无向图、知识图谱 | Graphviz |
| 数值（数量 / 流量 / 比例） | Sankey、XY Chart、Radar、Treemap | Mermaid |

按读者调抽象层级：面向业务方少节点少术语（流程图 / 用户旅程图 / 时间线）；面向研发保留服务名 / 接口名 / 状态名 / 异常分支（C4 / 组件图 / 时序图 / 状态图）；面向运维强调部署位置 / 依赖 / 调用链（拓扑图 / 部署图 / 依赖图）。

---

## 3. 第二步：跨工具选型启发式

默认 Mermaid，仅在命中下表条件时才离开它。不要凭「能不能画」选，要看可渲染性与长期维护。

| 条件 | 选型 |
| :--- | :--- |
| 文档内嵌、上手快、README / 博客 / 知识库 / 轻量方案 | **Mermaid**（默认） |
| 正式工程建模：UML / C4 / 部署 / 活动图，进设计文档 | **PlantUML** |
| 节点与边数量大、需自动布局：依赖图 / 调用链 / 拓扑 / 知识图谱 | **Graphviz** |
| 仅网页内展示简单标准流程，且不需要其他图类型 | **flowchart.js** |

平台已统一文档工具时，先看平台支持的渲染版本——Mermaid 尤其要注意版本差异。

Graphviz 选对布局引擎：`dot`（分层有向图 / 依赖图 / 调用链）、`neato` / `fdp`（一般网络与无向图）、`sfdp`（大规模图）、`circo`（环形 / 循环关系）、`twopi`（径向 / 中心扩散）、`osage`（分组集群）。

---

## 4. 渲染避坑清单

产出的图必须能在目标平台渲染。落盘前自检：

- [ ] **Mermaid 保留词加引号**：节点文字含 `end` 等保留词或特殊符号易被解析器吃掉，统一加引号
- [ ] **确认平台 Mermaid 版本**：嵌入前核对目标平台支持的 Mermaid 版本，避免新语法在旧渲染器失败
- [ ] **复杂流程换 ELK 布局**：线条交叉多时，flowchart / state diagram 改用 ELK 布局减少交叉
- [ ] **PlantUML 渲染链可达**：PlantUML 依赖 Java / 渲染器，纯文档平台不一定能渲染，选前确认渲染链
- [ ] **CI 渲染或校验**：长期维护的图优先选团队熟悉、CI 能渲染或校验的文本 DSL

---

## 5. 多图拆分约束

- 一张图只回答一个核心问题；超过一屏还看不清时，停止调样式，**拆图**
- 常见拆法：业务流程图 + C4 / 组件图 + 时序图 + 部署图，各自独立成图
- 图名描述结论而非类型（「订单状态流转图」优于「状态图」）
- 节点名用稳定的业务概念或系统边界，不用临时代码变量名
- 只是字段清单 / 接口参数 / 简单对比时，用表格而非图——只有关系 / 顺序 / 层级 / 依赖 / 状态迁移 / 数量流向是重点时，图才有价值

---

## 反模式

- ❌ 不判关系类型就条件反射上 Mermaid
- ❌ 一张图回答多个问题
- ❌ 大图靠调样式硬塞而不拆
- ❌ 图名只写类型不写结论
- ❌ 简单清单 / 对比用图而非表格
- ❌ 嵌入前不确认平台 Mermaid 版本，导致渲染失败
- ❌ 节点名用临时变量名，图随代码漂移失去长期可读性

---

## 关联资产

- **设计评审 rule**：[functional-design-quality](./functional-design-quality.md) / [technical-design-quality](./technical-design-quality.md)——设计文档嵌流程图 / 状态图时援引本判据
- **设计数据契约**：[specs/functional-design-modeling.md](../specs/functional-design-modeling.md) / [specs/technical-design-modeling.md](../specs/technical-design-modeling.md)——定义「制品必须含哪种图」，本 rule 与之互补（spec 说形状，本 rule 说判断）
- **中文写作**：[writing-chinese-technical](./writing-chinese-technical.md)

---

## 变更记录

### 1.0.0 — 2026-06-24

**Initial Release**：定义图表选型判据——关系类型 → 图类型 → 工具的速查表、跨工具选型启发式（默认 Mermaid，何时离开）、渲染避坑清单、多图拆分约束。
