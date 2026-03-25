# 提交工作

使用 AI Cortex 治理创建高质量的 git 提交 - 审查更改、逻辑拆分、编写清晰的消息（常规提交）、与 INDEX/manifest 同步。

## 概述

这项技能可以帮助您做出易于审查且安全交付的提交。它指导您检查更改、将混合工作拆分为逻辑提交、编写清晰的常规提交消息以及运行适当的验证步骤。

## AI Cortex 增强版

这是“commit-work”技能的增强版本，专为 AI Cortex 项目而开发，具有额外的治理和质量功能：

### 增强功能

- **预提交审查集成**：自动调用“review-diff”技能以在登台前捕获问题
- **注册表同步**：确保添加或修改技能时“skills/INDEX.md”和“manifest.json”保持同步
- **规范合规性**：遵循 AI Cortex `specs/skill.md` 结构和质量标准
- **增强的自检**：与 AI Cortex 治理相一致的全面验证清单

### 进化元数据

该技能集成了多个来源的内容：

#### 主要来源（分叉）

- **技能**：`提交工作`
- **存储库**：人类技能集合（假设）
- **版本**：1.0.0
- **许可证**：麻省理工学院
- **借用**：核心工作流结构、常规提交格式、补丁暂存方法

#### 集成组件

- **技能**：`审查差异`
- **存储库**：nesnilnehc/ai-cortex
- **版本**：1.3.0
- **许可证**：麻省理工学院
- **借用**：预提交审核方法

### 当前版本

- **版本**：2.0.0
- **许可证**：麻省理工学院

## 安装

### 对于 AI Cortex 用户


```bash
npx skills add nesnilnehc/ai-cortex --skill commit-work
```
文本

### 对于其他项目

该技能适用于任何 git 存储库，但在 AI Cortex 项目中使用时提供附加功能（自动注册表同步检查）。

## 用法

当您需要时激活此技能：

- 以清晰、可审查的方式提交您的工作
- 将混合更改拆分为逻辑、原子提交
- 编写常规提交消息
- 在推送之前确保提交符合质量标准
- 维护 AI Cortex 项目中的注册表同步

该技能将指导您完成从检查到验证的全面工作流程。

## 主要特点

### 工作流程步骤

1. 登台前检查工作树
2. **运行提交前审查**（AI Cortex 增强）
3. 决定提交边界并根据需要进行拆分
4. 仅暂存相关更改
5. 仔细审查分阶段的变更
6. 清楚地描述变化
7. 编写常规提交消息
8. 运行验证（测试/lint）
9. **如果需要同步注册表**（AI Cortex 项目）
10.重复直到工作树干净

### 常规提交格式


```text
type(scope): short summary

body explaining what and why

footer (BREAKING CHANGE if needed)
```


支持的类型：`feat`、`fix`、`refactor`、`docs`、`test`、`chore`、`perf`、`style`

## 示例（示例）

请参阅 [SKILL.md](SKILL.md#examples) 了解详细示例，包括：

- 简单的功能添加
- 需要拆分的混合更改
- AI Cortex 技能添加与注册表同步

## 相关技能

- [review-diff](../review-diff/SKILL.md): 预提交代码审查（集成在步骤 2 中）

## 贡献

这项技能是 AI Cortex 项目的一部分。提出改进建议：

1. 在 [nesnilnehc/ai-cortex](https://github.com/nesnilnehc/ai-cortex) 提出问题
2. 遵循贡献指南
3. 确保变更保持向后兼容性或明确记录重大变更

## 许可证

MIT 许可证 - 与原始的“commit-work”技能和 AI Cortex 项目相同。

## 版本历史

- **2.0.0**（当前）：AI Cortex 增强版，具有审核集成和注册表同步功能
- **1.0.0**：原始版本（分叉基线）

## 反馈

如果您发现问题或有改进建议，请在 [AI Cortex 存储库](https://github.com/nesnilnehc/ai-cortex/issues) 中提出问题。