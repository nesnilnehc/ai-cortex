# 快速开始与使用

消费项目通过 Agent 使用本库：对 Agent 说下方提示词即可。约定见 [AGENTS.md](../AGENTS.md) §2–§4。

---

## 给 Agent 的提示词

复制下方提示词发给 Agent。fork/自托管请替换 URL。项目内 AGENTS.md 由项目自管；写盘仅在被授权时执行。

**安装 / 配置**

```text
读取 https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/AGENTS.md，按指引发现并加载 skills/INDEX.md、rules/INDEX.md、commands/INDEX.md，后续按需使用 AI Cortex。无 AGENTS.md 则可在项目内创建并引用本库；有则追加引用。
```

**卸载**

```text
不再遵循 AI Cortex，从会话/上下文中移除已加载的技能、规则与约束，后续不再从 https://github.com/nesnilnehc/ai-cortex 或 https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/ 加载。若项目根目录 AGENTS.md 含 AI Cortex 引用，则移除该文件或删除其中相关引用。
```

---

## 如何使用

对 Agent 使用上方「安装/配置」提示词后，用自然语言或命令提任务（如「按规范写 README」、`/readme`、「脱敏这段文档」）。无需安装脚本，资产从 Raw URL 按需加载。

**可选**：在项目内固定引用时，可将本库 AGENTS.md 复制到项目根或自建 AGENTS.md 引用本库入口；或用 Git submodule 挂到项目下。
