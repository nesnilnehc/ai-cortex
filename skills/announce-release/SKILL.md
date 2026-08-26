---
name: announce-release
description: Create and optionally deliver grounded release announcements from a published Release Package across available channels; never owns changelog generation.
description_zh: 基于已发布的 Release Package 生成并可选投递多渠道发布公告；不负责 changelog 生成。
tags: [release, announcement, communication, notification]
version: 1.1.1
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [announce release, release announcement, release communication, notify release]
input_schema:
  type: free-form
  description: Published Release Package; target audiences/channels; optional delivery request
output_schema:
  type: document-artifact
  description: Grounded announcement drafts and, when authorized and supported, delivery receipts linked to the Release Package
---

# 技能（Skill）：公告发布（Announce Release）

## 目的

将已发布 Release Package 的事实转换为面向不同受众的公告，并在用户明确要求且运行时具备渠道能力时投递。材料生成归 `prepare-release`，版本发布归 `publish-release`。

## 核心目标

产出与已发布版本事实一致的公告；在渠道、权限和用户确认均满足时逐渠道投递，并保留可审计的 delivery receipt。

## 行为

1. 要求 package 为 `decision=release` / `status=published`，且版本、通道、tag、commit、发布回执和所有 required artifact 路径齐全；optional artifact 可为 `skipped` / `unavailable` / `failed`，不得因此阻塞普通公告。`not_required` 或缺少 required 事实时停止，不猜测。
2. 优先消费 package 的 `change_items`，按 `audiences`、`user_impact`、breaking/migration、语言、highlight 和 media 选择内容；artifact 用于补充已审核文案与链接。只有旧 package 没有 change items 时才回退解析 changelog/release notes，并明确标记推断。
3. 按受众生成 internal、customer-facing、technical/operator 草稿。同一事实可按受众改写表达，但版本、用户影响、迁移动作与来源不得漂移。结构遵循 [Universal Notification](../../specs/universal-notification.md)，实际 IM 投递遵循 [INP](../../protocols/im-notification-delivery.md)。
4. 发现可用的邮件、IM、网站、客户门户或项目 provider 工具，映射发送能力、目标、链接/附件支持和回执，并把每个目标渠道明确为 required 或 optional。没有工具时只输出草稿。
5. 投递前展示渠道、受众、正文、链接、权限和影响；确认后发送。逐渠道记录成功、失败和跳过。
6. 只有至少一个目标渠道收到成功回执、所有 required 渠道均成功，且用户要求记录状态时，才将 communication 写为 `announced`；required 渠道失败或没有成功投递时保持 `published`。optional 渠道失败必须保留回执，但不阻塞 `announced`。

## 输入与输出

输入为 `published` Release Package、目标受众/渠道和可选的投递请求。输出为按受众区分的公告草稿；在获得确认且具备渠道能力时，附逐渠道 delivery receipt，并按 Spec 记录 communication 结果。

## 限制

- 不生成或改写 `CHANGELOG.md` 的权威内容，不创建 tag，不发布构建产物。
- 不把 `internal` change item 自动暴露给 customer audience；不把技术 changelog 逐句复制成客户公告。
- 不把未发布版本、未验证功能或视频存在性写成事实。
- 没有渠道工具、账号或目标时不发送；不把凭据写入草稿或 package。
- video 仅作为 optional artifact 链接；缺失不阻塞普通公告，除非项目明确要求。

## 自检

- [ ] package 为 `decision=release` / `status=published`，公告中的版本/tag/commit 与其一致。
- [ ] 优先使用 change items，audience、语言、highlight、migration 和 media 选择可追溯。
- [ ] 每条事实可追溯到 package artifact 或发布回执。
- [ ] 渠道能力已发现，投递前已展示并获确认。
- [ ] 每个渠道有独立 receipt，失败未被隐藏。
- [ ] `announced` 只在符合条件的成功回执后写入。

## 示例

### 示例 1：只生成公告草稿

用户要求准备 v3.2.0 客户公告但未授权发送。读取 published package，生成客户版与技术版 Markdown 草稿，不调用渠道工具，也不改变状态。

### 示例 2：部分渠道失败

邮件成功，但被标为 required 的企业 IM 未连接。输出邮件 receipt 与 IM 未发送原因，package 保持 `published`，不把 required 渠道未完成的部分成功标为 `announced`。
