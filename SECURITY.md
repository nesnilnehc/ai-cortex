# Security Policy

## What this repository is

AI Cortex is a library of Markdown assets — skills, specs, protocols and rules. It is not a running service. The attack surface is two things:

1. **`bin/cortex`** — a POSIX shell installer that creates and removes symlinks under the user's home directory.
2. **Skill content** — skills instruct AI agents to take actions. Wording that leads an agent to perform destructive or out-of-scope operations is a security problem, not a quality problem.

## Supported versions

This is a rolling-release repository. Security fixes are provided for the latest commit on the default branch, `main`.

## Reporting a vulnerability

**Do not report security issues in a public issue.**

Use GitHub's private channel: **Security → Report a vulnerability** on this repository. If that is unavailable, contact the maintainer privately through the links on [@nesnilnehc](https://github.com/nesnilnehc)'s GitHub profile.

Please include what you can:

- The affected file or skill name
- Trigger conditions and reproduction steps
- Your assessment of the impact
- Any known mitigation or workaround

## Response timeline

- **Within 72 hours** — acknowledgement of receipt
- **Within 7 days** — initial assessment and a remediation plan
- On release of a fix — noted in `CHANGELOG.md`, with credit to the reporter if they consent

## In scope

- Path traversal, symlink attacks or unquoted variable expansion in `bin/cortex` leading to unintended deletion
- Skill content that induces an agent to leak credentials, run destructive commands without confirmation, or bypass a user approval gate
- Malicious content in a vendored, externally derived skill

## Out of scope

- A skill giving poor-quality advice — open a normal issue
- Documentation typos or broken links — open a normal issue, or send a PR
- Vulnerabilities in third-party AI agents themselves — report those upstream
