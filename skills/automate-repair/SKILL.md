---
name: automate-repair
description: Iteratively review changes, run automated tests, and apply targeted fixes until issues are resolved (or a stop condition is reached).
description_zh: 迭代审查变更、运行自动化测试并实施定向修复，直至问题解决或满足停止条件。
tags: [automation, devops, optimization]
version: 1.1.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [repair, fix tests, delivery, stabilize, auto repair, auto fix, auto fix changes]
aliases: [run-repair-loop]
compatibility: Requires a shell and the repo's toolchains to run tests (language-dependent). May require git for diff-based review.
input_schema:
  type: code-scope
  description: Repository path and scope (diff or codebase) to converge to clean state
  defaults:
    scope: diff
output_schema:
  type: diagnostic-report
  description: Repair loop report with iterations, commands, patches, and final state (persist only if explicitly requested)
---

# 技能 (Skill)：运行修复循环（回顾+测试+修复）

## 目的 (Purpose)

通过运行 **多次迭代循环** 将代码库收敛或更改设置为“干净”：

1. **回顾**（及早发现问题并防止倒退），
2. **测试**（获取可执行信号），
3. **修复**（应用最小的正确补丁），
4. 重复直到**不再存在阻塞问题**或达到**停止条件**。

---

## 核心目标（Core Objective）

**首要目标**：使用有界的、证据驱动的审查-测试-修复循环，将存储库收敛到“干净”状态——所有测试都通过并且没有“关键”/“主要”审查结果。

**成功标准**（必须满足所有要求）：

1. ✅ **完成解析的定义**：在循环开始之前确认飞行前选择（范围、测试模式、最大迭代、允许的操作）
2. ✅ **每次迭代证据优先**：每次迭代至少产生以下之一：新的测试结果、新的审查信号或具体的代码更改
3. ✅ **修复后重新运行测试**：失败的测试命令（或目标子集）始终在同一迭代中应用修复后重新运行
4. ✅ **有界循环**：循环由于收敛或显式停止条件而终止 - 没有无限重试
5. ✅ **结构化最终报告**：输出包括修复循环报告（附录：输出合同），其中包含命令运行、故障、补丁和剩余风险

**验收**测试：最终报告是否显示（a）测试通过且没有阻止审查结果，或（b）明确的停止条件，并为用户提供明确的剩余问题和选项？

---

## 范围边界 (Scope Boundaries)

**本技能负责**：

- 多次迭代审查→测试→修复循环
- 使用“review-diff”和“review-code”进行差异范围和代码库范围的审查
- 通过“run-automated-tests”执行测试（快速/ci/完整模式）
- 保留 API 合约的最少目标补丁
- 停止条件检测（无进展、环境阻碍、片状测试、迭代限制）
- 结构化修复循环报告输出

**本技能不负责**：

- 在没有明确用户确认的情况下安装依赖项
- 无需用户确认即可使用网络或启动 Docker/服务
- 未经用户明确批准的大型重构
- 修改不相关的同级存储库
- 在未经用户明确批准的情况下禁用测试、削弱断言或删除覆盖范围

**转交点**：当环路收敛或达到停止条件时，向用户呈现修复环路报告。对于有风险的更改（架构迁移、身份验证更改、广泛重构），请在申请之前暂停并请求明确批准。

---

## 使用场景（用例）

- “继续修复直到测试通过。”
- “进行审查-测试-修复循环并使存储库变得绿色。”
- “通过迭代测试和有针对性的修复来稳定此 PR/变更集。”
- “运行类似 CI 的测试，修复故障，重复直到稳定。”

---

## 行为（行为）

### 1. 飞行前（必须解决一次）

确认或默认以下内容：

- **目标**：存储库路径（默认“.”）和范围：
  - `diff`（默认）：关注当前更改，优先考虑`review-diff`。
  - `codebase`：审查指定的路径集，通过`review-code`优先考虑`review-codebase`/语言技能。
- **完成的定义**：
  - 测试：所选测试计划通过（快速/ci/完整）。
  - 审查：没有保留“关键”/“主要”审查结果。
  - 如果仅剩下“次要”/“建议”发现，请将其列出并询问是否解决它们。
- **循环边界**：
  - `max_iterations` 默认值：`5`。
  - `time_budget` 默认值：“尽力而为”；如果用户提供了时间限制，请严格遵守。
- **允许的操作**（不清楚时询问；默认为更安全的选择）：
  - 修改存储库文件：**是**（此技能用于修复），但保持最小程度的更改。
  - 安装依赖项：**否**，无需确认。
  - 网络访问：**否**，无需确认。
  - Docker/服务（DB/Redis/等）：**否**，无需确认。
  - 大型重构：**否**，未经确认。

### 2.迭代循环

对于“i = 1..max_iterations”：

1. **收集当前信号（证据优先）**
   - 如果范围 = `diff`：对当前 diff/未跟踪的添加运行/执行 `review-diff` 传递。
   - 如果范围=“代码库”或用户想要更深入的审查：运行“审查代码”（或相关的原子审查技能）。
   - 如果之前的迭代出现测试失败，请优先考虑首先解决这些失败。

2. **运行测试**
   - 使用“run-automated-tests”在所选模式下发现并运行最匹配的测试命令：
     - `fast`（默认）：仅进行单元测试，最少的设置。
     - `ci`：尽可能接近地镜像 CI 步骤。
     - `full`：包括集成/e2e（仅对依赖项/服务进行明确确认）。
   - 捕获：
     - 第一个失败的命令+退出代码
     - 最相关的错误摘录（除非要求，否则不要转储大量日志）

3. **综合修复计划（最小正确补丁）**
   - 选择首先要解决的**一个**主要问题：
     - 第一个失败的测试/命令通常获胜（最高信号）。
     - 如果审查发现“关键”安全/正确性问题，请在测试之前或同时修复该问题。
   - 更喜欢修复：
     - 改变最小表面积
     - 保留 API/合同，除非明确批准
     - 修复错误时添加或调整测试（如果可行）

4. **应用修复**
   - 实施补丁。
   - 避免不相关的格式或流失。
   - 如果修复需要进行有风险的更改（架构迁移、身份验证更改、广泛重构），请暂停并询问。

5. **重新运行最小验证**
   - 如果框架支持，重新运行最相关的失败测试子集；否则重新运行相同的测试命令。
   - If fixed, proceed to the next remaining failure/finding within the same iteration only if it is trivial;否则进入下一个循环迭代。

6. **汇合时尽早停车**
   - 如果测试通过并且没有“关键”/“主要”审查结果，则停止。

### 3.停止条件（不得永远循环）

如果发生任何情况，请停止并向用户询问方向：

- **没有进展**：同样的失败重复了 2 次迭代，没有新信息。
- **环境拦截器**：缺少工具链、缺少机密或不可用的依赖项（DB/Docker）并且用户尚未批准所需的设置。
- **片状测试**：怀疑不确定性故障（例如，在没有更改的情况下重试）。
- **达到迭代限制**：`max_iterations` 已耗尽，剩余失败。

停止时，提供最短路径选项：

- 运行不同的测试模式（`fast` -> `ci` -> `full`）
- 允许安装/网络/Docker
- 范围狭窄（仅修复第一个失败的测试）
- 增加迭代限制

### 报告持久性

默认情况下不要编写独立的报告文件。如果用户明确要求保留，请写入从项目规范解析的路径，或默认为“docs/calibration/repair-loop.md”并覆盖规范文件，除非明确请求快照。

---

## 输入与输出 (Input & Output)

### 输入（输入）

- 目标路径（默认`.`）
- 范围：“diff”（默认）或“codebase”（+ 路径）
- 测试模式：`fast`（默认）、`ci`、`full`
- 约束：允许安装/网络/Docker/服务（是/否）
- `max_iterations`（默认为`5`）
- 可选：时间预算

### 输出（输出）

- **修复循环报告**：
  - 完成使用的定义
  - 证据来源（哪些文件/CI 配置告知测试计划）
  - 对于每次迭代：
    - 测试命令运行和结果
    - 第一次失败摘录（如果有）
    - 所做的更改（触及的文件+意图）
    - 剩余的失败/发现
  - 最终状态：
    - 测试通过（哪个命令）
    - 剩余的审查项目（如果有）以及它们是否被阻止

---

## 限制（限制）

### 硬边界（Hard Boundaries）

- 未经明确确认，请勿安装依赖项、使用网络、启动 Docker/服务或运行破坏性命令。
- 不要要求用户将秘密粘贴到聊天中。更喜欢本地环境文件或文档化的开发流程。
- 不要通过禁用测试、削弱断言或删除覆盖范围来“修复”，除非用户明确批准并且权衡已记录在案。
- 避免默认进行大型重构；优先考虑能够解锁正确性的最小补丁。
- 将更改范围保持在目标存储库范围内；不要修改不相关的同级存储库。

### 技能边界 (Skill Boundaries)（避免重叠）

**不要做这些（其他技能可以处理它们）**：

- **仅测试执行**（无审查或修复循环）：使用“run-automated-tests”
- **测试质量评估**（覆盖范围、结构、边缘情况充分性）：使用“审查测试”
- **全面的代码审查**（无测试修复迭代）：使用“review-code”
- **仅差异审查**（没有测试执行或修复迭代）：使用 `review-diff`
- **从头开始编写新测试**（不修复现有故障）：使用开发技能

**何时停止并交接**：

- 环路收敛（测试通过，没有阻塞发现）→ 当前修复环路报告并停止
- 遇到停止条件（无进展、环境阻碍、片状测试、迭代限制）→ 显示选项并等待用户指示
- 用户请求一次性代码审查而不修复 → 移交给“review-code”或“review-diff”
- 用户要求仅运行测试而不修复 → 移交给“run-automated-tests”

---

## 自检（Self-Check）

### 核心成功标准

- [ ] **完成解析的定义**：在循环开始之前确认飞行前选择（范围、测试模式、最大迭代次数、允许的操作）
- [ ] **每次迭代证据优先**：每次迭代至少产生以下之一：新的测试结果、新的审查信号或具体的代码更改
- [ ] **修复后重新运行测试**：在同一迭代中应用修复后，失败的测试命令（或目标子集）始终重新运行
- [ ] **有界循环**：循环由于收敛或显式停止条件而终止 - 没有无限重试
- [ ] **结构化最终报告**：输出包括修复循环报告（附录：输出合同），其中包含命令运行、故障、补丁和剩余风险

### 流程质量检查

- [ ] **最小补丁表面**：每个修复仅涉及解决已识别问题所需的文件 - 没有不相关的格式或改动。
- [ ] **不稳定的测试意识**：检测到非确定性故障（例如，在不更改代码的情况下传递重试）并进行标记，而不是盲目地“修复”。
- [ ] **应用了风险更改暂停**：架构迁移、身份验证更改或广泛的重构在继续之前触发了明确的用户确认。
- [ ] **每次迭代跟踪的进度**：每个迭代日志都显示一个清晰的增量（新信号或新修复） - 没有空洞的迭代。

### 验收测试

最终报告是否显示（a）测试通过且没有阻止审查结果，或（b）明确的停止条件，并为用户提供明确的剩余问题和选项？

---

## 示例（示例）

### 示例 1：修复 Node 存储库中失败的单元测试

用户：“让测试通过。继续修复直到绿色。”

代理：

1. 飞行前：scope=`diff`，测试模式=`fast`，max_iterations=5；确认允许安装（`npm ci`）并且允许网络。
2. 迭代 1：运行 `npm test`，修复第一个失败的测试，重新运行 `npm test`。
3. 迭代 2：运行 `review-diff` 以捕获修复引入的边缘情况；重新运行`npm test`。
4. 当“npm test”通过并且没有重大审查结果时停止。

### 示例 2（边缘情况）：集成测试需要 Docker 和密钥

用户：“镜像 CI 并修复故障。”

代理：

1. 预检：建议测试模式=`ci`，但检测 CI 使用 `docker compose` 和 env 密钥。
2. 触发停止条件：环境拦截器（Docker + 机密未批准/不可用）。
3. 要求用户选择：
   - 仅在本地运行“快速”单元测试，或者
   - 允许 Docker 并提供非聊天秘密工作流，或者
   - 仅运行不需要机密的失败 CI 作业步骤。

---

## 附录：输出合约

每个技能执行必须以这种精确的 JSON 格式生成 **修复循环报告**：


```json
{
  "repair_loop_report": {
    "definition_of_done": {
      "tests": "test command passes",
      "review": "no critical/major findings"
    },
    "scope": "diff | codebase",
    "mode": "fast | ci | full",
    "max_iterations": 5,
    "iterations": [
      {
        "iteration": 1,
        "review": {
          "skill_used": "review-diff",
          "findings_count": {"critical": 0, "major": 1, "minor": 2},
          "blocking": ["unused import in utils.js"]
        },
        "tests": {
          "command": "npm test",
          "status": "failed",
          "exit_code": 1,
          "first_failure": "FAIL src/utils.test.js"
        },
        "fix": {
          "files_changed": ["src/utils.js"],
          "intent": "remove unused import"
        },
        "re_run": {
          "command": "npm test",
          "status": "passed"
        }
      }
    ],
    "final_state": {
      "tests_passing": true,
      "commands_passed": ["npm test"],
      "blocking_issues_remaining": [],
      "minor_suggestions": ["consider adding type hints"]
    },
    "stop_condition": "converged | max_iterations | environment_blocker | no_progress"
  }
}
```

|元素|类型 |描述 |
| :--- | :--- | :--- |
| `完成的定义` |对象|什么是成功|
| `范围` |字符串| `diff` 或 `代码库` |
| `模式` |字符串|测试模式：`fast`、`ci` 或 `full` |
| `最大迭代次数` |数量 |循环限制|
| `迭代` |数组|每次迭代的审查、测试、修复、重新运行 |
| `最终状态` |对象|最终状态：测试通过，仍有问题 |
| `停止条件` |字符串|为什么循环结束：`converged`、`max_iterations`、`environment_blocker`、`no_progress` |

此架构允许代理使用而无需进行散文解析。