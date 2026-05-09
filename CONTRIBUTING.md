# 贡献指南

感谢你对 AI Cortex 的贡献兴趣。本文档说明如何贡献技能、规则与改进。

## 快速开始

1. Fork 本仓库
2. 创建功能分支：`git checkout -b feat/your-skill-name`
3. 按下列指南修改
4. 提交 Pull Request

## 新增技能

技能遵循 [agentskills.io](https://agentskills.io) 标准格式。推荐使用 `/skill-creator` 自动生成骨架。

1. **起草**：在 `skills/<skill-name>/SKILL.md` 编写技能；YAML frontmatter 含必填字段（name、description、tags、version、license）
2. **补充文件**：可选 `README.md` 作为快速参考
3. **注册**：将技能添加到 `skills/INDEX.md`
4. **提交 PR**

### 命名约定

详见 [docs/architecture/asset-naming.md](docs/architecture/asset-naming.md)（4 类资产的命名规范集中文档）。

## 新增规则

规则位于 `rules/` 目录，须在 `rules/INDEX.md` 注册。遵循既有规则格式。下游消费方（如 Cursor / Trae）按各自方式拷贝或符号链接 `rules/`，本仓库不提供安装工具。

## 版本管理

本项目遵循 [Semantic Versioning](https://semver.org/)。修改技能时：

- **PATCH**（1.0.0 → 1.0.1）：勘误、元数据调整、引用更新
- **MINOR**（1.0.0 → 1.1.0）：新步骤、示例改进、交互策略变更
- **MAJOR**（1.0.0 → 2.0.0）：破坏性结构变更

更新 SKILL.md frontmatter 版本号后，同步更新 `skills/INDEX.md` 中的对应条目。

## 行为准则

保持专业、建设性与尊重。聚焦贡献的技术价值。

## 问题？

使用「question」标签提交 Issue，或查看 [技能目录](skills/INDEX.md) 了解既有能力。
