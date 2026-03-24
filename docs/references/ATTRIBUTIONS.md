---
artifact_type: reference
created_by: ai-cortex
lifecycle: living
created_at: 2026-03-24
status: active
---

# 参考来源与致谢

<!-- markdownlint-disable MD058 MD060 -->

本文件枚举 AI Cortex 技能中 `metadata.evolution.sources` 引用的外部仓库与技能，供许可合规与溯源使用。详见 [LICENSE_POLICY.md](./LICENSE_POLICY.md)。

---

## 按仓库

| 仓库 | 来源技能 | 版本 | 许可证 | 类型 | 借用内容 | 使用方 |
| --- | --- | --- | --- | --- | --- | --- |
| [anthropics/skills](https://github.com/anthropics/skills) | commit-work | 1.0.0 | MIT | fork | Core workflow, Conventional Commits format, patch staging approach | commit-work |
| [jwynia/agent-skills](https://github.com/jwynia/agent-skills) | requirements-analysis | 1.0.0 | MIT | fork | Diagnostic state model (RA0-RA5), problem-first methodology, anti-patterns, cons... | analyze-requirements |
| [nesnilnehc/ai-cortex](https://github.com/nesnilnehc/ai-cortex) | align-execution | 1.0.0 | MIT | reference | Drift model, traceback pattern, report template structure | align-architecture |
| [nesnilnehc/ai-cortex](https://github.com/nesnilnehc/ai-cortex) | analyze-requirements | 1.0.0 | MIT | reference | State-based validation style, handoff boundaries, structured self-check | align-planning |
| [nesnilnehc/ai-cortex](https://github.com/nesnilnehc/ai-cortex) | design-solution | 1.0.0 | MIT | reference | Phase-based process, alternatives framing, output artifact discipline | align-planning |
| [nesnilnehc/ai-cortex](https://github.com/nesnilnehc/ai-cortex) | design-solution | 1.0.0 | MIT | reference | Phase-based workflow, HARD-GATE pattern, incremental dialogue approach | analyze-requirements |
| [nesnilnehc/ai-cortex](https://github.com/nesnilnehc/ai-cortex) | review-diff | 1.3.0 | MIT | integration | Pre-commit review methodology | commit-work |
| [nesnilnehc/ai-cortex](https://github.com/nesnilnehc/ai-cortex) | design-solution | 1.0.0 | MIT | reference | Phase-based validation, HARD-GATE, trade-off framework, design doc structure | design-solution |
| [nesnilnehc/gstack](https://github.com/nesnilnehc/gstack) | retro | 2.0.0 | MIT | fork | Git-based metrics, per-author breakdown, praise and growth framing, commit type ... | conduct-retro |
| [nesnilnehc/gstack](https://github.com/nesnilnehc/gstack) | investigate | 1.0.0 | MIT | fork | Four-phase workflow, Iron Law, pattern analysis table, hypothesis testing rules,... | investigate-root-cause |
| [nesnilnehc/gstack](https://github.com/nesnilnehc/gstack) | document-release | 1.0.0 | MIT | fork | Post-ship doc audit workflow, per-file heuristics, CHANGELOG polish rules, cross... | sync-release-docs |
| [nesnilnehc/gstack](https://github.com/nesnilnehc/gstack) | careful | 0.1.0 | MIT | fork | Destructive pattern list, safe exceptions, warn-before-run behavior | warn-destructive-commands |
| [staruhub/ClaudeSkills](https://github.com/staruhub/ClaudeSkills) | request-analyzer | 1.0.0 | MIT | integration | Structured quality assessment (clarity/specificity/completeness), decision matri... | analyze-requirements |

---

## 备注

- **anthropics/skills**：上游仓库根目录未检出 LICENSE 文件；按惯例声明 MIT，建议定期复核。
- **jwynia/agent-skills**：GitHub API 未检测到仓库级 license；skills 目录下技能可能单独声明，建议定期复核。
- **nesnilnehc/ai-cortex**：本仓库内部引用。
