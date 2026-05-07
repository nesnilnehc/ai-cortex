---
artifact_type: adr
created_by: decision-record
lifecycle: snapshot
created_at: 2026-04-24
status: active
---

# ADR 004：规范驱动的制品架构闭环（v7.0.0）

**状态**：Accepted
**日期**：2026-04-24
**上下文**：ADR 003 登记了 5 项 v7.x 后续跟进工作；用户确认本次一次性全做，并把 plan-next 代码侧的读取契约接上

## 背景

v6.3（ADR 002 + ADR 003）建立了 plan-next 的三步法、执行态覆盖、Now tier 作用域、与 `specs/linking-modes.md` 6 项固定链接模式枚举。但 v6.3 留下 **半截闭环**：

1. plan-next 声明了 `artifact_norms_path` / `norms_proposal_path` 作为 frontmatter 输入，**但 Behavior 步骤里没有命令式算法实际读**——死契约
2. `discover-docs-norms` 不探测链接模式；`define-docs-norms` 不接受 `linking_mode` 字段输入——链接模式枚举**无处落盘**
3. 13+ 产出文档制品的技能 `path_pattern` 硬编码在 frontmatter——项目规范只能修人读参考，运行时**不被消费**
4. `colocation` / `parent-pointer` 链接模式被标记为"v6.3 不支持"——因为需要下游技能支持动态路径
5. `manifest` 模式无维护机制——清单文件会漂移，v6.3 承诺只读报为 G3 但没有实现

这些半截状态本可以分散到多个 MINOR release 慢慢补，但选择**协同 MAJOR 一次闭环**——避免 plan-next v6.3 的契约无限期死代码。

## 决策

### 决策 1：`specs/artifact-contract.md` v3.0 新增 §8 Runtime Norms Resolution Protocol

新增规范性段落规定：产出文档制品的技能**必须**实现 **Stage 0: Norms Resolution** 步骤，按统一发现顺序（调用方 frontmatter → `.ai-cortex/artifact-norms.yaml` → `docs/ARTIFACT_NORMS.md` → 技能默认 → 契约 fallback）读取项目规范。新增占位符语法（`{slug}` / `{topic}` / `{parent_slug}` / `{YYYY-MM-DD}` 等）与 `linking_mode` 输出真值表（§8.4）。错误处理（§8.6）明确畸形 halt、缺失 fall-through、占位符缺数据追问。

### 决策 2：技能 frontmatter `path_pattern` 从**硬规则**降级为**默认值**

语法不变，语义变化：项目规范在 `ARTIFACT_NORMS.md` 声明的同 artifact_type 的 `path_pattern` 覆盖技能 frontmatter 默认。部分覆盖（§8.5）——未声明的 artifact_type 继承契约默认。

### 决策 3：13+ 产出技能（外加 2 个新/升级技能）落实 Stage 0

- **5 个链接锚点技能 MAJOR bump**（都加 Stage 0 + colocation/parent-pointer 分支 + `upstream_ref` 输入字段）：
  - `analyze-requirements` v1.1.1 → v2.0.0
  - `design-solution` v1.1.1 → v2.0.0
  - `breakdown-tasks` v1.1.0 → v2.0.0
  - `capture-work-items` v1.1.0 → v2.0.0
  - `bootstrap-docs` v1.1.2 → v2.0.0
- **15 个固定路径技能 MINOR bump**（加 Stage 0 路径覆盖，无 linking_mode 分支——governance 类制品位置稳定）：
  - `define-mission` / `define-vision` / `define-north-star` / `define-strategic-pillars` / `design-strategic-goals` / `define-roadmap`
  - `align-planning` / `align-architecture` / `align-backlog`
  - `assess-docs` / `assess-docs-ssot` / `assess-docs-code-alignment` / `assess-docs-links`
  - `audit-docs` / `tidy-repo`
- **权威 / 选择 / 消费三角**升级：
  - `discover-docs-norms` v2.0 → **v3.0**：新增 Stage 2b 链接模式识别（6 固定枚举）；输出 `linking_mode` + confidence + evidence 到提案
  - `define-docs-norms` v1.0 → **v2.0**：新增 Stage 1b 链接模式选择 UI；把用户选定的 `linking_mode` 写入 `ARTIFACT_NORMS.md`；支持 `linking_mode_override` non-interactive 调用
  - `plan-next` v6.3.0 → **v7.0.0**：Step 0 Norms Resolution 可执行算法实际加载项目规范到 cache；Step 2.5 显式 `Step 2.5.1-2.5.3` 算法选择模式并触发前置闸门；Step 2.7 S5 任务路径扫描使用 cache-resolved path

### 决策 4：manifest 模式维护机制——新技能 `align-work-item-manifest` v1.0.0（advisory-only）

采纳 ADR 003 讨论的**(b) 新技能**路径，拒绝 (a) 自动登记与 (c) 纯人工：

- **拒绝 (a) 自动登记**：会把 manifest 突变逻辑散到 5+ 个产出技能，manifest schema 修改面爆炸
- **拒绝 (c) 纯人工**：`plan-next` 已把纯人工维护作为 G3 漂移源报告，制度化人工 = 把问题正式化
- **采纳 (b) 新技能**：沿用 `align-backlog` / `align-planning` / `align-architecture` 现有模式；产出技能保持简洁；漂移由显式对齐 pass 处理；v1.0.0 首版**只读 advisory**（只报不改），降低破坏面；未来 v2.x 视证据决定是否升级为自动修复

新技能 I/O：读项目规范的 manifest 位置 → 对比清单声明 vs 物理文件 → 输出三类漂移（悬挂 / 未登记 / 命名不符）到 `docs/calibration/work-item-manifest-alignment.md`。

### 决策 5：协同 MAJOR release——所有技能 MAJOR bump 同一 commit

**拒绝分散 MINOR 迭代**：如果 5 个链接锚点技能、2 个权威技能、plan-next 分别独立升级，中间状态（例如 discover v3 已发、define 仍 v1）会让 plan-next v7.0 的 cache 拿不到链接模式字段，等于继续死代码。

**接受 MAJOR 面大**：CLAUDE.md 明确允许协同 MAJOR bump；CHANGELOG migration note + `manifest.spec_version 2.5.0 → 3.0.0` 作可见外部信号；`v6.3-lts` tag 已打为回滚保险。

### 决策 6：manifest 版本同步升级

- `manifest.json` project version **2.0.0 → 3.0.0**
- `manifest.json` spec_version **2.5.0 → 3.0.0**
- `specs/artifact-contract.md` **→ v3.0.0**
- `specs/artifact-norms-schema.md` **v1.1.0 → v1.2.0**（MINOR：占位符语法 + 默认/覆盖语义是加法）
- `specs/terminology.md` **v1.1.0 → v1.1.1**（PATCH：一行 §7 Runtime Norms Resolution 入口）
- `specs/linking-modes.md` **v1.0.0 → v1.0.1**（PATCH：若需要交叉引用微调）

## 替代方案（全部已拒绝）

1. **分散 MINOR 迭代**：拒。见决策 5。
2. **不让下游技能读规范，保持 path_pattern 硬编码**：拒。项目自定义路径（尤其 colocation）不生效；`ARTIFACT_NORMS.md` 退化为人读参考；plan-next 仍需启发式。
3. **`linking_mode` 做自由文本，不做枚举**：拒。机器不可消费；discover/define 无明确对象；plan-next 扫描策略模糊。（已在 ADR 003 会话中被用户纠正）
4. **每种 linking_mode 一个专门 SKILL**（如 `enable-slug-linking` / `enable-colocation` 等）：拒。会让每个产出技能的选择分支爆炸；不符合"Rules 层最高权威"原则。
5. **manifest 自动登记写入产出技能**：拒。见决策 4。
6. **colocation / parent-pointer 推迟到 v7.1 或 v8**：拒。本次已经协同 MAJOR，再延后会让部分用户感到"宣称支持但实际不能用"的挫败。

## 后果

### 正面

- **ARTIFACT_NORMS.md 真正成为 Rules 层最高权威**：运行时契约落地，符合 CLAUDE.md 的"Authority Chain: AGENTS.md > specs/ > protocols/ > rules/ > docs/"精神
- **colocation / parent-pointer 模式可用**：采用这两种模式的项目首次获得工具链支持
- **plan-next v6.3 死契约激活**：Step 0 算法实际运行，Self-Check 变成可执行断言
- **linking_mode 端到端贯通**：discover 识别 → define 选择 → plan-next 消费 → 下游技能按模式输出
- **manifest 漂移有专人管**：`align-work-item-manifest` 新技能填补 v6.3 留下的空白

### 负面

- **MAJOR release 面大**：spec_version / project version 同时 bump；22 个技能文件改动
- **用户迁移成本**：若外部消费者 pin 在 spec_version 2.x，必须显式升级读新 §8
- **部分回滚仍受限**：`manifest.spec_version 3.0.0` 一旦 bump 不可无感回滚；但 Stage 0 是加法，单技能可以独立回滚

### 中性

- **固定路径技能"免费"获得覆盖能力**：即使多数项目用不到路径覆盖，契约一致性是长期收益
- **`align-work-item-manifest` v1.0.0 advisory-only**：v2.x 视实际使用证据决定是否升级为自动修复，避免过早承诺

## 部分回滚策略

Stage 0 是**加法**（技能保留 frontmatter `path_pattern` 默认），任一技能可以单独回滚到 pre-v7 版本。

**不可逆**的是 `manifest.spec_version: 3.0.0` 与 `specs/artifact-contract.md §8`——所以 W11 manifest bump 在所有 retrofit skill 通过 verify 后**最后执行**，保证回滚窗口最大。

已打 `v6.3-lts` tag（参见 commit 1ce60f3）作为整体回滚锚点。

## 验证

```bash
# Registry 一致性
npm run verify

# Stage 0 覆盖检查（v7.0 后所有产出技能应含 "Stage 0" 或 "Norms Resolution"）
grep -rL "Stage 0\|Norms Resolution" skills/*/SKILL.md | \
  grep -vE "(review-|automate-|simplify|pptx|drawio|frontend-design|decontextualize-text|commit-work|deliver-feature|integrate-worktrees|curate-skills|refine-skill-design|install-rules|init|warn-destructive-commands|promote-roadmap-items|prioritize-backlog|breakdown-tasks|capture-work-items|analyze-requirements|design-solution|bootstrap-docs|generate-|discover-skills|find-skills|web-design-guidelines|investigate-root-cause|sync-release-docs|review|security-review|fewer-permission-prompts|schedule|loop|keybindings-help|update-config|claude-api|assess-docs)"
# 预期：零未覆盖产出技能

# spec_version
grep "spec_version" manifest.json
# 预期：3.0.0
```

## 参考

- ADR 002：plan-next v6.0 结构重构
- ADR 003：plan-next v6.3 执行态 + 链接模式识别（5 项 v7.x 工作登记）
- `specs/artifact-contract.md` v3.0 §8
- `specs/artifact-norms-schema.md` v1.2
- `specs/linking-modes.md` v1.0
- `skills/plan-next/SKILL.md` v7.0
- `skills/discover-docs-norms/SKILL.md` v3.0
- `skills/define-docs-norms/SKILL.md` v2.0
- `skills/align-work-item-manifest/SKILL.md` v1.0（本 ADR 诞生的新技能）
- `v6.3-lts` git tag（回滚锚点）
