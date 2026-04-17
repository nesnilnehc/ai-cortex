---
artifact_type: adr
created_by: decision-record
lifecycle: snapshot
created_at: 2026-04-17
status: active
---

# 统一价值驱动的工作优先级与规划模型

**状态**: 已接受 (Accepted)
**日期**: 2026-04-17
**范围**: 所有使用 AI Cortex 治理的项目。定义 roadmap 结构、价值评估方法、容量分配机制，并为治理类工作建立战略位置。

---

## 1. 背景

- 使用 AI Cortex 的项目同时承担两类工作：**交付类**（用户可见功能）与**治理类**（ADR、文档规范、技术债、架构对齐等）。
- 业界少数流派（TOGAF、企业架构）使用 "governance roadmap" 这一说法，但在主流产品 / 软件工程社区**不是标准术语**（更常见叫 platform、engineering、tech debt roadmap）。
- 用 RICE 等单一价值框架跨类型比较时，治理类工作在 Reach 维度天然处于数量级劣势，长期被交付压力挤压至不做。
- 单一框架（仅 RICE 或仅 WSJF）会丢失不同维度信号：时间敏感性、用户感知、承诺层级。

---

## 2. 问题

需要同时解决：

1. **分类成本**：多 roadmap / type 标签等做法，每项工作要先判断类型，与"聚焦价值"冲突
2. **信号丢失**：单框架评分无法同时表达价值大小、时间敏感性、承诺层级
3. **治理饿死**：无保护机制时，基础工作在价值竞争中长期失败
4. **无战略代言**：缺"工程健康"类战略目标，治理工作没有合法战略位置

---

## 3. 决策（五合一）

### 3.1 单一 roadmap，不按类型分

所有项目采用**一份 roadmap + 一份 backlog**。不引入 governance / product / platform 等类型分类。全部工作条目在同一体系内按价值竞争。

### 3.2 多框架并行评分，不聚合

每个 backlog 条目并行跑四个框架（Kano 可选用于功能类）：

| 框架 | 捕捉维度 |
|---|---|
| **RICE** | 规模 × 影响（定量） |
| **WSJF** | 时间敏感性（Cost of Delay） |
| **MoSCoW** | 承诺层级（Must/Should/Could/Won't） |
| **ICE** | 定性快速判断 |

**不聚合成单一分数**（加权平均等于丢信号）。各框架结果并列呈现，**突出分歧点**。

### 3.3 分歧呈现 + 用户确认决策

priority 是**用户决策结果**，不是算法输出。工作流：

1. 技能计算四框架分数
2. Surface 框架间分歧（如 RICE=P3 但 WSJF=P1）
3. 用户基于分歧做判断
4. 写回 backlog 条目的 `priority_decision`（含决策依据引用）

分歧阈值：
- 分歧 ≤ 1 级差（如 P2 vs P3） → 默认采信 RICE，无需人工
- 分歧 ≥ 2 级差（如 P0 vs P3） → 必须人工确认

### 3.4 容量护栏按 strategic_goal 分配

roadmap 每 cycle 按 **strategic_goal_id** 分配容量，例（数值为示例，非规定）：

```
cycle 容量：
  目标 1（用户价值）:      60%
  目标 2（市场扩张）:       20%
  目标 3（工程健康）:       20%
```

- 每个 backlog 条目**必填** `strategic_goal_id`
- 容量护栏自动保护所有战略目标，包括工程健康
- **不引入 `type` 字段** —— strategic_goal 已是项目自定义分类维度，复用更自然

### 3.5 强制"工程 / 治理健康"战略目标

每个长期项目的 strategic-goals 必须包含一个"工程 / 治理健康可持续"类目标。`define-strategic-goals` 技能必须引导用户定义。

**默认模板**：

```markdown
## 目标 N: 工程与治理健康可持续

**描述**：确保项目的代码质量、文档一致性、治理机制持续演进，
支撑其他战略目标的长期可达成。

**关键结果示例**（按项目调整）：
- 核心文档规范（ARTIFACT_NORMS）100% 合规
- ADR 覆盖率 ≥ 90%
- 技术债 backlog 项数 ≤ X（按团队规模）
- plan-next 治理健康矩阵通过率 ≥ 95%
- 生产事故 MTTR ≤ Y 小时
```

项目可调整关键结果，但**不能完全省略**此目标。

---

## 4. 后果

### 收益

- 消除 "governance vs product" 分类争论 —— 单一 roadmap、单一 backlog
- 治理工作通过"工程健康"战略目标获得**合法战略代言**，不依赖额外机制保护
- 多框架评分保留决策信号，避免算法伪精确
- 优先级成为**有依据的用户决策**，非黑箱分数

### 代价

- backlog 条目字段增加（`strategic_goal_id` 必填，`priority_decision` 推荐）
- 需要新技能 `prioritize-backlog` 支持多框架评分流程
- 每个项目初始化时需定义"工程健康"目标（增加初始成本）

### 风险与缓解

| 风险 | 缓解 |
|---|---|
| 用户形式化定义"工程健康"但不真正按容量分配 | `define-roadmap` 强制用户明确每个目标的百分比 |
| 多框架分歧过多导致决策疲劳 | 分歧阈值机制（≤1 级差自动、≥2 级差人工） |
| backlog 条目缺 strategic_goal_id | `capture-work-items` 必填校验 |

---

## 5. 实施清单（高层，细节见 ADR 2）

| 技能 | 变更概要 |
|---|---|
| `define-strategic-goals` | 加"工程健康"默认目标模板与必需性引导 |
| `capture-work-items` | backlog 条目必填 `strategic_goal_id` |
| **新：`prioritize-backlog`** | 跑 RICE / WSJF / MoSCoW / ICE，呈现分歧，捕获 `priority_decision` |
| `define-roadmap` | 每 cycle 按 strategic_goal 分配容量，强制百分比 |

---

## 6. 不在此决策内

- 具体的 RICE / WSJF 阈值（项目自定）
- 具体容量比例（60/20/20 是示例）
- plan-next 如何使用 roadmap 和 strategic_goal 信息（见 ADR 2）
- 工作生命周期各阶段时机（见 ADR 2）

---

## 7. 替代方案（被否决）

### 替代 A：双 roadmap（product + governance）

**否决**：
- "governance" 在主流产品社区非标准术语（TOGAF 流派外少见）
- 两份 roadmap 需要同步，协调成本高
- 每项工作仍需判断类型

### 替代 B：单 roadmap + `type` 标签 + 按 type 容量护栏

**否决**：
- `type` 是人造分类轴，每项打标签都有判断成本
- `strategic_goal` 已是项目自定义维度，复用更自然
- 增加字段但不增加信息价值

### 替代 C：单框架（仅 RICE）+ 手动调整

**否决**：
- 手动调整破坏框架客观性，又不如多框架透明
- 多框架分歧保留的信号本身就是决策价值
