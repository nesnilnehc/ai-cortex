# ASQM 审计 — AI Cortex 技能

**审计日期**：2026-03-23
**范围**：`skills/` 下全部 52 个技能
**打分**：ASQM strict（基于证据；agent_native = 5 仅当 SKILL.md 含有显式 output contract 时）

---

## 1. 按状态的生命周期

| Status | 数量 | 技能 |
| :--- | :--- | :--- |
| **validated** | 51 | 除 warn-destructive-commands 外全部（含 tidy-repo） |
| **experimental** | 1 | warn-destructive-commands |
| **archive_candidate** | 0 | — |

**validated** ↔ Quality ≥ 17 且 Gate A（agent_native ≥ 4）且 Gate B（stance ≥ 3）；**experimental** ↔ Quality ≥ 10；**archive_candidate** ↔ 否则。

---

## 2. 打分公式与门限

- **Quality（线性）**：`asqm_quality = agent_native + cognitive + composability + stance`（各 0–5，总分 0–20）。
- **Gate A**（agent readiness）：agent_native ≥ 4。
- **Gate B**（design integrity）：stance ≥ 3。
- **validated**：Quality ≥ **17** 且 Gate A 且 Gate B。
- **experimental**：Quality ≥ 10。
- **archive_candidate**：其他情况。

---

## 3. 维度检查清单（严格）

| 维度 | 含义 | 所用证据 |
| :--- | :--- | :--- |
| **agent_native** | Agent 消费；机器可读契约 | SKILL.md 中的 Appendix / Output contract；agent.yaml 结构 |
| **cognitive** | 从用户转移至 Agent 的推理 | Steps、checklists、Self-Check、Behavior |
| **composability** | 与其他技能组合的便利性 | Handoff、清晰 I/O、聚合格式 |
| **stance** | 设计完整性、spec 对齐 | Restrictions、Self-Check、spec/skill.md 对齐 |

**严格规则**：仅当 SKILL.md 包含**显式、机器可解析的 output contract**（如「Appendix: Output contract」或等效表/spec）时 agent_native = 5。仅 prose 的输出描述 → agent_native ≤ 4。

---

## 4. 汇总表（分数与生命周期）

| Skill | agent_native | cognitive | composability | stance | asqm_quality | status |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| align-architecture | 5 | 5 | 5 | 5 | 20 | validated |
| align-backlog | 5 | 4 | 4 | 5 | 18 | validated |
| align-planning | 5 | 5 | 5 | 5 | 20 | validated |
| analyze-requirements | 5 | 5 | 5 | 5 | 20 | validated |
| assess-docs | 5 | 4 | 5 | 5 | 19 | validated |
| automate-repair | 5 | 4 | 4 | 4 | 17 | validated |
| automate-tests | 5 | 4 | 4 | 4 | 17 | validated |
| bootstrap-docs | 5 | 4 | 4 | 5 | 18 | validated |
| breakdown-tasks | 5 | 4 | 5 | 4 | 18 | validated |
| capture-work-items | 5 | 4 | 4 | 5 | 18 | validated |
| commit-work | 5 | 5 | 5 | 5 | 20 | validated |
| conduct-retro | 4 | 4 | 4 | 5 | 17 | validated |
| curate-skills | 5 | 4 | 5 | 5 | 19 | validated |
| decontextualize-text | 5 | 4 | 4 | 4 | 17 | validated |
| define-mission | 5 | 5 | 5 | 5 | 20 | validated |
| define-north-star | 5 | 5 | 5 | 5 | 20 | validated |
| define-roadmap | 5 | 5 | 5 | 5 | 20 | validated |
| define-strategic-pillars | 5 | 5 | 5 | 5 | 20 | validated |
| define-vision | 5 | 5 | 5 | 5 | 20 | validated |
| design-solution | 5 | 5 | 4 | 5 | 19 | validated |
| design-strategic-goals | 5 | 5 | 5 | 5 | 20 | validated |
| discover-docs-norms | 5 | 4 | 4 | 5 | 18 | validated |
| discover-skills | 5 | 3 | 5 | 4 | 17 | validated |
| generate-agent-entry | 5 | 4 | 4 | 5 | 18 | validated |
| generate-github-workflow | 5 | 4 | 4 | 5 | 18 | validated |
| generate-standard-readme | 5 | 3 | 4 | 5 | 17 | validated |
| install-rules | 5 | 4 | 4 | 5 | 18 | validated |
| investigate-root-cause | 4 | 5 | 4 | 5 | 18 | validated |
| plan-next | 5 | 5 | 5 | 5 | 20 | validated |
| refine-skill-design | 5 | 5 | 5 | 5 | 20 | validated |
| review-architecture | 5 | 4 | 5 | 5 | 19 | validated |
| review-code | 5 | 5 | 5 | 5 | 20 | validated |
| review-codebase | 5 | 4 | 4 | 5 | 18 | validated |
| review-diff | 5 | 4 | 5 | 5 | 19 | validated |
| review-dotnet | 5 | 4 | 5 | 5 | 19 | validated |
| review-go | 5 | 4 | 5 | 5 | 19 | validated |
| review-java | 5 | 4 | 5 | 5 | 19 | validated |
| review-orm-usage | 5 | 4 | 5 | 5 | 19 | validated |
| review-performance | 5 | 4 | 5 | 5 | 19 | validated |
| review-php | 5 | 4 | 5 | 5 | 19 | validated |
| review-powershell | 5 | 4 | 5 | 5 | 19 | validated |
| review-python | 5 | 4 | 5 | 5 | 19 | validated |
| review-react | 5 | 4 | 5 | 5 | 19 | validated |
| review-requirements | 5 | 4 | 5 | 5 | 19 | validated |
| review-security | 5 | 4 | 5 | 5 | 19 | validated |
| review-sql | 5 | 4 | 5 | 5 | 19 | validated |
| review-testing | 5 | 4 | 5 | 5 | 19 | validated |
| review-typescript | 5 | 4 | 5 | 5 | 19 | validated |
| review-vue | 5 | 4 | 5 | 5 | 19 | validated |
| sync-release-docs | 4 | 4 | 4 | 5 | 17 | validated |
| tidy-repo | 5 | 4 | 4 | 5 | 18 | validated |
| warn-destructive-commands | 4 | 4 | 3 | 5 | 16 | experimental |

---

## 5. 重叠与生态

- **review-code** (orchestrator)：overlaps with review-diff, review-codebase, external code-review skills；**market_position**: differentiated。
- **原子 review 技能**（review-diff、review-codebase、review-* 等）：overlap with each other and review-code；**market_position**: commodity。
- **analyze-requirements**：overlaps with design-solution, capture-work-items；**market_position**: differentiated。
- **conduct-retro**：overlaps with align-planning, assess-docs；**market_position**: differentiated。
- **investigate-root-cause**：overlaps with automate-repair, review-diff, review-code；**market_position**: differentiated。
- **sync-release-docs**：overlaps with discover-docs-norms, assess-docs, bootstrap-docs；**market_position**: differentiated。
- **warn-destructive-commands**：overlaps_with empty；**market_position**: commodity。
- **automate-repair**：overlaps with review-code, automate-tests；**market_position**: commodity。
- **automate-tests**：overlaps with automate-repair；**market_position**: commodity。
- **plan-next**（orchestrator）：overlaps with align-planning, align-architecture, assess-docs, discover-docs-norms, bootstrap-docs, review-code；**market_position**: differentiated。
- **tidy-repo**：overlaps with assess-docs, review-codebase, align-planning；**market_position**: differentiated。
- 其余技能 overlaps 见各 `agent.yaml`。

所有重叠使用 **Git-repo 形式** `owner/repo:skill-name`（如 `nesnilnehc/ai-cortex:review-diff`）。

---

## 6. 发现

### 6.14 Curation 运行 (2026-03-23) — tidy-repo 纳入

1. **tidy-repo**（Quality 18）：output_schema 含 artifact_type、path_pattern、lifecycle；Input & Output 含完整 Markdown 模板与 Machine-Readable Summary → agent_native 5。7-phase 行为、Self-Check、Handoff 点 → cognitive 4、composability 4。Scope Boundaries、Constraints、spec 对齐 → stance 5。overlaps_with: assess-docs, review-codebase, align-planning。**validated**。
2. 此前 6.13 运行：conduct-retro、investigate-root-cause、sync-release-docs、warn-destructive-commands 均已创建 agent.yaml 与 README。
2. **conduct-retro**（Quality 17）：output_schema 含 artifact_type、path_pattern，但无显式 Appendix → agent_native 4。5-step 行为、Self-Check → cognitive 4。overlaps_with: align-planning, assess-docs。**validated**。
3. **investigate-root-cause**（Quality 18）：output 为 prose + Debug Report 格式，无 Appendix → agent_native 4。5-phase、Iron Law、模式表、3-strike 规则 → cognitive 5。overlaps_with: automate-repair, review-diff, review-code。**validated**。
4. **sync-release-docs**（Quality 17）：output 为 side-effect + doc health summary prose → agent_native 4。9-step 流程、Self-Check → cognitive 4。overlaps_with: discover-docs-norms, assess-docs, bootstrap-docs。**validated**。
5. **warn-destructive-commands**（Quality 16）：prose 输出、session-scoped、无 handoff → composability 3。Quality 16 < 17 → **experimental**。market_position: commodity。
6. **agent.yaml 命名规范化**：automate-repair（原 run-repair-loop）、automate-tests（原 run-automated-tests）、plan-next（原 run-checkpoint）— `name` 与目录名对齐。
7. **overlaps_with 规范化**：assess-docs、align-planning 中 run-checkpoint → plan-next；automate-repair 中 run-automated-tests → automate-tests。

---

## 7. 建议

1. **warn-destructive-commands**（experimental）：可考虑增加 Appendix: Output contract、提升 composability（如与 freeze 类技能 handoff），以达 validated。
2. **无紧急变更**：50 validated；1 experimental；无 archive 候选。
3. **重叠为设计使然**：原子 review 技能与 review-code 重叠；conduct-retro 与 align-planning、assess-docs 互补；sync-release-docs 与文档链技能形成发版后 handoff。
4. **tidy-repo**：已纳入审计；尚未进入 INDEX.md 与 manifest.json，按规范需单独注册流程。
5. **后续**：新增或大改技能后，运行 `curate-skills` 刷新 agent.yaml 与 ASQM_AUDIT.md。

---

*由 curate-skills 技能生成（ASQM strict 打分）。*
