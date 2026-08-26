---
name: prepare-release
description: Build and validate a Release Package from repository history, version policy, quality gates, and optional release artifacts; does not publish or announce.
description_zh: 基于仓库历史、版本策略、质量门禁和可选发布材料构造并校验 Release Package；不负责发布或公告。
tags: [release, versioning, changelog, release-package, orchestration]
version: 1.3.1
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [prepare release, release package, release readiness, cut release]
input_schema:
  type: free-form
  description: Repository path; optional target version/channel, previous tag, artifact preferences, and dry-run preference
output_schema:
  type: document-artifact
  description: Release decision and Package manifest with version domains, change items, artifacts, checks, and readiness; no commit, tag, push, upload, or announcement
---

# 技能（Skill）：准备发布（Prepare Release）

## 目的

构造一个可审计的 [Release Package](../../specs/release-package.md)：确定版本和提交范围，生成或收集发布材料，运行必要门禁，并明确 `ready`、阻塞项与可选材料缺口。它是发布准备的编排器，不是发布执行器。

## 核心目标

成功时输出有证据的发布决策：需要发布时给出 SemVer、通道、版本域、目标 SHA、git range、结构化变化、材料和 readiness；没有产品、兼容性、安全、分发或运维发布意义时明确输出 `decision=none` / `status=not_required`，不制造空发布。

## 行为

### 1. 发现项目约定

按优先级读取 `CLAUDE.md`、`.ai-cortex/config.yaml`、版本文件、CI 配置、仓库文档和 git tags。优先复用已有版本脚本、changelog 生成器、测试命令和发布配置；不凭空发明命令。

同时建立版本域清单：识别产品版本的 canonical source，以及构建、API、协议、数据格式、Prompt、插件等独立版本域。为每个版本域记录 `current`、`source` 和本次 `action`；不得假设它们必须与产品版本一致。

### 2. 解析范围与版本

- 先按项目 tag 模式过滤产品发布 tag，排除 API contract、插件、数据格式等其他版本域的 tag；默认只读当前分支与最近产品发布 tag。
- 按实际发布影响判定 `major` / `minor` / `patch` / `none`：覆盖用户行为与兼容性，也包括安全修复、支持平台、安装/升级、分发和运维契约。Conventional Commit prefix 和 commit 数量只是线索；必要时查看 diff、需求或变更证据。
- 纯文档、测试、CI、内部重构或 rebuild-only 默认判为 `none`，除非它们改变上述发布影响。`none` 时输出 `not_required` 报告并停止材料生成。
- 用户提供版本时校验 SemVer，并以不带 `v` 前缀写入 manifest；未提供时展示候选版本与每条判定依据。
- 识别正式版或预发布通道。已有项目规则时按其 `alpha → beta → rc → stable` 或等价状态推进；没有规则时不自行发明通道，向用户确认。
- 记录完整 commit SHA 和可复现 range；没有上一 tag 时标记初始发布并提示风险。

### 3. 确认发布材料清单

在生成任何材料前，先根据项目约定提出一份可编辑的材料清单，并让用户一次确认。不得只问开放式问题“你需要什么材料”。

默认选中：

- `changelog`：面向维护者的变更记录
- `release_notes`：面向用户的本次发布摘要
- `manifest`：Release Package manifest

按项目证据推荐但默认不选中：

- `customer_notes`：存在外部用户、客户门户或客户文档约定时推荐
- `sbom`：项目已有供应链、安全或合规要求时推荐
- `checksums`：发布可下载的二进制、压缩包或安装包时推荐
- `build`：项目要求在准备阶段固化候选构建产物时推荐；否则留给 `publish-release`
- `video`：用户提到发布视频，或本地 AI Cortex 安装中存在 `changelog-video` 时推荐

向用户展示每项的用途、默认选择、required/optional 状态及推荐依据。用户可以增删材料或调整 required；显式输入优先于默认值。用户已给出完整清单时，只展示归一化结果供确认，不重复提问。

示例确认界面：

```text
本次建议准备：
[默认/必需] changelog、release notes、Release Package manifest
[可选/推荐] checksums（检测到可下载二进制）
[可选] customer notes、SBOM、release video

是否按此清单继续？你可以增删材料，或将某项改为必需/可选。
```

只有当用户选择 `video` 后，才询问会改变结果的缺失参数；至少确认它是否 required。受众、语言、时长和形式若未提供，可使用明确展示的默认值。

### 4. 构造发布材料

先把 release range 归一化为 `change_items`：每项包含稳定 ID、类别、技术摘要、用户影响、来源 commit/需求、受众，以及按需的 module、breaking/migration、多语言标题、highlight 和 media。内部变化可留作技术证据，但不得自动进入用户材料。

再识别已有 generator，只生成用户确认的 changelog、release notes、customer notes、manifest、SBOM/checksum/build artifacts：技术 changelog 保留接口、配置、迁移和运维细节；用户 release notes 只写可感知价值。两者从同一组 change items 派生，不互相复制后再改写事实。不要重复实现 `commit-work`、`automate-tests` 或 `generate-github-workflow`。

#### changelog-video 集成边界

`changelog-video` 是随 AI Cortex 分发的本地可选发布材料 Skill，不是本 Skill 的内置实现。只在用户选择 `video` 后调用；传入 `decision=release`、项目标识、版本与通道、git range、已确认的 customer-facing change items、可用 media 引用、输出目录、required 状态和已确认偏好，消费其 `kind: video` artifact entry 与 check 结果。不得要求它重新解析 git 或长篇 Markdown，也不得让它决定版本、修改 changelog、创建 tag 或发送公告。

- 本地存在：调用 `changelog-video`，将带 producer 信息的 video entry 纳入 manifest。
- 本地缺失：不得从 skills.sh、GitHub 或其他注册表自动安装。`video.required=false` 时记录 `unavailable` 并继续；required 时保持 `draft` 并提示通过 AI Cortex 的 canonical 安装更新恢复本地副本。
- 执行失败：optional 时记录真实失败并继续其他材料；required 时阻塞 ready。

### 5. 执行门禁

运行项目已声明的最小相关测试、lint、构建或安全检查；可复用 `automate-tests` 的发现逻辑。优先使用项目批准的命令，同时遵守其明确禁止的验证方式。每项 check 记录命令、状态和 evidence。需要审查信号时使用已有 `review-diff` / `orchestrate-code-review`，不在此重写审查能力。

### 6. 预览与写入

默认 `dry_run=true`：展示发布/不发布结论、版本与通道、各版本域动作、范围、change items、将生成/修改的文件、材料缺口和门禁结果。用户确认后才写入材料与 manifest。本 Skill 不创建 commit/tag、不 push、不上传、不发送公告；分别交给 `publish-release` 和 `announce-release`。

## 输入与输出

输入可包含 `repo_path`、`version`、`release_channel`、`previous_tag`、`artifacts`、`required_artifacts`、`video_preferences`、`output_path` 和 `dry_run`（默认 `true`）。输出为 release/none 决策、用户确认后的材料清单，以及符合 [Release Package Spec](../../specs/release-package.md) 的 version domains、change items、artifacts、checks 和 readiness。

## 限制

- 未确认预览结果不得修改版本文件或发布材料。
- 未确认材料清单前不得生成材料；不得把所有可选材料默认选中。
- 不把 commit/tag、构建上传、registry 发布、GitHub Release 或通知发送混入准备阶段。
- 不仅凭 commit prefix 决定版本，不为保持一致而升级独立版本域。
- 不把可选视频能力失败误报为整体失败，也不伪造 ready。
- 不在运行时下载、注册或升级任何 Skill；只调用 AI Cortex 本地副本，项目本地约定优先。

## 自检

- [ ] manifest 含 decision、完整 SHA、range、version domains、artifacts、checks、status。
- [ ] 版本候选按用户影响判断并有证据；`none` 不产生空发布。
- [ ] 产品版本 canonical source、独立版本域和预发布通道已识别。
- [ ] 技术与用户材料来自同一组可追溯 change items，受众边界明确。
- [ ] required checks 与 artifacts 已逐项判定。
- [ ] 已展示默认与可选材料、用途、required 状态和推荐依据，并取得确认。
- [ ] changelog-video 只作为本地 vendored 可选 Skill 接入，缺失时未触发外部安装。
- [ ] dry-run 预览已展示，未发生 publication 或 communication side effect。

## 示例

### 示例 1：普通 patch release

输入“准备 1.4.2 发布，生成 changelog 和 release notes”。读取最近 tag，复用项目测试命令，生成材料与 manifest；门禁通过后输出 `ready` 预览，等待确认写盘。

### 示例 2：视频能力不可用

video 为 optional，但本地 AI Cortex 安装缺少 `changelog-video`。manifest 将 video 记为 `unavailable`；其余门禁通过时仍可 `ready`，并提示更新 canonical AI Cortex 安装后补材料，不给出第三方运行时安装命令。

### 示例 3：用户未指定材料

检测到项目发布二进制文件，但没有客户门户或 SBOM 约定。先默认选择 changelog、release notes、manifest，把 checksums 标为“推荐但未选”，把 customer notes、SBOM、video 列为可选；用户确认后才生成。

### 示例 4：无需新版本

range 中只有 CI 调整与不可见的测试重构。尽管 commit prefix 含 `fix`，实际用户行为未改变，因此输出 `decision=none`、保留产品版本和其他版本域、不生成发布材料，也不移交 `publish-release`。

### 示例 5：预发布通道推进

项目规则声明当前为 `2.0.0-beta.2`，且进入 rc 的验收条件已满足。Skill 提议 `2.0.0-rc.0` 并说明依据；API contract 版本没有变化，标记为 `preserve`，不跟随产品版本升级。
