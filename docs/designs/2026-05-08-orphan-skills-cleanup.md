---
artifact_type: design
created_by: nesnilnehc
lifecycle: snapshot
created_at: 2026-05-08
status: active
---

# 治理熵清理：孤儿技能触发路径与里程碑归档生命周期

**日期**：2026-05-08
**起源**：在 recloud-agentfabric 项目使用 `plan-next` 时发现 `tidy-repo` 等卫生型技能从未被主动调用；进一步排查 64 个技能后识别出 8-10 个孤儿（无自然触发路径）。本设计建立两条解决路径：将孤儿技能挂入 `plan-next` 的诊断流；建立完成里程碑的归档生命周期，避免历史文档累积污染 AI 当前判断。

---

## 一、背景与问题

### 现象

- `tidy-repo` 等技能存在但用户从未主动调用
- 完成的里程碑 tasks.md 长期保留在 active 路径（如 m1/m2/m3 在 M5 进行中时仍占据 milestones/）
- 已 superseded 的 ADR 缺乏状态闭环字段，AI 读到时按 accepted 处理

### 根因

**孤儿技能问题**：卫生型与漂移检测型技能解决慢性问题，无急性触发，没有"什么事件让我想起调用它"的清晰答案。

**历史文档膨胀问题**：完成的执行细节（M4 周度计划 200+ 行、m3 任务 100+ 行）混在 active 路径中，每次 plan-next 扫描都要消化大量历史，污染当前判断。

### 约束

- 不引入 cron / schedule（不现实）
- 不在 commit-work 挂卫生检查（commit 级触发太频繁，污染信号）
- 触发路径只能是：自然事件链调 / `plan-next` 路由器兜底 / 用户显式调用

---

## 二、5 项关键决策

| # | 决策 | 选择 |
|---|---|---|
| 1 | 归档目录命名 | `_archive/`（与 `_templates/` 风格一致） |
| 2 | 摘要文件命名 | `m3-summary.md`（小写 + 连字符 + 类型后缀） |
| 3 | W6 阶段 3 批量推广方式 | LLM 判断（refine-skill-design 触达时由 LLM 评估并补齐 chains_to / triggers_after，不写脚本） |
| 4 | plan-next 阈值 | 默认值，不暴露给用户覆盖（保持简单） |
| 5 | chains_to 触发方式 | 自动追加到 plan-next 输出的「也要留意」末尾，标签 `链调`；plan-next 仍只读，由用户/编排器决定执行 |

---

## 三、改动总览

| WS | 改动 | 类型 | 主要文件 | 阶段 |
|---|---|---|---|---|
| W1 | 新增 `archive-milestone` 技能 | 新增 | `skills/archive-milestone/` + `specs/artifact-contract.md` | 1 |
| W2 | 新增 Rule `workflow-document-lifecycle.md` | 新增 | `rules/` + `rules/INDEX.md` | 1 |
| W3 | `align-architecture` 加 ADR 状态闭环 | 修改 | `skills/align-architecture/SKILL.md` + agent.yaml | 1 |
| W4 | `audit-docs` 加未归档/孤儿检测 | 修改 | `skills/audit-docs/SKILL.md` + agent.yaml | 1 |
| W5 | `plan-next` 加漂移巡检 + 卫生巡检 + chains_to 自动展开 | 修改（核心） | `skills/plan-next/SKILL.md` + agent.yaml | 2 |
| W6 | SKILL.md frontmatter 加 `chains_to` / `triggers_after` | 机制 | `specs/skill.md` + 首批 5 个技能 + 后续 LLM 判断推广 | 2-3 |

---

## 四、各 Workstream 详细设计

### W1 · 新增 archive-milestone 技能

**契约**

```yaml
input:
  milestone_slug: string  # 例 "m3"
  apply: bool             # 默认 false（dry-run），需显式 --apply 才落盘
output:
  artifact_type: milestone-summary
  path_pattern: docs/process-management/milestones/_archive/{slug}-summary.md
  lifecycle: snapshot
side_effects (apply=true):
  - 新建 milestones/_archive/{slug}-summary.md
  - 移除 milestones/{slug}/ 整个目录
  - 折叠 roadmap.md 中对应阶段段落为 ≤ 3 行引用
  - 全仓 grep 旧 tasks.md 路径，重定向到 summary
acceptance_criteria:
  - summary 含：完成日期 / 关键交付物 / 遗留缺口（指向后续里程碑） / 关键 ADR 引用
  - roadmap.md 该阶段段落折叠为 ≤ 3 行
  - 全仓 grep 无悬空引用
  - dry-run 模式下输出"将要发生的变更"不修改任何文件
```

**成熟度判定**（满足任一即可归档；全失败则技能拒绝执行并报告原因）

- 距完成日期 ≥ 60 天
- 当前进行中里程碑索引 ≥ slug + 2（M5 进行中时 m3 满足，m4 不满足）
- tasks.md 行数 > 300 且全部任务 status=done

**新文件清单**

```
skills/archive-milestone/
  SKILL.md       # 行为契约 + 反模式 + 自检
  agent.yaml     # frontmatter（含 has_output_contract / acceptance_criteria）
  README.md      # 何时调用 + dry-run 示例 + apply 示例
```

**契约更新**

`specs/artifact-contract.md` 添加 `milestone-summary` artifact_type 定义，path_pattern 为 `docs/process-management/milestones/_archive/*-summary.md`。

---

### W2 · 新增 Rule workflow-document-lifecycle.md

**位置**：`rules/workflow-document-lifecycle.md`

**核心约束**（5 条）

1. **ADR 状态字段优先**：读 ADR 时先查 `status` 字段。`superseded` 视为背景参考，不作当前约束；多个 `accepted` 在同一决策维度结论冲突时，停下报告而非自行裁决
2. **\_archive 路径排除**：路径含 `_archive/` 的文件仅作溯源参考，不纳入 `plan-next` / `assess-docs` 等技能的扫描范围（除非显式 `include_archive=true`）
3. **路线图历史阶段**：roadmap.md 中 `状态=已完成` 的阶段，只读摘要行；详细执行段视为历史，不作当前规划上下文
4. **状态字段冲突处理**：发现 `status` 字段冲突（如 ADR=accepted 但被新 ADR 显式 supersedes）→ 停下报告，要求人工裁决
5. **lifecycle 字段强制**：任何技能产出新制品时必须设置 `lifecycle: snapshot|living`；归档转换会修改这个字段（snapshot 即归档候选）

**注册**：`rules/INDEX.md` 增加一行注册条目。

---

### W3 · 扩展 align-architecture：ADR 状态闭环

**新增 Constraint 节**（追加在现有约束之后）

```
ADR 状态完整性检查（v1.4 起）：

扫描范围：docs/adr/*.md（或项目实际 ADR 路径）

违规类型：
- V1: status=superseded 但缺 superseded_by 字段
- V2: superseded_by 指向不存在的 ADR
- V3: status=accepted 但被另一 ADR 显式声明 supersedes 当前 ADR（双向不一致）
- V4: 多个 status=accepted 的 ADR 在同一决策维度上结论冲突
      （启发式：标题主语相似 + 决策动词相反，由 LLM 判断，置信度 ≥0.7 才报）

报告输出：docs/calibration/architecture-compliance.md 增加「ADR 状态完整性」章节
```

**版本**：`1.3.0 → 1.4.0`，`agent.yaml` 同步。

---

### W4 · 扩展 audit-docs：未归档/孤儿检测

**新增 Constraint 节**

```
未归档完成里程碑检测（v2.2 起）：

扫描：docs/process-management/milestones/*/tasks.md（排除 _archive/）

违规判定：
- 全部任务 status=done 或 ✅
- 且满足 archive-milestone 成熟度任一条件

输出动作：报为治理违规，路由建议 /archive-milestone {slug}
```

**版本**：`2.1.0 → 2.2.0`。

---

### W5 · 扩展 plan-next：漂移巡检 + 卫生巡检 + chains_to 展开（核心改动）

#### 5.1 步骤 2 增加两个子步

##### 步骤 2.2 漂移巡检

```
对每层制品 P 与其声明对齐的目标 T：
  比较 P.updated_at 与 T 实际状态最近变更时间
  超 drift_staleness_days（默认 30）→ 路由对应技能

路由表：
  backlog 老化（last_rescored_at > backlog_rescore_days，默认 90）  → /prioritize-backlog
  路线图 vs backlog 漂移                                              → /align-backlog
  架构文档 vs 代码漂移                                                → /align-architecture
  工作项清单 vs 执行漂移                                              → /align-work-item-manifest
  文档 SSOT 漂移信号                                                  → /assess-docs-ssot
  文档与代码对齐漂移                                                  → /assess-docs-code-alignment
  文档链路腐烂信号                                                    → /assess-docs-links
```

##### 步骤 2.3 卫生巡检

```
检查项：
- 已完成里程碑未归档（满足 archive-milestone 成熟度）→ /archive-milestone {slug}
- ADR 状态闭环违规                                       → /align-architecture
- 仓库结构漂移（_templates 遗漏 / 命名违规）             → /tidy-repo
- 技能层 SKILL.md 改动（git diff 检测）                  → /curate-skills
- 文档治理审计积压（assess-docs 类报告 > 30 天未更新）   → /audit-docs
```

#### 5.2 步骤 3 分层调整

漂移与卫生项强制进入「也要留意」节，**不挤占主路由的「现在该做」前两位**（除非主路由空闲且 hygiene 优先级达到 P1）。

#### 5.3 chains_to 自动展开

主路由生成后，对每条推荐技能 X 读其 `chains_to` 列表，把 X.chains_to 中每项作为额外条目附在「也要留意」末尾，标签 `链调`，依据字段写明"来自 X.chains_to"。

#### 5.4 反模式更新

删除原约束「对 done 节点重复报告缺口」。改写为：「不在主路由报告 done 节点为缺口；卫生巡检对 done 节点的检查为例外」。

#### 5.5 阈值字段（agent.yaml input_schema.defaults）

```yaml
thresholds:
  drift_staleness_days: 30
  backlog_rescore_days: 90
  milestone_archive_age_days: 60
  milestone_archive_lookback: 2     # 当前 - N 之前的里程碑成熟可归档
  audit_docs_staleness_days: 30
```

按决策 #4，这些字段不暴露给用户覆盖；保留在 SKILL.md 作为常量记录。

**版本**：`12.0.0 → 13.0.0`（major bump，核心契约扩展）。

---

### W6 · SKILL.md 链调字段机制

#### 6.1 specs/skill.md 增加约定

```yaml
chains_to:           # 完成本技能后建议链调的技能（plan-next 自动展开为「链调」推荐）
  - skill_name
triggers_after:      # 哪些技能完成后自然链调本技能（反向索引，便于诊断）
  - skill_name
```

两字段均可选；为空则不展开。

#### 6.2 首批增补（W5 实施时立即需要）

| 技能 | chains_to | triggers_after |
|---|---|---|
| `prioritize-backlog` | `[promote-roadmap-items]` | — |
| `bootstrap-docs` | `[assess-docs]` | — |
| `archive-milestone` | — | `[plan-next]` |
| `curate-skills` | `[refine-skill-design]` | `[refine-skill-design]` |
| `sync-release-docs` | `[review-codebase, audit-docs]` | — |

#### 6.3 剩余 50+ 技能批量推广

**决策 #3**：不写脚本，由 LLM 判断。每次 `refine-skill-design` 触达某技能时，LLM 评估其语义关系并补齐 chains_to / triggers_after。本设计不规定时间表；自然衰减式覆盖。

---

## 五、实施顺序

```
阶段 1（基础能力，预计 1-2 天）
├─ W2 写 rule（最小改动，先定调）
├─ W1 archive-milestone 技能（独立可用，dry-run 优先）
├─ W3 align-architecture 扩展
└─ W4 audit-docs 扩展

阶段 2（自动化路径，预计 2-3 天）
├─ W6 specs/skill.md 字段定义 + 首批 5 个技能补齐
└─ W5 plan-next 漂移巡检 + 卫生巡检 + chains_to 展开

阶段 3（长期机制，异步进行）
└─ W6 剩余 50+ 技能 chains_to / triggers_after 由 LLM 在 refine-skill-design 触达时增补
```

**关键依赖**：W5 依赖 W1（archive-milestone 必须存在才能被路由）、W3/W4（plan-next 路由的下游技能要支持新检查）、W6 首批（chains_to 数据要在）。

---

## 六、验收标准

每个 Workstream 独立可测：

| WS | 验收方法 | 通过标准 |
|---|---|---|
| W1 | 在 recloud-agentfabric 跑 `/archive-milestone m3 --apply=false`（dry-run） | 输出 summary 草稿 + roadmap 折叠预览 + 引用更新清单，无文件修改 |
| W2 | rule 注册到 INDEX.md；CLAUDE.md 加载后跑测试用例 | AI 在 superseded ADR 上正确判定为「背景参考不作约束」 |
| W3 | 在 recloud-agentfabric 跑 `/align-architecture` | 检出至少 1 个 ADR 状态违规（如有），输出到 architecture-compliance.md |
| W4 | 在 recloud-agentfabric 跑 `/audit-docs` | 检出 m3 未归档（若 m3 已超 60 天） |
| W5 | 在 recloud-agentfabric 跑 `/plan-next` | 「也要留意」自动出现 archive-milestone / audit-docs / align-architecture 路由；主路由 ≤3 条不被挤占 |
| W6 | grep 5 个技能 SKILL.md 含 `chains_to` 字段 | 字段格式一致；plan-next 能消费这些字段输出「链调」条目 |

**端到端验收**：在 recloud-agentfabric 跑一次 `/plan-next`，应该自动浮现 m3 归档建议（之前需手工识别），不再需要用户提示；同时主路由 T51 / T52 / T-SG5-002 不被挤占。

---

## 七、风险与边界

| 风险 | 缓解 |
|---|---|
| W5 改动过大，plan-next 输出爆炸（一屏放不下） | 漂移/卫生项强制进「也要留意」；主路由仍 ≤3 条；「也要留意」按优先级截断到 5 条 |
| archive-milestone 误删活跃文档 | 默认 dry-run；apply=true 必须显式传入；git 工作区不干净时拒绝执行 |
| chains_to 字段引发用户疑惑或自动级联错觉 | 标签 `链调` 明确语义；plan-next 仍只读不执行；rule W2 第 5 条说明 lifecycle 与 chains_to 无关 |
| 历史 ADR 大量缺 superseded_by 字段 | W3 首次跑会爆出大量违规——预期行为，分批修复，不阻塞合并 |
| LLM 判断 W6 字段（决策 #3）质量不稳 | 在 refine-skill-design 中加自检：chains_to 指向的技能必须存在 |

**边界声明**

- 本方案不引入 `schedule` / cron / hook
- `commit-work` 不挂任何卫生检查
- archive-milestone 默认 dry-run，需 `--apply` 显式确认才落盘
- plan-next 仍是只读路由器，chains_to 自动展开仅为输出层面，不触发任何下游执行

---

## 八、反模式

施工时避免以下做法：

- ❌ 把漂移/卫生检查放进 `commit-work`（污染 commit 级信号）
- ❌ 引入 cron / schedule 兜底（决策 #4 已排除）
- ❌ archive-milestone 自动执行不需 apply 标志（防误删）
- ❌ chains_to 字段自动级联调用下游技能（plan-next 必须保持只读）
- ❌ 在 plan-next 主路由位置塞漂移/卫生项（会挤掉真正的执行项）
- ❌ 写脚本批量推广 W6 字段（决策 #3 选择 LLM 判断）

---

## 九、后续追溯

施工时各 Workstream 的 commit 应在 PR 描述中引用本设计：

```
Refs: docs/designs/2026-05-08-orphan-skills-cleanup.md (W1)
```

W5 实施完成后，`skills/plan-next/SKILL.md` 的 `metadata.evolution.enhancements` 应追加一条引用本设计的条目。

完成所有 Workstream 后，本设计文档 `status: active → completed`，并在 CHANGELOG.md 提及。
