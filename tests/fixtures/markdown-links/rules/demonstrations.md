# Rule that shows the forbidden forms

Inline, as an example: `[some-skill](../skills/some-skill/SKILL.md)` — text, not a link.

In a fenced block:

```markdown
[some-skill](../skills/some-skill/SKILL.md)
[gone](./missing.md)
```

Inside a list item, where the fence carries the item's indentation:

1. Step one:

   ```markdown
   [some-skill](../skills/some-skill/SKILL.md)
   [gone](./missing.md)
   ```

2. Step two.

A longer fence holding a shorter one:

````markdown
```text
[some-skill](../skills/some-skill/SKILL.md)
```
````
