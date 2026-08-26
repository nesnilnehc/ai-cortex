---
name: publish-release
description: Validate a ready Release Package and execute the repository's publication steps—tag, build, package, and provider release—with explicit mutation gates.
description_zh: 校验 ready 状态的 Release Package，并按仓库约定执行 tag、构建、打包和发布；所有外部写入均有明确闸门。
tags: [release, publish, tag, build, package]
version: 1.2.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [publish release, ship release, tag and publish, release artifact]
input_schema:
  type: free-form
  description: Ready Release Package path or preparation result; optional provider and dry-run preference
output_schema:
  type: side-effect
  description: Publication result with tag, build/package evidence, provider receipt, rollback path, and updated Release Package status
---

# 技能（Skill）：发布版本（Publish Release）

## 目的

消费 `prepare-release` 生成的 `ready` Release Package，执行项目已配置的发布动作，并把实际结果写回 package。不重新生成 changelog，不写公告内容，也不默默假设目标平台。

## 核心目标

只在 Release Package 的 required 门禁与材料满足条件、且用户确认外部写入后，完成可追溯的 publication，并返回真实回执或明确失败状态。

## 行为

1. **加载与校验**：要求 `decision=release`、`status=ready`，确认版本、通道、canonical version source、各版本域动作、目标 SHA、required artifacts/checks、当前分支和工作树状态。`not_required`、失败门禁、SHA 不匹配或不允许的脏工作树均停止。
2. **发现发布路径**：按 `CLAUDE.md`、`.ai-cortex/config.yaml`、CI 配置、Makefile、manifest、bump 工具、Docker/GoReleaser 等本地证据发现版本同步、commit、tag、build/package/provider 命令；优先复用已有 pipeline，并记录项目明确禁止的命令。
3. **建立状态基线**：在 mutation 前记录 canonical version、预期被修改文件、HEAD、现有 release commits/tags 和工作树。若发现上次失败留下的目标版本、部分文件修改、commit 或 tag，先进入恢复流程，不重跑 mutator。
4. **dry-run**：展示版本域动作、预期文件、commit 边界、验证命令、tag、产物、权限/凭据、provider 和每一步回滚路径。版本同步、commit、tag、push、上传或发布前必须确认。
5. **版本与提交**：只执行 package 已确认的产品版本同步计划；独立版本域为 `preserve` 时不得联动修改。项目 release tool 自带 commit 时复用它；否则调用 AI Cortex 本地 vendored `commit-work` 承担精确暂存与 commit，本 Skill 负责顺序和回执。该 Skill 缺失时停止 commit 阶段，不从外部注册表安装或以内嵌简化流程替代。
6. **tag 前门禁**：在创建不可复用 tag 前，运行项目批准的 required validation，并验证 canonical version、派生版本、用户材料首条版本和预期文件一致。任一 required check 失败即停止，不创建 tag。
7. **发布与回执**：验证通过后按已发现的项目依赖顺序执行。需要 tag 前固化产物的项目先 build/package 再创建 annotated tag；以 tag 触发 CI 的项目先 tag，再等待流水线 build/package 回执。随后按授权 push 或触发 provider release。命令或工具缺失时报告未执行，不伪造成功；需要外部连接时先发现能力。
8. 仅在 provider 发布成功并有回执时将 package 状态写为 `published`。只有本地 commit/tag 时不得冒充 published。

### 部分修改恢复

版本工具失败后，先比较状态基线与当前状态：检查 canonical version、预期文件、HEAD、目标 commit 和 tag 是否已存在。把步骤分为 `not_started` / `partially_applied` / `complete`，只继续缺失步骤。不得为了“再试一次”直接重跑 bump；不得重复升级版本；目标 tag 已存在但指向错误 SHA 时停止并请求处理，不自动删除或改写远端状态。

## 与现有能力的边界

`generate-github-workflow` 负责工作流生成，本地 vendored `commit-work` 负责具体提交质量，`announce-release` 负责发布后的沟通。`publish-release` 只编排已确认的版本同步、commit、tag 与 provider 顺序，不重实现这些原子能力，也不在运行时下载缺失 Skill。外部派生 Skill 的来源由 [`../SOURCES.yaml`](../SOURCES.yaml) 统一维护。

## 输入与输出

输入为 `ready` Release Package 路径或准备结果，可选 provider 与 `dry_run`（默认 `true`）。输出为 publication receipt、实际 tag/产物信息、provider 回执、回滚路径，以及按 Spec 更新后的 package 状态。

## 限制

- 未确认不得 push、上传、创建 GitHub Release、发布 registry 或修改生产环境。
- 不跳过 required checks，不用新命令替代仓库已有发布入口。
- 不在 required validation 之前创建 tag；不盲目重跑已部分修改仓库的版本工具。
- 不升级 package 中标记为 `preserve` 的独立版本域。
- 不把凭据写入 manifest、日志或聊天；缺少凭据时停止并说明所需环境。
- 失败时保留准确状态和回滚路径，不自动删除远端 tag 或 release。

## 自检

- [ ] package 为 `decision=release` / `status=ready`，版本域、SHA、range、checks、artifacts 可追溯。
- [ ] 命令和 provider 均有本地配置或工具能力证据。
- [ ] mutation 前状态基线已记录，部分失败可判定已完成与缺失步骤。
- [ ] canonical version、派生版本和用户材料版本一致，required validation 在 tag 前通过。
- [ ] 每个不可逆写入动作前有确认。
- [ ] `published` 只在成功回执后写入。
- [ ] 输出含 tag、产物、回执、失败点和回滚路径。

## 示例

### 示例 1：已有 GoReleaser

发现 `.goreleaser.yaml` 与 tag-triggered workflow 后复用它们，确认后只执行项目规定的 tag/push，不复制 Docker 或 GoReleaser 配置。

### 示例 2：只有本地构建能力

能生成 tarball 但没有 provider。Skill 可完成本地 build/package 并输出待发布回执，但不把状态标为 `published`。

### 示例 3：版本工具在 commit hook 失败

发现 canonical version 与预期文件已更新，但 release commit 和 tag 不存在。不要再次执行 bump；校验修改集合后完成缺失 commit，重新运行 required validation，再创建 tag。若 tag 已存在且 SHA 不符，停止并报告冲突。
