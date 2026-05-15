---
artifact_type: adr
created_by: decision-record
lifecycle: snapshot
created_at: 2026-04-24
status: accepted
description: plan-next v6.3 补执行态、roadmap 推进与制品链接
---

# ADR 0003：plan-next v6.3 执行态覆盖与链接方案现实主义

**上下文**：ADR 0002 奠定的 plan-next v6.0 三步法上，回补三类实际差距——roadmap 到 design/task 的推进、task 执行态健康、制品间的链接串联方案

## 背景

v6.0（ADR 0002）重构了输出层语义与三步法，但在"roadmap → requirement/design/task → 代码"的贯穿链上留有三处盲区：

1. **推进范围模糊**：矩阵写了 `design-solution` / `analyze-requirements` 等技能，但未说明是对 roadmap 全量推进还是只对 Now tier 推进；实际敏捷/ShapeUp 惯例是 Now 深度优先。
2. **task 执行态失踪**：S5 "执行中"统一归静默，但 in-progress 超期未动、任务状态与代码不一致、完成未归档等真实发现在 v6 里无路由，造成"执行期 plan-next 几乎无话可说"。
3. **链接串联未言明**：requirement / design / task / PR 之间如何关联，v6 没给方案。默认下游技能的 `path_pattern` 已经用 `{topic}` / `{slug}` 作为锚点，但 plan-next 未利用该现实把"Now tier 某条目缺哪一层制品"精准报出。

三处差距之间有耦合：执行态判健康需要读任务状态（何处？）、需要把任务绑到 roadmap 条目（靠什么链？）——都回到"链接方案"这个前置问题。单独打补丁会反复踩这个耦合。

## 决策

### 决策 1：执行态纳入 S5，用"任务状态 × 代码活动"双信号交叉判健康

S5 "执行中"原为统一静默态，现拆为 2×2 交叉：

| 任务状态 | 代码活动 | 判定 | 归类 |
|---|---|---|---|
| in-progress | 近期 commit / PR 更新 | 健康执行 | S5 静默 |
| in-progress | 超 `task_stuck_days` 无更新 | 执行卡点 | `investigate-root-cause` + 人工 |
| todo | 有相关 commit / 分支 | 追踪漂移 | `align-planning` |
| done | 无 merge 证据 | 完成漂移 | `align-planning` / 人工验证 |
| done | merge 已合但未从 in-progress 移出 | 归档漂移 | `tidy-repo` / `align-planning` |

**单信号不可靠的理由**：仅看任务状态会把"任务维护不规范"误判为健康；仅看 commit 会把"低提交频率文档项目"误判为停滞。两者交叉后，偏离本身就是发现（G3 真相漂移的新子类型）。

**任务 priority 字段**：仅用于多个执行卡点间的 tiebreak，不参与 plan-next 的 P0-P3 路由优先级——治理层级不可让任务优先级僭越。

**降级**：若 `task_source` 未发现可扫任务源，S5 回退到仅代码活动判断（原 v6.2 行为），诊断依据注明降级原因。

### 决策 2：下游就绪度评估仅作用于 roadmap Now tier，深度优先逐层推进

原矩阵对 requirement / design / task 缺口的判定隐含全量扫描。修正为：

- **Now tier（1-3 条）**：按 slug 在下游目录 glob 匹配，无下游 = G1 真缺口
- **Next / Later tier**：无下游 = 正常状态，**不报告**
- **未分层 roadmap**：先路由 `promote-roadmap-items`，**不评估下游**
- **深度优先**：每个 Now tier 条目一次只报**最上游缺口**（requirement 缺时不同时提 design / task）

**理由**：广度优先（对所有 roadmap 条目都写全下游）会产生过期文档——50 条 roadmap 各写设计文档，执行到第 30 条时前 29 条的设计早已漂移。Now/Next/Later 分层的设计意图就是显式区分"立即深入"vs"先搁着"。

### 决策 3：矩阵 What/When G1 补入 `breakdown-tasks`

原 What/When G1 缺少"design 已有但 task 未拆"这个真实缺口的路由。补入 `breakdown-tasks`，限定条件为"Now tier + design 已 present + task 未拆"。

### 决策 4：链接模式固定枚举，识别权威委托 `discover-docs-norms`，plan-next 作为消费者

**职责三分**：

| 技能 | 职责 |
|---|---|
| **`discover-docs-norms`** | 维护模式枚举、扫描仓库、识别当前项目采用的模式（权威） |
| **`define-docs-norms`** | 把识别结果与候选模式作为选项呈现给用户，用户选定后固化到 `ARTIFACT_NORMS.md` |
| **plan-next** | 读识别结果，按结果决定扫描策略；不自行识别、不定义枚举 |

**固定模式枚举**：

权威定义在新规范 **[`specs/linking-modes.md`](../../../specs/linking-modes.md)**（LINKING_MODES_SPEC_V1，本 ADR 配套产出）。共 6 项：`slug` / `colocation` / `parent-pointer` / `manifest` / `mixed` / `none`。每项按 7 维描述（本质 / 识别信号 / 追溯方向 / 维护成本 / 工具要求 / 适用场景 / 示例），消除 LLM 与人对"模式"一词的理解分歧。`discover-docs-norms` 消费此规范的识别信号，`define-docs-norms` 消费此规范的描述作为选择 UI，plan-next 消费此规范的消费规则（§5）。

**plan-next 的消费流程**：

1. 读 `ARTIFACT_NORMS.md` 的 `linking_mode` 字段（由 `define-docs-norms` 写入，代表用户已选定）
2. 若无，读 `discover-docs-norms` 上次产生的提案文件（未批准的候选）
3. 若两者都无 / 过期 → **前置闸门路由**：在"现在该做"加一条 `discover-docs-norms` → `define-docs-norms` 作为 Now tier 下游评估的前置动作；不自行启发识别

**和 `execute=false` 的协调**：默认模式下 plan-next 仅读 discover 的既往产出；不调用生成新识别。`execute=true` 且识别结果缺失 / 过期时，plan-next 才按路由推荐顺序先调用 `discover-docs-norms`。

**替代方案（已拒绝）**：
- **"涌现属性，无枚举"**（前一版本尝试）：拒。用户无选择锚点；discover-docs-norms 产出格式不可机器消费；plan-next 扫描策略变得模糊。
- **plan-next 自带识别逻辑**：拒。重复实现 discover-docs-norms 的职责；同一功能两处维护必然漂移；违反单一职责。
- **模式无限扩展（无固定枚举）**：拒。识别判据无法定义；用户教育成本极高；定义 SSOT 失焦。
- **本决策（固定 6 枚举 + 职责三分 + plan-next 消费）**：采纳。枚举有限可教育；识别集中一处；plan-next 聚焦路由。

**下行清单的维护职责明示**：若识别结果是 manifest / mixed 含 manifest，plan-next **只读不写**。漂移作为 G3 报出，维护由 `align-*` 或下游技能承担。

## 替代方案

1. **四方案平等支持，plan-next 保持中立**：拒。技术现实已决定——方案 1 / 3 需下游协同改造。平等识别四方案会让 plan-next 逻辑膨胀，且误导用户以为方案 1 / 3 可即插即用。
2. **单独引入执行态新状态 S5a/b/c**：拒。7 态变 8+ 态，破坏 v6 "3 步法 + 7 态"的简洁叙事，且健康/卡点的区分是 S5 内部子态，不是新维度。
3. **把执行态交给 work-management 新技能，plan-next 继续 S5 静默**：拒。plan-next 定位是"治理入口路由器"，执行卡点本质是治理发现（任务状态漂移、完成漂移），不是执行引擎职责。
4. **方案 4 manifest 设为默认**：拒。维护成本显著（每次下游技能执行都要同步清单），且现有技能不产出清单。强加默认会让用户承担新负担。

## 后果

**正面**：
- 执行期不再是 plan-next 的盲区；S5 从"统一静默"升级为"健康 / 卡点 / 3 类漂移"五态
- Now tier 作用域 + 深度优先显著降低误报（不再因 50 条 roadmap 报 200 条下游缺口）
- 链接方案明确：slug 默认 + manifest 识别；消除前版"四方案中立"的认知负担
- `breakdown-tasks` 纳入矩阵，填补 design → task 真实缺口

**负面**：
- MINOR bump 6.3.0；新增 frontmatter 配置（`task_source` / `roadmap_tier_source` / `artifact_norms_path` / `norms_proposal_path` / `thresholds.task_stuck_days`）
- 2.5 / 2.6 / 2.7 三节新增让步骤 2 变长；用 Anti-Patterns 约束缓冲
- 共位目录 / 父指针方案使用者需等 v7.x，短期只能降级为 slug

**中性**：
- v7.x 将在下游技能栈协同改造后重新评估方案 1 / 3 的可行性（例如 design-solution 的 `path_pattern` 改为支持 `work/<slug>/design.md`）
- 方案 4 的自动维护机制（ADR 0003 未决）若未来需要，可新增 `align-work-item-manifest` 技能或在下游技能中加"登记步骤"

## 后续跟进（v7.x 候选）

**链条断点（本 ADR 引出的前置工作）**：决策 4 约定 plan-next 消费 `discover-docs-norms` 的识别结果，但当前 `discover-docs-norms` 尚未实现链接模式枚举与识别、`define-docs-norms` 尚未实现模式选择 UI。v6.3 的 plan-next 可以完成代码侧实现（读字段、前置闸门路由），但实际生效需下面两项落地。

**必需前置（阻塞 v6.3 full-effect 但不阻塞 plan-next 代码合并）**：

1. **`discover-docs-norms` v3.0**：新增"链接模式识别"章节，维护 6 项固定枚举（slug / colocation / parent-pointer / manifest / mixed / none）、对应识别判据、冲突解决规则；扫描后输出 `linking_mode: <枚举值>` 到提案文件
2. **`define-docs-norms` v2.0**：新增"链接模式选择"流程，把识别结果作为推荐选项 + 其他枚举作为备选呈现给用户；用户选定后把 `linking_mode` 字段写入 `ARTIFACT_NORMS.md`

**v7.x 扩展（非阻塞）**：

3. **colocation / parent-pointer 模式的完整生效**：需下游技能栈接受 `path_pattern` 改造（如 `design-solution` 支持输出到 `work/<slug>/design.md`）
4. **下行清单维护机制**：评估 `align-work-item-manifest` 新技能 vs 在下游技能中加"登记步骤"两条路径，决定 manifest 模式的维护落地
5. **规范驱动架构完整闭环**（v7.x 总愿景 / 最大工作量）：
   - **目标**：下游所有产出制品的技能（`analyze-requirements` / `design-solution` / `breakdown-tasks` / `capture-work-items` / `define-roadmap` / `design-strategic-goals` 等）在运行时读 `ARTIFACT_NORMS.md` 决定实际输出路径与命名
   - **现状差距**：SKILL.md frontmatter 中的 `path_pattern` 目前是**硬规则**；目标状态需降级为**默认值**，被规范文件覆盖
   - **前置依赖**：`specs/artifact-contract.md` 需新增"规范读取协议"小节规定技能如何读取 `ARTIFACT_NORMS.md`、如何合并默认值与项目覆盖、规范缺失时的 fallback 行为
   - **下游技能改造**：13+ 个产出制品的技能都需增加"规范读取"步骤，属 MAJOR bump 级别
   - **受益**：`ARTIFACT_NORMS.md` 真正成为 Rules 层最高权威；项目可定制路径 / 命名 / 链接约定而无需 fork 技能；plan-next 彻底脱离启发式

**落地顺序建议**：1 → 2 → (plan-next v6.3 full-effect) → 3 / 4 → 5。前两项是 plan-next v6.3 识别功能真正生效的前提；plan-next 代码侧的契约消费逻辑已在 v6.3 完成，等 1 / 2 落地即可自动生效。

## 参考

- ADR 0002：plan-next v6.0 结构重构
- **`specs/linking-modes.md` v1.0.0**（LINKING_MODES_SPEC_V1，本 ADR 配套产出）——链接模式的权威定义与 6 项枚举
- `skills/plan-next/SKILL.md` v6.3.0 步骤 2.5 / 2.6 / 2.7
- `specs/artifact-contract.md`
- `skills/discover-docs-norms/SKILL.md` v2.0.0
- `skills/define-docs-norms/SKILL.md` v1.0.0
- 下游技能 `path_pattern` 汇总（见决策 4 表格）
