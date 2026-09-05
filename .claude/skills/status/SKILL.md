---
name: status
description: Show kingdom or realm status — git, CI, open PRs/issues, plan and milestone state, cron jobs, migration progress.
argument-hint: [realm]
---

If a realm is given: repo git log -3, dirty state, `gh run list --limit 3`, `gh pr list`,
`gh issue list`, current plan (`ls docs/plans`), open milestone issue, `STATE.md` headline,
`memory/context.md` last block. Otherwise for every realm in `citadel/zr-repos.toml`: one row
(realm · version · zig · CI · plan PR · milestone · last cycle) plus
`python3 scripts/jobs.py plan` drift and `curl -s localhost:3000/jobs` last-run status.
