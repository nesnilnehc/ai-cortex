# Commit message template (Conventional Commits)

```text
<type>(<scope>): <summary>

<What changed.>
<Why it changed.>
```

## Types

- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `docs`: Documentation only changes
- `test`: Adding or updating tests
- `chore`: Changes to build process or auxiliary tools
- `perf`: Performance improvement
- `style`: Code style changes (formatting, missing semicolons, etc.)

## Notes

- Keep the summary imperative and specific ("Add", "Fix", "Remove", "Refactor")
- Avoid implementation minutiae; focus on behavior and intent
- If breaking: use `!` in header and/or add `BREAKING CHANGE:` footer
- Summary should be ≤72 characters for readability in git logs

## Examples

```text
feat(auth): add OAuth2 authentication support

Implement OAuth2 flow for third-party authentication.
Supports Google and GitHub providers initially.
```

```text
fix(api): prevent race condition in user creation

Add transaction lock to ensure atomic user record creation
and avoid duplicate entries when concurrent requests occur.
```

```text
refactor(utils)!: change date format to ISO 8601

BREAKING CHANGE: formatDate() now returns ISO 8601 strings
instead of locale-specific format. Update all callers to
handle the new format.
```
