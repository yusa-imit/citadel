#!/usr/bin/env python3
"""PreToolUse guard for Bash in kingdom sessions. Exit 2 blocks the call (before permission rules).

Blocks: force pushes; pushes that would land on main (explicit refspec, or a bare push while HEAD is
main); git add -A/--all/.; reset --hard; clean -f; history rewrites; deleting wip/* or plan/*
branches; merging PRs that are plan/hold/needs-human/wip/grant/draft/fork/foreign, or citadel PRs
that touch the permission surface; rm -rf of a workspace root; shell writes into citadel outside
the session's own realm or into another repo; jobs.py prune, and jobs.py apply unless a citadel
session runs it on a clean main equal to origin/main; direct calls to the cron server API. Grants
(protocol/GITHUB.md): the permission surface changes only through a PR the human merges. This is
a text matcher, not a policy engine — the GitHub ruleset on main is the server-side backstop.
"""
import json
import os
import re
import subprocess
import sys

data = json.load(sys.stdin)
cmd = (data.get("tool_input") or {}).get("command", "") or ""
cwd = os.path.realpath(data.get("cwd") or os.getcwd())
flat = " ".join(cmd.split())
# KINGDOM_CODESPACE exists for scripts/tests; the hook's environment comes from the launcher.
CODESPACE = os.path.realpath(os.environ.get("KINGDOM_CODESPACE", "/Users/fn/codespace"))
CITADEL = f"{CODESPACE}/citadel"
HOME = os.path.expanduser("~")
# Everything that decides what an unattended session may do. Citadel PRs touching it are grants.
PERMISSION_DIRS = ("core/", "workflows/", "scripts/", ".claude/", "protocol/")
RENDERED = re.compile(r"realms/[^/]+/(settings\.json|system\.md)")


def block(why):
    print(f"BLOCKED by kingdom guard: {why}. Command: {flat[:200]}", file=sys.stderr)
    sys.exit(2)


def realm_of(path):
    path = os.path.realpath(path)
    if not path.startswith(CODESPACE + "/"):
        return None
    return path[len(CODESPACE) + 1:].split("/")[0] or None


def on_permission_surface(rel):
    """True for a citadel-relative path that changes what sessions may do (tests excepted)."""
    if rel.startswith("scripts/tests/"):
        return False
    return rel == "CLAUDE.md" or rel.startswith(PERMISSION_DIRS) or bool(RENDERED.fullmatch(rel))


def citadel_git(*args):
    return subprocess.run(["git", "-C", CITADEL, *args], capture_output=True, text=True,
                          timeout=10).stdout


def cron_apply_refusal(command):
    """Why `jobs.py apply` may not run now, or None. Apply pushes citadel's workflows/ to the
    cron server, so it must be citadel's own jobs.py, run by a citadel session whose checkout is
    main == origin/main with a clean permission surface: then only merged content can reach it."""
    if realm != "citadel":
        return "only a citadel session may apply cron jobs"
    script = re.search(r"(\S*jobs\.py)\s+apply\b", command).group(1).strip("'\"")
    if not script.startswith("/") and re.search(r"(^|[\s;&|(])(cd|pushd)\s", command):
        return "after cd, name citadel's jobs.py by its absolute path"
    resolved = os.path.realpath(os.path.join(cwd, os.path.expanduser(script)))
    if resolved != f"{CITADEL}/scripts/jobs.py":
        return "only citadel's scripts/jobs.py may apply"
    try:
        branch = citadel_git("symbolic-ref", "--short", "HEAD").strip()
        head = citadel_git("rev-parse", "HEAD").strip()
        tracking = citadel_git("rev-parse", "refs/remotes/origin/main").strip()
        status = citadel_git("status", "--porcelain=v1", "--untracked-files=all", "-z")
    except Exception as e:
        return f"cannot inspect the citadel checkout ({e})"
    if branch != "main":
        return "the citadel checkout is not on main"
    if not head or head != tracking:
        return "citadel main differs from origin/main; pull first"
    dirty = [e[3:] for e in status.split("\0") if len(e) > 3 and on_permission_surface(e[3:])]
    if dirty:
        return f"uncommitted permission-surface files: {', '.join(dirty[:5])}"
    return None


realm = realm_of(cwd)  # None outside the workspace; 'citadel' for operator sessions

# ── git ────────────────────────────────────────────────────────────────────────
GIT = r"\bgit\b(?:\s+-C\s+\S+)?[^|;&]*?"
if re.search(GIT + r"\bpush\b[^|;&]*(\s--force\b|\s--force-with-lease\b|\s-f\b|\s\+\S)", flat):
    block("force push is forbidden")
# explicit refspec whose destination is main
if re.search(GIT + r"\bpush\b(?:\s+-\S+)*(?:\s+\S+)?\s+\+?(?:\S+:)?(?:refs/heads/)?main(?:\s|$)", flat):
    block("pushing to main is forbidden; open a PR")
# bare push (no refspec, or HEAD) while the checked-out branch is main
pm = re.search(GIT + r"\bpush\b(.*?)(?:$|[|;&])", flat)
if pm:
    toks = [t for t in pm.group(1).split() if not t.startswith("-")]
    dest = toks[1] if len(toks) > 1 else "HEAD"
    if dest == "HEAD" or ":" not in dest and dest == "":
        branch = "main"  # fail closed
        try:
            branch = subprocess.run(["git", "-C", cwd, "symbolic-ref", "--short", "HEAD"],
                                    capture_output=True, text=True, timeout=10).stdout.strip() or "main"
        except Exception:
            pass
        if branch == "main":
            block("pushing the checked-out main is forbidden; work on a branch and open a PR")
if re.search(GIT + r"\badd\b[^|;&]*(\s-A\b|\s--all\b|\s\.(\s|$))", flat):
    block("git add -A / . is forbidden; add explicit paths")
if re.search(GIT + r"\breset\b[^|;&]*--hard", flat):
    block("git reset --hard is forbidden")
if re.search(GIT + r"\bclean\b[^|;&]*\s-[a-zA-Z]*f", flat):
    block("git clean -f is forbidden")
if re.search(GIT + r"\b(filter-branch|filter-repo)\b", flat):
    block("history rewriting is forbidden")
if re.search(GIT + r"\bbranch\b[^|;&]*\s-[dD]\b[^|;&]*\b(wip|plan)/", flat) or re.search(GIT + r"\bpush\b[^|;&]*(--delete[^|;&]*\b(wip|plan)/|\s:(wip|plan)/)", flat):
    block("wip/* and plan/* branches are never deleted by the AI")

# ── destructive rm ────────────────────────────────────────────────────────────
for target in re.findall(r"\brm\b[^|;&]*\s-[a-zA-Z]*[rR][a-zA-Z]*\s+((?:\S+\s*)+)", flat):
    for tok in target.split():
        if tok.startswith("-"):
            continue
        t = os.path.expanduser(tok.replace("$HOME", HOME)).rstrip("/") or "/"
        t = os.path.realpath(t if t.startswith("/") else os.path.join(cwd, t))
        if t in ("/", HOME, CODESPACE) or (t.startswith(CODESPACE + "/") and t.count("/") == CODESPACE.count("/") + 1):
            block("refusing to remove a workspace or repository root")

# ── shell writes outside the session's territory (realm sessions only) ────────
if realm and realm != "citadel":
    own = f"{CITADEL}/realms/{realm}/"
    if re.search(r"(>>?|\btee\b|\bsed\s+-i|\bcp\b|\bmv\b|\binstall\b|\btruncate\b|\bdd\b)", flat):
        for tok in flat.split():
            t = tok.strip("'\"")
            if "/" not in t and not t.startswith("~") and "." not in t:
                continue
            if t.startswith("-"):
                continue
            path = t if t.startswith("/") or t.startswith("~") else os.path.join(cwd, t)
            path = os.path.realpath(os.path.expanduser(path.replace("$HOME", HOME)))
            if path.startswith(CITADEL + "/") and not path.startswith(own):
                block(f"realm session for '{realm}' may only write citadel/realms/{realm}/")
            other = realm_of(path)
            if other and other not in (realm, "citadel") and not path.startswith("/private/tmp"):
                block(f"realm session for '{realm}' may not write into another repository")
            rel = os.path.relpath(path, f"{CODESPACE}/{realm}")
            if not rel.startswith("..") and rel.split("/")[0] in ("CLAUDE.md", "CLAUDE.local.md", ".claude"):
                block("realm repos carry no AI files")
# ── cron server: only OWNER-merged citadel main reaches it ────────────────────
if re.search(r"\bjobs\.py\s+prune\b", flat):
    block("jobs.py prune is an operator action, not a session action")
if re.search(r"\bjobs\.py\s+apply\b", flat):
    refusal = cron_apply_refusal(flat)
    if refusal:
        block(f"jobs.py apply refused: {refusal}")
if re.search(r":3000/jobs\b", flat):
    block("the cron server is reached only through citadel's scripts/jobs.py")

# ── gh pr merge, any form ─────────────────────────────────────────────────────
if re.search(r"\bgh\s+pr\s+merge\b", flat):
    tail = flat.split("pr merge", 1)[1]
    repo_m = re.search(r"(?:-R|--repo)\s+(\S+)", tail)
    toks = [t for t in tail.split() if not t.startswith("-") and (not repo_m or t != repo_m.group(1))]
    selector = toks[0] if toks else None
    fields = "labels,isDraft,isCrossRepository,author,number,url,files,changedFiles"
    args = ["gh", "pr", "view"] + ([selector] if selector else []) + ["--json", fields]
    if repo_m:
        args += ["-R", repo_m.group(1)]
    try:
        out = subprocess.run(args, capture_output=True, text=True, timeout=25, cwd=cwd).stdout
        info = json.loads(out or "{}")
    except Exception as e:
        block(f"cannot inspect PR ({e})")
    if not info.get("number"):
        block("cannot identify the PR to merge")
    labels = {l["name"] for l in info.get("labels", [])}
    bad = labels & {"plan", "hold", "needs-human", "wip", "grant"}
    if bad or info.get("isDraft") or info.get("isCrossRepository"):
        block(f"PR #{info['number']} is {sorted(bad) or 'draft/fork'}; only the human merges it")
    if (info.get("author") or {}).get("login") != "yusa-imit":
        block("PR author is not the kingdom account")
    if "/yusa-imit/citadel/pull/" in (info.get("url") or ""):
        paths = [f.get("path", "") for f in info.get("files") or []]
        if len(paths) < (info.get("changedFiles") or 0):
            block(f"PR #{info['number']}'s file list is truncated; cannot rule out a grant")
        touched = [p for p in paths if on_permission_surface(p)]
        if touched:
            block(f"PR #{info['number']} changes the permission surface ({', '.join(touched[:3])});"
                  " it is a `grant` PR and only the human merges it (protocol/GITHUB.md)")
sys.exit(0)
