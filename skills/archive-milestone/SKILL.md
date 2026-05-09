---
name: archive-milestone
description: Archive a completed milestone by generating a snapshot summary, folding the roadmap stage, and removing the stale tasks directory.
description_zh: 将已完成里程碑转为快照摘要，折叠路线图历史阶段，移除历史任务目录，减少 AI 上下文污染。
tags: [governance, lifecycle, archive, milestone]
version: 1.1.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
  triggers_after: [plan-next]
triggers: [archive milestone, completed milestone cleanup, milestone summary]
input_schema:
  type: structured
  fields:
    milestone_slug:
      type: string
      required: true
      description: 里程碑目录名（如 "m3"）
    apply:
      type: bool
      required: false
      default: false
      description: false = dry-run（仅预览），true = 落盘执行
  defaults:
    apply: false
output_schema:
  type: document-artifact
  description: Milestone snapshot summary + roadmap fold preview + reference update list
  artifact_type: milestone-summary
  path_pattern: docs/process-management/milestones/_archive/{slug}-summary.md
  lifecycle: snapshot
---

# 技能：里程碑归档（Archive Milestone）

## 目的 (Purpose)

将已完成里程碑的历史执行细节从活跃路径移出，生成精简快照摘要，防止历史文档持续污染 AI 对当前项目状态的判断。

---

## 核心目标（Core Objective）

**首要目标**：为已完成里程碑生成快照摘要，折叠路线图历史段落，并将原始任务目录移至 `_archive/`。

**成功标准**（apply=true 时必须全部满足）：

1. ✅ 已在 `milestones/_archive/{slug}-summary.md` 生成快照摘要
2. ✅ 摘要含：完成日期 / 关键交付物（≤5 条）/ 遗留缺口（指向后续里程碑）/ 关键 ADR 引用
3. ✅ `roadmap.md` 中对应阶段已折叠为 ≤ 3 行引用
4. ✅ 全仓 grep 旧 tasks.md 路径已重定向到摘要
5. ✅ `milestones/{slug}/` 目录已移除（内容已在摘要中保留关键信息）

**验收测试**：执行后，AI 读取 `milestones/_archive/m3-summary.md` 能准确理解 m3 的关键结果，不需要读取原始 tasks.md。

---

## 成熟度判定

**满足以下任意一条即可归档**；全部不满足则技能拒绝执行并说明原因：

| 条件 | 判定依据 |
|---|---|
| 距完成日期 ≥ 60 天 | tasks.md frontmatter 中 `completed_at` 字段 |
| 当前进行中里程碑索引 ≥ slug + 2 | roadmap.md 中 `in-progress` 里程碑的数字后缀 |

两个条件均需同时满足"全部任务 status=done 或 ✅"。

未达成熟度时输出诊断：`里程碑 {slug} 尚不满足归档条件：{具体原因}`。

---

## 行为（Behavior）

### 阶段 1：成熟度检查

读取 `milestones/{slug}/tasks.md`，验证成熟度条件。不满足任一条件则停止。

### 阶段 2：摘要生成（始终执行）

从 `tasks.md` 提取：

- **完成日期**：frontmatter `completed_at` 或最后任务完成日期
- **关键交付物**：所有 `status=done` 的任务，按验收凭据分组，提炼为 ≤ 5 条
- **遗留缺口**：任何标记为"延后"、"下迭代"或未完成的条目，连同目标里程碑
- **关键 ADR 引用**：tasks.md 中提到的 ADR 编号

### 阶段 3：影响分析（始终执行）

检测：

- `roadmap.md` 中需折叠的阶段段落
- 全仓所有引用 `milestones/{slug}/tasks.md` 的文件

### 阶段 4：输出（dry-run vs apply）

**dry-run（apply=false，默认）**：

输出预览报告，不修改任何文件：

```
=== dry-run 预览 ===

将生成：
  docs/process-management/milestones/_archive/{slug}-summary.md
  （摘要草稿如下）

将修改：
  roadmap.md 第 N-M 行折叠为：
    ### {阶段名}（已完成 {日期}）→ 详见 [milestones/_archive/{slug}-summary.md]

将删除：
  docs/process-management/milestones/{slug}/（{N} 个文件）

引用更新（{K} 处）：
  {文件路径}:{行号} → 旧路径 → 新摘要路径

=== 无文件已修改 ===
```

**apply=true**：

按预览执行全部操作，最后输出操作日志。

---

## 反模式（Anti-Patterns）

- ❌ 未经成熟度检查直接执行
- ❌ apply=false 时修改任何文件
- ❌ git 工作区有未提交变更时执行 apply=true（应先 commit 保存现场）
- ❌ 摘要省略遗留缺口（历史决策的债务必须传递到后续里程碑）
- ❌ 仅生成摘要不折叠 roadmap.md（两者必须同步）
- ❌ 删除任务目录前未完成全仓引用更新

---

## 自检清单

**执行前**：

- [ ] 成熟度条件至少一条满足
- [ ] git 工作区干净（apply=true 时）
- [ ] 摘要模板字段完整（完成日期 / 交付物 / 缺口 / ADR）

**执行后（apply=true）**：

- [ ] `_archive/{slug}-summary.md` 存在且内容完整
- [ ] roadmap.md 阶段段落已折叠为 ≤ 3 行
- [ ] 全仓 grep `milestones/{slug}/tasks.md` 无结果
- [ ] `milestones/{slug}/` 目录不存在

---

## 示例（Examples）

### 示例 1：常规场景 — M3 完成后归档

**输入**：
- `docs/process-management/milestones/m3/` 含完成 60 天的 tasks.md（全部 status=completed）
- `roadmap.md` M3 阶段标记 ✅
- 后续里程碑 M4 已开始

**执行**（dry-run 默认）：
1. 成熟度检查：M3 完成日 ≥ 60 天 ✓，后续里程碑索引差 ≥ 1 ✓
2. 生成快照 `milestones/_archive/m3-summary.md`：完成日、5 条关键交付物、关键 ADR 引用
3. 给出影响分析：roadmap M3 节将折叠为 3 行；当前路径 `milestones/m3/` 将删除
4. 输出 dry-run 报告等待用户确认

**Apply 后**：roadmap.md M3 段折叠完成、`milestones/_archive/m3-summary.md` 生成、`milestones/m3/` 移除。

### 示例 2：边界场景 — 里程碑刚完成但成熟度不够

**输入**：M5 完成日仅 14 天，M6 尚未启动。

**执行**：
1. 成熟度检查：完成日 < 60 天 且 后续里程碑索引差 = 0
2. 拒绝执行：输出"里程碑尚未成熟（14 天 < 60 天阈值；后续里程碑未启动），建议在 ≥60 天后或 M6 启动后再归档"
3. 不生成快照、不修改 roadmap

**结果**：保留 M5 现状；用户可在条件满足后重新运行。
