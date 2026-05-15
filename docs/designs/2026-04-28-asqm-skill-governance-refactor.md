---
artifact_type: design
created_by: design-doc
lifecycle: snapshot
created_at: 2026-04-28
status: active
---

# ASQM Skill Governance Refactor — 15 阶段实施计划

**日期**：2026-04-28
**锚点决策**：[ADR 0008](../adr/0008-replace-asqm-with-acceptance-criteria.md)

## 目标

完整移除 ASQM 评分体系，改用 `has_output_contract + acceptance_criteria` 决定 skill status，并连带优化 62 个 skill 的输出合约覆盖率。

## 关键事实

- 62 个 skill 中 **34 个**已有中文输出合约（`## 附录：输出合约`/合同/契约），**28 个**需补写
- 切换瞬间 28 个 skill 从 validated 降为 experimental（预期行为，非 bug）
- 上一会话已完成：24 个 agent.yaml 的 primary_use 净化 + auto-iterate stance 4→5

## 阶段总览

### 基础层（Phases 1–7）

| Phase | 目标 | 输出 | 依赖 |
|-------|------|------|------|
| 1 | 写入 ADR 0008（完全移除语义） | `docs/adr/0008-*.md` | — |
| 2 | curate-skills 自身改造 | `skills/curate-skills/{SKILL.md, agent.yaml, README.md}` | 1 |
| 3 | 62 个 skill agent.yaml 批量手术 | 62 文件删除 14 行 + 新增 acceptance_criteria | 2 |
| 4 | refine-skill-design 同步更新 | `skills/refine-skill-design/SKILL.md` | 1 |
| 5 | ASQM_AUDIT.md → SKILL_INVENTORY.md | 重命名 + 内容重写，删除所有分数列 | 3 |
| 6 | 规范文件更新 | `specs/skill.md`、`CLAUDE.md`、`skills/INDEX.md`、translate 脚本 | 3 |
| 7 | 既往设计文档历史注释 | `docs/designs/2026-03-*.md` 头部追加退役说明 | 1 |

依赖链：`1 → 2 → 3 → (4 ‖ 5) → 6 → 7`

### 扩展优化层（Phases 8–15）

| Phase | 目标 | 优先级 | 工作量 |
|-------|------|--------|--------|
| 8 | 33 个 README 删除 `## 评分 (ASQM)` 节 | 高 | 低（批量） |
| 9A | investigate-root-cause → validated（补 output contract + MUST 规则） | 高 | 中 |
| 9B | decontextualize-text → validated（硬规则升 stance 4→5） | 中 | 低 |
| 9C | discover-skills → validated（composability 3→4 + 与 install-rules 交接合约） | 中 | 中 |
| 10 | 16 个 review-* atomic skill 添加 YAML schema 格式 output contract | 高 | 低（模板化批量） |
| 11 | 10 个高 composability 治理技能补 output contract（plan-next、align-* 优先） | 高/中 | 中高 |
| 12 | 剩余 18 个 skill 补 output contract（strategy chain + procedural） | 中 | 中 |
| 13 | review-codebase + review-diff 添加区别说明，不合并 | 低 | 极低（并入 10） |
| 14 | plan-next SKILL.md 补标准 section 标题 | 中 | 低（并入 11） |
| 15 | SKILL_INVENTORY.md 添加维护协议 | 中 | 极低（并入 5） |

扩展层依赖：

```
1→2→3→(4‖5)→6→7
         │
         ├─ Phase 8  (需 Phase 5 先完成)
         ├─ Phase 9  (需 Phase 1)
         ├─ Phase 10 (独立，最高 ROI)
         ├─ Phase 11 (需 Phase 9C — plan-next 交接设计)
         │      └─ Phase 14 (并入 11)
         └─ Phase 12 (需 Phase 11)
```

## 阶段详细规格

### Phase 1 — ADR 008

落盘 ADR 008，作为后续所有阶段的理由锚点。完全移除语义（不保留 informational annotation）。被拒方案需明确记录，避免下次 curate-skills 运行覆盖回旧设计。

### Phase 2 — curate-skills 改造

**SKILL.md**：
- 删除打分逻辑、cognitive mode ceiling、validation_gates 推导规则
- 新增 has_output_contract 检测（grep `## Appendix: Output contract` 或 `## 附录：输出合约`）
- 新增 acceptance_criteria 字段存在性检查
- status 推导改为：`has_output_contract AND len(acceptance_criteria) >= 1`

**agent.yaml**：
- 删除自身的 scores / asqm_quality / validation_gates
- 添加 has_output_contract + acceptance_criteria（自举：curate-skills 自己先满足新规则）

**README.md**：
- 删除 `## 评分 (ASQM)` 节

### Phase 3 — 62 个 skill agent.yaml 批量手术

**每文件操作**：
- 删除 `scores:` block（4 行）
- 删除 `asqm_quality:` 行
- 删除 `validation_gates:` block（多行）
- 添加 `has_output_contract: true|false`（基于 SKILL.md grep 结果）
- 添加 `acceptance_criteria:` 占位（至少 1 条；缺失则保持空数组并标 experimental）

**风险**：28 个 has_output_contract:false → status 降为 experimental。预期行为，由 Phase 10–12 后续补齐。

**执行策略**：脚本化批量改，先 pilot 5 个验证 diff 格式，再全量。

### Phase 4 — refine-skill-design 同步

更新 SKILL.md 中所有 ASQM 引用：审计标准、模板示例、自检表。改为基于新规则。

### Phase 5 — ASQM_AUDIT.md → SKILL_INVENTORY.md

`git mv ASQM_AUDIT.md SKILL_INVENTORY.md`，重写：
- 删除分数列（agent_native / cognitive / composability / stance / asqm_quality）
- 新增列：has_output_contract / acceptance_criteria_count / status
- 添加维护协议节（Phase 15 内容并入）

### Phase 6 — 规范文件更新

- `specs/skill.md`：删除 ASQM 章节，添加 acceptance_criteria 规范
- `CLAUDE.md`：更新 skill 治理段落
- `skills/INDEX.md`：regenerate（去掉分数列）
- translate 脚本：移除 ASQM 字段处理

### Phase 7 — 历史设计文档注释

`docs/designs/2026-03-02-*.md` 和 `2026-03-06-*.md` 头部追加：
> 注：本文档中 ASQM 评分体系已于 2026-04-28 由 [ADR 0008](../adr/0008-replace-asqm-with-acceptance-criteria.md) 退役。

不重写正文（snapshot 类文档保持时间冻结）。

### Phase 8 — README 批量清理

33 个 README 含 `## 评分 (ASQM)` 节，sed/脚本批量删除该节及其内容。

### Phase 9 — 三个 experimental skill 升级

- **9A investigate-root-cause**：补 output contract（findings + remediation 字段）+ 在 SKILL.md 添加 MUST 级行为规则
- **9B decontextualize-text**：将 stance 描述改为可验证的硬规则（例：必须移除组织标识符列表）
- **9C discover-skills**：补与 install-rules 的交接合约（输出 → install-rules 的输入 schema）

### Phase 10 — review-* atomic skills 输出合约

16 个 review-* skill 共用 findings list 模板：

```yaml
findings:
  - location: <path:line>
    category: <enum>
    severity: <P0|P1|P2|P3>
    title: <string>
    description: <string>
    suggestion: <string>
```

模板化批量插入 SKILL.md 附录节。最高 ROI 阶段。

### Phase 11 — 治理技能输出合约

10 个高 composability 治理技能（plan-next、align-backlog、align-architecture、align-planning、align-work-item-manifest、prioritize-backlog、promote-roadmap-items、capture-work-items、audit-docs、assess-docs）补 output contract。

plan-next 的输出是其他治理技能的输入，优先级最高。Phase 14（plan-next SKILL.md 标准 section 标题）并入此阶段。

### Phase 12 — 剩余 18 个 skill

strategy chain（define-mission/vision/north-star、design-strategic-goals、define-strategic-pillars、define-roadmap）+ procedural skills 补输出合约。

### Phases 13–15

并入对应阶段，不独立执行。

## 验收

- 全部 62 个 skill agent.yaml 无 scores / asqm_quality / validation_gates 字段
- 全部 62 个 skill 有 acceptance_criteria（≥1 条）
- 全部 62 个 skill 有 has_output_contract: true（即对应 SKILL.md 含输出合约附录）
- （历史）当时以 `npm run verify` 作为验收；本仓库已移除 npm 校验脚本
- SKILL_INVENTORY.md 反映新规则下的 status 分布

## 不在范围内

- acceptance_criteria 自动执行框架
- skill 行为级别的 evals/golden set
- LLM 评估替代品（任何形式的"自动打分"都不在此重构范围内）
