---
name: generate-github-workflow
description: "GitHub Actions YAML with embedded output contract: security-first, minimal permissions, version pinning. For CI, release, PR checks. Differs from generic templates by spec compliance and auditability."
description_zh: 生成嵌有输出契约的 GitHub Actions YAML：安全优先、最小权限、版本锁定；适用于 CI、发布与 PR 检查。
tags: [devops]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [github workflow, generate workflow]
input_schema:
  type: free-form
  description: Workflow requirements (CI, release, PR checks) and project context
output_schema:
  type: document-artifact
  description: GitHub Actions YAML workflow file(s) written to .github/workflows/
---

# 技能（Skill）：生成GitHub工作流程

## 目的 (Purpose)

为各种软件项目生成满足此技能的 **附录 A：工作流输出合同** 的 **GitHub Actions 工作流文件**。标准化结构、触发器和安全性可降低 CI/CD 设置成本并提高可维护性和可审核性，同时避免常见的安全和权限问题。该技能仅产生工作流YAML；它与文档或规则技能无关。如果用户稍后需要 README 或 AGENTS.md 更新，请单独调用这些技能。

---

## 核心目标（Core Objective）

**首要目标**：针对用户的场景、堆栈和安全态势生成完整、符合规范且可立即运行的 GitHub Actions 工作流 YAML 文件 — 只需要替换占位符即可部署。

**成功标准**（必须满足所有要求）：

1. ✅ **符合附录 A**：输出满足附录 A 中的所有强制结构和安全需求（名称、工作、运行、步骤、固定操作、无硬编码秘密）
2. ✅ **窄触发器**：`on` 块的范围仅限于特定分支/路径/标签 - 没有没有过滤器的裸露 `on: Push`
3. ✅ **最小权限**：在工作流程或作业级别将“权限”设置为场景类型所需的最低权限（CI：“内容：读取”；发布：“内容：写入”、“包：写入”）
4. ✅ **堆栈对齐**：Runner、语言版本、包管理器和命令与用户指定的堆栈匹配
5. ✅ **写入前用户确认**：列出必需的注释和占位符，并在写入 `.github/Workflows/` 之前获得用户确认

**验收**测试：用户替换占位符后，除了秘密名称和环境特定值之外，工作流是否可以在目标存储库中运行而无需进一步修改？

---

## 范围边界（范围边界）

**本技能负责**：

- 为 CI、PR 检查、发布和计划场景生成完整的 GitHub Actions 工作流 YAML
- 安全强化（固定操作、最小权限、无硬编码秘密）
- 堆栈对齐（Node/Python/Go/Rust 运行程序、包管理器、构建命令）
- 多工作流生成（CI + Release 分成单独的文件）
- 与现有工作流程的冲突检测
- Go + Docker + GHCR + GoReleaser 模式（参见附录 B）

**本技能不负责**：

- 链接到文档技能（README、AGENTS.md 更新）——在工作流生成后单独调用这些技能
- 无需用户确认即可写入 `.github/工作流s/`
- 在没有警告的情况下覆盖现有的工作流程
- 实现已在“.goreleaser.yaml”或 Dockerfile 中定义的构建/发布逻辑
- 生成非 GitHub CI/CD（GitLab CI、Jenkins 等）

**转交点**：生成并确认工作流YAML后，经用户批准将文件写入`.github/工作流/`。对于新工作流触发的文档更新，请单独使用文档技能。

---

## 使用场景（用例）

- **新项目设置**：将 CI（构建、测试、lint）或 PR 检查工作流添加到新存储库。
- **统一标准**：在多个存储库中协调工作流程风格和命名，以进行操作和审计。
- **填补空白**：使用最少的权限和固定版本将缺少的 CI/发布/预定工作流添加到遗留项目中。
- **基于场景**：为给定场景生成 YAML（例如“仅在 PR 上运行测试”、“在标签上构建和发布”）。

**何时使用**：当用户或项目需要“为当前或指定项目创建或添加 GitHub 工作流”时。

**范围**：此技能的输出遵循**嵌入式附录 A**（狭窄的触发器、最小权限、固定版本、可审核）。通用模板（例如 Skills.sh `github-actions-templates`）更加通用；这项技能强调安全性和可维护性。

---

## 行为（行为）

### 原则（原则）

- **附录A具有权威性**：输出的YAML必须满足附录A（结构、命名、安全性、可维护性）。
- **窄触发器**：`on`必须指定分支/路径/标签；避免每次推送时触发。常见模式：带有“branches”或“paths”的“push”/“pull_request”。 **发布** 工作流必须仅在版本标签上触发（例如`push:tags:['v*']`）并且存在于与 CI 不同的文件中。
- **最小权限**：当工作流需要repo write、PR或Secrets时，将工作流或作业级别的“权限”设置为所需的最低权限；例如CI `内容：读取`，释放`内容：写入`，`包：写入`；避免“全部”。
- **固定版本**：固定第三方操作（提交 SHA 或主要版本标签）；不要使用“@master”或未固定的引用；更喜欢安全/扫描操作的特定版本（例如 Trivy）。

### 语气和风格

- 使用客观的技术语言；保持工作流程和步骤“名称”简短且便于操作日志阅读。
- 匹配项目堆栈：按项目类型（Node/Python/Go/Rust）和现有约定选择运行器、包管理器和构建命令；如果项目已经有工作流程，请调整命名和风格。

### IN（输入）驱动

- 若存在 `CLAUDE.md` 或 `.ai-cortex/config.yaml`，优先读取其中的 `test_command`、`base_branch` 等；否则从用户输入或项目推断。参见 [docs/guides/project-config.md](../../docs/guides/project-config.md)。
- 使用用户的**场景**（例如“CI：在 PR 上运行测试”、“发布：在标签上构建和上传”）和 **堆栈**（语言、包管理器、测试/构建命令）来生成工作流；当信息丢失时使用合理的占位符并将其标记为替换；不要发明命令或路径。

### 交互（互动）

- **写入前确认**：生成YAML后，列出**必填注释**（占位符、分支名称、用户必须设置的Secret名称），然后要求确认；不要写入 `.github/工作流s/` 或在未经用户确认的情况下提交。
- **多个文件/发布**：如果生成多个工作流（例如 CI + Release）或使用写入权限（`contents: write`、`packages: write`），列出要创建/覆盖的文件和权限范围，然后在写入之前确认。
- **冲突**：如果目标路径已经存在目的相同或重叠的工作流，则警告并询问是否覆盖或保存到其他地方；不要默默地覆盖。

---

## 输入与输出 (Input & Output)

### 输入（输入）

- **场景**：目的（CI、PR 检查、发布、计划、矩阵）。
- **Stack**：语言和版本（例如 Node 20、Python 3.11、Go 1.21）、包管理器（npm/pnpm/yarn、pip、cargo）、测试/构建/发布命令。
- **触发器**：分支（例如`main`、`develop`）、路径过滤器、可选的`工作流_dispatch`。
- **目标路径**：写入文件的位置，默认项目根目录下的`.github/Workflows/`；对于多个工作流，指定每个文件名（例如“ci.yml”、“release.yml”）。

### 输出（输出）

- **工作流 YAML**：完整文件内容符合附录 A，准备写入 `.github/工作流s/<name>.yml`。
- **注释**：列出占位符（例如“npm run test”、分支“main”）、秘密名称以及用户必须配置的任何项目。

---

## 限制（限制）

### 硬边界（Hard Boundaries）

- **不要违反附录A**：输出必须有`name`、`on`、`jobs`，并且每个作业必须有`runs-on`和`steps`；不要使用未固定的第三方操作或硬编码的机密。
- **不要过度触发**：除非用户明确请求，否则不要使用没有分支/路径过滤器的裸“on:push”。
- **不要发明命令**：对未知的测试/构建/发布命令使用占位符并标记“替换为实际命令”；不要发明脚本或路径。
- **不要忽略现有的工作流**：如果项目已经有`.github/工作流/`，请调整命名和风格并避免重复或冲突。
- **不要重复构建逻辑**：如果项目使用 GoReleaser、Dockerfile 等进行构建和镜像塑造，则工作流程仅触发、登录并传递参数（例如 `GITHUB_TOKEN`、`BUILDX_BUILDER`）；不要重新实现该逻辑。

### 技能边界 (Skill Boundaries)

**不要做这些**（其他技能可以处理它们）：

- 不要链接到文档或自述文件技能 - 单独调用它们
- 未经用户确认，请勿写入 `.github/工作流s/`
- 不要默默地覆盖现有的工作流程
- 不要重新实现 `.goreleaser.yaml` 或 Dockerfiles 中已定义的构建/发布逻辑
- 不要为非 GitHub 平台（GitLab CI、Jenkins 等）生成 CI/CD

**何时停止并交接**：

- 编写工作流文件并确认后，如果需要 README/AGENTS.md 更新，请移交给文档技能
- 当用户需要注册表或机密配置时，提供指导但不自动进行外部服务设置

---

## 自检（Self-Check）

### 核心成功标准

- [ ] **符合附录 A**：输出满足附录 A 中的所有强制结构和安全需求（名称、工作、运行、步骤、固定操作、无硬编码秘密）
- [ ] **窄触发器**：`on`块的范围仅限于特定分支/路径/标签 - 没有没有过滤器的裸露`on：push`
- [ ] **最小权限**：在工作流程或作业级别将“权限”设置为场景类型所需的最低权限
- [ ] **堆栈对齐**：运行程序、语言版本、包管理器和命令与用户指定的堆栈匹配
- [ ] **写入前用户确认**：列出必需的注释和占位符，并在写入 `.github/Workflows/` 之前获得用户确认

### 流程质量检查

- [ ] **附录 A**：输出是否满足附录 A 中的强制结构和安全性？
- [ ] **触发器**：“on”是否缩小到特定分支/路径/标签？
- [ ] **权限和安全**：是否设置了最小“权限”？第三方操作已固定？没有硬编码的秘密吗？
- [ ] **可运行**：用户替换占位符后，工作流能否在目标仓库中运行？
- [ ] **堆栈对齐**：运行程序、语言版本、包管理器和命令是否与用户的堆栈匹配？
- [ ] **步骤顺序和依赖关系**：对于多步骤作业（例如 QEMU → Buildx → 登录 → GoReleaser），顺序是否正确以及 ids/env 变量是否已传递？请参阅 Go + Docker + GoReleaser 的 **附录 B**。

### 验收测试

用户替换占位符后，除了秘密名称和环境特定值之外，工作流是否可以在目标存储库中运行而无需进一步修改？

---

## 示例（示例）

### 示例 1：节点 CI（测试 + PR 上的 lint）

**输入**：场景：CI。堆栈：节点 20、pnpm、测试 `pnpm test`、lint `pnpm lint`。触发器：“pull_request”到“main”。文件：`ci.yml`。

**预期**：带有“name”的单个“ci.yml”，例如“CI”； `on: pull_request: 分支: [main]`;在 `ubuntu-latest` 上进行工作，包括结帐、设置 Node/pnpm、安装、lint、测试；使用固定的官方“actions/checkout”和“pnpm/action-setup”（或同等内容）；没有硬编码的秘密；如果设置了“权限”，则为只读。

### 示例 2：使用路径过滤器进行 PR 检查

**输入**：场景：PR 检查。堆栈：Go 1.21，测试“go test ./...”。仅当 `go.mod` 或 `*.go` 更改时触发。文件：`pr-check.yml`。

**预期**：`on.pull_request` 和 `paths: ['**.go', 'go.mod']`；固定“actions/setup-go”的工作，步骤结账，设置 Go，进行测试；如果不需要写入，则省略“权限”或“内容：读取”。

### 示例 3：Go 发布（Docker + GHCR + GoReleaser）

**输入**：场景：CD/发行版。堆栈：Go、Docker 多架构 (amd64/arm64)、GoReleaser for image 和 GitHub Release。触发器：仅“push”标签“v*”。文件：`release.yml`。

**预期**：`on:push:tags:['v*']`; `权限`包括`内容：写`、`包：写`。步骤：签出（`fetch-深度：0`）→设置Go（`go-version-file：go.mod`，缓存）→设置QEMU（`linux/amd64`，`linux/arm64`）→设置Docker Buildx（`id：buildx`，相同平台）→登录GHCR（`docker/login-action`，`ghcr.io`）→GoReleaser（`goreleaser/goreleaser-action` pinned, pass `GITHUB_TOKEN` and `BUILDX_BUILDER: ${{ steps.buildx.outputs.name }}`).不要重新实现 `.goreleaser.yaml`/Dockerfile 中定义的逻辑。 **参见附录 B**。

### 示例 4（边缘）：最少信息

**输入**：项目：legacy-api。没有描述。语言和命令未知。用户想要“至少一个 CI 占位符工作流程”。

**预期**：生成一个结构完整、符合附录 A 的 YAML；对运行程序和步骤使用占位符（例如“指定运行程序和安装/测试命令”）并标记“要替换”；保持“on”范围较小（例如“pull_request:branches:[main]”）；不要发明测试或构建命令；保留“name”、“on”、“jobs”、“runs-on”、“steps”和推荐字段（例如“permissions”），以便用户稍后填写。

---

## 附录 A：工作流输出契约

以下是此技能生成的工作流文件的**强制**；使用本附录进行自检。

**范围**：此技能为项目的 `.github/工作流s/` 生成的 YAML 工作流文件。

### A.1 文件和路径

- **位置**：必须位于目标项目的 `.github/Workflows/` 下。
- **命名**：`kebab-case`，扩展名`.yml`或`.yaml`；名称应反映目的（例如“ci.yml”、“pr-check.yml”、“release.yml”）。
- **一文件一个工作流**：一个文件定义一个工作流；对于复杂的情况分成多个文件；避免在一个文件中出现许多不相关的作业。

### A.2 所需结构

每个工作流 YAML 必须包含（推荐顺序）：

|领域|必填 |描述 |
| :------------------ | :----- | :-------------------------------------------------------------------------------------------------------------------------------------------- |
| `名称` |是的 |在 GitHub UI 中显示名称；简短易读（例如“CI”、“PR 检查”、“发布”）。                                                |
| `上` |是的 |触发器：`push`、`pull_request`、`工作流_dispatch`等；必须缩小分支/路径/标签；避免没有过滤器的广泛“on:push”。 |
| `工作` |是的 |至少一份工作；每个作业必须有“runs-on”和“steps”。                                                                      |
| `jobs.<id>.runs-on` |是的 |运行程序（例如“ubuntu-latest”）。                                                                                                   |
| `jobs.<id>.steps` |是的 |步骤列表；每个步骤都有“名称”（人类可读）和“使用”或“运行”。                                                        |

可选但推荐：`permissions`、`concurrency`、`env`。

### A.3 命名和可读性

- **作业 ID**：`kebab-case`，含义明确（例如`build`、`test`、`lint`、`deploy-preview`）。
- **步骤名称**：操作日志的简短、可扫描的描述。
- **工作流程名称**：与存储库中的文件名和其他工作流程对齐。

### A.4 安全和最小权限

- **权限**：如果未设置“权限”，GitHub 将使用默认的“GITHUB_TOKEN”权限。对于敏感操作，请将工作流或作业级别的“权限”设置为所需的最低限度。 **按类型**：CI（仅限构建/测试/扫描）→ `内容：读取`；发布（发布，GHCR 推送）→ 明确的 `contents: write`, `packages: write`;避免默认或“全部”。
- **Secrets**：通过Secrets注入秘密；切勿在 YAML 中对密钥、令牌或密码进行硬编码。
- **第三方操作**：首选官方或广泛使用的操作； pin 版本（提交 SHA 或主要版本标签）；不要使用“@master”或取消固定；使用特定版本进行安全/扫描操作以减少偏差。

### A.5 可维护性

- **CI 与 CD（推荐）**：CI 仅构建、测试和扫描； **没有发布**。 CD（图像推送、GitHub 发布）仅在版本标签上运行（例如“v*”）。使用单独的文件（例如 `ci.yml`、`release.yml`）；不要在一个工作流中混合“每次推送时运行”和“仅在标签上发布”。
- **重用**：将通用逻辑提取到复合​​操作或可重用的工作流中。
- **注释**：简要注释非明显的触发器、矩阵策略或环境使用情况；保持评论简短。
- **项目对齐**：Runner、语言版本、包管理器和命令必须与目标项目匹配；如果项目有现有的工作流程，请调整样式和命名。

### A.6 自检（生产者）

制作工作流程后：

- [ ] 文件位于 `.github/Workflows/` 下，名称为短横线大小写。
- [ ] 包含`name`、`on`、`jobs`；每个作业都有“runs-on”和“steps”。
- [ ] `on` 缩小到特定分支/路径/标签。
- [ ] 无硬编码秘密；固定的第三方操作（安全/扫描的特定版本）。
- [ ] 步骤和作业名称清晰；与项目堆栈和现有工作流程风格一致。
- [ ] YAML 有效（缩进，无重复键）；步骤顺序和依赖关系正确。

---

## 附录 B: Go + Docker + GHCR + GoReleaser

**Go + Docker + GHCR + GoReleaser** 工作流程的约定和实践；生成或编辑此类工作流程时，请同时遵循主要技能和附录 A。

### B.1 布局

- **CI 和 CD 分开**：两个工作流程。
  - **CI**（例如 `ci.yml`）：`push`/`pull_request` 到主分支。仅构建、测试、安全扫描； **没有发布**。
  - **CD**（例如`release.yml`）：仅在版本标签的`push`上（例如`v*`）。发布图像和 GitHub 发布。
- 不要在一个工作流中混合“每次推送时运行”和“仅在标签上发布”。

### B.2 权限

- 明确设置“权限”。 CI：`内容：已读`。发布：`内容：写入`，`包：写入`。不要使用“全部”。

### B.3 步骤和顺序

#### 去

- 将 `actions/setup-go@v5` 与 `go-version-file: go.mod` 一起使用。启用“缓存：true”。对于发布，请使用 `fetch-depth: 0` 进行检查（GoReleaser 需要）； CI 可以使用相同的方法来保持一致性。

#### CI（订单示例）

1. 签出（`获取深度：0`）
2. 设置 Go (go.mod + 缓存)
3. `去测试./...`
4. govulncheck： `go install golang.org/x/vuln/cmd/govulncheck@latest` 然后 `govulncheck ./...`
5. Docker Buildx（仅设置，单一平台）
6. 构建用于扫描的镜像：单架构`linux/amd64`、`push: false`、`load: true`、标签例如`local/your-app:ci-${{ github.sha }}`
7. 对该图像的琐碎：`severity: HIGH,CRITICAL`、`ignore-unfixed: true`、`exit-code: 1` 所以 CI 在发现上失败

仅在发布版本中使用多架构； CI 扫描单拱形以提高速度。

#### 发布（示例订单）

1. 签出（`获取深度：0`）
2. 设置 Go (go.mod + 缓存)
3. 设置 QEMU： `docker/setup-qemu-action`, `platforms: linux/amd64,linux/arm64`
4. 设置 Docker Buildx：`id: buildx`, `driver: docker-container`, `platforms: linux/amd64,linux/arm64`
5. 登录 GHCR：`docker/login-action`，注册表`ghcr.io`，密码`secrets.GHCR_TOKEN || Secrets.GITHUB_TOKEN`, `注销：true`
6. GoReleaser：`goreleaser/goreleaser-action@v6`，`args：release --clean`，env`GITHUB_TOKEN`和`BUILDX_BUILDER：${{steps.buildx.outputs.name}}`

QEMU 在 Buildx 之前； Buildx `platforms` 必须与 QEMU 匹配。 GoReleaser 需要多架构的 Buildx 构建器名称，因此设置 `id: buildx` 并传递 `BUILDX_BUILDER`。

### B.4 与 repo 配置的关系

- **Docker 镜像**：形状在 `.goreleaser.yaml` 和 Dockerfile 中定义； 工作流不重复构建逻辑。
- **GHCR**：GoReleaser 配置中的图像路径和标记； 工作流仅登录并传递`GITHUB_TOKEN`和Buildx构建器。
- **Makefile**：本地构建/测试可以保留； CI 步骤可以与 Make 目标保持一致，但不必依赖于它们。

### B.5 编辑时

1. **全流程**：更换一项工作可能会影响整个流程；验证结账 → Go → QEMU → Buildx → 登录 → GoReleaser 订单和依赖项。
2. **Action 版本**：使用当前主要版本（例如 `checkout@v4`、`setup-go@v5`、`setup-buildx-action@v3`、`goreleaser-action@v6`）；升级时检查变更日志以了解重大更改。
3. **Trivy**：固定版本（例如`@0.33.1`）以避免行为变化导致 CI​​ 损坏。
4. **YAML**：检查缩进并且没有重复的键；编辑后使用工具进行验证。

### B.6 经验教训

|问题 |方法|
| ：------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------ |
|单一工作流程太大 |分为 **CI + Release**：CI 用于构建/测试/扫描，仅通过 GoReleaser 在标签上发布；更清晰的权限和逻辑。           |
| GHCR 身份验证太复杂 |使用最小登录（`docker/login-action` + token）；避免可能导致错误失败的繁重身份验证。                                   |
|多架构清单验证失败 | **每个平台** 拉取并验证，而不是通用清单拉取。                                                              |
|日期/版本格式不一致 |在工作流和 Dockerfile 中使用一种格式（例如 ISO8601）；如果使用 GoReleaser 输出，请将 `dist/` 添加到 `.gitignore`。                 |
| GoReleaser 多架构构建失败 | GoReleaser 需要 Buildx 构建器：在 Buildx 步骤上设置 **id: buildx** 并传递 **BUILDX_BUILDER: ${{ steps.buildx.outputs.name }}**。 |
|版本漂移 |使用合理的版本限制并在升级时检查发行说明；首先在分支上进行验证。                            |

**检查工作流历史**：`git log --oneline -- .github/工作流/`

---

## 参考（参考文献）

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [工作流语法](https://docs.github.com/en/actions/using-工作流s/工作流-syntax-for-github-actions)
- [安全强化](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)