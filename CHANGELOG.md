# 更新日志 (Changelog)

本文档记录本项目的 notable 变更；版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

---

## [2.0.0] - 未发布

### 破坏性变更 (Breaking Changes)

自本版本起，**移除 `CORTEX_MODE` 及 static / dynamic / auto 模式**，统一为一种默认行为：Agent 从给定资产根（通常为本仓库或 Raw 根 URL）按需读取入口文件与索引并加载资产。

- **已移除**：
  - `AGENTS.md` 中的「模式开关 (Mode Switch)」段落及 `CORTEX_MODE=static|dynamic|auto` 选项。
  - [spec/usage.md](spec/usage.md) 中的「模式开关」章节及 static/dynamic/auto 表格。
  - 文档中「安装/配置（静态模式）」提示词及所有「动静态集成」「三种模式」表述。
- **默认行为**：Agent 读取 AGENTS.md 后，按指引从当前仓库或给定资产根（含 Raw 根 URL）解析 `skills/INDEX.md`、`rules/INDEX.md`、`commands/INDEX.md` 并加载对应 SKILL/RULE/Command；不再通过环境变量或配置切换模式。

### 迁移指引 (Migration)

- **旧提示词中含 `CORTEX_MODE=static`、`CORTEX_MODE=dynamic` 或 `CORTEX_MODE=auto`**：请删除该部分，改为使用唯一的安装/配置提示词：「读取 Raw 的 AGENTS.md，按指引发现并加载 skills/INDEX.md、rules/INDEX.md、commands/INDEX.md」。
- **若消费方需要离线或锁版本**：改用分发方式（如 Git submodule、Release 快照、按 manifest 同步到本地），而非模式开关；详见 [spec/installation.md](spec/installation.md)、[spec/distribution.md](spec/distribution.md)。

### 规则 (Rules)

- **重命名**：`chinese-technical-standard` → `writing-chinese-technical`（路径 `rules/chinese-technical-standard.md` 已删除，新路径 `rules/writing-chinese-technical.md`）。AGENTS.md 与 manifest.json 已更新引用；若外部有硬编码旧规则名或路径，请改为 `writing-chinese-technical` / `rules/writing-chinese-technical.md`。
- **新增**：`workflow-import`、`workflow-documentation`、`standards-coding`、`standards-shell`、`tools-list-dir-dotfiles`、`documentation-markdown-format`。详见 [rules/INDEX.md](rules/INDEX.md)。
- **规范**：`spec/rule.md` §2 补充规则命名约定（与 INDEX 分类对应）及文件名长度建议。

---

## [1.2.0] - 未发布

### 破坏性变更 (Breaking Changes)

自本版本起，**不再提供安装脚本与 Bridges**，改为仅通过**入口文件**供 Agent 发现与使用。

- **已移除**：
  - `scripts/install.sh`：一行安装脚本。
  - `scripts/sync.sh`：规则/命令同步脚本。
  - `bridges/` 目录：含 `README.md`、`cursor/README.md`、`github-actions/README.md`、`github-actions/sync-template.yml`。
  - `spec/bridges.md`：Bridges 规范。
- **manifest.json**：`distribution` 中已移除 `default_install_root`、`install_script`；仅保留 `spec`、`installation_spec`。
- **使用方式**：不再生成 `.cortex/` 或通过 Bridges 写入 `.cursorrules`、`.github/workflows/`；由 **Agent 直接读取本仓库的 AGENTS.md 与索引**，按 [spec/usage.md](spec/usage.md) 发现、注入、自检。

### 迁移指引 (Migration)

- **此前依赖 `curl .../install.sh | bash` 或 `scripts/sync.sh` 的用户**：请改用 README 与 [docs/getting-started.md](docs/getting-started.md) 中的「给 Agent 的提示词」，让 Agent 从本仓库绝对地址读取 AGENTS.md 并发现技能与规则；无需在本机执行安装命令。
- **此前通过 Bridges（如 GitHub Actions、Cursor）同步规则的项目**：可保留既有 `.cursorrules` 或 workflow 作为快照；后续更新请由 Agent 按需从本仓库拉取，或自行根据 [manifest.json](manifest.json) 与入口文件实现同步逻辑。
- **实现方（Agent/CI/集成工具）**：发现与资产根不再依赖 `.cortex/config.json` 或 `install_root`；应以当前仓库根、Raw 根 URL 或消费方给定的资产根解析 `skills/INDEX.md`、`rules/INDEX.md` 等。详见 [spec/usage.md](spec/usage.md)。

### 其他变更

- 文档与 spec 全面对齐「Spec 驱动 + 入口文件驱动」：安装和配置规范更名为「配置与使用」；架构与愿景表述更新。
- README、getting-started 中补充：涉及在项目内创建/修改/删除 AGENTS.md 的操作，仅在用户授权 Agent 写入时执行。
- spec/distribution.md 中明确 `manifest.json` 的 `distribution` 字段契约（仅 `spec`、`installation_spec`）。

---

[2.0.0]: https://github.com/nesnilnehc/ai-cortex/compare/v1.2.0...v2.0.0
[1.2.0]: https://github.com/nesnilnehc/ai-cortex/compare/v1.1.0...v1.2.0
