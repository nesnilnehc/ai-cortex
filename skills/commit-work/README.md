# 提交工作

使用 AI Cortex 治理创建高质量的 git 提交——审查更改、逻辑拆分、编写 Conventional Commits 消息，并同步相关 INDEX。

## 概述

这项技能可以帮助您做出易于审查且安全交付的提交。它指导您检查更改、将混合工作拆分为逻辑提交、编写清晰的常规提交消息以及运行适当的验证步骤。

## 来源与 AI Cortex 增强

这是 `softaworks/agent-toolkit` 中 `commit-work` 的本地 vendored 派生版本。AI Cortex 保留提交检查、逻辑拆分、补丁暂存和 Conventional Commits 工作流，并增加本仓库 review、INDEX 同步和输出契约。

固定上游 commit、digest、本地修改和许可证记录见 [`../SOURCES.yaml`](../SOURCES.yaml)；版权通知见 [THIRD_PARTY_NOTICES](../../docs/references/THIRD_PARTY_NOTICES.md)。历史上未经验证的 `anthropics/skills (assumed)` 来源不再使用。

- **当前版本**：2.0.1
- **许可证**：MIT

## 安装

统一由 AI Cortex 的 canonical 安装管理，见仓库根 [README](../../README.md#-install-and-use)。Agent 运行时不得从上游或 skills.sh 单独下载、替换本 Skill。

该技能适用于任何 git 仓库；在 AI Cortex 仓库中会额外检查对应 INDEX 是否同步。

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

## 示例 (Examples)

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

MIT；上游版权通知见 [THIRD_PARTY_NOTICES](../../docs/references/THIRD_PARTY_NOTICES.md)。

## 反馈

如果您发现问题或有改进建议，请在 [AI Cortex 存储库](https://github.com/nesnilnehc/ai-cortex/issues) 中提出问题。
