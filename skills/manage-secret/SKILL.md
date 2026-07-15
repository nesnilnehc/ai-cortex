---
name: manage-secret
description: Store, look up, or delete a personal credential (server SSH password, database password, website login, API key/token, certificate passphrase) in the macOS Keychain using a consistent <project>-<env>-<kind> naming scheme, and optionally record a pointer (never the secret itself) in the current project's Claude Code memory. Always use this skill whenever the user asks to save, store, remember, look up, rotate, or delete a password, API key, token, SSH credential, or database credential on this machine — even if they don't say "Keychain" or "security" explicitly, e.g. "save this database password so I don't lose it", "把这个数据库密码存一下", "记一条密钥", "这台服务器的密码帮我记下来", "what's the postgres password for staging again", "delete the old GitHub token from keychain". Do not use this for team-shared secret vaults, CI/CD secret injection, or anything that needs to sync across machines — those need a real secrets manager, not this skill.
description_zh: 在 macOS Keychain 中按 <project>-<env>-<kind> 三段式命名规范存取/删除个人凭据（服务器 SSH 密码、数据库密码、网站登录、API Key/Token、证书口令），并可选在当前项目的 Claude Code 记忆中记一条指针（绝不含密钥本身）。当用户要求保存、记住、查询、轮换或删除密码/API Key/Token/SSH 凭据/数据库凭据时始终使用本技能——即便对方没有明说"Keychain"或"security"，例如"把这个数据库密码存一下""记一条密钥""这台服务器的密码帮我记下来""staging 的 postgres 密码是什么来着""把旧的 GitHub token 从 keychain 删了"。团队共享密钥库、CI/CD 密钥注入、跨机器同步需求不适用本技能，那需要真正的密钥管理服务。
tags: [security, secrets, keychain, macos, credentials, memory]
version: 1.1.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [store keychain secret, save api key, save password, save credential, look up password, rotate secret, delete keychain entry, 存密钥, 记密码, 存到 keychain, 密钥管理, 查密码, 删除密钥]
input_schema:
  type: free-form
  description: A natural-language request naming a credential to store, look up, or delete, plus (for store) the secret value itself.
output_schema:
  type: side-effect
  description: A macOS Keychain generic-password entry created, updated, or deleted via the `security` CLI. Optionally a `reference`-type memory file created under the current project's memory directory plus an updated MEMORY.md index. The confirmation message never echoes the secret value.
---

# 技能（Skill）：密钥管理（Manage Secret）

## 目的（Purpose）

个人本机需要长期记住的密钥/凭据（服务器 SSH、数据库、网站登录、API Key、证书口令），統一存进 macOS Keychain，而不是散落在聊天记录、笔记、明文文件里。命名遵循固定的三段式规范，跨项目、跨环境都能定位到同一条凭据；需要时再补一条不含密钥本身的记忆指针，方便未来的对话直接知道"这个东西存在哪"。

个人本机场景不需要 Docker Vault 或团队级密码管理器——Keychain 的 Generic Password 类别本身就是为这个量级设计的。

## 核心目标（Core Objective）

**首要目标**：给定一句自然语言请求，确定唯一的 Keychain service 名，执行对应的 `security` 命令，且全程不把密钥明文回显到对话里。

**成功标准**（必须全部满足）：

1. ✅ **命名合规**：service 名符合 `<project>-<env>-<kind>` 三段式 kebab-case
2. ✅ **account 真实**：account 是凭据本身的登录账号，不是本机用户名占位
3. ✅ **无静默覆盖**：写入前探测过 service 是否已存在，存在时问过用户
4. ✅ **不泄露**：确认消息、记忆文件正文都不出现密钥明文
5. ✅ **记忆可选**：只有用户明确要求或话里明确暗示时才写记忆文件，不擅自决定

---

## 范围边界（Scope Boundaries）

**做什么**：

- 新增/更新一条 Keychain Generic Password（`security add-generic-password`）
- 查询一条已存的凭据（`security find-generic-password`），仅用于确认存在或供用户自己取值，不主动在对话里打印密钥
- 删除一条凭据（`security delete-generic-password`）
- 按用户要求，在当前项目 memory 目录下新增一条 `type: reference` 记忆，只记 service 名 + account + 取值命令

**不做什么**：

- 不管团队共享密钥库、CI/CD 变量注入——那是 1Password/Vault/GitLab CI Variables 的活
- 不假设跨机器同步——Generic Password 只存本机 `login.keychain-db`
- 不生成密码——用户要生成随机密码时用 `openssl rand -base64 24` 之类的工具，本技能只管存取
- 不在没有明确要求/暗示的情况下写记忆文件——避免每次存密钥都往项目里加一堆 memory 文件

---

## 使用场景（Use Cases）

- "把这个数据库密码存一下，账号是 wright_dev，密码是 xxx，这是 Wright 项目开发库的"
- "记一条密钥：omnireview 生产 Web 后台，账号 nimda，密码 xxx"
- "staging 环境的 postgres 密码是什么来着"
- "把旧的 GitHub token 从 keychain 里删了，service 好像是 shared-na-api"
- "这是我个人博客后台的账号密码，帮我存一下，顺便也记到当前项目的记忆里"（同时触发记忆写入）

---

## 行为（Behavior）

### 阶段 0：分类 — 识别操作类型

先确认执行环境：当前平台非 macOS，或本机没有 `security` 命令（`command -v security` 无输出）→ 停止，告知用户本技能仅支持 macOS Keychain，本机不满足条件（Linux 场景可用 `secret-tool` / `pass`，但不在本技能范围内）。

判断用户是要 **新增/更新**、**查询**，还是 **删除**。三种操作共用同一套字段推断逻辑（阶段 1），只是最终执行的 `security` 子命令不同。

### 阶段 1：提取 — 推断 project / env / kind / account

按下表推断，能推断的不要问，只对真缺且无法推断的字段追问：

| 字段 | 推断线索 | 缺省/兜底 |
|---|---|---|
| project | 用户点名的仓库/项目名（转 kebab-case）；提到"个人"→ `personal`；提到"团队共用"/"多个项目都用"→ `shared`；提到"这个项目"且当前 cwd 在某仓库下 → 用该仓库目录名 | 都判断不出来 → 问用户 |
| env | "生产"/"线上"/prod → `prod`；"开发" → `dev`；"测试"/QA → `test`；"预发"/staging → `staging`；"本地" → `local`；凭据本身没有环境概念（如个人网站账号）→ `na` | 判断不出来 → 问用户 |
| kind | "数据库"/db/postgres/mysql/redis/mongo → `db`；"服务器"/SSH/主机 → `ssh`；"网站"/"网页"/登录 → `web`；API/Token/密钥/key → `api`；"证书"/私钥口令 → `cert` | 判断不出来 → 问用户 |
| account | 用户描述里给出的真实登录账号/用户名 | kind=api 且用户没给账号 → 默认用 `token`；其他 kind 缺账号 → **必须问**，猜错了以后就定位不到 |
| secret（仅新增/更新时需要） | 用户明确给出的值 | 缺失时**必须问**，绝不能编造或留空写入 |
| purpose（可选） | 用户给的一句话说明，或从上下文合成一句简短描述 | 缺失不强制追问 |

拼出 `service = <project>-<env>-<kind>`，全小写 kebab-case。

### 阶段 2：冲突检测（仅新增/更新时）

写入前先探测：

```bash
security find-generic-password -a "<account>" -s "<service>" >/dev/null 2>&1
```

退出码为 0 说明已存在同名条目。此时不要静默覆盖——告诉用户"这个 service 名下已经有一条凭据了，是要覆盖，还是这其实是不同用途、应该换个 kind/env 段"，等用户确认再继续。

### 阶段 3：执行

```bash
# 新增/更新（purpose 缺失时省略 -j，不要传空字符串占位）
security add-generic-password -a "<account>" -s "<service>" -w "<secret>" [-j "<purpose>"] -U

# 查询 — 仅确认存在，不取值
security find-generic-password -a "<account>" -s "<service>" >/dev/null 2>&1

# 查询 — 用户明确要看值时才取值
security find-generic-password -a "<account>" -s "<service>" -w

# 删除
security delete-generic-password -a "<account>" -s "<service>"
```

不加 `-A`（allow-all-applications）——不显式放开权限面。

### 阶段 4：记忆（可选，按需触发）

只有以下情况才写记忆：用户明确说"也记到记忆里""顺便记一下""写个备注"之类，或整体请求本身就是在延续一次已建立的记忆规范讨论。默认**不**主动写。

写入前先定位当前项目的记忆目录：

```bash
memory_dir="$HOME/.claude/projects/$(pwd | sed 's/[\/.]/-/g')/memory"
[[ -d "$memory_dir" ]] || echo "NOT_FOUND"
```

- 目录不存在（不在任何项目里，或该项目从未在 Claude Code 里打开过）→ 跳过记忆这步，告诉用户"Keychain 已写入，但没找到当前项目的记忆目录，记忆部分跳过了"。
- 目录存在 → 在其中新建 `<service>.md`：

```markdown
---
name: <service>
description: <一句话，说明这是什么凭据的存放位置>
metadata:
  type: reference
---

<一句话事实：这是什么凭据>
密码存于 macOS Keychain，service: <service>，account: <account>。
取值：`security find-generic-password -a "<account>" -s "<service>" -w`

**Why:** <为什么要记这个>
**How to apply:** 需要用到该凭据时先取值，不在对话或文档中回显密钥本身。
```

再在同目录 `MEMORY.md` 里追加一行链接（若已有合适的分类小节就加进去，没有就新起一节，例如「## 密钥引用」）：

```markdown
- [<标题>](<service>.md) — 一句话钩子
```

### 阶段 5：确认

回显 service 名、account、执行的操作（新增/更新/查询到/已删除），**绝不回显密钥值本身**。

---

## 输入与输出（Input & Output）

### 输入要求

一句自然语言描述，含足够信息推断 project/env/kind；新增/更新时必须包含 account 和密钥值本身（除非 kind=api 允许省略 account）。

### 输出契约

- Keychain 里对应的 Generic Password 条目被创建/更新/删除
- 如果触发了记忆写入：一个新的 `memory/<service>.md` 文件 + 更新过的 `memory/MEMORY.md`
- 对话里的确认消息只含 service 名、account、操作结果，不含密钥值

---

## 约束（Restrictions）

### 硬边界（Hard Boundaries）

- 绝不在对话、记忆文件、任何持久化文本中回显密钥明文
- 绝不加 `-A`（allow-all-applications）
- 绝不在检测到同名 service 已存在时静默覆盖
- 绝不在没有明确要求/暗示时主动写记忆文件
- 绝不假设 Generic Password 会跨机器同步——这是已知限制，不是待修的 bug

### 失败模式

| 情形 | 处理 |
|---|---|
| 当前平台非 macOS，或找不到 `security` 命令 | 停止，说明本技能仅支持 macOS Keychain，本机不满足条件 |
| project/env/kind 无法从描述推断 | 问用户，不要瞎猜三段式——猜错了以后就找不到这条凭据 |
| account 缺失（非 api 类型） | 必须问，不用 `$USER` 顶替 |
| secret 缺失（新增/更新场景） | 必须问，绝不留空或用占位符写入 |
| 当前不在任何项目目录下，且用户要求写记忆 | 只完成 Keychain 部分，明确告知记忆部分被跳过 |
| service 已存在但用途不同 | 提示用户换 kind/env 段，而不是复用同一 service 覆盖 |

---

## 自检清单（Self-Check）

### 核心成功标准

- [ ] service 名是 `<project>-<env>-<kind>` 三段式 kebab-case
- [ ] account 是凭据本身的真实账号，不是 `$USER` 占位（api 类型除外，允许用 `token`）
- [ ] 新增/更新前探测过是否已存在同名 service
- [ ] 确认消息里没有出现密钥明文
- [ ] 记忆文件只在用户明确要求/暗示时才写，且正文没有密钥明文

### 过程质量检查

- [ ] 执行前已确认在 macOS 且 `security` 命令可用
- [ ] 查询操作若只是确认存在，没有多余带出 `-w` 取值
- [ ] 没有为了"图省事"而对无法推断的字段瞎猜
- [ ] 没有加 `-A`
- [ ] 记忆文件（若写）遵循 `type: reference` 的 frontmatter 格式，且 `MEMORY.md` 索引已同步更新

---

## 示例（Examples）

### 示例 1：新增一条数据库密码

Input: "把 Wright 开发库的密码存一下，账号是 wright_dev，密码是 Xk9#mPq2，用途是本地开发连接"

Output: 推断 `project=wright`、`env=dev`、`kind=db` → `service=wright-dev-db`；探测不存在同名条目 → 执行 `security add-generic-password -a "wright_dev" -s "wright-dev-db" -w "Xk9#mPq2" -j "本地开发连接" -U`；回显"已存入 Keychain：service=wright-dev-db，account=wright_dev"，不显示密码本身。

### 示例 2：命中已存在条目

Input: "记一下 omnireview 生产 web 后台密码，账号 nimda，密码 yyy"

Output: 拼出 `service=omnireview-prod-web`；探测发现已存在同名条目 → 提示用户"omnireview-prod-web 已经存过一条了，是要覆盖，还是这条其实是不同用途？"，等待确认后再执行。

### 示例 3：查询

Input: "staging 环境的 postgres 密码是什么来着，账号是 wright_app"

Output: 拼出 `service=wright-staging-db`（若用户提到项目名 Wright；未提及则先确认是哪个项目）；执行 `security find-generic-password -a "wright_app" -s "wright-staging-db" -w`，把取到的值直接告知用户（这是用户主动请求查看，不算"回显密钥"的禁止场景——禁止的是主动/无关场景下把密钥打印出来）。

### 示例 4：不在项目目录下，且要求写记忆

Input: "我个人博客后台密码存一下，账号 admin，密码 zzz，也记到记忆里"

Output: `project=personal`、`env=na`、`kind=web` → `service=personal-na-web`；写入 Keychain 成功；检测 `memory_dir` 不存在（当前不在任何 Claude Code 项目会话里）→ 告知用户"Keychain 已写入，但没检测到项目记忆目录，记忆部分跳过了，你可以在具体项目里让我补一条引用"。
