You are the citadel maintenance cycle for the Zig kingdom (cwd = citadel). Do, in order, each as a
commit to citadel (`git add <paths>`, push) or as a PR in the affected repo:
1. `/status` — one table for all realms; fix anything wrong in citadel itself (broken links, stale
   `docs/KINGDOM.md` versions vs `build.zig.zon`, `zr-repos.toml [deps]` vs real `build.zig.zon`).
2. Memory hygiene: every `realms/*/memory/*.md` under 200 lines; fold history.
3. `docs/ROADMAP.md`: tick items that GitHub shows done (merged plan PRs, closed milestones,
   tags); add blockers that appeared. Propagate releases recorded in `realms/*/STATE.md` into
   `docs/KINGDOM.md`.
4. Cron drift: `python3 scripts/jobs.py plan --check` — report drift and any `scheduled: false`
   kingdom job; never apply.
5. Open questions across realms (`gh issue list --label needs-human -R yusa-imit/<realm>`): list
   them in one comment on citadel issue "kingdom inbox" (create it if missing) so the human sees
   everything in one place.
6. Discord summary: `openclaw message send --channel discord --target user:264745080709971968
   --message "[citadel] <realms with open plan PRs> | <needs-human count> | <CI red list>"`.
Never use EnterPlanMode. Never push to main of any realm repo.
