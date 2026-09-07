# sirocco — Realm

| | |
|---|---|
| Layer | foundation |
| Path | `/Users/fn/codespace/sirocco` |
| GitHub | `yusa-imit/sirocco` |
| Version | 0.1.0 (`build.zig.zon`) · latest tag none (no tags yet) |
| Zig | 0.15.2 — migrating to 0.16.0 under plan `001` |
| Depends on | none — Zig std only (`build.zig.zon` `.dependencies = .{}`) |
| Consumers | sailor, zr, silica, zoltraak (planned, dotted in `KINGDOM.md`) · synod (adapter) |
| blocked_by | — |
| CI | Linux tests + 6 cross-compile targets (`.github/workflows/ci.yml`) |

## What it is

sirocco is the kingdom's foundation network runtime: a zero-dependency, completion-based
async I/O stack for Zig, meant to become the `std.Io.VTable` implementation (kqueue/epoll,
net, sleep/now) that silica, zoltraak, sailor, zr, and synod (adapter) run on. Today it is a
well-scaffolded but functionally empty skeleton — 187 lines across 8 files, six identical
module stubs (`io`, `net`, `tls`, `http`, `ws`, `task`) each raising `error.NotImplemented`,
plus a minimal CLI. `docs/PRD.md` and `docs/milestones.md` describe the intended surface
honestly as not-yet-built; per ROADMAP Phase 2 the PRD itself is due for a rewrite against
`std.Io.VTable` before Phase 1 ("Loop Core") lands.

## Build and test

```bash
zig build              # library + CLI
zig build test         # unit tests (~1s — 7 stub "module compiles" tests, no real I/O yet)
zig fmt --check src build.zig
```

Local-only: `zig build`, `zig build test`. CI-only: cross-compile, benchmarks, fuzz.
No servers or ports to start or kill — the runtime has no daemon yet and the CLI only
prints `version`/`--help`. Build and test are both near-instant given the current stub-only
codebase; this will change once Phase 1 (event loop, backends) lands.

## Realm-specific rules

Per `docs/adr/0001-std-io-vtable.md` (2026-09-08, plan 001 item 7): sirocco's public surface
is `std.Io` — one `Runtime.io()` call — not a parallel `io -> net -> tls -> http/ws` API.
Backends (kqueue/epoll/...) and net/file slot implementations are internal, one file per
concern, assembled only in `src/runtime.zig`.

- Completions are std's: `Io.Operation`/`Io.Operation.Storage` (caller-owned, intrusive) and
  `Io.Batch`. sirocco implements the `operate`/`batchAwaitAsync`/`batchAwaitConcurrent`/
  `batchCancel` slots, not its own completion queue type.
- Every blocking op takes its deadline via `Io.Timeout` (`.none | .duration | .deadline`)
  through `batchAwaitConcurrent`.
- Buffers are caller-owned; `net*`/`file*` read/write are vectored (`[]const []u8`) — the
  runtime never copies user buffers.
- Cancellation is std's vocabulary: `Io.Cancelable`, `error.Canceled` (one `l`, not
  `Cancelled`), `recancel`, `swapCancelProtection`, `checkCancel`. sirocco defines no
  cancellation type of its own.
- Backend isolation: only `src/backend/*` may touch OS APIs; every other file sees fibers,
  `Io.Operation`, and completions.
- The declared hybrid (`dir*`, `process*`/`child*`, `random`/`randomSecure`,
  `progressParentFile` — 40 of 109 vtable slots) forwards to an embedded `Io.Threaded` until
  each is implemented natively; `Options.unimplemented` makes the forwarding set visible and
  testable, never a hidden stopgap.
- Every vtable slot is differential-tested against `Io.Threaded` from one `Runtime`
  (`rt.io()` vs `rt.baselineIo()`).
- Servers shut down gracefully: stop accepting -> drain in-flight -> force close, in order.
- File size cap: 800 lines, one concept per file (stricter than the kingdom's per-function
  line-count rule).
- `docs/plans/000-inherited.md` carries a per-item supersession table against the ADR;
  `docs/plans/NNN-*.md` (plan 002+) is the source of truth for what's actually being built
  next, not `000-inherited.md`'s original checklists.

## Layout

| File | Lines | Role |
|---|---|---|
| `src/root.zig` | 21 | Library root — re-exports io/net/tls/http/ws/task, version 0.1.0 |
| `src/main.zig` | 36 | Minimal CLI: `version` and `--help` only |
| `src/io.zig` | 24 | Stub: event loop, completions, timers, cancellation (no backend yet) |
| `src/net.zig` | 23 | Stub: TCP/UDP/Unix sockets, address parsing, DNS, connection pool |
| `src/tls.zig` | 20 | Stub: TLS 1.3 client/server on `std.crypto.tls` |
| `src/http.zig` | 22 | Stub: HTTP/1.1 parser/client/server, HTTP/2 (HPACK) |
| `src/ws.zig` | 20 | Stub: WebSocket (RFC 6455) client/server framing |
| `src/task.zig` | 21 | Stub: thread pool, bounded channel, wait group, scheduler |

Planned per-module sub-files (`io/backend/{kqueue,epoll,io_uring,iocp}.zig`, `net/*.zig`,
`tls/*.zig`, `http/*.zig`, `http/h2/*.zig`, `ws/*.zig`, `task/*.zig`) do not exist yet — see
`docs/PRD.md` for the sketch, `docs/milestones.md` for the checklist. `tests/` and
`examples/` currently hold only `.gitkeep`; `bench/main.zig` is a scaffold.

## Known gaps (from STATE.md)

- Tiger Style counters (asserts, `catch unreachable`, `@panic`, `debug.print`, unbounded
  `while (true)`, files > 800 lines) are all 0 — not evidence of discipline, just evidence
  that no functional code has been written yet. Re-check once Phase 1 lands.
- No real test coverage: 7 trivial "module compiles" tests only; no loopback I/O, no
  fuzzing, no property tests. `tests/`/`examples/` are empty placeholders.
- Zig 0.16 probe: 2 surfaced compiler errors (~4 latent call sites across `src/main.zig` and
  `bench/main.zig`): `GeneralPurposeAllocator` removed, `argsAlloc` removed, stdout writer
  now needs an `Io` handle, `std.time.Timer` removed. Effort: trivial, <1h, no blockers —
  library modules already pass under 0.16 because they are stubs.
- No preserved `wip/*` branch this session — foundation repos (sigil, sirocco, strata,
  synod) have none; working tree is clean.
- External dependency timelines on sirocco (silica, zoltraak, sailor, zr, synod) are
  currently unfounded — the runtime they'd depend on does not exist yet.
