---
name: workflow-document-lifecycle
version: 1.0.0
scope: 读取或产出治理制品（ADR、路线图、里程碑任务、归档文档）的所有技能
recommended_scope: both
---

# Rule: 治理文档生命周期 (Governance Document Lifecycle)

## 适用范围 (Scope)

所有读取或产出治理制品的场景，包括但不限于：ADR 解读、路线图分析、里程碑状态判定、归档文件引用、技能产出新制品。

核心场景：`plan-next`、`assess-docs`、`align-architecture`、`audit-docs`、`archive-milestone` 执行期间。

## 强制约束 (Constraints)

1. **ADR 状态字段优先**：读取 ADR 时必须先检查 `status` 字段。`status: superseded` 的 ADR 仅作历史背景参考，不得将其结论作为当前架构约束；若同一决策维度存在多个 `status: accepted` 的 ADR 且结论冲突，必须停止并向用户报告，不得自行裁决。

2. **`_archive/` 路径排除**：路径中包含 `_archive/` 的文件仅作溯源参考；`plan-next`、`assess-docs` 等扫描型技能的默认范围**不包含** `_archive/`，除非调用时显式传入 `include_archive=true`。

3. **路线图历史阶段只读摘要**：`roadmap.md` 中标记为已完成（`status=done`、`✅`、`~~` 删除线或等效标记）的阶段，只读其摘要行；详细执行段落视为历史信息，不纳入当前规划上下文、不作为可执行依据。

4. **状态字段冲突停止上报**：发现 `status` 字段冲突（如某 ADR 标记为 `accepted`，但另一 ADR 的 `supersedes` 字段显式引用了它）时，必须停止处理并向用户报告冲突情况，要求人工裁决；不得假设任一一方优先。

5. **lifecycle 字段强制设置**：任何技能产出新制品时，必须在 frontmatter 中设置 `lifecycle: snapshot` 或 `lifecycle: living`；不得省略该字段。`snapshot` 制品是归档候选，`archive-milestone` 执行时会将活跃里程碑文档的 lifecycle 改写为 `snapshot`。

## 违规示例 (Bad Patterns)

- 读取 `status: superseded` 的 ADR 并将其技术决策用于当前设计约束判断。
- `plan-next` 扫描时将 `milestones/_archive/m3-summary.md` 纳入"未完成里程碑"统计。
- 分析路线图时将已完成阶段的详细任务列表当作当前执行上下文解读。
- 发现两个 `accepted` ADR 在"使用哪个向量数据库"上结论相反，未报告而自行选择较新的一个。
- 技能产出新的需求文档，frontmatter 缺少 `lifecycle` 字段。

## 修正指南 (Remediation)

1. 读取 ADR 时，先在 frontmatter 确认 `status`；若为 `superseded`，仅作背景参考，正文决策不作约束。
2. 调用扫描型技能前，确认默认排除 `_archive/`；仅在明确需要溯源时传入 `include_archive=true`。
3. 解析 `roadmap.md` 时，已完成阶段的段落在定位到"当前状态"后不继续解析其执行细节。
4. 遇到 ADR 状态不一致，输出冲突报告（冲突双方路径 + 各自状态 + 冲突字段），请用户决定如何修正后再继续。
5. 产出制品前，在 frontmatter 模板中加入 `lifecycle:` 字段；若生命周期不确定，默认为 `snapshot`。
