#!/usr/bin/env python3
"""
Translate AI Cortex skills to Simplified Chinese.

For each skill:
- SKILL.md: Keep YAML frontmatter as-is; add description_zh; translate body prose.
- README.md: Translate entire file.

Preserves: code blocks, YAML, tables, structure.
Follows: writing-chinese-technical (中英间距, 术语首次出现保留英文).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# Optional: use deep-translator for prose; fall back to dict-only if unavailable
try:
    from deep_translator import GoogleTranslator
    HAS_TRANSLATOR = True
except ImportError:
    HAS_TRANSLATOR = False

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = REPO_ROOT / "skills"
MANIFEST_PATH = REPO_ROOT / "manifest.json"

# --- description_zh: one-line Chinese summary per skill ---
DESCRIPTION_ZH = {
    "decontextualize-text": "将含私有上下文或内部依赖的文本转为通用、无偏向的表述，保留逻辑、移除组织标识，便于交接、开源或跨团队共享。",
    "generate-standard-readme": "生成固定结构的转换导向 README：10 秒理解、1 分钟运行、清晰的用途与场景；支持治理与采纳模式。",
    "discover-docs-norms": "通过对话与扫描，帮助建立项目级文档制品规范（路径、命名、生命周期）；产出 docs/ARTIFACT_NORMS.md。",
    "discover-skills": "识别能力缺口并从 AI Cortex 或公共技能目录推荐安装；提供前 1–3 条匹配及安装命令。",
    "refine-skill-design": "审计并重构既有 SKILL，使其符合规范与 LLM 最佳实践；适用于改进草稿、修复质量或对齐规范。",
    "generate-agent-entry": "按嵌入式输出契约编写或修订 AGENTS.md，确立项目身份、权威来源与行为预期；采用 AI Cortex 入口格式。",
    "review-code": "编排完整代码审查流水线：依次执行 scope、语言、框架、库与认知类审查技能，并聚合为统一报告。",
    "review-codebase": "对指定文件/目录/仓库进行架构与设计审查；涵盖技术债、模式与质量；diff 审查使用 review-diff。",
    "review-diff": "仅针对 git diff 审查影响、回归、正确性、兼容性与副作用；scope 原子技能，输出 findings 列表。",
    "review-dotnet": "按 .NET (C#/F#) 语言与运行时规范审查代码：async/await、nullable、API 版本、IDisposable、LINQ、可测性。",
    "review-java": "按 Java 语言与运行时规范审查代码：并发、异常、try-with-resources、API 版本、集合与 Stream、NIO、可测性。",
    "review-go": "按 Go 语言与运行时规范审查代码：并发、context、错误处理、资源管理、API 稳定性、类型语义、可测性。",
    "review-php": "按 PHP 语言与运行时规范审查代码：strict types、错误处理、资源管理、PSR、命名空间、null 安全、生成器、可测性。",
    "review-powershell": "按 PowerShell 规范审查代码：高级函数、参数设计、错误处理、对象管道、兼容性与可测性。",
    "review-python": "按 Python 规范审查代码：类型提示、异常、async/await、上下文管理器、依赖与可测性。",
    "review-sql": "审查 SQL 与查询代码：注入风险、参数化、索引与性能、事务、NULL 与约束、方言可移植性。",
    "review-vue": "审查 Vue 3 代码：Composition API、响应式、组件、状态 (Pinia)、路由与性能；框架级原子技能。",
    "review-security": "审查代码安全性：注入、敏感数据、认证、依赖、配置与加密；原子技能，输出 findings 列表。",
    "review-architecture": "审查代码架构：模块与层次边界、依赖方向、单一职责、循环依赖、接口稳定性与耦合。",
    "review-testing": "审查测试：存在性、覆盖度、质量与结构、边界与错误路径覆盖、可维护性；认知原子技能。",
    "generate-github-workflow": "生成嵌有输出契约的 GitHub Actions YAML：安全优先、最小权限、版本锁定；适用于 CI、发布与 PR 检查。",
    "curate-skills": "通过 ASQM 评分、生命周期管理与重叠检测治理技能清单；产出全库技能的质量评分与规范化文档。",
    "install-rules": "从源仓库将规则安装到 Cursor 或 Trae IDE；需显式确认与冲突检测；写盘前需用户批准。",
    "review-performance": "审查性能：复杂度、数据库/查询效率、I/O 与网络成本、内存与分配、并发竞争、缓存与延迟/吞吐回归。",
    "bootstrap-docs": "使用 project-documentation-template 初始化或适配项目文档；产出结构化生命周期文档；支持 Initialize / Adjust。",
    "capture-work-items": "将自由形式输入快速捕获为结构化、可持久的需求、缺陷或问题制品；无需深度验证。",
    "commit-work": "创建高质量 git 提交：清晰消息与合理范围；遵循 Conventional Commits，含 pre-commit 质量检查。",
    "design-solution": "从需求产出验证过的设计文档（架构、组件、数据流、权衡）；不含实现；用于下游任务拆解。",
    "breakdown-tasks": "将设计文档拆解为可执行任务列表：依赖、验收标准、负责人或 AI 执行提示。",
    "review-typescript": "审查 TypeScript/JavaScript 代码：类型安全、异步模式、错误处理与模块设计；原子技能。",
    "review-react": "审查 React 代码：组件设计、hooks 正确性、状态管理、渲染性能与可访问性；框架级原子技能。",
    "review-orm-usage": "审查 ORM 使用：N+1 查询、连接管理、迁移安全、事务与查询效率；库级原子技能。",
    "analyze-requirements": "通过诊断状态推进与结构化对话，将模糊意图或不完整需求转为可验证、可测试的需求。",
    "review-requirements": "审查既有需求文档质量：问题清晰度、可测试需求、约束清单、范围边界、需求 ID 与遗留问题。",
    "align-planning": "执行任务后追溯、漂移检测与自上而下校准，使规划（目标、需求、里程碑、路线图）与执行对齐。",
    "align-architecture": "对照代码实现验证架构与设计文档；当实现偏离 ADR 或设计时，产出架构合规报告。",
    "align-backlog": "将产品/工作待办与当前战略、目标、路线图对齐；分析待办项，识别脱节或孤儿工作，提出变更建议。",
    "assess-docs": "一次性评估文档健康：验证制品规范合规（路径、命名、front-matter）与各层证据就绪；产出缺口与最小补齐计划。",
    "automate-tests": "安全发现并执行仓库测试命令；基于证据选择命令并设安全护栏。",
    "automate-repair": "迭代审查变更、运行自动化测试并实施定向修复，直至问题解决或满足停止条件。",
    "plan-next": "分析项目状态并产出下一行动计划；运行对齐、文档就绪与产出驱动跟进；单周期报告。",
    "define-mission": "定义项目或组织的根本目的；回答项目为何存在；产出 mission 陈述并持久化到 docs。",
    "define-vision": "定义项目旨在创造的长远未来；回答我们在构建什么未来；产出 vision 陈述并持久化到 docs。",
    "define-north-star": "定义代表向用户交付核心价值的单一最重要指标；产出 North Star Metric 及理由、辅助指标与反例。",
    "design-strategic-goals": "定义 3–5 个推动项目走向 vision 与 North Star 的长期战略目标；产出 goals 文档。",
    "define-roadmap": "从战略目标推导由里程碑节点组成的路线图；每节点为阶段检查点，含成功标准与目标可追溯性。",
    "define-strategic-pillars": "从 vision 与 North Star 推导 3–5 个战略支柱（高层次主题），指导战略目标与路线图。",
}

# --- Term dictionary: EN -> ZH (apply for consistency; 术语首次出现可加英文) ---
TERM_DICT = {
    # Headings and structure
    "# Skill:": "# 技能 (Skill)：",
    "## Purpose": "## 目的 (Purpose)",
    "## Core Objective": "## 核心目标 (Core Objective)",
    "## Scope Boundaries": "## 范围边界 (Scope Boundaries)",
    "## Use Cases": "## 使用场景 (Use Cases)",
    "## Behavior": "## 行为 (Behavior)",
    "## Restrictions": "## 限制 (Restrictions)",
    "## Self-Check": "## 自检 (Self-Check)",
    "## Input": "## 输入 (Input)",
    "## Output": "## 输出 (Output)",
    "## Input & Output": "## 输入与输出 (Input & Output)",
    "## Examples": "## 示例 (Examples)",
    "## Appendix": "## 附录",
    "## References": "## 参考 (References)",
    "### Principles": "### 原则 (Principles)",
    "### Steps": "### 步骤 (Steps)",
    "### Interaction": "### 交互 (Interaction)",
    "### Hard Boundaries": "### 硬边界 (Hard Boundaries)",
    "### Skill Boundaries": "### 技能边界 (Skill Boundaries)",
    "### Handoff point": "### 转交点 (Handoff Point)",
    "**Primary Goal**": "**首要目标**",
    "**Success Criteria**": "**成功标准**",
    "**Acceptance Test**": "**验收测试**",
    "**This skill handles**": "**本技能负责**",
    "**This skill does NOT handle**": "**本技能不负责**",
    "**When to use**": "**何时使用**",
    "**Handoff point**": "**转交点**",
    # Common terms (avoid generic "skill" - too broad, use heading-specific only)
    "README": "README",
    "AGENTS.md": "AGENTS.md",
    "findings": "findings",
    "findings list": "findings 列表",
    "code review": "代码审查",
    "requirements": "需求",
    "design": "设计",
    "document": "文档",
    "artifact": "制品",
    "metadata": "元数据",
    "frontmatter": "front-matter",
    "handoff": "转交",
    "scope": "scope",
    "diff": "diff",
    "workflow": "工作流",
    "backlog": "待办",
    "roadmap": "路线图",
    "milestone": "里程碑",
    "vision": "vision",
    "mission": "mission",
    "North Star": "North Star",
    # README sections
    "**Status**": "**状态**",
    "## What it does": "## 用途",
    "## 它的作用": "## 用途",
    "## When to use": "## 何时使用",
    "## Inputs": "## 输入",
    "## Outputs": "## 输出",
    "## Scores (ASQM)": "## 评分 (ASQM)",
    "## Ecosystem": "## 生态",
    "## Full definition": "## 完整定义",
    "See [SKILL.md]": "见 [SKILL.md]",
    "validated": "已验证",
    "Score": "分数",
    "Dimension": "维度",
    "尺寸": "维度",
    "overlaps_with": "overlaps_with",
    "重叠_with": "overlaps_with",
    "market_position": "market_position",
    "market_position ": "market_position ",
    "agent_native": "agent_native",
    "代理本地": "agent_native",
    "asqm_quality": "asqm_quality",
    "cognitive": "cognitive",
    "认知": "cognitive",
    "composability": "composability",
    "可组合性": "composability",
    "stance": "stance",
    "立场": "stance",
    # Fix API over-translation of skill handles
    "**此技能处理**": "**本技能负责**",
    "**此技能不处理**": "**本技能不负责**",
    # Fix API mistranslations
    "**癌症目标**": "**首要目标**",
    "**财务目标**": "**首要目标**",
    "目的（目的）": "目的 (Purpose)",
    "## 目的（目的）": "## 目的 (Purpose)",
    "范围边界（范围边界）": "范围边界 (Scope Boundaries)",
    "## 范围边界（范围边界）": "## 范围边界 (Scope Boundaries)",
    "技能（Skill）": "技能 (Skill)",
    "# 技能（Skill）": "# 技能 (Skill)",
    # Heading: ensure (Skill) when we have 技能：
    "# 技能：": "# 技能 (Skill)：",
}

# Skills that are already fully translated (skip translation entirely)
ALREADY_TRANSLATED: set[str] = set()


def load_manifest() -> list[str]:
    """Load skill names from manifest.json."""
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return [c["name"] for c in data["capabilities"]]


def extract_frontmatter(content: str) -> tuple[str, str]:
    """Split content into YAML frontmatter and body."""
    if not content.strip().startswith("---"):
        return "", content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return "", content
    return parts[1].strip(), parts[2].lstrip("\n")


def add_description_zh_to_frontmatter(fm: str, skill_name: str) -> str:
    """Add or keep description_zh in frontmatter."""
    zh = DESCRIPTION_ZH.get(skill_name, "")
    if not zh:
        return fm
    if "description_zh:" in fm:
        # Replace existing
        fm = re.sub(r"description_zh:\s*[^\n]+", f"description_zh: {zh}", fm, count=1)
    else:
        # Insert after description
        match = re.search(r"(description:\s+[^\n]+)", fm)
        if match:
            pos = match.end()
            fm = fm[:pos] + f"\ndescription_zh: {zh}" + fm[pos:]
        else:
            fm = fm + f"\ndescription_zh: {zh}"
    return fm


def extract_code_blocks(text: str) -> tuple[str, list[str]]:
    """Replace code blocks with placeholders; return (text_with_placeholders, list of blocks)."""
    blocks = []
    pattern = re.compile(r"```[\s\S]*?```", re.MULTILINE)

    def repl(m):
        blocks.append(m.group(0))
        # Use hex placeholder to avoid API translating it
        return f"\n__CB{len(blocks)-1:04X}__\n"

    return pattern.sub(repl, text), blocks


def restore_code_blocks(text: str, blocks: list[str]) -> str:
    """Restore code blocks from placeholders."""
    for i, block in enumerate(blocks):
        text = text.replace(f"__CB{i:04X}__", block)
    return text


def chunk_text(text: str, max_len: int = 1500) -> list[str]:
    """Split text into chunks at paragraph boundaries."""
    chunks = []
    current = []
    current_len = 0
    for para in text.split("\n\n"):
        para_len = len(para) + 2
        if current_len + para_len > max_len and current:
            chunks.append("\n\n".join(current))
            current = [para]
            current_len = para_len
        else:
            current.append(para)
            current_len += para_len
    if current:
        chunks.append("\n\n".join(current))
    return chunks


def translate_with_api(text: str) -> str:
    """Translate text to Simplified Chinese using deep-translator."""
    if not text.strip():
        return text
    try:
        chunks = chunk_text(text)
        results = []
        for chunk in chunks:
            if chunk.strip():
                t = GoogleTranslator(source="en", target="zh-CN").translate(chunk.strip())
                results.append(t if t else chunk)
            else:
                results.append(chunk)
            import time
            time.sleep(1.5)  # Rate limit for free Google Translate
        return "\n\n".join(results)
    except Exception as e:
        print(f"    [WARN] Translation API error: {e}", file=sys.stderr)
        return text


def apply_term_dict(text: str) -> str:
    """Apply term dictionary for consistency. Longest matches first. Avoid recursive replacement."""
    out = text
    for en, zh in sorted(TERM_DICT.items(), key=lambda x: -len(x[0])):
        if en in zh:
            continue  # Skip if replacement contains original (avoid recursion)
        out = re.sub(re.escape(en), zh, out)
    return out


def translate_prose(text: str, use_api: bool = True, skip_if_chinese: bool = True) -> str:
    """
    Translate prose to Chinese.
    - Preserves code blocks
    - Pre-applies term dict so standard terms are not mistranslated
    - use_api: use deep-translator if available
    - skip_if_chinese: if text is already mostly Chinese, skip translation
    """
    if skip_if_chinese:
        chinese_chars = sum(1 for c in text if "\u4e00" <= c <= "\u9fff")
        if chinese_chars / max(len(text), 1) > 0.2:
            return apply_term_dict(text)

    text_no_code, blocks = extract_code_blocks(text)
    # Pre-apply dict so headings/key terms are not mistranslated by API
    text_pre = apply_term_dict(text_no_code)
    if use_api and HAS_TRANSLATOR:
        translated = translate_with_api(text_pre)
    else:
        translated = text_pre
    # Post-apply to fix any API mistranslations
    translated = apply_term_dict(translated)
    return restore_code_blocks(translated, blocks)


def process_skill_md(skill_name: str, use_api: bool, dry_run: bool = False) -> list[str]:
    """Process SKILL.md: add description_zh, translate body. Returns list of warnings."""
    path = SKILLS_ROOT / skill_name / "SKILL.md"
    if not path.exists():
        return [f"SKILL.md not found: {path}"]

    if skill_name in ALREADY_TRANSLATED:
        return []  # Skip entirely; already done

    content = path.read_text(encoding="utf-8")
    fm, body = extract_frontmatter(content)

    fm = add_description_zh_to_frontmatter(fm, skill_name)
    body_tr = translate_prose(body, use_api=use_api, skip_if_chinese=False)

    new_content = f"---\n{fm}\n---\n\n{body_tr}"
    if not dry_run:
        path.write_text(new_content, encoding="utf-8")
    return []


def process_readme(skill_name: str, use_api: bool, dry_run: bool = False) -> list[str]:
    """Process README.md: translate entire file. Returns list of warnings."""
    path = SKILLS_ROOT / skill_name / "README.md"
    if not path.exists():
        return []

    if skill_name in ALREADY_TRANSLATED:
        return []  # Skip; already done

    content = path.read_text(encoding="utf-8")
    translated = translate_prose(content, use_api=use_api, skip_if_chinese=False)
    if not dry_run:
        path.write_text(translated, encoding="utf-8")
    return []


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Translate skills to Simplified Chinese")
    parser.add_argument("--no-api", action="store_true", help="Skip API translation; use dict only")
    parser.add_argument("--skill", type=str, help="Process only this skill")
    parser.add_argument("--dry-run", action="store_true", help="Do not write files")
    args = parser.parse_args()
    use_api = not args.no_api and HAS_TRANSLATOR

    if not HAS_TRANSLATOR and not args.no_api:
        print("Warning: deep-translator not installed. Run: pip install deep-translator", file=sys.stderr)
        print("Falling back to dictionary-only translation.", file=sys.stderr)

    skills = load_manifest()
    if args.skill:
        if args.skill not in skills:
            print(f"Unknown skill: {args.skill}")
            sys.exit(1)
        skills = [args.skill]

    manual_review = []
    for name in skills:
        print(f"Processing {name}...")
        w1 = process_skill_md(name, use_api, dry_run=args.dry_run)
        w2 = process_readme(name, use_api, dry_run=args.dry_run)
        if w1 or w2:
            manual_review.append((name, w1 + w2))

    if manual_review:
        print("\n--- Skills needing manual review ---")
        for name, warns in manual_review:
            print(f"  {name}: {warns}")

    print(f"\nDone. Processed {len(skills)} skills.")


if __name__ == "__main__":
    main()
