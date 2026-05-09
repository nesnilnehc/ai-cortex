---
name: define-mission
description: Define the fundamental purpose of a project or organization. Answers why the project exists; produces a single mission statement persisted to docs.
description_zh: 定义项目或组织的根本目的；回答项目为何存在；产出 mission 陈述并持久化到 docs。
tags: [documentation, workflow]
version: 1.4.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [define mission, mission, why we exist]
input_schema:
  type: free-form
  description: Project or product identifier; current understanding of purpose from docs, README, or user
output_schema:
  type: document-artifact
  description: Mission statement written to docs/project-overview/mission.md (or project norms)
  artifact_type: mission
  path_pattern: docs/project-overview/mission.md
  lifecycle: living
---

# 技能：定义使命

> **角色**：战略链第一层，定义项目存在的根本目的
> **WHAT**：单一使命陈述（1–3 句，仅说明"为何存在"）
> **HOW**：从 README/docs/用户处引出目的，与用户确认后写入约定路径
> **区别**：愿景（未来状态）→ `define-vision`；指标 → `define-north-star`；目标 → `design-strategic-goals`

## 目的

定义并记录使命：项目或组织存在的持久原因。使命陈述回答"为什么存在这个？"，注重结果（我们服务的目的）而非实施（我们如何做或我们构建什么），在路线图或功能变化时保持稳定。

## 核心目标

**首要目标**：生成单一、用户确认的使命陈述，并持久化到约定路径。

**成功标准**：
1. ✅ 使命陈述存在：1–2 句话（最多 3 句），仅说明根本目的
2. ✅ 用户明确批准（"已批准"、"看起来不错"等）
3. ✅ 写入约定路径（默认 `docs/project-overview/mission.md`，按项目 norms 覆盖）
4. ✅ 不混入愿景、指标、目标、里程碑或实施细节
5. ✅ 措辞稳定：独立于功能或时间表

**验收测试**：新团队成员能否仅读使命就理解项目存在的原因？

## 范围边界

**本技能负责**：引出根本目的；起草 1–2 句使命；与用户确认；写入约定路径。

**本技能不负责**（交接给指定技能）：
- 愿景 → `define-vision`
- 北极星指标 → `define-north-star`
- 战略目标 → `design-strategic-goals`
- 里程碑/路线图 → `define-roadmap`

**交接点**：使命批准后 → 推荐 `define-vision`。

## 使用场景

- 新项目或战略刷新时定义"我们为何存在"
- 团队对方向认知不一致，需要单一来源
- 战略链起点（mission → vision → north-star → goals → roadmap）

## 行为

**执行**：
1. 加载上下文：项目名、领域、对目的的现有理解（README、现有文档、用户描述）
2. 引出：为谁？解决什么根本问题？为何值得做？
3. 起草使命陈述（1–2 句话，仅目的，无未来状态/指标/目标/功能）
4. 用户确认；若候选包含流行语或实施细节，提示重写
5. 持久化到约定路径；覆盖现有文件前必须确认

## 输入与输出

**输入**：项目标识符；对目的的现有理解（来自 README、docs 或用户）。

**输出**：使命陈述 Markdown 文档；路径见 frontmatter `output_schema.path_pattern`；生命周期 living。

## 限制

- **MUST NOT** 在使命陈述中包含愿景、指标、目标、里程碑、功能或实施细节
- **MUST NOT** 未经用户确认覆盖现有 mission.md
- **MUST** 应用 YAGNI：陈述即核心，仅在确有需要时添加可选段落（"为谁"、"解决什么问题"）

## 反模式

### ✅ 正确：以结果为中心

输入：README 说"我们构建了一个支持 YAML 配置、回滚和审核日志的 CLI"
使命草案："我们的存在是为了为团队提供可靠、可审核的部署方式，并具有回滚和清晰的历史记录。"

**为何正确**：聚焦目的（可靠部署），不列功能（YAML、CLI）。

### ❌ 错误：混入功能或未来状态

错误草案："我们构建了一个支持一键部署的 CLI，到 2027 年实现全行业最快回滚。"

**问题**：列出功能（"一键 CLI"）和指标/未来状态（"2027 年最快"）。功能属于产品文档，未来状态属于愿景。

## 示例

### 示例 1：仅使命，与愿景分开

**背景**：用户说"我们的部署工具需要一个使命，愿景稍后再考虑。"

**流程**：引出 who（工程团队）、问题（手动部署易错）、why（可靠性、安全性）。草案：「我们的存在是为了为工程团队提供单一、可靠的方式，将服务从代码部署到生产，将手动步骤降至最低、安全性提至最高。」用户确认 → 写入 `docs/project-overview/mission.md`。

### 示例 2：使命已存在，请求重写（边界场景）

**背景**：现有 mission.md 包含产品功能描述。

**流程**：读取现有版本，识别功能描述部分。提取目的：客户为何需要这个产品？起草精简版（仅目的）。覆盖前必须用户确认；保留旧版本到 git history 便于追溯。

## AI 重构指令

### 问题：使命陈述包含未来状态或指标

**识别**：陈述中出现"到 YYYY 年"、"实现 X% 提升"、"成为最快/最大"等。

**纠正**：
1. 识别未来状态/指标片段
2. 提示用户："这部分属于愿景或北极星，建议从使命中移除"
3. 重写为纯目的陈述
4. 推荐运行 `define-vision` 或 `define-north-star` 承接被移除的内容

### 问题：使命陈述列出功能

**识别**：陈述中出现"我们构建了 X"、"包含 A、B、C 功能"等。

**纠正**：将"我们构建了 X"重写为"我们的存在是为了 Y"，把功能视角转换为目的视角。

## 自检

- [ ] 使命陈述 1–2 句（最多 3 句），仅目的
- [ ] 用户已确认
- [ ] 写入约定路径
- [ ] 无愿景/指标/目标/里程碑/功能混入
- [ ] 措辞独立于时间表
