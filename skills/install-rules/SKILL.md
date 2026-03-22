---
name: install-rules
description: Install rules from source repo into Cursor or Trae IDE with explicit confirmation and conflict detection. Core goal - install rules to editor destinations with user approval before any write.
description_zh: 从源仓库将规则安装到 Cursor 或 Trae IDE；需显式确认与冲突检测；写盘前需用户批准。
tags: [automation, infrastructure]
version: 1.2.1
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
input_schema:
  type: free-form
  description: Source repo or local rules directory and target IDE (Cursor or Trae)
output_schema:
  type: side-effect
  description: Rule files written to IDE-specific destinations (.cursor/rules/ or .trae/project_rules.md)
---

# 技能（Skill）：安装规则

## 目的 (Purpose)

将规则源中的**规则**（AI 行为的被动约束）安装到编辑器的规则目标中。主要来源是该项目的“rules/”目录，或用户指定的 Git 存储库。支持的安装目标： **Cursor** (`.cursor/rules/`) 和 **Trae IDE** (`.trae/project_rules.md` / `.trae/user_rules.md`)。

---

## 核心目标（Core Objective）

**首要目标**：通过明确的用户确认和冲突检测，将规则从源存储库安装到 Cursor 或 Trae IDE 中。

**成功标准**（必须满足所有要求）：

1. ✅ **源已解析**：读取规则源（此存储库“rules/”或指定的 Git 存储库），并从“INDEX.md”或目录列表构建规则列表
2. ✅ **分析目标**：在任何写入之前扫描现有目标文件并识别冲突/重复项
3. ✅ **显示安装计划**：显示每个规则操作的显式计划（“创建/跳过/冲突/更新”）和向用户显示目标路径
4. ✅ **用户确认**：用户在创建或修改任何文件之前明确批准该计划
5. ✅ **已安装的规则**：所选规则以正确的格式写入目标目的地（光标“.mdc”文件或 Trae 托管块）
6. ✅ **报告的输出**：安装后摘要包括执行的操作、目标路径以及任何转换注释或失败

**验收**测试：用户能否验证安装了哪些规则、安装在何处以及是否检测到任何冲突？

---

## 范围边界（范围边界）

**本技能负责**：

- 解析规则源（此存储库或 Git 存储库）
- 列出源中可用的规则
- 分析目标状态（现有文件/冲突）
- 构建并展示安装计划
- 将规则安装到 Cursor（`.mdc` 格式）或 Trae（托管块）
- 报告安装结果

**本技能不负责**：

- 发现哪些技能可用（使用“discover-skills”）
- 创建或编写新规则（超出范围）
- 修改规则内容（准确保留源内容）
- 安装技巧（仅规则）

**转交点**：当规则安装并上报后，技能就完成了。如果用户想要发现技能，请移交给“发现技能”。

---

## 使用场景（用例）

- **此项目**：将当前存储库的 `rules/` 中的所有或选定规则安装到当前项目的 Cursor 或 Trae 规则中。
- **另一个 Git 存储库**：用户提供 `owner/repo` （以及可选的分支/引用和子路径）；列出该存储库中的规则并将选定的规则安装到 Cursor 或 Trae。
- **Bootstrap**：克隆 ai-cortex 或另一个提供规则的存储库后，安装其规则，以便代理在用户工作区中尊重它们。

---

## 行为（行为）

1. **解决来源**：
   - **此项目**：使用存储库的 `rules/` 目录。将 `rules/INDEX.md` 视为权威列表；如果存在，则解析注册表以获取规则名称和文件路径。否则列出 `rules/` 下的所有 `*.md` 文件（不包括 `INDEX.md`）。
   - **指定的 Git 存储库**：用户提供“所有者/存储库”或完整克隆 URL，以及可选的分支/引用和子路径（例如“规则”或“文档/规则”）。通过以下方式发现规则：(a) 在子路径中查找“INDEX.md”（或等效项）并解析注册表，或 (b) 列出该目录中的“*.md”文件。如果repo或路径不存在或不包含规则，请明确报告，不要写入文件。

2. **列出规则**：输出可安装规则的列表（名称、简短描述或范围）。让用户按名称选择“全部”或子集。

3. **分析目标状态（必填）**：
   - **光标**：列出现有的`./.cursor/rules/*.mdc`（项目级）或用户级规则目录（如果选择）。确定哪些目标文件名已经存在。
   - **Trae**：读取选定的目标文件（`./.trae/project_rules.md` 或 `./.trae/user_rules.md`，或全局用户级别（如果选择））（如果存在）。检测托管块是否已存在（参见步骤 6）。

4. **制定安装计划（必需）**：
   - 对于每个选定的规则，决定一个操作：“创建”、“跳过（相同）”、“冲突（不同）”或“更新（已批准显式覆盖）”。
   - 默认值必须是保守的：
     - 现有但不同的目标是“冲突”，直到用户明确批准覆盖。
     - 现有且相同的目标是“跳过”。
   - 在任何写入之前输出计划，包括预期的目标路径和每规则操作。

5. **写入前确认**：
   - 在用户明确确认计划之前，请勿创建、修改或覆盖`.cursor/rules/`、`.trae/`或任何目标路径下的任何文件。
   - 如果包含覆盖，则需要明确确认列出将覆盖哪些规则目标。

6. **安装到光标**：
   - **目标路径**：项目级别是`./.cursor/rules/`（相对于repo root）；用户级别取决于平台（例如“~/.cursor/rules/”，如果适用）。优先选择项目级别，除非用户要求用户级别。如果该目录不存在，则创建该目录。
   - **格式**：每条规则写入一个“.mdc”文件。将源规则元数据映射到 front-matter（“description”、可选的“globs”、可选的“alwaysApply”），并保留规则主体。
   - **幂等性**：在编写之前，将内容规范化并与现有目标内容（如果有）进行比较。如果相同，则“跳过”。
   - **冲突**：如果目标存在且不同，则不要覆盖，除非计划包含“更新”并且用户明确确认覆盖。

7. **安装到 Trae（托管块）**：
   - **目标路径**：项目级别为`./.trae/project_rules.md`；用户级别是“./.trae/user_rules.md”（项目范围）或全局用户级别路径（如果 Trae 支持）。优先选择项目级别，除非用户要求用户级别。如果`.trae/`目录不存在，则创建该目录。
   - **托管块（必需）**：
     - 仅在托管块内写入以避免修改用户编写的规则。
     - 在托管块周围使用“<!-- ai-cortex:begin -->”和“<!-- ai-cortex:end -->”等标记。
     - 如果托管块存在，则替换整个块内容；如果没有，则插入该块（通常附加到文件末尾）。
   - **块内容**：
     - 在块内，使用“## Rule: <name>”标头以稳定的顺序呈现每个规则的一个部分（首选“rules/INDEX.md”注册表顺序（如果可用））。
     - 保留每个规则主体（源头内容之后的所有内容）。
     - 按托管块内的规则名称进行重复数据删除（一个名称 → 一个部分）。
   - **幂等性**：如果重新渲染的托管块与当前托管块相同，则“跳过”并且不重写文件。

8. **输出**：安装后，报告计划、执行的操作、目标路径以及任何转换说明或失败。

---

## 输入与输出 (Input & Output)

### 输入（输入）

- **来源**：默认“此项目”（当前存储库“rules/”）。或者：Git 存储库 `owner/repo` 或 URL，带有可选的分支/引用和子路径（例如 `rules`、`docs/rules`）。
- **目标**：Cursor、Trae 之一或两者。
- **Scope**: "All" rules or a subset (list of rule names).
- **目的地**：项目级或用户级；默认项目级别。
- **冲突策略**：默认为保守（不覆盖）；覆盖需要明确确认。

### 输出（输出）

- **安装前**：规则列表+目标分析摘要+带有目标路径的安装计划（`创建/跳过/冲突/更新`）。
- **安装后**：执行的操作、目标路径以及任何错误或转换说明。

---

## 限制（限制）

### 硬边界（Hard Boundaries）

- **未经确认不得写入**：在未明确用户确认计划的情况下，请勿在 `.cursor/rules/`、`.trae/` 或任何目标路径下创建或修改文件。
- **未经确认不得覆盖**：如果目标已存在且有所不同，则不要覆盖，除非用户明确同意并且计划包含该目标的“更新”。

### 技能边界 (Skill Boundaries)（避免重叠）

**不要做这些（其他技能可以处理它们）**：

- 发现技能 → `发现技能`
- 创建或编辑规则内容 → 超出范围
- 安装技巧 (SKILL.md) → 超出范围

---

## 自检（Self-Check）

### 核心成功标准（必须满足所有标准）

- [ ] **源已解析**：规则源读取和从“INDEX.md”或目录列表构建的规则列表
- [ ] **分析目标**：在任何写入之前扫描现有目标文件并识别冲突/重复项
- [ ] **提供的安装计划**：使用向用户显示的每规则操作和目标路径进行规划
- [ ] **用户确认**：用户在创建或修改任何文件之前明确批准该计划
- [ ] **已安装的规则**：选定的规则以正确的格式写入目标目的地
- [ ] **报告的输出**：安装后摘要包括执行的操作、目标路径以及任何转换说明或失败

---

## 示例（示例）

### 示例 1：将此项目中的所有规则安装到 Cursor

- 阅读 `rules/INDEX.md` 并构建规则列表。
- 分析 `.cursor/rules/` 并制定保守的计划。
- 提出计划，获得确认，执行“创建”/“更新”操作，然后报告。

### 示例 2：将规则从另一个 Git 存储库安装到 Trae

- 解析`owner/repo`和子路径。
- 发现规则，为 Trae 托管块构建计划，确认，然后写入托管块。
- 报告已安装的规则和目标文件路径。

---

## 附录：输出合约 (Appendix: Output Contract)

当此技能运行完毕后，必须生成如下格式的安装后摘要报告（Side-effect report），以便代理或后续步骤能解析安装的规则以及是否有跳过/冲突：

| 字段 | 类型 | 描述 |
| :--- | :--- | :--- |
| `rule_name` | String | 安装或处理的规则名称 |
| `action` | String | 执行的操作 (`created` \| `skipped` \| `conflict` \| `updated`) |
| `target_path` | String | 规则写入的目标路径 (如 `.cursor/rules/xxx.mdc` 或 `.trae/project_rules.md`) |
| `status` | String | 最终状态 (`success` \| `failed` \| `pending_confirmation`) |

---

## 附录：输出合约 (Appendix: Output Contract)

当此技能运行完毕后，必须生成如下格式的安装后摘要报告（Side-effect report），以便代理链能解析安装的规则以及是否有跳过/冲突：

| 字段 | 类型 | 描述 |
| :--- | :--- | :--- |
| `rule_name` | String | 安装或处理的规则名称 |
| `action` | String | 执行的操作 (`created` \| `skipped` \| `conflict` \| `updated`) |
| `target_path` | String | 规则写入的目标路径 (如 `.cursor/rules/xxx.mdc`) |
| `status` | String | 最终状态 (`success` \| `failed` \| `pending_confirmation`) |