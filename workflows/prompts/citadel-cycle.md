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
5. Escalation — only when a human decision is genuinely needed. Collect realm issues labeled
   `needs-human` (`gh issue list --label needs-human -R yusa-imit/<realm>`) and check what is
   already escalated (`gh issue list -R yusa-imit/citadel --label needs-human --state open`).
   For each realm issue not yet escalated, open its own citadel issue titled
   `needs-human: <realm> — <topic>`, labels `needs-human` + `from:<realm>`
   (`gh label create from:<realm> --color EDEDED --force -R yusa-imit/citadel`), body = the
   question, the options, the AI's recommendation, what happens if unanswered, and a link to the
   realm issue. One citadel issue per question, never a second one and never a periodic status
   comment on an existing one. Close a citadel escalation (with a one-line reason) as soon as its
   realm issue is closed or has lost the label. Nothing needing a human ⇒ open nothing, comment
   nothing: silence is the normal outcome of this step.
6. Discord summary: `openclaw message send --channel discord --target user:264745080709971968
   --message "[citadel] <realms with open plan PRs> | <needs-human count> | <CI red list>"`.
Never use EnterPlanMode. Never push to main of any realm repo.
