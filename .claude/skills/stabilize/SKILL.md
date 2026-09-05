---
name: stabilize
description: Stabilization cycle for a realm — CI matrix, test-quality audit, Tiger Style audit, benchmark and docs drift, dependency pins. Each fix is its own PR.
argument-hint: <realm> [--one]
---

Realm from `$ARGUMENTS`. With `--one`, do exactly one bounded task (≤ 10 min) and return. Each
fix is a PR via `/implement`. Update `/Users/fn/codespace/citadel/realms/<realm>/STATE.md` numbers
at the end. Tiger Style counts use `\bassert\(` (any spelling).

1. CI: last 5 runs; any red → fix first.
2. Tiger Style audit (`tidy-auditor`, sonnet): counts of `catch unreachable` without a proof
   comment, `@panic` in library code, `std.debug.print` in library code, `while (true)` outside
   event loops, functions > 70 lines, files > 800 lines, `usize` in formats, missing `//!`.
   Fix one class per cycle, smallest-diff-first; record the rest in `STATE.md`.
3. Test quality (`test-writer`): remove always-pass assertions, add negative-space cases,
   make sure every declared error variant is provoked by a test, leak checks.
4. Docs drift: README claims vs code (version badge, feature list, install snippet).
5. Dependencies: tags only, newest kingdom tag (`/Users/fn/codespace/citadel/zr-repos.toml`).
6. Benchmarks (only if `pgrep -f "zig build"` shows no other Zig build): record in `STATE.md`,
   flag > 10 % regressions.
7. Hygiene: root files vs `/Users/fn/codespace/citadel/protocol/DOCS.md`, `.gitignore`,
   tracked artifacts.
