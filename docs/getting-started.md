# 快速开始与使用

使用方式：**提示词**（任意 Agent，零安装、IDE 无关）。定位与边界见 [positioning.md](positioning.md)。

约定见 [AGENTS.md](../AGENTS.md) §2–§4。

---

## 提示词方式

复制下方提示词发给 Agent。fork/自托管请替换 URL。

**接入**

```text
读取 https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/AGENTS.md，按指引发现并加载 skills/INDEX.md、rules/INDEX.md、commands/INDEX.md，后续按需使用 AI Cortex。无 AGENTS.md 则可在项目内创建并引用本库；有则追加引用。
```

**卸载**

```text
不再遵循 AI Cortex，从会话/上下文中移除已加载的技能、规则与约束，后续不再从 https://github.com/nesnilnehc/ai-cortex 或 https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/ 加载。若项目根目录 AGENTS.md 含 AI Cortex 引用，则移除该文件或删除其中相关引用。
```

配置后，用自然语言或命令提任务（如「按规范写 README」、`/readme`、「脱敏这段文档」）。可选：在项目根复制/引用本库 AGENTS.md 或使用 Git submodule。

---

## 此前通过 Cursor / TRAE 安装的用户

若此前通过安装脚本将规则/命令/技能写入 `.cursor/` 或 `.trae/`，可手动删除以下目录以卸载：

- 项目级：`./.cursor/`、`./.trae/`
- 用户级：`~/.cursor/`、`~/.trae/` 下由 AI Cortex 写入的 `rules/`、`commands/`、`skills/` 等子目录

本项目已不再提供安装/同步脚本，后续请使用提示词方式接入。详见 [定位](positioning.md)。
