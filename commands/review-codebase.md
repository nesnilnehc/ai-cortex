---
name: review-codebase
version: 1.0.0
recommended_scope: project
---

# Command: /review-codebase

## 触发意图 (Intent)

用户希望以高级全栈架构师与生产代码评审视角，对**指定文件、目录或仓库范围**的代码进行评审（不限于 git diff），识别缺陷、风险与改进点，并给出可落地的建议。

## 映射技能 (Mapped Skills)

- [review-codebase](../skills/review-codebase/SKILL.md)

## 参数化指令 (Params)

- 格式：`/review-codebase [path …]`
- 参数：可选，一个或多个文件或目录路径；未指定时可为当前仓库根或用户声明的关注路径。

## 交互反馈 (UX)

执行技能前可提示：「正在对指定范围进行生产级代码评审…」；执行后按文件或模块输出评审结论与建议，引用 file:行。
