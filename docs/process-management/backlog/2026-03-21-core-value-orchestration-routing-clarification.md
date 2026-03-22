---
artifact_type: backlog-item
created_by: capture-work-items
type: requirement
date: 2026-03-21
status: captured
source: user
trace_id:
---

# 核心价值澄清：编排、路由、统一输出与业务场景锚定

## 问题/背景 (Problem / Context)

围绕 AI Cortex 核心价值的讨论中，发现以下需澄清的问题：

1. **编排、路由、统一输出**：这些能力在 skills.sh、Cursor、Agent Factory 等生态中已存在类似实现。编排（orchestration）、路由（intent routing）、统一输出（structured output）并非独有。是否有更好的解决方案？本项目在这些维度的差异化定位是什么？

2. **Curated 资产库**： SkillAgent Collections、The Trust Registry、Awesome Agent Skills（630+）、Agent Skills Library（2622 from 48 sources）等均有 curated 集合。本项目的 curated 资产库与这些方案的差异何在？

3. **业务场景锚定**：核心价值可能在于「业务场景的锚定」而非规范、技术。当前 intent-routing 已定义 11 条意图（项目启动、需求评审、规划对齐、架构合规、文档分流、迭代编排、代码审查、交付收敛、技能治理、快速抓取、战略奠基等），但业务场景边界较模糊，需明确。

## 讨论结论摘要

### 编排 / 路由 / 统一输出

- **编排**：skills.sh 有 multi-agent-orchestration 等；AI Cortex 的差异化在于 code review 的**原子化分解 + 固定编排顺序 + 聚合**（review-code 编排 15+ 原子技能），而非「有编排」本身。
- **路由**：Cursor 有 intent routing；intent-routing 是**结构化**路由（primary/optional、short_triggers_zh），实现方式不同但非独有。
- **统一输出**：资产库内统一 findings 格式，使编排器可聚合；属设计选择，非独有能力。

### Curated 资产库

- 已有方案多按**类别**（DevOps、Security）或**平台**（Claude、Cursor）组织。
- 本项目可区分点：按**场景**（when_to_use、意图→技能）组织，而非仅按类别。

### 业务场景锚定（待定）

- intent-routing 的 11 条意图即当前定义的「业务场景」。
- 建议明确：业务域为「软件交付与项目治理」——从想法到 commit，含 alignment/compliance  checkpoint。

## 优化方案 (Optimization Recommendations)

### 方案 A：收敛核心价值到「场景锚定的 curated 资产库」

- **主张**：核心价值是「意图→路由→技能」的映射，intent-routing 为锚点。
- **行动**：在 README、mission、vision 中显式强调 intent-routing 与 11 条意图；弱化对「规范」「编排」的突出。
- **风险**：若其他 catalog 也做 scenario-based 组织，差异化减弱。

### 方案 B：收敛到「原子化 code review + 编排聚合」

- **主张**：差异化在于 review-code 的原子分解模式（scope → language → framework → cognitive）及聚合输出。
- **行动**：将 code review 域作为标杆案例，突出「可组合原子技能 + 编排器」模式。
- **风险**：局限于 code review，其他场景（需求、治理）的价值未显性化。

### 方案 C：编排/路由采用或对接更好的外部方案

- **主张**：编排、路由若有更成熟的框架（LangGraph、CrewAI 等），可评估对接或采用，而非自建。
- **行动**：调研 LangGraph、skills.sh orchestration skills 等；评估 AI Cortex 技能作为节点接入的可行性。
- **风险**：可能增加依赖与复杂度。

### 方案 D：业务场景边界明确化

- **主张**：将「业务场景」从模糊表述收敛到可枚举集合。
- **行动**：
  1. 定义业务域：软件交付 + 项目治理（含战略、需求、设计、实现、评审、交付、对齐）。
  2. 以 intent-routing 的 11 条意图为权威清单，在文档中显式列出。
  3. 新增场景时需满足「属于该业务域」且「与既有场景不重叠」。
- **风险**：过度收窄可能限制扩展。

## 验收标准 (Acceptance Criteria)

- [ ] 选定核心价值主张（A/B/C/D 或组合），并更新 README、mission、vision
- [ ] 若选方案 C：完成编排/路由外部方案调研，输出对比与建议
- [ ] 若选方案 D：在 docs 中明确业务域与 11 条意图的权威定义
- [ ] 使命/愿景表述与所选价值主张一致，避免过度宣称

## 备注 (Notes)

- 本工作项源自 2026-03-21 核心价值讨论会话。
- 相关文档：docs/project-overview/mission.md、vision.md、skills/intent-routing.json。
