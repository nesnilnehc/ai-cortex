# 推广与迭代 — 任务拆解与质量门禁

**Date:** 2026-03-06
**Source:** [requirements](../requirements-planning/promotion-and-iteration.md)、[design](../designs/2026-03-06-promotion-and-iteration.md)

**文档关系**：
- [backlog.md (index)](backlog.md)：Epic 快速导航
- [设计文档 (design)](../designs/2026-03-06-promotion-and-iteration.md)：设计决策与背景
- 本文档：Epic T1-T5 的**执行详情**，包含完整的任务定义、验收标准、质量门禁和依赖关系

---

## 总览

| Epic | 任务数 | 依赖 | 质量门禁 |
| :--- | :--- | :--- | :--- |
| T1 分发渠道验证 | 3 | 无 | QG-1 |
| T2 发布流程自动化 | 3 | T1 | QG-2 |
| T3 指标采集与报告 | 3 | 无 | QG-3 |
| T4 CI 集成 | 2 | T1, T2 | QG-4 |
| T5 季度检视流程 | 1 | T3 | QG-5 |

---

## Epic T1：分发渠道验证

### T1.1 skills.sh 安装验证脚本

**目标**：脚本可验证 `npx skills add nesnilnehc/ai-cortex` 是否成功。

| 项目 | 内容 |
| :--- | :--- |
| **产出** | `scripts/verify-install.mjs` 或等效脚本 |
| **验收标准** | ① 脚本在干净环境执行 `npx skills add nesnilnehc/ai-cortex` ② 成功时 exit 0，失败时 exit 1 ③ 输出包含 install 成功/失败及错误信息 ④ README 或脚本内注明运行前提（Node.js 版本、网络） |
| **依赖** | 无 |
| **质量门禁** | QG-1：脚本无硬编码 secrets；可在本地复现 |

### T1.2 Raw 链接可用性验证

**目标**：验证 INDEX、manifest、AGENTS、README 等 Raw URL 可访问。

| 项目 | 内容 |
| :--- | :--- |
| **产出** | `scripts/verify-links.mjs` 或扩展现有 `verify-registry.mjs` |
| **验收标准** | ① 检测 `https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/` 下关键文件（README.md、AGENTS.md、manifest.json、skills/INDEX.md） ② HTTP 200 视为通过 ③ 输出通过/失败清单 ④ 可配置 base URL 便于 fork 复用 |
| **依赖** | 无 |
| **质量门禁** | QG-1：非阻塞（网络故障不阻塞 CI，可标记为 warning） |

### T1.3 Plugin / marketplace 一致性验证

**目标**：marketplace.json 与 INDEX 一致（已有 verify-registry 覆盖则标记为完成）。

| 项目 | 内容 |
| :--- | :--- |
| **产出** | 确认 `verify-registry.mjs` 已覆盖 marketplace 校验；若未覆盖则补齐 |
| **验收标准** | ① marketplace 中每个 skill 均存在于 skills/ 且已入 INDEX ② INDEX 中符合 D9 的 skill 在 marketplace 中（或明确排除原因） ③ 脚本输出差异报告 |
| **依赖** | 无 |
| **质量门禁** | QG-1：与现有 verify-registry 行为一致，无回归 |

---

## Epic T2：发布流程自动化

### T2.1 发布前检查清单脚本

**目标**：一键执行所有发布前校验。

| 项目 | 内容 |
| :--- | :--- |
| **产出** | `scripts/pre-release-check.mjs`，串联 verify-registry、verify-skill-structure、verify-links、verify-install（可选） |
| **验收标准** | ① 单命令执行全部校验 ② 失败时汇总错误并 exit 1 ③ 文档说明用法及失败处理 |
| **依赖** | T1.1, T1.2, T1.3 |
| **质量门禁** | QG-2：全部子脚本通过时，本脚本必须通过 |

### T2.2 CHANGELOG / Release Notes 生成辅助

**目标**：从 CHANGELOG 或 commits 生成 Release Notes 草稿，供人工审核后发布。

| 项目 | 内容 |
| :--- | :--- |
| **产出** | 文档或简单脚本：说明如何从 CHANGELOG [Unreleased] 提取内容生成 GitHub Release 描述 |
| **验收标准** | ① 流程可重复 ② 输出格式符合 GitHub Release 常用结构 ③ 人工审核为必经步骤 |
| **依赖** | 无 |
| **质量门禁** | QG-2：不自动发布；仅生成草稿 |

### T2.3 文档与版本同步检查

**目标**：检测 README、AGENTS、manifest 中的版本号与 CHANGELOG / tag 一致性。

| 项目 | 内容 |
| :--- | :--- |
| **产出** | `scripts/verify-version-sync.mjs` 或扩展现有脚本 |
| **验收标准** | ① 比较 manifest.json version、README 中版本引用与 CHANGELOG 最新版本 ② 不一致时输出警告 ③ 可选：检查 README install 命令是否指向最新 tag |
| **依赖** | 无 |
| **质量门禁** | QG-2：警告不阻塞，可作为 release 前提醒 |

---

## Epic T3：指标采集与报告

### T3.1 技能数与 Spec 采纳率统计

**目标**：脚本输出技能总数、符合 spec 的占比。

| 项目 | 内容 |
| :--- | :--- |
| **产出** | 扩展现有 verify 脚本或独立 `scripts/metrics-skills.mjs` |
| **验收标准** | ① 输出 JSON 或表格：技能数、spec 通过数、采纳率 ② 可被 CI 或季度报告消费 ③ 与 verify-skill-structure 判定逻辑一致 |
| **依赖** | 无 |
| **质量门禁** | QG-3：结果可复现；无外部依赖（仅读本地文件） |

### T3.2 分发渠道可用性报告

**目标**：汇总 T1 各验证结果，输出可用性报告。

| 项目 | 内容 |
| :--- | :--- |
| **产出** | `scripts/report-distribution.mjs` 或复用 T2.1 输出格式 |
| **验收标准** | ① 输出 skills.sh、Raw links、marketplace 的通过/失败状态 ② 可写入文件供季度检视 ③ 时间戳与执行环境可记录 |
| **依赖** | T1 |
| **质量门禁** | QG-3：网络类检查失败时明确标注为「不可用」而非误报 |

### T3.3 季度指标报告模板

**目标**：定义季度检视时需填写的指标模板。

| 项目 | 内容 |
| :--- | :--- |
| **产出** | `docs/process-management/quarterly-metrics-template.md` |
| **验收标准** | ① 包含：技能数、spec 采纳率、分发渠道状态、文档就绪、推广动作执行情况 ② 每项有「基准」「目标」「实际」三列 ③ 与 design 中成功指标定义一致 |
| **依赖** | 无 |
| **质量门禁** | QG-3：模板可被人工填写，无需自动采集的项标注为「手动」 |

---

## Epic T4：CI 集成

### T4.1 PR 检查工作流

**目标**：PR 时自动运行 verify-registry、verify-skill-structure；可选 run verify-links。

| 项目 | 内容 |
| :--- | :--- |
| **产出** | `.github/workflows/pr-check.yml`（若尚未存在）或更新现有 workflow |
| **验收标准** | ① PR 到 main 时触发 ② verify-registry、verify-skill-structure 必须通过 ③ verify-links 可选（网络依赖可标记为 best-effort） ④ 使用项目 generate-github-workflow 技能生成或符合其输出约定 |
| **依赖** | T1, T2 |
| **质量门禁** | QG-4：不暴露 secrets；权限最小化；workflow 可本地复现 |

### T4.2 发布/审计工作流

**目标**：main 合并或 tag 时运行完整 pre-release-check；可按需触发 ASQM 审计。

| 项目 | 内容 |
| :--- | :--- |
| **产出** | `.github/workflows/release-check.yml` 或扩展现有 audit workflow |
| **验收标准** | ① 在 push tag 或 release 创建时触发 ② 运行 pre-release-check ③ 失败时阻止或标记 release ④ 可选：触发 curate-skills 或 ASQM 审计 |
| **依赖** | T2.1 |
| **质量门禁** | QG-4：与 pr-check 权限隔离；避免重复运行 |

---

## Epic T5：季度检视流程

### T5.1 季度检视 SOP

**目标**：定义每季度执行的检视步骤与产出。

| 项目 | 内容 |
| :--- | :--- |
| **产出** | `docs/process-management/quarterly-review-sop.md` |
| **验收标准** | ① 步骤包含：运行指标脚本、填写季度模板、更新 milestones、更新推广设计文档 ② 产出：更新后的 milestones、推广清单执行记录 ③ 可 15 分钟内完成（不含人工判断时间） |
| **依赖** | T3 |
| **质量门禁** | QG-5：SOP 与 quarterly-metrics-template 一致；无歧义 |

---

## 质量门禁总表

| ID | 名称 | 适用 Epic | 门禁条件 |
| :--- | :--- | :--- | :--- |
| QG-1 | 脚本安全与可复现 | T1 | 无硬编码 secrets；可本地执行；网络类检查失败不误报为逻辑错误 |
| QG-2 | 发布流程可控 | T2 | 不自动发布到生产；人工审核为必经步骤；子脚本通过则串联通过 |
| QG-3 | 指标可审计 | T3 | 指标定义与 design 一致；可复现；需手动项明确标注 |
| QG-4 | CI 安全与幂等 | T4 | 最小权限；无 secrets 泄露；workflow 可本地等效复现 |
| QG-5 | 流程一致性 | T5 | SOP 与模板、设计文档一致；无矛盾 |

---

## 验收标准汇总（按需求追溯）

| 需求 ID | 相关任务 | 验收通过条件 |
| :--- | :--- | :--- |
| R-01 推广策略可执行 | T5.1 | 季度 SOP 包含推广渠道清单执行；每季度至少检视一次 |
| R-02 迭代计划可追溯 | 已有 milestones | milestones 与 roadmap 对应；本任务拆解可追溯到 design |
| R-03 成功指标可度量 | T3.1, T3.2, T3.3 | 至少 3 个指标可采集或填写；有基准与目标 |
| R-04 设计文档已落稿 | 已完成 | 需求与设计文档已存在 |
| R-05 社区基础设施 | 已有 | CONTRIBUTING、Issue 模板已存在 |
| R-06 推广素材可复用 | T2.2, T2.3 | README/AGENTS 随版本更新；版本同步可验证 |

---

## 建议执行顺序

1. **Phase A（基础）**：T1.1, T1.2, T1.3 → T2.1
2. **Phase B（度量）**：T3.1, T3.2, T3.3
3. **Phase C（自动化）**：T4.1, T4.2
4. **Phase D（流程）**：T5.1

T2.2、T2.3 可与 Phase A 并行，优先级略低。
