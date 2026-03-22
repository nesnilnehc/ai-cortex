# 审查代码（编排器）

**状态**：已验证

## 用途

按固定顺序协调原子审查技能（范围→语言→框架→库→cognitive）并将其发现汇总到一份报告中。本身不执行代码分析；调用或模拟 review-diff、review-codebase、review-dotnet、review-java、review-sql、review-vue、review-security、review-architecture。

## 何时使用

- 完整的代码审查：用户要求“审查代码”或“审查我的更改”并期望一份合并报告。
- 预 PR 或预提交：运行完整的管道并获取一份报告。
- 对于单维度审查（例如仅差异或仅安全性），请改用相应的原子技能。

## 输入

- 用户意图（全面审查与特定维度）。
- 已知的代码范围（git diff 或路径）。

## 输出

- 包含标准格式调查结果的单一汇总报告（位置、类别、严重性、标题、描述、建议）。

## 评分 (ASQM)

| 维度 | 分数 |
| ：-------------- | :---- |
|agent_native | 5 |
|cognitive| 5 |
|composability | 5 |
|stance| 5 |
| **asqm_quality** | 20 |

## 生态

|领域 |价值|
| :------------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|overlaps_with（所有者/存储库：技能名称）| nesnilnehc/ai-cortex:审查-diff, nesnilnehc/ai-cortex:审查-代码库, wshobson/agents:代码审查-excellence, secondarysky/claude-skills:代码审查, Trailofbits/skills:差异审查, cxuu/golang-skills:go-code-review, obra/superpowers:请求代码审查，skillcreatorai/Ai-Agent-Skills:代码审查 |
|市场地位 |差异化|

## 完整定义

请参阅 [SKILL.md](./SKILL.md) 了解执行顺序、行为和输出契约。