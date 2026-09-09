---
name: standards-import
version: 1.0.0
scope: 代码重构、含模块引用的代码变更
recommended_scope: both
---

# Rule: Import Management

## Scope

Every change that adds, removes or renames a file or class, or modifies a namespace. Applies to any language or project that uses module references such as `using` or `import`.

## Constraints

1. **Update references together with the code**: after modifying code you must immediately check and update every affected `using`, `import` or equivalent module reference.
2. **Additions**: when adding a new dependency, add the corresponding reference statement at the top of the file.
3. **Removals**: when the last reference to a class is gone, delete the now-unnecessary reference statement.
4. **Renames and moves**: when a file or class is renamed or moved, update every statement referring to it immediately.
5. **Ordering**: group references in this order, with no blank line inside a group — standard library → third-party libraries → local or in-project references.
6. **No blank lines**: a blank line must not be inserted between `using` or `import` statements.
7. **Avoid aliases**: prefer the full namespace. Use an alias only when the namespace is excessively long or when there is a name collision, and add a comment explaining why.
8. **Verify**: after updating references you must run a compile, build or lint pass to confirm correctness.

## Bad Patterns

- A class renamed, but imports in other files left pointing at the old name.
- Blank lines inserted between or within reference groups.
- `using Alias = Long.Namespace` used without need and without a comment explaining why.
- Reference order scrambled — a local reference sitting between standard library and third-party ones.

## Remediation

1. After the main code change, search the whole repository for the affected symbol and update each reference.
2. Re-sort into "standard library → third-party → local" and remove blank lines between references.
3. Run the build or static check and fix whatever the broken references caused to fail.
