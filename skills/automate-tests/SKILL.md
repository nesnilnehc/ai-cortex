---
name: automate-tests
description: Discover and execute repository test commands safely with evidence-based command selection and safety guardrails.
description_zh: 安全发现并执行仓库测试命令；基于证据选择命令并设安全护栏。
tags: [automation, devops]
version: 1.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [run tests, automated tests, auto test, autotest]
aliases: [run-automated-tests]
compatibility: Requires git (optional), a shell, and the repo's language toolchain(s) (e.g., node, python, go, dotnet, java).
input_schema:
  type: code-scope
  description: Repository path containing test configuration and source code
  defaults:
    scope: repo
output_schema:
  type: diagnostic-report
  description: Test plan summary with commands run, results, and failure diagnostics
---

# 技能 (Skill)：运行自动化测试

## 目的 (Purpose)

确定目标存储库期望如何执行自动化测试（命令、框架、先决条件和范围），然后使用安全第一的交互策略运行最佳匹配的测试套件。

---

## 核心目标（Core Objective）

**首要目标**：通过基于证据的命令选择和安全护栏生成测试执行结果。

**成功标准**（必须满足所有要求）：

1. ✅ **发现测试计划**：确定的证据来源（文档、CI 配置或构建清单）
2. ✅ **选择的命令**：根据模式（fast/ci/full）和约束选择适当的测试命令
3. ✅ **获得用户确认**：在安装依赖项、使用网络或启动服务之前收到批准
4. ✅ **执行的测试**：使用捕获的输出和退出代码运行命令
5. ✅ **结果总结**：包含证据、命令、执行状态和失败（如果有）的测试计划摘要

**验收**测试：开发人员可以在没有额外上下文的情况下按照测试计划摘要重现测试执行吗？

---

## 范围边界 (Scope Boundaries)

**本技能负责**：

- 从存储库证据（文档、CI、构建清单）中发现测试命令
- 根据模式和约束选择适当的测试命令
- 执行带有安全护栏和用户确认的测试
- 通过证据和故障诊断总结测试结果

**本技能不负责**：

- 测试质量评估或覆盖率分析（使用“审查测试”）
- 修复失败的测试或调试测试失败（使用“run-repair-loop”）
- 编写新的测试或测试基础设施（使用开发技能）
- 审查测试代码以获得最佳实践（使用“审查测试”）

**转交点**：当测试完成（通过或失败）时，移交给“自动修复”以修复故障或“审查测试”以进行质量评估。

## 使用场景（用例）

- 您克隆了一个存储库，并且想要正确的测试命令而无需猜测。
- 存储库具有多个测试层（单元/集成/e2e），您需要一个安全的默认运行计划。
- CI 失败，您希望通过运行工作流中使用的相同命令在本地重现。

## 行为（行为）

1. **建立范围和约束（询问是否不明确）**
   - 如果用户未指定，则默认为**快速、本地、非破坏性**运行：
     - 仅单元测试，无外部服务，无 Docker，无网络相关设置。
   - 如果需要，请用户选择一种模式：
     - `fast`：仅进行单元测试，最少的设置。
     - `ci`：尽可能接近地镜像 CI 工作流命令。
     - `full`：包括集成/e2e 测试和服务依赖项。
   - 询问是否允许Docker、是否允许网络访问、是否允许安装依赖。

2. **发现测试计划（基于证据）**
   - 按顺序阅读这些来源；如果发现清晰、明确的测试命令，请尽早停止：
     - `README.md`、`CONTRIBUTING.md`、`TESTING.md`、`docs/testing*`、`Makefile`
     - CI 配置：`.github/工作流s/*.yml`、`.gitlab-ci.yml`、`azure-pipelines.yml`、`Jenkinsfile`
     - 构建清单：`package.json`、`pyproject.toml`、`setup.cfg`、`tox.ini`、`go.mod`、`pom.xml`、`build.gradle*`、`*.csproj`、`Cargo.toml`
   - 识别：
     - 主要测试入口点（`npm test`、`pnpm test`、`yarn test`、`pytest`、`tox`、`go test`、`dotnet test`、`mvn test`、`gradle test`、`cargo test`等）
     - 测试层和标记（单元、集成、e2e）
     - 环境先决条件（DB、Redis、Docker Compose、所需的环境变量、秘密）
     - CI 如何设置依赖关系（服务、缓存、产品）
   - 与启发式方法相比，更喜欢在文档或 CI 中找到**明确的说明**。

3. **选择执行计划**
   - 如果是“ci”模式：从存储库的 CI 工作流步骤（最接近的匹配）导出运行序列。
   - 如果是“快速”模式：选择最直接且先决条件最少的单元测试命令。
   - 如果存在多个堆栈（例如后端 + 前端），建议按确定的顺序单独运行每个堆栈。
   - 如果计划需要依赖项安装或服务启动，请在继续之前请求确认。

4. **有护栏执行**
   - 在运行命令之前，始终打印您将要运行的确切命令。
   - 使用以目标存储库为根的工作目录（默认为“.”）。
   - 捕获并总结失败：
     - 第一个失败的命令和退出代码
     - 最相关的错误摘录
     - 下一步操作（缺少工具链、缺少环境变量、服务未运行等）
   - 避免破坏性操作：
     - 未经用户明确批准，请勿运行“rm -rf”、“git clean -fdx”、“docker system prune”或数据库删除/迁移命令。
   - 如果存储库需要机密，请勿要求用户将机密粘贴到聊天中。首选“.env”文件、秘密管理器或记录的本地开发流程。

## 输入与输出 (Input & Output)

### 输入（输入）

- 目标存储库路径（默认“.”）。
- 模式：“fast”（默认）、“ci”或“full”。
- 约束：允许依赖项安装（是/否）、允许网络（是/否）、允许 Docker（是/否）。

### 输出（输出）

- 简短的“测试计划摘要”，其中包含：
  - 证据：哪些文件/路径告知了计划
  - 选择的命令（按顺序）
  - 假设和先决条件
  - 执行了什么以及跳过了什么（以及原因）
- 足以调试故障的命令记录片段（除非要求，否则不要转储极长的日志）。

## 限制（限制）

### 硬边界（Hard Boundaries）

- 当证据存在时不要发明测试命令（首选文档/CI）。
- 未经确认，请勿安装依赖项、运行 Docker 或启动外部服务。
- 除非用户明确请求，否则不要修改存储库文件（例外：如果用户请求产品，则生成报告文件）。
- 不泄露秘密；不要在聊天中请求敏感凭据。

### 技能边界 (Skill Boundaries)（避免重叠）

**不要做这些（其他技能可以处理它们）**：

- **测试质量评估**：评估测试覆盖率、测试设计或测试最佳实践→使用“审查测试”
- **修复测试失败**：调试失败的测试、修复损坏的测试代码或调查根本原因 → 使用“run-repair-loop”
- **编写测试**：创建新的测试用例、测试基础设施或测试框架 → 使用开发/实施技能
- **代码审查**：审查测试代码的质量、可维护性或最佳实践→使用“审查测试”
- **存储库分析**：全面的代码库结构分析或架构审查→使用 `review-codebase`

**何时停止并交接**：

- 测试失败，用户问“为什么？”或“如何解决？” → 移交给“run-repair-loop”进行调试和修复
- 用户问“这些测试好吗？”或“我们的覆盖范围是什么？” → 移交给“审查测试”进行质量评估
- 用户问“你能为 X 编写测试吗？” → 移交给开发工作流程进行测试实施
- 测试通过，用户询问“接下来我们应该测试什么？” → 将测试策略建议移交给“审查测试”

## 自检（Self-Check）

### 核心成功标准（必须满足所有标准）

- [ ] **发现测试计划**：确定的证据来源（文档、CI 配置或构建清单）
- [ ] **选择的命令**：根据模式（fast/ci/full）和约束选择适当的测试命令
- [ ] **获得用户确认**：在安装依赖项、使用网络或启动服务之前收到批准
- [ ] **执行的测试**：使用捕获的输出和退出代码运行命令
- [ ] **结果总结**：包含证据、命令、执行状态和失败（如果有）的测试计划摘要

### 流程质量检查

- [ ] **基于证据的选择**：我是否确定了至少一个权威的测试指令源（doc 文件、CI 工作流程或构建清单）？
- [ ] **应用安全护栏**：在安装依赖项、使用网络、启动 Docker/服务或更改状态的任何操作之前，我是否要求确认？
- [ ] **打印的命令**：我在运行命令之前是否打印了确切的命令？
- [ ] **诊断的故障**：如果测试失败，我是否提供了第一个失败的命令、退出代码和可能的根本原因类别？
- [ ] **无破坏性操作**：我是否在未经明确批准的情况下避免运行破坏性命令（`rm -rf`、`git clean`、`docker system prune`、数据库删除）？
- [ ] **无秘密泄露**：我是否避免在聊天中请求敏感凭据并更喜欢“.env”文件或记录的本地开发流程？

### 验收测试

**开发人员可以在没有额外上下文的情况下通过遵循测试计划摘要来重现测试执行吗？**

如果否：测试计划摘要不完整。添加缺失的证据、命令或先决条件。

如果是：技能执行完成。如果需要，继续转交。

## 示例（示例）

### 示例 1：带有 package.json 的 JavaScript Repo

用户：“为此存储库运行测试。”

代理人：

1. 检查 `package.json` 脚本和 `.github/Workflows/*`。
2. 确定模式“fast”并提出：
   - `npm test` （或者 `pnpm test` / `yarn test` 如果仓库对其进行了标准化）
3.询问：“安装依赖项（`npm ci`）并允许网络？”
4. 运行：
   - `npm ci`
   - `npm 测试`
5. 总结结果并指出失败的测试输出（如果有）。

### 示例 2（边缘情况）：Monorepo 需要 Docker 进行集成测试

用户：“在本地镜像 CI。”

代理：

1. 解析 `.github/工作流s/ci.yml` 并识别单独的作业：
   - 后端单元测试
   - 前端测试
   - 与“docker compose”的集成测试
2. 要求确认：
   - 允许Docker
   - 允许网络
   - 要运行哪些作业（所有作业与仅运行失败的作业）
3. 按受控顺序执行：
   - 按作业安装 deps
   - 首先运行单元测试
   - 启动集成测试服务
4. 如果集成测试失败，总结：
   - 服务运行状况/端口冲突
   - 缺少环境变量
   - CI 配置与本地配置有何不同

---

## 附录：输出合约

每个技能执行必须以这种精确的 JSON 格式生成**测试计划摘要**：


```json
{
  "test_plan_summary": {
    "mode": "fast | ci | full",
    "evidence": ["path/to/source1", "path/to/source2"],
    "commands": [
      {"command": "npm test", "purpose": "run unit tests", "order": 1}
    ],
    "prerequisites": ["npm ci", "Docker running"],
    "executed": ["npm ci", "npm test"],
    "skipped": ["integration tests - require Docker"],
    "result": {
      "status": "passed | failed | blocked",
      "exit_code": 0,
      "first_failure": {
        "command": "npm test",
        "exit_code": 1,
        "error_excerpt": "FAIL src/utils.test.js"
      }
    }
  }
}
```

|元素|类型 |描述 |
| :--- | :--- | :--- |
| `模式` |字符串|所选模式：`fast`、`ci` 或 `full` |
| `证据` |数组|告知测试计划的源文件 |
| `命令` |数组|具有目的和顺序的选定测试命令 |
| `先决条件` |数组|所需的设置步骤 |
| `已执行` |数组|命令实际运行 |
| `跳过` |数组|跳过的命令和原因 |
| `结果.状态` |字符串| “通过”、“失败”或“被阻止”|
| `结果.退出代码` |数量 |测试命令的退出代码 |
| `结果.first_failure` |对象|第一次失败详细信息（如果有）|

此架构允许代理使用而无需进行散文解析。