# sigil — debugging

_(migrated from the repo's former `.claude/memory/debugging.md`, which was empty)_

Format: `## <symptom>` / **Cause** / **Fix** / **How to detect next time**

No tricky issues resolved yet — the repo is still a pure stub scaffold with no real logic
(see `STATE.md`). One known-but-not-yet-hit issue is tracked in `STATE.md`'s Zig 0.16
probe summary rather than here (it hasn't been debugged, just predicted by static
grep/compile): `std.heap.GeneralPurposeAllocator` is removed in Zig 0.16 and
`src/main.zig:7` uses it — swap for `std.heap.DebugAllocator(.{})` when the 0.16 migration
lands. Move that entry here once it has actually been hit and fixed, with the real
compiler error text.
