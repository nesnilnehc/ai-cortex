# GitHub Actions 同步模板使用指南

> [!IMPORTANT]
> 本目录下的 `sync-template.yml` 是提供给 **能力集成方 (Consumer)** 使用的，旨在实现其项目与 `AI Cortex` 规范的自动化同步。

## 使用步骤

### 1. 复制文件
将 [sync-template.yml](./sync-template.yml) 复制到你项目的 **`.github/workflows/`** 目录下。

### 2. 重命名 (可选)
你可以将其重命名为 `ai-cortex-sync.yml`。

### 3. 配置权限
确保你的 GitHub Action 拥有写权限（Write Permission），以便它能将更新后的 `.cursorrules` 提交回仓库：
- 进入项目 Settings -> Actions -> General。
- 在 "Workflow permissions" 中选择 "Read and write permissions"。

### 4. 路径验证
- 脚本默认会将规则同步到根目录的 `.cursorrules`。
- 如果你的项目使用其他文件名（如 `.windsurfrules`），请修改 YAML 中调用 `sync.sh` 的参数。

## 运作原理
该工作流会定期触发，调用 AI Cortex 的远程 `sync.sh` 脚本，抓取最新的 Rules 和 Commands，并自动覆盖你本地的配置，最后通过 Git Bot 完成提交。
