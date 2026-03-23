# AGENTS.md 重构计划

**状态**：已完成  
**创建**：2026-03-23  
**目标**：将 AGENTS.md 从 ~120 行精简至 ~60–80 行，聚焦 Agent 在本仓库内工作时的入口契约。

---

## 1. 现状问题

| 问题 | 说明 |
| :--- | :--- |
| 过长 | 约 120 行，超过 generate-agent-entry 建议的 60–80 行 |
| 混入用户侧假设 | 发现与加载协议假定 intent-routing 会被注入，但设计上不要求注入用户环境 |
| 细则内嵌 | 匹配优先级、主动建议表等细则占篇幅，宜外迁 |
| 与 gstack 对比 | gstack AGENTS.md 约 50 行，以技能表 + 命令 + 约定为主，可读性更好 |

---

## 2. 重构原则

1. **受众单一**：仅面向 Agent 在本仓库内工作（迭代）时的行为契约；不含用户侧内容。
2. **精简**：只保留 Agent 必须知道的要素；细则放到链接文档。
3. **对齐 generate-agent-entry**：保持身份、权威、行为、参考表等结构，但压缩每节篇幅。
4. **参考 gstack**：技能表简洁、命令可执行、约定简短。

---

## 3. 目标结构（7 节，约 60–80 行）

| 节 | 内容 | 行数估计 |
| :--- | :--- | :---: |
| 1. 开场 | 一句定位：本文件是 Agent 与 AI Cortex 交互的入口契约；受众与范围见 docs/AUDIENCE_AND_SCOPE.md | 3–5 |
| 2. 项目身份 | 一行定位 + 资产表（Skill、目录、规范）；链接 mission/vision | 8–10 |
| 3. 权威来源 | 精简为 3–4 条：spec、INDEX/manifest、规则、原则；每项一行 + 链接 | 6–8 |
| 4. 行为预期 | 4 条编号，可执行（必须/应当/不得）；每条一句，可引用链接 | 8–10 |
| 5. 发现与自引用 | 一段摘要：资产根、发现（读 INDEX/manifest）、注入（SKILL 全文）、自引用（manifest capabilities）；细则见 docs/ 某文档 | 6–8 |
| 6. 语言与沟通 | 一句：中文优先，见 LANGUAGE_SCHEME | 2–3 |
| 7. 参考 | 表：Spec、Raw、规范、目录、自引用任务→技能映射（精简）、本地命令（verify、skill:check） | 15–20 |

---

## 4. 外迁内容

下列内容从 AGENTS.md 移除，迁至指定文档：

| 内容 | 迁往 | 说明 |
| :--- | :--- | :--- |
| 详细匹配优先级（intent、triggers、语义回退等） | docs/guides/discovery-and-loading.md（新建）或 intent-routing.md 补充 | 细则不必在入口展示 |
| 主动建议表（阶段→技能） | skills/intent-routing.md 或 docs/guides/proactive-suggestions.md | 表较长，单独维护 |
| 调用示例 | 保留 3 行精简版，或迁至 INDEX / intent-routing | 视最终篇幅决定 |
| 权威来源长列表 | 压缩为 3–4 条，详细列表放 AUDIENCE_AND_SCOPE 或新文档 | 避免重复 |
| 参考表中「自引用任务→资产」长句 | 精简为「自引用见 [INDEX](skills/INDEX.md)」+ 2–3 个典型映射 | 完整映射在 INDEX |

---

## 5. 新建或修订的配套文档

| 文档 | 操作 |
| :--- | :--- |
| docs/guides/discovery-and-loading.md | 新建：发现与加载细则（资产根、发现流程、匹配优先级、注入方式）；供需要时查阅 |
| skills/intent-routing.md | 可选：补充「主动建议」小节或链接；或保持现状 |
| docs/AUDIENCE_AND_SCOPE.md | 已存在；AGENTS 开场引用 |
| skills/generate-agent-entry/SKILL.md | 重构后需确认输出合约与本计划一致；必要时更新「目标 60–80 行」等说明 |

---

## 6. 验收标准

- [x] AGENTS.md 总行数 60–80 行（73 行）
- [x] 保留 7 节结构（开场、身份、权威、行为、发现、语言、参考）
- [x] 无用户侧内容（安装、用户使用说明等）
- [x] 细则已外迁至 docs/guides/discovery-and-loading.md、proactive-suggestions.md
- [x] 本地命令表保留 verify、skill:check 等迭代必需命令
- [x] 验证通过（verify、skill:check）
- [x] docs/AUDIENCE_AND_SCOPE.md 中 AGENTS 描述与本计划一致

---

## 7. 实施顺序

1. 新建 docs/guides/discovery-and-loading.md，迁移发现与加载细则
2. 新建或更新「主动建议」存放位置
3. 按目标结构重写 AGENTS.md
4. 更新 generate-agent-entry 输出合约（如必要）
5. 运行 verify、skill:check，确认无回归
6. 更新 AUDIENCE_AND_SCOPE 中 AGENTS 描述（如必要）
