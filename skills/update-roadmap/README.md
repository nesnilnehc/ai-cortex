# 更新路线图（Update Roadmap）

路线图落地后的日常运维入口：改状态、挪期并计算下游影响、产出「本次变更了什么」摘要。不改变条目所在的层级。

## 用途

`define-roadmap` 管从零建，`promote-roadmap-items` 管跨层晋升降级，两者之间还有一大块日常动作——某项开始做了、某项被卡住了、某项要往后推两周——本技能负责这一块。改为「有风险」或「阻塞」时，阻塞原因与缓解方案缺一不写入；挪期必须计算下游影响并标出越过硬期限的条目。

## 何时使用

- **进度同步**：某项开始了 / 完成了，状态要跟上
- **风险上报**：某项被卡住，需要记录阻塞原因与缓解方案
- **时点调整**：依赖滑期或范围变化，需要往后推并看清波及范围
- **变更沟通前**：需要一份「本次改了什么」供同步给干系人

## 输入

- `docs/process-management/roadmap.md` 与涉及条目的 frontmatter
- 目标变更意图（状态变更 / 挪期）
- 可选：阻塞详情

## 输出

- `roadmap.md` 与条目 frontmatter 同步更新（不留单边）
- 下游影响清单 + 硬期限越界项
- 本次变更摘要（变更项 / 原因 / 影响面）

## 与 promote-roadmap-items 的分界

**改变层级的归 promote，不改变层级的归本技能。** 把一个 Now 项推迟两周是本技能；把它挪到 Next 是 promote。判断标准是层级变没变，不是日期变没变。

## 安装

统一由 AI Cortex 的 canonical 安装管理，见仓库根 [README](../../README.md#-install-and-use)。

## 相关技能

- `promote-roadmap-items` —— 边界相邻：跨层调整交接给它
- `map-item-dependencies` —— 上游：提供 `depends_on` 供下游影响计算
- `review-roadmap` —— 信号源：体检发现的状态类问题在此处理
- `define-roadmap` —— 边界相邻：结构变更（里程碑 / 容量）归它

## 完整定义

参见 [SKILL.md](./SKILL.md)。
