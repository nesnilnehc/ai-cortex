---
artifact_type: rule
name: roadmap-quality
version: 1.0.0
scope: 评审或自检路线图文档时
recommended_scope: user
status: active
---

# Rule: 路线图质量（Roadmap Quality）

> 路线图制品的评审清单。每条独立可验证。
>
> 适用于：由 [skills/define-roadmap](../skills/define-roadmap/SKILL.md) 产出、存放于 `docs/process-management/roadmap.md`（或项目规范路径）的路线图文档。
>
> **本 rule 是路线图判据的唯一权威源**。生产侧（`define-roadmap`）、诊断侧（`plan-next`）、评审侧（`review-roadmap`）均引用本文件，不各自维护一份表述。

---

## 5 维审查清单

### 1. 完整性（结构齐全吗？）

- [ ] 每个阶段含核心模型四件套：里程碑（Milestone）/ 关键举措（Strategic Bets）/ 成功指标（Metrics）/ 推进条件（Promotion Criteria）
- [ ] 含「容量分配」章节，且声明了**总容量基线**（人周数 + 折算口径）
- [ ] 每个 strategic_goal 有百分比，百分比之和 = 100%
- [ ] 关键举措每阶段 2–5 个，不为空

### 2. 可执行性（下游能直接消费吗？）

- [ ] 总容量基线存在 —— 缺基线则 `promote-roadmap-items` 的「百分比 × 基线」无分母，容量护栏算不出结果
- [ ] 工程健康类目标容量 ≠ 0%
- [ ] 推进条件可判定（写明什么条件满足才进入下一阶段），非「视情况而定」
- [ ] Now 层条目数在 WIP 上限内（默认 3–5，项目可覆盖）
- [ ] 每个 Now 层条目可追溯到所属 strategic_goal

### 3. 清晰性（无歧义吗？）

- [ ] **成功指标为三元组**：当前值 / 目标值 / 参考系。参考系取行业基准、项目历史值或经验阈值；无参考时写「项目自定（无外部基准）」
- [ ] 里程碑为结果句式（`让 [客群] 能够 [达成某事]，从而 [业务影响]`），不是交付物名称
- [ ] 关键举措为可证伪的假设句式（`我们相信 [做 X] 对 [人群] 会带来 [结果]，因为 [假设]`），不是名词短语
- [ ] Later 阶段仅指方向，不写具体日期

### 4. 合理性（这份路线图成立吗？）

- [ ] 无功能列表：条目描述的是结果，不是功能名（如「深色模式」「SSO」这类裸功能名即为不合格）
- [ ] 无 TODO 混入：不含执行级任务
- [ ] 依赖已映射：Now 层条目无未决前置依赖；跨条目依赖已在条目 `depends_on` 中登记
- [ ] 优先级非单一来源拍定：条目优先级有可查的评分依据或显式记录的战略覆盖理由
- [ ] 变更频率在阈值内：路线图未在短周期内被反复重排（默认阈值为一个 cycle 内结构性变更 ≤ 2 次，项目可覆盖）

### 5. 可追溯性（能定位变更影响吗？）

- [ ] 每个阶段目标可映射到 `docs/project-overview/strategic-goals.md` 中的某一目标
- [ ] 明确声明「Backlog 必须映射到路线图，不属于路线图的需求默认不做」
- [ ] 文档标注了最后更新日期
- [ ] 被排除的干系人诉求（若有）在「本轮明确不做」章节列出并说明原因

---

## 反模式

每条对应上文某一维判据的失效形态，按维度顺序排列。检出时回查对应维度的清单条目。

**§1 完整性失效**

- ❌ **分母缺席**：只写各目标百分比，不写总容量基线。下游「百分比 × 基线」无从计算，容量护栏成了摆设

**§2 可执行性失效**

- ❌ **治理无容量**：工程健康类目标分到 0%。技术债与文档工作没有容量归属，在价值竞争中永远排不进来
- ❌ **Now 层堆积**：一次拉入远超 WIP 上限的条目。看着满负荷，实际每项都在等
- ❌ **推进条件含糊**：写「视情况而定」而非可判定的条件，阶段流转变成拍脑袋

**§3 清晰性失效**

- ❌ **指标缺参考系**：只写目标值，读者无法判断这个目标是激进还是保守
- ❌ **交付物冒充结果**：里程碑写成「上线 X 模块」而非「让谁能够做到什么」
- ❌ **赌注退化为名词**：关键举措只有名称，没有可证伪的假设，事后无从判断赌对没有

**§4 合理性失效**

- ❌ **功能清单冒充路线图**：通篇功能名，看不出为什么做、做成什么算成
- ❌ **依赖不查就排序**：只按优先级与容量排，被上游阻塞的条目照样进 Now，占着容量不产出
- ❌ **优先级无据可查**：既没有评分依据，也没有记录战略覆盖的理由，事后无人能复盘当初为何如此排
- ❌ **把重排当响应力**：每来一条新信息就动一次结构，变更频率越过阈值仍不自省

**§5 可追溯性失效**

- ❌ **目标映射断裂**：路线图条目找不到对应的战略目标，无法回答「这件事服务于哪个目标」
- ❌ **排除项不落纸**：只靠「不在路线图上的默认不做」这条隐式规则，被挡掉的诉求方逐个来问

**贯穿性失效**

- ❌ **容量满打满算**：百分比按日历容量而非有效容量分配，一个紧急问题就打乱全盘

---

## 判据依据

本清单的维度划分与失效形态由本 rule 自身的五维结构推出。其中涉及的产品管理通用概念，出处为公开出版物，列此便于追溯与延伸阅读：

| 概念 | 一手来源 |
| :--- | :--- |
| Now / Next / Later 分层；路线图是计划而非承诺 | McCarthy, Lombardo, Ryan, Connors，《Product Roadmaps Relaunched》(2017) |
| RICE 打分刻度与置信度锚点 | Intercom，"RICE: Simple prioritization for product managers" (2016) |
| 可证伪的假设句式 | Gothelf & Seiden，《Lean UX》 |
| 结果导向优于功能清单（"feature factory" 之弊） | Melissa Perri，《Escaping the Build Trap》 |
| 避免由个人意见定优先级（HiPPO） | Avinash Kaushik，*Web Analytics: An Hour a Day* |

---

## 关联资产

- **生产侧**：[skills/define-roadmap](../skills/define-roadmap/SKILL.md) —— 产出时按本清单构造
- **评审侧**：[skills/review-roadmap](../skills/review-roadmap/SKILL.md) —— 按本清单出 findings
- **消费侧**：[skills/promote-roadmap-items](../skills/promote-roadmap-items/SKILL.md) —— 容量与 WIP 判据的消费方
- **同族评审 rule**：[requirement-quality](./requirement-quality.md) / [functional-design-quality](./functional-design-quality.md) / [technical-design-quality](./technical-design-quality.md) / [task-quality](./task-quality.md)
