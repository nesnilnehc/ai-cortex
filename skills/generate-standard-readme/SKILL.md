---
name: generate-standard-readme
description: Generate lean, high-density README. Sections pruned by value threshold — not fixed count. Primary goal: reader knows what the project is, where to look, and how to use it within 30 seconds.
description_zh: 生成高信息密度 README。章节按价值门槛裁剪，非固定数量。首要目标：读者 30 秒内知道项目是啥、去哪看、怎么用。
tags: [documentation, devops, writing]
version: 2.1.1
license: MIT
recommended_scope: user
metadata:
  author: ai-cortex
triggers: [generate readme, readme]
input_schema:
  type: code-scope
  description: Repository or project path to generate README for
output_schema:
  type: document-artifact
  description: Lean README.md written to the project root; section count varies by project type and available content
---

# 技能（Skill）：生成精简 README

## 目的

为任何软件项目或文档仓库生成**高信息密度、低冗余**的首页文档。

唯一核心目标：读者在 30 秒内知道——
1. 这个项目是什么（一句话）
2. 去哪里找关键入口
3. 怎么用（可执行的最短路径）

---

## 适用范围

**本技能负责**：
- 按价值门槛裁剪章节的精简 README 生成
- 项目类型分流（代码/应用仓库 vs 文档/规范仓库）
- anti-fluff 输出（每个主张落到具体路径、命令、行为或约束）

**本技能不负责**：
- 完整 docs/ 套件 → 由 AgentFabric runtime 或人工按 `docs/ARTIFACT_NORMS.md` 承接
- AGENTS.md / 代理合同文件 → 使用 `generate-agent-entry`
- 敏感信息脱敏 → 使用 `decontextualize-text`

---

## 使用场景

- **新建仓库**：项目创建后需要首页文档，无现有 README。
- **资产治理**：跨服务统一 README 风格，提升可索引性。
- **遗留系统**：补全缺失文档，以最小信息量覆盖核心入口。
- **移交与发布**：项目转交或公开发布前确保首页文档完整。

**触发信号**：用户说"帮我写 README"、"生成自述文件"或直接提供仓库路径。

---

## 行为

### 交互策略

| 情况 | 行为 |
| :--- | :--- |
| 项目类型已知 | 直接生成，无需询问 |
| 项目类型不明 | 先检查仓库结构（是否有 `package.json` / `pyproject.toml` / `Dockerfile` / `INDEX.md` 等）推断类型；推断有把握则直接生成并说明推断依据；推断不确定时询问用户 |
| 用户未提供描述 | 从仓库名称和文件结构推断最保守描述，标注 `TBD`，不臆造 |
| 写文件前 | 默认直接写入 `README.md`；若仓库已有 README，先提示将覆盖，等待确认 |

### 默认骨架

```
# <项目名> [徽章（可选）]

<一句话说明>（必须）

## <核心入口 / 如何使用>（必须）

## License（必须）
```

其余章节按价值门槛决定是否保留。

### 章节价值门槛

**判定原则**：若某章节不能提供其他章节中不存在的新决策信息，则删除或并入最近的章节。

| 章节 | 类型 | 保留条件 |
| :--- | :--- | :--- |
| 标题 + 一句话说明 | **必须** | 无条件保留 |
| 核心入口 / 如何使用 | **必须** | 无条件保留 |
| License | **必须** | 无条件保留，含有效链接 |
| 功能列表 | 可选 | 存在 ≥2 个非显而易见的功能且一句话说明无法覆盖时 |
| 安装 | 可选（仅 code 类型） | 安装步骤超过 `pip install` / `npm install` 单行时 |
| 快速启动 | 可选（仅 code 类型） | 存在可复制粘贴的最小可运行示例时 |
| 配置/使用说明 | 可选 | 有非显而易见的配置项或参数时 |
| 贡献指南 | 可选 | 贡献流程有特殊要求时（PR 规范、测试门槛等） |
| 作者/致谢 | 可选 | 有明确归属需求时 |

**省略规则**：
- `doc` 类型仓库：默认不生成安装和快速启动节，改为导航索引
- 任何章节若内容为空或仅含 TBD → 省略（不保留空壳章节）
- 贡献/作者章节若只能写通用套话 → 省略

### 项目类型分流

**code 类型**（代码/应用仓库）

判定信号：存在 `package.json` / `pyproject.toml` / `Makefile` / `Dockerfile` / 主程序入口文件。

输出重点：安装路径、最小可运行示例、关键 API 入口。

```markdown
# MyApp

单行说明项目做什么。

## Installation

\```bash
npm install myapp
\```

## Usage

\```bash
myapp --input file.csv --output result.json
\```

## License

MIT — see [LICENSE](LICENSE)
```

**doc 类型**（文档/规范仓库）

判定信号：无可执行入口，主要内容为 `.md` / `.yaml` / `.json` spec 文件，存在 `INDEX.md` / `skills/INDEX.md`。

输出重点：导航索引、阅读路径。安装/快速启动默认省略。

```markdown
# MySpec

单行说明规范/文档的范围和受众。

## 如何使用

- 从 [INDEX.md](INDEX.md) 开始
- 核心定义见 [docs/architecture/terminology.md](docs/architecture/terminology.md)
- 贡献规范见 [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT — see [LICENSE](LICENSE)
```

### Anti-Fluff 规则

以下内容禁止出现：

| 禁止模式 | 示例 | 修复方向 |
| :--- | :--- | :--- |
| 空泛形容词堆叠 | "可复用、可治理、可落地" | 删除或替换为具体行为："通过 `skills/INDEX.md` 注册并与变更一并自检" |
| 无主语的价值主张 | "提高工程规范" | 删除或具体化："维护 `skills/INDEX.md` 与文档链接一致性" |
| 重复已知信息 | 在安装节重述描述节的内容 | 合并或删除 |
| 占位套话 | "欢迎贡献！请提 PR。" | 若无具体流程说明，省略贡献节 |
| 臆造命令或功能 | 无 `docker-compose.yml` 却写 `docker compose up` | 用 `TBD` 或省略 |

**每个主张必须落到**：具体文件路径 / shell 命令 / 可观测行为 / 明确约束。

---

## 输入与输出

### 输入

| 字段 | 必需 | 说明 |
| :--- | :--- | :--- |
| 项目名称 | 必需 | 用于标题 |
| 一句话描述 | 必需 | 精确说明项目做什么 |
| 项目类型 | 推荐 | `code` 或 `doc`；不提供时从仓库结构推断 |
| 许可证 | 推荐 | 类型 + 文件路径；不提供时用 `TBD` |
| 安装命令 | 可选 | 仅 `code` 类型项目使用 |
| 快速启动示例 | 可选 | 仅 `code` 类型项目使用 |
| 核心入口列表 | 可选 | 关键文件、目录、URL |

**未提供的字段**：用 `TBD` 占位或直接省略该章节；禁止臆造。

### 输出

- `README.md` 写入项目根目录
- 章节数由价值门槛决定，最少 3 节（标题+说明、入口/使用、许可证）
- 无损坏链接，内部路径优先

---

## 限制

- **禁止臆造**：所有命令、路径、功能必须来自输入或仓库实际内容；缺失时用 `TBD` 或省略
- **禁止损坏链接**：外部链接仅在高度稳定时使用（如 shields.io）；内部路径须可验证存在
- **禁止空壳章节**：每个保留章节至少含一条可执行信息；内容为空则省略
- **doc 类型硬限制**：doc 类型仓库不生成安装/快速启动节，即使用户要求也应说明理由
- **许可证不可省**：始终包含 License 节；未提供时用 `TBD` 而非省略
- **已有 README 须确认**：若目标目录已有 README.md，覆盖前必须提示用户

---

## 自检

生成 README 后逐项核查：

- [ ] **30 秒测试**：陌生读者能否在 30 秒内读完一句话说明并找到使用入口？
- [ ] **无空泛形容词**：未出现"可复用"、"可治理"、"专业"等无具体行为支撑的形容词
- [ ] **无臆造内容**：所有命令、路径、功能均来自输入或仓库实际内容
- [ ] **无损坏链接**：内部路径已验证存在；外部链接仅在高度稳定时使用
- [ ] **无空壳章节**：每个保留章节至少含一条可执行信息
- [ ] **许可证节存在**：含许可证类型 + 有效链接（或 TBD）
- [ ] **项目类型匹配**：doc 类型无安装/快速启动节；code 类型的安装命令实际可执行
- [ ] **价值门槛通过**：每个保留章节能提供其他章节不含的新决策信息

**验收标准**：以上 8 项全部通过，或对每个未通过项有明确的豁免理由。

---

## 示例

### 示例 1：代码仓库（精简输出）

**输入**：名称 `img-crush`，描述"批量压缩图片"，安装 `pip install img-crush`，用法 `img-crush ./images`，许可证 MIT。

**输出**：

```markdown
# img-crush

批量压缩图片，支持 WebP / PNG / JPEG 格式。

## Installation

\```bash
pip install img-crush
\```

## Usage

\```bash
img-crush ./images          # 原地压缩
img-crush ./images -o out/  # 输出到指定目录
\```

## License

MIT — see [LICENSE](LICENSE)
```

---

### 示例 2：文档/规范仓库（doc 类型）

**输入**：名称 `ai-cortex`，描述"agent-first 技能库"，许可证 MIT，核心入口 `skills/INDEX.md`、`AGENTS.md`。

**输出**：

```markdown
# ai-cortex

面向软件交付和项目治理的 agent-first 技能库。

## 如何使用

- 从 [AGENTS.md](AGENTS.md) 了解代理行为契约
- 浏览 [skills/INDEX.md](skills/INDEX.md) 查找可用技能
- 核心术语定义见 [docs/architecture/terminology.md](docs/architecture/terminology.md)

## License

MIT — see [LICENSE](LICENSE)
```

---

### 示例 3：边缘案例——信息极少的遗留项目

**输入**：名称 `legacy-auth`，无描述，无功能列表，安装和环境未知。

**处理**：
- 一句话说明：从名称推断最保守描述，标注 `TBD`
- 安装节：省略（无可执行命令）
- 功能节：省略（无内容）
- 许可证：`TBD`（不省略，只是内容待补）

**输出**：

```markdown
# legacy-auth

认证服务（详情待补充）。

## 如何使用

TBD — 请参阅项目内部文档。

## License

TBD
```

---

### 示例 4：失败案例——doc 类型仓库生成了安装节

**症状**：为文档规范仓库生成了 `## Installation` 节，内容为 `npm install` 或空 TBD。

**根因**：未识别项目类型，套用了 code 模板。

**修复**：检查仓库结构 → 无可执行入口则判定为 doc 类型 → 删除安装/快速启动节，替换为导航索引。
