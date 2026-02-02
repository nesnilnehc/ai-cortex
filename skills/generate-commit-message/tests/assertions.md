# Skill Verification Assertions: generate-commit-message

| 准则标号 | 描述 | 检测逻辑 |
| :--- | :--- | :--- |
| **B-01** | **格式** | 第一行是否为 `<type>(<scope>): <subject>`，且 type 属于 feat/fix/refactor/perf/test/docs/chore/build/ci/revert？ |
| **B-02** | **Subject** | 是否祈使语气、≤72 字符、结尾无句号？ |
| **B-03** | **与 diff 一致** | 是否基于实际 diff 内容，未虚构或偏离变更？ |
| **B-04** | **可直接使用** | 输出是否可直接作为 git commit 信息，无多余前缀或分析文字？ |

### 评估公式

- **Pass**: B-01 == 1 && B-02 == 1 && B-03 == 1 && B-04 == 1
- **Score**: Σ(B-n) / 4
