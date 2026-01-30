---
name: workflow-documentation
scope: 所有新建或维护 .md 文档
---

# Rule: 文档管理策略 (Documentation Management)

## 适用范围 (Scope)
所有创建、命名或维护 Markdown 文档（`.md`）的行为。适用于项目内文档库、设计文档、临时笔记等。

## 强制约束 (Constraints)

1. **最小化**：不为了记录思考过程而创建文档；不创建名为 SUMMARY、COMPLETE、FINAL、REVIEW、NOTES、*UPDATES*、*OPTIMIZATION* 等临时总结/完成记录文档。
2. **DRY**：不在多个文档中重复相同内容；使用文档间引用或一个主题一个权威文档。
3. **用户导向**：只写解决实际问题的使用文档，按用户角色组织（开发者、运维、CI/CD）；不写面向过程的思考记录。
4. **决策树**：创建任何 `.md` 前须自问：是否需要持续维护？是否已存在于其他文档？是否有 3 个以上用户会使用？任一为否则考虑不创建或使用 Wiki/Issue/内部笔记。
5. **临时文档**：允许的临时文档须有明确命名（如 `docs/design/YYYY-MM-DD-主题.md`、`*.draft.md`）、专门目录（如 `docs/design/`、`experiments/`、`meetings/`）及生命周期与清理策略；禁止无标识的 COMPLETE_SUMMARY、FINAL_NOTES 等。
6. **正式文档**：须包含清晰标题、概述、快速开始、详细说明、故障排查、相关链接、版本或更新日期。
7. **清理**：变更记录用 CHANGELOG.md；改进记录用 Issue/PR；临时文档到期后整合到正式文档或归档/删除。

## 违规示例 (Bad Patterns)

- 创建 `SUMMARY.md`、`COMPLETE_REFACTOR.md`、`REVIEW_2024.md`。
- 在多个 README 中复制相同安装步骤而非引用。
- 为一次重构过程新建「优化记录」文档而非写进 CHANGELOG 或 commit。

## 修正指南 (Remediation)

1. 拟创建文档前按决策树检查；若不必创建，改用 commit、注释或 Issue。
2. 已有类似内容时，更新现有文档或添加引用链接。
3. 临时内容使用 `*.draft.md` 与专门目录，并设定清理时间（如 7/14/30 天或决策完成后整合）。
4. 定期审查文档，合并重复、更新过时、归档或删除超期临时文档。
