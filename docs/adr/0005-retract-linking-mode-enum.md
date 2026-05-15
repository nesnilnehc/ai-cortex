---
artifact_type: adr
created_by: decision-record
lifecycle: snapshot
created_at: 2026-04-25
status: accepted
description: 回撤 linking_mode 枚举字段（认定为过度工程）
---

# ADR 0005：回撤 linking_mode 枚举字段（v8.0.0）

**上下文**：v7.0.0 发布次日用户连续三次质询 linking_mode 的必要性；回顾其他 AI 代理系统无同类设计；认定 v7.0 过度工程

## 背景

v7.0.0（ADR 004，2026-04-24）把 6 项链接模式（slug / colocation / parent-pointer / manifest / mixed / none）实现为 `ARTIFACT_NORMS.md` 的 `linking_mode` 枚举字段，由 `discover-docs-norms` Stage 2b 识别 + `define-docs-norms` Stage 1b 选择 UI + `plan-next` Step 2.5 消费协同完成闭环。v7.0 ship 后经进一步审视，三类问题浮现：

### 问题 1：与业界实践背离

考察主流 AI 代理系统（Cursor、Cline、Aider、Copilot Workspace、Claude Code 自身、Devin、MetaGPT 等），**没有任何系统把项目级跨制品链接约定形式化为 enum 选择字段**。普遍做法：

- LLM 语义推理 + `CLAUDE.md` / `AGENTS.md` 自然语言约定
- 文件名启发 + git 历史 + 目录邻近性
- 运行时每次会话推断（非持久化配置）
- 显式依赖声明（但在 task 级，非 project 级）

**洞察**：链接是**运行时发现问题**，不是**项目配置问题**。形式化强迫过早标准化，与真实开发节奏（约定会漂 / 有例外 / 处于迁移期）不符。

### 问题 2：6 模式都能用正交机制解决，枚举是多余的命名层

| 模式 | 实际需要的机制 | 是否需要 `linking_mode` 字段 |
|---|---|---|
| slug | 技能默认 `path_pattern` 含 `{topic}` | ❌ 已是默认 |
| colocation | 项目覆盖 `path_pattern` 为 `work/{slug}/<type>.md` | ❌ `path_pattern` 覆盖机制已足够 |
| parent-pointer | 技能收到 `upstream_ref` 输入时 emit `parent:` frontmatter | ❌ 条件 emit 已足够 |
| manifest | 项目建清单文件；消费者 glob 检测存在性 | ❌ 物理信号检测已足够 |
| mixed | 各种机制独立组合 | ❌ 无需"混合模式"字段 |
| none | 技能默认行为 | ❌ 无需表达"没有约定" |

**结论**：`linking_mode` 字段是**描述性 taxonomy 和实现机制之间的一层冗余抽象**。去掉它，三个正交机制（`path_pattern` 覆盖 / `upstream_ref` 输入 / manifest 物理文件）自然覆盖所有场景。

### 问题 3：Greenfield 用户获得负价值

新项目场景：`discover-docs-norms` 扫描无证据 → 报 `linking_mode: none, confidence 0`；用户被迫进入 `define-docs-norms` 从 6 选项中盲选。用户实际需要的是**决策支持**（每种约定适合什么场景），但工具给的是**审计报告 + 干巴巴菜单**。

审计（"当前实际怎么做"）和设计（"应该怎么做"）是两类活动，v7.0 把 linking_mode 当审计对象处理是类型错误——它是设计决策。

## 决策

### 决策 1：废弃 `linking_mode` 枚举字段

- `ARTIFACT_NORMS.md` 的 `linking_mode` 字段**移除**
- `specs/artifact-norms-schema.md` §6 标注废弃并提供迁移指南
- `specs/linking-modes.md` 降级为**描述性参考文档**（taxonomy 说明，非运行时配置）

### 决策 2：回撤 discover/define 的链接模式处理

- `discover-docs-norms` v3.0 → **v4.0**：移除 Stage 2b 链接模式识别；回归"路径 / 命名 / frontmatter / 生命周期"审计职责
- `define-docs-norms` v2.0 → **v3.0**：移除 Stage 1b 链接模式选择 UI；回归"固化已批准提案"抄写员职责

### 决策 3：回撤 plan-next 的 linking_mode 消费

- `plan-next` v7.0 → **v8.0**：Step 2.5 改为**按物理信号扫描**：
  - 层 1：resolved `path_pattern` glob（主要）
  - 层 2：`parent:` frontmatter 反向索引（可选增强）
  - 层 3：manifest 物理文件检测（可选增强）
- 三层独立运作可组合；不读 `linking_mode` 字段；不触发"先识别模式"前置闸门
- `norms_proposal_path` frontmatter 输入字段废弃（仅 v7.0 为读 proposal 的 linking_mode 而存在）

### 决策 4：保留 §8 Runtime Norms Resolution Protocol 的非模式部分

- §8.1 目的 / §8.2 发现顺序 / §8.3 占位符语法 / §8.5 合并语义 / §8.6 错误处理 / §8.7 校验钩子 **全部保留**——`path_pattern` 运行时覆盖机制是有价值的基础设施
- §8.4 Linking-mode 输出真值表 **简化**——不再分支 mode，只说"按 resolved path_pattern emit + 若提供 upstream_ref 则追加 parent: frontmatter"

### 决策 5：保留 `align-work-item-manifest`

新技能（v1.0.0 随 v7.0 shipped）v8.0 保留——它检测 manifest 物理文件的漂移，不依赖 `linking_mode` 字段（扫物理信号即可）。重新定位为"manifest-style 项目的可选审计技能"，适用范围独立于"项目是否声明 linking_mode"。

### 决策 6：版本统一 MAJOR bump

- `manifest.json` project version **3.0.0 → 4.0.0**
- `manifest.json` spec_version **3.0.0 → 4.0.0**
- `specs/artifact-contract.md` v3.0 → **v4.0**（§8.4 改写）
- `specs/artifact-norms-schema.md` v1.2 → **v2.0**（§6 废弃）
- `specs/linking-modes.md` v1.0 → **v2.0**（降级为描述性）
- `skills/discover-docs-norms` v3.0 → **v4.0**
- `skills/define-docs-norms` v2.0 → **v3.0**
- `skills/plan-next` v7.0 → **v8.0**

**链接锚点技能（v7.0 v2.0）不再 bump**——它们的 Stage 0 + `upstream_ref` 支持仍然有效，无需改动。

**固定路径技能（v7.0 MINOR）不再 bump**——它们的 Stage 0 path_pattern 覆盖支持仍然有效。

## 替代方案（已拒绝）

1. **保留 v7.0 全部设计不变**：拒。承认"过度工程"比 doubling down 更便宜；v7.0 ship 仅一天，用户未大规模依赖，撤回窗口最大。
2. **只修文案不动代码**：拒。把"模式选择"和"路径覆盖"混在一套接口里，长期认知负担；用户每次读文档都要消化两层抽象。
3. **保留字段但标 deprecated，v9 删除**：拒。字段没有合理使用场景，保留只会让新用户误用；一次清洁的断裂比长周期双轨维护便宜。
4. **只回撤 plan-next 不动 discover/define**：拒。discover 扫完输出没人读的字段、define 让用户选没人用的值，是独立的浪费。协同回撤。
5. **保留 linking_mode 但缩小为 1-2 个 enum 值**（如只保留 slug / manifest）：拒。既然所有模式都能用正交机制表达，枚举压缩到 2 项也没价值——**正交机制**本身是更好的抽象层。

## 后果

### 正面

- **认知负担显著降低**：用户不再需要学习 6 模式 enum；默认 slug 约定就是 AI Cortex canonical；自定义通过 `path_pattern` 覆盖直接表达
- **与业界实践对齐**：像 Cursor / Cline / Aider 一样依赖 `CLAUDE.md` + 物理信号 + LLM 推理，降低项目采用门槛
- **工具链更简洁**：discover 专注审计；define 专注抄写；plan-next 专注扫描；三者职责不重叠
- **正交能力更清晰**：`path_pattern` 覆盖 / `upstream_ref` 输入 / manifest 物理文件——三个独立机制组合出任何需要的行为
- **greenfield 用户零仪式**：新项目直接用默认，不需要先跑 discover→define

### 负面

- **v7.0 刚 ship 一天就回撤**：外部可能已有观察者注意到 v7.0，但未大规模采用；`v6.3-lts` + `v7.0.0` tag 都保留作参考
- **MAJOR bump 再次**：spec_version / project / 三个技能版本都升到 4.x / 3.x / 4.x / 3.x / 8.x
- **ADR 链条长**：ADR 002 → 003 → 004 → 005，读者需按序理解演化

### 中性

- **`specs/linking-modes.md` 降级为描述性文档**：保留 taxonomy 内容对沟通和审计有用，只是不再作为运行时配置对象
- **`align-work-item-manifest` 保留但重新定位**：从"manifest 模式的专职维护者"变为"manifest 风格项目的可选审计工具"——适用面不变

## 回滚策略

- 完整回到 v7.0：`git reset --hard v7.0-lts`（需要本次发布时打 tag）
- 完整回到 v6.3：`git reset --hard v6.3-lts`
- 部分回滚：Stage 0 是加法，任一技能可单独回到 pre-v7 版本；`path_pattern` 覆盖是纯加法；唯一不可逆的是 `manifest.spec_version` bump，故本次 bump 在所有改动通过 verify 后最后执行

## 参考

- ADR 004：规范驱动制品架构闭环（v7.0.0）——本 ADR 回撤其决策 1（§8.4 linking-mode 输出真值表）、决策 3 的 discover/define 部分、决策 4 的 manifest-only 定位
- ADR 003：plan-next v6.3 执行态 + 链接模式识别（源头引入 linking_mode 讨论）
- `specs/artifact-contract.md` v4.0
- `specs/linking-modes.md` v2.0（降级后）
- `specs/artifact-norms-schema.md` v2.0（§6 废弃后）
- `v6.3-lts` git tag（v7 前状态）
