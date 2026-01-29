# 安装和配置规范 (Installation & Configuration)

最简安装与配置方式，面向最终用户。

---

## 1. 快速安装

在目标仓库根目录执行（若从 fork 安装，将 `nesnilnehc/ai-cortex` 换成你的 组织/仓库名）：

```bash
curl -sL https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/scripts/install.sh | bash
```

**依赖**：`jq`。未安装时脚本会提示。

- **交互式**：在终端中直接执行上述命令时，脚本会在核心安装完成后**询问**是否注入 Bridges（GitHub Actions 工作流、Cursor 的 `.cursorrules` 等），按提示输入 `y` 或回车跳过。
- **参数化**：无需交互时，可通过参数或环境变量指定：
  - `curl -sL .../install.sh | bash -s -- .cortex github-actions cursor` — 安装到 `.cortex` 并注入 GitHub Actions 与 Cursor。
  - `CORTEX_BRIDGES=github-actions,cursor` — 环境变量（逗号分隔）指定要注入的 bridge，不询问。
- **可注入的 Bridges**（交互时会根据当前环境给出建议，可选注入）：

| 名称 | 产出 | 适用环境 |
| :--- | :--- | :--- |
| `github-actions` | `.github/workflows/ai-cortex-sync.yml` | GitHub 仓库（存在 `.git` 或 `.github/` 时建议注入，用于定时同步规则）。 |
| `cursor` | `.cursorrules` | 使用 Cursor IDE 的项目（存在 `.cursor/` 或 `.cursorrules` 时建议注入）。 |

契约与扩展见 [spec/bridges.md](bridges.md)。

---

## 2. 安装结果

- 当前目录下生成 **`.cortex/`**：内含 `config.json`、`skills/`、`rules/`、`commands/`（含 INDEX 与资产文件）。
- 根目录生成 **`AGENTS.md`**（若不存在或非 Cortex 版本则写入）。

---

## 3. 配置

`.cortex/config.json` 由安装脚本自动写入，必要字段：

| 字段 | 说明 |
| :--- | :--- |
| `source` | 本库 Raw 根 URL，用于同步与自举。 |
| `version` | 锁定版本，便于可复现。 |
| `mode` | `static` \| `dynamic` \| `auto`，与 AGENTS.md 中 `CORTEX_MODE` 一致。 |
| `install_root` | 安装根目录，如 `.cortex`。 |

---

## 4. 可选

- 指定安装目录：`curl -sL .../install.sh | bash -s -- .cortex`
- 环境变量：`CORTEX_ROOT`（安装目录）、`CORTEX_SOURCE`（来源 URL）、`CORTEX_BRIDGES`（要注入的 bridge，逗号分隔，如 `github-actions,cursor`）

Bridges 的定义、契约与当前列表见 [spec/bridges.md](bridges.md)。

---

入口文件（AGENTS.md、llms.txt、manifest.json）的用途与场景见 [spec/distribution.md](distribution.md)。
