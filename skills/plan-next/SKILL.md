---
name: plan-next
description: Analyze governance state and produce next-action routing plan from existing docs; read-only — never executes downstream skills.
description_zh: 基于现有治理文档分析状态并输出下一步路由计划；只读——不执行下游技能。
tags: [workflow, meta-skill, automation]
version: 10.1.0
license: MIT
recommended_scope: project
cognitive_mode: interpretive
metadata:
  author: ai-cortex
triggers: [plan next, next step, checkpoint, governance, iteration]
input_schema:
  type: free-form
  description: Governance docs sources, optional scope, optional threshold overrides.
  defaults:
    thresholds:
      task_stuck_days: 7
    task_source: auto
    roadmap_tier_source: docs/process-management/roadmap.md
    artifact_norms_path: docs/ARTIFACT_NORMS.md
output_schema:
  type: chat
  description: "Three-section report. Sections 1-2 (Now do / Also watch) are jargon-free natural language: no internal codes (L1-L5, G1-G4, P0-P3), no Chinese translations of those codes (资产缺失/真相漂移/内容不全/etc.), no raw status values (pending/blocked/etc.), no layer names (目标层/需求层/etc.). Section 3 (Diagnosis) is a technical traceability zone where internal codes are allowed."
---

# 技能：计划下一步（Plan Next）

> **角色**：治理入口路由器
> **WHAT**：按三步法 **扫**（盘点治理资产）→ **诊**（目标树遍历——逐目标深度优先找首个未完成节点，结合并行判定）→ **荐**（产出三节路由报告）
> **HOW**：只读诊断；单一维度问题（只查就绪度 / 漂移 / 已知缺失）直接调专用技能（`assess-docs` / `align-planning` / `define-*` 等）
> **区别**：不同于 `assess-docs`（深度文档评估）或 `align-planning`（漂移校准），本技能仅做路由分发，不做深度分析

---

## 目的与边界

盘点治理输入源并生成下一步行动路由。

**适用时机**：迭代收尾 / 发布前治理路径确认 / 输入源缺失补齐 / 对下一步无头绪时。其他场景见头部 HOW。

### 边界

| 维度 | 做 | 不做 |
|---|---|---|
| 路由 | 输出"现在该做"治理路由建议 | 不充当任务状态 API；不维护任务列表 / 不分配；不记任务历史，不答"本周晋升几条"类时序问题 |
| 执行 | 只读——产路由建议交用户或外层编排器 | 不自动推进下游；不充当自动化引擎——自动化由外层编排器 + `loop` 组合驱动 |

---

## 行为

**整体规则**：**无状态**——每次从零重扫，不依赖上次结果。三步法：**扫 → 诊 → 荐**。

### 步骤 0：规范解析

按 [artifact-contract §8.2](../../specs/artifact-contract.md#82-发现顺序) 顺序读项目规范到 `cache`：依序检查 `artifact_norms_path`（输入）→ `.ai-cortex/artifact-norms.yaml` → `docs/ARTIFACT_NORMS.md`，YAML 畸形则 HALT 诊断；缺失则继续不报错。`cache` 用于步骤 2.1 的 `path_pattern` 解析。

### 步骤 1：扫 — 资产盘点

**扫什么**：3 抽象层 × 5 主题（联合 MECE）。

| 抽象层 | 主题 | 扫描位置 | 细化字段 |
|---|---|---|---|
| 意图层 | **Why** | `docs/project-overview/{mission,vision,north-star,strategic-goals,strategic-pillars}.md` | — |
| 意图层 | **What/When** | `docs/process-management/{roadmap,backlog/}.md`、`docs/requirements/`、`docs/tasks/` | 路线图 → 节点状态；tasks/ → `status` |
| 意图层 | **How** | `docs/architecture/adrs/`、`docs/designs/` | `status` |
| 实施层 | **Is** | 仓库代码 | — |
| 元规则层 | **Rules** | `docs/ARTIFACT_NORMS.md`、`specs/`、`protocols/`、`rules/` | — |

抽象层互斥；细化字段是同主题的辅助维度，**不是独立扫描**，供 §2.1 消费。

**怎么扫**——对每项资产记录 2 字段：

| 字段 | 判据 |
|---|---|
| **路径** | 文件系统路径 |
| **状态** | `present`（存在且内容非空非占位）/ `placeholder`（仅含 `[TODO]`/`<待填>`/`TBD`）/ `missing`（不存在） |

### 步骤 2：诊 — 目标树遍历

**核心问题**：目标链在哪里卡住了？下一步该专注还是并行？

**模型**：治理制品构成一棵树；"下一步"= 优先级最高目标下，深度优先找首个未完成节点，结合并行判定给出执行建议。

```
战略目标
└── 路线图节点（多个，有顺序）
    └── 需求（多个，每路线图节点下）
        └── 设计/ADR（多个，每需求下）
            └── 任务（多个，每设计下）
```

**2 子步骤**（依次执行）：

| 子步 | 做什么 | 产出 |
|---|---|---|
| 2.0 前置闸门 | Rules 层是否就位？ | 否则短路 |
| 2.1 目标树遍历 | 逐目标深度优先遍历，定位首缺口 + 并行判定 | 每目标的当前位置 + 路由建议 |

G1-G4 缺口类型用作诊断依据节的子标签。

#### 2.0 前置闸门：Rules 层缺位检查

若 `ARTIFACT_NORMS.md` 缺失或 `specs/` 为空，触发**短路**：跳过目标树遍历，"现在该做"只列一条 P0 路由（建立规范 + 重跑 plan-next），"其他可留意"省略。

#### 2.1 目标树遍历

##### 节点状态判定

每个制品节点（路线图节点 / 需求 / 设计 / 任务）的状态按以下规则解析：

1. **显式优先**：读取制品文件 frontmatter 中的 `status:` 字段
   - 有效值：`pending`（默认）| `in-progress` | `done` | `blocked`
2. **子节点推算**（无显式 `status:` 时）：
   - 所有直接子节点 `done` → 当前节点视为 `done`
   - 任一直接子节点 `in-progress` → 当前节点视为 `in-progress`
   - 无子节点 → 视为 `pending`
3. **优先级**：显式字段 > 子节点推算

##### 并行决策规则

在任意层级，扫描该层所有兄弟节点后，按以下规则判定：

| 当前层兄弟节点状态 | 并行建议 |
|---|---|
| 仅 1 个 `in-progress`，其余 `pending` | **专注**：完成当前再启动下一个 |
| 1+ 个 `blocked`，有 `pending` 且独立 | **并行**：blocked 继续等待，启动下一个独立节点 |
| 多个 `in-progress`（均未 blocked） | **收敛**：识别最滞后的，优先推进至完成 |
| 全部 `done` | 触发上层下一兄弟推进 |
| 全部 `pending`，无 `in-progress` | **启动**：路由最高优先级 pending 节点 |

节点间有显式 `depends_on:` 依赖 → 被依赖节点必须先完成，不可并行。

##### 层级定义

| 层级 | 名称 | 存在性判据 | 完成判据 |
|---|---|---|---|
| L1 | 战略目标 | `strategic-goals.md` present 且非占位，含 ≥1 可识别目标项 | 所有目标项 `status = done` |
| L2 | 路线图节点 | 路线图节点存在且可追溯到 L1 某目标 | 节点 `status = done`（显式或子推算） |
| L3 | 需求 | 需求文件 present 且非占位 | `status = done`（显式或子推算） |
| L4 | 设计 | 设计/ADR 文件 present 且非占位 | `status = done`（显式或子推算） |
| L5 | 任务 | 任务记录 present | `status = done` |

**无目标场景**：`strategic-goals.md` 缺失且 `mission.md` 也缺失 → 路由 `define-mission`（P0）；`mission.md` present 但无战略目标 → 路由 `design-strategic-goals`（P0）。

**路线图未分层**：路线图存在但无 Now/Next/Later 分层 → 路由 `promote-roadmap-items`（P1），不继续评估下游。

##### 遍历算法

```
对 每个战略目标 G（按优先级顺序，跳过 status = done 的）：

  [L1] 目标自身 status = done？→ 跳过，检查下一目标

  [L2] 取 G 下所有路线图节点，应用并行决策规则：
    无节点 → 路由: define-roadmap / align-backlog（P1）；停止此目标
    全 done → G 达成；考虑新目标；停止
    取"当前焦点节点"集合 F（依并行决策）

  对 F 中每个节点 N（按优先级）：

    [L3] 取 N 下所有需求，应用并行决策规则：
      无需求 → 路由: analyze-requirements（P2）；停止此节点
      全 done → N 完成；移向下一兄弟路线图节点

    对当前焦点需求 R：

      [L4] 取 R 下所有设计，应用并行决策规则：
        无设计 → 路由: design-solution（P2）；停止此需求
        全 done → R 完成；移向下一兄弟需求

      对当前焦点设计 D：

        [L5] 取 D 下所有任务，应用并行决策规则：
          无任务 → 路由: breakdown-tasks（P2）；停止此设计
          全 done → D 完成；移向下一兄弟设计
          有 blocked 任务 + 有独立 pending 任务 → 并行：路由启动 pending
          有 in-progress 任务（未 blocked）→ 专注：执行中，检测卡点
```

##### 物理扫描方法（L3-L5 存在性检测）

```
2.1.1 从步骤 0 cache 读各 artifact_type 的 path_pattern
      （命中用项目值；未命中 fall back 到技能默认规范路径）
2.1.2 按节点 slug 在各 path_pattern 目录 glob
      → 匹配到 = 存在；未匹配 = G1 缺口
2.1.3 (增强) 扫前置属性 `parent:` 字段构反向索引补充信任度
2.1.4 (增强) 检测清单文件（如 `now/<slug>.md`）
      → 存在则对比清单 vs 物理；差异作 G3 漂移
2.1.5 G1 通过后检查层间内容对应（G3 链路）：
      L3→L4：设计含 parent/upstream_ref 指向需求，或内容明确响应需求关键约束
      L4→L5：任务含 parent 指向设计，或覆盖设计中的主要实现模块
      深度优先：L3→L4 G3 命中则不继续报 L4→L5 G3
```

诊断依据需注明扫描依赖的物理信号组合（例："slug + 检测到 2 个清单 + 无 parent 字段"）。

#### 诊步骤产出物

步骤 3 消费以下产出：

- **每目标遍历结果**：{目标名称, 当前焦点节点, 所在层级, 并行建议, 缺口子标签（G1/G2/G3）, 推荐技能}
- **blocked 节点列表**：[(层级, 节点名, blocked 原因（若有）)]
- **次要发现**：聚焦目标之外的其他发现

### 步骤 3：荐 — 路由生成与分层

**来源**：消费步骤 2 的产出（见"诊步骤产出物"）。

#### 3.1 分层决策

消费 §2.1 产出的每目标遍历结果，将缺口分层：

- **主链路由（最高优先级目标的首缺口）** → "现在该做"（1-3 条）
- **其余目标的首缺口 / blocked 节点** → "其他可留意"（上限 5 条，超出折叠为 "+N more, use --full"）
- **聚焦外发现** → "其他可留意"

**并行路由**：并行决策建议为"并行"或"收敛"时，在路由依据中明确说明并行理由或收敛目标；"专注"时只路由当前节点。

**兄弟推进规则**：当一个节点完成时，自动推进至同层下一兄弟节点，不需要用户重跑；遍历在下一兄弟的首缺口处停止。

#### 3.2 优先级（治理紧迫性）

- **现在（P0）**：阻断其他治理进展的根基问题（Rules 层缺失或 L1 无目标）
- **下次（P1）**：L2 路线图缺失或未对齐目标
- **以后（P2）**：L3-L5 任意层级缺口
- **可忽略（P3）**：其余次要发现

#### 3.3 每条路由五字段

主题 / 推荐技能（含调用提示词）/ 依据 / 优先级标签 / 完成标志。

**主题写法**：一句话说明要做什么、为什么现在做，自然语言，≤30 字（详见 反模式 · 内部术语节）。

**推荐技能写法**：斜杠命令 + 完成提示词，格式：

> `/skill-name [聚焦点：本次要做什么、范围、关键资产路径或任务 ID]`

提示词要求：说明本次调用的具体聚焦点，包含关键资产路径或任务 ID，≤40 字，可直接复制执行。

**优先级标签**（由 §3.2 内部优先级映射，前两节只用标签不用编号）：

| 内部码 | 用户标签 |
|---|---|
| P0 | `紧急` |
| P1 | `重要` |
| P2 | `缓` |
| P3 | `可略` |

**完成标志**：可观测的结果，1 句话；若执行受阻（战略冲突、依赖循环）则追加"受阻时回 plan-next 重评"。

#### 3.3.1 前两节输出禁用词

"现在该做"和"其他可留意"两节，以下词汇**一律禁止出现**——包括编码本身及其中文对应词：

| 禁止使用 | 允许的替代写法 |
|---|---|
| L1、L2、L3、L4、L5；目标层、路线图层、需求层、设计层、任务层 | 直接说"战略目标"、"路线图"、"需求文档"、"设计文档"、"任务" |
| G1、资产缺失 | 描述具体缺什么："`xxx.md` 不存在" |
| G2、内容不全 | 描述具体缺什么内容："缺 X 字段 / X 节" |
| G3、真相漂移、完成漂移、追踪漂移 | 描述具体不一致："任务状态未反映代码进度" |
| G4、位置错位 | 描述具体问题："文件命名不符规范" |
| P0、P1、P2、P3；现在/下次/以后/可忽略（作优先级标注） | 使用 `紧急` / `重要` / `缓` / `可略` |
| pending、in-progress、done、blocked（作用户输出原文） | 说"待开始"、"进行中"、"已完成"、"被阻塞" |
| Rules 层、Why 层、What 层、How 层、Is 层 | 说"规范文件"、"战略文档"、"计划文档"、"设计文档"、"代码实现" |

违反本表 = 输出不合格，须重写违规字段，不得保留。

#### 3.4 用户输出三节

````
# 下一步建议

> **现状**：<项目当前所处阶段与核心问题，≤25 字>

---

## 现在该做

**1. [行动名称]** · `紧急 / 重要 / 缓`

[一句话：做什么、为什么现在做]

- 推荐技能：`/skill-name [聚焦点，≤40 字]`
- 依据：[文件路径或可观测信号，≤20 字]
- 完成标志：[可观测结果，1 句话]

---

**2. [行动名称]** · `优先级标签`

...（格式同上，最多 3 条）

---

## 其他可留意

- **[主题]**：[一句说明] → [建议行动]
- ...（最多 5 条；超出写 "+N 条，加 --full 查看全量"）

---

<details>
<summary>诊断依据（技术追溯）</summary>

<!-- 本节为内部追溯区：L1-L5、G1-G4、P0-P3 及状态码（pending/in-progress/done/blocked）在此处允许使用 -->

- **项目情况**：[一句话摘要]
- **资产清单**：[仅列有状态变化的资产]
- **判定逻辑**：[目标树遍历路径；每目标首缺口层级；并行建议；层级编号可括注作追溯]

</details>
````

**用户 flag**：`--full` 强制全量展示。

---

## 反模式

**关于职责边界**：

- ❌ 调用任何下游技能（只读硬边界）
- ❌ 隐藏跳过原因（短路时必须明示）
- ❌ 混入下游执行细节（不写 ADR、不修代码、不整结构）

**关于路由本身**：

- ❌ 模糊措辞（"可能 / 或许 / 可以考虑"）
- ❌ 省略完成标志
- ❌ 一条路由混多个缺口类型
- ❌ 按缺口数量给优先级
- ❌ 树遍历跳层报告（L2 缺失时直接报 L3 路由）——违反"首缺口优先"
- ❌ 用 git 信号判"完成"——完成判定只看 `status` 字段
- ❌ 忽略显式 `status:` 字段，只用子节点推算——显式优先
- ❌ 有 blocked 节点时不考虑并行启动——blocked 是并行信号
- ❌ 多个 in-progress 未 blocked 时推荐继续并行扩展——应建议收敛
- ❌ 多目标合并路由但未在依据中注明各目标来源
- ❌ 路线图未分层时跳过 `promote-roadmap-items` 直接评估下游
- ❌ 忽略 `depends_on:` 字段强行建议并行——有依赖必须顺序

**关于树遍历与扫描**：

- ❌ 对 done 节点重复报告缺口
- ❌ 同时报同一节点的多层缺口（违反深度优先）
- ❌ 引入 mode 枚举或配置字段（直接看物理信号）
- ❌ 承担清单维护职责（只读，差异作 G3；维护是 `align-work-item-manifest` 的事）

**关于内部术语泄漏**：

- ❌ 前两节出现编码：L1-L5、G1-G4、P0-P3 任一形式
- ❌ 前两节出现编码中文对应词：资产缺失、内容不全、真相漂移、完成漂移、追踪漂移、位置错位、目标层、路线图层、需求层、设计层、任务层、Rules 层、Why 层、What 层、How 层、Is 层
- ❌ 优先级使用旧标签"现在/下次/以后/可忽略"或 P0-P3 编号（改用 `紧急/重要/缓/可略`）
- ❌ status 值原文出现在前两节：pending/in-progress/done/blocked（改用：待开始/进行中/已完成/被阻塞）
- ❌ 诊断依据用层级编号作主语（允许括注追溯，不允许作主语）
- ❌ 示例标题写"L2→L3 推进"（用自然语言场景描述）

---

## 自检

**扫**：

- [ ] 缓存已加载或明示"no norms found"
- [ ] 资产 2 字段齐（路径 + 状态）
- [ ] 路线图是否分层已判定；未分层时已路由 `promote-roadmap-items`

**诊**：

- [ ] 战略目标已读取；无目标时已触发 L1 路由
- [ ] 每个节点的 status 已按"显式优先 > 子节点推算"解析
- [ ] 每个层级的兄弟节点已全量扫描并分类（done / in-progress / blocked / pending）
- [ ] 并行决策规则已应用；建议（专注 / 并行 / 收敛 / 启动）已标注
- [ ] L3-L5 物理扫描完成（glob + 可选 parent: + 可选 manifest）
- [ ] L3→L4 / L4→L5 G3 链路检查已执行；深度优先（上层 G3 命中不继续报下层）
- [ ] "完成"判定仅依赖 status 字段，未引入 git 信号

**荐**：

- [ ] 五字段齐；完成标志齐
- [ ] 优先级标签正确映射（紧急 / 重要 / 缓 / 可略）
- [ ] 深度优先（每目标只报树中首缺口）
- [ ] 并行建议已体现在路由依据中
- [ ] 多目标合并路由时依据中已列所有目标来源

**输出**：

- [ ] 前两节无编码：L1-L5、G1-G4、P0-P3
- [ ] 前两节无编码中文对应词：资产缺失、内容不全、真相漂移、完成漂移、追踪漂移、位置错位
- [ ] 前两节无旧优先级标签：现在/下次/以后/可忽略；优先级统一为 `紧急/重要/缓/可略`
- [ ] 前两节无英文状态码：pending、in-progress、done、blocked
- [ ] 只读已遵守
- [ ] "其他可留意"≤5 条；短路时已省略
- [ ] 诊断依据注明每目标的遍历位置

---

## 示例

### 示例 1：战略半成品（正常路径）

**场景**：项目有 mission / vision；无 strategic-goals；roadmap 存在但无法追溯到战略目标。

**输出**（示例）：

#### 下一步建议

##### 现在该做

**1. 补充战略目标文档** · `重要`

战略目标缺失，路线图节点无法追溯到目标，后续层级遍历无法继续。

- 推荐技能：`/design-strategic-goals 基于 mission.md 和 vision.md 生成 strategic-goals.md，包含可识别的目标项`
- 依据：`docs/project-overview/strategic-goals.md` 缺失
- 完成标志：strategic-goals.md 写入并含可识别目标项；受阻时回 plan-next 重评

---

##### 其他可留意

- **路线图节点对齐**：节点无法追溯到战略目标 → 待战略目标补齐后 `/align-backlog`

##### 诊断依据

<details>
<summary>展开</summary>

- **项目情况**：有使命愿景但无战略目标，路线图对齐待建立
- **判定逻辑**：L1 战略目标层缺失（G1），遍历在 L1 停止；路线图对齐问题降级到"其他可留意"（L2 依赖 L1 就绪）

</details>

### 示例 2：新项目起步（短路场景）

**场景**：新项目，`docs/ARTIFACT_NORMS.md` 不存在，`specs/` 为空。

**输出**（示例）：

#### 下一步建议

##### 现在该做

**1. 建立文档规范基础** · `紧急`

规范文件缺失，后续所有文档创建无统一标准，治理无法推进。

- 推荐技能：`/discover-docs-norms` → `/define-docs-norms 基于项目结构生成 docs/ARTIFACT_NORMS.md`
- 依据：`docs/ARTIFACT_NORMS.md` 缺失
- 完成标志：ARTIFACT_NORMS.md 落盘后重跑 plan-next

---

##### 其他可留意

（短路场景省略——治理规则未建立时下游创建无统一标准。补齐规范后重跑 plan-next 获完整路由。）

##### 诊断依据

<details>
<summary>展开</summary>

- **项目情况**：规范层缺位，触发短路输出
- **判定逻辑**：Rules 层缺位命中 2.0 前置闸门，跳过目标树遍历

</details>

### 示例 3：兄弟节点推进 + 并行决策

**场景**：目标 A，路线图节点 N1（in-progress）。N1 下有需求 R1（in-progress，子推算）和需求 R2（pending）。R1 下有设计 D1a（done）和 D1b（in-progress）。D1b 下任务尚未拆解。

**遍历路径**：N1 → R1（in-progress，子推算）→ 兄弟扫描：D1a done，D1b in-progress → 进入 D1b → 无任务（L5 缺口）→ 路由 `breakdown-tasks`。

**并行判定**：D1b 为唯一 in-progress 设计，R2 pending。建议：**专注** D1b，完成后 R2 自动成为下一焦点。

**输出**（示例）：

#### 下一步建议

##### 现在该做

**1. 为设计 D1b 拆解可执行任务** · `缓`

D1b 设计就绪但尚无任务，无法进入执行；D1a 已完成触发推进到 D1b。

- 推荐技能：`/breakdown-tasks 基于设计 D1b 拆解任务清单，参考 D1a 拆解粒度`
- 依据：D1b 设计文件存在，任务文件缺失；D1a done 触发兄弟推进
- 完成标志：D1b 任务列表创建且有至少一条任务记录

---

##### 其他可留意

- **需求 R2**：D1b 完成后的下一焦点 → 专注 D1b，D1b 完成后自动推进到 R2

##### 诊断依据

<details>
<summary>展开</summary>

- **项目情况**：目标 A 处于执行阶段，N1→R1→D1b，任务层缺口
- **判定逻辑**：D1a done 触发兄弟推进到 D1b；D1b in-progress 且无任务（G1）；并行建议"专注"（仅 1 个 in-progress，其余 pending）

</details>

### 示例 4：路线图未分层

**场景**：战略目标存在，路线图存在但节点无 Now/Next/Later 分层，仅为扁平列表。

**输出**（示例）：

#### 下一步建议

##### 现在该做

**1. 为路线图建立当期/下期/远期分层** · `重要`

路线图是扁平列表，无法确定当前执行焦点，下游层级无法评估。

- 推荐技能：`/promote-roadmap-items 将 roadmap.md 中的节点按 Now/Next/Later 优先级分层`
- 依据：`docs/requirements-planning/roadmap.md` 存在但无分层结构
- 完成标志：路线图含 Now/Next/Later 分层后重跑 plan-next

---

##### 其他可留意

（无法评估下游，待路线图分层后重跑。）

##### 诊断依据

<details>
<summary>展开</summary>

- **项目情况**：路线图存在但未分层，遍历在 L2 停止
- **判定逻辑**：路线图未分层命中"路线图未分层"规则，路由 `promote-roadmap-items`，不继续评估下游

</details>

### 示例 5：blocked 触发并行

**场景**：目标 A，路线图节点 N1。N1 下需求 R1（blocked，等待外部依赖）和 R2（pending，与 R1 无 depends_on 依赖）。

**并行判定**：R1 blocked，R2 pending 且独立 → **并行**：建议同时启动 R2。

**输出**（示例）：

#### 下一步建议

##### 现在该做

**1. 启动需求 R2 的方案设计** · `缓`

R1 被外部依赖阻塞，R2 与 R1 无依赖关系，并行启动 R2 可避免等待浪费。

- 推荐技能：`/design-solution 为需求 R2 创建设计文档，R1 blocked 期间并行推进`
- 依据：R1 blocked（等待外部依赖）；R2 无 `depends_on` 依赖
- 完成标志：R2 设计文件创建；受阻时（R2 与 R1 存在隐含耦合）回 plan-next 重评

---

##### 其他可留意

- **需求 R1**：blocked，等待外部依赖 → 人工介入解除；解除后重跑 plan-next

##### 诊断依据

<details>
<summary>展开</summary>

- **项目情况**：目标 A，N1 下 R1 blocked，R2 pending
- **判定逻辑**：并行决策规则"1+ blocked + 有独立 pending"→ 建议并行；R2 无 depends_on 依赖，可安全启动

</details>
