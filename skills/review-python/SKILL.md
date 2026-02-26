---
name: review-python
description: "Review Python code for language and runtime conventions: type hints, exceptions, async/await, context managers, dependencies, and testability. Language-only atomic skill; output is a findings list."
tags: [eng-standards]
related_skills: [review-diff, review-codebase, review-code]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
---

# Skill: Review Python

## Purpose

Review code in **Python** for **language and runtime conventions** only. Do not define scope (diff vs codebase) or perform security/architecture analysis; those are handled by scope and cognitive skills. Emit a **findings list** in the standard format for aggregation. Focus on type hints, exception handling, async/await patterns, context managers, dependency management, and testability.

---

## Use Cases

- **Orchestrated review**: Used as the language step when [review-code](../review-code/SKILL.md) runs scope -> language -> framework -> library -> cognitive for Python projects.
- **Python-only review**: When the user wants only language/runtime conventions checked (e.g. after adding a new Python file).
- **Pre-PR Python checklist**: Ensure type hints, exception handling, and async patterns are correct.

**When to use**: When the code under review is Python and the task includes language/runtime quality. Scope (diff vs paths) is determined by the caller or user.

---

## Behavior

### Scope of this skill

- **Analyze**: Python language and runtime conventions in the **given code scope** (files or diff provided by the caller). Do not decide scope; accept the code range as input.
- **Do not**: Perform scope selection (diff vs codebase), security review, or architecture review; do not review non-Python files for Python-specific rules unless explicitly in scope.

### Review checklist (Python dimension only)

1. **Type hints**: Use `typing` module for complex types, avoid `Any` where possible, use `Optional[T]` over `T | None` for Python <3.10, proper use of `Union`, `List`, `Dict`, `Callable`, and generic type hints.
2. **Exception handling**: Catch specific exceptions, avoid bare `except:`, use `raise ... from` for exception chaining, avoid swallowing exceptions without logging, proper use of `try/finally`.
3. **Async/await**: Proper use of `async def` and `await`, avoid blocking calls in async functions, proper exception handling in async context, use of `asyncio.gather`, `asyncio.create_task` for concurrency.
4. **Context managers**: Use `with` statement for resource management, implement `__enter__`/`__exit__` or use `@contextmanager`, avoid manual open/close.
5. **Dependency management**: Pin dependencies in `requirements.txt` or `pyproject.toml`, avoid `import *`, use virtual environments, proper use of `sys.path` manipulation.
6. **Mutable defaults**: Avoid mutable default arguments (e.g. `def foo(a=[]):`), use `None` and initialize inside function.
7. **Naming conventions**: Follow PEP8 (snake_case for functions/variables, PascalCase for classes, SCREAMING_SNAKE_CASE for constants).
8. **Testability**: Avoid global state, use dependency injection, mock external services, avoid tight coupling.

### Tone and references

- **Professional and technical**: Reference specific locations (file:line). Emit findings with Location, Category, Severity, Title, Description, Suggestion.

---

## Input & Output

### Input

- **Code scope**: Files or directories (or diff) already selected by the user or by the scope skill. This skill does not decide scope; it reviews the provided Python code for language conventions only.

### Output

- Emit zero or more **findings** in the format defined in **Appendix: Output contract**.
- Category for this skill is **language-python**.

---

## Restrictions

- **Do not** perform security, architecture, or scope selection. Stay within Python language and runtime conventions.
- **Do not** give conclusions without specific locations or actionable suggestions.
- **Do not** review non-Python code for Python-specific rules unless the user explicitly includes it (e.g. embedded code snippets).

---

## Self-Check

- [ ] Was only the Python language/runtime dimension reviewed (no scope/security/architecture)?
- [ ] Are type hints, exception handling, async patterns, context managers, and testability covered where relevant?
- [ ] Is each finding emitted with Location, Category=language-python, Severity, Title, Description, and optional Suggestion?
- [ ] Are issues referenced with file:line?

---

## Examples

### Example 1: Mutable default argument

- **Input**: `def foo(items=[]):`
- **Expected**: Emit a finding for mutable default argument; suggest using `None` and initializing inside. Category = language-python.

### Example 2: Bare except

- **Input**: `except: pass`
- **Expected**: Emit a finding to catch specific exceptions; reference the bare except clause. Category = language-python.

### Example 3: Async blocking call

- **Input**: `async def fetch(): requests.get(url)` inside an async function.
- **Expected**: Emit a finding to use `aiohttp` or `httpx`; reference the blocking call. Category = language-python.

### Edge case: Mixed Python and SQL

- **Input**: Python file with embedded SQL strings for database queries.
- **Expected**: Review only Python conventions (type hints, exception handling). Do not emit SQL-injection findings; that is for review-security or review-sql.

---

## Appendix: Output contract

Each finding MUST follow the standard findings format:

| Element | Requirement |
| :--- | :--- |
| **Location** | `path/to/file.ext` (optional line or range). |
| **Category** | `language-python`. |
| **Severity** | `critical` \| `major` \| `minor` \| `suggestion`. |
| **Title** | Short one-line summary. |
| **Description** | 1-3 sentences. |
| **Suggestion** | Concrete fix or improvement (optional). |

Example:

```markdown
- **Location**: `utils/helpers.py:42`
- **Category**: language-python
- **Severity**: major
- **Title**: Mutable default argument
- **Description**: Using a list as default argument leads to shared state across calls.
- **Suggestion**: Use `def foo(items=None):` and initialize with `if items is None: items = []`.
```
