# sigil — Realm

| | |
|---|---|
| Layer | foundation |
| Path | `/Users/fn/codespace/sigil` |
| GitHub | `yusa-imit/sigil` |
| Version | 0.1.0 (`build.zig.zon`) · latest tag — (no tags cut yet) |
| Zig | 0.15.2 (migrating to 0.16.0 under plan 001) |
| Depends on | none — Zig std only (ADR-001); `build.zig.zon` `.dependencies = .{}` |
| Consumers | zr, silica, zoltraak, synod — all planned/dotted in `KINGDOM.md`, no solid |
| | dependency edge exists yet (nothing in sigil is implemented to depend on) |
| blocked_by | — |
| CI | Linux tests + 6 cross-compile targets (`.github/workflows/ci.yml`) |

## What it is

sigil is the kingdom's planned unified Value-IR + comptime-reflection serialization and
config library: one `Value`/`ValueTree` representation and a `struct <-> Value` reflection
layer underneath JSON (+ JSON Pointer/JSONPath/Patch/Merge Patch), TOML 1.0, YAML 1.2 core
subset, MessagePack, CBOR, Protobuf wire format, CSV, and a layered (file + env + args)
config loader. It exists to let zr's TOML/YAML, zoltraak's JSON/JSONPath, silica's JSON
types, and synod's message encoding stop reimplementing the same Value-tree problem.
**As of this survey (2026-09-05) none of that is built.** The repo is a freshly bootstrapped
scaffold (2 commits): 10 top-level modules are identical ~19-26 line stub files (a doc
comment, `Error = error{NotImplemented}`, one compile-check test), their planned submodule
directories are empty, and `src/main.zig` (a version/--help CLI) is the only real code.
See `STATE.md` for the full honest inventory.

## Build and test

```bash
zig build              # library + CLI
zig build test         # unit tests (~1s; 12 tests, all compile-check placeholders today)
zig fmt --check src build.zig
```

Local-only: `zig build`, `zig build test`. CI-only: cross-compile, benchmarks, fuzz.
No servers, daemons, or ports — sigil is a library + single-shot CLI, nothing to kill
between runs. `bench/main.zig` is wired into the `bench` build step but has no benchmarks
yet (the perf-targets table in `docs/milestones.md` and `docs/PRD.md` §5 is still empty).

## Realm-specific rules

These are sigil's own design rules (not already covered by `citadel/core/rules/`):

- **Parsers never trust input**: default depth limit 128, explicit input-size limits, an
  alias-expansion cap (YAML), and explicit overflow errors — never silent truncation.
- **Diagnostics are first-class**: every parse failure fills `Diagnostics{line, col,
  message}`. No position-less parse errors anywhere in the format modules.
- **DOM ownership**: the DOM is arena-owned via `ValueTree`, freed once as a unit.
  Reflection result slices are tied to the tree's lifetime — this must be doc-commented at
  every function that returns one.
- **Round-trip guarantee**: for TOML/YAML/JSON, parse -> stringify -> parse must yield the
  same `Value` (comments excepted). This is a property-tested invariant, not just a unit test.
- **Numeric exactness**: `i64`/`u64`/`f64` are preserved distinctly through the pipeline; no
  silent int -> float coercion.
- **Format modules are siblings, not a hierarchy**: `json/`, `toml/`, `yaml/`, `msgpack/`,
  `cbor/`, `proto/`, `csv/` must not import each other. Only `core/` and `reflect/` are
  shared underneath all of them.
- **zuda-first does not apply here**: sigil is foundation-layer (zero kingdom deps by
  ADR-001), so the kingdom's usual "check zuda before writing a container" rule is moot —
  sigil is itself one of the things other repos are meant to stop reimplementing.
- **Consumer registry** (what each planned consumer is expected to replace with sigil, once
  it exists): zr -> its local TOML/YAML readers; zoltraak -> its local JSON/JSONPath;
  silica -> its local JSON value types; synod -> its message encoding. None of these
  migrations can start before sigil ships a real JSON or TOML module.
- **Release quirk**: `build.zig.zon` already declares `0.1.0` with nothing implemented —
  do not tag or publish a release until Phase 1 (core + reflect) lands; a `zig fetch` today
  would hand a consumer an empty library.

## Layout

| Path | Lines | Status |
|---|---:|---|
| `src/root.zig` | 26 | library root; re-exports the 10 stubs + `sigil.version` |
| `src/main.zig` | 36 | CLI entry point (version/--help); only real working code |
| `src/core.zig` (+ empty `src/core/`) | 23 | stub: Value/ValueTree/Number/Timestamp/Diagnostics |
| `src/reflect.zig` (+ empty `src/reflect/`) | 21 | stub: comptime struct<->Value mapping |
| `src/json.zig` (+ empty `src/json/`) | 21 | stub: JSON scanner/DOM/writer |
| `src/path.zig` (+ empty `src/path/`) | 21 | stub: JSON Pointer/JSONPath/Patch/MergePatch |
| `src/toml.zig` (+ empty `src/toml/`) | 20 | stub: TOML 1.0 |
| `src/yaml.zig` (+ empty `src/yaml/`) | 20 | stub: YAML 1.2 core subset |
| `src/msgpack.zig` (+ empty `src/msgpack/`) | 19 | stub: MessagePack |
| `src/cbor.zig` (+ empty `src/cbor/`) | 19 | stub: CBOR |
| `src/proto.zig` (+ empty `src/proto/`) | 19 | stub: Protobuf wire format |
| `src/csv.zig` (+ empty `src/csv/`) | 19 | stub: CSV reader/writer |
| `src/config.zig` (+ empty `src/config/`) | 21 | stub: layered config loader |
| `bench/main.zig` | — | benchmark harness, wired into `build.zig` `bench` step |
| `examples/`, `tests/` | — | `.gitkeep` only, no files yet |

`docs/PRD.md` (192 lines) has the full design; `docs/milestones.md` is the single source of
truth for progress (Phases 1-6, all unchecked). Module layout above is reference-only —
update this table and `memory/architecture.md` when structure changes.

## Known gaps (from STATE.md)

All Tiger Style grep metrics read 0 (asserts, `catch unreachable`, `@panic`,
`std.debug.print`, unbounded `while (true)`, files > 800 lines) — this is a **non-finding**,
not a clean bill of health: at 285 LOC of stub files there is no logic yet to violate
anything. Revisit once Phase 1-2 (core/json) land real parsing code.

Top risks carried forward:
- README's module table describes the intended end state as already built; only a small
  "Status: Bootstrap" line says otherwise — easy for a reader (or a consumer) to miss.
- All 12 tests are compile-check placeholders; zero functional coverage exists to catch
  regressions once real parsers land.
- `0.1.0` is declared with nothing implemented; see the release quirk above.

No `wip/*` branch exists for sigil this session — `dirty_tree` was clean (no uncommitted or
stashed work to preserve). Foundation repos (sigil, sirocco, strata, synod) have none.
