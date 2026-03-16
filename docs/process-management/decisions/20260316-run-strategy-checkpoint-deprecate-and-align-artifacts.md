# 不保留 run-strategy-checkpoint 与 align-* 产物的取舍

**状态**: 提案 (Proposed)  
**日期**: 2026-03-16  
**范围**: 移除 run-strategy-checkpoint 后，align-* 技能是否应产出「策略检查点」类产物及如何落地。

---

## 1. 决策前提

- **倾向**: 不保留技能 `run-strategy-checkpoint`。
- **待决**: align-* 是否应有「策略/里程碑检查点」类相关产物；若有，形态与归属（谁产出、写到哪里）。

---

## 2. 当前产物理清

| 技能 | 产出物 | 路径 | 生命周期 |
| :--- | :--- | :--- | :--- |
| align-planning | Planning Alignment Report | `docs/calibration/planning-alignment.md` | living |
| align-backlog | Backlog Alignment Report | `docs/calibration/backlog-alignment.md` | living |
| align-architecture | Architecture Compliance Report | `docs/calibration/architecture-compliance.md` | living |
| run-checkpoint | Cycle report（聚合） | `docs/calibration/cognitive-loop.md` | living |
| run-strategy-checkpoint（拟移除） | Strategy checkpoint report | `docs/calibration/YYYY-MM-DD-strategy-checkpoint.md` | snapshot |

**run-checkpoint 规则**: 编排时**不**单独持久化各 align-* 的报告，只产出**一份** cycle report（cognitive-loop.md），其中汇总各步发现与 Recommended Next Tasks。

**run-strategy-checkpoint 当前提供的价值**: 在治理门产出「按里程碑/目标的状态（在轨 / 偏离 / 阻塞）+ 建议下一步」的**独立快照报告**，可选择性消费 align-planning / align-backlog 的输出作为证据。

---

## 3. 取舍选项

### 选项 A：不增加策略检查点类产物

- **做法**: 移除 run-strategy-checkpoint 后，不再有专门的「策略检查点」报告。治理门只看：
  - 单独运行时的 align-planning / align-backlog 报告，和/或
  - run-checkpoint 的 cognitive-loop 报告（已含发现 + Recommended Next Tasks）。
- **优点**: 技能与产物最简单；不新增契约与路径。
- **缺点**: 没有「按里程碑/目标列出的在轨/偏离/阻塞 + 建议」的固定视图，需从对齐报告或 cycle report 中自行提炼。

---

### 选项 B：由 run-checkpoint 的 cycle report 承载「策略/里程碑状态」视图

- **做法**: 不保留 run-strategy-checkpoint；在 run-checkpoint 的**周期报告**中增加固定小节（例如「Strategy / Milestone status」）：当本周期执行了 align-planning（及可选的 align-backlog）时，根据其发现**综合**出「每个里程碑/目标：在轨 / 有风险 / 偏离 / 阻塞 + 简要证据 + 建议」。
- **产出**: 仍是单一 cognitive-loop.md，无额外文件。
- **优点**: 治理门仍有一份「按里程碑/目标的状态 + 建议」视图，且与现有「单产物」规则一致；不增加新技能。
- **缺点**: run-checkpoint 的 report 结构略加重；需在 SKILL 中约定该小节为可选（仅当执行了相关 align-* 时出现）。

---

### 选项 C：由某 align-* 技能扩展产出「检查点摘要」

- **做法**: 例如让 align-planning（或 align-backlog）在 Full 模式或特定触发下，多产出一段「per-milestone status + recommendations」摘要，可写进同一报告末尾或单独小节。
- **优点**: 单独跑 align-planning 时也能拿到检查点式摘要。
- **缺点**: 混合「对齐分析」与「治理门状态摘要」两种职责，技能边界变模糊；与「align-* 只做对比与建议」的约定易冲突。

---

### 选项 D：在契约中保留「策略检查点」形态，由编排或轻量步骤填充

- **做法**: 在 artifact-contract 或 ARTIFACT_NORMS 中保留 `strategy-checkpoint` 类型与路径约定（如 `docs/calibration/YYYY-MM-DD-strategy-checkpoint.md`），但不设独立技能；由 run-checkpoint 在聚合时**可选**写出该文件（例如在 milestone-closed / release-candidate 等触发下），内容为「按里程碑/目标的状态 + 建议」。
- **优点**: 保留按日期的快照能力，便于审计或对外汇报。
- **缺点**: 多一种产物与路径约定；run-checkpoint 需增加「何时写、写哪份」的规则。

---

## 4. 建议方向

- **首选**: **选项 B** — 不保留 run-strategy-checkpoint；由 run-checkpoint 的 cycle report 在执行了 align-planning（及可选 align-backlog）时，增加「Strategy / Milestone status」小节，综合出按里程碑/目标的状态与建议。这样 align-* 的「相关产物」仍是既有报告（planning-alignment、backlog-alignment），策略检查点**视图**作为 cognitive-loop 的一部分存在，不增加新技能与新文件类型。
- **若后续确有按日快照或对外单独报告需求**: 再考虑选项 D，在 run-checkpoint 中增加「可选写出 strategy-checkpoint 文件」的规则，并在 artifact 契约中保留该类型。

---

## 5. 后续动作（若采纳本决策）

1. **移除 run-strategy-checkpoint**: 删除技能目录；从 INDEX、scenario-map、manifest、AGENTS.md、相关决策与 proposed-strategy-skills 中移除引用。
2. **align-* 产物**: 保持现有 planning-alignment、backlog-alignment、architecture-compliance 报告不变；不要求 align-* 产出额外的「策略检查点」专用文件。
3. **run-checkpoint**: 在 SKILL 的 Phase 3（Aggregate Governance Report）中约定：当本周期执行了 align-planning（及可选的 align-backlog）时，报告须包含「Strategy / Milestone status」小节（按里程碑/目标的状态 + 建议）；从 related_skills 与说明中移除对 run-strategy-checkpoint 的引用。
4. **align-backlog**: related_skills 与 Handoff 中移除 run-strategy-checkpoint；里程碑/发布门场景改为「可先 align-backlog，结果由 run-checkpoint 聚合」。
5. **20260316-align-skills-replan**: 将「战略文档 ↔ 执行/backlog 一致性由 run-strategy-checkpoint 覆盖」改为「由 run-checkpoint 周期报告中的 Strategy/Milestone status 小节 + align-planning/align-backlog 报告共同覆盖；不再保留 run-strategy-checkpoint」。

---

## 6. 小结

| 问题 | 结论 |
| :--- | :--- |
| 是否保留 run-strategy-checkpoint？ | 不保留。 |
| align-* 是否要有「策略检查点」类**独立**产物？ | 不强制；建议不新增独立产物类型。 |
| 策略/里程碑状态视图从哪里来？ | 由 run-checkpoint 的 cognitive-loop 报告在聚合时综合 align-* 发现，以固定小节形式呈现。 |
