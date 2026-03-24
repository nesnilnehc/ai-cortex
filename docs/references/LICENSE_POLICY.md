---
artifact_type: reference
created_by: ai-cortex
lifecycle: living
created_at: 2026-03-24
status: active
---

# 许可证策略

本文件定义 AI Cortex 项目中技能及其参考来源的许可证要求。

---

## 1. 技能本体

- 本仓库所有技能（`skills/*/SKILL.md`）必须声明 `license: MIT`。
- 验证：`npm run verify:skill-structure` 强制此约束。

---

## 2. 参考来源（evolution.sources）

当技能在 `metadata.evolution.sources` 中引用外部仓库或技能时：

- **允许的许可证**：MIT、Apache-2.0、BSD-3-Clause、BSD-2-Clause 等与 MIT 兼容的宽松许可证。
- **必须声明**：每个 source 须包含 `license` 字段，且不得使用不允许 fork/integration 的许可证。
- **上游未检出时**：若上游仓库根目录无 LICENSE 文件，在 evolution.sources 中可按惯例声明（如 MIT），并注明「as declared by AI Cortex；upstream verification recommended」。见 [ATTRIBUTIONS.md](./ATTRIBUTIONS.md)。

---

## 3. 参考

- [spec/skill.md](../../spec/skill.md) 第 2.1 节：演进元数据
- [ATTRIBUTIONS.md](./ATTRIBUTIONS.md)：参考来源枚举表
