# 审查代码库（review-codebase）

对给定路径（文件 / 目录 / 仓库）做 scope-only 原子审查，覆盖 5 维：模块边界、模式一致性、跨模块依赖、技术债、接口稳定性。

## 与同伴技能的关系

- `review-diff` — 二选一伙伴：本技能看快照，review-diff 看 git 变更
- `orchestrate-code-review` — 编排器：把本技能作为 scope 步候选

## 何时使用

- 新模块审查：给定 `src/auth/` 看当前结构
- 遗留路径审计：给定路径看技术债与边界问题
- 采样审查：同事指定的文件或目录，无需 diff

## 何时不用

- 仅审查 git 变更 → `review-diff`
- 安全 / 性能 / 架构 cognitive 维度 → `review-security` / `review-performance` / `review-architecture`
- 语言 / 框架特定约定 → `review-<lang>` / `review-<framework>`

## 输入

- 路径（一个或多个 file / dir）
- 可选：focus 提示

## 输出

- Findings list（含 file:line 引用），按文件或模块分组

## 完整定义

见 [SKILL.md](./SKILL.md)。
