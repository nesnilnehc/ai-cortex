---
artifact_type: audit-docs
created_by: audit-docs
lifecycle: living
created_at: 2026-03-24
last_reviewed_at: 2026-03-26
status: active
---

# 文档治理审计报告（执行后）

**审计日期**：2026-03-26  
**范围**：`docs/` 全量 Markdown（47 个文件）  
**模式**：full（含 SSOT Phase 9）  
**执行说明**：已完成本轮“全部执行”（断链修复 + SSOT P1 冲突收敛）

---

## 执行结论

本轮结论：**91/100（EXCELLENT）**。

- 断链已从 14 降到 **0**（全部修复）。
- SSOT 冲突已从 `P1 + P2` 收敛到仅 **1 个 P2**。
- Frontmatter 覆盖率保持高位：**46/47（97.9%）**。
- 目录结构、Canonical Source、时间戳命名规则保持合规（0 违规）。

---

## 审计证据

```bash
npm run verify
python3 scripts/ssot_integrity_checker.py docs docs/calibration/ssot-phase9-audit.md
python3 scripts/test_ssot_checker.py
```

附加统计：
- Markdown 本地链接解析（剔除代码示例链接）→ 断链 `0`
- 文档图扫描 → 孤儿文档 `14`
- Frontmatter/元数据完整性扫描

---

## 集成评分

| 维度 | 分数 | 状态 | 说明 |
| :--- | :---: | :--- | :--- |
| 结构健康度 | 95 | Excellent | 根目录分类稳定，命名/时间戳规则 0 违规 |
| 规范准备度 | 86 | Good | frontmatter 覆盖高，但仍有元数据缺项 |
| SSOT 对齐度 | 93 | Excellent | P1 已清零，仅剩 1 个 P2 |
| 文档图健康度 | 90 | Excellent | 断链 0，孤儿文档 14（主要为校准与历史决策） |
| **综合分** | **91** | **EXCELLENT** | 进入维护模式 |

---

## 已完成项（本轮全部执行）

### 1. 断链修复（14/14）

已修复文件：
- `docs/architecture/README.md`
- `docs/designs/2026-03-02-ai-cortex-evolution-roadmap.md`
- `docs/guides/protocols-quickstart.md`
- `docs/guides/protocols-usage.md`
- `docs/process-management/backlog/2026-03-23-agents-md-refactor-plan.md`
- `docs/process-management/decisions/20260322-strategic-goals-milestones-framing.md`
- `docs/process-management/roadmap.md`
- `docs/references/README.md`

并补充缺失文档：
- `docs/guides/proactive-suggestions.md`（新增，消除引用空洞）

### 2. SSOT P1 冲突收敛

`docs/calibration/ssot-integrity-audit.md` 已改为摘要页，仅保留结论并指向 canonical：

- canonical：`docs/calibration/ssot-phase9-audit.md`

执行后 `ssot_phase9` 结果：
- 覆盖文档：47
- 冲突数：1（P2）
- P1：0

---

## 当前剩余问题（非阻塞）

### A. Frontmatter 元数据缺项（10）

- calibration 设计文档缺 `lifecycle`（3）
- protocols 指南缺 `created_by`（4）
- backlog/decision 文件缺 `created_at` 或 `created_by`（3）

### B. 孤儿文档（14）

集中在：
- `docs/calibration/`（历史分析与校准记录）
- `docs/process-management/decisions/`（部分历史 ADR）
- `docs/process-management/backlog/`（部分历史条目）

---

## 后续建议（维护模式）

1. 补齐 10 处 frontmatter 元数据缺项。  
2. 为 `calibration` 与 `decisions` 增加目录索引页，减少孤儿文档。  
3. 将 `scripts/ssot_integrity_checker.py` 的日期输出改为动态当天，避免报告日期漂移。  

---

## 成功标准复核

- [x] 规范已建立或验证  
- [x] 仓库结构已审计  
- [x] 文档已完成 full 评估（含 SSOT）  
- [x] 统一审计报告已更新  
- [x] 用户确认的“全部执行”动作已完成  
