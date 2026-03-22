# 场景枚举参考材料

**用途**：为 intent-routing 的意图覆盖提供校验依据，支撑软件交付与项目治理领域。

**使用方式**：场景设计时从下列标准/框架提取过程/活动，映射为场景；新增场景需可追溯至某一来源。

---

## 目录

1. [国际标准](#1-国际标准)
2. [过程能力与评估](#2-过程能力与评估)
3. [质量与测试](#3-质量与测试)
4. [项目管理](#4-项目管理)
5. [敏捷与交付](#5-敏捷与交付)
6. [知识体系](#6-知识体系)
7. [运维与服务](#7-运维与服务)
8. [方法与模型](#8-方法与模型)
9. [经典著作](#9-经典著作)
10. [奠基性论文](#10-奠基性论文)
11. [映射与获取](#11-映射与获取)

---

## 1. 国际标准

### 1.1 ISO/IEC/IEEE 12207:2017 — 软件生命周期过程

- **出处**：<https://www.iso.org/standard/63712.html>、<https://standards.ieee.org/ieee/12207/5672>
- **说明**：软件生命周期过程的国际标准；与 15288 对齐，共 30 个过程。

**技术过程（14 个）**：Business/mission analysis → Stakeholder requirements → System/software requirements → Architecture definition → Design definition → System analysis → Implementation → Integration → Verification → Transition → Validation → Operation → Maintenance → Disposal

### 1.2 ISO/IEC/IEEE 15288:2023 — 系统生命周期过程

- **出处**：<https://www.iso.org/standard/81702.html>
- **说明**：与 12207 统一模型；系统级生命周期。

### 1.3 ISO/IEC/IEEE 29148:2018 — 需求工程

- **出处**：IEEE Xplore
- **说明**：定义需求工程过程与制品；何谓良好需求、属性与特征。

### 1.4 ISO/IEC/IEEE 15289:2019 — 生命周期信息制品

- **出处**：<https://www.iso.org/standard/74909.html>
- **说明**：12207/15288 过程与信息制品的映射；文档类型与内容要求。

---

## 2. 过程能力与评估

### 2.1 CMMI 2.0 — Practice Areas

- **出处**：<https://cmmiinstitute.com/cmmi>
- **说明**：25 个实践域；质量、工程、服务、供应商、计划、韧性、支持、治理、绩效改进。

### 2.2 ISO/IEC 15504 (SPICE) — 过程评估

- **出处**：维基百科
- **说明**：已被 ISO/IEC 33000 系列替代；过程能力评估的奠基标准。

### 2.3 ISO/IEC 33000 — 过程评估框架

- **出处**：<https://www.iso.org/standard/54176.html> 等
- **说明**：33002（评估要求）、33003（测量框架）、33004（参考模型）、33010（评估指南）。

---

## 3. 质量与测试

### 3.1 ISO/IEC 25010 — 产品质量模型 (SQuaRE)

- **出处**：<https://www.iso.org/standard/78176.html>
- **说明**：9 个质量特征；功能性、性能、兼容性、易用性、可靠性、安全、可维护性、灵活性、安全。

### 3.2 ISO/IEC/IEEE 29119 — 软件测试

- **出处**：<https://www.softwaretestingstandard.org/>
- **说明**：Part 1 概念、Part 2 测试过程、Part 3 文档、Part 4 技术；组织/项目/动态测试层级。

### 3.3 IEEE 730 — 软件质量保证过程

- **出处**：IEEE Xplore
- **说明**：SQA 计划与过程要求；与 12207 协调。（730-2014 已 Inactive；P730-2026 在编）

### 3.4 IEEE 828 — 配置管理

- **出处**：IEEE
- **说明**：配置项识别、变更控制、状态报告；P828 在修订中。

---

## 4. 项目管理

### 4.1 PMBOK Guide — 项目管理知识体系

- **出处**：PMI <https://www.pmi.org/pmbok-guide-standards>
- **说明**：5 个过程组（启动、规划、执行、监控、收尾）；49 个过程；知识领域。

---

## 5. 敏捷与交付

### 5.1 Scrum Guide — 事件与工件

- **出处**：<https://scrumguides.org/>
- **说明**：Sprint, Sprint Planning, Daily Scrum, Sprint Review, Sprint Retrospective；Product/Sprint Backlog, Increment。

### 5.2 DevOps 价值流

- **说明**：Plan → Code → Build → Test → Release → Deploy → Operate → Monitor；闭环。

### 5.3 Lean Software Development — Poppendieck

- **说明**：7 原则（整体优化、内建完整性、赋能团队、快速交付、延迟决策、放大学习、消除浪费）；22 个思考工具。

### 5.4 SAFe — 规模化敏捷框架

- **出处**：<https://www.scaledagileframework.com/>
- **说明**：Lean Portfolio Management、Team and Technical Agility、ART、PI Planning；5 大核心学科。

### 5.5 Kanban — 看板软件开发

- **说明**：可视化工作流、WIP 限制、流动管理、反馈环；持续流、无 Sprint 边界。

---

## 6. 知识体系

### 6.1 SWEBOK 4.0 — 软件工程知识域

- **出处**：<https://www.computer.org/education/bodies-of-knowledge/software-engineering>
- **说明**：18 个知识域；需求、设计、构造、测试、维护、配置管理、架构、运维、安全等。

---

## 7. 运维与服务

### 7.1 ITIL 4 — 服务管理

- **出处**：<https://www.axelos.com/business-solutions/itil>
- **说明**：34 个管理实践；Service Value Chain（Plan, Engage, Design and Transition, Obtain/Build, Deliver and Support）；事件、问题、变更、监控。

---

## 8. 方法与模型

### 8.1 V-Model — 验证与确认

- **说明**：左半需求/设计分解，右半集成/验证；7 阶段：需求分析、系统设计、架构设计、实现与单元测试、集成测试、系统测试、验收测试。

### 8.2 Spiral Model — Boehm 螺旋模型

- **出处**：Boehm 1986/1988 论文
- **说明**：风险驱动；每圈 4 扇区：Planning、Objective Setting、Development and Validation、Risk Assessment；过程模型生成器。

### 8.3 ATAM — 架构权衡分析方法

- **出处**：SEI/CMU
- **说明**：架构评估；质量属性场景；9 步骤、两阶段；识别权衡与风险。

### 8.4 ADR — 架构决策记录

- **出处**：adr.github.io、Cognitect 2011
- **说明**：记录架构决策的上下文、决策、后果；Markdown 格式；支持可追溯性。

---

## 9. 经典著作

### 9.1 综合教材

| 著作 | 作者 | 与场景 |
|------|------|--------|
| Software Engineering: A Practitioner's Approach（软件工程：实践者的研究方法） | Pressman | Process、Modeling、Quality、Project Management |
| Software Engineering | Sommerville | 过程模型、需求、敏捷、演化 |
| Software Engineering: Theory and Practice | Pfleeger, Atlee | 过程、风险、设计、架构 |

### 9.2 项目管理与团队

| 著作 | 作者 |
|------|------|
| The Mythical Man-Month | Brooks |
| Peopleware | DeMarco, Lister |

### 9.3 需求与设计

| 著作 | 作者 |
|------|------|
| Writing Effective Use Cases | Cockburn |
| Software Requirements | Wiegers, Beatty |
| Software Architecture in Practice | Bass, Clements, Kazman |
| Design Patterns | Gamma et al. |
| Domain-Driven Design | Evans |

### 9.4 实现与质量

| 著作 | 作者 |
|------|------|
| Code Complete | McConnell |
| The Pragmatic Programmer | Hunt, Thomas |
| Refactoring | Fowler |
| Clean Code | Martin |

### 9.5 生命周期与交付

| 著作 | 作者 |
|------|------|
| Rapid Development | McConnell |
| Extreme Programming Explained | Beck |
| Lean Software Development | Poppendieck |
| Continuous Delivery | Humble, Farley |
| Accelerate | Forsgren, Humble, Kim |
| Team Topologies | Skelton, Pais |

---

## 10. 奠基性论文

| 论文 | 作者 | 年份 | 要点 |
|------|------|------|------|
| No Silver Bullet — Essence and Accident in Software Engineering | Brooks | 1986 | 本质 vs 次要复杂度；快速原型、增量开发、概念设计 |
| A Spiral Model of Software Development and Enhancement | Boehm | 1986/1988 | 风险驱动过程模型 |
| Documenting Architecture Decisions | Michael Nygard (Cognitect) | 2011 | ADR 概念提出 |

---

## 11. 映射与获取

### 11.1 AI Cortex 维度 → 来源

| 维度 | 可参考来源 |
|------|------------|
| 软件交付 | 12207/15288 技术过程、DevOps、V-Model、SWEBOK |
| 项目治理 | 12207 组织与技术管理、CMMI、Scrum、PMBOK、SAFe |
| 质量与测试 | ISO 25010、29119、IEEE 730 |
| 运维/监控 | DevOps Operate/Monitor、ITIL 4、SWEBOK operations |

### 11.2 获取途径

| 类型 | 途径 |
|------|------|
| ISO/IEEE 标准 | ISO Store、IEEE Xplore（付费） |
| CMMI、ITIL | 各机构官网（付费） |
| Scrum Guide | scrumguides.org（免费） |
| 经典著作 | O'Reilly、Microsoft Press、Addison-Wesley、Pearson |
| 论文 | IEEE Xplore、ACM DL、arXiv |

---

*本文档为参考汇编，非标准正文；具体条款以各标准正式出版物为准。*
