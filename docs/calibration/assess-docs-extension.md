---
artifact_type: design
created_by: claude
created_at: 2026-03-24
status: approved
---

# 设计文档：assess-docs 扩展（code-to-docs 对齐 + 依赖图）

## 目的

扩展 assess-docs 的能力，使其能检测：
1. 代码变更与文档同步情况（code-to-docs alignment）
2. 文档之间的依赖关系和孤立文档（dependency graph）

## 模块 1：Code-to-Docs Alignment

### 输入
```
--code-diff [branch | pr | auto]
  branch: 指定 feature branch（如 feature/new-api）
  pr: 从当前 PR 检测（需要 gh CLI）
  auto: 自动检测（若在 feature branch 则用当前，否则报错）
```

### 处理流程

**步骤 1：获取 code diff**
```bash
git diff main...HEAD --name-status
# 输出：M src/api/auth.py, A src/utils/cache.ts, D src/old-module/, ...
```

**步骤 2：分类代码变更**
```typescript
interface CodeChange {
  file: string;
  type: 'M' | 'A' | 'D'; // Modified, Added, Deleted
  area: string; // 推断的代码区域：api, utils, core, tests, etc.
}

// 分类规则：
// src/api/* → area: "api"
// src/utils/* → area: "utils"
// src/core/* → area: "core"
// tests/* → area: "tests"
// docs/* → area: "docs"
```

**步骤 3：推断应更新的文档**
```typescript
const docUpdateMap = {
  'api': ['docs/architecture/api-design.md', 'docs/guides/api-endpoints.md'],
  'utils': ['docs/architecture/system-design.md'],
  'core': ['docs/architecture/'],
  'auth': ['docs/design-decisions/authentication.md'],
  'db': ['docs/architecture/data-model.md'],
};

// 对于每个代码变更，查找相关文档
```

**步骤 4：检查相关文档是否更新**
```
对比：
- 代码中修改的文件 → 应该更新的文档
- 实际在 PR 中修改的文档 → 检查是否涵盖所有相关文档

输出：
✗ src/api/auth.py [Modified]
  → Expected docs: docs/architecture/api-design.md [NOT UPDATED] ⚠️ HIGH
  → Expected docs: docs/design-decisions/auth-flow.md [UPDATED] ✓
```

### 输出

新增到 assess-docs 报告的部分：

```markdown
## Code-to-Docs Alignment (when --code-diff provided)

**Changed files:** 5 (3 modified, 1 added, 1 deleted)
**Code areas affected:** api, utils, auth
**Related docs status:**

| Code Change | Area | Expected Docs | Status | Risk |
| --- | --- | --- | --- | --- |
| src/api/auth.py | api | docs/architecture/api-design.md | NOT UPDATED | HIGH |
| src/utils/cache.ts | utils | docs/architecture/system-design.md | UPDATED | ✓ |

**Recommendation:** Update the following docs before release:
1. docs/architecture/api-design.md (API changes)
2. docs/design-decisions/auth-flow.md (if auth changed)

**Auto-fix suggestions:**
- Update README capability list
- Add new API endpoint to docs/api-endpoints.md
- Update CHANGELOG (voice: user-facing)
```

---

## 模块 2：Documentation Dependency Graph

### 处理流程

**步骤 1：扫描所有 markdown 文件中的链接**

```typescript
interface DocLink {
  from: string;                    // 源文件（如 docs/architecture/api.md）
  to: string;                      // 目标文件（如 docs/design-decisions/auth.md）
  type: 'markdown' | 'wiki' | 'url'; // 链接类型
  valid: boolean;                   // 链接是否有效
}

// 识别三种链接格式：
// 1. Markdown: [title](../path/file.md) 或 [title](./file.md)
// 2. Wiki: [[file]] 或 [[dir/file]]
// 3. URL: https://example.com/...
```

**步骤 2：构建图并检测问题**

```typescript
interface GraphAnalysis {
  nodes: string[];                       // 所有文档
  edges: DocLink[];                      // 所有链接
  issues: {
    isolated: string[];                  // 孤立文档（无入度和出度）
    broken: DocLink[];                   // 损坏链接（目标不存在）
    cycles: string[][];                  // 循环引用（A→B→C→A）
    deepNesting: {file: string, depth: number}[]; // 嵌套过深（引用链太长）
  };
  stats: {
    totalDocs: number;
    totalLinks: number;
    brokenLinks: number;
    orphanDocs: number;
    healthScore: number;                 // 0-100，越高越好
  };
}
```

**步骤 3：识别孤立文档**

孤立文档 = 无任何文件链接到它，且它也不链接到任何其他文件

```
孤立的例子：
- docs/archive/old-decisions/2024-auth.md
- docs/calibration/temp-notes.md
```

### 输出

新增到 assess-docs 报告的部分：

```markdown
## Documentation Graph Health

**Graph Statistics:**
- Total documents: 42
- Total internal links: 127
- Broken links: 2
- Orphan documents: 3
- Health score: 92%

### Broken Links (need fixing)

| From | To | Issue |
| --- | --- | --- |
| docs/architecture/api.md | ../design/auth-flow.md | File not found (expected ../design-decisions/auth-flow.md) |

### Isolated Documents (consider archiving or linking)

- docs/archive/old-decisions/2024-auth.md
- docs/calibration/temp-notes.md
- docs/guides/deprecated-workflow.md

**Recommendation:**
- Fix 2 broken links (review suggests typos in paths)
- Archive or link 3 isolated documents
- Consider creating index for docs/guides/ area

### Cross-Document Consistency

**Version mismatches:**
- README.md mentions "v1.2" but CHANGELOG.md latest is "v1.1" ⚠️

**Outdated references:**
- docs/architecture/api.md references "deprecated endpoint /v1/auth" (removed in v1.1)
```

---

## 集成到 assess-docs

### 输入参数（新增）
```
--code-diff [branch | pr | auto]
  可选。若提供，分析代码变更与文档同步情况

--check-links [true | false]
  默认 true。检查内部链接有效性

--orphan-threshold [days]
  默认 180。文档超过这个天数未修改且无链接，视为孤立
```

### 新的阶段

在当前的 6 个阶段后增加：

**阶段 7：Code-to-Docs Analysis**（若 --code-diff 提供）
- 获取 code diff
- 推断应更新的文档
- 比对实际修改的文档
- 输出 alignment findings

**阶段 8：Documentation Graph Analysis**
- 构建依赖图
- 检测孤立、损坏、循环
- 计算 health score
- 输出 graph findings

### 修改现有阶段

**第 3 阶段（准备情况评分）**：
- 加入 "Graph Health Score" 作为新指标

**输出报告**：
- 在现有的"Compliance Findings"和"Layer Readiness"后，加入：
  - "Code-to-Docs Alignment"（可选）
  - "Documentation Graph Health"（必需）

---

## 实现路径

### 文件修改

1. **SKILL.md**
   - 第 0 阶段：新增参数说明（--code-diff, --check-links）
   - 第 7-8 阶段：详细逻辑
   - 输出部分：新增两个章节

2. **实现脚本**（若需要）
   - `lib/code-diff-analyzer.ts`：分析 code diff
   - `lib/graph-analyzer.ts`：构建和分析文档图

### 关键实现细节

**Code diff 解析**：
```bash
git diff <base>...HEAD --name-status --diff-filter=MAD
# 输出类似：
# M  src/api/auth.py
# A  src/utils/cache.ts
# D  src/old-module/
```

**链接提取**（正则）：
```regex
Markdown: \[.*?\]\((\.{0,2}/.*?\.md|[^)]*\.md)\)
Wiki: \[\[([^\]]+)\]\]
```

**孤立文档检测**（图论）：
```
图节点 = 所有 .md 文件
图边 = 文件之间的链接
孤立节点 = (in-degree == 0 AND out-degree == 0)
```

---

## 验收标准

- [ ] assess-docs 支持 --code-diff 参数
- [ ] code-to-docs alignment 检测准确（无误报）
- [ ] dependency graph 构建正确（无遗漏节点或边）
- [ ] 孤立文档检测有效（可识别 docs/archive/ 等）
- [ ] broken links 检测准确（通过 file exists 检查）
- [ ] 新输出部分格式一致，可被其他工具解析
- [ ] 在 ai-cortex 项目测试：
  - 创建一个 feature branch，修改代码
  - 运行 assess-docs --code-diff=auto
  - 验证能正确识别未更新的文档
  - 验证能检测出孤立文档

