---
name: changelog-video
description: Generate and validate an optional release video from confirmed Release Package change items using repository-local media tooling; never installs tools or decides or publishes the release.
description_zh: 使用仓库本地媒体工具，从已确认的 Release Package change items 生成并校验可选发布视频；不安装工具，也不决定或发布版本。
tags: [release, changelog, video, release-package]
version: 1.0.1
license: Apache-2.0
compatibility: Requires a video renderer already available through the target repository or runtime; never downloads one.
recommended_scope: project
metadata:
  author: ai-cortex
  origin: vendored-derived
  source-registry: ../SOURCES.yaml
triggers: [changelog video, release video, generate release video]
input_schema:
  type: free-form
  description: Confirmed Release Package identity and customer-facing change items; output directory; optional audience, language, duration, aspect ratio, narration, captions, media, and renderer preferences
output_schema:
  type: document-artifact
  description: A validated video artifact entry and check evidence, or an explicit unavailable/failed result; never a release decision or publication receipt
---

# 技能（Skill）：生成变更视频（Changelog Video）

## 目的与边界

把已确认的 Release Package `change_items` 转换为短发布视频，并返回可直接并入 package manifest 的 `kind: video` artifact entry。此 Skill 只负责视频材料，不重新分析 git、不决定版本、不修改 changelog、不创建 tag、不发布视频，也不发送公告。

本地副本由 AI Cortex 统一安装和更新。不得在运行时从 skills.sh、GitHub、raw URL 或其他注册表下载、注册或升级 Skill；外部来源仅用于维护期溯源，见 [`../SOURCES.yaml`](../SOURCES.yaml)。

## 输入契约

必需输入：

- `decision=release`、`project`、`version`、`release_channel` 和 `range`
- 已由 `prepare-release` 确认的 customer-facing `change_items`
- `output_dir`
- `required`，用于决定失败是否阻塞 Release Package readiness

可选输入：`audience`、`language`、`duration_seconds`、`aspect_ratio`、`narration`、`captions`、`media`、项目品牌资料和 renderer 偏好。每个 change item 至少应有稳定 ID、用户影响、受众和来源；缺少事实时返回缺口，不回读 git 猜测。

当输入来自 `prepare-release` 时，沿用已经确认的选择，只询问会改变结果的缺失信息。独立调用时先展示下列可编辑默认值并一次确认：

```text
[默认] 受众：customer
[默认] 语言：沿用 release notes
[默认] 时长：45–60 秒
[默认] 画幅：16:9
[默认] 字幕：有旁白时必需
[可选] 旁白、项目品牌素材、已有产品录屏

是否按此设置生成？你可以修改任一项。
```

## 行为

### 1. 校验发布事实

确认 `decision=release`，版本、通道、range 与 change items 齐全。只选择受众匹配且具有可验证 `user_impact` 的条目；`internal` 条目不得进入客户视频，除非用户明确改变受众。

### 2. 发现本地制作路径

按项目文档、配置、现有脚本、CI 和当前运行时工具发现已经可用的视频 renderer、字幕、音频和媒体处理能力，优先复用项目约定。只使用本地文件或当前上下文已经授权的工具。

没有可用 renderer 时：

- `required=false`：返回 `status: unavailable` 和缺失证据，不安装任何东西。
- `required=true`：返回阻塞结果，由 `prepare-release` 保持 package 为 `draft`。

### 3. 形成脚本和分镜

- 用一句话说明本次版本带来的核心变化，再选择 3–5 个最有用户价值的 change items。
- 每个口播或画面事实必须映射到 change item ID；迁移要求和 breaking change 不得弱化。
- 优先表现用户体验的变化、真实产品界面、经提供素材支持的类比或简洁图示；无法诚实可视化时使用文字卡，不发明不存在的 UI。
- 旁白文本与屏幕文字分别维护：屏幕文字简短，旁白可以补充上下文；二者共享同一事实来源。
- 输出 storyboard 预览，列出时长、场景、来源 ID、所需素材和将创建的文件，确认后才渲染。

### 4. 渲染并限制写入

只在用户确认后调用已发现的本地制作路径。所有中间文件和最终文件必须位于 `output_dir`；不得修改产品源码、版本文件、changelog 或 Release Package 之外的发布状态。不得为完成渲染而安装 Skill、CLI、字体、媒体或模型。

### 5. 校验产物

至少验证：

- 视频文件存在且非空，容器、时长、分辨率与确认值一致；
- 抽取开头、中段、结尾帧，检查黑帧、裁切、不可读文字和错误素材；
- 选择旁白时验证音轨存在，选择字幕时验证字幕在有声区间可见；
- 视频中的版本、功能、迁移和 CTA 与 Release Package 一致；
- 输出目录不含凭据、临时 token 或未授权媒体。

任一 required gate 失败时不得返回 `status: present`。

## 输出契约

成功时返回：

```yaml
artifact:
  kind: video
  audience: customer
  path: <output_dir>/release-<version>.mp4
  required: false
  status: present
  source: [<change-item-id>]
  producer:
    skill: changelog-video
    version: 1.0.1
    origin: vendored-derived
    source_registry: skills/SOURCES.yaml
checks:
  - name: changelog-video
    status: passed
    evidence: <renderer and validation summary>
    required: false
```

不可用或失败时返回同一结构，将 `path` 设为 `null`，artifact status 使用 `unavailable` 或 `failed`，对应 check status 使用 `skipped` 或 `failed`；不得伪造 MP4、renderer 回执或验证结果。

## 与 Release Skills 的边界

- `prepare-release` 决定是否选择视频、提供 change items，并消费 artifact/check 结果。
- `changelog-video` 负责脚本、分镜、渲染和媒体验证。
- `publish-release` 只发布已在 package 中登记的视频，不重新生成。
- `announce-release` 只链接或分发已发布视频。

## 上游说明

本 Skill 的“以体验为画面、限制口播条目、分离口播与屏幕文字、抽帧验证”等思路派生自 HyperFrames `changelog-video`。AI Cortex 版本不包含上游品牌素材、字体、音乐、固定语音、仓库路径或 sibling skills；精确来源与固定 commit 见来源清单，上游许可证见 [`LICENSE.upstream`](LICENSE.upstream)。

## 自检

- [ ] 输入来自已确认的 Release Package change items，没有重新解析 git 决定事实。
- [ ] 已展示并确认受众、语言、时长、画幅、字幕/旁白和素材选择。
- [ ] 只使用本地或已授权工具，未安装或下载任何 Skill 或 renderer。
- [ ] 每个场景可追溯到 change item，未泄露 internal 内容。
- [ ] 视频、音频、字幕和抽样帧已按选择验证。
- [ ] 输出只包含 artifact/check 结果，不创建 tag、发布或公告。
