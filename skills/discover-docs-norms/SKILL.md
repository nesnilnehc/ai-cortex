---
name: discover-docs-norms
description: Help users establish project-specific artifact norms (paths, naming, lifecycle) through scanning and confirmation. Core goal - produce docs/ARTIFACT_NORMS.md with all norms in human-readable + machine-parseable format.
description_zh: 通过对话与扫描，帮助建立项目级文档制品规范（路径、命名、生命周期）；产出 docs/ARTIFACT_NORMS.md。
tags: [documentation, workflow]
version: 1.2.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [discover norms, document norms]
input_schema:
  type: free-form
  description: Project path, optional starting point (AI Cortex default, project-documentation-template, blank)
output_schema:
  type: document-artifact
  description: docs/ARTIFACT_NORMS.md (single source of truth for all artifact norms)
---

# 技能（Skill）：发现文档规范

## 目的 (Purpose)

帮助用户为文档治理定义特定于项目的产品规范（路径、命名、生命周期）。项目可能有自己的文档结构；该技能发现并形式化它，以便其他技能（捕获工作项、设计解决方案、评估文档）可以遵循项目规范。

---

## 核心目标（Core Objective）

**首要目标**：自动推导项目特定的文档规范，生成 `docs/ARTIFACT_NORMS.md` 作为单一规范来源。

**成功标准**（必须满足所有要求）：

1. ✅ **自动扫描项目结构**：扫描 docs/ 目录，推断现有约定
2. ✅ **推导规范**：基于扫描结果，自动推导路径、命名、front-matter 规范，生成置信度评分
3. ✅ **简化用户确认**：仅要求用户确认推导结果（而非选择起点）
4. ✅ **生成单一规范文件**：
   - `docs/ARTIFACT_NORMS.md`（人类可读 + 机器可解析的完整规范）
   - 包含：路径映射、命名约定、front-matter 标准、置信度评分
5. ✅ **用户确认**：用户在最终写入之前明确批准了规范

**验收测试**：
- 其他技能（如 assess-docs、tidy-repo）能否读取输出并正确应用规范？
- 置信度评分 > 90%？
- 生成的 linting.yaml 和 templates 可用？

---

## 范围边界（范围边界）

**本技能负责**：

- 扫描项目`docs/`结构
- 确认产品路径和命名的对话
- 根据项目文档模板标准生成 `docs/ARTIFACT_NORMS.md`（参考 project-documentation-template）
- 从 AI Cortex 默认、项目文档模板或空白开始

**本技能不负责**：

- 引导完整的项目文档（使用“bootstrap-docs”）
- 评估文档准备情况（使用“assess-docs”）
- 根据规范验证现有文档（使用“评估文档”；合规性是其报告的一部分）

**转交点**：编写并确认规范后，将其移交给其他文档制作技能或“评估文档”以进行合规性和准备情况检查。

---

## 使用场景（用例）

- **新项目**：尚无产品规范；用户希望在使用捕获工作项或设计解决方案之前建立它们。
- **现有项目**：项目具有自定义的“docs/”结构；将其正式化，以便技能协调一致。
- **迁移**：采用 AI Cortex 默认值或项目文档模板；创建规范文件以保持一致性。

---

## 行为（行为）

### 交互（互动）政策

- **输入**：项目路径（默认 CWD）
- **处理**：自动扫描 docs/ → 自动推导规范 → 计算置信度
- **交互**：仅展示推导结果，要求用户确认（y/e/n）
- **确认**：用户选择后，在写入文件前再次确认路径

### 第 1 阶段：扫描

1.检查项目根目录和`docs/`（如果存在）
2. 识别现有路径：待办、设计、adr、校准等。
3. 记下示例文件中的任何约定（命名、前面的内容）

### 第 2 阶段：自动推导规范（改进）

而不是"选择起点"，系统现在**自动扫描 + 推导**：

1. **扫描项目 docs/ 结构**
   - 枚举所有 .md 文件
   - 读取各文件的 front-matter
   - 记录文件路径、名称、大小、修改时间

2. **推断 Artifact Type**（基于优先级）
   - ① Front-matter 的 `artifact_type` 字段（置信度 100%）
   - ② 路径关键词（如 `docs/architecture/` → architecture，置信度 90%）
   - ③ 文件名关键词（如 `adr-`, `design-` → 对应类型，置信度 70%）
   - ④ Front-matter title 关键词（置信度 60%）
   - ⑤ 默认 "other"（置信度 10%）

3. **推导命名约定**
   - 扫描文件名，检测主导的大小写风格（kebab-case? snake_case? camelCase?）
   - 检测日期格式（YYYY-MM-DD? YYYY-MM? YYYYMMDD?）
   - 检测常见前缀/后缀

4. **推导路径约定**
   - 为每个 artifact_type，统计现有文件的路径
   - 取最常见的路径作为该类型的规范路径
   - 例：如果 5 个 goals 文件都在 `docs/` 中，则规范为 `docs/`

5. **推导 Front-matter 标准**
   - 扫描所有文件的 front-matter
   - 统计各字段出现频率
   - 将出现在 >= 50% 文件中的字段列为"必需"

6. **生成置信度评分**
   - 总体置信度 = 平均推断置信度
   - 输出：推导出的规范 + 置信度指标

### 第 3 阶段：用户确认（简化）

系统展示推导结果，用户仅需确认，无需选择起点：

**展示内容**：
```
推导出的规范（置信度 95%）：

✓ 路径约定:
  - goals         → docs/goals/
  - requirements  → docs/requirements-planning/
  - architecture  → docs/architecture/
  - designs       → docs/design-decisions/
  - adrs          → docs/process-management/decisions/
  - milestones    → docs/process-management/milestones/
  - roadmaps      → docs/
  - todos         → docs/

✓ 命名约定:
  - 大小写: kebab-case
  - 日期格式: YYYY-MM-DD (如 2026-03-06-auth.md)

✓ Front-matter 必需字段:
  - artifact_type, created_by, lifecycle, created_at

这个规范对吗？
(y) Yes, confirm  / (e) Edit specific paths  / (n) No, start over
```

**用户选项**：
- `y`：确认，进入第 4 阶段
- `e`：编辑特定项（如改变 requirements 的路径）
- `n`：重新扫描（重新跑第 2 阶段，可能需要手工调整文件）

### 第 4 阶段：生成输出文件

1. 根据推导结果 + 用户确认，生成单一规范文件 `docs/ARTIFACT_NORMS.md`：

   **`docs/ARTIFACT_NORMS.md`**（人类可读 + 机器可解析）
   ```markdown
   ---
   artifact_type: governance
   created_by: discover-docs-norms
   created_at: 2026-03-24
   status: draft
   ---

   # 项目文档规范

   **推导日期**: 2026-03-24
   **推导置信度**: 95%
   **推导工具**: discover-docs-norms v1.1.0

   ## 路径约定

   | Artifact Type | Path Pattern | 说明 | 置信度 |
   | --- | --- | --- | --- |
   | goals | `docs/goals/` | 项目目标 | 100% |
   | requirements | `docs/requirements-planning/` | 需求规划 | 90% |
   | architecture | `docs/architecture/` | 架构文档 | 95% |
   | design | `docs/design-decisions/` | 设计决策 | 85% |
   | adr | `docs/process-management/decisions/` | 架构决策记录 | 80% |
   | milestone | `docs/process-management/milestones/` | 里程碑计划 | 75% |
   | roadmap | `docs/` | 产品路线图 | 70% |
   | todo | `docs/` | 待办项目 | 65% |

   ## 命名约定

   - **大小写**: `kebab-case`（例：`2026-03-24-authentication-design.md`）
   - **日期格式**: `YYYY-MM-DD`（例：`2026-03-24`）
   - **模式**: `[YYYY-MM-DD-]artifact-name.md`

   ## Front-Matter 标准

   **必需字段**：
   ```yaml
   artifact_type: [goals|requirements|architecture|design|adr|milestone|roadmap|todo]
   created_by: [author name or tool name]
   created_at: YYYY-MM-DD
   status: [draft|approved|active|archived]
   ```

   **推荐字段**：
   - `lifecycle`: 文档生命周期阶段
   - `tags`: 主题标签
   - `related`: 相关文档链接

   ## 验证规则

   ### Naming
   - ✅ 文件名必须符合 `kebab-case`
   - ✅ 日期前缀必须是 `YYYY-MM-DD`
   - ✅ 不允许 `snake_case` 或 `camelCase`

   ### Paths
   - ✅ goals 必须在 `docs/goals/`
   - ✅ requirements 必须在 `docs/requirements-planning/`
   - （按表格规定）

   ### Front-Matter
   - ✅ 四个必需字段必须存在
   - ✅ artifact_type 必须与路径对应
   - ✅ created_at 必须是有效的日期

   ## 根目录结构

   ### 根目录允许的文件
   - 索引文件：`README.md`、`README_*`、`README.*`
   - 目录索引：`INDEX.md`、`INDEX_*`
   - 治理文件：`ARTIFACT_NORMS.md`、`LANGUAGE_SCHEME.md`、`CHANGELOG.md`、`CONTRIBUTING.md`
   - 项目元数据文件：`LICENSE`、`AUTHORS` 等

   ### 必要的组织结构
   所有其他文件必须按其 artifact_type 和 path_pattern 分类到指定的子目录中。

   **验证规则**：
   - ✅ 文件所在目录必须与其 artifact_type 对应
   - ✅ docs/ 根目录不应有内容制品（如文档、需求、架构等）
   - ✅ 所有内容必须有明确的类别化目录

   ## 整体置信度: 95%

   ### 低置信度项（需关注）
   - 待办项（todos）：置信度 65%，建议与用户确认
   - 里程碑（milestones）：置信度 75%，可能需要调整路径

   ---

   **推导依据**：
   - 扫描了 docs/ 中的 42 个文件
   - 分析了现有 front-matter 和路径模式
   - 参考了 project-documentation-template 最佳实践
   ```

2. 输出写入前，向用户确认：
   - 是否同意提议的路径映射？
   - 是否同意命名和 front-matter 标准？
   - 是否需要调整任何部分？

3. 写入 `docs/ARTIFACT_NORMS.md` 到磁盘

---

## 输入与输出 (Input & Output)

### 输入（输入）

- 项目路径（默认：当前工作空间根目录）
- （无需用户选择起点——系统自动推导）

### 输出（输出）

**单一规范文件**：
- `docs/ARTIFACT_NORMS.md`：完整规范文档（人类可读 + 机器可解析）
  - 包含：路径约定、命名约定、front-matter 标准、验证规则、置信度评分
  - 其他技能（assess-docs、tidy-repo）从此文件解析规范信息

---

## 限制（限制）

### 硬边界（Hard Boundaries）

- **未经确认不得覆盖**：未经用户明确批准，请勿写入或覆盖规范文件。
- **架构合规性**：输出必须遵循 [spec/artifact-norms-schema.md](../../spec/artifact-norms-schema.md)。

### 技能边界 (Skill Boundaries)（避免重叠）

**不要做这些（其他技能可以处理它们）**：

- **完整文档 bootstrap**：引导完整项目文档 → 使用 `bootstrap-docs`
- **准备情况评估**：评估文档就绪 → 使用 `assess-docs`
- **合规性验证**：验证制品规范合规 → 使用 `assess-docs`（在其报告中包含合规性）

**何时停止并交接**：

- 用户问「能帮我建立完整文档结构吗？」→ 移交给 `bootstrap-docs`
- 用户问「文档准备好发布了吗？」→ 移交给 `assess-docs`
- 规范已写入且用户确认 → 交接完成

---

## 自检（Self-Check）

- [ ] 已扫描 docs/ 目录并推导规范
- [ ] 已计算置信度评分（目标 > 90%）
- [ ] 用户已确认推导结果
- [ ] 已生成 `docs/ARTIFACT_NORMS.md` 规范文件
- [ ] 规范文件已写入磁盘

### 验收测试

**1. 其他技能（assess-docs、tidy-repo）能否从 `docs/ARTIFACT_NORMS.md` 解析规范？**
- assess-docs 能否解析路径约定、命名规则、front-matter 标准？
- tidy-repo 能否应用这些规范进行结构整理？

**2. 规范文档格式是否一致且可解析？**
- 规范文档是否包含所有必要的验证规则？
- 是否清楚地标注了置信度？

**3. 置信度 > 90%？**

若所有答案为"是"，技能完成。否则，调整推导规则。

---

## 示例（示例）

### 示例 1：新项目，AI Cortex 默认值

**上下文**：空项目，没有文档/。

**步骤**：从 AI Cortex 默认开始。建议路径：`docs/待办/`、`docs/design-decisions/`、`docs/process-management/decisions/`、`docs/calibration/`。用户确认。编写“docs/ARTIFACT_NORMS.md”并根据需要创建“docs/”子目录。

### 示例 2：现有自定义结构

**上下文**：项目有“docs/work-items/”、“docs/decisions/”，没有正式规范。

**步骤**：扫描结构。建议映射：待办项 → `docs/work-items/`，adr → `docs/decisions/`。用户确认。使用自定义路径编写规范文件。

---

## 附录：输出合约

该技能为项目规范生成单一**规范文档**输出。输出必须符合项目文档模板标准：

|元素|要求 |
| :--- | :--- |
| **主要输出** | `docs/ARTIFACT_NORMS.md` — 项目级规范文档（governance 类型）|
| **内容结构** | YAML front-matter + Markdown 规范表 + 验证规则 + 置信度评分|
| **必需部分** | 路径约定、命名约定、front-matter 标准、验证规则、置信度|
| **可解析性** | 其他技能必须能从 Markdown 表格解析路径映射和验证规则 |
| **路径映射** | 每个 artifact_type 映射到一个 path_pattern；用户在写入前必须确认|