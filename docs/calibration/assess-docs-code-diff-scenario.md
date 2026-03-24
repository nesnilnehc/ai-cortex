---
artifact_type: design
created_by: claude
created_at: 2026-03-24
status: approved
---

# 设计文档：assess-docs Code Diff Scenario

## 背景

当前有独立的 `sync-release-docs` 技能用于在代码发版后更新文档。但这个功能应该是 `assess-docs` 的一个 scenario，而不是独立技能。

**改进**：`assess-docs --code-diff=<branch>` 整合 sync-release-docs 的功能。

## Code Diff Scenario

### 输入

```bash
assess-docs --code-diff=main
  # 比对：当前 branch vs main 的差异

assess-docs --code-diff=auto
  # 自动检测：
  # - 若在 feature branch，对比 main
  # - 若在 main，对比上一个 release tag
  # - 否则报错

assess-docs --code-diff=pr
  # 若在 PR context（有 GITHUB_REF/GITHUB_SHA），自动提取基准 branch
```

### 处理流程

**第 7 阶段（code-to-docs alignment）的详细步骤**：

1. **获取代码 diff**
   ```bash
   git diff <base>..HEAD --name-status --diff-filter=MAD
   git diff <base>..HEAD --unified=0  # 获取具体改动行数
   ```

2. **提取代码变更信息**
   ```
   文件: src/api/auth.py
   变更类型: M (Modified)
   代码区域: api
   改动行数: +45, -20
   关键变更:
     - func authenticate() signature changed
     -新增 refresh_token() 方法
     - 移除 deprecated_login() 方法
   ```

3. **推断应更新的文档**
   ```
   代码变更类型 → 应更新的文档

   src/api/* 修改 →
     docs/architecture/api-design.md
     docs/guides/api-endpoints.md
     docs/design-decisions/*

   src/auth/* 修改 →
     docs/design-decisions/authentication.md
     docs/architecture/security.md

   src/db/* 修改 →
     docs/architecture/data-model.md

   README 中提到的 API/功能修改 →
     docs/README.md
     docs/CHANGELOG.md （如果版本更新）
   ```

4. **检查相关文档是否更新**
   ```
   对比：
   - 推断应更新的文档集合：{D1, D2, D3, ...}
   - 实际修改的文档集合：{D2, D4, ...}

   差集（应更新但未更新）：{D1, D3, ...} → HIGH RISK
   ```

5. **生成建议**
   ```
   AUTO-FIX SUGGESTIONS:

   High Priority (code changed, docs not):
   - [ ] Update docs/architecture/api-design.md
         - Document new refresh_token() method
         - Update endpoint list

   - [ ] Update docs/CHANGELOG.md
         - Add entry: "Changed: Simplified auth flow"
         - Add entry: "Removed: deprecated_login() method"

   Medium Priority (preventive):
   - [ ] Review docs/design-decisions/authentication.md
         - Verify if design still aligns with new implementation

   Optional:
   - [ ] Update docs/README.md capability list
   ```

### 输出示例

当运行 `assess-docs --code-diff=main` 时，报告包含：

```markdown
## Code-to-Docs Alignment (Code Diff Provided)

**Comparison**: main...HEAD

**Code Summary**:
- Files changed: 12 (9 modified, 2 added, 1 deleted)
- Net impact: +180 lines, -95 lines
- Areas: api (6), auth (3), utils (2), db (1)

### Changed Code by Area

| Area | Files | Key Changes | Docs Status |
| --- | --- | --- | --- |
| api | src/api/auth.py | + refresh_token()<br/>- deprecated_login() | ⚠️ NEEDS UPDATE |
| auth | src/auth/*.py | Security policy tightened | ✓ Updated |
| utils | src/utils/cache.ts | New LRU cache impl | ⚠️ NOT MENTIONED |
| db | src/db/migration.sql | Schema: +user_sessions | ⚠️ NOT UPDATED |

### Documentation Alignment Report

**Missing Updates** (Code changed, docs not):
1. ❌ docs/architecture/api-design.md
   - Reason: API endpoints changed
   - Action: Add refresh_token, remove deprecated_login
   - Estimated effort: 15 min

2. ❌ docs/architecture/data-model.md
   - Reason: New user_sessions table added
   - Action: Update ER diagram, add table description
   - Estimated effort: 20 min

3. ❌ docs/CHANGELOG.md
   - Reason: Version updated (v1.0 → v1.1)
   - Action: Document all breaking changes
   - Estimated effort: 10 min

**Extra Updates** (Docs changed, but code doesn't require):
- ✓ docs/design-decisions/auth-flow.md
  - Status: Proactively updated to reflect design refinements
  - Note: Good practice, but not critical

**Consistency Checks**:
- ✓ README capability list matches implementation
- ✓ CONTRIBUTING.md workflow still valid
- ✓ API examples in docs/guides/ use current endpoints

### Actionable Recommendations

**Before Releasing v1.1:**
1. Update 3 high-priority docs (est. 45 min)
2. Review 2 design docs for alignment (est. 30 min)
3. Test all code examples in docs (est. 20 min)

**Priority Order**:
1. CHANGELOG.md (release blockers)
2. API documentation (customer-facing)
3. Architecture docs (internal reference)

**Auto-Execute Suggestions**:
```bash
# Add to CHANGELOG
docs/CHANGELOG.md: Add release entry for v1.1

# Generate API endpoint list from code
docs/guides/api-endpoints.md: Auto-generate from src/api/

# Refresh ER diagram
docs/architecture/data-model.md: Request Miro/diagram update
```

**Release Readiness**:
- Code ready: ✓
- Docs ready: ❌ (3 critical, 0 optional)
- Ready for release: NO (fix docs first)
```

### 与现有 assess-docs 报告的集成

在 6 个阶段的输出后，新增：

```markdown
---

## Phase 7: Code-to-Docs Alignment

[上述内容]

---

## Phase 8: Documentation Graph Health

[前面设计的依赖图分析]
```

---

## 实现细节

### 何时适用

- **PR 合并前检查**：确保代码变更对应文档更新
- **发版前检查**：确保文档与即将发布的代码一致
- **文档审查**：code reviewer 可快速验证文档是否完整

### 特殊情况

1. **纯代码变更**（如重构、性能优化）
   - 若无 API 或功能改变，docs alignment 可为 PASS

2. **纯文档变更**（如 typo 修复）
   - code-diff 为空，跳过此阶段

3. **文档-先策略**（设计文档已存在）
   - 代码与文档一致，alignment 为 PASS

4. **breaking change**
   - 标记为 CRITICAL，需人工确认

### 和 sync-release-docs 的区别

| 功能 | sync-release-docs | assess-docs --code-diff |
| --- | --- | --- |
| 检测代码变更 | ❌ | ✅ |
| 比对文档完整性 | ✓（部分） | ✅ |
| 检测合规问题 | ❌ | ✅ |
| 检测孤立文档 | ❌ | ✅（新增） |
| 输出建议 | ✓ | ✅（更详细） |
| **结论** | **功能受限** | **功能完整** |

---

## 验收标准

- [ ] assess-docs 支持 --code-diff 参数
- [ ] code diff 准确解析（无遗漏文件）
- [ ] 推断应更新的文档准确（>90%）
- [ ] alignment 检查不产生误报
- [ ] 建议可操作且优先级清晰
- [ ] 在 ai-cortex PR 测试：
  - 创建 feature branch 修改代码
  - 运行 `assess-docs --code-diff=main`
  - 验证能正确识别文档缺口
  - 验证建议有用（开发者能照着做）

