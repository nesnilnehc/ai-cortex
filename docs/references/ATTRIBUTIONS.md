---
artifact_type: reference
created_by: ai-cortex
lifecycle: living
created_at: 2026-03-24
status: active
---

# 参考来源与致谢

<!-- markdownlint-disable MD058 MD060 -->

本文件是 [`skills/SOURCES.yaml`](../../skills/SOURCES.yaml) 的人工可读索引，枚举 AI Cortex 当前分发的外部派生 Skill。详见 [LICENSE_POLICY.md](./LICENSE_POLICY.md)。

---

## 按仓库

| 仓库 | 上游路径 | 固定 commit | 许可证 | 本地 Skill | 本地处理 |
| --- | --- | --- | --- | --- | --- |
| [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) | `skills/commit-work` | `06825f04669d4364a16abc267650c86cf153d349` | MIT | `commit-work` | 保留提交工作流，集成 AI Cortex review、INDEX 和输出契约 |
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | `.agents/skills/changelog-video` | `4f00336c92f6418aab82c060853da604dd832197` | Apache-2.0 | `changelog-video` | 改为 Release Package 输入，移除品牌资产、固定语音、仓库路径和 sibling-skill 依赖 |

---

## 备注

- 历史记录曾把 `commit-work` 来源写成未经验证的 `anthropics/skills (assumed)`；当前表以可核验且内容匹配的 `softaworks/agent-toolkit` 为准。
- skills.sh 页面只用于发现，不是 AI Cortex 的安装或更新来源。
- 完整 digest、修改列表和更新策略以 `skills/SOURCES.yaml` 为准。
