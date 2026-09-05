# tidy

The kingdom's reference lint. One file, `tidy.zig`, zero dependencies, compiles and passes its
own unit tests under both `/opt/homebrew/bin/zig` (0.15.2) and
`/Users/fn/.zr/toolchains/zig/0.16.0/zig` (0.16.0) — the two toolchains a realm may be pinned to
during the kingdom's 0.15 → 0.16 migration window. See `citadel/core/rules/tiger-style.md`
§5 ("Mechanical checks") for the rules this file enforces; this is that checker.

## Wiring it into a realm's `build.zig`

```zig
const tidy = b.addExecutable(.{
    .name = "tidy",
    .root_module = b.createModule(.{
        // Vendor tidy.zig into the realm, e.g. as tools/tidy.zig.
        .root_source_file = b.path("path/to/tidy.zig"),
        .target = b.graph.host,
    }),
});
const run_tidy = b.addRunArtifact(tidy);
run_tidy.addArgs(&.{ "--root", b.pathFromRoot(".") });
// Or, to match the tool's own defaults, no args are needed at all: it walks
// `src/`, `build.zig`, `bench/`, `tests/` from the current working directory
// and reads `./tidy_baseline.txt`, both relative to wherever `zig build` runs.

const test_step = b.step("test", "Run unit tests and tidy");
test_step.dependOn(&run_tidy.step);
// ... dependOn(&run_unit_tests.step) etc.

const tidy_step = b.step("tidy", "Run the tidy lint on its own");
tidy_step.dependOn(&run_tidy.step);
```

Then:

```sh
zig build tidy   # lint only
zig build test   # unit tests + tidy, since test_step depends on run_tidy
```

`tidy` exits 1 if any check fails, 0 otherwise, so `run_tidy.step` fails the build the same way
a failing test does. `zig build` runs the realm's own pinned toolchain, so `tidy.zig` only ever
needs to compile under *that one* version at build time — the dual-toolchain requirement is for
compiling `tidy.zig` itself while it lives here in citadel and travels between realms mid-cycle.

`tidy.zig` has no imports beyond `std` — vendor it by copying the file into the realm (e.g.
`tools/tidy.zig` or `scripts/tidy.zig`) rather than referencing citadel's copy, since a realm
must build standalone without `--add-dir citadel`.

## Flags

```
tidy [--root <dir>] [--baseline <path>]
```

- `--root <dir>` — defaults to `.` (the current working directory, normally the repo root when
  run via `zig build tidy`). Everything is walked and reported relative to this root.
- `--baseline <path>` — defaults to `./tidy_baseline.txt`. A missing baseline file is not an
  error: it is treated as empty, so every over-length function fails until it is either
  shortened or added to the baseline.

## What it checks

Walks `src/`, `build.zig`, `bench/`, `tests/` under `--root`, skipping any directory named
`.zig-cache`, `zig-out`, or `zig-pkg`, and considers every `.zig` file found.

1. **Line length** — at most 100 Unicode code points per line (counted as code points, not
   bytes, so multi-byte UTF-8 text is not penalized for its encoded size).
2. **Doc header** — the first line of every `.zig` file under `src/` must start with `//!`.
3. **Function length** — any `fn name(` (no space before the paren) whose body spans more than
   70 lines fails, unless listed in the baseline (see below). Measured by brace depth from the
   line containing `fn name(` to the line where that depth first returns to zero — braces inside
   string/char literals, `//` comments, and multiline string literals (`\\` lines) are ignored.
4. **Ban list** — each hit prints the matched pattern plus a suggested replacement:

   | Pattern | Scope | Exception |
   |---|---|---|
   | `catch unreachable` | everywhere | same or previous line has `// proof:` |
   | `@panic(` | everywhere | `src/main.zig`, `bench/`, `tests/` |
   | `std.debug.print(` | everywhere | `src/main.zig`, `bench/`, `tests/` |
   | `std.time.` | `src/` only | filename ends in `main.zig` |
   | `std.crypto.random` | `src/` only | — |
   | `const Self = @This()` | everywhere | — |
   | `usingnamespace` | everywhere | — |
   | `anyerror` | only when the line also has `pub fn` | — |
   | ` == error.` / ` != error.` | everywhere | — |
   | `// FIXME` | everywhere | — |
   | `dbg(` | everywhere | — |

5. **File length** — files over 800 lines print a WARNING. Warnings are listed and counted in
   the summary but never cause a non-zero exit on their own.

Output is one line per finding:

```
path:line: rule: message [replacement]
```

(the `[replacement]` suffix only appears for ban-list findings), followed by a summary line:

```
tidy: N finding(s), F failing, W warning(s)
```

Exit code is 1 if any finding is a failure (any check above except file-length), 0 otherwise.

### Known limitation

Detection is line-oriented, not a real parser: `fn name(` is matched by simple substring search
line-by-line (skipping identifier characters immediately before `fn`), so a string or comment
that happens to contain literal text shaped like `fn name(` will be mismeasured. In practice this
does not occur in idiomatic Zig source; it is a deliberate simplicity trade-off for a
dependency-free reference lint, not a design goal to fix.

## How the baseline works

`tidy_baseline.txt` (default path `./tidy_baseline.txt`, override with `--baseline`) lists
functions that are already over 70 lines and have not been shortened yet, one per line:

```
path:function_name:lines
```

- `path` is the file's path relative to `--root` (the same form printed in findings, e.g.
  `src/pool.zig`), `function_name` is the bare identifier after `fn`, and `lines` is the
  function's current measured span.
- Blank lines and lines starting with `#` are ignored, so the file can carry comments.
- **The baseline may only shrink.** Every entry is checked against the function's actual current
  length on every run:
  - If the function has shrunk to 70 lines or fewer, the entry is now stale — remove it. Reported
    as `stale-baseline: ... shrank to N lines; remove it from tidy_baseline.txt` (a failure, so
    a baseline is never allowed to drift out of sync silently).
  - If the function has grown past the recorded length, that is a regression — the entry is
    reported as `stale-baseline: ... grew to N lines (baseline says M); the baseline may only
    shrink` (a failure). Update the recorded number only by actually shortening the function, not
    by editing the baseline number upward.
  - If the recorded function no longer exists at all (renamed or removed), the entry is reported
    as `stale-baseline: baseline entry ... matches no function` (a failure) — delete the line.
  - Otherwise (still over 70 lines, and no more than the recorded length) the entry is silently
    accepted: the function fails check 3 but the baseline entry covers it, so nothing is printed.

See `tidy_baseline.txt.example` in this directory for the exact format. Copy it to
`tidy_baseline.txt` at the realm's root (or wherever `--baseline` points) and edit it to match
that realm's actual long functions — do not copy the example values verbatim.

## Verifying a copy of this file

```sh
zig test tidy.zig                       # in-memory unit tests, no filesystem access
zig build-exe tidy.zig -femit-bin=tidy  # or wire it via build.zig as shown above
./tidy --root /path/to/a/realm
```

Run both commands under each toolchain the kingdom currently supports (0.15.2 and 0.16.0) before
trusting a change to this file — the dual-toolchain compatibility is the entire point of keeping
`tidy.zig` a single comptime-branched source file instead of two.
