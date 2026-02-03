---
name: generate-github-workflow
description: 为项目创建符合规范的 GitHub Actions 工作流；支持 CI（构建/测试/发布）、PR 检查、定时任务等常见场景。
tags: [devops, eng-standards]
version: 1.0.0
related_skills: []
recommended_scope: project
---

# Skill: 生成 GitHub Workflow (Generate GitHub Workflow)

## 目的 (Purpose)

为**各类软件项目**快速生成**符合本技能「附录 A：Workflow 产出规范」约定**的 GitHub Actions 工作流文件。通过标准化的结构、触发条件与安全约定，降低 CI/CD 配置成本，提升可维护性与可审计性，并避免常见安全与权限问题。本技能仅产出工作流 YAML，不自动链式触发文档或规则类技能；若用户需后续更新 README 或 AGENTS.md 等，可另行调度对应技能。

---

## 适用场景 (Use Cases)

- **新项目基建**：为新仓库快速添加 CI（构建、测试、Lint）或 PR 检查工作流。
- **统一工程规范**：为企业内多仓库统一工作流风格与命名，便于运维与审计。
- **补齐流水线**：为遗留项目补充缺失的 CI/发布/定时任务，且符合最小权限与版本固定约定。
- **按场景定制**：根据用户指定的场景（如「仅 PR 时跑测试」「发布时打 tag 并构建产物」）生成对应 YAML。

**何时使用**：当用户或项目需要「为当前/指定项目创建或补充 GitHub Workflow」时。

---

## 行为要求 (Behavior)

### 核心原则

- **以附录 A 为据**：产出的 YAML 必须符合本技能「附录 A：Workflow 产出规范」中关于结构、命名、安全与可维护性的约定。
- **触发收窄**：`on` 须明确分支/路径/标签等，避免对全仓任意 push 触发；常用模式为 `push`/`pull_request` 配合 `branches` 或 `paths`。**发布类** workflow 触发须收窄到版本 tag（如 `push: tags: ['v*']`），且与 CI 分文件，不在同一 workflow 里混「每次 push」与「仅 tag 发布」。
- **最小权限**：涉及仓库读写、PR、Secrets 时，在工作流或 job 级别显式声明 `permissions`，仅授予必要范围；CI 用 `contents: read`，发布类用 `contents: write`、`packages: write` 等，避免 `all`。
- **版本固定**：使用的第三方 Action 须固定版本（commit SHA 或带主版本号的 tag），禁止 `@master` 或未指定版本；安全/扫描类（如 Trivy）建议用具体版本号。

### 语气与风格

- 使用**客观、技术化**的语言；step `name` 与工作流 `name` 简洁可读，便于在 Actions 日志中定位。
- 与目标项目技术栈一致：根据项目类型（Node/Python/Go/Rust 等）与既有约定选择运行器、包管理器与构建命令；若项目已有 workflow，风格与命名应与之协调。

### 输入驱动

- 根据用户提供的**场景**（如「CI：PR 时跑测试」「发布：打 tag 时构建并上传 Release」）与**技术栈**（语言、包管理器、测试/构建命令）生成对应工作流；缺失信息时使用合理默认并标注可替换占位符，不虚构命令或路径。

### 交互策略 (Interaction)

- **产出后核对**：生成工作流 YAML 后，须先输出**必要说明**（占位符、分支名、Secrets 名称等需用户替换或配置的项），再请用户确认或补充；未经用户确认不得直接写入目标仓库的 `.github/workflows/` 或提交。
- **多文件/发布类**：若一次生成多个 workflow（如 CI + Release）或涉及发布权限（`contents: write`、`packages: write`），须在写入前明确列出将创建/覆盖的文件与权限范围，由用户确认后再执行写入。
- **与既有 workflow 冲突**：若目标路径下已存在同名或语义重叠的 workflow，须提示用户并询问覆盖或另存；不得静默覆盖。

---

## 输入与输出 (Input & Output)

### 输入 (Input)

- **场景**：工作流用途（如 CI、PR 检查、发布、定时任务、多矩阵构建）。
- **技术栈**：语言与版本（如 Node 20、Python 3.11、Go 1.21）、包管理器（npm/pnpm/yarn、pip、cargo）、测试/构建/发布命令。
- **触发偏好**：分支（如 `main`、`develop`）、路径过滤（如仅 `src/` 变更时触发）、是否支持 `workflow_dispatch`。
- **目标路径**：工作流文件拟写入的路径（默认为项目根下的 `.github/workflows/`）；若为多工作流，须明确每个文件名（如 `ci.yml`、`release.yml`）。

### 输出 (Output)

- **标准工作流 YAML**：符合本技能「附录 A：Workflow 产出规范」的完整文件内容，可直接写入 `.github/workflows/<name>.yml`。
- **必要说明**：若使用了占位符（如 `npm run test`、分支名 `main`）、Secrets 名称或需用户后续配置的项，须在交付时简要列出，便于用户替换或创建 Secret。

---

## 禁止行为 (Restrictions)

- **禁违反附录 A**：不得产出缺少 `name`、`on`、`jobs` 或 job 内 `runs-on`/`steps` 的 YAML；不得使用未固定版本的第三方 Action 或硬编码密钥。
- **禁过度触发**：不得使用仅 `on: push` 且无任何分支/路径过滤的配置，除非用户明确要求。
- **禁虚构命令**：未提供的测试/构建/发布命令应使用占位符并注明「请替换为实际命令」，不得编造项目不存在的脚本或路径。
- **禁忽略项目既有约定**：若项目已有 `.github/workflows/` 下文件，新工作流命名与风格须与之协调，避免重复或冲突。
- **禁重复构建逻辑**：若项目使用 GoReleaser、Dockerfile 等定义构建与镜像形态，workflow 只负责触发、登录与传参（如 `GITHUB_TOKEN`、`BUILDX_BUILDER`），不重复实现应由上述配置定义的构建逻辑。

---

## 质量检查 (Self-Check)

- [ ] **附录 A 合规**：产出是否满足本技能「附录 A：Workflow 产出规范」中强制性结构与安全约定？
- [ ] **触发收窄**：`on` 是否已收窄到明确分支/路径/标签？
- [ ] **权限与安全**：是否显式声明了最小所需 `permissions`？第三方 Action 是否已固定版本？无硬编码密钥？
- [ ] **可运行性**：用户将占位符替换为实际命令/分支/Secret 后，是否能在目标仓库内正常运行？
- [ ] **与项目一致**：运行器、语言版本、包管理器与命令是否与用户提供的技术栈一致？
- [ ] **步骤顺序与依赖**：多步骤 job（如 QEMU→Buildx→登录→GoReleaser）是否顺序正确、必要 id 与环境变量是否传递完整？生成 Go + Docker + GoReleaser 类 workflow 时见**附录 B**。

---

## 示例 (Examples)

### 示例 1：Node 项目 CI（PR 时测试 + Lint）

**输入**：场景：CI。技术栈：Node 20，pnpm，测试 `pnpm test`，Lint `pnpm lint`。触发：`pull_request` 针对 `main`。文件名：`ci.yml`。

**预期产出要点**：单文件 `ci.yml`，`name` 如「CI」；`on: pull_request: branches: [main]`；job 使用 `ubuntu-latest`，步骤为 checkout、setup Node/pnpm、install、lint、test；使用官方 `actions/checkout` 与 `pnpm/action-setup`（或等效）并固定版本；无硬编码密钥；若需 `permissions` 则仅读权限。

### 示例 2：Go 项目 PR 检查 + 路径过滤

**输入**：场景：PR 检查。技术栈：Go 1.21，测试 `go test ./...`。仅当 `go.mod` 或 `*.go` 变更时触发。文件名：`pr-check.yml`。

**预期产出要点**：`on.pull_request` 带 `paths: ['**.go', 'go.mod']`；job 中 `actions/setup-go` 固定版本，步骤 checkout、setup Go、go test；无写权限需求时 `permissions` 可省略或设为 `contents: read`。

### 示例 3：Go 项目 Release（Docker + GHCR + GoReleaser）

**输入**：场景：CD/发布。技术栈：Go，Docker 多架构（amd64/arm64），GoReleaser 发布镜像与 GitHub Release。触发：仅 `push` 版本 tag `v*`。文件名：`release.yml`。

**预期产出要点**：`on: push: tags: ['v*']`；`permissions` 含 `contents: write`、`packages: write`。步骤顺序：Checkout（`fetch-depth: 0`）→ Set up Go（`go-version-file: go.mod`，cache）→ Set up QEMU（`linux/amd64,linux/arm64`）→ Set up Docker Buildx（`id: buildx`，`platforms` 与 QEMU 一致）→ 登录 GHCR（`docker/login-action`，registry `ghcr.io`）→ GoReleaser（`goreleaser/goreleaser-action` 固定版本，传 `GITHUB_TOKEN` 与 `BUILDX_BUILDER: ${{ steps.buildx.outputs.name }}`）。不重复实现应由 `.goreleaser.yaml`/Dockerfile 定义的构建逻辑。**详见本技能附录 B**。

### 示例 4（边界）：信息极少的项目

**输入**：项目名：legacy-api。描述：无。语言与命令未知。需要「至少有一个 CI 占位 workflow」。

**预期行为**：仍产出一份结构完整、符合附录 A 的 YAML；在运行器与步骤中使用占位符（如「请指定运行器与安装/测试命令」），并明确标注「待替换」；`on` 仍须收窄（如 `pull_request: branches: [main]`）；不虚构具体测试或构建命令；保留 `name`、`on`、`jobs`、`runs-on`、`steps` 及推荐字段（如 `permissions`），便于用户后续补齐。

---

## 附录 A：Workflow 产出规范

以下为产出的工作流文件须满足的**强制性约定**；自检时以本附录为判定依据。

**范围**：由本技能产出的、用于放入项目 `.github/workflows/` 的 YAML 工作流文件。

### A.1 文件与路径

- **存放位置**：必须位于目标项目的 `.github/workflows/` 目录下。
- **文件命名**：使用 `kebab-case`，扩展名为 `.yml` 或 `.yaml`；文件名应能反映工作流用途（如 `ci.yml`、`pr-check.yml`、`release.yml`）。
- **单文件单职责**：一个文件定义一条工作流；复杂场景可拆分为多个文件，避免单文件内堆积过多不相关 job。

### A.2 强制性结构

每个工作流 YAML 必须包含且顺序建议如下：

| 字段 | 必填 | 说明 |
| :--- | :--- | :--- |
| `name` | 是 | 工作流在 GitHub UI 中的显示名称；简洁、可读，如「CI」「PR 检查」「发布」。 |
| `on` | 是 | 触发条件：`push`、`pull_request`、`workflow_dispatch` 等；须明确分支/路径/标签，避免过于宽泛（如仅 `on: push` 且无分支过滤）。 |
| `jobs` | 是 | 至少一个 job；每个 job 须有 `runs-on` 与 `steps`。 |
| `jobs.<id>.runs-on` | 是 | 运行器，如 `ubuntu-latest`；须明确指定。 |
| `jobs.<id>.steps` | 是 | 步骤列表；每步应有 `name`（人类可读）与 `uses` 或 `run`。 |

可选但推荐：`permissions`、`concurrency`、`env`。

### A.3 命名与可读性

- **Job id**：使用 `kebab-case`，语义清晰（如 `build`、`test`、`lint`、`deploy-preview`）。
- **Step name**：使用简短、可扫读的英文或中文描述，便于在 Actions 日志中定位问题。
- **工作流 name**：与文件名呼应，避免与仓库内其他工作流混淆。

### A.4 安全与最小权限

- **默认权限**：若未声明 `permissions`，GitHub 会对 `GITHUB_TOKEN` 使用默认权限；涉及敏感操作时，应在工作流或 job 级别显式设置 `permissions`，仅授予必要范围。**按类型建议**：CI 仅构建/测试/扫描时用 `contents: read` 即可；发布类（Release、推送 GHCR 等）须显式 `contents: write`、`packages: write` 等，避免默认或使用 `all`。
- **Secret**：敏感信息必须通过 Secrets 注入，不得在 YAML 中硬编码密钥、令牌或密码。
- **第三方 Action**：优先使用官方或广泛采用的 Action，并固定版本（commit SHA 或带主版本号的 tag），避免使用 `@master` 或未固定版本；安全/扫描类（如 Trivy）建议用具体版本号以减少行为漂移。

### A.5 可维护性

- **CI 与 CD 分离（推荐）**：CI 只做构建、测试、安全扫描，**不发布**；CD（发布镜像、GitHub Release 等）仅由版本 tag（如 `v*`）触发。两者分文件（如 `ci.yml` 与 `release.yml`），不在同一 workflow 里混「每次 push 都跑」与「仅 tag 才发布」，以降低权限与逻辑复杂度。
- **复用**：公共逻辑可抽成 Composite Action 或可复用 workflow；重复的 step 序列应考虑抽象。
- **注释**：对非显而易见的触发条件、矩阵策略或环境变量用途，可在 YAML 中用注释简要说明；注释以简体中文或英文均可，保持简洁。
- **与项目一致**：产出的运行器（如 Node/Python/Go 版本）、包管理器、构建命令等须与目标项目的技术栈与既有约定一致；若项目已有部分 workflow，风格与命名应与之协调。

### A.6 质量自检（产出方）

产出工作流文件后，执行以下自检：

- [ ] 文件位于 `.github/workflows/` 且文件名为 kebab-case。
- [ ] 包含 `name`、`on`、`jobs`，且每个 job 包含 `runs-on` 与 `steps`。
- [ ] `on` 已收窄到明确分支/路径/标签，避免对全仓任意 push 触发。
- [ ] 无硬编码密钥或敏感信息；第三方 Action 已固定版本（安全/扫描类建议用具体版本号）。
- [ ] 步骤与 job 命名清晰，与项目技术栈及既有 workflow 风格一致。
- [ ] 修改后做 YAML 校验（缩进、无重复 key）；关键步骤顺序与依赖完整。

---

## 附录 B：Go + Docker + GHCR + GoReleaser 撰写经验

适用于 **Go + Docker + GHCR + GoReleaser** 类项目的约定与经验，在生成或修改该类 workflow 时与本技能正文及附录 A 一并遵循。

### B.1 架构约定

- **CI 与 CD 分离**：两个 workflow，职责清晰。
  - **CI**（如 `ci.yml`）：`push` / `pull_request` 到主分支（如 `main`）。只做构建、测试、安全扫描，**不发布**。
  - **CD**（如 `release.yml`）：仅 `push` 版本标签（如 `v*`）时运行。发布镜像与 GitHub Release。
- **不混在一起**：不在同一 workflow 里既做“每次 push 都跑”又做“只有 tag 才发布”，避免权限过大、逻辑难维护。

### B.2 权限

- **最小权限**：每个 workflow 显式写 `permissions`。
  - CI：`contents: read` 即可。
  - Release：需要 `contents: write`、`packages: write`（GHCR 与 Release 都要）。
- 不默认给 `all`，避免误用 token。

### B.3 技术选型与步骤顺序

**Go**

- 用 `actions/setup-go@v5`，版本用 `go-version-file: go.mod`，与仓库一致。
- 开启 `cache: true`，加速依赖拉取。
- Checkout 时：**Release 需要完整历史**（GoReleaser 等会用到），所以 `fetch-depth: 0`；CI 也可用 `fetch-depth: 0` 以便需要时一致。

**CI 流程顺序（示例）**

1. Checkout（`fetch-depth: 0`）
2. Set up Go（go.mod + cache）
3. 运行测试：`go test ./...`
4. govulncheck：`go install golang.org/x/vuln/cmd/govulncheck@latest` 后 `govulncheck ./...`
5. Docker Buildx（仅 `setup-buildx`，不设多平台）
6. 构建镜像用于扫描：单架构 `linux/amd64`，`push: false`，`load: true`，tag 用本地名如 `local/your-app:ci-${{ github.sha }}`
7. Trivy 扫描该镜像：`severity: HIGH,CRITICAL`，`ignore-unfixed: true`，`exit-code: 1` 使有问题时 CI 失败

**经验**：CI 不发布镜像，只“能构建 + 能扫到高危问题”。多架构放在 Release 做，CI 只扫单架构省时间。

**Release 流程顺序（示例）**

1. Checkout（`fetch-depth: 0`）
2. Set up Go（go.mod + cache）
3. Set up QEMU：`docker/setup-qemu-action`，`platforms: linux/amd64,linux/arm64`
4. Set up Docker Buildx：`id: buildx`，`driver: docker-container`，`platforms: linux/amd64,linux/arm64`
5. 登录 GHCR：`docker/login-action`，registry `ghcr.io`，密码用 `secrets.GHCR_TOKEN || secrets.GITHUB_TOKEN`，`logout: true`
6. GoReleaser：`goreleaser/goreleaser-action@v6`，`args: release --clean`，环境变量传 `GITHUB_TOKEN` 和 `BUILDX_BUILDER: ${{ steps.buildx.outputs.name }}`

**经验**：多架构必须先 QEMU 再 Buildx，且 Buildx 的 `platforms` 与 QEMU 一致。GoReleaser 要拿到 Buildx 的 builder 名字才能正确做多架构构建，所以必须 `id: buildx` 并传入 `BUILDX_BUILDER`。

### B.4 与仓库其他配置的关系

- **Docker 镜像**：发布形态由 `.goreleaser.yaml` 和 Dockerfile（或 `Dockerfile.goreleaser`）决定；workflow 不重复写 Docker 构建逻辑，交给 GoReleaser。
- **GHCR**：镜像路径、标签策略在 GoReleaser 配置里；workflow 只负责登录与传 `GITHUB_TOKEN`/Buildx builder。
- **Makefile**：本地构建/测试保持可用；CI 的步骤可与 Make 目标对齐，但不强依赖。

### B.5 修改 workflow 时的注意点

1. **动一个 job 就整体跑一遍流程**：例如改 Release 时想清楚 checkout → Go → QEMU → Buildx → 登录 → GoReleaser 是否还完整、顺序是否对。
2. **Action 版本**：用当前主版本（如 `checkout@v4`、`setup-go@v5`、`setup-buildx-action@v3`、`goreleaser-action@v6`）；升级时看 changelog，注意 breaking changes。
3. **Trivy**：用固定版本号（如 `@0.33.1`），避免新版本行为变化导致 CI 红。
4. **YAML**：缩进、key 不重复；改完可用在线或本地工具校验。

### B.6 演进与踩坑（通用教训）

| 问题 / 阶段 | 对策与教训 |
|-------------|------------|
| 单体 workflow 体积过大（上千行） | 拆成 **CI + Release** 两个 workflow：CI 负责构建/测试/扫描，Release 仅 tag 触发、走 GoReleaser，权限与逻辑都更清晰。 |
| GHCR 认证步骤过复杂 | 复杂 auth-verify 容易误报失败；**简化为必要登录**（`docker/login-action` + token）即可。 |
| 多架构镜像的元数据校验失败 | 多架构 manifest 不能按「通用」方式拉取校验；改为**按平台分别 pull** 再校验。 |
| 日期/版本格式不统一 | 在 workflow 与 Dockerfile 里统一日期格式（如 ISO8601）；若用 GoReleaser 产出，可将 `dist/` 加入 `.gitignore`。 |
| GoReleaser 多架构构建失败 | GoReleaser 需使用 Buildx 的 builder；在 Release workflow 里为 Buildx 步骤加 **id: buildx**，并传环境变量 **BUILDX_BUILDER: ${{ steps.buildx.outputs.name }}**。 |
| GoReleaser / Action 版本漂移 | 使用较宽松的版本约束（如 `~> v2`）并定期看 release notes；升级时在分支上先验证。 |

**查看当前仓库的 workflow 历史**：`git log --oneline -- .github/workflows/`

---

## 参考资源

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Workflow 语法](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [安全加固](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
