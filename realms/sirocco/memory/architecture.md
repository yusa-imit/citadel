# sirocco — architecture

_(migrated from the repo's former `.claude/memory/architecture.md`; keep under 200 lines)_

**Resolved 2026-09-08** (plan 001 item 7, PR TBD): the open question below was answered by
`docs/adr/0001-std-io-vtable.md` — sirocco implements `std.Io.VTable` directly; there is no
public `io -> net -> tls -> http/ws` layering. See `docs/PRD.md` §4 for the current design;
record here only what **diverges** from or **refines** the PRD.

## Layering (as designed, none built yet)

Public surface is one type: `sirocco.Runtime`, with `Runtime.io()` returning `std.Io`.
Internal files, one concern each, assembled only in `src/runtime.zig`:

- `src/sched.zig` (P0: fibers, cancel state, `Io.Group`), `src/futex.zig` (P1),
  `src/timer.zig` (P2: `now`/`clockResolution`/`sleep`), `src/submit.zig` (P3:
  `operate`/`batchAwaitAsync`/`batchAwaitConcurrent`/`batchCancel` — this is where
  `Io.Operation`'s `file_read_streaming`/`file_write_streaming`/`net_receive` live, *not*
  under `file*`/`net*`), `src/net.zig` (P4: 16 `net*` slots), `src/file.zig` (P5: 28
  `file*` slots), `src/stderr.zig` (P6), `src/hybrid.zig` (declared forwarding list),
  `src/backend/{kqueue,epoll,uring,iocp}.zig` (readiness/completion only — the only files
  touching OS APIs).
- `threaded: Io.Threaded` is embedded in `Runtime`: forwarding target for the 40-slot
  hybrid (`dir*`, `process*`/`child*`, `random`/`randomSecure`, `progressParentFile`),
  fallback backend (`Options.backend = .threaded`), and differential-test oracle
  (`rt.baselineIo()`), all from one field. `Io.userdata` is `&rt.threaded`; sirocco state
  is recovered with `@fieldParentPtr("threaded", t)` — zero-indirection forwarding, no
  per-slot thunks.
- `tls`/`http`/`ws`/`task` as public modules are gone. `std.crypto.tls.Client`,
  `std.http.Client`, `Io.Group`/`Io.Queue`/`Io.Event` run on sirocco's vtable unmodified.
- Only `src/runtime.zig` names a `VTable` field; a comptime assertion
  (`@typeInfo(Io.VTable).@"struct".fields.len == 109`) fails the build if the pinned std's
  vtable shape ever changes.

**Previously open question, now resolved**: the old layering (`io -> net -> tls -> http/ws`
as a *public* API) predated `std.Io.VTable` and is retired; `docs/plans/000-inherited.md`
carries the full per-item supersession table.

## Interfaces

`std.Io.VTable`, 109 slots, grouped P0–P6 + hybrid — full list in `docs/PRD.md` §4.3.
Cancellation is std's `Io.Cancelable`/`error.Canceled` (one `l`); sirocco defines no
cancellation type. No sirocco-defined vtable exists yet — Phase 1 of plan 002 opens it.

## Formats

_(no wire or file formats defined yet)_
