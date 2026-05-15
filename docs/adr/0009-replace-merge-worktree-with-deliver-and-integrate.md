---
artifact_type: adr
created_by: decision-record
lifecycle: snapshot
created_at: 2026-05-07
status: accepted
description: 把 merge-worktree 拆为 deliver-feature + integrate-worktrees
---

# ADR 0009：用 `deliver-feature` 与 `integrate-worktrees` 替代 `merge-worktree`

## 背景

旧技能 `merge-worktree` 强制要求 CWD 为主仓库根，且当前分支为 main——从 worktree 内调用即立即 halt。这导致最常见的"在 worktree 内开发完一个 feature 想交付"场景需要：cd 回主仓库 → 调技能 → 在批量列表中找到刚开发完的那一个 worktree → 合并 → 手动 cd 回原 worktree。多余步骤源自该技能定位为"从 main 批量集成"，未覆盖"从 worktree 单点交付"。

桌面文档 `~/Desktop/deliver-feature-redesign.md` 提议将技能改名为 `deliver-feature`、做"双上下文路由"、下挂两个内部实现（Layer 0/1a/1b/2 架构 + `visibility: internal` / `internal_implementations` 字段）。命名方向合理，但提议的实现层架构与项目现有四层治理模型（Skill / Spec / Protocol / Rule）以及 [`specs/skill.md`](../../../specs/skill.md) 的字段集冲突——其中 `visibility: internal` 与 `internal_implementations` 在规范中均不存在，引入将造成"软扩展"事实标准。

## 决策

**完全移除 `merge-worktree`，从零设计两个独立的 atomic skill：**

| 新技能 | 职责 | 调用上下文 |
|--------|------|-----------|
| [`deliver-feature`](../../../skills/deliver-feature/SKILL.md) | 单点交付：在 linked worktree 内将当前 feature 分支以 `--no-ff` 合并到 main 并 push，全程通过 `git -C <main-repo>` 驱动主仓库、CWD 不离开 worktree | 必须在 linked worktree 内、当前分支 ≠ main |
| [`integrate-worktrees`](../../../skills/integrate-worktrees/SKILL.md) | 批量集成：在主仓库 main 分支上扫描所有 linked worktree、用户多选后顺序 merge + push，统一清理成功项 | 必须在主仓库根、当前分支 = main |

**两者**：
- 不放在 orchestrator 之下（详见"替代方案 B"被拒原因）
- 共享部分 triggers（`finish feature`、`merge feature` 等），由 Claude agent 根据上下文自动选择具体调用哪一个，得到"一个语义指令两种上下文一致 UX"的效果
- 在彼此的 SKILL.md 中以 Handoff Point + Examples 互相 cross-reference，保证误调用时立刻给出正确指引

## 替代方案与被拒原因

### 替代方案 A：单一技能 + 内部 if-else 路由两条路径

**被拒原因**：两条路径的**用户意图、输入数（1 vs N）、输出形态、决策点、失败语义**全部不同——A 失败即结束，B 失败要让用户决定 abort/continue；A 没有"多选"步骤，B 必须有；A 输出单分支摘要，B 输出 per-worktree 表格。把两套相互独立的 task 塞进同一 SKILL.md 违反 [`specs/skill.md` §4](../../../specs/skill.md) 的"独立职责"原则，且让 Behavior 章节臃肿。

### 替代方案 B：Orchestrator + 2 个 atomic（`deliver-feature` 作 router，下挂 `*-single` 与 `*-batch`）

**被拒原因**：项目中真正的 orchestrator（如 [`review-code`](../../../skills/review-code/SKILL.md)）的核心价值是**串行调用多个 skill 然后聚合结果**（review-security + review-performance + review-architecture 合成一份报告）。本场景两条路径**互斥永不并行、永不聚合**，加 router skill 仅做 if-else，是 layer without value。"一个命令"的 UX 不需要 router skill——通过两个 atomic skill 共享 triggers + Claude 上下文路由即可达成。

### 替代方案 C：桌面文档的 Layer 0/1a/1b/2 + `visibility: internal` / `internal_implementations` 字段

**被拒原因**：
1. `visibility: internal` 与 `internal_implementations` 在 [`specs/skill.md`](../../../specs/skill.md) 中均不存在；引入需先经规范修订，否则将形成"事实标准"的软扩展
2. Layer 0/1a/1b/2 的层级体系无法对应项目的四层治理模型（Skill / Spec / Protocol / Rule）；Layer 2 "shared utilities" 在四层模型中应是 Protocol 而非"层"
3. 四层 + 内部技能引入的概念负担没有被相应的功能复杂度抵消（详见替代方案 B 的论证）

### 替代方案 D：原地扩展 `merge-worktree` 加 worktree 路径

**被拒原因**：扩展后的能力与"merge-worktree"这个偏实现细节的命名彻底脱节——技能名应反映用户意图（deliver / integrate）而非操作对象（worktree）。即使保留命名做扩展，也违反 ADR 0008 后确立的"职责单一、可验收"原则——一个技能两条上下文路径意味着两套 acceptance_criteria，与"原子技能"定位冲突（详见替代方案 A）。

## 迁移路径

迁移期间无并存机制，避免新旧字段同时出现造成认知负担：

1. **删除** `skills/merge-worktree/` 整目录
2. **新建**：
   - `skills/deliver-feature/`（SKILL.md + agent.yaml + README.md）
   - `skills/integrate-worktrees/`（SKILL.md + agent.yaml + README.md）
3. **manifest.json**：移除 `merge-worktree` 条目，新增上述两条
4. **skills/INDEX.md**：移除 `merge-worktree` 行，新增上述两行
5. **skills/SKILL_INVENTORY.md**：（历史）曾通过 `node scripts/generate-skill-inventory.mjs` 重新生成；相关脚本已移除
6. **ADR 0004 grep 正则表达式**：将 `merge-worktree` 替换为 `deliver-feature|integrate-worktrees`
7. （历史）当时以 `npm run verify` 作为收尾校验；本仓库已移除 npm 脚本

## 后果

**正面**：

- 两个独立技能各自有清晰的职责、acceptance_criteria、handoff——`deliver-feature` 的 acceptance 包括"CWD 全程未离开 worktree"，`integrate-worktrees` 的 acceptance 包括"批量预检后再 merge"，互不混淆
- `deliver-feature` 通过 `git -C <main-repo>` 解决了"交付时被迫离开 worktree"的核心痛点
- 命名以用户意图为中心（deliver / integrate），符合 [`specs/skill.md` §1](../../../specs/skill.md) 的 verb-noun 规范
- 与 ADR 0008 的"acceptance-criteria 决定 status"一致，每个技能的 status=validated 由各自可验证条件支撑

**负面 / 风险**：

- 破坏性变更：`manifest.json` 中的 `merge-worktree` 路径不存在了；外部对该技能名的引用需更新
- 两个技能维护两套 SKILL.md/agent.yaml/README.md，文件数从 3 增至 6——但每套文件描述的是真正独立的能力，与"无效拆分"不同
- 共享 triggers 依赖 Claude agent 正确识别 git 上下文做路由；若 agent 误判，需要技能内的 halt 守卫兜底——两个技能的 Examples 已分别覆盖该错误路径并给出指向对方的提示

## 不在此 ADR 范围内

- CLI 一键入口（`claude deliver-feature` 不区分上下文自动路由）：若需要，应以 slash command 形式实现，不在 skill 层增加 router
- 共享合并流程的 Protocol 化：`deliver-feature` 与 `integrate-worktrees` 共用的"pull → merge --no-ff → push"primitive 是 git 命令而非 skill 级逻辑，YAGNI 原则下暂不抽 Protocol；若未来出现第三个调用方再考虑
- Acceptance criteria 自动执行：与 ADR 0008 同范畴的后续工作

## 相关决策

- [ADR 0005 / 0006](./0005-retract-linking-mode-enum.md)：硬删除而非软保留的先例，本 ADR 沿用
- [ADR 0008](./0008-replace-asqm-with-acceptance-criteria.md)：用 acceptance_criteria 决定 status，本 ADR 的两个新技能各自填写 ≥1 条
