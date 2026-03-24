---
artifact_type: roadmap
created_by: define-roadmap
lifecycle: living
created_at: 2026-03-24
status: active
---

# AI Cortex 演进路线图

**日期**：2026-03-02
**状态**：已批准
**批准人**：用户
**方法**：design-solution 技能（结构化对话）

## 目标

支撑 [4 个战略目标](../../project-overview/strategic-goals.md) 在工程基础设施、技能覆盖、编排、生态与规范成熟度四个维度的实现路径。

本文档关注**架构与分层**（Layer A-E），具体里程碑与阶段定义见 [roadmap.md](../roadmap.md)。

## 文档关系

- [strategic-goals.md](../../project-overview/strategic-goals.md)：4 个战略目标（权威定义）
- [roadmap.md](../roadmap.md)：里程碑与阶段计划（权威定义）
- 本文档：支撑路线图的架构与技术分层

## 背景

截至本分析时：

- 版本 2.0.0，单人维护（57 次提交），约 33 天活跃开发
- 28 个 canonical 技能，7 条规则，1 个 spec（skill.md v2.0.0）
- Spec v2.0.0 迁移刚完成：所有技能已具备 Core Objective 节
- 无 CI/CD；`verify-registry.mjs` 为唯一自动化检查（手动执行）
- 代码审查生态成熟：15/28 个技能与 review 相关，具备清晰组合图
- ASQM 审计上次运行 2026-02-27；2 个新技能（`design-solution`、`commit-work`）尚未审计
- 多渠道分发：skills.sh、SkillsMP、Claude Plugin（8/28 个技能已暴露）

## 架构

路线图按 5 层、4 个实施阶段组织：

```text
Layer A: Engineering Infrastructure (CI/CD, quality gates)
Layer B: Skill Coverage (languages, frameworks, libraries)
Layer C: Orchestration & Composition (orchestrators, skill chains)
Layer D: Ecosystem & Distribution (Plugin sync, community)
Layer E: Specification Evolution (lifecycle, testable spec)
```

阶段按依赖顺序排列：基础设施优先，随后能力、编排、生态。

## 组件

### A1. CI/CD 自动化

**推荐方案**：最小化 GitHub Actions + 自用 (Dogfooding)

- PR 触发：运行 `verify-registry.mjs` 校验 registry 同步
- main 分支合并：触发 ASQM 审计检查
- 使用项目自身的 `generate-github-workflow` 技能生成初始 workflow

| Alternative | Pros | Cons | Best for |
| :--- | :--- | :--- | :--- |
| **A: Minimal CI + Dogfood (recommended)** | Dogfoods own assets; low maintenance | Limited CI value for pure-Markdown project | Current stage |
| B: Extended CI + Spec compliance | Also solves E12 (spec testing) | Higher dev effort; script-spec sync burden | Governance-focused stage |
| C: CI + Release automation | Full release pipeline | Over-engineering for solo project | Community-ready stage |

### A2. 质量门自动化

**推荐方案**：CI 集成的增量审计

- 对新增/修改技能的结构检查：YAML 元数据完整性、Core Objective 存在性
- Registry 同步：INDEX 与 manifest 一致性
- ASQM 维度提示（非阻塞）：供人工确认的预估分数

| Alternative | Pros | Cons | Best for |
| :--- | :--- | :--- | :--- |
| **A: CI integration + incremental audit (recommended)** | Low friction; informational | ASQM scoring needs LLM; scripts can only check structure | Near-term |
| B: ASQM scoring scripted | Repeatable, objective | Cannot replace human judgment on semantic dimensions | Mid-term enhancement |

### B3. 语言审查扩展

**推荐方案**：TypeScript/JavaScript 优先，Rust 其次

按 Agent 编程场景频率的优先级矩阵：

| Language | Priority | Rationale |
| :--- | :--- | :--- |
| **TypeScript/JavaScript** | P0 | Agent 开发最常用语言；覆盖前端 + Node.js + Deno |
| **Rust** | P1 | 系统 + WASM；审查复杂度高（所有权、生命周期） |
| Ruby | P2 | Rails 生态仍活跃但小众 |
| Kotlin | P2 | Android + 服务端；与 Java review 重叠 |
| Swift | P3 | 仅 Apple 生态 |
| C/C++ | P3 | 审查规则极复杂；ROI 需评估 |

| Alternative | Pros | Cons | Best for |
| :--- | :--- | :--- | :--- |
| **A: TS/JS first + Rust next (recommended)** | Maximizes coverage value | Two skills to build | Broadest impact |
| B: Demand-driven | Avoids unused skills | Reactive; may miss market window | Resource-constrained |
| C: Full rollout | Wide coverage | Maintenance burden; quality may vary | Community with contributors |

### B4. 框架审查扩展

**推荐方案**：React 优先，随后 ASP.NET Core

| Framework | Priority | Rationale |
| :--- | :--- | :--- |
| **React** | P0 | 前端框架市占率最高 |
| **Next.js** | P1 | React 元框架；SSR/RSC 审查场景独特 |
| **ASP.NET Core** | P1 | 与 review-dotnet 形成完整 .NET 审查链 |
| Spring Boot | P2 | 与 review-java 互补 |
| Django/FastAPI | P2 | 与 review-python 互补 |
| Angular | P3 | 市占率下降 |

| Alternative | Pros | Cons | Best for |
| :--- | :--- | :--- | :--- |
| **A: React first + chain completion (recommended)** | Fills largest gap; synergy with TS/JS | Need to prioritize among many options | Maximum value |
| B: One framework per language skill | Complete orchestration chains | Some combinations may be low-frequency | Completeness-oriented |

### B5. 库级审查技能

**推荐方案**：按领域而非按具体库

- `review-orm-usage`：N+1 查询、连接泄漏、迁移安全性（覆盖 Prisma、EF、SQLAlchemy 等）
- `review-http-client-usage`：超时、重试、熔断模式
- `review-auth-library-usage`：token 处理、会话安全

| Alternative | Pros | Cons | Best for |
| :--- | :--- | :--- | :--- |
| B: Domain-based (recommended) | Not tied to specific libraries; broader applicability | Cannot provide library-specific best practices | Sustainable approach |
| A: Specific libraries (Prisma, EF) | Deep, actionable advice | Fast library iteration; high maintenance | High-traffic libraries |
| C: Skip for now | Zero maintenance | Misses deep review value | If cognitive skills suffice |

### C7. 多编排器模式

**推荐方案**：按序运行原子技能（无专用编排器）

流程：review-codebase（理解）→ review-architecture（识别问题）→ generate-standard-readme（文档化）→ generate-agent-entry（建立 Agent 契约）。原 `onboard-repo` 编排器已移除；按需使用上述原子技能。

| Alternative | Pros | Cons | Best for |
| :--- | :--- | :--- | :--- |
| **A: Atomic sequence (current)** | No extra skill to maintain; user picks steps | No single "onboard repo" trigger | Simplicity |
| B: quality-gate | Directly supports CI/CD | Overlaps with run-repair-loop | CI-focused |
| C: Protocol first, orchestrators later | One-time investment benefits all | May over-engineer | Spec-purist approach |

### C8. 技能链与工作流协议

**推荐方案**：轻量 I/O 契约

- 在 spec 中增加可选字段：`input_schema` 与 `output_schema`
- 定义标准中间 artifact 格式（Findings List、Document Artifact、Diagnostic Report）
- 编排器按 schema 自动匹配上下游

| Alternative | Pros | Cons | Best for |
| :--- | :--- | :--- | :--- |
| **A: I/O contracts in spec (recommended)** | Incremental; backward-compatible | Schema granularity needs careful design | Natural spec evolution |
| B: Event-driven model | Loose coupling; flexible | Too complex for pure-Markdown project | Platform with runtime |
| C: Explicit pipeline YAML | Declarative; easy to understand | New spec maintenance burden | Pipeline-centric workflows |

### D9. Claude Plugin 同步策略

**推荐方案**：定义入选标准 + CI 校验

- Plugin 入选标准：ASQM ≥ 18，非原子 review 技能，具备独立使用价值
- CI 检查：校验 `marketplace.json` 与 INDEX 一致性（同 verify-registry）

| Alternative | Pros | Cons | Best for |
| :--- | :--- | :--- | :--- |
| **A: Selection criteria + CI (recommended)** | Principled; auto-prevents staleness | Need to maintain criteria | Governed approach |
| B: Expose all 28 skills | Maximum coverage | Atomic review skills add noise | Simplicity |
| C: Tiered exposure (Core + Extended) | Good UX | Claude Plugin may not support tiers | If platform supports it |

### D10. 社区基础设施

**推荐方案**：渐进式社区就绪

- Phase 1（当前）：CONTRIBUTING.md（引用 spec/skill.md）、Issue 模板（Bug / Feature / New Skill Request）
- Phase 2（出现贡献者时）：含 Self-Check 清单的 PR 模板、CHANGELOG.md
- Phase 3（活跃社区）：CODEOWNERS、Discussion 模板

| Alternative | Pros | Cons | Best for |
| :--- | :--- | :--- | :--- |
| **A: Gradual (recommended)** | Invest as needed | Requires discipline to phase | Solo → small team transition |
| B: Full setup at once | Complete | Empty files if no community | Projects expecting contributors |
| C: Stay as-is | Zero maintenance | Barrier for external contributors | Purely solo project |

### E11. 技能版本生命周期策略

**推荐方案**：版本号与生命周期解耦 + 约定

- 版本号（SemVer）：反映内容成熟度；`0.x.x` = 不稳定 API，`1.0.0+` = 稳定契约
- ASQM 状态：反映质量分数（validated / experimental / archive_candidate）
- 在 INDEX.md 增加「Stability」列：experimental / stable / mature
- 约定：validated 技能在契约稳定时应从 `0.x.x` 升级至 `1.0.0`

| Alternative | Pros | Cons | Best for |
| :--- | :--- | :--- | :--- |
| **A: Decouple + convention (recommended)** | Clear; two dimensions serve distinct purposes | One more field to maintain in INDEX | Pragmatic approach |
| B: Version = status | Simple; one glance | May force premature 1.0.0 | Strict versioning |
| C: lifecycle YAML field | Machine-readable | Overlaps with ASQM status | Automation-heavy |

### E12. 可测试规范（可执行验证）

**推荐方案**：渐进式 spec 验证脚本 + JSON Schema

**脚本 `verify-skill-structure.mjs`** 检查：

- YAML 元数据完整性（name、description、tags、version、license）
- 必选标题（Purpose、Core Objective、Use Cases、Behavior、I/O、Restrictions、Self-Check、Examples）
- Core Objective 子节（Primary Goal、Success Criteria、Acceptance Test）
- Success Criteria 数量：3–6 项
- 名称与目录名一致
- 名称格式：1–64 字符，kebab-case，无连续连字符

**YAML 元数据的 JSON Schema** 校验：

- 字段类型与约束
- 标签值相对 INDEX 标签体系
- 版本格式（SemVer）
- 名称格式正则

| Alternative | Pros | Cons | Best for |
| :--- | :--- | :--- | :--- |
| **A+B: Script + JSON Schema (recommended)** | Covers structural + metadata; industrial tooling | Semantic checks still need human/LLM | Comprehensive |
| A: Custom script only | Full control | Reinvents schema validation | Quick start |
| C: LLM-assisted audit | Handles semantic checks | Non-deterministic; costly; not CI-friendly | Manual audits |

## 实施阶段

按依赖与价值排序：

### Phase 1：基础（基础设施）

```text
E12 Testable Spec  →  A1 CI/CD Automation  →  A2 Quality Gates
```

先建立检查能力，再纳入 CI，最后自动化质量评估。

**交付物**：

- `scripts/verify-skill-structure.mjs`
- `schemas/skill-metadata.json`
- `.github/workflows/pr-check.yml`
- `.github/workflows/audit.yml`

### Phase 2：能力扩展

```text
E11 Lifecycle Strategy (define conventions before adding new skills)
B3  review-typescript  →  B4 review-react
```

先建立生命周期约定，再构建前端审查链（TS 语言 + React 框架）。

**交付物**：

- 含 Stability 列的更新后 INDEX.md
- `skills/review-typescript/`
- `skills/review-react/`

### Phase 3：组合升级

```text
C8 I/O Contract Protocol  →  C7 repo onboarding flow (atomic skills in sequence)
B5 Domain-level library review (review-orm-usage, etc.)
```

先定义协议。Repo onboarding 通过按序运行 review-codebase → review-architecture → generate-standard-readme → generate-agent-entry 实现（onboard-repo 编排器已移除）。

**交付物**：

- Spec 修订：可选 `input_schema` / `output_schema` 字段
- `skills/review-orm-usage/`

### Phase 4：生态成熟

```text
D9  Plugin Sync Strategy
D10 Community Infrastructure Phase 1
```

**交付物**：

- Plugin 入选标准文档
- `marketplace.json` 同步的 CI 检查
- `CONTRIBUTING.md`
- `.github/ISSUE_TEMPLATE/`（bug、feature、new-skill）

## 已考虑的权衡

| Direction | Chosen approach | Key trade-off |
| :--- | :--- | :--- |
| CI/CD | Minimal + dogfood | 对纯 Markdown 项目的价值 vs 开销 |
| Language expansion | TS/JS priority | 广度 vs 深度；选择影响最大的语言 |
| Framework expansion | React first | 市占率 vs 链完整性 |
| Library review | Domain-based | 通用性 vs 库特定深度 |
| Orchestrators | run-checkpoint, review-code | Demo 价值 vs CI 集成（quality-gate） |
| Skill chains | I/O contracts | 简洁 vs 事件驱动灵活性 |
| Plugin sync | Selection criteria | curation 质量 vs 全量暴露 |
| Community | Gradual | 投入 vs 实际贡献者需求 |
| Lifecycle | Convention-based | 清晰 vs 额外维护 |
| Spec testing | Script + Schema | 覆盖 vs 语义检查局限 |

## 验收标准

- [x] Phase 1 交付物：spec 验证脚本与 CI workflow 可运行
- [x] Phase 2 交付物：review-typescript 与 review-react 已发布并审计
- [x] Phase 3 交付物：I/O 契约协议已定义；通过原子技能实现 repo onboarding
- [x] Phase 4 交付物：Plugin 同步已自动化；CONTRIBUTING.md 与 Issue 模板已就绪
- [x] 所有新技能通过 ASQM 校验（质量 ≥ 17）
- [x] 现有技能质量或 registry 同步无回归
