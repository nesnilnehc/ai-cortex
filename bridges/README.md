# 桥接层说明 (The Bridge Layer)

## 1. 核心矛盾
AI Cortex 的核心协议（`spec/`）是**工具无关**的，但 IDE（如 Cursor, Windsurf）和特定的 Agent 框架需要**特定格式**的配置文件（如 `.cursorrules`, `agent.json`）才能激活“被动约束”和“快捷指令”。

## 2. 桥接方案 (The Bridge Strategy)

### 同步流：拉取模式 (Pull-based Flow)
**核心逻辑**：并非由本库主动推送到其他项目，而是由各 **应用项目 (Consumer Repos)** 主动从本库拉取配置。
- **原因**：安全性（不需要应用库的写入权）与扩展性（应用库自行决定更新时机）。

### A. 被动约束同步 (Rule Sync)
- **工具需求**：Cursor 需要根目录下的 `.cursorrules` 文件。
- **桥接方式**：应用项目下载本库的 [sync.sh](../scripts/sync.sh)，在本地运行以生成 `.cursorrules`。
- **价值**：应用项目始终作为本库的“订阅者”。

---

## 3. 目录结构说明
- **`bridges/` (本项目内)**：存放的是 **“适配模板 (Templates)”** 和 **“接入指南 (User Guides)”**。它相当于一个插件商店。
- **应用项目内**：同步后产生的 `.cursorrules` 或 `.github/workflows/` 内容，才是真正生效的“物理配置”。

### B. 自动化集成 (CI/CD Automation) - **高级方案**
通过 GitHub Actions 实现项目的“能力自动对齐”：
1. **定时拉取**：项目每天自动运行同步脚本。
2. **静默更新**：发现本库有新规范时，Action 自动提交 PR 或直接更新 `.cursorrules`。
3. **使用指南**：参考 [github-actions/README.md](./github-actions/README.md)。

### B. 命令快捷映射 (Command Mapping)
- **工具需求**：某些 Agent 框架需要 JSON 格式的 Command Registry。
- **桥接方式**：将 `commands/*.md` 解析并转化为目标框架所需的配置文件。

### C. 软性自执行 (Soft Enforcement)
- **逻辑**：即便没有 IDE 的强制约束文件，我们在 `AGENTS.md` 中教导智能体：“在开始任何任务前，请先扫描 `rules/` 目录。”
- **效果**：智能体在心智层面实现了规则的“自加载”。

## 3. 目录结构
- `bridges/`：存放各种 IDE/平台的同步模板、脚本或配置转换工具。
