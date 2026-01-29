# 使用规范 (Usage)

本规范定义**运行时契约**（发现、注入、自检），供实现方（Agent）遵循。快速开始与使用说明见 [docs/getting-started.md](../docs/getting-started.md)；配置与使用见 [spec/installation.md](installation.md)。

---

## 1. 发现

- 读取 `skills/INDEX.md` 获取能力列表；以当前仓库或给定的资产根（如本库根、Raw 根 URL、消费方子模块路径）解析 `skills/INDEX.md`、`rules/INDEX.md`（配置与使用见 [spec/installation.md](installation.md)）。
- 按 `description`、`tags` 与当前任务语义匹配，选中 SKILL/RULE；若 SKILL 有 `related_skills`，按需递归或并行加载。

---

## 2. 注入

- 将选中的 SKILL 或 RULE 的 **完整 Markdown** 作为系统指令或即时约束载入上下文。
- 每个 SKILL/RULE 作为原子单位注入，避免碎片化复制。
- **嵌套加载 (Nesting)**：规则须在执行任何 Skill 之前先注入（将 rules/ 下相关准则载入为恒久约束），再加载技能。

---

## 3. 自检

- 产出内容后，按该技能的 **「质量检查 (Self-Check)」** 章节自审，仅在所有项通过后提交。
- 若技能定义了交互策略（如遇事询问），先暂停并向用户确认。

---

## 4. 组合与集成（可选）

- **组合**：可链式调用多技能（如先脱敏再生成 README）；执行技能时保持全局 Rule 加载。
- **集成方式**：云端引用（运行时拉 URL）、Git 子模块、或按 manifest 同步到本地；详见安装与分发约定。

资产与文档描述语言遵循 [AGENTS.md](../AGENTS.md) 沟通准则及 [spec/rule.md](rule.md) 语言与描述。
