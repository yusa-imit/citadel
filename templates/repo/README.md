# {{NAME}}

> {{TAGLINE}}

{{DESCRIPTION}}

[![CI](https://github.com/yusa-imit/{{NAME}}/workflows/CI/badge.svg)](https://github.com/yusa-imit/{{NAME}}/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Zig](https://img.shields.io/badge/zig-0.15.x-orange.svg)](https://ziglang.org)

---

## Status

**Bootstrap** — API 설계 및 Phase 1 구현 중. 안정 릴리즈 전까지 API는 변경될 수 있다.

## Modules

{{MODULE_TABLE}}

## Install

```bash
zig fetch --save https://github.com/yusa-imit/{{NAME}}/archive/refs/tags/v0.1.0.tar.gz
```

```zig
// build.zig
const {{NAME}} = b.dependency("{{NAME}}", .{ .target = target, .optimize = optimize });
exe.root_module.addImport("{{NAME}}", {{NAME}}.module("{{NAME}}"));
```

## Build

```bash
zig build            # library + CLI
zig build test       # unit tests
zig build bench      # benchmarks
zig build docs       # API docs → zig-out/docs
```

## Part of the Zig Kingdom

{{NAME}} is a foundation component consumed by: {{CONSUMERS}}.
See [citadel](https://github.com/yusa-imit/citadel) for the full map.

## License

MIT — see [LICENSE](LICENSE).
