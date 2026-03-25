# 变更日志

本文件记录本项目的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)，
版本遵循 [Semantic Versioning](https://semver.org/specs/v2.0.0.html)。

## [Unreleased]

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
