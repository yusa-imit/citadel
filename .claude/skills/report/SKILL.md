---
name: report
description: End-of-cycle report for a realm — write the counter and memory in citadel, commit with a lock, comment on GitHub, send the Discord summary. Quiet when nothing changed.
argument-hint: <realm> <mode> <summary>
---

```
R=<realm>; CITADEL=/Users/fn/codespace/citadel; REALM=$CITADEL/realms/$R
```

1. Counter: write `n` (from `/cycle` step 0.3) to `$REALM/memory/counter` — only completed cycles
   count. Update `$REALM/memory/context.md`: prepend `## Cycle <n> — <date> — <mode>` with
   Done / PRs / Next / Blockers / Open questions (≤ 15 lines); update `last_seen_at`; keep the
   file under 200 lines by folding older blocks into one "History" paragraph. Update
   `architecture.md`, `decisions.md`, `debugging.md`, `patterns.md` if something durable was
   learned. Only files under `$REALM/` may change (the guard hook enforces it).
2. Commit: `python3 $CITADEL/scripts/hooks/citadel_commit.py $R $n`. Under a lock it pushes
   only your realm's changed memory, `STATE.md` and `REALM.md` straight onto origin/main —
   whatever branch the shared checkout is on and whatever other realms left dirty — then
   fast-forwards the checkout when that is safe. Copy any `warning:` line into Blockers. A
   non-zero exit commits nothing locally: your edits stay in the working tree and your next
   cycle carries them. Never `git add`/`commit`/`stash`/`switch` in citadel yourself, and never
   commit another realm's files; the helper is the only writer.
3. Quiet mode (CONTRACT rule 8 carve-out): if the inbox found no owner actions, no PR was opened
   or merged, and the plan/CI state is identical to the previous cycle's block, skip step 4 and
   send step 5 only if no Discord line was sent today (one heartbeat per realm per day).
4. GitHub: one comment on the tracking issue (or the open plan PR): mode, done, next.
5. Discord: `openclaw message send --channel discord --target user:264745080709971968
   --message "[<realm>] cycle <n> <mode> | done: … | next: … | blockers: …"`.
