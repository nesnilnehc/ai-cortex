# 回顾 TypeScript

**状态**：已验证

## 用途

仅审查语言和运行时约定的 TypeScript 和 JavaScript 代码：类型安全和类型系统使用、异步模式和 Promise 处理、错误处理、模块设计 (ESM/CJS)、运行时正确性（空/未定义、相等、强制）、API 和接口设计以及性能和内存。以标准格式发出结果列表。不执行范围选择或安全/架构审查。

## 何时使用

- 精心安排的审查：在 TypeScript/JavaScript 项目运行审查代码时用作语言步骤。
- 仅 TypeScript 审查：当用户只想检查 TypeScript/JavaScript 语言约定时。
- PR 前语言检查表：确保类型安全、异步正确性和模块设计健全。

## 输入

- 包含 TypeScript 或 JavaScript 代码（.ts、.tsx、.js、.jsx、.mts、.mjs、.cts、.cjs）的代码范围（文件、目录或 diff），由用户或范围技能提供。

## 输出

- 结果列表：位置、类别=语言打字稿、严重性、标题、描述、可选建议。

## 评分 (ASQM)

| 维度 | 分数 |
| ：-------------- | :---- |
|agent_native | 5 |
|cognitive| 4 |
|composability | 5 |
|stance| 5 |
| **asqm_quality** | 19 | 19

## 生态

|领域|价值|
| :------------------------------------ | :------------------------------------------------------------------------------------------------------------------------ |
|overlaps_with（所有者/存储库：技能名称）| nesnilnehc/ai-cortex:审查代码库，nesnilnehc/ai-cortex:审查代码，nesnilnehc/ai-cortex:审查差异 |
|市场地位 |商品 |

## 完整定义

请参阅 [SKILL.md](./SKILL.md) 查看清单和输出合同。