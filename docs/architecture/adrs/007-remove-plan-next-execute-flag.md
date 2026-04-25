---
artifact_type: adr
created_by: decision-record
lifecycle: snapshot
created_at: 2026-04-25
status: active
---

# ADR 007：移除 plan-next 的 `execute` 参数（v9.0.0）

**状态**：Accepted
**日期**：2026-04-25
**上下文**：plan-next v8.1 的 `execute=true` 模式实际上是空头支票——文档只一句"按推荐顺序串调下游"，没定义错误处理、重试、并行、检查点等执行引擎语义；同时与"导航不开车"的 stateless / read-only 定位冲突

## 背景

plan-next 的 frontmatter 一直有 `execute: false` 默认参数；`execute=true` 模式字面意义是"按路由顺序执行下游技能"。但深入审视后发现：

1. **vaporware 现状**：`execute=true` 在文档中只一句话，没有任何执行引擎该有的实质语义——
   - 错误如何处理？没说
   - 步骤间状态怎么传？没说
   - 失败重试 / 部分成功 / 回滚？都没说
   - 并行/串行？没说
2. **与定位冲突**：plan-next 在 v6.3-v8.1 多轮迭代中已经把"**导航不开车**"作为硬边界——执行态边界节明确说"不自动推进执行（默认 `execute=false`）——只导航不开车"。而 `execute=true` 一旦被用，plan-next 就变成驾驶员，违反此边界。
3. **职责膨胀风险**：保留 `execute=true` 暗示 plan-next 应该长出执行引擎能力——错误处理、状态机、重试、并行——这些是 workflow engine 的职责，与 plan-next "**入口路由器**"定位不符。

## 决策

### 决策 1：移除 `execute` 参数

- frontmatter `input_schema.defaults` 删除 `execute: false` 字段
- frontmatter `input_schema.description` 不再列 `execute flag`
- agent.yaml `inputs:` 不再列 `optional execute flag`
- 所有提及 `execute=false` / `execute=true` 的句子改写为"plan-next 永不执行下游"

### 决策 2：明示 read-only 硬边界

文档级声明：plan-next 是 **read-only** 诊断器——盘点 + 状态识别 + 缺口判定 + 路由建议。**永不调用**任何下游技能。这不是"默认行为"也不是"可配置"，是硬边界。

### 决策 3：自动化由外层组合驱动

自动化迭代场景由三层正交原语组合：

| 层 | 职责 | 技能 |
|---|---|---|
| 调度（周期化） | "每 N 分钟触发一次" | `loop` |
| 驱动（执行 1 步） | 读 plan-next 输出 → 挑"现在该做"最高优先级 1 条 → 执行 → 处理失败 | orchestrator 技能（如 `auto-iterate`） |
| 诊断（read-only） | 盘点 + 识别 + 路由建议 | **plan-next** |

典型组合：

- `/plan-next` —— 一次性诊断
- `/loop /plan-next 30m` —— 周期诊断（持续监控 + 人工反应）
- `/loop /auto-iterate 30m` —— 全自动 autopilot（需 `auto-iterate` 落地）

每层失败 / 重试 / 状态由各层自处理；plan-next 不背执行职责。

### 决策 4：`auto-iterate` 登记为后续工作项（不在本次实现）

新建 `auto-iterate` 技能不属于本次 v9.0 scope。本 ADR 只移除 `execute` 字段、明示边界、登记 orchestrator 模式。`auto-iterate` 落地由独立工作推进（包含错误处理、用户确认、`--auto` 模式、checkpoint 等执行引擎设计）。

## 替代方案（已拒绝）

1. **保留 `execute=true` 并把它实现完整**：拒。会让 plan-next 长出 workflow engine 能力，违反"入口路由器"单一职责定位；plan-next 的稳定性与 orchestrator 的迭代性混在一起，演化耦合。
2. **保留 `execute=true` 作为占位 / 已废弃字段**：拒。空头字段会误导新用户尝试使用并撞失败；干净移除比软废弃便宜。
3. **不动 `execute`，用文档约束"实践中只用 false"**：拒。约束应反映在 API 表面，不是"看文档时小心"。

## 后果

### 正面

- **plan-next 边界更紧**：read-only 在 frontmatter / Behavior / Anti-Patterns / Self-Check 一致，无 escape hatch
- **职责拆分清晰**：诊断（plan-next）/ 驱动（orchestrator）/ 调度（loop）三层正交，未来扩展不互扰
- **空头字段消除**：`execute=true` 不再吊在 frontmatter 里挑战读者实现想象力
- **API 收窄**：`input_schema` 字段更少（虽 marginal），与"plan-next 是导航器"的简洁定位匹配

### 负面

- **MAJOR bump**（v8.1 → v9.0）：移除 frontmatter 输入字段是 API breaking change
- **依赖未来 `auto-iterate`**：autopilot 场景在 `auto-iterate` 落地前不可用——但 v8.1 的 `execute=true` 实际也不可用（vaporware），所以是把 vaporware 替换为"未实现的明确占位"

### 中性

- 用户传 `execute: true/false` 在 v9 会被忽略（input 不再识别此字段，不报错）
- 历史 `execute=false` 默认行为 = v9 的 read-only 行为，迁移无变化

## 参考

- ADR 002 / 003 / 004 / 005 / 006 —— plan-next 演化历程
- v8.1-lts tag —— 移除前的最后状态（回滚锚点，待 v9.0 commit 后打）
- 后续工作：建立 `auto-iterate` 技能（不在本 ADR scope）
