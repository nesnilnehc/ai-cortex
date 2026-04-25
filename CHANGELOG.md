# 变更日志

本文件记录本项目的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)，
版本遵循 [Semantic Versioning](https://semver.org/specs/v2.0.0.html)。

## [Unreleased]

### Changed（plan-next v9.0.0 — 移除 execute 参数，read-only 边界硬化，2026-04-25）

详见 [ADR 007](docs/architecture/adrs/007-remove-plan-next-execute-flag.md)。

- `skills/plan-next` v8.1.0 → **v9.0.0** —— frontmatter 移除 `execute` 字段（v8.1 的 `execute=true` 是 vaporware：文档只一句"按推荐顺序串调下游"，无错误处理 / 重试 / 状态等执行引擎语义；与"导航不开车"的 read-only 定位冲突）
- 文档级声明：plan-next 永不执行下游，**read-only 是硬边界**而非可配置默认
- 自动化迭代改由三层正交原语组合：`plan-next`（诊断 read-only） + orchestrator（驱动，如 `auto-iterate`）+ `loop`（调度）
- `auto-iterate` 登记为后续工作项，不在本次实现

### Migration（plan-next v8 → v9）

- 调用方传 `execute: true/false` 字段在 v9 被忽略（不报错，无副作用）——v8.1 默认行为 = v9 唯一行为
- 想 autopilot 的项目等 `auto-iterate` 技能落地；当前可用 `/loop /plan-next 30m` 做持续监控（人工反应模式）

### Changed（v9.0.0 — 彻底删除 linking_mode + 统一三类路径，2026-04-25）

**第二次 MAJOR**：`manifest.version` 4.0.0 → 5.0.0；`spec_version` 4.0.0 → 5.0.0。详见 [ADR 006](docs/architecture/adrs/006-delete-linking-mode-and-unify-artifact-paths.md)。

**动机**：v8.0 的"软废弃"策略留下 35+ 处 linking_mode 残留引用和一个 `specs/linking-modes.md` 文件——让新加入者仍需理解这个已经不存在的概念；同时 analyze-requirements / design-solution / breakdown-tasks 三类产出路径不统一（父目录层级 / 命名后缀 / 日期前缀三类差异），抵消了"slug 贯通"的愿景。

**删除**（除 ADR / CHANGELOG 历史外的所有 linking_mode 引用）：

- `specs/linking-modes.md` 整个文件删除
- `manifest.json` 的 `LINKING_MODES_SPEC_V1` 注册条目删除
- `specs/INDEX.md` Linking Modes 行删除
- `specs/terminology.md` §6 Linking Mode 入口删除
- `specs/artifact-norms-schema.md` §6 "链接模式字段（已废弃）" 整节删除
- `specs/artifact-contract.md` §8.4 中 v7 残留场景描述清理；§8.6 错误表中 3 行 linking_mode 错误场景删除并合并为通用 `{parent_slug}` 缺失场景
- 所有技能 SKILL.md / agent.yaml / README.md 里"v8.0 linking_mode 已废弃 / 不涉及 linking_mode 分支" 注释删除

**统一路径**（canonical 改为 `docs/<type>/{slug}.md`）：

- `analyze-requirements` v2.0 → **v3.0**：`docs/requirements-planning/{topic}.md` → `docs/requirements/{slug}.md`
- `design-solution` v2.0 → **v3.0**：`docs/design-decisions/YYYY-MM-DD-{topic}.md` → `docs/designs/{slug}.md`
- `breakdown-tasks` v2.0 → **v3.0**：`docs/process-management/tasks/YYYY-MM-DD-{topic}.md` → `docs/tasks/{slug}.md`
- `specs/artifact-contract.md` v4.0 → **v5.0**：§2 制品类型表与 §附录 A 机器可读 schema 同步更新
- `specs/artifact-norms-schema.md` v2.0 → **v3.0**：示例更新；§6 删除

**保留**：

- ADR 003 / 004 / 005 / 006：linking_mode 演化历程的决策记录
- CHANGELOG v7.0 / v8.0 / v9.0 条目：变更历史
- Stage 0 Norms Resolution 机制：所有产出技能保留，仅 canonical 默认值变化
- `upstream_ref` 可选输入 + `parent:` frontmatter emit：链接锚点技能保留
- `align-work-item-manifest` v1.0.0：保留为 manifest 风格项目的可选审计工具；不依赖任何 mode 字段
- backlog-item / adr / doc-assessment 三类路径：各自领域惯例保留，不纳入统一

### Migration Notes（v8.0 → v9.0.0）

项目仓库迁移二选一：

1. **推荐**：`git mv` 旧文件到新路径（去日期前缀）：
   ```
   docs/requirements-planning/*.md        → docs/requirements/*.md
   docs/design-decisions/YYYY-MM-DD-*.md  → docs/designs/*.md
   docs/process-management/tasks/YYYY-MM-DD-*.md → docs/tasks/*.md
   ```

2. **保留旧路径**：在 `docs/ARTIFACT_NORMS.md` 显式声明覆盖：
   ```yaml
   artifact_types:
     requirements:
       path_patterns: ["docs/requirements-planning/{topic}.md"]
     design:
       path_patterns: ["docs/design-decisions/YYYY-MM-DD-{topic}.md"]
     tasks:
       path_patterns: ["docs/process-management/tasks/YYYY-MM-DD-{topic}.md"]
   ```

若曾在 `ARTIFACT_NORMS.md` 声明过 `linking_mode` 字段 → 直接删除该字段（路径覆盖 + `upstream_ref` 输入 + manifest 物理文件三机制替代）。

**回滚锚点**：`v8.0-lts` tag（commit 11d9ea1）；`v7.0-lts` tag；`v6.3-lts` tag。

### Changed（v8.0.0 — 回撤 linking_mode 枚举，2026-04-25）

**MAJOR 回撤**：`manifest.version` 3.0.0 → 4.0.0；`manifest.spec_version` 3.0.0 → 4.0.0。详见 [ADR 005](docs/architecture/adrs/005-retract-linking-mode-enum.md)。

**动机**：v7.0.0 发布次日发现 `linking_mode` 枚举字段属过度工程——与业界实践（Cursor / Cline / Aider / Copilot 等主流代理系统均无同类设计）相悖；6 种模式都能用 `path_pattern` 覆盖 + `upstream_ref` 输入 + manifest 物理文件检测三个正交机制解决，枚举是冗余抽象层；greenfield 用户获得负价值（被迫盲选 6 选项）。

**回撤内容**：

- `specs/artifact-norms-schema.md` **v1.2 → v2.0** — 废弃 §6 `linking_mode` 字段；提供迁移指南
- `specs/linking-modes.md` **v1.0 → v2.0** — 降级为描述性 taxonomy 参考文档；§3–§5 标注"退休"；不再作为运行时配置对象
- `specs/artifact-contract.md` **v3.0 → v4.0** — §8.4 Linking-mode 输出真值表简化为"按 resolved path_pattern + 可选 parent: frontmatter"；§8.1–§8.3 / §8.5–§8.7 全部保留（path_pattern 覆盖机制有价值）
- `skills/discover-docs-norms` **v3.0 → v4.0** — 移除 Stage 2b 链接模式识别；回归路径/命名/frontmatter/生命周期审计职责
- `skills/define-docs-norms` **v2.0 → v3.0** — 移除 Stage 1b 链接模式选择 UI；回归"固化已批准提案"抄写员职责
- `skills/plan-next` **v7.0 → v8.0** — Step 2.5 改为按物理信号扫描（resolved path_pattern glob + 可选 parent: 反向索引 + 可选 manifest 文件检测）；移除 `linking_mode` 字段读取、移除"先识别模式"前置闸门；Step 0 `norms_proposal_path` frontmatter 输入字段废弃

**保留**（v7.0 的有价值部分）：

- `specs/artifact-contract.md §8` 的 path_pattern 运行时覆盖机制（§8.2 发现顺序 / §8.3 占位符语法 / §8.5 合并 / §8.6 错误 / §8.7 校验）
- 所有产出技能的 Stage 0 Norms Resolution 步骤（v7.0 已加，v8.0 不变）
- 链接锚点技能（analyze-requirements / design-solution / breakdown-tasks / capture-work-items / bootstrap-docs）的 `upstream_ref` 可选输入字段
- `align-work-item-manifest` v1.0.0 新技能——重新定位为 manifest 风格项目的可选审计工具（不依赖 linking_mode 字段，靠物理文件检测）

**项目迁移指南**（原依赖 v7.0 linking_mode 字段的项目）：

| 原 linking_mode 值 | v8.0 迁移做法 |
|---|---|
| `slug` / `none` | 什么都不用改——AI Cortex 默认即 slug 约定 |
| `colocation` | 删除 `linking_mode` 字段；在 `artifact_types` 下覆盖各类型 `path_pattern` 为 `work/{topic}/<type>.md` |
| `parent-pointer` | 删除 `linking_mode` 字段；调用下游技能时传 `upstream_ref`；技能自动 emit `parent:` frontmatter |
| `manifest` | 删除 `linking_mode` 字段；保留清单文件；`plan-next` / `align-work-item-manifest` 通过物理存在性检测消费 |
| `mixed` | 删除 `linking_mode` 字段；每种正交机制独立声明 |

**回滚锚点**：`v6.3-lts` tag（v7 前状态）；v7.0 状态在 git 历史中以 commit `8a49da6` 定位

### Added（v7.0.0 — 规范驱动制品架构闭环，2026-04-24）

**重大版本升级**：`manifest.version` 2.0.0 → 3.0.0；`manifest.spec_version` 2.5.0 → 3.0.0。详见 [ADR 004](docs/architecture/adrs/004-norms-driven-artifact-architecture.md)。

**新增规范（Runtime Norms Resolution）**：

- `specs/artifact-contract.md` **v1.2 → v3.0** — 新增 **§8 Runtime Norms Resolution Protocol**：产出文档制品的技能**必须**实现 Stage 0 Norms Resolution 步骤；按 §8.2 发现顺序读项目规范；§8.3 占位符语法（`{slug}` / `{topic}` / `{parent_slug}` / `{YYYY-MM-DD}` 等）；§8.4 linking_mode 输出真值表；§8.5 部分覆盖合并；§8.6 错误处理；§8.7 校验钩子
- `specs/artifact-norms-schema.md` **v1.1 → v1.2** — `path_pattern` 明确从硬规则降级为默认值；占位符语法统一声明

**新增技能**：

- `align-work-item-manifest` **v1.0.0 (experimental, advisory-only)** — 检测 manifest 链接模式下清单文件与物理制品的漂移（悬挂引用 / 未登记 / 命名不符三类）；v1.0.0 只读不改；输出供 `plan-next` 作 G3 漂移源消费

**协同 MAJOR bump**（权威-选择-消费三角 + 5 链接锚点）：

- `discover-docs-norms` **v2.0 → v3.0** — 新增 Stage 2b 链接模式识别；按 `specs/linking-modes.md §3` 判据识别 6 枚举（slug / colocation / parent-pointer / manifest / mixed / none）；输出 `linking_mode` + confidence + evidence 到提案
- `define-docs-norms` **v1.0 → v2.0** — 新增 Stage 1b 链接模式选择 UI；推荐 + 5 备选呈现；`mixed` 模式追问主/辅；写 `linking_mode` 到 `ARTIFACT_NORMS.md`；支持 `linking_mode_override` non-interactive 调用
- `plan-next` **v6.3 → v7.0** — Step 0 Norms Resolution 算法实际执行（v6.3 声明的契约激活）；Step 2.5 显式 `Step 2.5.1-2.5.3` 模式选择与前置闸门路由；Step 2.7 S5 任务路径使用 cache-resolved path_pattern
- `analyze-requirements` **v1.1.1 → v2.0** — 加 Stage 0 + colocation/parent-pointer 分支 + `upstream_ref` 输入
- `design-solution` **v1.1.1 → v2.0** — 同上（design artifact_type）
- `breakdown-tasks` **v1.1 → v2.0** — 同上（tasks artifact_type）
- `capture-work-items` **v1.1 → v2.0** — 重构 "路径检测" 为 Stage 0；同上（backlog-item artifact_type）
- `bootstrap-docs` **v1.1.2 → v2.0** — 同上（adr artifact_type）

**协同 MINOR bump**（15 个固定路径治理技能加 Stage 0 路径覆盖，无 linking 分支）：

- `define-mission` v1.2 → v1.3；`define-vision` v1.2 → v1.3；`define-north-star` v1.1 → v1.2
- `define-strategic-pillars` v1.0 → v1.1；`design-strategic-goals` v1.1 → v1.2
- `define-roadmap` v3.1 → v3.2
- `align-planning` v1.3 → v1.4；`align-architecture` v1.2 → v1.3；`align-backlog` v1.0 → v1.1
- `assess-docs` v4.0 → v4.1；`assess-docs-ssot` v1.0 → v1.1；`assess-docs-code-alignment` v1.0 → v1.1；`assess-docs-links` v1.0 → v1.1
- `audit-docs` v2.0 → v2.1
- `tidy-repo` v1.2 → v1.3

**协同 PATCH bump**：

- `specs/terminology.md` v1.1 → v1.1.1（§7 Runtime Norms Resolution 入口）
- `specs/linking-modes.md` v1.0.0 → v1.0.1（交叉引用微调）

### Migration Notes（v6.3 → v7.0.0）

1. **消费 artifact-contract.md 的外部代码**：§8 是新增规范段，消费方需实现 Stage 0 或声明遵循 v2.x 行为——若 `spec_version` pin 在 2.x，升级到 3.0 前请读新 §8
2. **项目级 `ARTIFACT_NORMS.md`**：可选增加 `linking_mode` 字段（6 枚举之一）；未加不影响工作，但 plan-next v7 会触发前置闸门路由推荐运行 `discover-docs-norms` → `define-docs-norms`
3. **链接锚点技能调用方**：新增 `upstream_ref` 可选输入（parent-pointer / colocation 模式下必需）；`artifact_norms_path` 亦可选
4. **回滚锚点**：`v6.3-lts` git tag（commit 1ce60f3）为 pre-v7 完整状态；回滚建议 `git reset --hard v6.3-lts`（需确认回滚范围）

### Removed（2026-03-25）

- **删除自动生成脚本和单元测试**：移除 `scripts/generate-skills-index.mjs`、`scripts/generate-skillgraph.mjs`、`scripts/test/` 与 `skills/skillgraph.md`。`skills/INDEX.md` 改为手动维护；`npm run verify` 只进行验证而不自动生成。理由：INDEX.md 和 skillgraph.md 属于治理文档，手动维护使其保持精确性；单元测试冗余，因 `verify-registry.mjs` 本身已验证库函数正确性。

### Removed（2026-03-23）

- **intent-routing 完全废弃**：删除 `skills/intent-routing.json`、`skills/intent-routing.md` 与 `scripts/generate-intent-routing.mjs`。路由改由技能自描述（description、tags、triggers）完成，与 Agent Skills 规范及 gstack 等主流实践对齐。routing_rules 中通用规则已迁移至 `docs/guides/discovery-and-loading.md`；主动建议表保留于 `docs/guides/proactive-suggestions.md`。

### Changed（意图路由迁移 2026-03-21）

- **scenario-map → intent-routing**：`scenario-map.json`/`scenario-map.md` 更名为 `intent-routing.json`/`intent-routing.md`；每条意图增加 `intent` 字段（意图句）；`scenarios` 改 `intents`；脚本、规范、AGENTS.md、docs 引用已更新。
- `docs/designs/scenario-enumeration.md` 已删除；新建 `docs/process-management/backlog/intent-backlog.md` 为待实现意图表。

### Changed（治理）

- 校准输出现按 `docs/ARTIFACT_NORMS.md` 覆盖规范文件（doc-readiness、planning alignment、architecture compliance、cognitive loop）；仅在显式请求时生成快照。
- 更新 `assess-docs`、`align-planning`、`align-architecture`、`run-checkpoint`、`run-repair-loop` 的输出路径与版本，减少冗余报告制品。
- **run-checkpoint v1.2.0** — Phase 0.5 Planning Readiness Gate；preparation 流程含 discover-docs-norms、bootstrap-docs；readiness 缺失时以 Minimal Fill Plan 短路。
- **技能命名**（按 20260310-skill-naming-audit 优秀标准）：
  - `orchestrate-governance-loop` → `run-checkpoint`
  - `assess-documentation-readiness` → `assess-docs`
  - `bootstrap-project-documentation` → `bootstrap-docs`
  - `validate-document-artifacts` → `validate-doc-artifacts`（2026-03 并入 `assess-docs`）
  - 文档相关技能统一 `doc` 术语
- `specs/skill.md` v2.5.0 — 命名优先级规则：语义正确与规范性优先，口语化与易记次之

### Added（新增）

- `docs/ARTIFACT_NORMS.md` — 定义规范、非快照校准输出的项目制品规范
- `align-architecture` 技能 (v1.0.0) — 校验 ADR/设计 vs 代码实现；产出 Architecture Compliance Report

### Removed（移除）

- **validate-doc-artifacts** — 并入 **assess-docs** (v3.0.0)；单一报告现覆盖 artifact-norms 合规（路径、命名、front-matter）及层级 readiness + minimal fill plan
- 被规范 living 制品取代的一次性校准报告及已完成 backlog 项
- scenario-map.json 中的 Architecture Compliance 场景（short triggers：align architecture、architecture compliance、design vs code）

### Changed（对齐）

- `align-execution` (v1.0.0 → v1.1.0) — 瘦身为仅 planning 层；移除 Architecture 层与 Architecture Drift；design vs code 合规交 `align-architecture`
- `align-execution` → `align-planning` — 更名以明确 planning vs implementation 边界
- `run-checkpoint`（原 orchestrate-governance-loop）— 移除基于 trigger 的路由；统一序列（align-planning → assess-doc-readiness）+ 输出驱动的后续（align-architecture、run-repair-loop、design-solution、analyze-requirements）；trigger 仅作元数据
- `scripts/generate-skillgraph.mjs` — 将 align-architecture 加入 lifecycle chain 与 project governance loop；更新 governance loop 图以反映统一序列
- `skills/ASQM_AUDIT.md` — curate-skills：新增 align-architecture（Quality 20，validated）；更新 align-planning overlaps

### Changed（此前）

- **技能命名（spec verb-noun 合规）**：`documentation-readiness` → `assess-documentation-readiness`，`execution-alignment` → `align-execution`，`project-cognitive-loop` → `orchestrate-governance-loop`；manifest、scenario-map、scripts、docs 中所有引用已更新
- `scripts/generate-skillgraph.mjs` — 从 manifest 与 SKILL frontmatter 自动生成 `skills/skillgraph.md`；含全局概览
- `scripts/generate-scenario-map.mjs` — 从 `skills/scenario-map.json` 自动生成 `skills/scenario-map.md`
- `scripts/generate-skills-docs.mjs` — 包装脚本，运行上述两个生成器
- `skills/scenario-map.json` — scenario-to-skill 映射的规范来源（编辑此文件，非 scenario-map.md）

### Changed（自动化）

- `skills/skillgraph.md` — 现为自动生成；新增全局概览节（Code Review、Lifecycle、Onboarding、Governance、Standalone）
- `skills/scenario-map.md` — 现从 scenario-map.json 自动生成
- `scripts/verify-registry.mjs` — 校验前运行 generate-skills-docs；校验 scenario-map.json 技能引用
- `specs/skill.md` §9 — 文档生成说明；scenario-map 来源现为 scenario-map.json

## [2.1.0] - 2026-03-06

### Added（新增）

- `execution-alignment` 技能 — 任务后追溯、漂移检测与自上而下校准
- `docs/requirements-planning/` 与 `docs/architecture/` — 最小脚手架；指向 goals、roadmap、milestones
- `documentation-readiness` 技能 — 文档证据评估与 minimal-fill plan
- `project-cognitive-loop` 技能 — 编排治理周期（requirements、design、alignment、docs）
- `skills/scenario-map.md` — 基于任务的 scenario-to-skill 映射
- execution-alignment、documentation-readiness、project-cognitive-loop 的 agent.yaml 与 README
- `analyze-requirements` 技能 (v1.0.0) — 将模糊意图转化为已验证需求
- 7 个此前缺失技能的 I/O schema 契约
- 验证脚本增强：agent.yaml/README.md 存在性、related_skills 有效性、marketplace.json 同步
- CHANGELOG.md

### Changed（变更）

- `skillgraph.md` — 新增 project governance loop（analyze-requirements → design-solution → execution-alignment → documentation-readiness → project-cognitive-loop）
- `project-cognitive-loop` — 单一制品输出规则；Recommended Next Tasks（owner、scope、rationale）；被路由技能不再单独输出
- `analyze-requirements` 默认输出路径改为 `docs/requirements-planning/`（保持 `docs/requirements/` 兼容）
- Curate Skills 审计：ASQM_AUDIT §6.5、§7；run-repair-loop README 状态与分数规范化
- `run-automated-tests` 与 `run-repair-loop` 从 experimental (v0.1.0) 升级为 stable (v1.0.0)
- 升级 `schemas/skill-metadata.json` 至 spec v2.2.0（新增 `input_schema`/`output_schema` 字段）
- CI workflow 版本引用从 spec v2.0.0 更新为 v2.2.0

### Removed（移除）

- 过时的 `.agents/skills/commit-work/` 分叉（规范版本位于 `skills/commit-work/`）

### Fixed（修复）

- ASQM 审计覆盖缺口（7 个未打分技能）
- 路线图验收标准复选框现反映实际完成状态
- `skills/analyze-requirements/SKILL.md` 中 7 个 markdownlint 问题（MD032、MD040）

## [2.0.0] - 2026-03-02

### Added（新增）

- Spec v2.0.0 → v2.2.0：Core Objective 结构、I/O 契约协议、Scope Boundaries 灵活性
- `design-solution` 技能 — 设计验证的结构化对话
- `commit-work` 技能 (v2.0.0) — Conventional Commits 及提交前质量检查
- `review-typescript` 技能 — TypeScript/JavaScript 语言审查
- `review-react` 技能 — React 框架审查
- `onboard-repo` 编排器技能 — 端到端仓库接入
- `review-orm-usage` 技能 — ORM 使用模式审查
- `review-testing` 认知技能 — 测试存在性、覆盖率、质量
- Spec 验证基础设施（`verify-skill-structure.mjs`、`schemas/skill-metadata.json`）
- CI workflows（`pr-check.yml`、`audit.yml`）
- `CONTRIBUTING.md` 与 GitHub Issue 模板（bug、feature、new-skill）
- 演进路线图（`docs/designs/2026-03-02-ai-cortex-evolution-roadmap.md`）
- INDEX.md Stability 列（experimental / stable / mature）

### Changed（变更）

- 33 个技能迁移至 spec v2 结构（Core Objective、Success Criteria、Acceptance Test）
- `review-code` 编排器更新至 v2.6.0（cognitive 链中新增 review-testing）
- 正式化 Plugin 选择标准（ASQM >= 18、standalone value）

## [1.0.0] - 2026-02-14

### Added（新增）

- 26 个规范技能，涵盖 review、documentation、automation、meta-skill 类别
- `review-code` 编排器 (v2.5.0)，scope → language → framework → library → cognitive 链
- 15 个 review 技能：diff、codebase、dotnet、java、go、php、powershell、python、sql、vue、security、architecture、performance
- `curate-skills` — ASQM 打分与生命周期管理
- `discover-skills` — 技能发现与推荐
- `decontextualize-text` — 隐私保护文本泛化
- `generate-standard-readme` — 标准化 README 生成
- `generate-github-workflow` — GitHub Actions workflow 生成
- `refine-skill-design` — 技能审计与优化
- `generate-agent-entry` — AGENTS.md 编写
- `install-rules` — Cursor 与 Trae 规则安装
- `bootstrap-project-documentation` — 项目文档脚手架
- `run-automated-tests` 与 `run-repair-loop`（experimental）
- ASQM 审计框架，4 维度打分
- `manifest.json` 机器可读注册表
- `skills/INDEX.md` 规范目录与标签体系
- `skillgraph.md` 代码审查组合图
- Claude Plugin 集成（`.claude-plugin/marketplace.json`）
- 7 条编码标准、写作规范与工作流策略规则

### Changed（变更）

- 从 llm-skills 更名为 AI Cortex
- 采用 entry-file 驱动契约（`AGENTS.md`）
- 合并为仅技能目录（移除 commands 与过时 spec）

## [0.1.0] - 2026-01-23

### Added（新增）

- 含 decontextualization 技能的初始仓库
- README、LICENSE (MIT)、基本项目结构

[Unreleased]: https://github.com/nesnilnehc/ai-cortex/compare/v2.1.0...main
[2.1.0]: https://github.com/nesnilnehc/ai-cortex/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/nesnilnehc/ai-cortex/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/nesnilnehc/ai-cortex/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/nesnilnehc/ai-cortex/releases/tag/v0.1.0
