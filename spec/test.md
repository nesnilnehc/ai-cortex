# 技能测试规范 (Skill Test Specification)

> **自解释说明（Agent 必读）**  
> 本文件即「测试入口」：**仅阅读本文件并按 [§ 执行清单](#执行清单agent-可直接执行) 操作，即可完成仓库内所有带测试技能的验证**。数据源与步骤均在下方写明，无需再读其他脚本或各技能目录。

本规范定义 `skills/*/tests/` 下测试文件的格式与运行策略，供贡献者、CI 与 Agent 使用。

**文档定位**：本文档既是 **Spec（规范）** 也是 **可执行说明（Runbook）**。

- **Spec 部分**：约定测试文件格式（assertions.md、cases.json）、数据源（manifest.json 与 test_path）、与 manifest 的对应关系；供实现者、贡献者、CI 遵循。  
- **可执行部分**：执行清单明确「如何跑」全量测试，供 Agent 直接按步骤运行。  

自解释、可执行并不改变其规范性质：规范定义契约，执行清单是「按该契约运行测试」的权威说明；二者合一便于单文件发现与执行，仍属 Spec 的一种形态。

---

## 数据源与约定

### 待测技能列表从哪里来

- **唯一数据源**：仓库根目录的 **`manifest.json`**。
- **取法**：读取 `manifest.json`，解析 `capabilities` 数组，**仅保留 `test_path` 不为 `null` 的项**。
- **每项所用字段**：
  - `name`：技能名（用于输出与记录）；
  - `path`：该技能的 `SKILL.md` 路径（执行依据）；
  - `test_path`：该技能的 `tests/` 目录路径（如 `skills/decontextualize-text/tests/`）。

### 每个技能的测试文件

| 文件 | 路径 | 用途 |
| :--- | :--- | :--- |
| **assertions.md** | `{test_path}assertions.md` | 产出质量的判定准则（Pass 条件、评分维度）；用于对执行结果逐条判分。 |
| **cases.json** | `{test_path}cases.json` | 用例列表。每项约定包含：`id`、`description`、`input`、`expected_behavior`（或等价字段）；`input` 为执行技能的输入，`expected_behavior` 可为自然语言描述，供人工或 LLM 对照。 |

- **cases.json**：JSON 数组，每条约定的字段名由各技能自述；上表为推荐字段。
- **assertions.md**：可含表格（准则标号、描述、检测逻辑）与评估公式（如 Pass 条件、Score 计算）。

---

## 执行清单（Agent 可直接执行）

按下列步骤执行即完成「全量技能测试」；无需再读其他测试说明。

1. **枚举待测技能**
   - 读取仓库根目录的 **`manifest.json`**。
   - 从 `capabilities` 中筛选出 **`test_path != null`** 的项，得到列表：`[(name, path, test_path), ...]`。

2. **对每个技能**
   - 读取 **`path`** 指向的 **`SKILL.md`**（执行技能时的依据）。
   - 读取 **`test_path`** 下的 **`assertions.md`**（判分准则）与 **`cases.json`**（用例列表）。
   - 若 `cases.json` 或 `assertions.md` 不存在，则跳过该技能或标记为「无用例/无断言」，并继续下一技能。

3. **对每个用例**（即 `cases.json` 中的每一条）
   - 以该条的 **`input`** 为输入，**按该技能的 SKILL.md 执行一次**（在编辑器或对话中把 input 交给执行方，并指示其按对应 SKILL.md 执行）。
   - 用该技能的 **`assertions.md`** 对本次产出逐条判定，得到 **Pass/Fail** 或 **Score**。
   - **记录**：技能名、用例 `id`、结果（Pass/Fail 或分数）。

4. **汇总**
   - 可选：输出一份简要结果表（技能名、通过数/总用例数、失败用例 id 等）。

**自动化（未来）**：若实现统一 runner（如基于 LLM-as-judge 或确定性断言），可在 CI 中调用；当前以人工或 Agent 按本清单执行为主。

---

## 谁运行、何时运行

- **贡献者**：在提交 PR 或合并前，对改动过的技能按本规范执行一次自测。
- **Agent**：在产出或修改技能时，可按本文件「执行清单」做自检。
- **CI（可选）**：若引入自动化测试 runner，可在 PR 时对 `skills/*/tests/` 做回归；当前无统一 runner，由人工或 Agent 按本规范执行。
- **何时**：修改某技能的 `SKILL.md` 或该技能下 `tests/` 后，在合并到默认分支前至少运行一次该技能的测试；新增技能时建议同时新增至少 1 个用例与对应 assertions。

---

## 与 manifest 的对应

- `manifest.json` 中 **`capabilities[].test_path`** 指向该技能的 **`tests/`** 目录（如 `skills/foo/tests/`）。
- 若有同步或集成流程，可按 `test_path` 拉取 `assertions.md`、`cases.json` 到消费方；运行策略由消费方或本仓库贡献流程自行决定，本规范仅约定格式与推荐执行时机。

---

## 参考

- 技能编写与结构见 [spec/skill.md](skill.md)。
- 用例与断言示例：`skills/decontextualize-text/tests/`、`skills/generate-standard-readme/tests/`。
