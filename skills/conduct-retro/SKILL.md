---
name: conduct-retro
description: Weekly or sprint engineering retrospective. Analyzes commit history, work patterns, and code quality metrics. Team-aware: per-person contributions with praise and growth areas. Use when asked to "weekly retro", "what did we ship", or "engineering retrospective".
description_zh: 周/迭代工程回顾：分析提交历史、工作模式与代码质量指标；按人分解贡献，含表扬与成长建议。适用于「周回顾」「发了什么」「工程复盘」。
tags: [workflow, documentation]
version: 1.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
  evolution:
    sources:
      - name: "retro"
        repo: "https://github.com/nesnilnehc/gstack"
        version: "2.0.0"
        license: "MIT"
        type: "fork"
        borrowed: "Git-based metrics, per-author breakdown, praise and growth framing, commit type analysis, hotspot detection"
    enhancements:
      - "Platform-agnostic: base branch from project config, no gstack binaries"
      - "Output to docs/calibration/ per artifact-contract"
      - "Removed global mode, telemetry, Greptile, skill usage"
triggers: [retro, weekly retro, engineering retrospective, what did we ship]
input_schema:
  type: free-form
  description: Optional time window (7d, 14d, 30d); default 7d
output_schema:
  type: document-artifact
  description: Retrospective report with metrics, per-author breakdown, praise, growth areas
  artifact_type: retro-report
  path_pattern: docs/calibration/YYYY-MM-DD-retro.md
  lifecycle: snapshot
---

# 技能 (Skill)：工程回顾

## 目的 (Purpose)

通过分析 Git 提交历史、工作模式与代码质量指标，产出周或迭代的工程回顾报告；支持多人协作时的按人分解，含表扬与成长建议，与 `align-planning` 互补（后者关注规划对齐，本技能关注交付复盘）。

---

## 核心目标（Core Objective）

**首要目标**：产出一份可读的工程回顾报告，包含聚合指标、按人贡献分解、表扬与成长建议，并持久化到 `docs/calibration/`。

**成功标准**（必须满足所有要求）：

1. ✅ **基准分支已检测**：从 CLAUDE.md、`.ai-cortex/config.yaml` 或 `gh repo view` 获取 base branch；参见 [docs/guides/project-config.md](../../docs/guides/project-config.md)
2. ✅ **时间窗口已解析**：支持 `7d`（默认）、`14d`、`30d`；使用 midnight-aligned 起止日期
3. ✅ **Git 数据已收集**：commits、LOC、contributors、commit 类型、热点文件
4. ✅ **指标与按人分解**：计算 commits、insertions/deletions、test ratio、活跃天数；每名贡献者含表扬 1–2 项、成长建议 1 项
5. ✅ **报告已持久化**：写入 `docs/calibration/YYYY-MM-DD-retro.md`；语气鼓励但坦诚，表扬具体、成长建议以投资视角表述

**验收测试**：队友能否阅读报告并清楚了解本周/本迭代发了什么、谁贡献了什么、哪些做得好、可改进之处？

---

## 范围边界（Scope Boundaries）

**本技能负责**：

- 基于 Git 的交付指标分析
- 按人贡献分解与表扬/成长建议
- 回顾报告持久化

**本技能不负责**：

- 规划与执行对齐（使用 `align-planning`）
- 文档健康评估（使用 `assess-docs`）
- 跨项目/跨工具聚合（无全局模式）

**转交点**：报告产出后，可移交 `align-planning` 做规划校准，或由团队基于报告讨论后续行动。

---

## 使用场景（Use Cases）

- 周/迭代结束时的工程复盘
- 用户问「这周发了什么」「我们 ship 了多少」
- 团队协作时需按人反馈
- 交付节奏与质量趋势观察

---

## 行为（Behavior）

### 前置：解析参数与检测 base branch

1. **时间窗口**：默认 `7d`；支持 `14d`、`30d`。计算 midnight-aligned 起止日期（如 7d：`--since="YYYY-MM-DDT00:00:00"`）。
2. **base branch**：优先从 CLAUDE.md、`.ai-cortex/config.yaml` 读取 `base_branch`；否则 `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`；失败则 `main`。

### Step 1：收集 Git 数据

```bash
# Commits with author, date, subject, stats
git log origin/<base> --since="<start>T00:00:00" --format="%H|%aN|%ae|%ai|%s" --shortstat

# Per-author commit counts
git shortlog origin/<base> --since="<start>T00:00:00" -sn --no-merges

# Numstat for test vs prod LOC
git log origin/<base> --since="<start>T00:00:00" --format="COMMIT:%H|%aN" --numstat

# Hotspot files
git log origin/<base> --since="<start>T00:00:00" --format="" --name-only | grep -v '^$' | sort | uniq -c | sort -rn

# Commit timestamps for session/peak analysis
git log origin/<base> --since="<start>T00:00:00" --format="%at|%aN|%ai|%s" | sort -n
```

若在 base branch 上，先 `git fetch origin <base>`。使用 `origin/<base>` 而非本地 branch。

### Step 2：计算指标

| Metric | 说明 |
|--------|------|
| Commits to main | 窗口内 commit 数 |
| Contributors | 贡献者数量 |
| Total insertions/deletions | 增删行数 |
| Net LOC | 净增行 |
| Test LOC ratio | 测试文件增行 / 总增行（估算） |
| Active days | 有 commit 的天数 |
| Commit type mix | feat/fix/refactor/test/chore/docs 占比 |

### Step 3：按人分解

对每名贡献者：commits、LOC、主要变更目录（top 3）、commit 类型占比。

**当前用户**：从 `git config user.name` 识别，标注为「你」；给予最详尽的个人复盘。

**队友**：
- **表扬**：1–2 项具体、有据（锚定实际 commit）
- **成长建议**：1 项具体、建设性；以投资视角表述

### Step 4：热点与模式

- Top 10 最常变更文件
- fix 占比 >50% 时提示：可能反映 review 缺口
- 测试比例过低时提示：建议加强测试

### Step 5：持久化报告

写入 `docs/calibration/YYYY-MM-DD-retro.md`，其中 YYYY-MM-DD 为报告日期。结构：

```markdown
# Engineering Retro: [date range]

## Summary
[Tweetable one-liner]

## Metrics
[Table]

## Per-Author Breakdown
### You (name)
...
### [Teammate]
- Praise: ...
- Growth: ...

## Hotspots & Patterns
...

## Suggestions for Next Period
...
```

---

## 输入与输出 (Input & Output)

### 输入

- 可选：时间窗口 `7d`、`14d`、`30d`（默认 7d）

### 产出

- `docs/calibration/YYYY-MM-DD-retro.md` 回顾报告
- 输出到对话的摘要（Tweetable 与核心指标）

---

## 限制（Restrictions）

### 硬边界

- 需在含 `.git` 的仓库内运行
- 使用 `origin/<base>` 的远程数据，不依赖本地未 push 的 commit

### 技能边界 (Skill Boundaries)

**不要做这些（其他技能可以处理它们）**：

- **规划对齐**：使用 `align-planning`
- **文档评估**：使用 `assess-docs`

---

## 自检（Self-Check）

### 成功标准

- [ ] base branch 已正确检测
- [ ] 时间窗口已正确解析
- [ ] Git 数据已收集
- [ ] 指标已计算
- [ ] 按人分解含表扬与成长建议
- [ ] 报告已写入 `docs/calibration/`

### 验收测试

队友能否从报告中清楚了解本周/本迭代的交付情况与反馈？

---

## 示例（Examples）

### 示例 1：默认 7 天回顾

**输入**：`conduct-retro` 或 `conduct-retro 7d`  
**输出**：过去 7 天的指标、按人分解、报告写入 `docs/calibration/2026-03-23-retro.md`。

### 示例 2：14 天回顾

**输入**：`conduct-retro 14d`  
**输出**：过去 14 天的回顾报告。
