# synod — debugging

_(migrated from the repo's former .claude/memory; keep under 200 lines)_

Format: `## <symptom>` / **Cause** / **Fix** / **How to detect next time**

Empty — the old `.claude/memory/debugging.md` had no entries (no real code existed yet to
produce tricky bugs). Add entries here as they're resolved during Phase 1 onward.

One tooling gotcha surfaced by the Zig 0.16 migration probe, worth knowing before that plan
lands: `zig build test` on 0.16 can report all tests passing even when `main()` itself would
fail to compile-and-run, because `zig test` never calls `main` and Zig's lazy top-level
analysis skips code that only `main` reaches. Verify 0.16 readiness with `zig build` (builds
the real executable) or `zig test src/main.zig`, not `zig build test` alone.

## `git commit` blocked by the kingdom guard on a hygiene-cleanup commit message

**Cause**: `guard_bash.py`'s realm-write check tokenizes the flat shell command and treats any
whitespace-free token containing `/` or `.` as a candidate path, then blocks if it resolves
under the realm root to `CLAUDE.md` or `.claude/`. A commit message *prose* token like
`CLAUDE.md/.claude/` (describing what an earlier PR removed) matches this even though nothing
is actually being written there — it's a text match, not a semantic one.

**Fix**: rephrase the commit message to avoid a bare `CLAUDE.md`/`.claude` pair joined by `/`
with no space (e.g. "the old AI-config files" instead of naming the literal paths back to back).

**How to detect next time**: `PreToolUse:Bash hook error: ... BLOCKED by kingdom guard: realm
repos carry no AI files` on a `git commit` (not a file write) — the command itself wrote
nothing; the message text tripped the matcher.

## `memory/counter` silently under-counts a completed cycle

**Cause**: cycle 9's `/report` step updated `context.md` (prepended the cycle block, moved the
watermark) but never wrote `memory/counter` — it stayed at 8 even though PR #12 merged and item
9 was ticked, a fully completed cycle. Root cause not confirmed (report-step partial failure or
an ordering slip), but the effect is durable: the next session's preflight computes `n =
counter + 1`, silently redoing a cycle number and drifting the every-5th-cycle STABILIZATION
cadence by one forever unless caught.

**Fix**: before trusting `n = counter + 1` in preflight, cross-check `context.md`'s most recent
`## Cycle <n>` header and the realm's merged-PR/issue history for that cycle. If the counter is
behind what `context.md`/GitHub show as the last fully-completed cycle, treat the *next* integer
after the true last-completed cycle as `n` (not `counter + 1`), and write the corrected value at
this cycle's report step so the drift self-heals rather than persisting.

**How to detect next time**: `context.md`'s top block cycle number is `>= counter + 1` at the
start of preflight (it should always be exactly `counter`, since `/report` writes both together).
