#!/usr/bin/env python3
"""PostToolUse: run zig fmt on an edited .zig file with the toolchain the repo declares."""
import json
import os
import re
import subprocess
import sys

data = json.load(sys.stdin)
path = (data.get("tool_input") or {}).get("file_path", "") or ""
if not path.endswith(".zig") or not os.path.exists(path):
    sys.exit(0)
root = os.path.dirname(path)
zig = "zig"
while root and root != "/":
    zon = os.path.join(root, "build.zig.zon")
    if os.path.exists(zon):
        if re.search(r'minimum_zig_version\s*=\s*"0\.16', open(zon).read()):
            zig = "/Users/fn/.zr/toolchains/zig/0.16.0/zig"
        break
    root = os.path.dirname(root)
r = subprocess.run([zig, "fmt", path], capture_output=True, text=True)
if r.returncode != 0:
    print(f"zig fmt failed for {path}: {r.stderr.strip()[:500]}", file=sys.stderr)
sys.exit(0)
