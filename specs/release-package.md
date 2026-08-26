---
id: RELEASE_PACKAGE_SPEC_V1
name: Release Package Schema
description: Structural contract for release decisions, version domains, change evidence, artifacts, and stage results shared across release workflows.
version: 1.2.1
status: active
lifecycle: living
created_at: 2026-08-26
scope: |
  Defines the Release Package object shared by release preparation, publication,
  and communication skills. It does not define a CI provider, registry API,
  deployment process, or media-generation implementation.
related:
  - ./spec-modeling.md
  - ./universal-notification.md
  - ../skills/prepare-release/SKILL.md
  - ../skills/changelog-video/SKILL.md
  - ../skills/publish-release/SKILL.md
  - ../skills/announce-release/SKILL.md
---

# Release Package 规范

> **数据契约**：定义跨发布准备、发布执行与发布沟通阶段共享的发布包结构

## 1. 定位与适用范围

Release Package 是一次候选发布的可审计载体，把版本、提交范围、发布材料、质量证据与阶段状态放在同一个对象中。

适用：准备版本、执行发布、生成发布沟通材料，以及在阶段之间传递发布证据。

不适用：具体平台的上传 API、部署协议、媒体生成算法或渠道投递格式。

## 2. 心智模型

Release Package 回答六个问题：Decision（是否值得形成新版本）、Identity（哪个项目/提交范围）、Versions（哪些版本域变化）、Changes（用户与技术上改变了什么）、Artifacts（有哪些材料）、State（当前阶段与证据）。

## 5. 正文结构契约

### 5.1 顶层字段

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `schema_version` | string | 必 | Release Package schema 版本 |
| `project` | string | 必 | 项目标识 |
| `decision` | enum | 必 | `release` / `none` |
| `version` | string | 条件 | `decision=release` 时必填；不带 `v` 前缀的 SemVer |
| `release_channel` | string | 条件 | `decision=release` 时必填，如 `alpha` / `beta` / `rc` / `stable` |
| `version_source` | string | 条件 | `decision=release` 时必填；产品版本的 canonical source 路径 |
| `version_domains` | object | 必 | 产品、构建、API、协议等独立版本域及本次动作 |
| `commit` | string | 必 | 发布对应的完整提交 SHA |
| `range` | string | 必 | 从上一发布到本次提交的 git range |
| `status` | enum | 必 | `draft` / `not_required` / `ready` / `published` / `announced` |
| `change_items` | array | 条件 | `decision=release` 时必填；供材料、视频和公告复用的结构化变化 |
| `artifacts` | object | 必 | 发布材料索引 |
| `checks` | array | 必 | 已执行门禁及结果 |
| `publication` | object | 条件 | `status` 为 `published` 或更晚时必填 |
| `communication` | object | 条件 | `status` 为 `announced` 时必填 |

### 5.2 Artifact entry

每个 entry 至少包含 `path`、`kind`、`audience`、`required`、`status` 和 `source`。`kind` 可为 `changelog`、`release_notes`、`customer_notes`、`manifest`、`sbom`、`checksums`、`build`、`video` 或 `other`；`status` 可为 `planned`、`present`、`skipped`、`unavailable` 或 `failed`。`audience` 至少区分 `technical`、`operator`、`customer` 和 `internal`；`source` 指向生成该材料的 change items 或权威文件。由 Skill 生成的材料还应包含 `producer`，至少记录本地 Skill 名称、版本和来源分类：AI Cortex 原创 Skill 使用 `origin: native`，外部派生本地副本使用 `origin: vendored-derived` 并附 `source_registry`。`video` 默认是可选材料；required artifact 只有在 `status=present` 时才满足 readiness。

### 5.3 Version domain entry

每个版本域至少包含 `current`、`source` 和 `action`（`bump` / `preserve` / `derive`）。只有产品版本域可默认参与 SemVer bump；构建、API、协议、数据格式或 Prompt 版本不得仅为“保持一致”而联动升级。

### 5.4 Change item

每项变化至少包含稳定 `id`、`kind`（`feature` / `improvement` / `fix` / `breaking` / `internal`）、`summary`、`user_impact`、`sources` 和 `audiences`。可选字段包括 `module`、多语言 `title` / `body`、`migration`、`highlight` 和 `media`。技术 changelog、用户 release notes、视频与公告应从同一组 change items 派生，而不是相互复制后各自改写事实。

### 5.5 Check entry

每个 check 至少包含 `name`、`status`（`passed` / `failed` / `skipped`）、`evidence` 和 `required`。required check 失败或缺 evidence 时不得变为 `ready`。`decision=none` 时状态必须为 `not_required`，不得创建 publication 结果。

### 5.6 Publication entry

`publication` 至少包含目标 commit、tag、provider、逐步骤状态与成功 receipt。逐步骤状态使用 `not_started` / `partially_applied` / `complete` / `failed`，覆盖版本同步、release commit、validation、tag、build/package 和 provider publish。该状态用于失败恢复，不得仅以最终布尔值覆盖中间事实。

### 5.7 Communication entry

`communication` 至少包含目标 audience、逐渠道 required/optional 标记、投递状态和 receipt。只有至少一个渠道成功且所有 required 渠道成功时，顶层状态才可从 `published` 变为 `announced`；optional 渠道失败必须保留，但不阻塞该状态转换。

## 6. 反模式

- ❌ 三个 Skill 各自定义版本、制品或状态字段
- ❌ 仅按 commit prefix 或 commit 数量决定 SemVer，而不检查实际用户影响
- ❌ 为保持版本号一致而联动升级 API、构建、Prompt 等独立版本域
- ❌ 用 `published` 表示“只创建了本地 tag”
- ❌ 把可选 `video` 材料默认为发布阻塞项
- ❌ 没有提交 SHA 或 git range，导致内容不可追溯
- ❌ 将渠道私有消息块直接塞进 Release Package

## 7. 示例

### 7.1 可发布包

```yaml
schema_version: 1.2.1
project: example-service
decision: release
version: 2.4.0
release_channel: stable
version_source: package.json
version_domains:
  product: {current: 2.3.1, source: package.json, action: bump}
  api: {current: 1.8.0, source: api/openapi.yaml, action: preserve}
commit: 0123456789abcdef0123456789abcdef01234567
range: v2.3.1..0123456
status: ready
change_items:
  - id: export-filter
    kind: feature
    summary: Add saved filters to exports
    user_impact: Users can reuse filters when exporting reports
    sources: [abc1234]
    audiences: [technical, customer]
artifacts:
  changelog: {kind: changelog, audience: technical, path: CHANGELOG.md, required: true, status: present, source: change_items}
  release_notes: {kind: release_notes, audience: customer, path: RELEASE_NOTES.md, required: true, status: present, source: change_items}
  video: {kind: video, audience: customer, path: null, required: false, status: skipped, source: change_items, producer: {skill: changelog-video, version: 1.0.1, origin: vendored-derived, source_registry: skills/SOURCES.yaml}}
checks:
  - {name: tests, status: passed, evidence: "pytest", required: true}
```

### 7.2 无需形成新版本

```yaml
schema_version: 1.2.1
project: example-service
decision: none
version_domains:
  product: {current: 2.3.1, source: package.json, action: preserve}
commit: 0123456789abcdef0123456789abcdef01234567
range: v2.3.1..0123456
status: not_required
artifacts: {}
checks: []
```

### 7.3 缺少可选视频能力

```yaml
artifacts:
  video: {kind: video, audience: customer, path: null, required: false, status: unavailable, source: change_items}
checks:
  - {name: changelog-video, status: skipped, evidence: "vendored local skill is not installed", required: false}
```

## 8. 与其他资产关系

- `prepare-release` 构造并校验 Release Package。
- `changelog-video` 消费已确认的 change items，并返回可选 video artifact 与 check 结果。
- `publish-release` 消费 `ready` 包并写入 publication 结果。
- `announce-release` 消费 `published` 包并写入 communication 结果。
- [Universal Notification](./universal-notification.md) 定义通知结构；渠道投递流程由 [INP](../protocols/im-notification-delivery.md) 定义。
