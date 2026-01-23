# llm-skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

面向 LLM Agent 的可复用 **Skill**、**Rule**、**Command** 工程化资产库。
将能力与行为显式化、可组合化，而不是隐藏在零散的 Prompt 中。

---

## 这是什么

- **Skill**：能做什么（目的、场景、输入、输出）
- **Rule**：该怎么 / 不该怎么做（边界、安全、禁止项）；约束型，不直接产出
- **Command**：如何触发（意图、调用形式）

**不包含**：Runtime / 框架、Tool Server / 协议、厂商绑定配置、Prompt 试验场。  
本仓库只关注「能做什么、该怎么行为」，不关心「用什么协议、运行时如何实现」。

---

## 仓库结构

> 规划结构，目录随贡献完善。

```text
llm-skills/
├── skills/        # Skill
├── rules/         # Rule
├── commands/      # Command
├── templates/
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

---

## 设计原则

- **工具无关**：不绑运行时、协议、平台
- **可组合**：Skill 可叠加
- **显式**：写清在文档里，不塞在 Prompt
- **稳定**：长期复用、可演进

---

## 使用

把 `skills/`、`rules/`、`commands/` 下的 `SKILL.md`、`RULE.md` 等引入你的 Agent 框架或 Prompt 即可。自描述，无运行时依赖。

---

## 适合谁

- 正在构建或维护 **LLM Agent** 的开发者
- 希望将 **Prompt、规则（Rule）、能力（Skill）结构化管理** 的团队
- 不想让关键行为逻辑散落在 Prompt 中、希望长期复用与演进的人

---

## License

MIT
