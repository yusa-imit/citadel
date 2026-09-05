# sirocco — architecture

_(migrated from the repo's former `.claude/memory/architecture.md`; keep under 200 lines)_

See `docs/PRD.md` §4 for the intended layering. Record here only what **diverges** from or
**refines** the PRD — the old file was an empty skeleton (no modules had landed), so there
is nothing to reconcile yet. Layering as designed, carried over from the old `CLAUDE.md`
since it is not restated in `citadel/core/`:

## Layering (as designed, none built yet)

- Strict one-directional dependency: `io -> net -> tls -> http/ws`. Each layer must be
  independently usable. `task` (thread pool, channel, scheduler) sits alongside, not in
  the chain.
- `io`: event loop, completions, timers, cancellation, backend abstraction
  (`io/backend/{kqueue,epoll,io_uring,iocp}.zig`).
- `net`: TCP/UDP/Unix sockets, address parsing, DNS resolver, connection pool
  (`net/{address,tcp,udp,unix,dns,pool}.zig`).
- `tls`: TLS 1.3 client/server on `std.crypto.tls` (`tls/{client,server,pem}.zig`).
- `http`: HTTP/1.1 parser/client/server + HTTP/2 HPACK
  (`http/{parser,client,server}.zig`, `http/h2/{hpack,stream}.zig`).
- `ws`: WebSocket (RFC 6455) client/server framing, ping/pong, close handshake
  (`ws/{frame,client,server}.zig`).

**Open question carried from ROADMAP Phase 2**: this layering predates Zig 0.16's
`std.Io.VTable`, whose purpose overlaps it almost entirely (event loop, backends, net,
sleep/now). The PRD is due a rewrite to target `std.Io.VTable` directly before Phase 1
implementation starts — do not treat the layering above as final until that rewrite lands.

## Interfaces

_(no vtables, ownership rules, or lifetime contracts defined yet — all six modules are
`Error{ NotImplemented }` stubs)_

## Formats

_(no wire or file formats defined yet)_
