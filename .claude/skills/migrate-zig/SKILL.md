---
name: migrate-zig
description: Migrate a realm from Zig 0.15.2 to 0.16.0 following the kingdom checklist (std.Io, allocators, ArrayList, time, threads, build.zig, tests, CI).
argument-hint: <realm>
---

Read `citadel/core/rules/zig-0.16.md` first. Toolchain: `/Users/fn/.zr/toolchains/zig/0.16.0/zig`
(global `zig` is 0.15.2 until the realm is migrated; after migration set `minimum_zig_version`
to `0.16.0` so `mlugg/setup-zig@v2` resolves it in CI).

Order inside a realm: `build.zig` (`link_libc` on the module, no `linkLibC()`) →
`src/main.zig` (`pub fn main(init: std.process.Init)`) → allocators → `std.fs` → `std.Io.Dir/File`
→ `std.time` → `std.Io.Clock/Timestamp` → `std.Thread.*` sync → `std.Io.*` → `std.net` →
`std.Io.net` → `std.io` readers/writers → `ArrayList` `.empty` → `std.mem.indexOf*` → `find*`
→ `error.Canceled` prongs → tests (`std.testing.io`, Smith fuzzers) → CI (`0.16.0`).

Convention (kingdom-wide, decided in sigil's 001): library functions that do I/O take
`io: std.Io` as the first parameter after the receiver; long-lived owning structs may cache an
`Io` field; tests use `std.testing.io`. Do not build on `std.Io.Threaded.global_single_threaded`.

Blockers: a consumer cannot finish until its kingdom dependencies have tagged 0.16 releases
(`blocked_by` in `REALM.md`). Migrate what compiles without them, keep the PR open as draft
(`gh pr ready --undo`) until the tags exist, then bump `build.zig.zon` hashes.
