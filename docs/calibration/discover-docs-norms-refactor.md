---
artifact_type: design-decision
created_by: claude
created_at: 2026-03-24
status: approved
---

# 设计文档：discover-docs-norms 自动推导引擎

## 目的
将 discover-docs-norms 从被动（用户选择起点）改进为主动（系统自动推导规范）。

## 核心设计

### Phase 1：项目结构扫描（新增/改进）

**输入**：项目根目录

**输出**：结构化的 docs 快照

```typescript
interface DocsSnapshot {
  root: string;                    // docs/ 路径
  directories: Directory[];        // 所有子目录
  files: DocumentFile[];           // 所有 markdown 文件
  artifacts: {                     // 按推断的 artifact_type 分组
    goals: DocumentFile[];
    requirements: DocumentFile[];
    architecture: DocumentFile[];
    designs: DocumentFile[];
    adrs: DocumentFile[];
    milestones: DocumentFile[];
    roadmaps: DocumentFile[];
    todos: DocumentFile[];
    other: DocumentFile[];
  };
  conventions: {                   // 发现的约定
    namingPatterns: NamingPattern[];
    frontmatterFields: string[];
    pathPatterns: PathPattern[];
    commonPrefixes: string[];      // 如 "2026-03-" 前缀
  };
}

interface DocumentFile {
  name: string;
  path: string;                    // 相对路径：docs/architecture/api-design.md
  fullPath: string;               // 绝对路径
  inferredType: string;            // 推断的 artifact_type
  confidence: number;              // 推断置信度（0-1）
  frontmatter?: Record<string, any>;
  lastModified: Date;
  size: number;
}

interface NamingPattern {
  pattern: string;                 // 如 "YYYY-MM-DD-*.md" 或 "*.md"
  count: number;                   // 符合此模式的文件数
  examples: string[];              // 示例文件名
}

interface PathPattern {
  type: string;                    // artifact_type
  paths: string[];                 // 发现的路径，如 ["docs/architecture", "docs/design-decisions"]
  confidence: number;              // 置信度
  count: number;                   // 该类型的文件数
}
```

### Phase 2：Artifact Type 推断引擎（新增）

**逻辑**：基于路径、文件名、front-matter 推断 artifact_type

```typescript
function inferArtifactType(file: DocumentFile): {type: string, confidence: number} {
  // 规则优先级（从高到低）

  // 1. Front-matter artifact_type 字段（最确定）
  if (file.frontmatter?.artifact_type) {
    return { type: file.frontmatter.artifact_type, confidence: 1.0 };
  }

  // 2. 路径关键词匹配
  const pathRules = {
    'goal': ['docs/goals', 'docs/vision', 'docs/mission'],
    'requirement': ['docs/req', 'docs/requirements', 'docs/requirements-planning'],
    'architecture': ['docs/arch', 'docs/architecture', 'docs/design'],
    'design': ['docs/design-decisions', 'docs/decisions', 'docs/designs'],
    'adr': ['docs/adr', 'docs/adrs', 'docs/architecture-decisions'],
    'milestone': ['docs/milestone', 'docs/milestones', 'docs/process-management/milestones'],
    'roadmap': ['docs/roadmap', 'docs/strategy', 'docs/planning'],
    'todo': ['docs/todo', 'docs/todos', 'docs/work-items'],
  };

  for (const [type, patterns] of Object.entries(pathRules)) {
    if (patterns.some(p => file.path.includes(p))) {
      return { type, confidence: 0.9 };
    }
  }

  // 3. 文件名关键词匹配
  const nameKeywords = {
    'adr': ['ADR', 'adr-'],
    'design': ['design-', 'proposal-'],
    'todo': ['TODO', 'todo-'],
  };

  for (const [type, keywords] of Object.entries(nameKeywords)) {
    if (keywords.some(kw => file.name.includes(kw))) {
      return { type, confidence: 0.7 };
    }
  }

  // 4. Front-matter title 关键词
  const titleKeywords = {
    'goal': ['goal', 'vision', 'mission'],
    'requirement': ['requirement', 'user story'],
    'architecture': ['architecture', 'design', 'system design'],
    'adr': ['decision', 'adr'],
  };

  const title = file.frontmatter?.title || '';
  for (const [type, keywords] of Object.entries(titleKeywords)) {
    if (keywords.some(kw => title.toLowerCase().includes(kw))) {
      return { type, confidence: 0.6 };
    }
  }

  // 5. 默认
  return { type: 'other', confidence: 0.1 };
}
```

### Phase 3：命名约定检测（新增）

**逻辑**：扫描文件名，推断项目使用的命名风格

```typescript
function detectNamingConventions(files: DocumentFile[]): NamingConvention {
  const conventions = {
    case: { camelCase: 0, snake_case: 0, kebab_case: 0, PascalCase: 0 },
    separators: { '_': 0, '-': 0 },
    dateFormat: { 'YYYY-MM-DD': 0, 'YYYY-MM': 0, 'YYYYMMDD': 0, none: 0 },
  };

  files.forEach(file => {
    const name = file.name.replace('.md', '');

    // 检测大小写风格
    if (/^[a-z]+([A-Z][a-z]+)*$/.test(name)) conventions.case.camelCase++;
    if (/^[a-z_]+$/.test(name)) conventions.case.snake_case++;
    if (/^[a-z-]+$/.test(name)) conventions.case.kebab_case++;
    if (/^[A-Z][a-zA-Z]+$/.test(name)) conventions.case.PascalCase++;

    // 检测分隔符
    if (name.includes('_')) conventions.separators['_']++;
    if (name.includes('-')) conventions.separators['-']++;

    // 检测日期格式
    if (/^\d{4}-\d{2}-\d{2}/.test(name)) conventions.dateFormat['YYYY-MM-DD']++;
    else if (/^\d{4}-\d{2}/.test(name)) conventions.dateFormat['YYYY-MM']++;
    else if (/^\d{8}/.test(name)) conventions.dateFormat['YYYYMMDD']++;
    else conventions.dateFormat.none++;
  });

  // 返回最多的约定
  return {
    case: Object.entries(conventions.case).sort((a, b) => b[1] - a[1])[0][0],
    separator: Object.entries(conventions.separators).sort((a, b) => b[1] - a[1])[0][0],
    dateFormat: Object.entries(conventions.dateFormat).sort((a, b) => b[1] - a[1])[0][0],
  };
}
```

### Phase 4：Front-matter 标准化检测（新增）

**逻辑**：扫描现有 front-matter，推断应包含的字段

```typescript
function detectFrontmatterStandard(files: DocumentFile[]): string[] {
  const fieldFrequency = {};

  files.forEach(file => {
    if (file.frontmatter) {
      Object.keys(file.frontmatter).forEach(field => {
        fieldFrequency[field] = (fieldFrequency[field] || 0) + 1;
      });
    }
  });

  // 返回出现在 >= 50% 文件中的字段
  const threshold = files.length * 0.5;
  return Object.entries(fieldFrequency)
    .filter(([_, count]) => count >= threshold)
    .map(([field, _]) => field);
}
```

### Phase 5：规范推导（新增）

**逻辑**：基于 snapshot + 检测结果，生成规范

```typescript
function deriveNorms(snapshot: DocsSnapshot, conventions: NamingConvention): ProjectNorms {
  const norms = {
    paths: {},           // artifact_type → path pattern
    naming: conventions, // 推断出的命名规则
    frontmatter: {},     // artifact_type → 必需字段
    lifecycle: {},       // artifact_type → 生命周期状态
  };

  // 为每个 artifact_type，推导最常见的路径
  for (const [type, files] of Object.entries(snapshot.artifacts)) {
    if (files.length === 0) continue;

    const pathCounts = {};
    files.forEach(f => {
      const dir = f.path.split('/').slice(0, -1).join('/');
      pathCounts[dir] = (pathCounts[dir] || 0) + 1;
    });

    const mostCommonPath = Object.entries(pathCounts)
      .sort((a, b) => b[1] - a[1])[0][0];

    norms.paths[type] = mostCommonPath || `docs/${type}`;
  }

  // Front-matter 标准
  const allFrontmatterFields = detectFrontmatterStandard(
    Object.values(snapshot.artifacts).flat()
  );
  norms.frontmatter.common = allFrontmatterFields;

  return norms;
}
```

### Phase 6：用户确认（改进）

**原本**：用户从多个起点中选择
**改进**：系统展示推导结果，用户只需确认

```
推导出的规范：

✓ 路径:
  - goals         → docs/
  - requirements  → docs/requirements-planning/
  - architecture  → docs/architecture/
  - designs       → docs/design-decisions/
  - adrs          → docs/architecture-decisions/
  - milestones    → docs/process-management/milestones/
  - roadmaps      → docs/
  - todos         → docs/

✓ 命名:
  - 大小写: kebab-case
  - 分隔符: - (dash)
  - 日期格式: YYYY-MM-DD

✓ Front-matter 字段:
  - 必需: artifact_type, created_by, lifecycle, created_at

这个规范对吗？(y/n 或 edit)
```

## 输出物

### 1. ARTIFACT_NORMS.md（增强）
包含推导出的规范，加上置信度指标：
```markdown
# 项目文档规范

## 推导信息
- 扫描日期: 2026-03-24
- 扫描文件数: 45
- 推导置信度: 95%

## 路径约定
| Artifact Type | Path Pattern | 文件数 | 置信度 |
| --- | --- | --- | --- |
| goals | docs/ | 3 | 90% |
| ...
```

### 2. artifact-norms.yaml（新增）
机器可读的规范，包含完整的 linting 规则

### 3. docs-linting.yaml（新增）
明确的 linting 规则：
```yaml
rules:
  naming:
    pattern: "kebab-case"
    datePrefix: "YYYY-MM-DD"
  paths:
    goals: "docs/"
    requirements: "docs/requirements-planning/"
    # ...
  frontmatter:
    required:
      - artifact_type
      - created_by
      - lifecycle
      - created_at
    optional:
      - status
      - updated_at
```

### 4. docs-templates/ 目录（新增）
每个 artifact_type 的模板：
```
docs-templates/
  ├── goal.md
  ├── requirement.md
  ├── architecture.md
  ├── design.md
  ├── adr.md
  ├── milestone.md
  ├── roadmap.md
  └── todo.md
```

## 实现路径

### 新文件：discover-docs-norms/lib/scanner.ts
- docsSnapshot()
- inferArtifactType()
- detectNamingConventions()
- detectFrontmatterStandard()

### 新文件：discover-docs-norms/lib/deriver.ts
- deriveNorms()
- generateLintingConfig()
- generateTemplates()

### 修改：discover-docs-norms/SKILL.md
- 第 79-92 行：替换为新的 Phase 1-2
- 第 93-100 行：改为 Phase 3（仅确认，不选择）

## 验收标准

- [ ] 扫描 ai-cortex 项目 docs/
- [ ] 推导出正确的规范（与现有手工规范一致）
- [ ] 生成 linting.yaml 和 templates/
- [ ] 置信度 > 90%
- [ ] 用户确认流程简化（选择 → 确认）

