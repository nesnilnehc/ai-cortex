# 分发规范 (Distribution)

本规范定义本项目**如何交付**：渠道、交付物与入口文件。用户如何安装与配置、如何使用，见 [安装和配置](installation.md) 与 [使用](usage.md)。

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
| **manifest.json** | 注册表：Skill/Rule/Command 路径与版本；`distribution.install_script` 指向安装脚本。 | CI/CD、集成工具、安装脚本。 |

**如何选择**：Agent 初次进仓库 → 读 `AGENTS.md`；通过 URL 拉取能力 → 用 `llms.txt`；脚本同步或安装 → 解析 `manifest.json`。

---

## 3. 与安装、使用的关系

- 用户**安装与配置**（一行命令、`.cortex/`、`config.json`）：见 [spec/installation.md](installation.md)。
- 用户**使用**（发现、注入、自检、模式开关）：见 [spec/usage.md](usage.md)。
