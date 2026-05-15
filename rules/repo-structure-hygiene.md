---
artifact_type: rule
name: repo-structure-hygiene
version: 1.0.0
scope: 审计或自检仓库目录结构时（runtime / linter / CI / 人工执行）
recommended_scope: user
status: active
---

# Rule: 仓库结构卫生（Repository Structure Hygiene）

> 仓库目录结构的硬约束集合。运行时（AgentFabric / linter / CI / 人工）按本规则执行检测；本规则只规定判据，不规定如何检测。
>
> 与 `rules/doc-health-criteria.md` 互补——前者管文档健康（链接 / SSOT / 对齐），本规则管目录结构（错放 / 命名 / 空目录 / 过期）。

---

## 1. 错放文件

- [ ] 文件所在目录与其类型 / 内容相符（如 `.md` 不在 `src/`，`.py` 不在 `docs/`）
- [ ] `docs/` 根目录仅放索引 / 治理文件（README / INDEX / ARTIFACT_NORMS / CONTRIBUTING 等）；其他类型文件按 `docs/ARTIFACT_NORMS.md` 的 path_pattern 归位
- [ ] artifact_type 推断（从 frontmatter / 文件名 / 内容）应与所在目录一致

---

## 2. 命名一致性

- [ ] 文件名遵循 kebab-case（与 `docs/architecture/asset-naming.md` 对齐）
- [ ] 时间戳前缀 `YYYY-MM-DD-` 仅用于允许带时间戳的 artifact_type（如 `adr` / `design-decision`）；其他类型禁带时间戳
- [ ] 时间戳格式必须 `YYYY-MM-DD`（不接受 `YYYY/MM/DD` / `YYYYMMDD` / `YY-M-D` 等变体）
- [ ] 同目录内命名风格一致（不混用 PascalCase / snake_case / kebab-case）

---

## 3. 空目录

- [ ] 目录非空（仅含 `.gitkeep` 视为空）
- [ ] 例外：依赖目录（`node_modules` / `.venv` / `dist` / `build` / `__pycache__`）不视为空目录违规——它们应在 `.gitignore` 中

---

## 4. 过期制品

判定为过期的文件：

- [ ] 扩展名为 `.bak` / `.tmp` / `.orig` / `.swp`
- [ ] 文件名含 `DEPRECATED` / `OLD` / `UNUSED` / `LEGACY` 等显式标记
- [ ] 超过 180 天未修改且全仓 grep 无引用（孤立 + 陈旧）

过期制品应：删除 / 归档至 `.archive/` / 在 frontmatter 标 `status: deprecated` 之一。

---

## 5. 重复条目

- [ ] 同目录下文件名高度相似的不应共存（如 `util.py` 与 `utils.py` / `auth.py` 与 `Auth.py`）
- [ ] 重复时必须有明确区分理由（注释或 README 说明）

---

## 6. 顶层目录结构

- [ ] 顶层目录只出现项目约定中存在的目录（按 `docs/ARTIFACT_NORMS.md` 或仓库 README 列出）
- [ ] 项目要求的标准目录（如 `docs/` / `src/`）必须存在

---

## 反模式

- ❌ 文件名不符 kebab-case 且未在项目约定中列出豁免
- ❌ `.bak` / `.tmp` 等备份文件提交到仓库
- ❌ 空目录提交且无 `.gitkeep` 标识保留意图
- ❌ docs/ 根直接放具体 artifact 文件（如 `docs/goals.md` 应在 `docs/process-management/goals/` 等子目录）
- ❌ 错位时间戳前缀（requirement / specs 等带 `2026-03-01-` 前缀）

---

## 关联资产

- 检测执行（`find` / `ls` / 自定义脚本 / linter）由 runtime / CI 工具承接，本规则只规定判据
- 安全的可逆操作（`git mv` 文件 / `rmdir` 空目录）由人工或 AgentFabric runtime 在用户确认后执行
- 危险操作（删除非空目录 / 修改 git 历史 / 重命名涉及大量引用更新）必须人工执行，不在自动化范围
