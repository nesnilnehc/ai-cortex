# 快速开始与使用

两种使用方式：**提示词**（任意 Agent，零安装）或 **Cursor / TRAE 安装**（脚本写入本地）。选哪种见 [README 快速开始](../README.md#快速开始)。

约定见 [AGENTS.md](../AGENTS.md) §2–§4。

---

## 提示词方式

复制下方提示词发给 Agent。fork/自托管请替换 URL。

**安装 / 配置**

```text
读取 https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/AGENTS.md，按指引发现并加载 skills/INDEX.md、rules/INDEX.md、commands/INDEX.md，后续按需使用 AI Cortex。无 AGENTS.md 则可在项目内创建并引用本库；有则追加引用。
```

**卸载**

```text
不再遵循 AI Cortex，从会话/上下文中移除已加载的技能、规则与约束，后续不再从 https://github.com/nesnilnehc/ai-cortex 或 https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/ 加载。若项目根目录 AGENTS.md 含 AI Cortex 引用，则移除该文件或删除其中相关引用。
```

配置后，用自然语言或命令提任务（如「按规范写 README」、`/readme`、「脱敏这段文档」）。可选：在项目根复制/引用本库 AGENTS.md 或使用 Git submodule。

---

## Cursor / TRAE 方式

无需克隆：下载安装脚本并执行，脚本会自动拉取仓库。**不传参数即交互式**，按提示选择 target/scope/preset。

安装：

```bash
curl -sL https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/scripts/install.py | python3 -
```

卸载（须与安装时 `--scope` 一致；用户级加 `--scope user`）：

```bash
curl -sL https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/scripts/uninstall.py | python3 - --target cursor
```

完整说明见 [README § Cursor / TRAE 安装与卸载](../README.md#cursor--trae-安装与卸载)。
