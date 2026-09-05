# sailor — architecture

_(migrated from the repo's former .claude/memory/architecture.md + decisions.md, 2026-09-05)_

## Module dependency graph

```
sailor.tui ─────┬──→ sailor.color ──→ sailor.term
                │
sailor.repl ────┤
                │
sailor.progress ┘

sailor.arg  (standalone)
sailor.fmt  (standalone)
```

Lower layers must never import higher layers. Enforced order for implement/fix work:
`term → color → arg → repl → progress → fmt → tui` (see `REALM.md`).

## Key architectural decisions

### Immediate-mode rendering (TUI)
- No persistent widget tree.
- Every frame: caller builds layout → renders widgets → framework diffs the output buffer.
- Inspired by ratatui (Rust).
- Rationale: simpler mental model, no hidden state, easier testing.

### Widget = plain struct, no vtable
- Widget struct has a `render(self, buf: *Buffer, area: Rect)` method.
- Caller passes the widget value to `Frame.render()`.
- Rationale: zero-cost, no runtime dispatch, comptime type checking.

### Writer-based output
- All output goes through a user-provided `std.io.Writer` (0.16: `std.Io.Writer`).
- The library never touches stdout/stderr directly.
- Rationale: testability (`fixedBufferStream`), composability, no global state.

### Module independence
- Each module is independently importable — `sailor.arg` works without `sailor.tui`.
- Rationale: consumers have different needs (zoltraak's server only needs arg+color; silica's
  shell needs arg+repl+fmt+tui).

## Naming and provenance

- Project named "sailor" 2026-02-27 (short, memorable, no Zig-ecosystem namespace conflicts).
- v2.0.0 (2026-04-13) removed `Buffer.setChar` and `Rect.new`; kept `Block.withTitle`-style
  builders — see `docs/v1-to-v2-migration.md` in the repo for the full breaking-change list.
