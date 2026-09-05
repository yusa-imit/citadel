#!/usr/bin/env python3
"""PreToolUse guard for Edit/Write in realm sessions.

A realm session (cwd = /Users/fn/codespace/<realm>) may write inside its own repo and inside
citadel/realms/<realm>/ only. It may never create CLAUDE.md or .claude/ inside a realm repo, and it
may never touch citadel's brain (core/, protocol/, .claude/, workflows/, scripts/, docs/).
"""
import json
import os
import sys

data = json.load(sys.stdin)
path = (data.get("tool_input") or {}).get("file_path", "") or ""
cwd = data.get("cwd") or os.getcwd()
path = os.path.realpath(path) if path else ""
cwd = os.path.realpath(cwd)
CODESPACE = "/Users/fn/codespace"
CITADEL = f"{CODESPACE}/citadel"

def block(why):
    print(f"BLOCKED by kingdom guard: {why}: {path}", file=sys.stderr)
    sys.exit(2)

if not path:
    sys.exit(0)
if cwd.startswith(CITADEL):
    sys.exit(0)  # operator / citadel-cycle sessions are not restricted here
realm = os.path.relpath(cwd, CODESPACE).split(os.sep)[0]
if cwd.startswith(CODESPACE + "/") and realm and not realm.startswith("."):
    repo = f"{CODESPACE}/{realm}"
    rel = os.path.relpath(path, repo) if path.startswith(repo + "/") else None
    if rel is not None:
        parts = rel.split(os.sep)
        if parts[0] in ("CLAUDE.md", "CLAUDE.local.md", ".claude"):
            block("realm repos carry no AI files (citadel/protocol/DOCS.md)")
        sys.exit(0)
    if path.startswith(CITADEL + "/"):
        if path.startswith(f"{CITADEL}/realms/{realm}/"):
            sys.exit(0)
        block(f"realm session for '{realm}' may only write citadel/realms/{realm}/")
    if path.startswith(CODESPACE + "/") and not path.startswith("/private/tmp") and not path.startswith("/tmp"):
        block(f"realm session for '{realm}' may not write into another repository")
sys.exit(0)
