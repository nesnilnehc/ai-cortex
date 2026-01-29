# Cursor Rules Bridge Template

> [!TIP]
> 如何将 `AI Cortex` 的规则同步到 Cursor？

## 1. 推荐的做法
在你的项目根目录创建 `.cursorrules`，并写入以下内容：

```markdown
# Base on AI Cortex Framework
# Repository: https://github.com/nesnilnehc/ai-cortex

## Rules Injection
请在执行任务时始终遵守以下远程（或本地子模块）规则：
1. https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/rules/chinese-technical-standard.md
2. [添加其他需要的规则 URL...]

## Command Shortcuts
如果你支持自定义 Slash Commands，请参考以下逻辑映射：
- /readme -> 调用集成在项目中的 generate-standard-readme 技能。
```

## 2. 自动化脚本建议 (future)
未来我们将提供 `cortex sync --target cursor` 命令，自动将 `rules/*.md` 的内容汇聚并覆盖到 `.cursorrules` 中。
