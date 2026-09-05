---
name: report
description: End-of-cycle report for a realm — update citadel realm memory, commit citadel, comment on GitHub, send the Discord summary.
argument-hint: <realm> <mode> <summary>
---

1. `citadel/realms/<realm>/memory/context.md`: prepend a block
   `## Cycle <n> — <date> — <mode>` with Done / PRs / Next / Blockers / Open questions
   (≤ 15 lines). Keep the file under 200 lines: fold older blocks into one "History" paragraph.
   Update `architecture.md`, `decisions.md`, `debugging.md`, `patterns.md` if anything durable
   was learned.
2. `cd /Users/fn/codespace/citadel && git add realms/<realm> && git commit -m
   "chore(<realm>): cycle <n> memory" && git pull --rebase && git push`.
3. GitHub: one comment on the tracking issue (or the open plan PR): mode, done, next.
4. Discord: `openclaw message send --channel discord --target user:264745080709971968
   --message "[<realm>] cycle <n> <mode> | done: … | next: … | blockers: …"`.
