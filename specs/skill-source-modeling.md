---
id: SKILL_SOURCE_MODELING_SPEC_V1
name: Vendored Skill Source Registry Schema
description: Defines the source, pin, license, modification, and update contract for externally derived Skills vendored into AI Cortex.
version: 1.0.0
status: active
lifecycle: living
created_at: 2026-08-26
scope: |
  Applies to externally derived Skills distributed by AI Cortex and recorded in skills/SOURCES.yaml.
  It does not model ordinary software packages, CLI tools, APIs, or informational references.
related:
  - ../skills/SOURCES.yaml
  - ../docs/adr/0011-vendor-external-skills.md
  - ../docs/references/LICENSE_POLICY.md
  - ../docs/references/ATTRIBUTIONS.md
---

# 外部派生 Skill 来源规范

> **数据契约**：定义 AI Cortex 内 vendored 外部派生 Skill 的来源、固定版本、许可证、修改和更新记录

## 1. 定位与适用范围

`skills/SOURCES.yaml` 是 AI Cortex 当前外部派生 Skill 的机器可读来源清单。凡是复制、改编、fork 或实质借用外部 Skill 工作流并继续作为 AI Cortex Skill 分发的本地目录，都必须登记；普通工具依赖、行业标准、文档链接和已删除的历史 Skill 不登记。

运行时只加载 `skills/` 下的本地副本。来源清单用于维护、审计、许可证合规和生成 SPDX，不是依赖解析器，也不授权 Agent 联网安装。

## 2. 心智模型

每个登记项必须回答五个问题：

| 问题 | 字段 |
|---|---|
| 本地调用什么？ | `local_path`、`local_version` |
| 从哪里派生？ | `upstream.repository`、`upstream.path` |
| 固定到什么内容？ | `upstream.ref`、`tree`、`skill_digest` |
| 以什么许可分发？ | `license`、`notice` |
| AI Cortex 改了什么、如何更新？ | `modifications`、`update_policy` |

“已登记”不等于“运行时可下载”；只有本地目录存在、已在 `skills/INDEX.md` 注册并由 canonical installer 同步后，Agent 才可调用。

## 3. 命名约定

- 来源清单固定为 `skills/SOURCES.yaml`。
- Skill key、`local_path` 目录名和 `SKILL.md` 的 `name` 必须一致。
- 清单中的本地路径一律相对仓库根目录。上游许可证副本可放在目标 Skill 的 `LICENSE.upstream`；集中致谢使用 `docs/references/THIRD_PARTY_NOTICES.md`。

## 5. 正文结构契约

### 5.1 根结构

```yaml
schema_version: "1.0"
policy:
  distribution: vendored-only
  runtime_external_install: forbidden
  update: reviewed
skills: {}
```

`distribution` 和 `runtime_external_install` 是全仓不变量，不得为单个 Skill 增加 `on-demand`、`remote` 或 `auto-install` 例外。

### 5.2 Skill entry

| 字段 | 类型 | 必填 | 约束 |
|---|---|---|---|
| `local_path` | path | 必 | `skills/<name>`，目录必须存在 |
| `local_version` | SemVer | 必 | 与本地 `SKILL.md` 一致 |
| `origin` | enum | 必 | 当前固定为 `vendored-derived` |
| `upstream.repository` | HTTPS Git URL | 必 | 仓库 URL，不使用 raw URL |
| `upstream.path` | path | 必 | 上游 Skill 根目录 |
| `upstream.ref` | full commit SHA | 必 | 40 位 commit，不得为 branch/tag/`latest` |
| `upstream.tree` | digest | 必 | 固定上游目录 Git tree |
| `upstream.skill_digest` | digest | 必 | 上游 `SKILL.md` 的 SHA-256 |
| `license` | SPDX expression | 必 | 已核验的上游/本地分发许可证 |
| `notice` | path | 必 | 相对仓库根目录的本地许可证或 NOTICE 路径，文件必须存在 |
| `update_policy` | enum | 必 | `reviewed-merge` 或 `reviewed-port` |
| `modifications` | list[string] | 必 | 至少一项，说明本地差异 |

### 5.3 更新校验

维护期更新必须先固定新的 commit，比较 upstream tree 与本地差异，复核许可证和资产，再更新本地副本、版本、来源清单、致谢和 SPDX 输入。更新不得发生在业务 Skill 调用过程中。

## 6. 反模式

- ❌ Skill 正文要求 Agent 执行 `npx skills add`、clone 外部仓库或读取浮动 raw URL。
- ❌ `upstream.ref` 使用 `main`、tag、版本范围或省略 commit。
- ❌ 复制外部 Skill 但只写 `author: ai-cortex`，没有来源和 notice。
- ❌ 只登记一个入口 Skill，却遗漏复制进仓库的 sibling Skill 或资源。
- ❌ 把外部 CLI/API 当成外部 Skill 登记，或借来源清单自动安装软件依赖。

## 7. 示例

```yaml
skills:
  example-skill:
    local_path: skills/example-skill
    local_version: 1.0.0
    origin: vendored-derived
    upstream:
      repository: https://github.com/example/skills.git
      path: skills/example-skill
      ref: 0123456789abcdef0123456789abcdef01234567
      tree: sha1:0123456789abcdef0123456789abcdef01234567
      skill_digest: sha256:0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
    license: MIT
    notice: docs/references/THIRD_PARTY_NOTICES.md
    update_policy: reviewed-merge
    modifications: [Adapted output contract]
```

## 8. 与其他资产关系

- [ADR 0011](../docs/adr/0011-vendor-external-skills.md) 决定只采用 vendored 分发策略。
- [许可证策略](../docs/references/LICENSE_POLICY.md) 规定许可核验和 notice 保留。
- [来源与致谢](../docs/references/ATTRIBUTIONS.md) 是人类可读视图。
- Release Package 的 SPDX artifact 可从本清单和仓库内容生成，但 SPDX 不参与运行时 Skill 发现。
