# 分发规范 (Distribution)

本规范定义本项目**如何交付**：渠道、交付物与入口文件。用户如何配置与使用，见 [配置与使用](installation.md) 与 [使用](usage.md)。

---

## 1. 分发渠道

| 渠道 | 形式 | 适用场景 |
| :--- | :--- | :--- |
| **源码仓库** | Git clone / submodule | 贡献者、需要版本锁定的项目。 |
| **Raw 资源** | 固定 Base URL（如 `https://raw.githubusercontent.com/.../main/`） | 动态自举、按需拉取单文件。 |
| **发布包（可选）** | GitHub Releases 附件（zip/tar）或 `dist/` 快照 | 离线、内网或需固定版本且不依赖 Git 的场景。 |

当前以“源码仓库 + Raw 资源”为主。

---

## 2. 交付物与入口文件

| 文件 | 用途 | 主要受众 |
| :--- | :--- | :--- |
| **AGENTS.md** | Agent 操作手册：如何扫描、自检、与 spec 交互。 | 拥有文件读取权限的智能体（如 Cursor Agent）。 |
| **llms.txt** | 基于 [llms-txt.org](https://llms-txt.org/) 的机器发现入口；全库文档路径索引。 | AI 搜索引擎、爬虫、通过 URL 拉取能力的 Agent。 |
| **manifest.json** | 注册表：Skill/Rule/Command 路径与版本；供程序化拉取与发现。 | CI/CD、集成工具、Agent。 |

**如何选择**：Agent 初次进仓库 → 读 `AGENTS.md`；通过 URL 拉取能力 → 用 `llms.txt`；程序化发现资产 → 解析 `manifest.json`。

### manifest.json 的 distribution 字段

`manifest.json` 的 **`distribution`** 对象仅包含以下字段，供实现方（Agent、CI、集成工具）解析：

| 字段 | 说明 |
| :--- | :--- |
| **spec** | 本规范路径（如 `spec/distribution.md`）。 |
| **installation_spec** | 配置与使用规范路径（如 `spec/installation.md`）。 |

本项目**不提供** `install_script`、`default_install_root` 等字段；资产通过入口文件发现与按需拉取，无安装脚本。

---

## 3. 与配置、使用的关系

- 用户**配置与使用**（由 Agent 读取入口、发现资产）：见 [spec/installation.md](installation.md)、[spec/usage.md](usage.md)。
