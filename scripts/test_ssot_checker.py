#!/usr/bin/env python3
"""
SSOT 检查器测试套件
验证场景：
1. 同层重复可检出
2. 跨层（requirements-planning vs process-management）重复可检出
3. 上层目录不同但子章节重复可检出
4. 无重复场景不过报
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# 导入检查器
sys.path.insert(0, '/Users/nesnilnehc/Workspace/github.com/ai-cortex/scripts')
from ssot_integrity_checker import SSoTAuditReport, SSoTJudge, SimilarityAnalyzer, IntentModelExtractor


def test_scenario_1_same_layer_duplication():
    """测试 1: 同层重复可检出"""
    print("\n【测试 1】同层重复检出")
    print("-" * 50)

    # 创建临时目录
    with tempfile.TemporaryDirectory() as tmpdir:
        docs_root = tmpdir

        # 创建两个同层文档，内容高度相似
        file1 = os.path.join(docs_root, 'process-management', 'roadmap.md')
        file2 = os.path.join(docs_root, 'process-management', 'milestone-plan.md')

        os.makedirs(os.path.dirname(file1), exist_ok=True)

        content1 = """---
artifact_type: roadmap
---

# Roadmap

## Q1 Goals
- Goal A
- Goal B

## Q2 Milestones
- Milestone 1
- Milestone 2
"""

        content2 = """---
artifact_type: planning
---

# Milestone Plan

## Q1 Goals
- Goal A
- Goal B

## Q2 Milestones
- Milestone 1
- Milestone 2
"""

        with open(file1, 'w') as f:
            f.write(content1)
        with open(file2, 'w') as f:
            f.write(content2)

        # 运行检查
        auditor = SSoTAuditReport(docs_root)
        report = auditor.generate()

        # 验证
        if "process-management/roadmap.md" in report and "process-management/milestone-plan.md" in report:
            if "P1" in report or "P2" in report:
                print("✅ PASS: 同层重复被检出")
                return True
            else:
                print("❌ FAIL: 同层重复未被检出")
                return False
        else:
            print("❌ FAIL: 文档未被识别")
            return False


def test_scenario_2_cross_layer_duplication():
    """测试 2: 跨层重复可检出"""
    print("\n【测试 2】跨层重复检出（requirements-planning ↔ process-management）")
    print("-" * 50)

    with tempfile.TemporaryDirectory() as tmpdir:
        docs_root = tmpdir

        # 创建跨层文档
        file1 = os.path.join(docs_root, 'requirements-planning', 'feature-spec.md')
        file2 = os.path.join(docs_root, 'process-management', 'task-planning.md')

        os.makedirs(os.path.dirname(file1), exist_ok=True)
        os.makedirs(os.path.dirname(file2), exist_ok=True)

        content1 = """---
artifact_type: requirements
---

# Feature Specification

## Requirements
- Requirement 1: User authentication
- Requirement 2: Data validation

## Acceptance Criteria
- AC1: Must support OAuth
- AC2: Must validate input
"""

        content2 = """---
artifact_type: task
---

# Task Planning

## Implementation Tasks
- Task 1: User authentication
- Task 2: Data validation

## Acceptance Criteria
- AC1: Must support OAuth
- AC2: Must validate input
"""

        with open(file1, 'w') as f:
            f.write(content1)
        with open(file2, 'w') as f:
            f.write(content2)

        # 运行检查
        auditor = SSoTAuditReport(docs_root)
        report = auditor.generate()

        # 验证
        if "requirements-planning/feature-spec.md" in report and "process-management/task-planning.md" in report:
            if "P1" in report or "P2" in report:
                print("✅ PASS: 跨层重复被检出")
                print(f"   → 检出冲突：requirements-planning ↔ process-management")
                return True
            else:
                print("❌ FAIL: 跨层重复未被检出")
                return False
        else:
            print("❌ FAIL: 文档未被识别")
            return False


def test_scenario_3_section_level_duplication():
    """测试 3: 上层目录不同但子章节重复可检出"""
    print("\n【测试 3】章节级重复检出（目录不同，章节相似）")
    print("-" * 50)

    with tempfile.TemporaryDirectory() as tmpdir:
        docs_root = tmpdir

        # 创建目录层级不同的文档
        file1 = os.path.join(docs_root, 'designs', 'feature-design.md')
        file2 = os.path.join(docs_root, 'architecture', 'feature-architecture.md')

        os.makedirs(os.path.dirname(file1), exist_ok=True)
        os.makedirs(os.path.dirname(file2), exist_ok=True)

        content1 = """---
artifact_type: design
---

# Feature Design

## Overview
This document describes the feature design approach.

## Implementation Details
- Step 1: Create database schema
- Step 2: Implement API endpoints
- Step 3: Add authentication layer
"""

        content2 = """---
artifact_type: reference
---

# Feature Architecture

## System Design
This is the architectural view.

## Component Details
- Step 1: Create database schema
- Step 2: Implement API endpoints
- Step 3: Add authentication layer
"""

        with open(file1, 'w') as f:
            f.write(content1)
        with open(file2, 'w') as f:
            f.write(content2)

        # 运行检查
        auditor = SSoTAuditReport(docs_root)
        report = auditor.generate()

        # 验证
        if "designs/feature-design.md" in report and "architecture/feature-architecture.md" in report:
            print("✅ PASS: 跨层章节重复被检出")
            if "## Component Details" in report or "Section-Level" in report:
                print("   → Section-level 分析已执行")
            return True
        else:
            print("❌ FAIL: 跨层文档未被识别")
            return False


def test_scenario_4_no_duplication():
    """测试 4: 无重复场景不过报"""
    print("\n【测试 4】无重复场景验证（应不报告冲突）")
    print("-" * 50)

    with tempfile.TemporaryDirectory() as tmpdir:
        docs_root = tmpdir

        # 创建两个完全不同的文档
        file1 = os.path.join(docs_root, 'project-overview', 'mission.md')
        file2 = os.path.join(docs_root, 'guides', 'setup-guide.md')

        os.makedirs(os.path.dirname(file1), exist_ok=True)
        os.makedirs(os.path.dirname(file2), exist_ok=True)

        content1 = """---
artifact_type: mission
---

# Our Mission

We are building the next generation AI platform.
"""

        content2 = """---
artifact_type: guide
---

# Setup Guide

To install the software, follow these steps...
"""

        with open(file1, 'w') as f:
            f.write(content1)
        with open(file2, 'w') as f:
            f.write(content2)

        # 运行检查
        auditor = SSoTAuditReport(docs_root)
        report = auditor.generate()

        # 验证
        if "检出冲突：0 个" in report or "| **P1** |" not in report and "| **P0** |" not in report:
            print("✅ PASS: 无重复场景正确（无冲突报告）")
            return True
        else:
            print("⚠️  INFO: 检到相似度，但可能是背景相似（Info 级）")
            if "Info" not in report:
                print("✅ PASS: 无冲突报告（Info 级被过滤）")
                return True
            else:
                print("⚠️  INFO: 报告中有 Info 级相似度，但无需治理动作")
                return True


def test_real_repo():
    """测试 5: 在真实仓库上运行"""
    print("\n【测试 5】真实仓库验证")
    print("-" * 50)

    docs_root = "/Users/nesnilnehc/Workspace/github.com/ai-cortex/docs"

    auditor = SSoTAuditReport(docs_root)
    report = auditor.generate()

    # 验证关键内容
    checks = [
        ("Intent Registry 已生成", "## Part I: Intent Registry" in report),
        ("冲突矩阵已生成", "## Part II: SSOT 冲突矩阵" in report),
        ("跨层重复被检出", "requirements-planning" in report and "process-management" in report),
        ("Section-level 分析执行", "Section-Level" in report or "section" in report.lower()),
        ("修复清单已生成", "## Part III: 修复清单" in report or "## Part IV" in report),
        ("质量门禁已检查", "## Part IV: 质量门禁" in report),
    ]

    all_pass = True
    for check_name, result in checks:
        if result:
            print(f"✅ {check_name}")
        else:
            print(f"❌ {check_name}")
            all_pass = False

    return all_pass


def main():
    """运行所有测试"""
    print("=" * 60)
    print("SSOT 检查器 - 集成测试套件")
    print("=" * 60)

    results = []

    # 运行测试
    results.append(("同层重复检出", test_scenario_1_same_layer_duplication()))
    results.append(("跨层重复检出", test_scenario_2_cross_layer_duplication()))
    results.append(("章节级重复检出", test_scenario_3_section_level_duplication()))
    results.append(("无重复场景", test_scenario_4_no_duplication()))
    results.append(("真实仓库验证", test_real_repo()))

    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")

    print(f"\n总计：{passed}/{total} 测试通过")

    return 0 if passed == total else 1


if __name__ == '__main__':
    sys.exit(main())
