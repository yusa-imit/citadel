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
