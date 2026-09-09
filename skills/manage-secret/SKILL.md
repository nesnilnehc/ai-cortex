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

# Skill: Manage Secret

## Purpose

Secrets and credentials this machine has to remember long term (server SSH, databases, website logins, API keys, certificate passphrases) all go into the macOS Keychain, instead of scattering across chat logs, notes, and plaintext files. Names follow one fixed three-part convention, so the same credential can be located across projects and environments; where it helps, add a memory pointer that holds no secret itself, so a later conversation knows straight away "where this thing lives".

A personal, single-machine setup needs no Docker Vault and no team-grade password manager — the Keychain's Generic Password class was designed for exactly this scale.

## Core Objective

**Primary goal**: given one natural-language request, settle on a unique Keychain service name, run the matching `security` command, and at no point echo the secret in cleartext into the conversation.

**Success criteria** (all of them must hold):

1. ✅ **Naming compliant**: the service name follows the three-part `<project>-<env>-<kind>` kebab-case form
2. ✅ **Real account**: account is the credential's own login name, not the local username as a placeholder
3. ✅ **No silent overwrite**: the service was probed for existence before writing, and the user was asked when one already existed
4. ✅ **No leak**: neither the confirmation message nor the body of the memory file carries the secret in cleartext
5. ✅ **Memory is optional**: the memory file is written only when the user asks for it or clearly implies it, not on the skill's own initiative

---

## Scope Boundaries

**What it does**:

- Create or update one Keychain Generic Password (`security add-generic-password`)
- Look up a stored credential (`security find-generic-password`), only to confirm it exists or to let the user fetch the value themselves; it does not print the secret into the conversation unprompted
- Delete one credential (`security delete-generic-password`)
- On the user's request, add a `type: reference` memory under the current project's memory directory, recording only the service name, the account, and the retrieval command

**What it does not do**:

- It leaves team-shared secret vaults and CI/CD variable injection alone — that is the job of 1Password/Vault/GitLab CI Variables
- It assumes no cross-machine sync — a Generic Password lives only in this machine's `login.keychain-db`
- It does not generate passwords — for a random password, reach for a tool such as `openssl rand -base64 24`; this skill only stores and retrieves
- It does not write a memory file without an explicit request or hint — that avoids piling memory files into the project every time a secret is stored

---

## Use Cases

- "Save this database password, the account is wright_dev, the password is xxx, it's for the Wright project's dev database"
- "Record a secret: omnireview production web admin, account nimda, password xxx"
- "What's the postgres password for the staging environment again"
- "Delete the old GitHub token from the keychain, the service is something like shared-na-api"
- "Here's the login for my personal blog admin, save it for me, and record it in the current project's memory while you're at it" (also triggers the memory write)

---

## Behavior

### Stage 0: classify — identify the operation

Confirm the execution environment first: the current platform is not macOS, or this machine has no `security` command (`command -v security` prints nothing) → stop, and tell the user this skill supports the macOS Keychain only and this machine does not meet the condition (on Linux, `secret-tool` / `pass` do the job, but they are outside this skill's scope).

Decide whether the user wants a **create/update**, a **look-up**, or a **delete**. All three operations share the same field-inference logic (Stage 1); only the `security` subcommand finally executed differs.

### Stage 1: extract — infer project / env / kind / account

Infer from the table below; do not ask about what can be inferred, and follow up only on fields that are genuinely missing and cannot be inferred:

| Field | Inference cues | Default/fallback |
|---|---|---|
| project | The repository/project name the user names (converted to kebab-case); "personal" mentioned → `personal`; "shared by the team"/"used by several projects" → `shared`; "this project" mentioned and the current cwd sits inside a repository → use that repository's directory name | Nothing can be determined → ask the user |
| env | "production"/"live"/prod → `prod`; "development" → `dev`; "testing"/QA → `test`; "pre-release"/staging → `staging`; "local" → `local`; the credential has no notion of environment at all (a personal website account, say) → `na` | Cannot be determined → ask the user |
| kind | "database"/db/postgres/mysql/redis/mongo → `db`; "server"/SSH/host → `ssh`; "website"/"web page"/login → `web`; API/Token/secret/key → `api`; "certificate"/private-key passphrase → `cert` | Cannot be determined → ask the user |
| account | The real login name/username given in the user's description | kind=api and the user gave no account → default to `token`; any other kind missing an account → **must be asked**, since a wrong guess leaves it unfindable later |
| secret (needed for create/update only) | The value the user states explicitly | Missing → **must be asked**; never invent one and never write it empty |
| purpose (optional) | The one-line note the user gives, or a short description synthesized from context | Missing → no forced follow-up |

Assemble `service = <project>-<env>-<kind>`, all lowercase kebab-case.

### Stage 2: conflict detection (create/update only)

Probe before writing:

```bash
security find-generic-password -a "<account>" -s "<service>" >/dev/null 2>&1
```

Exit code 0 means an entry of that name already exists. Do not silently overwrite it — tell the user "there is already a credential under this service name; do you want to overwrite it, or is this actually a different use that should get a different kind/env segment", and wait for the user's confirmation before continuing.

### Stage 3: execute

```bash
# Create/update (omit -j when purpose is missing; do not pass an empty string as a placeholder)
security add-generic-password -a "<account>" -s "<service>" -w "<secret>" [-j "<purpose>"] -U

# Look up — confirm existence only, do not fetch the value
security find-generic-password -a "<account>" -s "<service>" >/dev/null 2>&1

# Look up — fetch the value only when the user explicitly asks to see it
security find-generic-password -a "<account>" -s "<service>" -w

# Delete
security delete-generic-password -a "<account>" -s "<service>"
```

Do not add `-A` (allow-all-applications) — do not widen the permission surface explicitly.

### Stage 4: memory (optional, triggered on demand)

Write memory only in these cases: the user explicitly says something like "record it in memory too", "note it down while you're at it", or "leave a remark"; or the request itself continues an established discussion about memory conventions. By default, **do not** write it unprompted.

Locate the current project's memory directory before writing:

```bash
memory_dir="$HOME/.claude/projects/$(pwd | sed 's/[\/.]/-/g')/memory"
[[ -d "$memory_dir" ]] || echo "NOT_FOUND"
```

- The directory does not exist (not inside any project, or the project has never been opened in Claude Code) → skip the memory step and tell the user "the Keychain entry is written, but no memory directory was found for the current project, so the memory part was skipped".
- The directory exists → create `<service>.md` inside it:

```markdown
---
name: <service>
description: <one line saying where this credential is stored>
metadata:
  type: reference
---

<one-line fact: what this credential is>
The password lives in the macOS Keychain, service: <service>, account: <account>.
Retrieve: `security find-generic-password -a "<account>" -s "<service>" -w`

**Why:** <why this is worth recording>
**How to apply:** fetch the value when the credential is needed; do not echo the secret itself into a conversation or a document.
```

Then append one link line to `MEMORY.md` in the same directory (add it to a suitable existing subsection, or start a new one, such as "## Secret references"):

```markdown
- [<title>](<service>.md) — one-line hook
```

### Stage 5: confirm

Echo back the service name, the account, and the operation performed (created/updated/found/deleted), and **never echo the secret value itself**.

---

## Input & Output

### Input requirements

One natural-language description, carrying enough information to infer project/env/kind; a create/update must include the account and the secret value itself (unless kind=api, where the account may be omitted).

### Output contract

- The matching Generic Password entry in the Keychain is created/updated/deleted
- If the memory write was triggered: one new `memory/<service>.md` file plus an updated `memory/MEMORY.md`
- The confirmation message in the conversation carries only the service name, the account, and the outcome — not the secret value

---

## Restrictions

### Hard Boundaries

- Never echo a cleartext secret into the conversation, a memory file, or any persisted text
- Never add `-A` (allow-all-applications)
- Never silently overwrite once a service of the same name is detected
- Never write a memory file unprompted, absent an explicit request or hint
- Never assume a Generic Password syncs across machines — that is a known limitation, not a bug awaiting a fix

### Failure modes

| Situation | Handling |
|---|---|
| The current platform is not macOS, or the `security` command cannot be found | Stop, and explain that this skill supports the macOS Keychain only and this machine does not meet the condition |
| project/env/kind cannot be inferred from the description | Ask the user; do not guess wildly at the three parts — a wrong guess leaves the credential unfindable |
| account missing (non-api kinds) | It must be asked; do not stand `$USER` in for it |
| secret missing (create/update) | It must be asked; never write it empty or with a placeholder |
| Not inside any project directory, and the user asked for a memory write | Complete the Keychain part only, and state plainly that the memory part was skipped |
| The service exists but serves a different use | Prompt the user to change the kind/env segment, rather than reusing and overwriting the same service |

---

## Self-Check

### Core success criteria

- [ ] The service name is the three-part `<project>-<env>-<kind>` kebab-case form
- [ ] account is the credential's own real account, not a `$USER` placeholder (api kinds excepted, where `token` is allowed)
- [ ] Before the create/update, the existence of a service of the same name was probed
- [ ] No cleartext secret appears in the confirmation message
- [ ] The memory file is written only on an explicit request or hint from the user, and its body holds no cleartext secret

### Process quality checks

- [ ] macOS and an available `security` command were confirmed before execution
- [ ] A look-up meant only to confirm existence does not needlessly pull the value with `-w`
- [ ] No field that could not be inferred was guessed at "to save trouble"
- [ ] `-A` was not added
- [ ] The memory file (where written) follows the `type: reference` frontmatter format, and the `MEMORY.md` index was updated alongside it

---

## Examples

### Example 1: storing a database password

Input: "Save the password for the Wright dev database, the account is wright_dev, the password is Xk9#mPq2, it's for local development connections"

Output: infer `project=wright`, `env=dev`, `kind=db` → `service=wright-dev-db`; the probe finds no entry of the same name → run `security add-generic-password -a "wright_dev" -s "wright-dev-db" -w "Xk9#mPq2" -j "local development connection" -U`; echo back "stored in the Keychain: service=wright-dev-db, account=wright_dev", without showing the password itself.

### Example 2: hitting an existing entry

Input: "Note down the omnireview production web admin password, account nimda, password yyy"

Output: assemble `service=omnireview-prod-web`; the probe finds an entry of the same name → prompt the user "omnireview-prod-web already holds an entry; overwrite it, or is this one actually a different use?", and wait for confirmation before executing.

### Example 3: a look-up

Input: "What's the postgres password for the staging environment again, the account is wright_app"

Output: assemble `service=wright-staging-db` (given that the user named the project Wright; if not, confirm which project first); run `security find-generic-password -a "wright_app" -s "wright-staging-db" -w` and give the retrieved value straight to the user (the user asked to see it, so this is not the forbidden "echo the secret" case — what is forbidden is printing the secret unprompted or in an unrelated context).

### Example 4: not in a project directory, with a memory write requested

Input: "Save my personal blog admin password, account admin, password zzz, and record it in memory too"

Output: `project=personal`, `env=na`, `kind=web` → `service=personal-na-web`; the Keychain write succeeds; the check finds `memory_dir` absent (this is not a Claude Code project session) → tell the user "the Keychain entry is written, but no project memory directory was detected, so the memory part was skipped; you can ask me to add a reference from inside a specific project".
