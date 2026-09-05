#!/usr/bin/env python3
"""Scaffold a Zig kingdom component repository from citadel/templates/repo + specs/<name>.json.

Usage:
    scripts/scaffold.py <name> [--out DIR] [--force]

Idempotent for template-owned files when --force is given; never touches src/ files that already exist.
"""
import argparse
import datetime as dt
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "templates" / "repo"
SPECS = ROOT / "specs"


def render(text: str, ctx: dict) -> str:
    def sub(m):
        key = m.group(1)
        if key not in ctx:
            raise KeyError(f"unknown template key {{{{{key}}}}}")
        return ctx[key]
    return re.sub(r"\{\{([A-Z_]+)\}\}", sub, text)


def module_table(spec):
    rows = ["| Module | Purpose |", "|---|---|"]
    for m in spec["modules"]:
        rows.append(f"| `{spec['name']}.{m['name']}` | {m['doc']} |")
    return "\n".join(rows)


def module_tree(spec):
    lines = []
    mods = spec["modules"]
    for i, m in enumerate(mods):
        last = i == len(mods) - 1
        lines.append(f"│   {'└' if last else '├'}── {m['name']}.zig{' ' * max(1, 20 - len(m['name']))}# {m['doc'].split('.')[0]}")
        for f in m["files"]:
            lines.append(f"│   {' ' if last else '│'}   ├── {m['name']}/{f}")
    return "\n".join(lines)


def phase_checklist(spec):
    out = []
    for p in spec["phases"]:
        out.append(f"## {p['title']}\n")
        for item in p["items"]:
            out.append(f"- [ ] {item}")
        out.append("")
    return "\n".join(out)


def bullets(items):
    return "\n".join(f"- {i}" for i in items)


def zig_fingerprint(name: str) -> str:
    """Run `zig init` in a temp dir *named after the package* — the fingerprint's upper
    half is derived from the package name, so the directory name must match."""
    import tempfile, shutil
    with tempfile.TemporaryDirectory() as td:
        scratch = pathlib.Path(td) / name
        scratch.mkdir()
        subprocess.run(["zig", "init"], cwd=scratch, check=True, capture_output=True)
        zon = (scratch / "build.zig.zon").read_text()
        return re.search(r"\.fingerprint = (0x[0-9a-f]+)", zon).group(1)


def write(path: pathlib.Path, content: str, force: bool, made: list):
    if path.exists() and not force:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    made.append(str(path.relative_to(path.parents[len(path.relative_to(path.anchor).parts) - 1])) if False else str(path))


def module_stub(spec, m):
    files = "\n".join(f"//!   - `{m['name']}/{f}`" for f in m["files"]) or "//!   (single-file module)"
    return f"""//! {spec['name']}.{m['name']} — {m['doc']}
//!
//! Planned files (see docs/PRD.md):
{files}
//!
//! Status: stub. Public declarations are added as PRD phases land.

const std = @import("std");

/// Module-level error set. Extend as functionality lands; keep names descriptive
/// (`error.ChecksumMismatch`, not `error.Invalid`).
pub const Error = error{{
    NotImplemented,
}};

test "{m['name']}: module compiles" {{
    std.testing.refAllDecls(@This());
}}
"""


def root_zig(spec):
    imports = "\n".join(f'pub const {m["name"]} = @import("{m["name"]}.zig");' for m in spec["modules"])
    return f"""//! {spec['name']} — {spec['tagline']}
//!
//! Library root. Consumers `@import("{spec['name']}")` and reach modules as
//! `{spec['name']}.<module>`. Every module is independent; import only what you use.
//!
//! See docs/PRD.md for the full design and docs/milestones.md for progress.

const std = @import("std");

pub const version = std.SemanticVersion{{ .major = 0, .minor = 1, .patch = 0 }};

{imports}

test {{
    std.testing.refAllDecls(@This());
}}
"""


def main_zig(spec):
    return f"""const std = @import("std");
const {spec['name']} = @import("{spec['name']}");

/// Minimal CLI: `{spec['name']} version` / `{spec['name']} --help`.
/// Diagnostic subcommands are added as modules land (see docs/PRD.md).
pub fn main() !void {{
    var gpa_state = std.heap.GeneralPurposeAllocator(.{{}}){{}};
    defer _ = gpa_state.deinit();
    const gpa = gpa_state.allocator();

    const args = try std.process.argsAlloc(gpa);
    defer std.process.argsFree(gpa, args);

    var stdout_buffer: [512]u8 = undefined;
    var stdout_writer = std.fs.File.stdout().writer(&stdout_buffer);
    const out = &stdout_writer.interface;
    defer out.flush() catch {{}};

    const cmd = if (args.len > 1) args[1] else "--help";
    if (std.mem.eql(u8, cmd, "version")) {{
        try out.print("{spec['name']} {{f}}\\n", .{{{spec['name']}.version}});
    }} else {{
        try out.print(
            \\\\{spec['name']} — {spec['tagline']}
            \\\\
            \\\\usage: {spec['name']} <command>
            \\\\  version    print library version
            \\\\  --help     this text
            \\\\
        , .{{}});
    }}
}}

test "cli: version is exposed" {{
    try std.testing.expectEqual(@as(u32, 0), {spec['name']}.version.major);
}}
"""


def bench_main(spec):
    return f"""//! {spec['name']} benchmark harness. Run: `zig build bench -- [filter]`
//! Each benchmark prints `name  ops/s  ns/op` so results can be pasted into docs/milestones.md.

const std = @import("std");
const {spec['name']} = @import("{spec['name']}");

const Bench = struct {{ name: []const u8, run: *const fn (std.mem.Allocator) anyerror!u64 }};

fn noop(_: std.mem.Allocator) !u64 {{
    return 1;
}}

const benches = [_]Bench{{
    .{{ .name = "noop", .run = noop }},
}};

pub fn main() !void {{
    var gpa_state = std.heap.GeneralPurposeAllocator(.{{}}){{}};
    defer _ = gpa_state.deinit();
    const gpa = gpa_state.allocator();

    const args = try std.process.argsAlloc(gpa);
    defer std.process.argsFree(gpa, args);
    const filter: ?[]const u8 = if (args.len > 1) args[1] else null;

    var buf: [1024]u8 = undefined;
    var w = std.fs.File.stdout().writer(&buf);
    const out = &w.interface;
    defer out.flush() catch {{}};

    for (benches) |b| {{
        if (filter) |f| if (std.mem.indexOf(u8, b.name, f) == null) continue;
        var timer = try std.time.Timer.start();
        const ops = try b.run(gpa);
        const ns = timer.read();
        const ns_per_op = if (ops == 0) 0 else ns / ops;
        const ops_per_s = if (ns == 0) 0 else ops * std.time.ns_per_s / ns;
        try out.print("{{s:<32}} {{d:>12}} ops/s {{d:>10}} ns/op\\n", .{{ b.name, ops_per_s, ns_per_op }});
    }}
}}
"""


def build_zon(spec, fp):
    return f""".{{
    .name = .{spec['name']},
    .version = "0.1.0",
    .fingerprint = {fp}, // Changing this has security and trust implications.
    .minimum_zig_version = "0.15.2",
    .dependencies = .{{}},
    .paths = .{{
        "build.zig",
        "build.zig.zon",
        "src",
        "LICENSE",
        "README.md",
    }},
}}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--out", default=str(ROOT.parent))
    ap.add_argument("--force", action="store_true", help="overwrite template-owned files")
    a = ap.parse_args()

    spec = json.loads((SPECS / f"{a.name}.json").read_text())
    repo = pathlib.Path(a.out) / spec["name"]
    repo.mkdir(parents=True, exist_ok=True)
    made = []

    zon_path = repo / "build.zig.zon"
    if zon_path.exists():
        fp = re.search(r"\.fingerprint = (0x[0-9a-f]+)", zon_path.read_text()).group(1)
    else:
        fp = zig_fingerprint(spec["name"])

    ctx = {
        "NAME": spec["name"],
        "TAGLINE": spec["tagline"],
        "DESCRIPTION": spec["description"],
        "CONSUMERS": spec["consumers"],
        "MODULE_TABLE": module_table(spec),
        "MODULE_TREE": module_tree(spec),
        "DOMAIN_RULES": bullets(spec["domain_rules"]),
        "REVIEW_CHECKLIST": bullets(spec["review_checklist"]),
        "TEST_CATEGORIES": bullets(spec["test_categories"]),
        "PHASE_CHECKLIST": phase_checklist(spec),
        "FIRST_TASKS": bullets(spec["first_tasks"]),
        "FINGERPRINT": fp,
        "DATE": dt.date.today().isoformat(),
    }

    # Template-owned files (overwritable with --force)
    mapping = {
        "build.zig": "build.zig",
        "gitignore": ".gitignore",
        "LICENSE": "LICENSE",
        "README.md": "README.md",
        "ci.yml": ".github/workflows/ci.yml",
        "milestones.md": "docs/plans/000-inherited.md",
    }
    for src, dst in mapping.items():
        write(repo / dst, render((TEMPLATES / src).read_text(), ctx), a.force, made)
    write(repo / "docs" / "PRD.md", (SPECS / f"{spec['name']}.PRD.md").read_text(), a.force, made)

    # Source files: created once, never overwritten (developers own them after bootstrap)
    write(repo / "build.zig.zon", build_zon(spec, fp), False, made)
    write(repo / "src" / "root.zig", root_zig(spec), False, made)
    write(repo / "src" / "main.zig", main_zig(spec), False, made)
    write(repo / "bench" / "main.zig", bench_main(spec), False, made)
    for m in spec["modules"]:
        write(repo / "src" / f"{m['name']}.zig", module_stub(spec, m), False, made)
        if m["files"]:
            (repo / "src" / m["name"]).mkdir(exist_ok=True)
    for d in ("examples", "tests"):
        (repo / d).mkdir(exist_ok=True)
        write(repo / d / ".gitkeep", "", False, made)

    print(f"{spec['name']}: {len(made)} files written → {repo}")


if __name__ == "__main__":
    main()
