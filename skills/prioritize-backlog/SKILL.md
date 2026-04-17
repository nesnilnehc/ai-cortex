---
name: prioritize-backlog
description: Score unprioritized backlog items with multiple frameworks (RICE, WSJF, MoSCoW, ICE) in parallel, surface framework disagreements, and capture the user's priority decision with rationale.
description_zh: 用多框架（RICE / WSJF / MoSCoW / ICE）并行评分未定优先级的 backlog 条目，呈现框架分歧，并捕获用户决策依据。
tags: [workflow, automation, meta-skill]
version: 1.0.0
license: MIT
recommended_scope: project
cognitive_mode: interpretive
metadata:
  author: ai-cortex
triggers: [prioritize backlog, score backlog, backlog ranking, planning prep]
input_schema:
  type: free-form
  description: Batch of backlog items with priority=unset; strategic-goals.md; optional project-specific thresholds
output_schema:
  type: chat
  description: Per-item scoring table across 4 frameworks + disagreement call-outs + user's priority_decision written back to each backlog file
---

# 技能：优先级评分（Prioritize Backlog）

## 目的 (Purpose)

用多个价值框架并行评估一批 backlog 条目，呈现框架间的分歧，由用户做出优先级决策并记录依据。

---

## 核心目标（Core Objective）

**首要目标**：将一批 `priority: unset` 的 backlog 条目评估出用户确认的 `priority` 值和 `priority_decision` 依据，写回每个 backlog 文件。

**成功标准**（必须全部满足）：

1. ✅ 每个条目有 4 个框架（RICE / WSJF / MoSCoW / ICE）的评分
2. ✅ 框架间分歧已显式 surface（≥ 2 级差触发人工决策）
3. ✅ 每条目最终 `priority` 由用户确认，不是算法输出
4. ✅ 每条目写回 `priority_decision` 字段（记录依据引用哪个框架或人工理由）
5. ✅ 输出批量结果表，用户可跨条目比较

**验收测试**：读者能否从 backlog 条目的 frontmatter 直接看到优先级 + 决策依据，不用反查对话？

---

## 范围边界（Scope Boundaries）

**本技能负责**：

- 读取一批 `priority: unset` 的 backlog 条目
- 对每条跑 RICE / WSJF / MoSCoW / ICE 评分
- Surface 框架间分歧
- 捕获用户决策并写回 backlog frontmatter

**本技能不负责**：

- 创建新的 backlog 条目（用 `capture-work-items`）
- 修改已有 `priority` 的条目（需显式请求重评）
- 将条目晋升进 roadmap（用 `promote-roadmap-items`）
- 为单一条目评分（该技能是**批量**工作流，单条评分会丢失对比性）

**交接点**：评分完成后交给 `promote-roadmap-items` 做 backlog → roadmap 晋升。

---

## 使用场景（Use Cases）

- `capture-work-items` 批量捕获后建议触发
- Planning ceremony 前批量处理未评分积压
- 战略刷新后，重新评估 backlog（此时显式传入 `re-score=true`）
- `plan-next` 输出的大缺口被 capture 后进入评分

---

## 行为（Behavior）

### 阶段 0：读取输入

1. 扫描 backlog 目录（`docs/process-management/backlog/` 或 `docs/backlog/`），筛选 `priority: unset` 的条目
2. 读取 `docs/project-overview/strategic-goals.md`（用于 WSJF 的 Cost of Delay 判断和 MoSCoW 的 Must 判断）
3. 若没有 unset 条目 → 结束，报告"无待评分条目"
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

### 阶段 4：捕获决策并写回

对每个条目：

1. 确定最终 `priority`（自动采信或用户输入）
2. 确定 `priority_decision` 字段内容，格式：
   ```
   priority_decision:
     final: P<N>
     frameworks:
       rice: P<N>
       wsjf: P<N>
       moscow: <level>
       ice: P<N>
     rationale: <one-sentence reason if disagreement was ≥ 2 levels>
     decided_by: <auto|user>
     decided_at: <ISO date>
   ```
3. 更新 backlog 文件的 frontmatter（`priority` + `priority_decision`）

### 阶段 5：输出最终报告

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

- 不对 `priority` 已有值的条目重评（除非显式 `re-score=true`）
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

---

## 自检（Self-Check）

- [ ] 只扫描 `priority: unset` 的条目
- [ ] 每条目跑了全部 4 个框架
- [ ] 分歧 ≥ 阈值的条目 surface 了，并要求人工决策
- [ ] 分歧 ≤ 阈值的条目自动采信 RICE，但各框架分数仍可见
- [ ] 每条目 `priority_decision` 写回，含 frameworks 结果和 rationale（若分歧）
- [ ] 批量汇总报告含总数、分布、下一步建议
- [ ] 未自动调用 `promote-roadmap-items`

---

## 示例（Examples）

### 示例 1：批量评分（主流场景）

**输入**：backlog 目录下有 5 个 `priority: unset` 条目。

**输出摘要**：

```
## Batch Scoring Summary

| # | Title | RICE | WSJF | MoSCoW | ICE | 分歧 | 建议 |
|---|---|---|---|---|---|---|---|
| 1 | 支付 API 响应时间优化 | P1 | P1 | Should | P1 | 0 级 | **自动 P1** |
| 2 | ARTIFACT_NORMS 格式升级 | P3 | P3 | Could | P3 | 0 级 | **自动 P3** |
| 3 | Q3 支持多币种 | P2 | P0 | Must | P2 | 2 级 | **需人工** |
| 4 | 登录错误 500 修复 | P1 | P2 | Should | P1 | 1 级 | 自动 P1 |
| 5 | 新增技术债：重构 auth 模块 | P3 | P2 | Could | P2 | 1 级 | 自动 P3 |

## 需人工决策：Item #3

- RICE=P2 理由：Reach=500 商户 × Impact=中 × Confidence=70% / Effort=5 周
- WSJF=P0 理由：法律要求 Q3 前必须支持，Cost of Delay 极高
- MoSCoW=Must 理由：合规硬截止
- ICE=P2

**分歧焦点**：合规时间敏感性（WSJF+MoSCoW）vs 规模/工作量（RICE+ICE）

**决策请求**：P? 理由？
```

用户回："P0，合规时间敏感必须前置"

**写回结果**：Item #3 frontmatter 更新为 `priority: P0` + `priority_decision.rationale: "Q3 合规硬截止；时间敏感性（WSJF/MoSCoW）压过规模判断"`。

### 示例 2：单条目请求（边缘场景）

**用户**：尝试单独为一个刚捕获的 bug 跑 prioritize-backlog。

**技能响应**：

> "检测到仅 1 条 `priority: unset` 条目。单条评分会丢失对比性（RICE / WSJF 依赖相对比较）。建议：
> 1. 先用 `capture-work-items` 捕获更多条目，再批量评分
> 2. 或明确请求 `single-item=true` 继续（评分质量会降低）"

若用户坚持 `single-item=true`：跳过 WSJF 相对分位计算，用绝对阈值，并在输出中标记"单条评分，质量可能偏差"。

---

## 附录：输出契约

每个 backlog 条目的 frontmatter 被更新为：

```yaml
priority: P0 | P1 | P2 | P3
priority_decision:
  final: P<N>
  frameworks:
    rice: P<N>
    wsjf: P<N>
    moscow: Must | Should | Could | Won't
    ice: P<N>
  rationale: <optional, required if framework disagreement ≥ 2 levels>
  decided_by: auto | user
  decided_at: <ISO date>
```
