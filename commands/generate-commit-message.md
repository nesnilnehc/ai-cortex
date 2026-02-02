---
name: generate-commit-message
version: 1.0.0
recommended_scope: project
---

# Command: /generate-commit-message

## 触发意图 (Intent)

用户希望根据当前工作区的 git diff 生成一条符合 Conventional Commits 规范的专业 Git 提交信息，用于直接执行 `git commit`。

## 映射技能 (Mapped Skills)

- [generate-commit-message](../skills/generate-commit-message/SKILL.md)

## 参数化指令 (Params)

- 格式：`/generate-commit-message`
- 无参数；输入为当前分支的 staged + unstaged diff。

## 交互反馈 (UX)

执行技能前可提示：「正在根据当前 diff 生成 Conventional Commits 提交信息…」；执行后仅输出生成的提交信息正文，无多余说明。
