---
name: rename-session
description: Suggest or change the current AI agent session title using its actual topic and the user's preferences. Use when asked to name or rename the current conversation; do not organize other sessions.
version: 0.1.0
license: MIT
---

# Name the current session

Use the current conversation to suggest or set a concise, recognizable title.
This skill covers the current session only; it does not scan, rename or organize
other sessions.

1. Follow the user's requested title or naming preferences. Otherwise, summarize
   the main subject and concrete goal in the conversation's language. Consider
   the conversation's sustained goal and a substantive change of direction;
   a minor late follow-up need not replace the main topic. A useful
   default is `project or domain: subject and goal`, but omit any part that is
   uncertain or unwanted. A working directory alone does not establish the topic.
   For recurring work, include a period only when known and useful.
2. Never place credentials or other sensitive information in the title or output.
   If the subject is unclear, say so and offer a safe, general suggestion.
3. If the user requests suggestions only, return the suggestion without changing
   the session. If the user asks to rename it, use an available supported host
   tool for the current session, subject to the host's authorization rules. Find
   a current-session rename capability among the host's available tools; do not
   assume a particular interface exists. If the current title is known and already
   matches, report it without writing. An
   explicit request to rename authorizes that action; do not add another approval
   step unless the host requires one.
4. If the host cannot identify or rename the current session, provide the proposed
   title and explain the limitation. When the host supplies a documented manual
   rename method, include it. Do not modify internal databases or session files as
   a fallback. Report a rename as successful only when the host confirms it; if
   supported, verify the resulting title. Report failures and unverified outcomes.

Do not install tools, persist preferences or create schedules as part of naming.
