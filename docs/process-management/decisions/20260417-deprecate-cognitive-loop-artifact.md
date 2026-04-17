---
artifact_type: adr
created_by: decision-record
lifecycle: snapshot
created_at: 2026-04-17
status: active
---

# 废弃 cognitive-loop artifact，plan-next 改对话直出

**状态**: 已接受 (Accepted)
**日期**: 2026-04-17
**范围**: 移除 `docs/calibration/cognitive-loop.md` 这一治理 artifact；调整 plan-next 输出契约从文件落盘改为对话直出；supersede ADR-20260316 中相关条目。

---

## 1. 背景

- `cognitive-loop` 在 `docs/ARTIFACT_NORMS.md` 注册为 living artifact，路径 `docs/calibration/cognitive-loop.md`。
- 历史上 ADR-20260316 把它指派为 `run-checkpoint` 的"单一周期聚合报告"，并明确以"不增加新技能与新文件类型"为设计原则。
- 现状盘点（2026-04-17）：
  - `run-checkpoint` skill 已不存在（既无 `skills/run-checkpoint/` 目录，也未注册于 manifest.json）。其能力被合并入 `plan-next` v3.0.0。
  - 当前 `cognitive-loop.md` 唯一生产者是 `plan-next`。
  - 现存样本 `docs/calibration/cognitive-loop.md` 停留在 2026-03-22，超过一个月未更新；frontmatter 标注的 `created_by: align-planning` 与实际生产者 `plan-next` 不符。
  - 多处文档（align-planning README、align-backlog SKILL、define-roadmap）仍引用 `run-checkpoint`，已成陈旧引用。

---

## 2. 问题

`cognitive-loop.md` 作为 artifact 同时承担两种相互冲突的角色：

1. **路由建议载体**（plan-next 当前实际用途）：使用者读完即据此调用下游技能，文件随后失效。
2. **审计制品**（ARTIFACT_NORMS 注册时的定位）：长期保留、跨周期可追溯。

事实证明角色 1 占主导（文件无人定期更新，价值主要在生成那一刻被消费）。把短寿路由建议固化为 living artifact 带来三类成本：

- **维护负担**：文件需符合 artifact 规范，落盘后需有人保证新鲜度
- **归属混乱**：原 ADR 假设的所有者已不存在，文件 frontmatter 与实际生产者不一致
- **认知开销**：使用者面对一份过期一个月的报告，需自行判断"是否还能信"

---

## 3. 决策

1. **废弃 `cognitive-loop` artifact 类型**：从 `docs/ARTIFACT_NORMS.md` 移除注册行。
2. **plan-next 改为对话直出**：路由建议直接以结构化对话内容呈现给使用者，不写文件。
   - SKILL.md frontmatter `output_schema.type` 由 `document-artifact` 改为 `chat`
   - Success Criterion #5（"周期报告写入文件"）替换为"路由建议在对话中以固定 3 节呈现：输入源清单、准备门结论、推荐路由任务"
3. **删除现存样本** `docs/calibration/cognitive-loop.md`（已过期且其声明的所有者错误）。
4. **本 ADR supersede ADR-20260316 中的对应条目**：原 ADR 的"由 run-checkpoint 的 cognitive-loop 报告承载策略/里程碑视图"假设失效。如未来确需周期聚合报告，应另立 ADR 重新设计。

---

## 4. 后果

**收益**：

- 减少一个治理 artifact 类型，治理产物清单更聚焦
- 消除 plan-next、run-checkpoint、align-planning 三方归属混乱
- plan-next 输出契约与其实际用途（一次性路由建议）一致

**代价**：

- 历史规划快照不再有专属文件，依赖 git log 与对话历史回溯
- 跨会话审计"上次怎么规划的"略不便（但实际场景中，下次 plan-next 会重新评估）

**可接受的风险**：

- 若未来出现"需要跨周期聚合的治理报告"需求，可单独立项设计新 artifact，不与本决策冲突

---

## 5. 实施清单

| # | 文件 | 动作 |
|---|---|---|
| 1 | `skills/plan-next/SKILL.md` | 改 frontmatter 输出契约；改 Success Criterion #5；改 Input/Output 章节；版本 3.0.0 → 4.0.0 |
| 2 | `skills/plan-next/README.md` | 第 8 行改为对话输出 |
| 3 | `skills/plan-next/agent.yaml` | 移除 `outputs` 中的文件路径；版本同步 4.0.0 |
| 4 | `docs/ARTIFACT_NORMS.md` | 删除 `cognitive-loop` 行 |
| 5 | `docs/calibration/cognitive-loop.md` | 删除文件 |
| 6 | `skills/align-planning/README.md` | `run-checkpoint` → `plan-next` |
| 7 | `skills/align-backlog/SKILL.md` | line 67 `run-checkpoint` → `plan-next`；line 88 删除 |
| 8 | `skills/define-roadmap/README.md` | `run-checkpoint` → `plan-next` |
| 9 | `skills/define-roadmap/SKILL.md` | `run-checkpoint` → `plan-next` |

---

## 6. 不做的事

- **不修改 ADR-20260316 原文**：保留历史决策痕迹，仅由本 ADR supersede。
- **不修改 `scripts/ssot_integrity_checker.py`**：脚本只做通用 `calibration` 目录归类，与本 artifact 无关。
- **不动 CHANGELOG.md / 历史审计快照**：历史记录保留原貌。
