# 计划：完全废弃 intent-routing

**日期**：2026-03-23  
**状态**：待执行  
**类型**：技术决策与执行计划

---

## 1. 背景与目标

### 1.1 问题

- 技能设计被引导强调意图→技能映射，偏离「提供可被发现、可执行的技能」的核心。
- 主流实践（Agent Skills 规范、Cursor、gstack）均采用技能自描述（description = what + when to use），无集中 intent-routing 配置。
- intent-routing 增加维护负担：每次新增/变更技能需同步 JSON，且与 skill prose 存在冗余。

### 1.2 目标

- 完全废弃 `skills/intent-routing.json` 与 `skills/intent-routing.md`。
- 从规范、脚本、文档、技能中移除所有 intent-routing 引用。
- 采用技能自描述 + 可选根技能/主动建议文档的方式，与主流实践对齐。

---

## 2. 影响范围

### 2.1 需删除的文件

| 文件 | 说明 |
| :--- | :--- |
| `skills/intent-routing.json` | 意图→技能映射源 |
| `skills/intent-routing.md` | 由 JSON 生成的文档 |
| `scripts/generate-intent-routing.mjs` | 生成 intent-routing.md 的脚本 |

### 2.2 需修改的脚本

| 文件 | 变更 |
| :--- | :--- |
| `scripts/generate-skills-docs.mjs` | 移除对 `generate-intent-routing.mjs` 的调用 |
| `scripts/verify-registry.mjs` | 移除 intent-routing.md / intent-routing.json 的校验逻辑；更新成功输出文案 |
| `scripts/skill-check.mjs` | 移除 Intent routing (short_triggers) 检查块 |

### 2.3 需修改的规范

| 文件 | 变更 |
| :--- | :--- |
| `spec/skill.md` | 移除 §2.2 Intent routing 条目；§2 可选调用字段中删除对 `short_triggers_zh` 与 intent-routing 的引用；§7 注册/检查清单中删除 intent-routing 相关要求 |
| `spec/registry-sync-contract.md` | 从范围与 3.4 节移除 intent-routing；从 generate-skills-docs 说明中移除 intent-routing |

### 2.4 需修改的文档

| 文件 | 变更 |
| :--- | :--- |
| `AGENTS.md` | 发现流程中删除对 intent-routing.json 的引用；参考表中删除 intent-routing 相关行 |
| `README.md` | 移除意图锚定段落；路由描述改为「按 description、tags、triggers 语义匹配」；PR 说明中删除 intent-routing.json |
| `docs/guides/discovery-and-loading.md` | 删除对 intent-routing 的引用；§4 路由规则改为「主技能优先、缺口时调用可选、多意图时升级 plan-next」等通用规则（从 routing_rules 提炼） |
| `docs/guides/proactive-suggestions.md` | 移除「基于 intent-routing.json 提炼」；表格保留为独立参考，改为「供 Agent 主动建议时参考」 |
| `docs/AUDIENCE_AND_SCOPE.md` | 从 §2 表格删除 intent-routing.json 行；从 §4 删除 intent-routing 澄清 |
| `docs/LANGUAGE_SCHEME.md` | 删除 intent-routing 相关表格行与说明 |

### 2.5 需修改的技能

| 技能 | 变更 |
| :--- | :--- |
| `skills/refine-skill-design/SKILL.md` | 使用场景与行为中删除「添加到 intent-routing.json」的指引 |
| `skills/commit-work/SKILL.md` | Self-Check、注册表同步相关条目中删除 intent-routing.json |

### 2.6 需修改的其他引用

| 文件 | 变更 |
| :--- | :--- |
| `skills/INDEX.md` | 删除「意图优先导航」段及对 intent-routing 的引用；§4 调度改为「按 description、tags、triggers 匹配；链式调用遵循 Handoff Point 与 Scope Boundaries」 |
| `skills/skillgraph.md` | 删除对 intent-routing.md 的引用（由 generate-skillgraph.mjs 生成，需改模板） |
| `scripts/generate-skillgraph.mjs` | 输出中删除对 intent-routing.md 的引用 |

### 2.7 历史/决策文档（仅注释或归档，不强制修改）

| 文件 | 说明 |
| :--- | :--- |
| `docs/process-management/decisions/20260316-run-strategy-checkpoint-*.md` | 提及 intent-routing，可加注「intent-routing 已废弃」 |
| `docs/process-management/decisions/20260316-align-skills-replan.md` | 同上 |
| `docs/process-management/backlog/2026-03-21-core-value-orchestration-routing-clarification.md` | 同上 |
| `CHANGELOG.md` | 本次变更增加一条记录 |

---

## 3. 需保留并迁移的内容

### 3.1 routing_rules（来自 intent-routing.json）

以下规则迁移至 `docs/guides/discovery-and-loading.md` §4：

- 仅当主技能输出暴露出缺口时再调用可选技能。
- 一周期内多意图活跃时升级至 plan-next。
- 使用制品移交（需求/设计/对齐/文档就绪报告）而非隐式上下文传递。

（「每个意图优先选用一个主技能」与 intent 绑定，废弃后不再适用。）

### 3.2 主动建议表

`docs/guides/proactive-suggestions.md` 中的阶段→技能表保留，改为独立参考文档，不再声明来源为 intent-routing.json。

---

## 4. 执行阶段

### Phase 0：迁移与准备

1. 在 `docs/guides/discovery-and-loading.md` §4 补充上述 routing_rules 三条（若尚未覆盖）。
2. 更新 `docs/guides/proactive-suggestions.md`，移除对 intent-routing.json 的引用。

### Phase 1：脚本与生成逻辑

1. 修改 `scripts/generate-skills-docs.mjs`，移除 `generate-intent-routing.mjs` 调用。
2. 修改 `scripts/verify-registry.mjs`，移除 intent-routing 校验块，更新输出文案。
3. 修改 `scripts/skill-check.mjs`，移除 Intent routing 检查。
4. 修改 `scripts/generate-skillgraph.mjs`，删除对 intent-routing.md 的引用。

### Phase 2：删除文件

1. 删除 `scripts/generate-intent-routing.mjs`。
2. 删除 `skills/intent-routing.json`。
3. 删除 `skills/intent-routing.md`。

### Phase 3：规范与文档

1. 更新 `spec/skill.md`（Intent routing、注册清单、short_triggers_zh 相关）。
2. 更新 `spec/registry-sync-contract.md`。
3. 更新 `AGENTS.md`、`README.md`。
4. 更新 `docs/AUDIENCE_AND_SCOPE.md`、`docs/LANGUAGE_SCHEME.md`。
5. 更新 `skills/INDEX.md`（脚本仅替换 §3 表格，§1–2 与 §4 为手写，直接编辑）。

### Phase 4：技能 prose

1. 更新 `skills/refine-skill-design/SKILL.md`。
2. 更新 `skills/commit-work/SKILL.md`。

### Phase 5：验证与收尾

1. 运行 `npm run verify`，确认通过。
2. 运行 `npm run skill:check`，确认无残留引用。
3. 更新 `CHANGELOG.md`。
4. 可选：在相关 ADR/backlog 中加注「intent-routing 已废弃」。

---

## 5. 依赖与顺序

- Phase 0 可与其他 Phase 并行准备。
- Phase 1 必须在 Phase 2 之前（否则 verify 会失败）。
- Phase 2 删除文件后，Phase 3、4 的修改才能完全生效。
- 建议顺序：0 → 1 → 2 → 3 → 4 → 5。

---

## 6. 回滚

若需回滚，从 git 恢复已删除文件，并还原脚本与文档修改。建议在单独分支执行，合并前完成全量验证。
