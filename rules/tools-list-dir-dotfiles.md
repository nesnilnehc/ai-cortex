---
name: tools-list-dir-dotfiles
version: 1.0.0
scope: Agent 使用目录列举工具时
recommended_scope: both
---

# Rule: list_dir 点文件限制 (List Dir Dotfiles Limitation)

## 适用范围 (Scope)

当 Agent 使用 `list_dir` 或等效「列举目录内容」的工具时。适用于查找项目配置、验证文件是否存在、分析项目结构等场景。

## 强制约束 (Constraints)

1. **认知**：`list_dir` 类工具默认不显示以点（`.`）开头的文件（dotfiles），仅凭其输出不能断定「目录下没有某配置文件」。
2. **完整性检查**：当需要查看完整目录内容（如查找 `.env`、`.gitignore`、`.eslintrc`、`.editorconfig` 等）时，不得仅依赖 `list_dir` 的结果。
3. **替代做法**：须采用以下至少一种方式：使用 `ls -la`（或等效命令）查看含隐藏文件；使用 `read_file` 直接读取已知配置文件名；使用 `glob_file_search` 搜索如 `**/.env*`、`**/.*rc` 等模式。
4. **验证存在性**：在结论「某文件不存在」前，若该文件为常见点文件或配置，须用上述替代方式再次确认。

## 违规示例 (Bad Patterns)

- 仅用 `list_dir` 检查目录后断言「没有 .env」。
- 分析项目结构时只依据 `list_dir` 输出，未考虑被隐藏的配置文件。
- 查找环境变量或敏感配置时未使用 `ls -la` 或直接读取。

## 修正指南 (Remediation)

1. 需要完整目录列表时，优先使用 `ls -la` 或等价方式。
2. 已知可能存在的配置文件名时，直接使用 `read_file` 尝试读取。
3. 需要批量查找点文件时，使用 `glob_file_search` 等带模式匹配的工具。
4. 在给出「文件不存在」的结论前，对常见 dotfiles 做上述补充检查。
