---
name: writing-chinese-technical
version: 1.3.0
scope: 全局文档产出
recommended_scope: user
---

# Rule: Chinese Technical Writing

## Scope

Applies to every Chinese-language document, Chinese code comment and Chinese agent output in this project. [docs/LANGUAGE_SCHEME.md](../docs/LANGUAGE_SCHEME.md) decides which assets are written in Chinese; any document that does use Chinese must conform to this rule and follow the registration conventions in [rules/INDEX.md](./INDEX.md).

## Constraints

1. **Chinese–Latin spacing**: one space must be kept between a Chinese character and an adjacent Latin word or digit — “使用 Git 提交”, not “使用Git提交”.
2. **Numbers and units**: a space must be kept between a number and its unit — “10 Gbps”, “20 TB”, not “10Gbps”, “20TB”. Do not add a space between a Latin character or half-width digit and a full-width punctuation mark.
3. **Terminology**: prefer the Chinese term defined under this project's `specs/`, and keep the English in parentheses on first use.
4. **Punctuation**: full-width punctuation in Chinese sentences, half-width in English sentences, half-width digits throughout. Use backticks when quoting code or a term.
5. **Interface strings**: prompts do not need terminal punctuation — “请输入用户名”. Complete sentences end with 「。」. Avoid 「!」.
6. **Tone**: keep a professional, no-nonsense engineering voice. Text must not contain excessive emoji, nor filler particles such as “哒” or “呢”.

## Bad Patterns

- `使用Python进行开发` — missing space
- `10Gbps`, `20TB` — missing space between number and unit
- `这个技能好厉害呀！` — unprofessional tone
- `请点击"确定"按钮` — should use Chinese corner brackets, or no quotes at all
- An interface prompt ending in a period or exclamation mark — “请重试。”

## Remediation

When a violation is found, immediately rewrite the affected block until it conforms.
