# 技能翻译人工复核清单 (Skills Translation Manual Review)

**生成日期**：2026-03-21  
**脚本**：`scripts/translate-skills-zh.py`  
**范围**：48 个技能 (skills/) 的 SKILL.md 与 README.md

---

## 已完成自动翻译

所有 48 个技能均已通过脚本完成首轮翻译，包括：

- SKILL.md：frontmatter 添加 `description_zh`；正文翻译
- README.md：全文翻译
- 代码块、YAML、表格结构已保留

---

## 建议人工复核的技能

### 高优先级（术语/规范一致性）

| 技能 | 问题类型 | 说明 |
| :--- | :--- | :--- |
| discover-docs-norms | 术语 | `.ai-cortex/Product-norms.yaml` 应为 `.ai-cortex/artifact-norms.yaml`（与 spec/artifact-norms-schema.md 一致） |
| bootstrap-docs | 术语 | `Product-contract` → `artifact-contract`；`Product-norms-schema` → `artifact-norms-schema`；路径需与 spec 一致 |
| assess-docs | 术语 | 同上 |
| plan-next, align-architecture, capture-work-items | 术语 | `Product-norms` / `artifact-norms` 一致性 |

### 中优先级（技能名与链接）

| 技能 | 问题 | 说明 |
| :--- | :--- | :--- |
| define-mission, define-vision, define-north-star | 技能名 | 文中 `设计战略目标`、`define-里程碑` 等应为 `design-strategic-goals`、`define-milestones`（kebab-case） |
| design-strategic-goals, define-milestones, define-roadmap | 同上 | 技能间引用应使用英文标识符 |
| define-strategic-pillars | 同上 | 转交说明中的技能名 |

### 低优先级（语气与可读性）

| 技能 | 建议 |
| :--- | :--- |
| 含长列表的技能 | 检查列表项是否符合中文技术写作规范（中英间距、术语首次出现加英文） |
| generate-standard-readme | 标题 `# 技能（Skill）：` 与 `技能 (Skill)` 格式统一 |
| README 的 ASQM 表 | 表头 `Dimension`、`agent_native` 等保持英文，与 `docs/LANGUAGE_SCHEME.md` 一致 |

---

## 已自动修复项

- `**癌症目标**` → `**首要目标**`（Primary Goal 误译）
- `**财务目标**` → `**首要目标**`
- `## 目的（目的）` → `## 目的 (Purpose)`
- `### 边界技能（技能边界）` → `### 技能边界 (Skill Boundaries)`
- 代码块占位符：由 `__CODE_BLOCK_N__` 改为 `__CBXXXX__`，避免被 API 翻译

---

## 运行脚本

```bash
# 安装依赖
python3 -m venv .venv-translate
source .venv-translate/bin/activate
pip install deep-translator

# 翻译全部技能
python scripts/translate-skills-zh.py

# 仅翻译指定技能
python scripts/translate-skills-zh.py --skill analyze-requirements

# 字典模式（不调用 API）
python scripts/translate-skills-zh.py --no-api

# 试运行（不写入文件）
python scripts/translate-skills-zh.py --dry-run
```

---

## 参考

- [docs/LANGUAGE_SCHEME.md](../LANGUAGE_SCHEME.md) — 语言归属与 MECE 规则
- [rules/writing-chinese-technical.md](../../rules/writing-chinese-technical.md) — 中文技术写作规范
