---
artifact_type: guide
created_by: ai-cortex
lifecycle: living
created_at: 2026-05-09
status: active
---

# 文档创建决策指引

> 该不该创建一份新 markdown 文档？放哪儿？本指引用决策树回答。
>
> 配套：约束清单见 [rules/workflow-documentation.md](../../rules/workflow-documentation.md)。

---

## 决策树

创建任何新 `.md` 之前自问以下 4 个问题：

1. **是否需要持续维护？**
   - 是 → 进入问题 2
   - 否 → 不创建文档；用 commit message、PR description、Issue 评论或临时笔记

2. **该主题是否已存在权威文档？**
   - 是 → 不新建；更新已有文档或添加引用链接
   - 否 → 进入问题 3

3. **是否有 ≥ 3 个用户/Agent 会消费这份文档？**
   - 是 → 进入问题 4
   - 否 → 考虑用 Wiki / 内部笔记 / Slack pin 替代

4. **文档生命周期是什么？**
   - 长期（living）→ 创建在正式目录（`docs/architecture/`、`docs/guides/` 等），完整 frontmatter
   - 短期（snapshot）→ 必须命名为 `*.draft.md` 或 `YYYY-MM-DD-主题.md`，放专门目录（`docs/design/`、`experiments/`、`meetings/`），并设定清理时间

---

## 路径速查

| 内容性质 | 推荐路径 |
|----|----|
| 架构决策记录 | `docs/adr/NNNN-{topic}.md` |
| 设计文档 | `docs/designs/YYYY-MM-DD-{slug}.md` |
| 长期使用指引 | `docs/guides/{slug}.md` |
| 参考资料 | `docs/references/{slug}.md` |
| 草稿 / 未定稿 | `<最终位置>.draft.md` |
| 临时讨论笔记 | `experiments/`、`meetings/` 等专门目录 |

---

## 反模式

- ❌ 创建 `SUMMARY.md`、`COMPLETE_REFACTOR.md`、`REVIEW_2024.md` 这类无明确生命周期的总结文档
- ❌ 在多个 README 中复制相同安装步骤（应有唯一权威 + 引用）
- ❌ 把临时讨论放在 `docs/` 顶级（污染正式文档区）
- ❌ 把版本变更记录写进新文档（应进 CHANGELOG.md）

---

## 相关

- 约束清单：[rules/workflow-documentation.md](../../rules/workflow-documentation.md)
- 文档制品命名与路径：[docs/architecture/terminology.md](../architecture/terminology.md)
