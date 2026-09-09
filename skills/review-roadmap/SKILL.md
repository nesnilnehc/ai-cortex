---
name: review-roadmap
description: "Review an existing roadmap document against roadmap-quality criteria: core model completeness, capacity baseline and allocation, metric triplets, outcome framing, dependency mapping, and change frequency. Evaluative atomic skill; output is a findings list."
description_zh: 按 roadmap-quality 判据评估既有路线图文档：核心模型完整性、容量基线与分配、指标三元组、结果导向、依赖已映射、变更频率。评估型原子技能，产出 findings 列表。
tags: [code-review, planning]
version: 1.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [review roadmap, roadmap review, roadmap quality, check roadmap, roadmap health]
input_schema:
  type: document-artifact
  description: Existing roadmap document (path or content) to evaluate; secondary inputs are strategic-goals.md and the backlog items referenced by the Now tier
  artifact_type: roadmap
output_schema:
  type: findings-list
  description: Zero or more findings with location, category, severity, and suggestion, covering all five roadmap quality dimensions
---

# 技能：审查路线图（Review Roadmap）

## 目的 (Purpose)

按既定质量判据评估**现有路线图文档**。不生成也不改写路线图——那是 `define-roadmap` 与 `update-roadmap` 的职责。产出 **findings 列表**，供作者在下游消费之前修补。

**判据不在本技能内**：全部条目定义在 [rules/roadmap-quality.md](../../rules/roadmap-quality.md)，本技能只负责执行评估与组织输出。判据变更改那份 rule，不改本文件。

---

## 核心目标（Core Objective）

**首要目标**：产出覆盖五个质量维度的路线图 findings 列表，使作者能在晋升决策依赖它之前把问题补齐。

**成功标准**（必须全部满足）：

1. ✅ 五个维度全部扫过：完整性 / 可执行性 / 清晰性 / 合理性 / 可追溯性
2. ✅ 每条 finding 含 location / category / severity / title / description / suggestion
3. ✅ 判据全部引自 `rules/roadmap-quality.md`，本技能不新造判据
4. ✅ 无法评估的维度显式标注「无法评估」及原因，不静默跳过
5. ✅ 不改写路线图，只出发现与建议

**验收测试**：作者能否只看 findings 列表就知道该改哪几处、改成什么样？

**交接点**：findings 交给作者；结构性缺口交接 `define-roadmap`，状态与时点类缺口交接 `update-roadmap`。

---

## 范围边界（Scope Boundaries）

**本技能负责**：

- 按 `rules/roadmap-quality.md` 逐维评估既有路线图
- 产出带位置、严重度与建议的 findings 列表
- 标注无法评估的维度及原因

**本技能不负责**：

- 生成或改写路线图（`define-roadmap` / `update-roadmap`）
- 判定编排 mode —— 那是编排层「检测上下文」的职责，本技能只出 findings
- 晋升决策（`promote-roadmap-items`）
- 依赖识别（`map-item-dependencies`）
- 维护判据本身（`rules/roadmap-quality.md`）

---

## 使用场景（Use Cases）

- **晋升前把关**：容量与依赖判据不过关时，晋升算不出正确结果
- **接手他人路线图**：快速看清这份路线图缺什么
- **定期体检**：路线图是 living 文档，随时间会漂
- **编排链路的入口**：作为 `orchestrate-roadmap-planning` 的第 0 步，为后续步骤提供条件判定依据

---

## 行为（Behavior）

### 交互政策

- **默认**：读取 `docs/process-management/roadmap.md` 或项目规范路径；用户可指定路径或直接粘贴内容
- **只读**：全程不修改任何文件
- **不追问**：这是一次性评估，缺信息就记为 finding 或标为无法评估，不与用户来回澄清

### 执行过程

1. **加载判据**：读取 [rules/roadmap-quality.md](../../rules/roadmap-quality.md)。**该文件缺失时 halt**——没有判据就没有评估基准，此时凭印象打分只会产出看似权威实则无依据的结论。
2. **加载路线图与佐证源**：读取目标文档。判据中有三条的数据不在 roadmap.md 里，须一并读取，否则这些维度无从求值：

   | 判据 | 数据在哪 |
   |---|---|
   | Now 层条目可追溯到所属 strategic_goal | 条目 frontmatter 的 `strategic_goal_id`，兼看 `docs/project-overview/strategic-goals.md` |
   | Now 层条目无未决前置依赖 | 条目 frontmatter 的 `depends_on` |
   | 优先级非单一来源拍定 | 条目 frontmatter 的 `priority_decision`（含 `strategic_override`） |

   **缺失处理**：backlog 条目读不到、或 roadmap.md 的 Now 层未引用具体条目时，这三条判据标注为「无法评估 —— <原因>」。**不得因读不到就记为通过**，那等于让判据形同虚设。
3. **逐维扫描**：按 rule 的五维清单逐条核对，每条不通过即生成一条 finding。
4. **变更频率维度的工具适配**：该维度需要读 git log 统计 roadmap.md 的结构性变更次数。
   - **发现**：确认当前目录是 git 仓库且 roadmap.md 有提交历史
   - **执行**：统计设定窗口内该文件的结构性变更次数，与 rule 中的阈值比较
   - **缺失处理**：非 git 仓库、浅克隆导致历史不全、或该文件无提交历史时，本维度标注为「无法评估 —— <具体原因>」。**不得静默跳过，也不得据此推断该维度通过**
5. **定严重度**：按下表机械映射，不做主观加权。
6. **输出 findings 列表**。

### 严重度映射

| 严重度 | 判定 |
|---|---|
| `关键` | 缺总容量基线或容量分配；核心模型四件套缺项；Now 层条目有未决前置依赖 |
| `主要` | 成功指标非三元组；里程碑或关键举措未用规定句式；容量百分比之和 ≠ 100%；工程健康目标为 0% |
| `轻微` | 缺「本轮明确不做」章节；缺最后更新日期；变更频率接近但未越阈值 |

### findings 格式

```yaml
- location: <文档内章节或行>
  category: 完整性 | 可执行性 | 清晰性 | 合理性 | 可追溯性
  severity: 关键 | 主要 | 轻微
  title: <一句话结论>
  description: <哪里不符合，对照哪条判据>
  suggestion: <改成什么样，可直接照做>
```

---

## 输入与输出 (Input & Output)

**输入**：既有路线图文档（路径或内容）；`rules/roadmap-quality.md`；佐证源 `strategic-goals.md` 与 Now 层引用的 backlog 条目。

**输出**：findings 列表（零条或多条）+ 无法评估维度的说明。零 findings 时明确说明该路线图通过全部判据。

---

## 限制（Restrictions）

### 硬边界（Hard Boundaries）

- **不改写**：不生成新的路线图文本、里程碑或指标。只出 findings 与建议，落笔交给作者或 `define-roadmap`
- **不内嵌判据**：所有判据引自 `rules/roadmap-quality.md`；需要新判据时改那份 rule，不在本技能里加
- **rule 缺失即 halt**：没有判据基准不得凭印象评估
- **不输出 mode**：编排层的上下文检测由编排层自己做，本技能只出 findings
- **无法评估必须显式标注**：不得因为工具缺失或佐证源读不到就把某维度记为通过

### 反模式（避免）

- ❌ **把判据抄进技能**：判据两处维护必然漂移，这正是本技能刻意规避的
- ❌ **静默跳过 git 依赖的维度**：读不到历史就说读不到，不要让读者以为已评估
- ❌ **主观加权严重度**：severity 按映射表机械判定，不按「感觉这条更要紧」调整
- ❌ **顺手把问题改了**：评估与改写混在一起，作者就看不清原始问题是什么

### 技能边界（避免重叠）

| 动作 | 归属 |
|---|---|
| 生成 / 改写路线图 | `define-roadmap` |
| 改状态 / 挪期 | `update-roadmap` |
| 晋升 / 降级 | `promote-roadmap-items` |
| 依赖识别 | `map-item-dependencies` |
| 判据维护 | `rules/roadmap-quality.md` |
| 跨层治理诊断 | `plan-next` |

---

## 自检（Self-Check）

- [ ] 已加载 `rules/roadmap-quality.md`；缺失时已 halt
- [ ] 五个维度全部扫过
- [ ] 每条 finding 六个字段齐全
- [ ] 严重度按映射表机械判定
- [ ] 变更频率维度已走「发现 → 执行 → 缺失处理」；无法评估时已写明原因
- [ ] 依赖 backlog 条目 frontmatter 的三条判据已读取佐证源；读不到时已标「无法评估」而非记为通过
- [ ] 未改写路线图文档
- [ ] 未输出 mode 或其他编排层字段
- [ ] 零 findings 时已明确说明通过

---

## 示例（Examples）

### 示例 1：缺容量基线（主流场景）

**输入**：一份 Now / Next / Later 齐全的路线图，含容量分配百分比表，但表头没有总容量基线。

**输出**（节选）：

```yaml
- location: "## 容量分配（当前 cycle）"
  category: 可执行性
  severity: 关键
  title: 缺总容量基线，下游容量护栏算不出结果
  description: 容量分配只有百分比，没有声明总容量基线。promote-roadmap-items 的公式是「百分比 × 总容量基线」，缺基线即缺分母，各目标的分配容量无法计算。对照 rules/roadmap-quality.md §2。
  suggestion: 在容量分配表头补一行总容量基线，格式为「<N> 人周（<人数> 人 × <周期> − 开销，按有效工时 <60–70>% 折算）」。可重跑 define-roadmap 第 8 步采集。
```

**结果**：作者知道这份路线图看着完整，但晋升环节会立刻卡住。

### 示例 2：非 git 仓库（边缘场景）

**输入**：路线图内容由用户直接粘贴，不在任何 git 仓库中。

**流程**：

1. 前四个维度正常扫描。
2. 变更频率维度：发现阶段即确认无 git 仓库 → 无法读取历史。
3. 标注该维度为「无法评估 —— 输入为粘贴内容，无 git 提交历史可供统计变更频率」。
4. **不据此推断该维度通过**，也不在 findings 里编造一条变更频率相关问题。

**输出**（节选）：

```text
无法评估的维度：
- 合理性 / 变更频率：输入为粘贴内容，无 git 提交历史。
  如需评估此维度，请提供仓库内的 roadmap.md 路径。
```

**结果**：读者清楚哪一块没查过，不会误以为全维度都过了。

### 示例 3：判据文件缺失（边缘场景）

**输入**：一份路线图，但项目未安装 `rules/roadmap-quality.md`。

**流程**：

1. 第 1 步加载判据即失败。
2. **halt**，不进入扫描。
3. 说明理由：没有判据基准就评估，产出的会是一份看似权威、实则无依据的清单——这比不评估更有害。
4. 给出补救路径：从 AI Cortex 安装 `rules/roadmap-quality.md`，或显式指定另一份判据文件。

**结果**：技能拒绝在无基准的情况下产出结论，而不是凭印象凑一份。
