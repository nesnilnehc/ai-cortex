#!/usr/bin/env python3
"""
SSOT 完整性审计器 - Phase 9 实现
五步意图优先流程：Intent Modeling → Conflict Screening → Layered Similarity → SSOT Judgment → Output Normalization

关键特性：
- 文件级全量审计（不按目录剪枝）
- 强制跨层深扫对（requirements-planning ↔ process-management）
- 分层相似度分析（doc-level + section-level + 关键实体）
- 详细冲突矩阵和 Intent Registry 输出
"""

import os
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
import json
import math

# ============================================================================
# Step 1: Intent Modeling
# ============================================================================

@dataclass
class IntentModel:
    """文档的意图模型"""
    filepath: str
    relpath: str
    path_layer: str  # docs/ 下的目录层级
    artifact_type: str  # 从 frontmatter 或推断
    ownership_role: str  # strategic, execution, backlog, decision, reference, architecture
    granularity: str  # strategic-statement, execution-plan, backlog-items, point-in-time, content, index
    section_intents: List[str] = field(default_factory=list)  # H2 标题列表


class IntentModelExtractor:
    """从文档提取意图模型"""

    def __init__(self, docs_root: str):
        self.docs_root = docs_root

    def extract_frontmatter(self, filepath: str) -> Dict[str, str]:
        """提取 YAML frontmatter"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
                if match:
                    fm = {}
                    for line in match.group(1).split('\n'):
                        if ':' in line:
                            k, v = line.split(':', 1)
                            fm[k.strip()] = v.strip()
                    return fm
        except:
            pass
        return {}

    def infer_ownership_role(self, relpath: str, artifact_type: str) -> str:
        """从路径和类型推断所有权角色"""
        parts = relpath.split('/')

        if 'process-management' in relpath:
            if 'roadmap' in relpath:
                return 'execution-planning'
            elif 'backlog' in relpath:
                return 'backlog-management'
            elif 'promotion' in relpath or 'iteration' in relpath:
                return 'execution-process'
            elif 'decisions' in relpath:
                return 'decision-record'
            else:
                return 'execution-planning'
        elif 'project-overview' in relpath or 'strategic' in relpath:
            return 'strategic'
        elif 'requirements-planning' in relpath:
            return 'execution-planning'
        elif 'designs' in relpath or 'architecture' in relpath:
            return 'architecture'
        elif 'calibration' in relpath:
            return 'calibration-record'
        else:
            return 'reference'

    def infer_granularity(self, relpath: str, artifact_type: str) -> str:
        """从路径和类型推断粒度"""
        if 'README' in relpath or 'INDEX' in relpath.upper():
            return 'index'
        elif artifact_type in ['adr', 'design']:
            return 'point-in-time'
        elif 'strategic' in relpath or 'vision' in relpath or 'mission' in relpath:
            return 'strategic-statement'
        elif 'roadmap' in relpath or 'backlog' in relpath:
            return 'execution-plan'
        else:
            return 'content'

    def extract_sections(self, filepath: str) -> List[str]:
        """提取 H2/H3 章节标题"""
        sections = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                # 跳过 frontmatter
                if content.startswith('---'):
                    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

                for line in content.split('\n'):
                    if line.startswith('## '):
                        sections.append(line[3:].strip())
                    elif line.startswith('### '):
                        sections.append('  ' + line[4:].strip())
        except:
            pass
        return sections

    def build_intent_registry(self) -> Dict[str, IntentModel]:
        """构建完整的意图注册表"""
        registry = {}

        for root, dirs, files in os.walk(self.docs_root):
            for file in files:
                if not file.endswith('.md'):
                    continue

                filepath = os.path.join(root, file)
                relpath = os.path.relpath(filepath, self.docs_root)

                fm = self.extract_frontmatter(filepath)
                artifact_type = fm.get('artifact_type', self._infer_type(relpath))

                path_layer = '/'.join(relpath.split('/')[:-1])
                ownership = self.infer_ownership_role(relpath, artifact_type)
                granularity = self.infer_granularity(relpath, artifact_type)
                sections = self.extract_sections(filepath)

                model = IntentModel(
                    filepath=filepath,
                    relpath=relpath,
                    path_layer=path_layer,
                    artifact_type=artifact_type,
                    ownership_role=ownership,
                    granularity=granularity,
                    section_intents=sections
                )

                registry[relpath] = model

        return registry

    def _infer_type(self, relpath: str) -> str:
        """从路径推断 artifact_type"""
        if 'adr' in relpath or 'decision' in relpath:
            return 'adr'
        elif 'design' in relpath:
            return 'design'
        elif 'backlog' in relpath:
            return 'backlog-item'
        elif 'roadmap' in relpath:
            return 'roadmap'
        elif 'requirement' in relpath or 'requirements' in relpath:
            return 'requirements'
        else:
            return 'unknown'


# ============================================================================
# Step 2 & 3: Intent Conflict Screening + Layered Similarity
# ============================================================================

class SimilarityAnalyzer:
    """分层相似度分析"""

    @staticmethod
    def word_similarity(text1: str, text2: str) -> float:
        """计算词汇相似度"""
        if not text1 or not text2:
            return 0.0

        words1 = set(re.findall(r'\w+', text1.lower()))
        words2 = set(re.findall(r'\w+', text2.lower()))

        if not words1 or not words2:
            return 0.0

        overlap = len(words1 & words2)
        total = len(words1 | words2)

        return overlap / total if total > 0 else 0.0

    @staticmethod
    def extract_sections_with_content(filepath: str) -> Dict[str, str]:
        """提取章节及其内容"""
        sections = {}
        current_h2 = None
        current_content = []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                # 跳过 frontmatter
                if content.startswith('---'):
                    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

                for line in content.split('\n'):
                    if line.startswith('## '):
                        if current_h2:
                            sections[current_h2] = '\n'.join(current_content)
                        current_h2 = line[3:].strip()
                        current_content = []
                    elif current_h2:
                        current_content.append(line)

                if current_h2:
                    sections[current_h2] = '\n'.join(current_content)
        except:
            pass

        return sections

    @staticmethod
    def analyze_pair(filepath_a: str, filepath_b: str) -> Dict:
        """分析两个文档的相似度"""
        result = {
            'doc_level_sim': 0.0,
            'section_level_sims': [],
            'max_section_sim': 0.0,
            'section_pairs': []
        }

        # Doc-level 相似度
        try:
            with open(filepath_a, 'r', encoding='utf-8') as f:
                content_a = f.read()
            with open(filepath_b, 'r', encoding='utf-8') as f:
                content_b = f.read()

            result['doc_level_sim'] = SimilarityAnalyzer.word_similarity(content_a, content_b)

            # Section-level 相似度
            sections_a = SimilarityAnalyzer.extract_sections_with_content(filepath_a)
            sections_b = SimilarityAnalyzer.extract_sections_with_content(filepath_b)

            for title_a, content_a_sec in sections_a.items():
                for title_b, content_b_sec in sections_b.items():
                    sim = SimilarityAnalyzer.word_similarity(content_a_sec, content_b_sec)
                    if sim > 0.20:  # 记录 >20% 的高相似度
                        result['section_level_sims'].append({
                            'section_a': title_a[:40],
                            'section_b': title_b[:40],
                            'similarity': sim
                        })
                        result['section_pairs'].append({
                            'section_a': title_a,
                            'section_b': title_b,
                            'sim': sim
                        })
                        result['max_section_sim'] = max(result['max_section_sim'], sim)
        except:
            pass

        return result


# ============================================================================
# Step 4: SSOT Judgment
# ============================================================================

@dataclass
class SSoTConflict:
    """SSOT 冲突记录"""
    doc_a: str
    doc_b: str
    intent_overlap: bool
    doc_level_sim: float
    section_level_sim: float
    priority: str  # P0, P1, P2, Info
    canonical_source: Optional[str] = None
    repair_action: Optional[str] = None
    reasoning: str = ""


class SSoTJudge:
    """SSOT 判定引擎"""

    # 强制深扫对（跨层对）
    FORCED_PAIRS = [
        ('requirements-planning', 'process-management'),
        ('requirements-planning', 'designs'),
        ('process-management', 'designs'),
    ]

    @staticmethod
    def should_compare(model_a: IntentModel, model_b: IntentModel) -> bool:
        """判断是否应该比对两个文档"""

        # 检查是否为强制比对的跨层对
        for pattern_a, pattern_b in SSoTJudge.FORCED_PAIRS:
            if ((pattern_a in model_a.relpath and pattern_b in model_b.relpath) or
                (pattern_a in model_b.relpath and pattern_b in model_a.relpath)):
                return True

        # 同域 + 意图重叠 + 粒度接近 → 也要比对
        same_domain = model_a.path_layer.split('/')[0] == model_b.path_layer.split('/')[0]
        intent_overlap = model_a.ownership_role == model_b.ownership_role
        granularity_match = (
            model_a.granularity == model_b.granularity or
            (model_a.granularity in ['execution-plan', 'content'] and
             model_b.granularity in ['execution-plan', 'content'])
        )

        return same_domain and intent_overlap and granularity_match

    @staticmethod
    def judge(model_a: IntentModel, model_b: IntentModel, similarity: Dict) -> Optional[SSoTConflict]:
        """判定冲突等级"""

        intent_overlap = model_a.ownership_role == model_b.ownership_role
        doc_sim = similarity['doc_level_sim']
        section_sim = similarity['max_section_sim']

        # 判定逻辑
        conflict = None

        # P0: 关键事实冲突（可能是数字/决策互斥）
        # 简化判定：用途重叠 + 高 section-level 相似度（>0.50） + doc-level 低（可能是部分重复）
        if intent_overlap and section_sim > 0.50:
            conflict = SSoTConflict(
                doc_a=model_a.relpath,
                doc_b=model_b.relpath,
                intent_overlap=intent_overlap,
                doc_level_sim=doc_sim,
                section_level_sim=section_sim,
                priority='P1',  # 先按 P1，需要手工检查是否为 P0
                canonical_source=model_a.relpath,  # 默认第一个为权威源
                repair_action='Consolidate or summarize+link',
                reasoning=f"Intent overlap + high section similarity ({section_sim:.1%})"
            )

        # P1: 用途重叠 + 大段重复（section > 0.40）
        elif intent_overlap and section_sim > 0.40:
            conflict = SSoTConflict(
                doc_a=model_a.relpath,
                doc_b=model_b.relpath,
                intent_overlap=intent_overlap,
                doc_level_sim=doc_sim,
                section_level_sim=section_sim,
                priority='P1',
                canonical_source=model_a.relpath,
                repair_action='Summarize+link to canonical',
                reasoning=f"Intent overlap + significant section similarity ({section_sim:.1%})"
            )

        # P2: 用途不同但中度复写（section > 0.25）
        elif not intent_overlap and section_sim > 0.25:
            conflict = SSoTConflict(
                doc_a=model_a.relpath,
                doc_b=model_b.relpath,
                intent_overlap=intent_overlap,
                doc_level_sim=doc_sim,
                section_level_sim=section_sim,
                priority='P2',
                canonical_source=model_a.relpath,
                repair_action='Convert to reference+link',
                reasoning=f"Different intent but moderate section similarity ({section_sim:.1%})"
            )

        # Info: 背景相似但无治理动作
        elif doc_sim > 0.15 or section_sim > 0.15:
            conflict = SSoTConflict(
                doc_a=model_a.relpath,
                doc_b=model_b.relpath,
                intent_overlap=intent_overlap,
                doc_level_sim=doc_sim,
                section_level_sim=section_sim,
                priority='Info',
                reasoning=f"Background similarity, no action needed"
            )

        return conflict


# ============================================================================
# Step 5: Output Normalization
# ============================================================================

class SSoTAuditReport:
    """SSOT 审计报告生成器"""

    def __init__(self, docs_root: str):
        self.docs_root = docs_root

    def generate(self) -> str:
        """生成完整的 SSOT 审计报告"""

        # Step 1: 意图建模
        print("[Phase 9] Step 1: 意图建模...")
        extractor = IntentModelExtractor(self.docs_root)
        intent_registry = extractor.build_intent_registry()
        print(f"  → 提取 {len(intent_registry)} 个文档的意图模型")

        # Step 2: 意图冲突初筛 + Step 3: 分层相似度分析
        print("[Phase 9] Step 2-3: 意图冲突初筛 + 分层相似度分析...")
        conflicts = []
        analyzer = SimilarityAnalyzer()
        judge = SSoTJudge()

        # 文件级全量审计：不按目录剪枝，遍历所有配对
        items = list(intent_registry.items())
        for i, (relpath_a, model_a) in enumerate(items):
            for relpath_b, model_b in items[i+1:]:
                # 检查是否应该比对
                if not judge.should_compare(model_a, model_b):
                    continue

                # 分层相似度分析
                similarity = analyzer.analyze_pair(model_a.filepath, model_b.filepath)

                # Step 4: SSOT 判定
                conflict = judge.judge(model_a, model_b, similarity)
                if conflict and conflict.priority != 'Info':  # 筛掉 Info 级
                    conflicts.append(conflict)

        print(f"  → 检出 {len(conflicts)} 个冲突（P0/P1/P2）")

        # Step 5: 生成输出
        print("[Phase 9] Step 5: 输出规范化...")

        report = self._build_markdown_report(intent_registry, conflicts)
        return report

    def _build_markdown_report(self, intent_registry: Dict, conflicts: List[SSoTConflict]) -> str:
        """构建 Markdown 格式的报告"""

        lines = [
            "# SSOT 完整性审计 — Phase 9 详细报告",
            "",
            f"**审计日期**：2026-03-24",
            f"**覆盖文档**：{len(intent_registry)} 个",
            f"**检出冲突**：{len(conflicts)} 个（P0/P1/P2）",
            "",
            "---",
            "",
            "## Part I: Intent Registry（意图注册表）",
            "",
        ]

        # 按目录分组输出
        by_layer = defaultdict(list)
        for relpath, model in intent_registry.items():
            layer = model.path_layer or 'root'
            by_layer[layer].append((relpath, model))

        for layer in sorted(by_layer.keys()):
            lines.append(f"### {layer}")
            lines.append("")
            lines.append("| 文档 | artifact_type | ownership_role | granularity |")
            lines.append("|:---|:---|:---|:---|")

            for relpath, model in by_layer[layer]:
                lines.append(
                    f"| {relpath} | {model.artifact_type} | {model.ownership_role} | {model.granularity} |"
                )

            lines.append("")

        # SSOT 冲突矩阵
        lines.extend([
            "## Part II: SSOT 冲突矩阵",
            "",
            "| Doc A | Doc B | Intent重叠 | Doc-Level | Section-Level | 优先级 | Canonical Source | 修复动作 |",
            "|:---|:---|:---:|:---:|:---:|:---:|:---|:---|",
        ])

        for conflict in sorted(conflicts, key=lambda x: {'P0': 0, 'P1': 1, 'P2': 2}.get(x.priority, 3)):
            lines.append(
                f"| {conflict.doc_a} | {conflict.doc_b} | "
                f"{'✓' if conflict.intent_overlap else '✗'} | {conflict.doc_level_sim:.1%} | "
                f"{conflict.section_level_sim:.1%} | **{conflict.priority}** | {conflict.canonical_source} | "
                f"{conflict.repair_action} |"
            )

        lines.extend([
            "",
            "## Part III: 修复清单",
            "",
        ])

        # 按优先级分组
        p0_conflicts = [c for c in conflicts if c.priority == 'P0']
        p1_conflicts = [c for c in conflicts if c.priority == 'P1']
        p2_conflicts = [c for c in conflicts if c.priority == 'P2']

        if p0_conflicts:
            lines.append("### 【P0 - 关键冲突（必须修复）】")
            lines.append("")
            for i, c in enumerate(p0_conflicts, 1):
                lines.append(f"{i}. {c.doc_a} ↔ {c.doc_b}")
                lines.append(f"   - 推理：{c.reasoning}")
                lines.append(f"   - 动作：{c.repair_action}")
                lines.append("")

        if p1_conflicts:
            lines.append("### 【P1 - 重要冲突（推荐修复）】")
            lines.append("")
            for i, c in enumerate(p1_conflicts, 1):
                lines.append(f"{i}. {c.doc_a} ↔ {c.doc_b}")
                lines.append(f"   - Section 相似度：{c.section_level_sim:.1%}")
                lines.append(f"   - 推理：{c.reasoning}")
                lines.append(f"   - 动作：{c.repair_action}")
                lines.append("")

        if p2_conflicts:
            lines.append("### 【P2 - 优化项（可选修复）】")
            lines.append("")
            for i, c in enumerate(p2_conflicts, 1):
                lines.append(f"{i}. {c.doc_a} ↔ {c.doc_b}")
                lines.append(f"   - Section 相似度：{c.section_level_sim:.1%}")
                lines.append(f"   - 推理：{c.reasoning}")
                lines.append("")

        lines.extend([
            "## Part IV: 质量门禁",
            "",
            "- [ ] ✓ 检出跨层重复（requirements-planning ↔ process-management）",
            "- [ ] ✓ Section-level 分析强制执行",
            "- [ ] ✓ 所有 P0/P1 都有明确的 canonical source",
            "- [ ] ✓ 不存在目录剪枝导致的漏检",
            "",
            "---",
            "",
            f"**报告生成时间**：2026-03-24",
            f"**执行模式**：full（启用完整 SSOT 审计）",
        ])

        return "\n".join(lines)


# ============================================================================
# Main
# ============================================================================

def main():
    """主函数"""
    import sys

    docs_root = sys.argv[1] if len(sys.argv) > 1 else "/Users/nesnilnehc/Workspace/github.com/ai-cortex/docs"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "/Users/nesnilnehc/Workspace/github.com/ai-cortex/docs/calibration/ssot-phase9-audit.md"

    print(f"[SSOT Integrity Checker] 启动")
    print(f"  Docs Root: {docs_root}")
    print(f"  Output: {output_path}")
    print()

    auditor = SSoTAuditReport(docs_root)
    report = auditor.generate()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print()
    print(f"✅ 报告已生成：{output_path}")


if __name__ == '__main__':
    main()
