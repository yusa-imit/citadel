Show the state of the whole Zig kingdom.

1. For each repo in `zr-repos.toml` (path relative to citadel): branch, last commit (`git log -1 --format='%h %ad %s' --date=short`), dirty files count, ahead/behind
2. CI: `gh run list -R yusa-imit/<repo> --limit 1 --json conclusion,createdAt` for each
3. Cron: `python3 scripts/jobs.py plan` — report drift between workflows/ and the server, and `curl -s $CRON_SERVER_URL/jobs` last-run status per job
4. Foundation progress: count checked/unchecked boxes in `../<name>/docs/milestones.md` for sigil, sirocco, strata, synod
5. Output one table: repo | layer | last commit | CI | cron last run | milestone progress
