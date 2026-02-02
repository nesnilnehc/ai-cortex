---
name: review-code
version: 1.0.0
recommended_scope: project
---

# Command: /review-code

## 触发意图 (Intent)

用户希望以高级全栈架构师与生产代码评审视角，**仅针对当前工作区的代码变更（git diff）**进行逐文件评审，识别缺陷、风险与改进点，并给出可落地的建议。

## 映射技能 (Mapped Skills)

- [review-code](../skills/review-code/SKILL.md)

## 参数化指令 (Params)

- 格式：`/review-code`
- 无参数；输入为当前分支的 staged + unstaged diff。

## 交互反馈 (UX)

执行技能前可提示：「正在对当前 diff 进行生产级代码评审…」；执行后按文件输出评审结论与建议，引用 file:line 或 @@ 块。
