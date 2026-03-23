---
name: warn-destructive-commands
description: Warn before destructive commands. Checks Bash commands for rm -rf, DROP TABLE, force-push, git reset --hard, kubectl delete, and similar patterns. User can override each warning. Use when touching prod, debugging live systems, or in shared environments.
description_zh: 在破坏性命令执行前发出警告。检查 Bash 命令中的 rm -rf、DROP TABLE、force-push、git reset --hard、kubectl delete 等模式。用户可覆盖每次警告。适用于接触生产、调试线上或共享环境。
tags: [workflow, security]
version: 1.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
  evolution:
    sources:
      - name: "careful"
        repo: "https://github.com/nesnilnehc/gstack"
        version: "0.1.0"
        license: "MIT"
        type: "fork"
        borrowed: "Destructive pattern list, safe exceptions, warn-before-run behavior"
    enhancements:
      - "Platform-agnostic: prose-based advisory, no PreToolUse hooks or gstack scripts"
      - "Optional: users may implement check script via project config"
triggers: [careful, safety mode, prod mode, warn destructive]
input_schema:
  type: free-form
  description: Session context; skill activates advisory behavior for the session
output_schema:
  type: side-effect
  description: Warning prompts when destructive patterns detected; user may proceed or cancel
---

# 技能 (Skill)：破坏性命令警告

## 目的 (Purpose)

在会话中执行 Bash 命令前，检查是否包含破坏性模式；若命中则先警告用户并征得确认再执行，降低误操作风险。适用于接触生产、调试线上系统或共享环境。

---

## 核心目标（Core Objective）

**首要目标**：在每次执行 Bash 命令前，若检测到破坏性模式，则先 AskUserQuestion 警告并等待用户确认或取消；确认后方可执行。

**成功标准**（必须满足所有要求）：

1. ✅ **模式检查**：在执行任何 Bash 命令前，对照下表检查命令字符串
2. ✅ **命中时警告**：若命中破坏性模式，使用 AskUserQuestion 展示命令、风险与选项（A) 继续 B) 取消）
3. ✅ **安全例外**：下表「安全例外」中的模式不触发警告
4. ✅ **用户可覆盖**：用户选择继续时，执行命令；选择取消则不执行
5. ✅ **会话生效**：技能激活后，本会话内所有 Bash 命令均受此约束

**验收测试**：若用户输入含 `rm -rf /important` 的命令，Agent 是否先警告并等待确认？

---

## 范围边界（Scope Boundaries）

**本技能负责**：

- 破坏性模式的识别与警告
- 安全例外（build 产物目录等）的放行

**本技能不负责**：

- 目录编辑范围限制（freeze 类能力；若需可单独实现）
- 执行前的强制拦截（依赖主机是否支持 PreToolUse；本技能为 prose 指导，Agent 自行检查）

**转交点**：技能激活后持续生效直至会话结束；用户可随时选择「继续」覆盖单次警告。

---

## 使用场景（Use Cases）

- 用户说「be careful」「safety mode」「prod mode」
- 接触生产环境或共享仓库
- 执行可能影响数据的操作前
- 调试线上问题时

---

## 行为（Behavior）

### 激活

当用户请求本技能时，输出：

```
Safety mode active. I will warn before running any command matching destructive patterns. You can override each warning.
```

### 破坏性模式表

| Pattern | Example | Risk |
|---------|---------|------|
| `rm -rf` / `rm -r` / `rm --recursive` | `rm -rf /var/data` | Recursive delete |
| `DROP TABLE` / `DROP DATABASE` | `DROP TABLE users;` | Data loss |
| `TRUNCATE` | `TRUNCATE orders;` | Data loss |
| `git push --force` / `-f` | `git push -f origin main` | History rewrite |
| `git reset --hard` | `git reset --hard HEAD~3` | Uncommitted work loss |
| `git checkout .` / `git restore .` | `git checkout .` | Uncommitted work loss |
| `kubectl delete` | `kubectl delete pod` | Production impact |
| `docker rm -f` / `docker system prune` | `docker system prune -a` | Container/image loss |

### 安全例外（不警告）

- `rm -rf node_modules` / `.next` / `dist` / `__pycache__` / `.cache` / `build` / `.turbo` / `coverage`

### 执行流程

1. **收到 Bash 命令**：在调用 Bash 工具前，检查命令字符串是否命中上表模式（含安全例外）。
2. **若命中**：AskUserQuestion，例如：
   ```
   The following command matches a destructive pattern:
   [命令]

   Risk: [对应风险描述]
   A) Proceed anyway
   B) Cancel
   ```
3. **用户选 A**：执行命令。
4. **用户选 B**：不执行，输出 "Command cancelled."
5. **若未命中**：直接执行。

---

## 输入与输出 (Input & Output)

### 输入

- 用户激活请求（如 "be careful", "safety mode"）

### 产出

- 会话内对破坏性命令的警告提示
- 用户确认后的执行或取消

---

## 限制（Restrictions）

### 硬边界

- 仅检查 Bash 工具调用的命令字符串；不解析管道、子 shell 或脚本内的间接调用
- 若主机支持 PreToolUse 等钩子，用户可自行配置检查脚本（参见 [docs/guides/project-config.md](../../docs/guides/project-config.md)）

### 技能边界 (Skill Boundaries)

**不要做这些（其他技能可以处理它们）**：

- **目录编辑限制**：非本技能职责；需独立实现

---

## 自检（Self-Check）

### 成功标准

- [ ] 破坏性模式表已完整对照
- [ ] 安全例外已正确排除
- [ ] 命中时已先警告再执行
- [ ] 用户可选择继续或取消
- [ ] 会话内所有 Bash 命令均受此约束

### 验收测试

输入 `rm -rf /tmp/test`（或任意破坏性命令）时，是否先出现警告并等待确认？

---

## 示例（Examples）

### 示例 1：rm -rf 触发警告

**命令**：`rm -rf /var/cache`  
**行为**：命中 `rm -rf`，AskUserQuestion 警告「Recursive delete」；用户选 A 则执行，选 B 则取消。

### 示例 2：安全例外不警告

**命令**：`rm -rf node_modules`  
**行为**：属于安全例外，不警告，直接执行。

### 示例 3：git push --force 触发警告

**命令**：`git push -f origin main`  
**行为**：命中 force-push，警告「History rewrite」；用户确认后执行。
