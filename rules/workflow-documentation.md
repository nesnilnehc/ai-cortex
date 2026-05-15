---
artifact_type: rule
name: workflow-documentation
version: 1.0.0
scope: 所有新建或维护 .md 文档
recommended_scope: user
status: active
---

# Rule: 文档管理策略（Documentation Management）

## 适用范围 (Scope)

所有创建、命名或维护 Markdown 文档（`.md`）的行为，含产品文档（SKILL.md / agent.yaml / README / specs / 正文 *.md）与临时文档（设计稿、复盘、审计快照等）。

---

## 强制约束 (Constraints)

1. **最小化**：不为了记录思考过程而创建文档；产品文档不写讨论过程或版本演化痕迹（详见下方"临时文档判别"）
2. **DRY**：不在多个文档中重复相同内容；同一主题须有唯一权威文档，其他位置以引用方式接入
3. **用户导向**：只写解决实际问题的使用文档；不写面向过程的思考记录
4. **临时文档必须显式标识**：满足下方"临时文档判别"任一条件的文档，文件名必须含日期前缀或 `.draft` 后缀，并存放于专门目录（`docs/designs/`、`experiments/`、`meetings/` 等）
5. **变更记录归位**：版本变更进 `CHANGELOG.md`；改进记录进 Issue / PR；不另开新文档

---

## 临时文档判别（满足任一即是）

### 文件名形态

- 含 `SUMMARY` / `COMPLETE` / `FINAL` / `REVIEW` / `NOTES` / `UPDATES` / `OPTIMIZATION` 等纯总结性词汇
- 非以 `YYYY-MM-DD-` 开头且非以 `.draft.md` 结尾的过程性记录

### 正文形态

- **版本演化叙述**：`v\d+\.\d+ 起` / `v\d+\.\d+ 移除` / `v\d+\.\d+ 简化` / `v\d+\.\d+ 回撤` / `v\d+\.\d+ 引入`
- **节标题后缀**：`（新增）` / `（已废弃）` / `（v\d.\d 简化）` / `（v\d.\d 重写）`
- **过程词汇**：`废弃` / `vaporware` / `待建` / `历史` / `原本` / `回撤` / `沿用历史` / `本次新增`

### 例外（不视为临时文档）

- spec 文件顶部的"变更记录"小节（局部 CHANGELOG，公认惯例）
- ADR 自身的"背景 / 决策 / 替代方案 / 后果"叙述（其文体本质）
- `CHANGELOG.md` 通篇

---

## 违规示例 (Bad Patterns)

- 创建 `SUMMARY.md` / `COMPLETE_REFACTOR.md` / `REVIEW_2024.md`
- 在多个 README 中复制相同安装步骤而非引用
- 为一次重构过程新建"优化记录"文档，而非写进 CHANGELOG 或 commit
- 临时文档放在仓库根或正式 `docs/` 路径，未带 `.draft` 后缀或日期前缀
- SKILL.md / specs 正文出现 `v1.3 起 / 移除 / 简化` 等版本演化叙述

---

## Commit 前自检

stage 任意 markdown 文件前，对照本规则的"临时文档判别"清单 grep；命中即按"必须显式标识"约束处理（重命名 / 移到专门目录 / 删除版本演化痕迹挪到 ADR 或 CHANGELOG）。

---

## 相关指引

- 文档创建决策（"该不该创建？放哪儿？"）见 [docs/guides/document-decision-tree.md](../docs/guides/document-decision-tree.md)
- 仓库结构卫生约束见 [rules/repo-structure-hygiene.md](./repo-structure-hygiene.md)
- 文档健康判据（链接图、SSOT、对齐）见 [rules/doc-health-criteria.md](./doc-health-criteria.md)
