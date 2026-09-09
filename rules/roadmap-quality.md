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

- ❌ **功能驱动无结果**：路线图列功能名而无结果与指标，读者看不出为什么做
- ❌ **单一来源拍板**：优先级由个人意见定，无评分依据也无战略覆盖记录
- ❌ **当成承诺**：把路线图当交付合同，用具体日期锁死 Next / Later
- ❌ **未映依赖**：不检查依赖就排序，导致 Now 层条目被上游阻塞
- ❌ **闭门产出**：路线图无干系人输入，也未列出被排除项
- ❌ **路线图横跳**：每来一条新信息就重排一次，把频繁变更当成响应力
- ❌ **指标缺参考系**：只写目标值，读者无法判断该目标值是激进还是保守
- ❌ **容量满打满算**：百分比按日历容量而非有效容量分配，未规划工作一来就全盘打乱

---

## 判据来源

三条判据来自外部实践，在此登记出处以便追溯：

| 判据 | 出处 |
| :--- | :--- |
| 五条反模式（功能驱动 / 单一来源拍板 / 当成承诺 / 未映依赖 / 闭门产出） | deanpeters/product-manager-skills 的 `roadmap-planning` |
| 变更频率阈值与防横跳 | anthropics/knowledge-work-plugins 的 `roadmap-update` |
| 结果化检查（条目是否仍停留在功能名） | phuryn/pm-skills 的 `outcome-roadmap` |

---

## 关联资产

- **生产侧**：[skills/define-roadmap](../skills/define-roadmap/SKILL.md) —— 产出时按本清单构造
- **评审侧**：[skills/review-roadmap](../skills/review-roadmap/SKILL.md) —— 按本清单出 findings
- **消费侧**：[skills/promote-roadmap-items](../skills/promote-roadmap-items/SKILL.md) —— 容量与 WIP 判据的消费方
- **同族评审 rule**：[requirement-quality](./requirement-quality.md) / [functional-design-quality](./functional-design-quality.md) / [technical-design-quality](./technical-design-quality.md) / [task-quality](./task-quality.md)
