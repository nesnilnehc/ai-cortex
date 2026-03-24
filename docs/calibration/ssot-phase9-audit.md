# SSOT 完整性审计 — Phase 9 详细报告

**审计日期**：2026-03-24
**覆盖文档**：41 个
**检出冲突**：1 个（P0/P1/P2）

---

## Part I: Intent Registry（意图注册表）

### architecture

| 文档 | artifact_type | ownership_role | granularity |
|:---|:---|:---|:---|
| architecture/README.md | architecture | architecture | index |

### architecture/adrs

| 文档 | artifact_type | ownership_role | granularity |
|:---|:---|:---|:---|
| architecture/adrs/001-io-contract-protocol.md | adr | architecture | point-in-time |

### calibration

| 文档 | artifact_type | ownership_role | granularity |
|:---|:---|:---|:---|
| calibration/assess-docs-extension.md | design | calibration-record | point-in-time |
| calibration/discover-docs-norms-refactor.md | design-decision | calibration-record | content |
| calibration/ASQM_AUDIT.md | audit-report | calibration-record | content |
| calibration/cognitive-loop.md | calibration-report | calibration-record | content |
| calibration/audit-docs.md | audit-docs | calibration-record | content |
| calibration/ssot-integrity-audit.md | audit-report | calibration-record | content |
| calibration/assess-docs-code-diff-scenario.md | design | calibration-record | point-in-time |
| calibration/doc-readiness.md | doc-readiness | calibration-record | content |

### designs

| 文档 | artifact_type | ownership_role | granularity |
|:---|:---|:---|:---|
| designs/2026-03-02-ai-cortex-evolution-roadmap.md | roadmap | architecture | execution-plan |
| designs/2026-03-06-promotion-and-iteration.md | design | architecture | point-in-time |

### guides

| 文档 | artifact_type | ownership_role | granularity |
|:---|:---|:---|:---|
| guides/discovery-and-loading.md | guide | reference | content |
| guides/project-config.md | guide | reference | content |

### process-management

| 文档 | artifact_type | ownership_role | granularity |
|:---|:---|:---|:---|
| process-management/promotion-iteration-tasks.md | execution-plan | execution-process | content |
| process-management/promotion-channel-checklist.md | execution-plan | execution-process | content |
| process-management/roadmap.md | roadmap | execution-planning | execution-plan |
| process-management/backlog.md | backlog | backlog-management | execution-plan |

### process-management/backlog

| 文档 | artifact_type | ownership_role | granularity |
|:---|:---|:---|:---|
| process-management/backlog/2026-03-06-add-prioritize-requirements-skill.md | backlog-item | backlog-management | execution-plan |
| process-management/backlog/2026-03-21-core-value-orchestration-routing-clarification.md | backlog-item | backlog-management | execution-plan |
| process-management/backlog/2026-03-23-agents-md-refactor-plan.md | backlog-item | backlog-management | execution-plan |
| process-management/backlog/2026-03-23-deprecate-intent-routing-plan.md | backlog-item | backlog-management | execution-plan |

### process-management/decisions

| 文档 | artifact_type | ownership_role | granularity |
|:---|:---|:---|:---|
| process-management/decisions/20260322-strategic-goals-milestones-framing.md | strategic-goals | decision-record | strategic-statement |
| process-management/decisions/20260316-execution-chain-requirements-design-tasks.md | adr | decision-record | point-in-time |
| process-management/decisions/20260322-merge-milestones-into-roadmap.md | roadmap | execution-planning | execution-plan |
| process-management/decisions/20260316-align-skills-replan.md | adr | decision-record | point-in-time |
| process-management/decisions/20260316-run-strategy-checkpoint-deprecate-and-align-artifacts.md | adr | decision-record | point-in-time |

### project-overview

| 文档 | artifact_type | ownership_role | granularity |
|:---|:---|:---|:---|
| project-overview/mission.md | mission | strategic | strategic-statement |
| project-overview/strategic-goals.md | strategic-goals | strategic | strategic-statement |
| project-overview/north-star.md | north-star | strategic | content |
| project-overview/README.md | index | strategic | index |
| project-overview/vision.md | vision | strategic | strategic-statement |

### references

| 文档 | artifact_type | ownership_role | granularity |
|:---|:---|:---|:---|
| references/readme-diagram-standards.md | reference | reference | content |
| references/README.md | reference | reference | index |
| references/ATTRIBUTIONS.md | reference | reference | content |
| references/LICENSE_POLICY.md | reference | reference | content |
| references/skill-install-guide.md | guide | reference | content |

### requirements-planning

| 文档 | artifact_type | ownership_role | granularity |
|:---|:---|:---|:---|
| requirements-planning/promotion-and-iteration.md | requirements | execution-planning | content |
| requirements-planning/README.md | requirements | execution-planning | index |

### root

| 文档 | artifact_type | ownership_role | granularity |
|:---|:---|:---|:---|
| LANGUAGE_SCHEME.md | governance | reference | content |
| ARTIFACT_NORMS.md | governance | reference | content |

## Part II: SSOT 冲突矩阵

| Doc A | Doc B | Intent重叠 | Doc-Level | Section-Level | 优先级 | Canonical Source | 修复动作 |
|:---|:---|:---:|:---:|:---:|:---:|:---|:---|
| process-management/promotion-iteration-tasks.md | requirements-planning/promotion-and-iteration.md | ✗ | 11.5% | 26.0% | **P2** | process-management/promotion-iteration-tasks.md | Convert to reference+link |

## Part III: 修复清单

### 【P2 - 优化项（可选修复）】

1. process-management/promotion-iteration-tasks.md ↔ requirements-planning/promotion-and-iteration.md
   - Section 相似度：26.0%
   - 推理：Different intent but moderate section similarity (26.0%)

## Part IV: 质量门禁

- [ ] ✓ 检出跨层重复（requirements-planning ↔ process-management）
- [ ] ✓ Section-level 分析强制执行
- [ ] ✓ 所有 P0/P1 都有明确的 canonical source
- [ ] ✓ 不存在目录剪枝导致的漏检

---

**报告生成时间**：2026-03-24
**执行模式**：full（启用完整 SSOT 审计）