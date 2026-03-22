# Spec 设计原则：技能规范的整体设计思路

**Date:** 2026-03-22  
**Status:** Proposed  
**Context:** spec/skill.md YAGNI/DRY 优化后的设计反思

---

## 1. Spec 的目标

技能规范服务于三类消费者：

| 消费者 | 需求 |
| :--- | :--- |
| **技能作者** | 知道要写什么、怎么写、如何验证 |
| **Agent/编排器** | 能发现、加载、链式调用技能 |
| **工具/脚本** | 校验、生成 INDEX、维护 registry |

Spec 应在**最小必要约束**下满足三类需求，避免为单一消费者过度设计。

---

## 2. 结构设计原则

### 2.1 分层：必选 vs 可选

- **必选**：所有技能都必须满足，否则 REJECT。应尽量少、尽量稳定。
- **可选**：按需采用，用于扩展能力（如 I/O 契约、D/C 模式）。明确标注「可选」，避免与必选混淆。

**当前问题**：部分「可选但推荐」条款（如 When to Stop）与必选混在一起，作者不易判断优先级。建议：必选集中在前 4 节，可选集中在 §8。

### 2.2 单一事实来源（SSOT）

同一概念只在一处完整定义，他处引用。

- **Scope Boundaries = Skill Boundaries (don't)**：合并术语，§4 引用 §4.2。
- **Divergent/Convergent**：仅在 §8.5 定义，§4、§4.1、§4.2 引用。
- **Success Criteria ↔ Self-Check**：Self-Check 明确为「复制 Core Objective 的 Success Criteria」，不再重复描述。

**已落实**：v2.7.3 将 D/C 多处重复收缩为「见 §8.5」。

### 2.3 渐进披露（Progressive Disclosure）

- **主 spec**：覆盖 80% 技能所需内容，控制在可读长度（如 ≤400 行）。
- **附录 / 扩展**： niche 模式（如 D/C、evolution 详情）可移至 `references/` 或外部文档，主 spec 只保留摘要与链接。

**建议**：若 §8.5 未来再扩展，考虑移至 `docs/references/divergent-convergent-pattern.md`，主 spec 保留表格摘要。

---

## 3. 内容设计原则

### 3.1 YAGNI

- **不写入 spec 的**：尚未有消费者、尚未有技能使用的功能。例如 `aliases`、`compatibility`、`allowed-tools` 在生态未明确需求前，不占用主篇幅。
- **延后至需求的**：`metadata.evolution` 完整结构 → 引用 agentskills.io，待有 fork 需求时再细化。
- **示例技能**：引用真实存在的技能（如 `breakdown-tasks`、`design-solution`），避免假设性技能名导致混淆。

### 3.2 DRY

- **定义**：概念一次定义，多处引用。
- **示例**：一个完整示例覆盖多节（如 Core Objective + Self-Check 共用 design-solution 示例），避免重复展示相同内容。
- **重要性/理由**：合并为一句或引用前文，不重复罗列 bullet。

### 3.3 可验证性

- **质量门**：REJECT/WARN 条件明确、可自动化检查。如「缺少 Skill Boundaries → REJECT」可由脚本解析 Restrictions 节判断。
- **Success Criteria**：3–6 条、可勾选，便于 Self-Check 执行。
- **Acceptance Test**：一句话问题，便于人工或 Agent 判断完成与否。

---

## 4. 维护策略

### 4.1 版本与变更日志

- 变更日志保留最近 5–10 条，过久条目可归档至 `docs/references/spec-changelog-archive.md`。
- 主版本升级时，在 spec 开头明确「迁移指南」链接，避免作者遗漏。

### 4.2 与技能生态对齐

- 示例中的技能名、路径须与 `skills/INDEX.md`、`spec/artifact-contract.md` 一致。新增规范时运行 verify-registry 与 curate-skills 做回归检查。
- 引用外部规范（agentskills.io、artifact-contract）时使用稳定链接，避免失效。

### 4.3 自举

- spec 本身可被「技能化」：`refine-skill-design`、`curate-skills` 读取 spec 进行校验。Spec 的修改应考虑这些技能的兼容性。
- 质量保证流程（§7.1）应引用实际存在的脚本与技能，避免占位符命令。

---

## 5. 后续可考虑的改进

| 改进项 | 收益 | 成本 |
| :--- | :--- | :--- |
| 增加简短目录（≤10 条） | 长文档导航 | 低 |
| 将 §8.5 D/C 移至 references | 主 spec 更短 | 需更新引用 |
| 必选/可选标签表格 | 作者快速判断 | 中（需维护） |
| 从 agentskills.io 同步 YAML 字段 | 生态兼容 | 需定期同步 |
| Schema 化（JSON Schema 描述 SKILL 结构） | 自动化校验 | 高 |

---

## 6. 总结

优秀 spec 的特征：**最少必要约束 + 单一事实来源 + 可验证 + 与生态对齐**。v2.7.3 的 YAGNI/DRY 优化是在此方向上的收敛；后续迭代应继续避免「为未来可能性」扩展，优先满足当前技能作者与工具的实际需求。
