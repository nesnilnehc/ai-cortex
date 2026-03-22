# 贡献指南

感谢你对 AI Cortex 的贡献兴趣。本文档说明如何贡献技能、规则与改进。

## 快速开始

1. Fork 本仓库
2. 创建功能分支：`git checkout -b feat/your-skill-name`
3. 按下列指南修改
4. 运行验证：`npm run verify && node scripts/verify-skill-structure.mjs`
5. 提交 Pull Request

## 新增技能

所有技能须符合 [技能规范](spec/skill.md)。质量保障流程：

1. **起草**：按规范编写 `skills/<skill-name>/SKILL.md`
2. **补充文件**：在技能目录创建 `README.md` 与 `agent.yaml`
3. **注册**：将技能加入 `manifest.json`（`skills/INDEX.md` 由脚本生成）
4. **验证**：运行 `node scripts/verify-registry.mjs && node scripts/verify-skill-structure.mjs`
5. **提交 PR**：CI 将自动校验注册表同步与技能结构

### 技能清单

- [ ] 目录名为 kebab-case，与 YAML `name` 一致
- [ ] YAML 元数据含必填字段（name, description, tags, version, license）
- [ ] 含所有必填标题（Purpose, Core Objective, Use Cases, Behavior, Input & Output, Restrictions, Self-Check, Examples）
- [ ] Core Objective 含 Primary Goal、Success Criteria（3–6 项）、Acceptance Test
- [ ] Self-Check 与 Success Criteria 对齐
- [ ] Skill Boundaries 定义技能不处理的内容
- [ ] 至少 2 个示例（含一个边界情况）
- [ ] 从 manifest 与 frontmatter 重新生成 `skills/INDEX.md`
- [ ] 更新 `manifest.json` 以包含新能力
- [ ] `verify-registry.mjs` 与 `verify-skill-structure.mjs` 通过

### 命名约定

使用 `verb-noun` 格式（如 `review-typescript`、`generate-standard-readme`）。审查类技能遵循现有模式：

- 语言：`review-<language>`（如 `review-python`）
- 框架：`review-<framework>`（如 `review-react`）
- 库：`review-<domain>-usage`（如 `review-orm-usage`）
- 认知：`review-<concern>`（如 `review-security`）

## 新增规则

规则位于 `rules/` 目录，须在 `rules/INDEX.md` 注册。遵循既有规则格式。使用 `install-rules` 技能将规则安装到 Cursor。

## 版本管理

本项目遵循 [Semantic Versioning](https://semver.org/)。修改技能时：

- **PATCH**（如 1.0.0 → 1.0.1）：勘误、元数据调整、引用更新
- **MINOR**（如 1.0.0 → 1.1.0）：新步骤、示例改进、交互策略变更
- **MAJOR**（如 1.0.0 → 2.0.0）：破坏性结构变更

在 SKILL.md 的 YAML frontmatter 中更新版本，然后重新生成 `skills/INDEX.md`。

## 行为准则

保持专业、建设性与尊重。聚焦贡献的技术价值。

## 问题？

使用「question」标签提交 Issue，或查看 [技能目录](skills/INDEX.md) 了解既有能力。
