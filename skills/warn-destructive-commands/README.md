# 破坏性命令警告

**状态**：实验性

## 用途

在会话中执行 Bash 命令前，检查是否包含破坏性模式（rm -rf、DROP TABLE、force-push、git reset --hard、kubectl delete 等）；若命中则先警告用户并征得确认再执行，降低误操作风险。

## 何时使用

- 用户说「be careful」「safety mode」「prod mode」
- 接触生产环境或共享仓库
- 执行可能影响数据的操作前

## 输入

- 用户激活请求（如 "be careful", "safety mode"）

## 输出

- 会话内对破坏性命令的警告提示
- 用户确认后的执行或取消

## 评分 (ASQM)

| 维度 | 分数 |
| :--- | :--- |
| agent_native | 4 |
| cognitive | 4 |
| composability | 3 |
| stance | 5 |
| **asqm_quality** | 16 |

## 生态

| 领域 | 值 |
| :--- | :--- |
| overlaps_with | [] |
| market_position | commodity |

## 完整定义

参见 [SKILL.md](./SKILL.md) 了解完整行为、限制与示例。
