---
artifact_type: adr
created_by: decision-record
lifecycle: snapshot
created_at: 2026-05-15
status: accepted
description: 采用 XDG canonical 路径 + bin/cortex POSIX sh 脚本取代多种历史安装模式，实现跨 IDE 统一安装与更新
---

# ADR 0010: Installation Strategy — XDG Canonical Path + bin/cortex

## 背景 (Context)

AI Cortex 承载 4 类资产（skills / rules / specs / protocols）。项目积累了多种本地安装模式，互相不兼容：

1. **README 主推「整仓克隆到 IDE 子目录」**（`~/.claude/skills/ai-cortex/`），但实际用户机器跑的是 Vercel `skills` CLI 扁平模式（`~/.agents/skills/<skill>`），两者并行存在。
2. **多 IDE = 多份克隆**，每个 IDE 各自 `git pull` 才能升级，违反 SSOT。
3. **资产分发需求不同**：skills/rules 需要"安装"到 IDE 可见位置；specs/protocols 只要克隆路径稳定即可（Agent 按路径直读）。README 未区分。
4. **Cursor 规则漂移**：`.cursor/rules/` 8 个 .mdc 与 `rules/` 12 个源文件已漂移，手工同步不可持续。

## 决策 (Decision)

采用 **XDG canonical 路径** + **`bin/cortex` POSIX sh 脚本** 作为统一安装机制：

- **Canonical 路径**：`${XDG_DATA_HOME:-$HOME/.local/share}/ai-cortex`（遵循 freedesktop.org XDG Base Directory Specification）
- **脚本**：`bin/cortex`，5 个子命令（install / update / clean / status / uninstall）
- **skills**：per-skill symlink 到 `~/.agents/skills/<skill>`（Codex-compatible）以及检测到的 IDE 专用路径 `~/.claude/skills/<skill>` / `~/.cursor/skills/<skill>`（与 Vercel CLI 布局兼容）
- **rules**：Claude Code 用 `.md` symlink；Cursor 自动翻译为 `.mdc`（`recommended_scope: user` → `alwaysApply: true`）
- **specs / protocols**：不安装，Agent 从 `$CORTEX_HOME` 直读
- **legacy 清理**：`cortex clean` 命令扫描并清理历史多种安装模式残留

## 被拒方案 (Rejected Alternatives)

| 方案 | 被拒原因 |
|------|---------|
| 纯提示词驱动（README 长文）| 不幂等；不同 IDE 需重复执行；无法自动处理漂移 |
| Vercel `skills` CLI 单选 | 只处理 skills，不处理 rules/specs/protocols；需要 Node.js |
| 每个 IDE 单独克隆 | 多份克隆违反 SSOT；多处 `git pull` 升级路径脆弱 |
| `curl \| sh` bootstrap | 安全风险；`git clone` + 两条命令已足够简洁 |
| brew formula | 维护成本高；本项目是 markdown 资产库，非可执行工具 |

## 后果 (Consequences)

- Agent 调用安装只需两条命令：`git clone ... $CORTEX_HOME && $CORTEX_HOME/bin/cortex install`
- Codex 的可用 skill 列表通常在会话启动时注入；安装或更新后需开启新会话才能稳定看到新同步的 AI Cortex skills
- Vercel CLI 既有安装默认共存不冲突（cortex 检测到非 cortex symlink 会跳过）
- `cortex uninstall --remove-home` 需要显式 `--remove-home` flag 才删除 CORTEX_HOME，防止误删仓库
- Cursor `.mdc` 自动生成，源文件 `rules/*.md` 需有 `recommended_scope` 字段和 `# Rule: ...` H1 标题
