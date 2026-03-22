# 技能安装与重装说明

本文档说明如何安装、升级与重装 AI Cortex 技能，适用于通过 [skills.sh](https://skills.sh)（`npx skills add`）安装的用户。

## 首次安装

```bash
npx skills add nesnilnehc/ai-cortex
```

全局安装（跨项目、跨 Agent 可用）：

```bash
npx skills add nesnilnehc/ai-cortex -g
```

仅安装指定技能：

```bash
npx skills add nesnilnehc/ai-cortex --skill <skill-name>
```

## 升级已有技能

使用 `--force` 覆盖本地已有版本：

```bash
npx skills add nesnilnehc/ai-cortex --force
```

## 完整重装（推荐场景）

若满足以下任一情况，建议先卸载再安装：

- 技能曾改名（如 `discover-document-norms` → `discover-docs-norms`）
- 技能结构或定义有较大变更
- 升级后出现行为异常或冲突

### 一键重装脚本

```bash
./scripts/uninstall-reinstall-ai-cortex.sh
```

该脚本会：

1. 从 `~/.agents/.skill-lock.json` 提取来源为 `nesnilnehc/ai-cortex` 的技能
2. 调用 `npx skills remove ... -g -y` 卸载上述技能
3. 调用 `npx skills add nesnilnehc/ai-cortex -g --force -y` 重新安装
4. 列出当前已安装技能以验证

**说明**：脚本仅卸载 AI Cortex 技能，不会影响其他来源的技能（如 anthropics、vercel-labs 等）。

### 手动重装

若需完全清空全局技能后再安装：

```bash
npx skills remove --all -g -y
npx skills add nesnilnehc/ai-cortex -g -y
```

**注意**：此方式会卸载所有来源的技能，需自行重装其他包。

## 无 Node 环境

使用 fallback 脚本，将仓库内容复制到指定目录：

```bash
./scripts/install-fallback.sh --dest <目标目录>
```

需自行将 `skills/`、`rules/`、`AGENTS.md` 等接入目标 Agent 的配置。

## 安装位置

| 范围 | 路径 | 说明 |
| :--- | :--- | :--- |
| 全局 | `~/.agents/skills/` | 技能实际文件 |
| Cursor | `~/.cursor/skills/` | 多为指向 `~/.agents/skills/` 的 symlink |
| 注册表 | `~/.agents/.skill-lock.json` | 记录已安装技能及来源 |

## 常见问题

**Q：脚本执行报错 `command not found: npx`？**

需安装 Node.js。若无法安装，使用 `scripts/install-fallback.sh`。

**Q：重装后 Cursor 未识别新技能？**

重启 Cursor 或重新加载窗口（Command Palette → Developer: Reload Window）。
