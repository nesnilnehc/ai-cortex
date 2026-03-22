---
name: generate-standard-readme
description: Generate professional, governance-ready README with fixed structure. Core goal - produce standardized front-page documentation that explains purpose, usage, and contribution guidelines. Use for asset governance, audit, or unified documentation standards.
description_zh: 生成固定结构的转换导向 README：10 秒理解、1 分钟运行、清晰的用途与场景；支持治理与采纳模式。
tags: [documentation, devops, writing]
version: 1.2.1
license: MIT
recommended_scope: user
metadata:
  author: ai-cortex
triggers: [generate readme, readme]
input_schema:
  type: code-scope
  description: Repository or project path to generate README for
output_schema:
  type: document-artifact
  description: Standardized README.md written to the project root
---

# 技能（Skill）：生成标准README

## 目的 (Purpose)

为**任何软件项目**（开源、内部服务、微服务、工具）创建**专业、一致、高度可读的**首页文档。标准化的信息布局可降低协作成本、提高工程规范并保持核心资产的可发现性。

---

## 核心目标（Core Objective）

**首要目标**：制作一个具有固定结构的标准化自述文档，使读者能够在 3 分钟内了解项目目的、安装和贡献。

**成功标准**（必须满足所有要求）：

1. ✅ **创建 README 文件**：以完整标准结构的“README.md”写入项目根目录
2. ✅ **存在所有 9 个必需部分**：标题/徽章、描述、功能、安装、快速入门、使用、贡献、许可证、作者
3. ✅ **安装命令可执行**：复制粘贴命令无需修改即可工作（无硬编码路径或损坏的链接）
4. ✅ **通过三秒清晰度测试**：读者观看后3秒内了解项目目的
5. ✅ **包含许可证部分**：指定许可证类型并链接到许可证文件

**验收测试**：新开发人员能否仅使用 README 在 3 分钟内理解项目的用途、安装并运行基本示例？

---

## 范围边界（范围边界）

**本技能负责**：

- 具有固定 9 部分结构的自述文件生成
- 专业的语气和治理就绪的格式
- 资产发现和审计的标准化文档
- 徽章生成和部分排序

**本技能不负责**：

- 项目类型特定的模板（使用 softaworks/agent-toolkit 中的“crafting- effective-readmes”）
- 全面的项目文档（使用“bootstrap-docs”）
- 代理条目文件或 AGENTS.md（使用 `generate-agent-entry`）
- 隐私/安全编辑（如果需要，使用“decontextualize-text”）

**转交点**：当 README 完成所有 9 个部分并通过验收测试后，移交给用户进行审查或提交版本控制。

---

## 使用场景（用例）

- **新项目**：快速添加新存储库的标准自述文件。
- **资产治理**：跨内部服务或库统一自述文件风格，以实现更好的索引和跨团队发现。
- **审计和合规性**：使遗留系统达到内部审计或架构审查的文档标准。
- **移交和发布**：在转移项目、更改所有权或公开发布时，确保受众能够理解目的、用途以及如何贡献。

**何时使用**：当项目需要一个“第一面”来解释它是什么、如何使用它以及如何协作时。

---

**范围**：该技能强调**固定的输出结构**和**治理**（统一风格、审计、可发现性）；输出契约嵌入在技能中。对于按项目类型创建模板或引导式问答创建，请使用 Skills.sh 的“crafting-efficient-readmes”（例如 softaworks/agent-toolkit）。

---

## 行为（行为）

### 原则（原则）

- **清晰**：读者立即了解该项目是什么以及它解决什么问题。
- **完整性**：包括用户和贡献者需要的一切。
- **可操作**：提供复制粘贴安装和快速启动命令。
- **专业**：使用标准 Markdown 和传统的章节顺序。

### 语气和风格

- 使用**中立、客观**的语言；避免炒作（“最好的”、“革命性的”），除非有数据支持。
- **直接简洁**：短句；避免使用填充形容词和官僚措辞；专业性体现在清晰度和易读性上，而不是形式上。
- 保持代码示例简短，注释清晰。

### 视觉元素

- **徽章**：包括顶部的许可证、版本、构建状态等。
- **结构**：使用“---”或清晰的标题级别来分隔各个部分。
- **表情符号**：谨慎使用（例如📦、🚀、📖）以提高可扫描性。

---

## 输入与输出 (Input & Output)

### 输入（输入）

- **项目元数据**：名称，一行描述。
- **功能**：核心功能。
- **要求**：例如Node.js/Python 版本。
- **安装/运行**：具体的 shell 命令。

### 输出（输出）

- **自述文件来源**：具有以下结构的 Markdown：
  1. 头衔和徽章
  2. 核心说明
  3.✨ 特点
  4.📦安装
  5. 🚀 快速启动
  6. 📖 使用/配置
  7. 🤝 贡献
  8. 📄 许可证
  9. 👤 作者和致谢

---

## 限制（限制）

### 硬边界（Hard Boundaries）

- **没有损坏的链接**：不要添加 404 的链接。
- **无冗余重复**：不要在多个部分中重复相同的事实（例如许可证）。
- **无硬编码路径**：在安装和快速启动示例中使用占位符或变量。
- **需要许可证**：始终包含许可证部分；不要省略它。
- **仅限固定结构**：始终使用 9 节结构；不要偏离或重新排序部分。
- **无发明**：不要发明用户未提供的功能、命令或细节；使用占位符来弥补缺失的信息。

### 技能边界 (Skill Boundaries)（避免重叠）

**不要做这些（其他技能可以处理它们）**：

- **项目类型模板**：按项目类型（React、Python 等）创建 README 模板 → 使用 `crafting-efficient-readmes` (softaworks/agent-toolkit)
- **全面的文档**：创建完整的文档套件（架构文档、API 文档、指南）→ 使用 `bootstrap-docs`
- **代理条目文件**：创建 AGENTS.md 或代理合同文件 → 使用 `generate-agent-entry`
- **隐私编辑**：从文档中删除 PII 或敏感信息 → 使用 `decontextualize-text`
- **内容细化**：改进现有的 README 散文或结构 → 使用一般写作/编辑技能

**何时停止并交接**：

- 用户问“你能创建所有项目文档吗？” → 移交给“bootstrap-docs”
- 用户询问“你能创建一个 AGENTS.md 文件吗？” → 移交给 `generate-agent-entry`
- 用户问「你能为 React 项目定制这个吗？」→ 针对项目类型模板建议 `crafting-efficient-readmes`
- 包含所有 9 个部分的自述文件 → 移交给用户进行审查/提交

---

## 自检（Self-Check）

### 核心成功标准（必须满足所有标准）

- [ ] **创建 README 文件**：以完整标准结构的“README.md”写入项目根目录
- [ ] **存在所有 9 个必需部分**：标题/徽章、描述、功能、安装、快速入门、使用、贡献、许可证、作者
- [ ] **安装命令可执行**：复制粘贴命令无需修改即可工作（无硬编码路径或损坏的链接）
- [ ] **通过三秒清晰度测试**：读者在观看后 3 秒内了解项目目的
- [ ] **包含许可证部分**：指定许可证类型并链接到许可证文件

### 流程质量检查

- [ ] **语气**：文字是否直接、简洁，没有官僚或报告式的措辞？
- [ ] **徽章**：徽章链接是否指向正确的分支或文件？
- [ ] **窄屏幕**：表格和长代码块在小屏幕上可读吗？
- [ ] **没有发明**：我是否避免发明了用户未提供的功能或命令？
- [ ] **使用的占位符**：对于缺失的信息，我是否使用了明确的占位符（例如“TBD”）而不是猜测？

### 验收测试

**新开发人员能否仅使用自述文件在 3 分钟内了解该项目的用途、安装并运行基本示例？**

如果否：自述文件不完整或不清楚。查看各部分是否缺少信息或令人困惑的说明。

如果是：自述文件已完成。继续转交。

## 示例（示例）

### 之前与之后

**之前（最少）**：

> **我的项目**
>
> 该程序处理图像。
> 安装：pip install 。
> 运行：python run.py

**之后（标准）**：

> **我的项目**
>
> [![许可证：MIT](https://img.shields.io/badge/License-MIT-blue.svg)](许可证)
>
> 高性能图像批处理工具，可通过并发加速压缩。
>
> ---
>
> **✨ 特点**
>
> - **并发压缩**：多线程；比基线更快。
> - **格式**：WebP、PNG、JPEG 转换。
>
> ---
>
> **📦安装**
>
> 
```bash
> pip install my-project
> ```

>
> ---
>
> **🚀 快速启动**
>
> 
```python
> from myproject import Compressor
> Compressor('images/').run()
> ```


### 边缘案例：遗留项目，信息很少

- **输入**：名称：legacy-auth。没有描述。没有功能列表。环境和安装未知。
- **预期**：仍然生成结构完整的自述文件；使用占位符（例如“查看功能源”、“安装步骤待定”）并标记“待完成”；不要发明功能或命令；保留徽章、部分顺序和许可证，以便用户稍后填写。

---

## 附录：输出合约

当此技能生成自述文件时，它遵循以下合同：

|栏目顺序|必填 |
| :------------ | :-------------------------- |
| 1 |头衔和徽章|
| 2 |核心说明|
| 3 |特点|
| 4 |安装|
| 5 |快速入门|
| 6 |使用/配置|
| 7 |贡献 |
| 8 |许可证|
| 9 |作者和致谢 |

限制：不能有损坏的链接；没有多余的重复；没有硬编码路径；需要许可部分。

---

## 参考（参考文献）

- [GitHub 自述文件文档](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- [很棒的自述文件](https://github.com/matiassingers/awesome-readme)
- [Shields.io（徽章）](https://shields.io/)