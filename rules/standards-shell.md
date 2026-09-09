---
name: standards-shell
version: 1.0.0
scope: every *.sh script
recommended_scope: user
---

# Rule: Shell Coding Standards

## Scope

This rule applies automatically whenever a Bash or Shell script (`*.sh`) is edited or generated.

## Constraints

1. **Strict mode**: always `set -euo pipefail`.
2. **Logging**: use the standard log functions (`log_debug`, `log_info`, `log_error`). Never `echo "[DEBUG]"`, `echo "[INFO]"` or similar directly.
3. **Function comments**: document parameters and return value (for example `# 参数: $1 - 说明, $2 - 说明（可选）`, `# 返回: 0 成功，1 失败`).
4. **Section separators**: use `# =============================================================================` followed by the section name.
5. **Error handling**: install a `trap` (for example `trap 'log_error "错误: 第 $LINENO 行"; exit 1' ERR`).
6. **Naming**: `UPPER_CASE` for globals, `lower_case` for locals and function names, `readonly` for constants.
7. **Variable expansion**: always quote — `"$VAR"`, `"${VAR:-default}"`. Avoid bare `$VAR`.
8. **Conditionals**: use `[[ ]]`, not `[ ]` (for example `[[ -f "$file" ]]`, `[[ "$str" == "value" ]]`).

## Bad Patterns

- A script without `set -euo pipefail`, or without a `trap`.
- `echo "[INFO] ..."` instead of the shared log function.
- A function with no parameter or return documentation.
- Unquoted variables (`$VAR`), or file tests inside `[ ]`.

## Remediation

1. Add `set -euo pipefail` and a `trap` at the top of the script.
2. Define and consistently use `log_*` functions; replace every direct echo used for logging.
3. Add parameter and return-value comments to each function (this repository uses `# 参数` / `# 返回`).
4. Quote every expansion as `"$VAR"`; convert conditionals to `[[ ... ]]`.
5. Run `bash -n script.sh` for a syntax check before committing.
