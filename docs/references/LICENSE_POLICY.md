---
artifact_type: reference
created_by: ai-cortex
lifecycle: living
created_at: 2026-03-24
status: active
---

# 许可证策略

本文件定义 AI Cortex 原创 Skills 与外部派生 Skills 的许可证和通知要求。

## 1. 原创 Skill

- AI Cortex 原创 `skills/*/SKILL.md` 默认声明 `license: MIT`。
- 仓库根 [`LICENSE`](../../LICENSE) 覆盖 AI Cortex 原创内容，不覆盖另有明确许可证的 vendored 内容。

## 2. 外部派生 Skill

- 所有外部派生 Skill 必须作为审核后的本地副本进入 `skills/`，并登记在 [`skills/SOURCES.yaml`](../../skills/SOURCES.yaml)。
- 来源必须固定到完整 commit、Git tree 和 `SKILL.md` SHA-256；不得以 branch、tag、`latest` 或 raw URL 作为发布依据。
- 只接受明确允许复制、修改和再分发的许可证。MIT、Apache-2.0、BSD-2-Clause、BSD-3-Clause 可进入评审；未发现许可证或许可证不明确时不得 vendor。
- Skill frontmatter 的 `license` 必须反映该本地副本实际适用的 SPDX license expression，不得为统一外观把 Apache-2.0 派生内容标成 MIT。
- 必须保留上游要求的版权与许可证文本；集中通知见 [THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md)，完整许可证可随 Skill 保存为 `LICENSE.upstream`。

## 3. 维护与发布

- 上游检查和更新只发生在维护期，经过 diff、许可证、脚本和资产复核后合并；Agent 运行时不得安装或升级外部 Skill。
- 从 `skills/SOURCES.yaml`、本地文件和许可证通知生成 SPDX；SPDX 是发布审计产物，不替代来源清单或更新流程。
- 删除外部派生 Skill 时同步删除来源登记、无其他使用者的许可证副本和通知条目；Git 历史保留旧版本溯源。

## 4. 参考

- [skill-source-modeling.md](../../specs/skill-source-modeling.md)：来源清单数据契约
- [ATTRIBUTIONS.md](./ATTRIBUTIONS.md)：当前外部派生 Skill 人工索引
- [THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md)：许可证与版权通知
