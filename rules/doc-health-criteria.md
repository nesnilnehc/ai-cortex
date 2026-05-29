---
artifact_type: rule
name: doc-health-criteria
version: 1.0.0
scope: 评估或自检文档健康度时（runtime / linter / CI 执行）
recommended_scope: user
status: active
---

# Rule: 文档健康判据（Document Health Criteria）

> 项目文档"健康"的硬约束集合。运行时（AgentFabric / linter / CI / 人工）按本规则执行检测，本规则不规定如何检测。
>
> 与各 spec（requirement-modeling / functional-design-modeling / technical-design-modeling / task-modeling / universal-notification）配套：spec 定义"对象长什么样"，本规则定义"对象之间的图关系怎样才健康"。

---

## 1. 规范合规

针对每份文档：

- [ ] 文件路径符合 `docs/ARTIFACT_NORMS.md` 中对应 `artifact_type` 的 `path_pattern`
- [ ] 文件名符合命名规范（kebab-case；时间戳前缀仅对允许类型）
- [ ] frontmatter 含必填字段（artifact_type / lifecycle / created_at；按类型可能扩展）
- [ ] frontmatter 字段值在枚举内（artifact_type / lifecycle / status）

---

## 2. 链接图健康

针对全仓 markdown 链接图：

- [ ] **无坏链**：所有相对路径链接指向存在的文件 / 锚点
- [ ] **无孤立文档**：每份文档可从 README 或对应 INDEX.md 链接到达
- [ ] **无循环引用**：A→B→A 视为环
- [ ] **链长 ≤ 4**：从 README 出发到任何文档的最短路径 ≤ 4 跳
- [ ] **外部 URL** 仅做格式校验（不做 HEAD 请求）

---

## 3. SSOT 完整性

针对语义重叠的多份文档：

- [ ] **canonical source 唯一**：同一概念 / 同一字段 / 同一指标在仓库中只有一份权威定义
- [ ] **重复表述同步**：当一份文档引用另一份时，使用链接而非内容复制
- [ ] **无矛盾定义**：两份文档描述同一事物时不得给出冲突值（版本号、时间、字段定义等）
- [ ] **意图分层清晰**：path_layer / artifact_type / ownership / granularity 不重叠

---

## 4. 代码 / 文档对齐

针对代码 diff（PR / branch）：

- [ ] **新增能力**有对应 README / ARCHITECTURE 更新
- [ ] **API 变更**有对应文档同步（接口签名、字段、行为）
- [ ] **废弃 / 移除**在 CHANGELOG 中显式标注
- [ ] **代码示例**与代码现状一致（未引用已删 API）

---

## 5. 层级就绪度

针对治理文档分层（mission / vision / goals / roadmap / requirements / designs / tasks）：

- [ ] **下层不超前于上层**：requirements 必须可追溯到 roadmap 节点；designs 必须可追溯到 requirement；tasks 必须可追溯到 design
- [ ] **frontmatter `parent` 字段**正确指向上游
- [ ] **完成态从下而上推算**：所有子节点 done → 父节点视为 done

---

## 反模式

- ❌ 同一字段定义在 2 份及以上文档中独立维护（违反 SSOT）
- ❌ 文档与代码不一致（如 README 列出已删除的能力）
- ❌ 文档名带时间戳但 artifact_type 不允许（如 requirements / specs）
- ❌ 孤立文档（无任何文档链接到它）
- ❌ 循环引用（A → B → C → A）
- ❌ 跨层 parent 错位（task `parent:` 指向 requirement 而非 design）

---

## 关联资产

- 检测执行（构建链接图、扫 frontmatter、对比 diff、计算 readiness）由 AgentFabric runtime 或 linter / CI 工具承接，本规则只规定判据
- 工具建议：lychee（链接）、markdownlint（格式）、自定义脚本（SSOT / 对齐 / 就绪度）
