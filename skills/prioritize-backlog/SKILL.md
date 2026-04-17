---
name: prioritize-backlog
description: Force a clean re-score of every backlog item with four frameworks (RICE, WSJF, MoSCoW, ICE) in parallel — ignores any existing priority, auto-detects multi-file or single-file backlog layouts, surfaces framework disagreements, and captures the user's final decision with rationale.
description_zh: 对全部 backlog 条目强制重评（忽略原 priority），并行跑 RICE / WSJF / MoSCoW / ICE 四框架；自动适配多文件目录或单文件 backlog 形态，呈现分歧并捕获用户决策依据。
tags: [workflow, automation, meta-skill]
version: 2.0.0
license: MIT
recommended_scope: project
cognitive_mode: interpretive
metadata:
  author: ai-cortex
triggers: [prioritize backlog, score backlog, backlog ranking, planning prep, re-score backlog]
input_schema:
  type: free-form
  description: Backlog items in any priority state, located either as one-file-per-item under a backlog directory or as a single backlog.md (yaml-list / H2+yaml / table); plus strategic-goals.md and optional project-specific thresholds
output_schema:
  type: chat
  description: Per-item scoring table across 4 frameworks + disagreement call-outs + detected backlog mode + user's priority_decision (with previous-value field) written back to each item in its native format
---

# 技能：优先级评分（Prioritize Backlog）

## 目的 (Purpose)

用多个价值框架并行评估一批 backlog 条目，呈现框架间的分歧，由用户做出优先级决策并记录依据。

---

## 核心目标（Core Objective）

**首要目标**：对一批 backlog 条目（无视当前 priority 状态）执行**强制全量重评**，给出用户确认后的新 `priority` 与 `priority_decision`，并写回各自所在的 backlog 形态（多文件目录或单文件）。

**成功标准**（必须全部满足）：

1. ✅ 每个条目有 4 个框架（RICE / WSJF / MoSCoW / ICE）的评分
2. ✅ 框架间分歧已显式 surface（≥ 2 级差触发人工决策）
3. ✅ 每条目最终 `priority` 由用户确认，不是算法输出
4. ✅ 每条目写回 `priority_decision` 字段（含 `previous` 旧值快照，便于回看本次覆盖了什么）
5. ✅ 输出批量结果表，用户可跨条目比较
6. ✅ 报告头声明检测到的 backlog 形态（`multi-file` / `yaml-list` / `h2-yaml` / `table`），并按该形态执行写回

**验收测试**：读者能否从 backlog 条目的 frontmatter / yaml 块 / 表格行直接看到新 priority + 决策依据 + 被覆盖的旧值，不用反查对话？

---

## 范围边界（Scope Boundaries）

**本技能负责**：

- 自动识别 backlog 形态（多文件目录 / 单文件 yaml-list / h2-yaml / table）并读取**全部**条目
- 对每条强制重新跑 RICE / WSJF / MoSCoW / ICE 评分（忽略原 priority 与 priority_decision）
- Surface 框架间分歧
- 捕获用户决策并按检测到的形态写回（多文件改 frontmatter；单文件改对应 yaml 块 / 表格单元格）

**本技能不负责**：

- 创建新的 backlog 条目（用 `capture-work-items`）
- 将条目晋升进 roadmap（用 `promote-roadmap-items`）
- 为单一条目评分（该技能是**批量**工作流，单条评分会丢失对比性）
- 归档旧评估历史（仅保留 `previous` 单字段；如需 history 由调用方负责）

**交接点**：评分完成后交给 `promote-roadmap-items` 做 backlog → roadmap 晋升。

---

## 使用场景（Use Cases）

- `capture-work-items` 批量捕获后建议触发
- Planning ceremony 前对积压做一次干净的全量重评
- 战略刷新后任何节点直接重跑（无需额外开关 —— 默认就是覆盖式重评）
- `plan-next` 输出的大缺口被 capture 后进入评分
- 单文件 backlog（如轻量项目维护一份 `backlog.md`）也能直接处理

---

## 行为（Behavior）

### 阶段 0：读取输入与形态探测

1. **形态探测（按优先级尝试，命中即停）**

   | 优先级 | 形态 | 探测条件 |
   |---|---|---|
   | 1 | `multi-file` | `docs/process-management/backlog/` 或 `docs/backlog/` 存在，且至少一个 `*.md` 文件含 `artifact_type: backlog-item` 或 `priority:` frontmatter 字段 |
   | 2 | `yaml-list` | 单文件 `docs/process-management/backlog.md` 或 `docs/backlog.md` 存在，frontmatter 或顶层 YAML 含 `items:` 数组 |
   | 3 | `h2-yaml` | 同上单文件，正文中存在 `## <title>` 标题紧随 ```yaml … ``` 代码块 |
   | 4 | `table` | 同上单文件，正文存在含 `Title` 与 `Priority`（或等价列）的 Markdown 表格 |

   优先吃项目自定义路径（若存在 `.ai-cortex/artifact-norms.yaml` 或 `docs/ARTIFACT_NORMS.md` 中的 `backlog-item.path_pattern`）。

   **全未命中** → halt 报告"未发现可识别的 backlog 形态"，提示先运行 `capture-work-items`。

   **检测到混合形态**（既有目录又有单文件）→ 默认采用 multi-file 并在报告里告知用户单文件被忽略；不双写，避免不一致。

2. 读取 `docs/project-overview/strategic-goals.md`（用于 WSJF 的 Cost of Delay 判断和 MoSCoW 的 Must 判断）。

3. **枚举全部条目**（不再筛选 `priority: unset`）：把已有 `priority` / `priority_decision` 仅作 audit log 显示，**不参与新评分**，避免锚点偏差。

4. 若条目总数 = 1 → **halt 并警告**："单条评分会丢失对比性。建议至少 2 条一起评。是否继续？"

### 阶段 1：多框架并行评分

对每个条目同时计算：

#### RICE

```
RICE = (Reach × Impact × Confidence) / Effort
```

- **Reach**：受影响人数或实例数（定量）
- **Impact**：1（低）/ 2（中）/ 3（高）
- **Confidence**：0-100%（对 Reach × Impact 估算的信心）
- **Effort**：人周

映射为优先级等级：
| RICE 分数 | 级别 |
|---|---|
| ≥ 1000 | P0 |
| 200-1000 | P1 |
| 50-200 | P2 |
| < 50 | P3 |

（阈值是默认示例，项目可自定）

#### WSJF

```
WSJF = Cost of Delay / Job Size
```

- **Cost of Delay** = Business Value + Time Criticality + Risk Reduction / Opportunity Enablement
- **Job Size** = 相对工作量（斐波那契数列：1, 2, 3, 5, 8, 13, 20）

映射为优先级等级（按当前 backlog 的 WSJF 分位数）：
| WSJF 分位 | 级别 |
|---|---|
| Top 10% | P0 |
| 10-30% | P1 |
| 30-70% | P2 |
| Bottom 30% | P3 |

#### MoSCoW

按承诺层级分类：

- **Must**：本周期不做会严重阻塞或违反合规 → P0
- **Should**：本周期做会显著提升价值 → P1
- **Could**：有时间做就做 → P2
- **Won't**：明确本周期不做 → P3

#### ICE

```
ICE = Impact × Confidence × Ease
```

- 每维度 1-10 定性打分
- Impact：对战略目标的影响
- Confidence：估算的信心
- Ease：实施的容易程度（越高越容易）

映射：
| ICE 分数 | 级别 |
|---|---|
| ≥ 500 | P0 |
| 200-500 | P1 |
| 50-200 | P2 |
| < 50 | P3 |

### 阶段 2：Surface 分歧

对每个条目计算**框架间最大分歧**：

| 分歧级差 | 处理 |
|---|---|
| ≤ 1 级（如 P1 vs P2） | 默认采用 **RICE** 结果，无需人工决策 |
| ≥ 2 级（如 P0 vs P3） | 显式 surface，必须人工决策 |

分歧阈值项目可自定（默认 2 级）。

### 阶段 3：呈现批量结果

输出格式：

```
## Batch Scoring Summary

| # | Title | RICE | WSJF | MoSCoW | ICE | 分歧 | 建议 |
|---|---|---|---|---|---|---|---|
| 1 | ... | P1 | P1 | Should | P2 | 1 级 | 自动采 P1 |
| 2 | ... | P3 | P1 | Could | P3 | 2 级 | **需人工** |
| ... |

## 需人工决策的条目（分歧 ≥ 2 级）

### Item #2: <title>

- RICE=P3 理由：Reach 仅 10 人、Effort 8 周
- WSJF=P1 理由：Q3 里程碑依赖本项，Cost of Delay 高
- MoSCoW=Could
- ICE=P3

**分歧焦点**：时间敏感性（WSJF）vs 规模（RICE）

**请决策**：P? 理由？
```

### 阶段 4：捕获决策并写回（按形态分发）

对每个条目：

1. 确定最终 `priority`（自动采信或用户输入）。
2. 构造 `priority_decision` 字段内容，**必含** `previous`：

   ```yaml
   priority_decision:
     final: P<N>
     previous: P<N> | unset
     frameworks:
       rice: P<N>
       wsjf: P<N>
       moscow: Must | Should | Could | Won't
       ice: P<N>
     rationale: <one-sentence reason if disagreement was ≥ 2 levels>
     decided_by: auto | user
     decided_at: <ISO date>
   ```

3. **按形态写回**：

   | 形态 | 写回方式 |
   |---|---|
   | `multi-file` | 更新各 `*.md` 文件 frontmatter 的 `priority` + `priority_decision` |
   | `yaml-list` | 修改单文件中 `items[i].priority` + `items[i].priority_decision`，保持 YAML 缩进与键序 |
   | `h2-yaml` | 替换该条目对应 ```yaml``` 代码块内的 `priority` + `priority_decision`，保持代码块位置 |
   | `table` | 更新表格 `Priority` 单元格；`priority_decision` 写到表格下方 `## Priority Decisions` 小节，按条目锚点列出 |

   写回前确认：旧值已记录到 `priority_decision.previous`，避免被静默吞掉。

### 阶段 5：输出最终报告

报告头必须包含：

- `Backlog mode: multi-file | yaml-list | h2-yaml | table`
- `Re-scored items: N (含 X 条覆盖了原 priority；Y 条原为 unset)`

报告体：

- 处理总数、自动决策数、人工决策数
- 各优先级分布统计
- 建议下一步（如 `promote-roadmap-items` 批量晋升）

---

## 输入与输出 (Input & Output)

**输入**：见 frontmatter `input_schema` —— backlog 目录、strategic-goals.md、可选阈值覆盖。

**输出**：对话批量评分表 + 每个 backlog 文件 frontmatter 被更新（`priority` 和 `priority_decision` 字段）。

---

## 限制（Restrictions）

### 硬边界（Hard Boundaries）

- **强制全量重评**：默认覆盖所有条目的 `priority` 与 `priority_decision`，旧值仅以 `previous` 单字段保留，不做历史归档（保持技能单一职责，归档由调用方负责）
- **不混合形态**：探测到 multi-file 即不再扫单文件，反之亦然，避免双写不一致
- 不自动聚合多框架成单一分数（保留分歧信号是核心价值）
- 分歧 ≥ 阈值时必须人工决策，不得默认兜底
- 不创建新的 backlog 条目（那是 `capture-work-items` 的职责）

### 技能边界 (Skill Boundaries)

**不做（其他技能负责）**：

| 动作 | 归属 |
|---|---|
| 创建新 backlog 条目 | `capture-work-items` |
| 把 backlog 条目晋升进 roadmap | `promote-roadmap-items` |
| 拆分任务 | `breakdown-tasks` |
| 需求详细分析 | `analyze-requirements` |

---

## Anti-Patterns

- ❌ **不要加权平均四框架分数** —— 聚合等于丢分歧信号，破坏本技能核心价值
- ❌ **不要为单条目独立评分** —— 没有对比组，RICE / WSJF 的相对性失效
- ❌ **不要隐藏分歧** —— 即使默认自动采信 RICE，也要在报告表里显示各框架分数
- ❌ **不要忽略 strategic_goal_id** —— 战略目标决定 MoSCoW 的 Must 判断
- ❌ **不要用模糊措辞**（"大概"、"可能"）写 `priority_decision.rationale` —— 必须具体引用框架或数据
- ❌ **不要在重评时"比对旧 priority 是否合理后再决定是否覆盖"** —— 这等于给框架打分加锚点偏差，违反本技能"强制干净重评"的设计意图
- ❌ **不要丢弃旧值** —— `priority_decision.previous` 必须写入；让用户能在一处看到本次改动了什么
- ❌ **不要尝试在两种形态间双写** —— 多文件与单文件择一，避免数据漂移

---

## 自检（Self-Check）

- [ ] 已声明 backlog 形态（`multi-file` / `yaml-list` / `h2-yaml` / `table`）并按形态写回
- [ ] 形态探测失败时已 halt，并指引 `capture-work-items`
- [ ] 扫描全部条目，旧 priority 仅作展示不参与评分（无锚点偏差）
- [ ] 每条目跑了全部 4 个框架
- [ ] 分歧 ≥ 阈值的条目 surface 了，并要求人工决策
- [ ] 分歧 ≤ 阈值的条目自动采信 RICE，但各框架分数仍可见
- [ ] 每条目 `priority_decision` 写回，含 frameworks 结果、rationale（若分歧）、`previous` 旧值快照
- [ ] 批量汇总报告含 `Backlog mode`、覆盖统计、优先级分布、下一步建议
- [ ] 未自动调用 `promote-roadmap-items`

---

## 示例（Examples）

### 示例 1：多文件 backlog 全量重评（主流场景）

**输入**：`docs/process-management/backlog/` 下 5 个条目，混合状态 —— 3 个 `priority: unset`、1 个 `priority: P2`（旧）、1 个 `priority: P3`（旧）。

**形态探测**：命中 `multi-file`。

**输出摘要**：

```
Backlog mode: multi-file
Re-scored items: 5 (含 2 条覆盖了原 priority；3 条原为 unset)

## Batch Scoring Summary

| # | Title | 旧 | RICE | WSJF | MoSCoW | ICE | 分歧 | 建议 |
|---|---|---|---|---|---|---|---|---|
| 1 | 支付 API 响应时间优化 | unset | P1 | P1 | Should | P1 | 0 级 | **自动 P1** |
| 2 | ARTIFACT_NORMS 格式升级 | P3 | P3 | P3 | Could | P3 | 0 级 | **自动 P3（与旧值一致）** |
| 3 | Q3 支持多币种 | unset | P2 | P0 | Must | P2 | 2 级 | **需人工** |
| 4 | 登录错误 500 修复 | P2 | P1 | P2 | Should | P1 | 1 级 | **自动 P1（覆盖旧 P2）** |
| 5 | 新增技术债：重构 auth 模块 | unset | P3 | P2 | Could | P2 | 1 级 | 自动 P3 |

## 需人工决策：Item #3
（同前略）
```

**写回结果片段**（Item #4，被覆盖的条目）：

```yaml
priority: P1
priority_decision:
  final: P1
  previous: P2
  frameworks:
    rice: P1
    wsjf: P2
    moscow: Should
    ice: P1
  decided_by: auto
  decided_at: 2026-04-17
```

### 示例 2：单文件 backlog（h2-yaml 形态）

**输入**：`docs/backlog.md` 维护一份"轻量 backlog"，每条目是 H2 标题 + 行内 yaml 块：

```markdown
## 支付 API 响应时间优化
```yaml
strategic_goal_id: goal-1
priority: P2
```
原因：…

## 登录错误 500 修复
```yaml
strategic_goal_id: goal-1
priority: unset
```
…
```

**形态探测**：multi-file 路径不存在 → yaml-list 不命中 → **命中 `h2-yaml`**。

**写回方式**：替换每条对应的 yaml 代码块内的 `priority` + `priority_decision`，保留代码块外的描述正文不变；`priority_decision.previous` 写入旧值（一条原为 P2，一条为 unset）。

报告头：`Backlog mode: h2-yaml`、`Re-scored items: 2 (含 1 条覆盖了原 priority；1 条原为 unset)`。

---

## 附录：输出契约

每个 backlog 条目（无论形态）被更新为：

```yaml
priority: P0 | P1 | P2 | P3
priority_decision:
  final: P<N>
  previous: P<N> | unset       # 本次重评前的旧 priority；强制写入，便于覆盖审计
  frameworks:
    rice: P<N>
    wsjf: P<N>
    moscow: Must | Should | Could | Won't
    ice: P<N>
  rationale: <optional, required if framework disagreement ≥ 2 levels>
  decided_by: auto | user
  decided_at: <ISO date>
```

写入位置依形态而异：

| 形态 | 写入位置 |
|---|---|
| `multi-file` | 各 `*.md` 的 frontmatter |
| `yaml-list` | 单文件中 `items[i]` 节点 |
| `h2-yaml` | 单文件中该条目对应的 ```yaml``` 代码块 |
| `table` | 表格 `Priority` 单元格 + 表格下方 `## Priority Decisions` 小节按条目锚点列出 |
