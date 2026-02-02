---
name: standards-shell
version: 1.0.0
scope: 所有 *.sh 脚本
recommended_scope: user
---

# Rule: Shell 脚本编码标准 (Shell Coding)

## 适用范围 (Scope)

所有 Bash/Shell 脚本（`*.sh`）。在编辑或生成此类文件时自动适用。

## 强制约束 (Constraints)

1. **严格模式**：始终使用 `set -euo pipefail`。
2. **日志**：使用标准日志函数（如 `log_debug`、`log_info`、`log_error`），禁止直接 `echo "[DEBUG]"`、`echo "[INFO]"` 等。
3. **函数注释**：必须包含参数与返回值说明（如 `# 参数: $1 - 说明, $2 - 说明（可选）`、`# 返回: 0 成功，1 失败`）。
4. **模块分隔**：使用 `# =============================================================================` 与模块名称作为分隔。
5. **错误处理**：实现 `trap` 错误捕获（如 `trap 'log_error "错误: 第 $LINENO 行"; exit 1' ERR`）。
6. **命名**：全局变量 `UPPER_CASE`，局部变量与函数名 `lower_case`，常量使用 `readonly`。
7. **变量引用**：始终使用引号（`"$VAR"`、`"${VAR:-default}"`），避免未加引号的 `$VAR`。
8. **条件测试**：使用 `[[ ]]` 而非 `[ ]`（如 `[[ -f "$file" ]]`、`[[ "$str" == "value" ]]`）。

## 违规示例 (Bad Patterns)

- 脚本未使用 `set -euo pipefail` 或未设置 `trap`。
- 使用 `echo "[INFO] ..."` 而非统一日志函数。
- 函数无参数/返回值注释。
- 变量未加引号（`$VAR`）或在 `[ ]` 中测试文件。

## 修正指南 (Remediation)

1. 在脚本头部加入 `set -euo pipefail` 与 `trap`。
2. 定义并统一使用 `log_*` 函数，替换所有直接 echo 的日志。
3. 为每个函数补充 `# 参数`、`# 返回` 注释。
4. 变量引用改为 `"$VAR"`；条件改为 `[[ ... ]]`。
5. 提交前执行 `bash -n script.sh` 做语法检查。
