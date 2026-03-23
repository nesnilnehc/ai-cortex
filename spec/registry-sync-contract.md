# 注册表同步契约

**状态**：MANDATORY  
**版本**：1.0.0  
**范围**：manifest.json、skills/INDEX.md、skills/*/SKILL.md、marketplace.json

**变更记录**：

- v1.0.0 (2026-03-06)：初版；定义由 verify-registry.mjs 执行的同步规则。

---

## 1. 目的

本契约规定技能注册表制品须保持的一致性。`scripts/verify-registry.mjs` 强制执行这些规则。`skills/INDEX.md` 由 manifest 与 SKILL frontmatter 生成。

---

## 2. 权威来源

| 制品 | 路径 | 角色 |
| :--- | :--- | :--- |
| manifest.json | 仓库根 | 可执行能力列表；`capabilities[].name` 与 `capabilities[].path` |
| skills/INDEX.md | skills/ | 生成的人工可读目录；含 name、tags、version、stability、purpose 的表行 |
| skills/{name}/SKILL.md | skills/ | 单技能定义；含 name、version、tags 的 YAML frontmatter |
| .claude-plugin/marketplace.json | 仓库根 | Claude 插件子集；`plugins[].skills[]` |

---

## 3. 同步规则

### 3.1 manifest.json ↔ skills/

- 每个 `manifest.capabilities[].name` 须有目录 `skills/{name}/` 且包含 `SKILL.md`。
- 每个 `manifest.capabilities[].path` 须等于 `skills/{name}/SKILL.md`。
- 每个包含 `SKILL.md` 的目录 `skills/{name}/` 须出现在 `manifest.capabilities` 中。

### 3.2 skills/INDEX.md ↔ manifest.json

- 生成的 INDEX 须包含 manifest.json 中的每个技能。
- 生成的 INDEX 不得包含 manifest.json 中不存在的技能。
- 生成的 skills/INDEX.md 中不得有重复技能名。

### 3.3 skills/INDEX.md ↔ skills/{name}/SKILL.md

- 对于每行 INDEX，对应 SKILL.md 的 frontmatter 须有：
  - `name` 等于技能名（与目录名一致）。
  - `version` 等于 INDEX 中的版本。
  - `tags` 与 INDEX 中的 tags 相等（顺序无关）。
  - Purpose 来源：`description_zh`（若存在）或 `description`；当项目有 `docs/LANGUAGE_SCHEME.md` 时，优先 `description_zh`。

### 3.4 marketplace.json

- `plugins[].skills[]` 中的每个技能路径须解析为 manifest 与 INDEX 中存在的技能。

---

## 4. 验证

在仓库根运行：

```bash
node scripts/verify-registry.mjs
```

运行前，`generate-skills-docs.mjs` 会从源重新生成 INDEX.md 与 skillgraph.md。若有同步规则违反，脚本以 1 退出。

---

## 5. 更新流程

新增技能时：

1. 创建带有效 frontmatter 的 `skills/{name}/SKILL.md`。
2. 将能力加入 `manifest.json` 的 capabilities 数组。
3. 重新生成 `skills/INDEX.md`。
4. 可选：加入 marketplace.json。
5. 运行 `node scripts/verify-registry.mjs` 确认同步。
