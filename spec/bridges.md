# Bridges 规范 (Bridges Specification)

Bridges 是本项目提供的**适配层**：将本库的规则/命令转换为特定 IDE 或 CI 所需的配置文件，在**安装阶段**由安装脚本按用户选择或参数注入。

---

## 1. 定义

**Bridge**：一个具名适配器，对应 `bridges/` 下的一个子目录，在安装时可选执行，产出目标平台约定的文件（如 `.cursorrules`、`.github/workflows/xxx.yml`）。

- **输入**：本库的 Raw 根 URL（由安装脚本传入）、本库的 rules/commands 等资产路径。
- **输出**：消费方仓库内的一处或多处约定路径的配置文件。
- **触发**：由安装脚本通过交互询问或参数/环境变量 `CORTEX_BRIDGES` 决定是否执行。

---

## 2. 契约

| 约定项 | 说明 |
| :--- | :--- |
| **名称** | 与 `bridges/<name>/` 目录名一致，小写，连字符分隔（如 `github-actions`、`cursor`）。安装脚本以该名称识别并调用。 |
| **目录** | 每个 bridge 占 `bridges/<name>/`，内含模板或说明；至少包含 `README.md` 说明用途与用法。 |
| **产出路径** | 由本规范或该 bridge 的 README 明确写出（如 cursor → `.cursorrules`），安装脚本按约定写入消费方仓库根目录或指定路径。 |
| **调用方式** | 安装脚本按名称拉取模板（如 `bridges/<name>/*.yml`）并做变量替换，或下载并执行 `scripts/sync.sh <name> <base_url>`；具体以安装脚本实现为准。 |

---

## 3. 当前 Bridges

| 名称 | 产出路径 | 说明 |
| :--- | :--- | :--- |
| `github-actions` | `.github/workflows/ai-cortex-sync.yml` | 定时从本库拉取并同步规则；模板见 [bridges/github-actions/sync-template.yml](../bridges/github-actions/sync-template.yml)，使用见 [bridges/github-actions/README.md](../bridges/github-actions/README.md)。 |
| `cursor` | `.cursorrules` | 将规则与命令写入 Cursor 使用的根目录文件；逻辑由 [scripts/sync.sh](../scripts/sync.sh) 提供，说明见 [bridges/cursor/README.md](../bridges/cursor/README.md)。 |

---

## 4. 如何新增 Bridge

1. 在 `bridges/` 下新建目录 `bridges/<name>/`，名称与安装脚本可识别的 bridge 名称一致。
2. 至少提供 `README.md`，说明用途、产出路径、使用步骤。
3. 若需模板文件（如 YAML），放在该目录下；安装脚本拉取时会将本库 Raw 根 URL 等做替换。
4. 在 **scripts/install.sh** 的 bridge 分支中增加对 `<name>` 的处理（拉取模板或调用 sync.sh）。
5. 在本规范 **§3 当前 Bridges** 中增加一行，并更新 [bridges/README.md](../bridges/README.md) 的目录说明。

---

## 5. 与安装和配置的关系

- 用户侧：是否注入、注入哪些 Bridge，由 [spec/installation.md](installation.md) 与安装脚本约定（交互或 `CORTEX_BRIDGES`）。
- 本规范：定义 Bridge 的**契约**（名称、目录、产出、如何新增），供维护者与安装脚本实现遵循。
