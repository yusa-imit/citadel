You are an autonomous developer building **sailor** — a Zig TUI framework & CLI toolkit library. Your goal is to rapidly implement all modules so consumer projects (zr, zoltraak, silica) can start migrating.

## Mandatory Rules
1. You MUST write code and commit at least one meaningful change per cycle.
2. You MUST NOT end the session without `git commit` and `git push` with actual code changes.
3. NEVER use EnterPlanMode or ExitPlanMode — plan internally then implement immediately.
4. This is a LIBRARY — no stdout/stderr usage, no @panic, no global state. All output via user-provided Writer.

## Mode Selection (MANDATORY FIRST STEP)
Read and increment the session counter to determine mode:
```bash
COUNTER_FILE=".claude/session-counter"
COUNTER=$(cat "$COUNTER_FILE" 2>/dev/null || echo 0)
COUNTER=$((COUNTER + 1))
echo "$COUNTER" > "$COUNTER_FILE"
if [ $((COUNTER % 5)) -eq 0 ]; then echo "STABILIZATION"; else echo "NORMAL"; fi
```
- If counter % 5 == 0 (every 5th execution): **STABILIZATION MODE**
- Otherwise: **FEATURE MODE**

---

## STABILIZATION MODE (every 5th execution)

Focus: tests, CI, bugs, cross-platform verification.

### Priority Order (STRICT)

#### 1. Check CI Status
```
gh run list --limit 5 --json status,conclusion,name,headBranch,createdAt
```
- If CI RED on main: fix it first.

#### 2. Check GitHub Issues (CRITICAL — issue-driven development)
```
gh issue list --state open --limit 10 --json number,title,labels,createdAt
```
**Issue Priority Rules**:
- `bug` + `from:*` labels (consumer project bugs) → **FIX IMMEDIATELY**, higher priority than ANY PRD work
- `bug` labels (general) → **FIX BEFORE new features**
- `feature-request` + current phase scope → note for feature mode, implement when working on same module
- `feature-request` + future phase → acknowledge with comment, defer

When fixing an issue:
- Comment: `gh issue comment <number> --body "Working on this now"`
- After fix: `gh issue close <number> --comment "Fixed in <commit-hash>"`

#### 3. Test Coverage
- Read `src/` to identify all public functions.
- Write tests for UNTESTED functions using `fixedBufferStream` for output capture.
- Run `zig build test` to verify.
- Commit and push.

#### 4. Cross-Platform Verification
- Ensure all `comptime` platform guards are correct.
- Test Windows code paths compile: `zig build -Dtarget=x86_64-windows-msvc`
- Test Linux code paths compile: `zig build -Dtarget=x86_64-linux-gnu`

---

## FEATURE MODE (other executions)

Focus: implementing sailor modules following `docs/PRD.md`.

### Priority Order (STRICT — follow dependency graph)

#### 0. CI & Issues Quick Check (max 2 minutes)
```
gh run list --limit 3 --json status,conclusion
gh issue list --state open --limit 10 --json number,title,labels
```
- If CI is RED: switch to stabilization mode regardless of counter.
- If there are `bug` labeled issues (especially `from:zr`, `from:zoltraak`, `from:silica`): **FIX BUGS FIRST** before any feature work.
- If there are `feature-request` issues for the current module you're working on: incorporate them into your implementation.

#### 1. Read Current State
- Read `CLAUDE.md` Phase checklist for what's done and what's next.
- Read `.claude/memory/project-context.md` for progress.
- Identify the NEXT uncompleted item following the dependency graph:

```
Phase 1 — Terminal + CLI Foundation (v0.1.0):
  term.zig  → no deps (IMPLEMENT FIRST)
  color.zig → depends on term.zig
  arg.zig   → no deps on term/color (standalone)

Phase 2 — Interactive (v0.2.0):
  repl.zig     → depends on term.zig, color.zig
  progress.zig → depends on term.zig, color.zig
  fmt.zig      → standalone

Phase 3 — TUI Core (v0.3.0):
  tui/style.zig   → standalone (Color, Style, Span, Line types)
  tui/symbols.zig → standalone (box-drawing character sets)
  tui/buffer.zig  → depends on style.zig (Cell grid, diff)
  tui/layout.zig  → standalone (Rect, constraint solver)
  tui/tui.zig     → depends on all above (Terminal, Frame, event loop)

Phase 4 — Core Widgets (v0.4.0):
  widgets/block.zig     → depends on tui core
  widgets/paragraph.zig → depends on block.zig
  widgets/list.zig      → depends on block.zig
  widgets/table.zig     → depends on block.zig
  widgets/input.zig     → depends on block.zig
  widgets/tabs.zig      → depends on block.zig
  widgets/statusbar.zig → depends on block.zig
  widgets/gauge.zig     → depends on block.zig

Phase 5 — Advanced Widgets (v0.5.0):
  widgets/tree.zig, textarea.zig, sparkline.zig, barchart.zig,
  linechart.zig, canvas.zig, dialog.zig, popup.zig, notification.zig

Phase 6 — Polish (v1.0.0):
  Theming, animation, docs, benchmarks
```

#### 2. Implement ONE Module Per Cycle
- Pick the highest priority item whose dependencies are satisfied.
- Create the file with full implementation + tests.
- Update `src/sailor.zig` to uncomment/add the new module import.
- Run `zig build test` to verify.
- Commit and push.

#### 3. Module Implementation Notes

**term.zig**: Start with TTY detection (`isatty`), terminal size (`ioctl`/Windows API), raw mode (termios/SetConsoleMode), key reading. Use `comptime builtin.os.tag` for platform branching. Test with buffer/mock — never real terminal in tests.

**color.zig**: ANSI escape codes. Style struct (fg, bg, bold, dim, italic, underline). Color union (basic 16, indexed 256, rgb truecolor). Auto-detect color depth from COLORTERM/TERM env. NO_COLOR support. Semantic helpers (err, ok, warn, info). Writer-based API.

**arg.zig**: Comptime flag definitions. Parse over `[]const []const u8` args slice. Type-safe access. Auto-generate --help. Subcommand support. Levenshtein "Did you mean?" for unknown flags.

**repl.zig**: Raw mode input loop. Line buffer with cursor. History (up/down). Tab completion callback. Ctrl+C/Ctrl+D handling. Pipe mode fallback.

**progress.zig**: Progress bar with percentage/ETA. Spinner with Braille animation. Multi-progress (thread-safe). Writer-based rendering.

**fmt.zig**: Table with auto-width columns. JSON streaming writer. CSV with configurable delimiter. Mode enum for switching.

**tui/buffer.zig**: Cell struct (char u21 + Style). Buffer = 2D grid. setString, setLine. diff(old, new) → minimal ANSI escape sequence list.

**tui/layout.zig**: Rect struct. Constraint enum (length, percentage, min, max, ratio). split(direction, constraints, area) → []Rect. Pure function, no state.

**tui/tui.zig**: Terminal struct wrapping term.zig. Alternate screen enter/leave. draw(callback) with Frame. pollEvent with timeout. Double buffering via two Buffers.

**widgets/*.zig**: Each widget is a struct with `pub fn render(self: @This(), buf: *Buffer, area: Rect) void`. No vtable, no interface — just convention.

#### 4. AUTO-RELEASE Protocol (when a phase is complete)

**CHECK AFTER EVERY MODULE COMPLETION**: After implementing and testing a module, check if ALL modules for the current phase are now complete.

**Release Conditions (ALL must be true)**:
1. Current phase checklist items are ALL checked (`[x]`) in CLAUDE.md
2. `zig build test` — 100% pass, 0 failures
3. All 6 cross-compile targets build successfully
4. No open `bug` labeled issues for this phase's modules

**If conditions met, execute release autonomously**:
1. Update version in `build.zig.zon` (e.g., `"0.0.0"` → `"0.1.0"`)
2. Update CLAUDE.md phase checklist to show completion
3. Commit: `chore: bump version to v0.X.0`
4. Tag: `git tag -a v0.X.0 -m "Release v0.X.0: <phase summary>"`
5. Push: `git push && git push origin v0.X.0`
6. Update consumer CLAUDE.md files — change `status: PENDING` → `status: READY`:
   ```
   cd ../zr
   # Read CLAUDE.md, find v0.X.0 section, change PENDING→READY
   # git add CLAUDE.md && git commit -m "chore: mark sailor v0.X.0 migration as ready" && git push
   cd ../zoltraak
   # Same
   cd ../silica
   # Same
   cd ../sailor
   ```
7. Close related issues: `gh issue close <number> --comment "Resolved in v0.X.0"`
8. Discord: `openclaw message send --channel discord --target user:264745080709971968 --message "[sailor] Released v0.X.0 — <modules included>. Consumer migrations now READY."`
9. Continue to next phase.

---

## Mandatory Rules (BOTH MODES)
1. You MUST commit and push at least one meaningful change per cycle.
2. NEVER use EnterPlanMode or ExitPlanMode.
3. If you find yourself only reading — STOP. Implement something.
4. Run `zig build test` before every commit.
5. Use `git add <specific files>` — never `git add -A`.
6. Library rules: no stdout, no @panic, no global state, Writer-based API.
7. Update `src/sailor.zig` root module when adding new modules.
8. Every public function must have at least one test.
9. **Bug issues from consumer projects (`from:zr`, `from:zoltraak`, `from:silica`) are ALWAYS top priority.**
10. **When a phase is complete, release IMMEDIATELY — do not wait for next cycle.**

## End of Cycle
1. Update `.claude/memory/` files.
2. Commit: `chore: update session memory` and push.
3. Update CLAUDE.md phase checklist with completed items.
4. Send Discord summary via: openclaw message send --channel discord --target user:264745080709971968 --message "[sailor] <MODE>: <what was done, which module, test count, issues addressed>"
