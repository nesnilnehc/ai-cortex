---
artifact_type: execution-plan
created_by: ai-cortex
lifecycle: living
created_at: 2026-03-24
status: active
---

# 推广渠道清单 (Promotion Channel Checklist)

**来源:** [promotion-and-iteration design](../designs/2026-03-06-promotion-and-iteration.md)、[requirements](../requirements-planning/promotion-and-iteration.md) R-01  
**更新频率:** 每季度检视  
**负责人:** Maintainer

**权威位置:** 本清单为推广渠道的唯一权威来源；其他文档仅保留链接或摘要。

---

## 渠道 1：skills.sh

| 动作 | 频率 | 验收标准 | 本季度执行 |
| :--- | :--- | :--- | :---: |
| 确保 `npx skills add nesnilnehc/ai-cortex` 可安装 | 随版本发布 | `npx skills add nesnilnehc/ai-cortex -y` 返回 0 | ☑ |
| README 含 install 指引 | 随文档更新 | 含 npx 命令、`--force`、按 skill 安装 | ☑ |

**验证命令：** `npx skills add nesnilnehc/ai-cortex -y`（需网络，-y 免交互便于脚本验证）

---

## 渠道 2：Raw 链接可用性

| 动作 | 频率 | 验收标准 | 本季度执行 |
| :--- | :--- | :--- | :---: |
| 可选校验 README、AGENTS、manifest、INDEX 的 Raw URL 可访问 | 随版本发布 | HTTP 200 | ☑ |

**验证命令：** `node scripts/verify-links.mjs`

**Raw 根地址：** `https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/`

| 文件 | Raw URL | 状态 |
| :--- | :--- | :--- |
| README.md | <https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/README.md> | 200 ✓ |
| AGENTS.md | <https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/AGENTS.md> | 200 ✓ |
| manifest.json | <https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/manifest.json> | 200 ✓ |
| skills/INDEX.md | <https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/skills/INDEX.md> | 200 ✓ |

---

## 渠道 3：SkillsMP / Claude Plugin

| 动作 | 频率 | 验收标准 | 本季度执行 |
| :--- | :--- | :--- | :---: |
| marketplace.json 与 INDEX 一致 | 随技能发布 | verify-registry.mjs 通过 | ☑ |
| 符合 D9 的技能纳入 marketplace | 随技能发布 | ASQM ≥ 18、非原子 review、独立使用价值 | ☑ |

**验证命令：** `node scripts/verify-registry.mjs`

---

## 渠道 4：README / AGENTS 可分享素材

| 动作 | 频率 | 验收标准 | 本季度执行 |
| :--- | :--- | :--- | :---: |
| README 含 Raw 链接、定位、install 指引 | 随文档更新 | 可直接复用到其他项目 | ☑ |
| AGENTS.md 含入口约定、加载约束（默认本地优先、外链不作为依赖） | 随文档更新 | 可被 Agent 加载 | ☑ |
| 版本与 CHANGELOG 一致 | 随版本发布 | README badge、manifest version 同步 | ☑ |

---

## 本季度执行记录

| 执行日期 | 渠道 | 结果 | 备注 |
| :--- | :--- | :--- | :--- |
| 2026-03-06 | 2 Raw 链接 | ✓ 全部 200 | `verify-links.mjs` 通过 |
| 2026-03-06 | 3 marketplace | ✓ Registry OK | `verify-registry.mjs` 通过 |
| 2026-03-06 | 4 文档 | ✓ 就绪 | README 2.1.0、AGENTS 本地入口、版本同步 |
| 2026-03-06 | 1 skills.sh | ✓ 通过 | `npx skills add nesnilnehc/ai-cortex -y` 返回 0 |
