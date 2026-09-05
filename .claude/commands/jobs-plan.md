Diff the version-controlled AI workflow definitions against the running cron server.

1. `python3 scripts/jobs.py plan`
2. Explain each create/update in one line (what changes and why it matters — schedule, model, prompt)
3. If the user wants to apply: run `python3 scripts/jobs.py apply` and let it prompt; do not pass `--yes`

Focus: $ARGUMENTS
