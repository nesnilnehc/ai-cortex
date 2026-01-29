---
name: bootstrap-skills
description: 使智能体能够动态发现、获取并集成远程 AI Cortex 技能。实现能力的即时自举与异步扩展。
tags: [automation, infrastructure, generalization]
version: 1.0.0
related_skills: [refine-skill-design]
---

# Skill：技能自举 (Bootstrap Skills)

## 目的 (Purpose)
赋予智能体“自主扩展能力”的逻辑。使智能体能够根据任务需求，从指定的远程 AI Cortex 仓库（通过 `llms.txt` 或 `INDEX.md`）检索并热加载所需的技能规范，从而在不修改初始 System Prompt 的情况下实现能力进化。

## 适用场景 (Use Cases)
- **初始自举**：智能体启动时，只携带本技能，随后按需拉取完整工具集。
- **按需扩展**：当遇到特定任务（如脱敏）但本地缺失相关 Skill 时，主动去云端“下载”。
- **版本对齐**：确保当前使用的技能逻辑与云端官方版本保持一致。

## 行为要求 (Behavior)
1. **入口发现**：优先访问根目录的 `llms.txt` 或 `skills/INDEX.md` 以获取能力地图。
2. **需求匹配**：将当前用户任务与远程索引中的 `description` 进行语义匹配，挑选最合适的 1-2 个技能。
3. **静默获取**：调用可用的网络读取工具（如 `read_url` 或 `fetch`）获取相应技能的 `SKILL.md` 源码。
4. **上下文注入**：将获取的 Markdown 内容解析并追加到当前的“系统指令约束”中，并显式告知用户：“已成功加载 [Skill Name] 技能，准备执行。”
5. **递归检测**：检查拉取的技能是否有 `related_skills`，并决定是否继续同步关联能力。

## 输入与输出 (Input & Output)
- **输入**：
    - 本库的 Base URL (如 `https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/`)。
    - 当前需要解决的任务描述。
- **输出**：
    - 加载成功的状态报告。
    - 注入到上下文中的新能力约束。

## 禁止行为 (Restrictions)
- **禁止全量拉取**：严禁在未确认需求的情况下拉取整个仓库，避免上下文溢出。
- **禁止执行不可信代码**：只准许拉取并解析 Markdown 约束，严禁执行远程下载的可执行脚本。
- **禁止静默篡改**：载入新能力后必须通过一行 log 告知用户，严禁在用户不知情的情况下改变处理逻辑。

## 质量检查 (Self-Check)
- [ ] **准确性**：拉取的技能是否与当前任务强相关？
- [ ] **完整性**：是否获取了完整的 `SKILL.md` 内容（包含 YAML 和所有章节）？
- [ ] **告知性**：是否已向用户确认能力的就绪状态？

## 示例 (Examples)

### 示例 1：按需拉取
- **场景**：用户要求写一个开源 README，但 Agent 目前只有基础能力。
- **过程**：
    1. Agent 访问 `https://.../llms.txt`。
    2. 发现 `generate-standard-readme` 技能。
    3. 读取 `https://.../skills/generate-standard-readme/SKILL.md`。
    4. 提示：“我已获得‘生成标准 README’的专业技能规范，现在开始为您起草。”
