---
artifact_type: rule
name: standards-cross-team-contracts
version: 1.0.0
scope: 两个或更多独立演进的 service / repo / team 之间共享的接口、数据形状、状态机、事件 payload
recommended_scope: user
status: active
created_at: 2026-05-09
---

# Rule: 跨团队契约协作 (Cross-Team Integration Contracts)

## 适用范围 (Scope)

凡满足以下任一条件的契约文件，均适用本规则：

- 描述本仓库**对外提供**的接口、数据形状、状态机、事件 payload，并被另一个独立演进的 repo / team / service 消费。
- 描述本仓库**对外消费**的第三方接口（profile 文件），需要追踪上游版本演化。
- OpenAPI / JSON Schema / Protobuf / 事件 schema 等机器可读契约。

不适用：仓库内部模块之间的接口（同一团队、同一发布周期），那是设计文档（`-design.md`）而不是契约。

## 强制约束 (Constraints)

### 1. **单向广播，禁止双向 todo 跟踪**

Provider 在自己的 contract 文件里维护 SemVer + CHANGELOG；consumer 各自决定何时升级、自有 backlog 跟踪实施进度。

- ❌ 在 contract 文档里写「Phase A：对方团队 D+3 完成 X」「@xxx 团队待办」
- ❌ 在 contract 文档里维护跨团队联调里程碑表
- ✅ Contract 只声明「v1.2.0 起新增 X 字段、消费者按需自适配」；实施排期在各自仓库的 `tasks.md` 或 backlog
- ✅ 上游变更通过 CHANGELOG 通知；下游不订阅时，CI/PR 不会被对方的进度阻塞

**为什么**：双向 todo 跟踪会把对方的实施细节渗进自己的产品文档，contract 变成跨团队甘特图；一旦对方排期漂移，本仓库的契约文档要被动改写。Provider 单向广播 + Consumer 自跟踪是 Pact、OpenAPI 等行业实践的最小公约数。

### 2. **SemVer + CHANGELOG 是最小可行版本化协议**

每个 contract 文件必须在 frontmatter 或正文显著位置声明 `contract_version: MAJOR.MINOR.PATCH`，并在文件末尾或专门 `CHANGELOG.md` 维护版本史。

| 类型 | 触发条件 |
| --- | --- |
| **MAJOR** | 删字段 / 改 URL / 改状态机语义 / 改枚举值含义 |
| **MINOR** | 新增字段 / 新增端点 / 新增枚举值 / 行为兼容扩展 |
| **PATCH** | 文档修订 / 错误码补充 / 示例更新 |

每次 bump 必须留 CHANGELOG 条目，含：变更类型（Added / Changed / Removed / BREAKING）、影响面、向后兼容性说明、引用的代码位置或 PR 链接。

- ❌ 修改字段语义但 contract_version 没动，对方靠 git diff 才发现
- ❌ CHANGELOG 写「1.5.0 完善文档」（无信息量）
- ✅ `### 1.8.0 — 2026-05-09` + 「**Changed (BREAKING for un-shipped consumers)**: chunkId → feedbackId（理由 + 实现链接 + 兼容性说明）」

**为什么**：consumer 升级前需要快速判断「是否影响我的代码」。SemVer 给出第一层过滤（PATCH 可无脑跟、MAJOR 必读），CHANGELOG 给出第二层（具体改了什么）。没有这两层，每次升级都要 diff 全文。

### 3. **文件命名以后缀显式标注契约类型**

| 后缀 | 含义 | 示例 |
| --- | --- | --- |
| `*-contract.md` | 跨团队接口/数据/生命周期契约（强制承诺） | `lifecycle-contract.md` |
| `*-design.md` | 内部设计意图（不对外承诺） | `lifecycle-design.md` |
| `*-guide.md` | 使用指南 / 集成手册 | `bff-integration-guide.md` |
| `*-schema.md` | 数据结构 schema 描述 | `patch-schema.md` |
| `*-profile.md` | 第三方接口的本地剖面 | `<upstream>-server-api-profile.md` |

强制要求：跨团队消费的文件**必须**用 `-contract` 后缀。设计文件**禁止**用 `-contract` 后缀（即使写得很正式）。

- ❌ 同时存在 `system-contract.md` 和 `system-spec.md` 指代同一接口
- ❌ 把设计意图（待选方案、tradeoff 讨论）放进 `-contract.md`
- ❌ 把对外承诺的字段映射放进 `-design.md`
- ✅ `field-mapping-contract.md`（对外，强制）+ `field-mapping-design.md`（如有，内部 tradeoff）

**为什么**：consumer 一眼能识别哪些文件是承诺、哪些是内部讨论；`grep -- '-contract\.md$'` 即可拿到本仓库所有对外承诺的清单。

### 4. **契约目录扁平化**

不要建 `contracts/` 子目录把契约和设计分两层；用文件名后缀承担类型语义即可。

- ❌ `integrations/<x>/contracts/lifecycle-contract.md` + `integrations/<x>/lifecycle-design.md`（同一域两层）
- ✅ `integrations/<x>/lifecycle-contract.md` + `integrations/<x>/lifecycle-design.md`（同一域一层）

例外：当一个集成域的契约数 ≥10 且来自异质来源（如多个上游产品的 `*-profile.md` 各自独立）时，可以建子目录按来源分组（例如 `upstream/zentao/`、`upstream/jira/`），但同一来源内部仍扁平。

**为什么**：`contracts/` 子目录是伪结构——文件后缀已经标注了类型，再用目录区分一遍是冗余；引用路径变长（`../../../foo` 一堆）；新人理解成本高（要先理解「为什么 lifecycle-contract 在 contracts/ 但 lifecycle-design 不在」）。

### 5. **跨 repo 引用契约时锚定版本号，不锚定文件路径**

下游 repo 在自己的代码 / 文档里引用上游 contract 时，必须引用 `contract_version`（如 `lifecycle-contract@1.0.0`）而不是 git commit hash 或文件 URL。

- ❌ 「按 https://github.com/upstream/repo/blob/main/contracts/foo.md 实现」（main 分支会变）
- ❌ 「参考 commit abc1234 的 contract」（除非是受冻结的快照引用）
- ✅ 「实现 `lifecycle-contract@1.0.0`」+ 在升级时改成 `@1.1.0`
- ✅ Contract 文件本身在 frontmatter 写 `contract_version: 1.0.0`，downstream 代码注释引用版本号

**为什么**：URL/commit 引用强耦合上游目录结构；版本号是**承诺**，不会因为文件迁移、目录重构而失效（`lifecycle-contract@1.0.0` 始终指向同一份语义，无论文件搬到哪）。

## 违规示例 (Bad Patterns)

```markdown
<!-- ❌ contract 文档里写实施清单 -->
## §6 任务归档约定

- [ ] Phase A：对方团队实现 lifecycle UI（D+3）
- [ ] Phase B：联调 + 验收（D+5）
- [ ] @zhangsan 负责 Phase C
```

```markdown
<!-- ❌ 改字段没动版本 -->
contract_version: 1.5.0
（实际把 chunkId 改成 feedbackId 了，CHANGELOG 没动）
```

```markdown
<!-- ❌ 命名歧义 -->
docs/integration/foo-spec.md       # 是 spec 还是 contract？
docs/integration/foo-contract.md   # 跟上面是同一份？
```

```text
<!-- ❌ 子目录冗余 -->
docs/integrations/<x>/clarification/
  contracts/
    lifecycle-contract.md
    split-contract.md
  lifecycle-design.md
  split-design.md
```

```markdown
<!-- ❌ 强耦合 URL -->
按照 https://gitlab/repo/-/blob/main/api.md 实现接口。
```

## 修正指南 (Remediation)

1. **清理实施清单**：把 contract 文档里的 Phase / 待办 / 联调表挪进各方仓库的 `backlog.md` 或 `tasks.md`；contract 只保留 SemVer 表 + CHANGELOG。
2. **补足版本头**：每个 `*-contract.md` 在 frontmatter 加 `contract_version: 1.0.0`（首次落地写 1.0.0，后续按 SemVer 递增）；首次落地的 CHANGELOG 写 `### 1.0.0 — YYYY-MM-DD`，注明 Initial Release 内容。
3. **改名统一后缀**：所有跨团队消费文件改成 `-contract.md`；设计文件去掉「contract」字样。
4. **拆 contracts/ 子目录**：用 `git mv contracts/foo.md foo.md` 把 `*-contract.md` 提到与 `*-design.md` 同级，并 `grep -rl 'contracts/foo' . | xargs sed -i '' 's|contracts/foo|foo|g'` 同步引用。
5. **替换 URL 引用为版本号**：下游代码注释、跨 repo 文档把 `<URL>` 引用改为 `<contract-name>@<version>`。

## 与其他规则的关系

- **互补 `standards-documentation`**：那条 rule 约束**所有**文档的 frontmatter 必填字段（`artifact_type` / `created_by` / `lifecycle` / `created_at`）；本 rule 只约束**契约类**文档额外的 `contract_version` 与 CHANGELOG。两者并行生效。
- **互补 `workflow-documentation`**：那条 rule 约束临时文档不要泛滥；本 rule 处理已经决定保留的契约文档怎么演化。
- **互补 `standards-nats-integration`**：那条 rule 约束 NATS / JetStream 的运行时消息治理（subject、headers、原语选型）；本 rule 约束契约文档本身的写法与版本化。两者正交，跨团队场景同时生效。
- **不重叠 `standards-coding`**：`-coding` 是单仓库内的代码规范；本 rule 是跨仓库的协作规范。

## 落地参考

AgentFabric 项目（recloud-agentfabric）的 `docs/architecture/integrations/zentao/clarification/lifecycle-contract.md` 是符合本规则的范例：

- §头部 frontmatter 含 `contract_version: 1.0.0`
- §5 是 SemVer 表 + CHANGELOG（首条 v1.0.0 — 2026-05-09 Initial Release）
- 同目录的 `lifecycle-design.md` 承担设计意图，不冒充契约
- 没有 `contracts/` 子目录，扁平布局
- 不跟踪禅道项目组的 Phase 排期，只单向广播版本变更

`contracts/CHANGELOG.md` 是 OpenAPI 契约（机器可读）的对应实践——`clarification-api.yaml` 1.7.0 → 1.8.0（BREAKING：chunkId → feedbackId）→ 1.9.0（Added：getBadges），每次 bump 都伴随完整的 Added / Changed / Removed 条目 + 实现链接 + 兼容性说明。

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| 1.0.0 | 2026-05-09 | 初版：单向广播、SemVer + CHANGELOG、文件后缀语义化、扁平布局、版本号引用五约束 |
