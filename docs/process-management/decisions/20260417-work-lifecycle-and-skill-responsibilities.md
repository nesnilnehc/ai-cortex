---
artifact_type: adr
created_by: decision-record
lifecycle: snapshot
created_at: 2026-04-17
status: active
---

# 工作生命周期与技能职责（事件驱动版）

**状态**: 已接受 (Accepted)
**日期**: 2026-04-17
**范围**: 定义使用 AI Cortex 治理的项目中，工作如何从 backlog 渐进细化到执行；定义 plan-next v5 定位；识别缺失技能并给出 positioning。
**依赖**: ADR-20260417-unified-value-driven-prioritization-model（本 ADR 以其单 roadmap + 多框架 + 容量护栏 + 工程健康目标为前提）

---

## 1. 背景

- AI 辅助开发（Claude Code、Cursor 等）大幅压缩 requirement → design → code → ship 的时间尺度，**Sprint 已成为过慢的计划单元**
- 业界后 Sprint 运动明确（Shape Up、Kanban-native、Continuous Planning、Trunk-based + CD）
- 治理工作（包括 plan-next）之前的"cycle 开始 / 结束"假设隐含 Sprint 节律，已不匹配现代实践
- plan-next v4 虽有完整 5×4 矩阵，但对"项目当前状态"无感知，始终输出全量，造成认知负担

---

## 2. 问题

1. **生命周期时机不清**：backlog → roadmap → requirement → task → 执行 的过渡点没规则
2. **技能职责边界模糊**：哪些技能负责前向（预防性诊断）、哪些负责后向（追溯对齐），未明示
3. **Sprint 假设过时**：各技能潜规则绑定 Sprint cadence，AI 时代 session 内可跑完多层
4. **plan-next 无状态感知**：对项目刚起步 / 执行中 / 健康期输出无差异，用户体感笨重
5. **缺关键技能**：Roadmap planning ceremony（backlog → roadmap 晋升）与多框架评分流程无技能支撑

---

## 3. 决策

### 3.1 Progressive Elaboration 原则 + JIT 时间尺度

**原则**：工作分析细化**延迟到真正需要时**（Just-in-time，不 Just-in-case）。

**AI 时代的时间尺度**（与传统 Agile 对比）：

| 层 | 传统 JIT | AI 时代 JIT |
|---|---|---|
| Strategic goals | 年度 | 季度 |
| Roadmap | 季度 | 月度 |
| Requirement 分析 | Sprint 开始（2 周窗口） | 同一 session 内，coding 前几分钟 |
| Task 拆分 | Sprint planning | 执行前 5 分钟 |
| 执行 | Sprint | 小时-当天 |

各层不同压缩度：**战略层仍慢（需要反思），执行层大幅压缩（AI 辅助）**。

### 3.2 事件驱动 cadence（非 Sprint）

所有技能的触发机制从"日历驱动"改为"事件驱动"：

| 技能 | 触发事件 |
|---|---|
| `plan-next` | 开始新工作前 / 感到摩擦 / 战略层变动 / 最长 N 天必跑一次（防腐） |
| `align-planning` | 执行完成 / merge / release 后 |
| `prioritize-backlog` | backlog 积压未评分项 ≥ 阈值，或 planning 前主动跑 |
| `plan-roadmap-pull` | 容量释出（完成一批工作）/ 战略层变动 / cycle 结束 |

**不再有"每周一跑 plan-next"这类日历绑定**。

### 3.3 前向 vs 后向技能职责边界

| 方向 | 技能 | 回答的问题 |
|---|---|---|
| **前向** | `plan-next` | 现在有哪些治理缺口？下一步该做什么治理动作？ |
| **后向** | `align-planning` / `align-backlog` / `align-architecture` | 已经做了什么？跟 plan 对得上吗？漂移在哪？ |

两者**互补不竞争**：
- cycle 开始（或工作启动前）→ `plan-next` 前向体检
- cycle 结束（或工作完成后）→ `align-*` 后向追溯

用户的"反向推导"（有任务先做、后补 backlog → requirement → task）是 pull-based 合法模式，由 `align-planning` 承担，**不属于 plan-next 职责**。

### 3.4 plan-next v5 Positioning

**plan-next 定位**（五问回答）：

| 问题 | 答案 |
|---|---|
| 独特回答什么？ | 治理资产有哪些缺口？下一步该做什么治理动作？ |
| 消费什么？ | 治理资产（mission/vision/NSM/strategic-goals/roadmap/backlog/ADR/code 等） |
| 产出什么？ | 结构化对话：输入源清单 + 准备门结论 + 推荐路由任务 |
| 何时触发？ | 事件驱动（见 3.2） |
| 与已有机制关系？ | **读但不写**项目计划；小缺口直接路由修复，大缺口 capture 成 backlog 项进入同一条价值赛道 |

### 3.5 plan-next v5 引入状态机（矩阵的解释器）

**状态机 positioning**：

| 问题 | 答案 |
|---|---|
| 独特回答什么？ | 项目当前在生命周期哪一阶段？（矩阵本身不回答） |
| 消费什么？ | 矩阵 Phase 0 的资产状态扫描结果 |
| 产出什么？ | 状态标签（S1-S7）+ 层级显示权重建议 |
| 何时触发？ | plan-next 每次调用派生（不独立触发） |
| 与矩阵关系？ | **上下游（解释器）** —— 矩阵产诊断，状态机解释诊断。不是替代、不是并列叠加 |

**7 态定义**：

| 状态 | 判定信号 | 激活层（Primary 聚焦） |
|---|---|---|
| **S1 Greenfield** | 所有 Why 层资产缺失或仅占位 | Why × G1 |
| **S2 Strategy drafted** | Why 层 ≥2 项 present；roadmap 缺 | What × G1 |
| **S3 Plan drafted, 稀薄 backlog** | roadmap present；backlog 条目 < 阈值（默认 5） | What × G2 |
| **S4 Backlog rich, idle** | roadmap+backlog 齐全；无 in-progress；近 N 天无 commit | Pull ceremony（prioritize → pull） |
| **S5 Execution in-flight** | 有 in-progress task / 未合并 PR / 近 N 天有 commit | 静默，仅 Rules×G1 打断 |
| **S6 Post-execution, 可能漂移** | 近期 merge/release；上次 align-planning > N 天 | Is × G3（触发 align-planning） |
| **S7 Healthy / Idle** | 矩阵无缺口 + 无 in-flight + 漂移近期查过 | Quiet mode（明示无治理行动需要） |

**状态检测信号**：文件存在性、frontmatter 字段、文件 mtime、git log、git status、`docs/calibration/planning-alignment.md` 的 created_at。

**低 confidence fallback**：状态检测不确定时（多个状态都有部分匹配）降级到全矩阵输出，不强行归类。

### 3.6 plan-next v5 两层输出模型

**两层输出 positioning**：

| 问题 | 答案 |
|---|---|
| 独特回答什么？ | 相同诊断数据，如何同时提供聚焦和全景？ |
| 消费什么？ | 矩阵 Phase 1 诊断结果 + 状态机的激活层建议 |
| 产出什么？ | Primary 层（激活层详细路由） + Secondary 层（其他层压缩摘要） |
| 何时触发？ | plan-next 输出合成时 |
| 与矩阵 / 状态机关系？ | **表现层** —— 在数据（矩阵）和解释（状态机）之上，决定显示权重 |

**输出结构**：

```
项目状态：S<N>（<判定摘要>）
判定依据：<关键信号>

=== Primary：激活层路由 ===
<详细路由表：主题 | 缺口 | 技能 | 依据 | 优先级 | 停止条件>

=== Secondary：全矩阵其他发现 ===
<压缩表：格子 | 一句话概述 | 建议（立即 / 推迟 / 不阻塞）>
```

**关键原则**：
- 矩阵的 MECE 覆盖完整保留（Secondary 中呈现）
- 状态机误判时 Secondary 兜底（用户能看到被"去优先化"的格子）
- 用户 flag `--force-full-matrix` 可强制全量输出

### 3.7 新增两个技能的 positioning

#### 3.7.1 `prioritize-backlog`

| 问题 | 答案 |
|---|---|
| 独特回答什么？ | 这批 backlog 条目的优先级分别应该是多少？ |
| 消费什么？ | 一批 `priority: unset` 的 backlog 条目 + strategic-goals |
| 产出什么？ | 每条目四框架评分 + 分歧呈现 + 用户决策的 `priority_decision` |
| 何时触发？ | backlog 未评分项 ≥ 阈值 / planning 前主动调用 / capture-work-items 批量捕获结束后的建议 |
| 与现有技能关系？ | **上游 capture-work-items**（拿到未评分项）；**下游 plan-roadmap-pull**（评分后可进入晋升决策） |

**核心流程**：
1. 读取所有 `priority: unset` 的 backlog 条目
2. 对每条跑 RICE + WSJF + MoSCoW + ICE
3. Surface 框架间分歧（≥ 2 级差的突出）
4. 呈现给用户、捕获决策依据
5. 写回 `priority` 和 `priority_decision` 字段

**不自动链式**：`capture-work-items` 不自动调用 `prioritize-backlog`（节律不同：capture 高频，prioritize 批量）。只建议，不执行。

#### 3.7.2 `plan-roadmap-pull`

| 问题 | 答案 |
|---|---|
| 独特回答什么？ | 已优先级评分的 backlog 条目中哪些应该晋升进入当前 roadmap 的 Now？ |
| 消费什么？ | priority 已定的 backlog + 当前 roadmap 状态 + strategic_goal 容量分配 |
| 产出什么？ | Now / Next / Later 更新建议 + 容量使用报告 + 晋升 / 降级决策 |
| 何时触发？ | Roadmap planning ceremony（容量释出 / 战略变动 / 按需） |
| 与现有技能关系？ | **上游 prioritize-backlog**（消费评分结果）；**下游执行**（生成 Now 项后进入 requirement 分析 → session） |

**核心流程**：
1. 读取 backlog（priority 已定）、roadmap 现状、strategic_goal 容量分配
2. 计算每个目标的剩余容量
3. 按优先级 + 战略目标匹配从 backlog 拉条目晋升
4. 呈现给用户、捕获确认
5. 更新 roadmap.md + 被晋升条目的 status 字段

**注意命名**：用 "pull"（拉取）而非 "cycle"（周期）—— 明确它是**事件驱动**的晋升动作，不是固定周期仪式。

---

## 4. 后果

### 收益

- 工作生命周期时机**显式规则化**，不依赖 Sprint 假设
- 前向 / 后向职责明晰，避免 plan-next 越位管理执行跟踪
- plan-next v5 状态机让输出 **按当前需要聚焦**，降低认知负担
- 矩阵的系统性覆盖通过 Secondary 层完整保留
- 缺失的两个技能（prioritize-backlog、plan-roadmap-pull）定位清晰、无重叠

### 代价

- plan-next 实现复杂度显著增加（新增状态检测 + 两层输出合成）
- 需要新写两个技能
- 用户需要理解"状态机是矩阵的解释器"这个概念层次

### 风险与缓解

| 风险 | 缓解 |
|---|---|
| 状态误判掩盖真实问题 | Secondary 层兜底；低 confidence fallback 到全矩阵 |
| 事件触发条件定义不严，导致"什么时候该跑 plan-next"仍不清 | 各技能 SKILL.md 明示触发条件；最长 N 天防腐兜底 |
| 两层输出结构过度设计 | Primary / Secondary 仅两层，不再增加；不允许引入第三层 |
| plan-next v5 改造破坏 v4 契约 | 不破坏：frontmatter 仍是 chat；三节结构保留；只在内部扩展 |

---

## 5. 实施清单

按依赖顺序：

| # | 技能 | 变更 |
|---|---|---|
| 1 | `define-strategic-goals` | 加"工程健康"默认目标模板（支撑 ADR 1 决策 3.5） |
| 2 | `capture-work-items` | `strategic_goal_id` 必填；结束时建议（不执行）`prioritize-backlog` |
| 3 | **新：`prioritize-backlog`** | 多框架评分 + 分歧呈现 + 写回 `priority_decision` |
| 4 | **新：`plan-roadmap-pull`** | 晋升 backlog → Now；按 strategic_goal 容量控制 |
| 5 | `define-roadmap` | 每 cycle 按 strategic_goal 分配容量，强制百分比敲定 |
| 6 | `plan-next` v4 → v5 | 加状态检测（Phase 0.6）+ 两层输出合成 |
| 7 | `align-planning` README | 明示后向职责，与 plan-next 前向互补（已部分做） |

**实施顺序**：1-2 先做（字段契约）→ 3-4（新技能）→ 5（消费这些契约）→ 6（plan-next v5，消费所有上游）→ 7（文档对齐）

---

## 6. 不在此决策内

- 具体的事件触发阈值（如 "N 天无 commit 视为 idle" 的 N 值，项目自定）
- `prioritize-backlog` 分歧阈值具体等级差（项目自定，默认 ≥ 2 级）
- 状态机 7 态是否足够（本 ADR 定 7 态，后续发现不足可修订）
- plan-next v5 的技术实现细节（如何读 git log 等，留给 SKILL.md）

---

## 7. 替代方案（被否决）

### 替代 A：plan-next 状态机完全取代矩阵

**否决**：矩阵是 MECE 覆盖基础，放弃会损失系统性视角 + 失去状态误判兜底。**Positioning 错误**：状态机应是矩阵的解释器，不是替代品。

### 替代 B：plan-next 只输出激活层，折叠其他层

**否决**：用户 2026-04-17 会话中反对。失去全矩阵可见性，状态误判时无兜底。

### 替代 C：保留 Sprint cadence，各技能按周期触发

**否决**：违背 AI 时代实际工作节律（session 级压缩）；日历驱动僵化。

### 替代 D：把 prioritize-backlog 自动链入 capture-work-items

**否决**：两技能节律不同（capture 高频、prioritize 批量）；单条 prioritize 缺对比性，评分会失真；破坏 sprint planning ceremony 的批量价值。
