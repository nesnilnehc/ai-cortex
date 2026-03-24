# ASQM 审计 — AI Cortex 技能

**审计日期**：2026-03-24
**范围**：`skills/` 下全部 53 个技能
**打分**：ASQM strict（基于证据；agent_native = 5 仅当 SKILL.md 含有显式 output contract 时）

---

## 1. 按状态的生命周期

| Status | 数量 | 示例技能 |
| :--- | :---: | :--- |
| **Validated** | 15 | align-architecture, align-backlog, align-planning, ... (12 more) |
| **Experimental** | 38 | automate-repair, automate-tests, breakdown-tasks, ... (35 more) |
| **Archive_Candidate** | 0 | — |

**Lifecycle Rules:**
- **Validated** ↔ Quality ≥ 17 且 Gate A（agent_native ≥ 4）且 Gate B（stance ≥ 3）
- **Experimental** ↔ Quality ≥ 10
- **Archive_Candidate** ↔ 其他情况

---

## 2. 打分公式与门限

**Quality（线性）**：
`asqm_quality = agent_native + cognitive + composability + stance`

各维度评分范围：0–5 分，总分 0–20 分。

| 维度 | 范围 | 说明 |
| :--- | :---: | :--- |
| **agent_native** | 0–5 | Agent 消费；机器可读契约（仅 5 = 显式 output contract） |
| **cognitive** | 0–5 | 从用户转移至 Agent 的推理；步骤、检查清单、行为 |
| **composability** | 0–5 | 与其他技能组合的便利性；交接点、清晰 I/O、聚合 |
| **stance** | 0–5 | 设计完整性、spec 对齐；限制、自查、规范遵守 |

**Gate Rules:**
- **Gate A** (Agent-ready): agent_native ≥ 4
- **Gate B** (Design integrity): stance ≥ 3

---

## 3. 汇总表（分数与生命周期）

| Skill | agent_native | cognitive | composability | stance | quality | status |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| automate-tests | 4 | 4 | 3 | 5 | 16 | Experimental |
| conduct-retro | 5 | 3 | 3 | 5 | 16 | Experimental |
| curate-skills | 4 | 4 | 3 | 5 | 16 | Experimental |
| define-mission | 5 | 3 | 4 | 4 | 16 | Experimental |
| define-vision | 5 | 3 | 4 | 4 | 16 | Experimental |
| refine-skill-design | 4 | 4 | 3 | 5 | 16 | Experimental |
| automate-repair | 4 | 3 | 3 | 5 | 15 | Experimental |
| breakdown-tasks | 4 | 3 | 3 | 5 | 15 | Experimental |
| commit-work | 4 | 3 | 3 | 5 | 15 | Experimental |
| discover-docs-norms | 4 | 3 | 3 | 5 | 15 | Experimental |
| discover-skills | 4 | 3 | 3 | 5 | 15 | Experimental |
| generate-agent-entry | 4 | 3 | 3 | 5 | 15 | Experimental |
| generate-github-workflow | 4 | 3 | 3 | 5 | 15 | Experimental |
| generate-standard-readme | 4 | 3 | 3 | 5 | 15 | Experimental |
| investigate-root-cause | 4 | 3 | 3 | 5 | 15 | Experimental |
| review-architecture | 4 | 3 | 3 | 5 | 15 | Experimental |
| review-code | 4 | 3 | 3 | 5 | 15 | Experimental |
| review-codebase | 4 | 3 | 3 | 5 | 15 | Experimental |
| review-diff | 4 | 3 | 3 | 5 | 15 | Experimental |
| review-dotnet | 4 | 3 | 3 | 5 | 15 | Experimental |
| review-go | 4 | 3 | 3 | 5 | 15 | Experimental |
| review-java | 4 | 3 | 3 | 5 | 15 | Experimental |
| review-orm-usage | 4 | 3 | 3 | 5 | 15 | Experimental |
| review-performance | 4 | 3 | 3 | 5 | 15 | Experimental |
| review-php | 4 | 3 | 3 | 5 | 15 | Experimental |
| review-powershell | 4 | 3 | 3 | 5 | 15 | Experimental |
| review-python | 4 | 3 | 3 | 5 | 15 | Experimental |
| review-react | 4 | 3 | 3 | 5 | 15 | Experimental |
| review-requirements | 4 | 3 | 3 | 5 | 15 | Experimental |
| review-security | 4 | 3 | 3 | 5 | 15 | Experimental |
| review-sql | 4 | 3 | 3 | 5 | 15 | Experimental |
| review-testing | 4 | 3 | 3 | 5 | 15 | Experimental |
| review-typescript | 4 | 3 | 3 | 5 | 15 | Experimental |
| review-vue | 4 | 3 | 3 | 5 | 15 | Experimental |
| warn-destructive-commands | 4 | 4 | 2 | 5 | 15 | Experimental |
| decontextualize-text | 4 | 3 | 3 | 4 | 14 | Experimental |
| install-rules | 4 | 3 | 2 | 5 | 14 | Experimental |
| sync-release-docs | 4 | 3 | 2 | 5 | 14 | Experimental |
| audit-docs | 5 | 4 | 5 | 5 | 19 | Validated |
| align-architecture | 5 | 3 | 5 | 5 | 18 | Validated |
| align-planning | 5 | 3 | 5 | 5 | 18 | Validated |
| define-north-star | 5 | 4 | 4 | 5 | 18 | Validated |
| plan-next | 5 | 4 | 4 | 5 | 18 | Validated |
| tidy-repo | 5 | 4 | 4 | 5 | 18 | Validated |
| align-backlog | 5 | 3 | 4 | 5 | 17 | Validated |
| analyze-requirements | 5 | 3 | 4 | 5 | 17 | Validated |
| assess-docs | 5 | 3 | 4 | 5 | 17 | Validated |
| bootstrap-docs | 5 | 3 | 4 | 5 | 17 | Validated |
| capture-work-items | 5 | 3 | 4 | 5 | 17 | Validated |
| define-roadmap | 5 | 3 | 4 | 5 | 17 | Validated |
| define-strategic-pillars | 5 | 3 | 4 | 5 | 17 | Validated |
| design-solution | 5 | 3 | 4 | 5 | 17 | Validated |
| design-strategic-goals | 5 | 3 | 4 | 5 | 17 | Validated |

---

## 4. 维度分析

### Agent Native Distribution

- **Score 5**: 19 skills
- **Score 4**: 35 skills

### Cognitive Distribution

- **Score 4**: 8 skills
- **Score 3**: 46 skills

### Composability Distribution

- **Score 5**: 3 skills
- **Score 4**: 15 skills
- **Score 3**: 33 skills
- **Score 2**: 3 skills

---

## 5. 主要发现

### 5.1 Validated Skills (v2.0.0 Curation)

**Count**: 16 skills

All validated skills meet strict ASQM criteria:
- Quality ≥ 17 (Gate A: agent_native ≥ 4, Gate B: stance ≥ 3)
- Explicit output_schema in SKILL.md (YAML front matter with artifact_type and path_pattern)
- Clear scope boundaries and design integrity

- **align-architecture** (Q18): 5/3/5/5
- **align-backlog** (Q17): 5/3/4/5
- **align-planning** (Q18): 5/3/5/5
- **analyze-requirements** (Q17): 5/3/4/5
- **assess-docs** (Q17): 5/3/4/5
- **audit-docs** (Q19): 5/4/5/5
- **bootstrap-docs** (Q17): 5/3/4/5
- **capture-work-items** (Q17): 5/3/4/5
- **define-north-star** (Q18): 5/4/4/5
- **define-roadmap** (Q17): 5/3/4/5
- **define-strategic-pillars** (Q17): 5/3/4/5
- **design-solution** (Q17): 5/3/4/5
- **design-strategic-goals** (Q17): 5/3/4/5
- **plan-next** (Q18): 5/4/4/5
- **tidy-repo** (Q18): 5/4/4/5

### 5.2 Experimental Skills

**Count**: 38 skills

Experimental skills have quality ≥ 10 but do not meet validated threshold.
**Paths to validation:**

1. **Improve cognitive dimension** (currently 3): Add explicit step sequences, checklists, behavioral patterns
2. **Improve composability** (currently 3): Add handoff points, clearer I/O contracts, integration patterns
3. **Some lack output_schema**: Add explicit YAML front matter with artifact_type, path_pattern

- **automate-tests** (Q16): composability 3
- **conduct-retro** (Q16): cognitive 3 | composability 3
- **curate-skills** (Q16): composability 3
- **define-mission** (Q16): cognitive 3
- **define-vision** (Q16): cognitive 3
- **refine-skill-design** (Q16): composability 3
- **automate-repair** (Q15): cognitive 3 | composability 3
- **breakdown-tasks** (Q15): cognitive 3 | composability 3
- **commit-work** (Q15): cognitive 3 | composability 3
- **discover-docs-norms** (Q15): cognitive 3 | composability 3
- **discover-skills** (Q15): cognitive 3 | composability 3
- **generate-agent-entry** (Q15): cognitive 3 | composability 3
- **generate-github-workflow** (Q15): cognitive 3 | composability 3
- **generate-standard-readme** (Q15): cognitive 3 | composability 3
- **investigate-root-cause** (Q15): cognitive 3 | composability 3
- **review-architecture** (Q15): cognitive 3 | composability 3
- **review-code** (Q15): cognitive 3 | composability 3
- **review-codebase** (Q15): cognitive 3 | composability 3
- **review-diff** (Q15): cognitive 3 | composability 3
- **review-dotnet** (Q15): cognitive 3 | composability 3
- **review-go** (Q15): cognitive 3 | composability 3
- **review-java** (Q15): cognitive 3 | composability 3
- **review-orm-usage** (Q15): cognitive 3 | composability 3
- **review-performance** (Q15): cognitive 3 | composability 3
- **review-php** (Q15): cognitive 3 | composability 3
- **review-powershell** (Q15): cognitive 3 | composability 3
- **review-python** (Q15): cognitive 3 | composability 3
- **review-react** (Q15): cognitive 3 | composability 3
- **review-requirements** (Q15): cognitive 3 | composability 3
- **review-security** (Q15): cognitive 3 | composability 3
- **review-sql** (Q15): cognitive 3 | composability 3
- **review-testing** (Q15): cognitive 3 | composability 3
- **review-typescript** (Q15): cognitive 3 | composability 3
- **review-vue** (Q15): cognitive 3 | composability 3
- **warn-destructive-commands** (Q15): composability 2
- **decontextualize-text** (Q14): cognitive 3 | composability 3
- **install-rules** (Q14): cognitive 3 | composability 2
- **sync-release-docs** (Q14): cognitive 3 | composability 2

---

## 6. 建议与后续行动

### 6.1 立即行动（High Priority）

1. **Update Experimental Skills to Validated (Q16 → Q17+)**:
   - Review top 10 experimental skills (Q16, Q15) and enhance cognitive + composability
   - Add structured step sequences if missing (cognitive = 5)
   - Define handoff points and I/O contracts (composability = 4–5)

2. **audit-docs (v1.4.0)**:
   - Validated (Q19), highest quality orchestrator with full integration
   - SSOT detection integrated as internal logic (not separate skill)

### 6.2 中期改进（Next Iteration）

1. **Review all review-* skills**: Consolidate overlapping domain-specific review skills into atomic
   - Consider creating review-code as orchestrator with atomic sub-skills

2. **Add explicit market_position to all skills**: Differentiate between:
   - **differentiated**: Orchestrators (audit-docs, plan-next, review-code)
   - **commodity**: Atomic domain reviews (review-python, review-go, etc.)
   - **experimental**: Low-quality or niche skills

### 6.3 长期规划（Roadmap）

1. **Skill ecosystem maturity**:
   - Move all 38 experimental skills to validated by:
     - Improving cognitive dimension (structured steps + checklists)
     - Improving composability (handoff + aggregation)
   - Target: 54 validated, 0 experimental

2. **Overlap analysis & consolidation**:
   - Review-code vs review-diff, review-codebase → consolidate into orchestrator pattern
   - Define clear boundaries between orchestrator and atomic skills

3. **CI/CD integration**:
   - Add curate-skills to pre-merge workflow
   - Auto-update agent.yaml and ASQM_AUDIT.md on each skill change

---

## 7. 结论

**Skills evaluated**: 53
**Validated**: 15 (28%)
**Experimental**: 38 (72%)
**Archive_Candidate**: 0

**No changes needed** for validated skills; they meet all ASQM criteria.

**Actionable next steps**:
1. Use this report to prioritize experimental skill improvements
2. Schedule review sessions for top experimental skills (Q16, Q15)
3. Re-run curate-skills after each enhancement to track progress
4. Integrate into CI/CD: validate all PRs with ASQM framework

_由 curate-skills 技能生成（ASQM strict 打分，2026-03-24 19:17:42）。_