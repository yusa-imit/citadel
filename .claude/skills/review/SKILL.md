---
name: review
description: Tiger Style code review of the current branch or a PR for a realm; reports CRITICAL/WARNING/SUGGESTION with file:line.
argument-hint: <realm> [pr-number]
---

Call `code-reviewer` (sonnet) on `git diff main...HEAD` (or `gh pr diff <n>`). Checklist:
assertions (≥ 2 per function, pre/post, positive+negative, paired), limits on loops/queues,
no recursion without a bounded stack, allocation discipline, exhaustive error switches, no
`catch unreachable` without proof, sized integers, options at call site, 70/100 limits,
`//!` headers, tests for every error variant, leak-free tests. Output CRITICAL / WARNING /
SUGGESTION with `file:line` and the fix.
