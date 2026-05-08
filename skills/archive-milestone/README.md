# archive-milestone

将已完成里程碑从活跃路径归档为快照摘要，折叠路线图历史阶段，防止历史文档污染 AI 对当前项目状态的判断。

## 何时调用

- `plan-next` 的卫生巡检（步骤 2.3）检测到未归档的已完成里程碑时
- 里程碑完成后 ≥ 60 天
- 当前进行中里程碑索引 ≥ 目标 + 2（如 M5 进行中，m3 满足，m4 不满足）
- tasks.md > 300 行且全部任务已完成

## 默认行为：dry-run

**不传 `apply` 参数时默认 dry-run**，只输出预览，不修改任何文件。这是安全默认值。

## 示例

### Dry-run（预览，推荐先执行）

```
/archive-milestone m3
```

或明确指定：

```
/archive-milestone m3 apply=false
```

输出示例：

```
=== dry-run 预览 ===

将生成：
  docs/process-management/milestones/_archive/m3-summary.md

  完成日期：2026-02-15
  关键交付物：
    - T31 QueryRouter 混合检索上线（commit abc123）
    - T32 BGE-M3 Embedding 接入（ADR-006 compliant）
    ...

将修改：
  roadmap.md 第 45-89 行折叠为：
    ### M3 混合检索基础设施（已完成 2026-02-15）→ 详见 [milestones/_archive/m3-summary.md]

将删除：
  docs/process-management/milestones/m3/（3 个文件，共 312 行）

引用更新（2 处）：
  docs/architecture/system-architecture.md:78 → 已更新
  docs/calibration/planning-alignment.md:34  → 已更新

=== 无文件已修改 ===
```

### Apply（确认执行）

**确认 dry-run 预览无误后**，传入 `apply=true`：

```
/archive-milestone m3 apply=true
```

执行前提：git 工作区无未提交变更（技能会主动检查）。

## 产出文件

| 文件 | 说明 |
|---|---|
| `milestones/_archive/{slug}-summary.md` | 快照摘要（lifecycle: snapshot） |

## 摘要结构

```markdown
---
artifact_type: milestone-summary
created_by: archive-milestone
lifecycle: snapshot
created_at: YYYY-MM-DD
milestone_slug: {slug}
completed_at: YYYY-MM-DD
---

# {里程碑名称} 归档摘要

## 关键交付物
...

## 遗留缺口
...

## 关键 ADR
...
```

## 不会执行

- 不自动执行（必须显式调用）
- dry-run 时不修改任何文件
- 不归档未达成熟度条件的里程碑
