---
id: DESIGN_MODELING_SPEC_V2
name: Design Modeling Schema
description: Spec defining design document fields, formats, and validation rules. Covers 10 required structural sections (MECE across what/structure/behavior/why/verify), 7 optional sections, frontmatter contract, and traceability to requirements.
version: 2.0.0
status: active
lifecycle: living
created_at: 2026-05-09
scope: |
  Defines the structural contract for design documents: required sections, optional sections,
  field formats, and frontmatter. Applies to architectural designs, component designs,
  data flow specifications, and trade-off analyses derived from validated requirements.
related:
  - ./spec-modeling.md
  - ./requirement-modeling.md
  - ./task-modeling.md
  - ../rules/design-quality.md
---

# 设计建模规范

> **数据契约**：定义设计文档的字段结构与正文骨架

---

## 1. 定位与适用范围

设计文档（design document）描述如何实现一份验证过的需求——架构、数据模型、接口、流程、权衡。它是从需求到任务列表之间的桥梁：需求回答"做什么"，任务回答"怎么拆"，设计回答"怎么实现"。

适用：

- **架构设计**：系统层、组件层、模块层架构
- **组件设计**：单一组件的接口、数据流、状态
- **变更设计**：现有系统的修改方案
- **集成设计**：跨服务 / 跨系统集成方案

不适用：

- 代码层级的具体实现（应写在代码注释或 ADR）
- 单一函数 / 类的局部设计（直接写在 PR 描述）
- 探索性原型方案（应写为 `experiments/` 或 ADR 候选）

---

## 3. 命名约定

```
<topic>-design.md
```

- `<topic>`：所设计对象的简短描述（kebab-case，如 `notification-pipeline-design.md`）
- 单一项目内若只有一份设计文档，可简化为 `design.md`
- 存放位置由项目治理决定（典型：`docs/designs/` 或 `docs/<feature>/design.md`）

---

## 4. Frontmatter 契约

```yaml
---
artifact_type: design
lifecycle: snapshot
created_at: YYYY-MM-DD
parent: <path to upstream requirement document>
status: draft | approved | superseded
# 条件字段
superseded_by: <path to new design>   # status: superseded 时必填
---
```

### 4.1 字段表

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `artifact_type` | string | 必 | 固定 `design` |
| `lifecycle` | enum | 必 | 固定 `snapshot`（设计是时点决策） |
| `created_at` | date | 必 | 设计完成日期 |
| `parent` | path | 必 | 上游 requirement 文档路径（可追溯性） |
| `status` | enum | 必 | `draft` / `approved` / `superseded`（语义见 §4.2） |
| `superseded_by` | path | 条件 | `status: superseded` 时必填，指向继任设计文档路径 |

### 4.2 状态机语义

| 状态 | 含义 | 转入条件 |
|---|---|---|
| `draft` | 草稿，尚在评审 | 设计文档首次落地 |
| `approved` | 已批准，可派生任务 | 评审通过，可作为任务列表的 `parent` |
| `superseded` | 被新设计替代 | 新设计文档已落地并接管（需填 `superseded_by`） |

---

## 5. 正文结构契约

### 5.1 必填章节（10 节）

按 **What / How-结构 / How-行为 / Why / Verify** 五维 MECE 组织。每份设计文档必须包含以下 10 节：

| # | 章节 | 维度 | 用途 | 校验 |
|---|---|---|---|---|
| 1 | 目标（Goal） | What | 陈述设计要解决的问题与成功状态 | ≤ 200 字符；不含实现细节；与上游 requirement 一致 |
| 2 | 架构（Architecture） | How-结构 | 系统 / 组件的层次、边界、外部依赖 | 含至少一种结构化表达（图 / 表 / 列表）；标注外部与内部依赖 |
| 3 | 组件（Components） | How-结构 | 关键组件及其职责 | ≥ 1 个组件；每个组件含名称、职责、依赖；职责单一可述 |
| 4 | 数据模型（Data Model） | How-结构 | 实体、字段、关系（持久化层） | ≥ 1 个实体；每个实体含字段、类型、约束、关系；关键索引标注 |
| 5 | 接口契约（Interfaces / APIs） | How-结构 | 对外暴露的接口（REST / gRPC / 事件 schema） | 每个接口含路径 / 方法 / 入参 / 出参 / 错误码；事件含 topic + payload schema |
| 6 | 数据流与业务流程（Data Flow & Workflow） | How-行为 | 数据如何在组件间流动，业务状态如何演化 | 关键路径数据流必须标注；含状态机或时序图（涉及多步流程时） |
| 7 | 错误处理策略（Error Handling） | How-行为 | 关键失败路径与处理方法 | ≥ 2 条关键失败路径；每条含：失败条件、检测方式、恢复策略 |
| 8 | 测试策略（Test Strategy） | Verify | 声明验证方法（**不写测试代码**） | 含测试层次（单元 / 集成 / 端到端）；含验收方式（自动化 / 人工） |
| 9 | 权衡分析（Trade-offs） | Why | 考虑过的替代方案与选择理由 | ≥ 2 种替代方案；每种含优点 / 缺点 / 是否选用 + 理由 |
| 10 | 验收标准（Acceptance Criteria） | Verify | 设计完成的可验证条件 | ≥ 3 条；每条可追溯至上游 requirement 的某条 acceptance |

### 5.2 可选章节

按场景需要添加。每项有明确触发条件——不满足则不写：

| 章节 | 触发场景 |
|---|---|
| 范围定义（Scope） | 设计边界容易被误读（多系统集成、跨团队） |
| 部署与运维（Deployment & Operations） | 含部署变更、扩缩容策略、配置管理 |
| 横切关注点（Cross-cutting Concerns） | 安全 / 性能 / 可观测性有专门设计 |
| UI 设计（UI Design） | 前端项目，含交互流程、组件层次、状态管理 |
| 作业调度（Scheduling） | 含定时任务 / 后台 job / 队列消费者 |
| 风险与假设（Risks & Assumptions） | 设计依赖未验证的关键假设或承担明显技术风险 |
| 关联文档（References） | 引用 ADR / 外部规范 / 上游设计 |

---

## 6. 反模式

- ❌ 含代码或脚手架（设计不写实现，实现在代码层）
- ❌ 单一方案不做权衡（缺 §9 权衡分析）
- ❌ 无验收标准（无法追溯到需求）
- ❌ 测试策略写测试代码而非验证方法
- ❌ 无 `parent` frontmatter（孤立设计，无可追溯性）
- ❌ `superseded` 状态未填 `superseded_by`
- ❌ 权衡分析只列被选方案的优点（必须含被拒方案的缺点）
- ❌ 组件节用大段散文描述而非结构化字段
- ❌ 数据模型只列实体名不含字段 / 类型 / 关系（无法据此实施）
- ❌ 接口契约只写"有一个 API"不列方法 / 入参 / 出参（无法据此对接）

---

## 7. 示例

### 7.1 紧凑骨架示例：用户认证模块设计

每节用 1-3 句展示骨架，实际设计文档每节应展开为完整内容。

````markdown
---
artifact_type: design
lifecycle: snapshot
created_at: 2026-05-15
parent: ../requirements/AUTH-REQ-001.md
status: approved
---

# 设计：用户认证模块

## 目标

为 Web / 移动客户端提供基于 JWT 的统一认证；支持邮箱密码登录、第三方 OAuth、会话续期；预期 QPS 峰值 500。

## 架构

```
[Client] → [API Gateway] → [Auth Service] → [User Store (PostgreSQL)]
                                ↓                    ↓
                          [Token Issuer]      [Audit Log]
```

外部依赖：OAuth Provider（Google / GitHub）、SMTP（邮件验证码）
内部依赖：通用 Crypto Lib、Metrics Collector

## 组件

- **Auth Service**：登录 / 注册 / 验证主流程。职责：凭证校验、token 签发。依赖：User Store、Token Issuer。
- **Token Issuer**：签发与验证 JWT。职责：密钥管理、claim 注入、过期控制。
- **OAuth Adapter**：对接第三方 provider。职责：authorization code 兑换、用户信息归一化。

## 数据模型

```
User
  id: UUID PK
  email: string UNIQUE NOT NULL (index)
  password_hash: string NULL (OAuth 用户为空)
  oauth_provider: enum NULL (google/github)
  oauth_subject_id: string NULL
  created_at: timestamp NOT NULL
  email_verified_at: timestamp NULL

Session
  id: UUID PK
  user_id: UUID FK -> User.id (cascade delete, index)
  refresh_token_hash: string NOT NULL (index)
  expires_at: timestamp NOT NULL
  revoked_at: timestamp NULL
```

约束：(oauth_provider, oauth_subject_id) UNIQUE；password_hash 与 oauth_provider 至少存在其一。

## 接口契约

- `POST /auth/login` — body: `{email, password}` → 200 `{access_token, refresh_token, expires_in}` / 401 `INVALID_CREDENTIALS` / 423 `ACCOUNT_LOCKED`
- `POST /auth/oauth/{provider}/callback` — body: `{code, state}` → 200 同上 / 400 `INVALID_STATE`
- `POST /auth/refresh` — body: `{refresh_token}` → 200 `{access_token, expires_in}` / 401 `TOKEN_EXPIRED`
- `POST /auth/logout` — header: `Authorization: Bearer <token>` → 204
- 事件：`USER_LOGGED_IN` / `LOGIN_FAILED` / `SESSION_REVOKED`（schema 见 universal-notification spec）

## 数据流与业务流程

登录主流程：
```
Client → POST /auth/login
  → Auth Service: bcrypt.compare(password, password_hash)
  → 成功：Token Issuer 签发 access (15min) + refresh (30d)
        → 写入 Session 表
        → 发 USER_LOGGED_IN 事件
        → 返回 token pair
  → 失败：写入 Audit Log，连续 5 次锁账户 15 分钟
```

会话状态机：`active` → (logout) → `revoked` / `active` → (expires_at 过) → `expired`

## 错误处理策略

- **密码错误**：返回 401 INVALID_CREDENTIALS；不区分"用户不存在"与"密码错误"（防止用户枚举攻击）；连续失败 5 次 → 423 ACCOUNT_LOCKED
- **OAuth provider 不可用**：返回 503 OAUTH_UPSTREAM_UNAVAILABLE；客户端提示用户改用邮箱密码登录
- **数据库写入失败**：5xx 不返回 token；记录 ERROR 日志触发告警

## 测试策略

- 单元测试：密码哈希、JWT 签发与验证、OAuth state 校验
- 集成测试：完整登录 / 刷新 / 登出链路（含 mock OAuth provider）
- 安全测试：用户枚举攻击、暴力破解、token 重放（自动化扫描 + 季度人工 review）
- 验证方式：CI 自动跑单元 + 集成；安全测试半年一次

## 权衡分析

- **方案 A：JWT + Refresh Token**（选用）。优点：无状态 access token 易扩展、refresh 可吊销。缺点：实现复杂，密钥轮转需谨慎设计。
- **方案 B：Session Cookie**（拒）。优点：实现简单、原生支持登出。缺点：跨域 / 跨端不友好；移动端需要额外适配。
- **方案 C：仅 access token 无 refresh**（拒）。优点：最简单。缺点：用户需频繁登录（短过期）或安全弱（长过期）。

## 验收标准

- [ ] 邮箱密码登录 p95 延迟 ≤ 300ms（对应 AUTH-REQ-001 §验收 1）
- [ ] 支持 Google / GitHub OAuth 登录（对应 §验收 2）
- [ ] 连续 5 次失败锁账户 15 分钟（对应 §验收 4 安全要求）
- [ ] 安全扫描无 OWASP Top 10 高危项（对应 §验收 5）
````

---

## 8. 与其他资产关系

- **配套 rule**：[rules/design-quality.md](../rules/design-quality.md)——设计文档质量评审清单（5 维：完整性 / 可执行性 / 清晰性 / 合理性 / 可追溯性）
- **上游 spec**：[requirement-modeling.md](./requirement-modeling.md)——设计的 `parent` 必须指向已批准的 requirement
- **下游 spec**：[task-modeling.md](./task-modeling.md)——任务列表的 `parent` 应指向 `approved` 状态的设计文档
- **相关行业标准**：IEEE 1016（Software Design Description）、C4 Model、arc42 模板、Google Design Doc 实践
- **递归基础**：本 spec 自身遵循 [spec-modeling.md](./spec-modeling.md) v2.0.0 的 8 节骨架；跳过 §2 心智模型（设计的"必答维度"已落在 §5.1 的 10 节 MECE 结构中，不需要额外抽象 N 问框架）
