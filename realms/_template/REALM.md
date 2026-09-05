# {{NAME}} — Realm

| | |
|---|---|
| Layer | {{LAYER}} |
| Path | `/Users/fn/codespace/{{NAME}}` |
| GitHub | `yusa-imit/{{NAME}}` |
| Version | {{VERSION}} (`build.zig.zon`) · latest tag {{TAG}} |
| Zig | {{ZIG}} |
| Depends on | {{DEPS}} |
| Consumers | {{CONSUMERS}} |
| blocked_by | {{BLOCKED_BY}} |
| CI | Linux tests + 6 cross-compile targets (`.github/workflows/ci.yml`) |

## What it is

{{ONE_PARAGRAPH}}

## Build and test

```bash
zig build              # library + CLI
zig build test         # unit tests ({{TEST_TIME}})
zig fmt --check src build.zig
```

Local-only: `zig build`, `zig build test`. CI-only: cross-compile, benchmarks, fuzz.
{{RUN_NOTES}}

## Realm-specific rules

{{RULES}}

## Layout

{{LAYOUT}}

## Known gaps (from STATE.md)

{{GAPS}}
