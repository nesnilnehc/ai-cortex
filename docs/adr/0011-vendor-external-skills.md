---
artifact_type: adr
created_by: decision-record
lifecycle: snapshot
created_at: 2026-08-26
status: accepted
description: 外部派生 Skill 统一以审核后的本地副本分发，禁止 Agent 在运行时按需下载安装
---

# ADR 0011：统一 vendored 外部 Skill 管理

## 背景

Release Skills 引入 `changelog-video` 后，出现了两种外部 Skill 管理候选：把审核后的副本纳入 AI Cortex，或只声明远端来源并让 Agent 在调用时安装。后一种方案依赖网络、浮动上游、客户端安装行为和会话重新发现机制；同一能力也可能在不同机器得到不同内容。现有 `bin/cortex` 已经把仓库作为 canonical source 安装到各 Agent，因此并行维护第二套运行时解析方式会破坏单一来源。

## 决策

所有被 AI Cortex Skill 调用、编排或对外承诺的外部派生 Skill，必须以审核后的本地副本存在于 `skills/`，在 `skills/SOURCES.yaml` 固定上游仓库、路径、commit、digest、许可证和本地修改，并由 `bin/cortex install/update` 与其他 Skill 一起分发。

Agent 运行时不得从 skills.sh、GitHub、raw URL 或其他注册表下载、注册或更新 Skill。外部同步只发生在维护流程中，经过差异与许可证审核后形成新的 AI Cortex commit。

## 替代方案

- **运行时按需安装**：被拒。依赖网络和客户端实现，安装后还可能需要新会话；浮动来源会使同一 Release Package 的行为不可复现。
- **按风险混合 vendored 与 on-demand**：被拒。调用方必须理解两套缺失、授权、升级和回滚语义，增加编排复杂度。
- **只记录 SPDX**：被拒。SPDX 适合发布与审计，不提供 Skill 解析、安装或调用语义。

## 后果

- Agent 调用只依赖本地 `skills/`，行为可复现且符合仓库默认禁止外部抓取的规则。
- `commit-work` 作为 MIT 派生副本恢复真实来源；`changelog-video` 以去品牌、无 sibling-skill 下载的 Apache-2.0 派生版本纳入仓库。
- AI Cortex 维护者承担上游监测、合并、许可证和 NOTICE 更新成本。
- 可选 Skill 本地缺失时只报告 canonical AI Cortex 安装不完整，不提供第三方即时安装分支。
