#!/usr/bin/env python3
"""Manage the kingdom's autonomous-development cron jobs from version-controlled files.

    scripts/jobs.py render          # realms/<r>/settings.json + prompts/system for every realm job
    scripts/jobs.py export          # cron server → workflows/{jobs.toml, prompts/, system/}
    scripts/jobs.py plan            # show what apply would create/update (no changes)
    scripts/jobs.py apply [--yes]   # workflows/ → cron server (create, PATCH, pause/resume by job name)
    scripts/jobs.py prune [--yes]   # delete server-only jobs
    scripts/jobs.py argv <realm>    # the extraArgs a realm job must carry (also used by scripts/kingdom)

Job identity is the `name` field. Prompt = workflows/prompts/<name>.md, system prompt =
workflows/system/<name>.md (optional). Schedule/model/etc. live in workflows/jobs.toml.
Server: $CRON_SERVER_URL (default http://localhost:3000) — see ../cron.
"""
import json
import json as _json
import os
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
WF = ROOT / "workflows"
SERVER = os.environ.get("CRON_SERVER_URL", "http://localhost:3000")
FIELDS = ["expression", "cwd", "model", "permissionMode", "timeoutMs", "maxBudget",
          "allowedTools", "extraArgs", "sessionLimitThreshold", "dailyBudgetUsd", "blockTokenLimit"]
CITADEL = "/Users/fn/codespace/citadel"


def expected_extra_args(realm):
    """Single source of truth for realm-session flags (scripts/kingdom reads this via `argv`)."""
    return ["--add-dir", CITADEL,
            "--settings", f"{CITADEL}/realms/{realm}/settings.json",
            "--strict-mcp-config",
            "--permission-prompts", "none",
            "--effort", "high"]


def realms_from_toml():
    jobs = toml_load((WF / "jobs.toml").read_text())
    return [n[:-len("-cycle")] for n in jobs if n.endswith("-cycle") and n != "citadel-cycle"]


def http(method, path, body=None):
    req = urllib.request.Request(SERVER + path, method=method,
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(body).encode() if body is not None else None)
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read() or b"{}")


# ── minimal TOML (subset: [tables], key = "str" | int | bool | ["a","b"]) ─────
def toml_dump(jobs):
    out = ["# Kingdom cron jobs — one table per job. Prompts live in prompts/<name>.md.",
           "# Apply with: python3 scripts/jobs.py apply", ""]
    for j in jobs:
        out.append(f"[jobs.{j['name']}]")
        for k in FIELDS:
            v = j.get(k)
            if v is None:
                continue
            if isinstance(v, bool):
                out.append(f"{k} = {str(v).lower()}")
            elif isinstance(v, (int, float)):
                out.append(f"{k} = {v}")
            elif isinstance(v, list):
                out.append(f"{k} = [{', '.join(json.dumps(x) for x in v)}]")
            else:
                out.append(f"{k} = {json.dumps(v)}")
        out.append("")
    return "\n".join(out)


def toml_load(text):
    jobs, cur = {}, None
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip() if not line.strip().startswith('"') else line.strip()
        if not line:
            continue
        m = re.match(r"\[jobs\.([A-Za-z0-9_.-]+)\]", line)
        if m:
            cur = jobs.setdefault(m.group(1), {"name": m.group(1)})
            continue
        k, _, v = line.partition("=")
        k, v = k.strip(), v.strip()
        if v in ("true", "false"):
            cur[k] = v == "true"
        elif re.fullmatch(r"-?\d+", v):
            cur[k] = int(v)
        elif re.fullmatch(r"-?\d+\.\d+", v):
            cur[k] = float(v)
        elif v.startswith("["):
            cur[k] = json.loads(v)
        else:
            cur[k] = json.loads(v)
    return jobs


def local_jobs():
    jobs = toml_load((WF / "jobs.toml").read_text())
    for name, j in jobs.items():
        j.setdefault("enabled", True)
        if name.endswith("-cycle") and name != "citadel-cycle":
            realm = name[:-len("-cycle")]
            exp = expected_extra_args(realm)
            if j.get("extraArgs") != exp:
                sys.exit(f"{name}: extraArgs drift; expected {exp}")
            if not (ROOT / "realms" / realm / "settings.json").is_file():
                sys.exit(f"{name}: missing realms/{realm}/settings.json — run: jobs.py render")
            if j.get("maxBudget") is None:
                sys.exit(f"{name}: maxBudget is required for kingdom jobs")
        p = WF / "prompts" / f"{name}.md"
        if not p.exists():
            sys.exit(f"missing prompt file: {p}")
        j["prompt"] = p.read_text().rstrip("\n")
        s = WF / "system" / f"{name}.md"
        if s.exists():
            j["appendSystemPrompt"] = s.read_text().rstrip("\n")
    return jobs


def cmd_render():
    """Render per-realm settings from core/fleet-settings.json and the cycle prompt/system files.
    jobs.toml is hand-maintained; extraArgs there must match `scripts/kingdom argv <realm>`."""
    fleet = (ROOT / "core" / "fleet-settings.json").read_text()
    contract = (ROOT / "core" / "CONTRACT.md").read_text().rstrip("\n")
    # Rules are appended to the system prompt: .claude/rules of an --add-dir directory and of
    # ancestor directories do NOT load in realm sessions (probed 2026-09-06), so this is the only
    # channel that provably reaches every session.
    rules_dir = ROOT / "core" / "rules"
    order = ["00-kingdom.md", "git-github.md", "docs.md", "testing.md", "tiger-style.md", "zig-0.16.md"]
    rules = []
    for name in order:
        text = (rules_dir / name).read_text()
        if text.startswith("---"):  # strip paths: frontmatter
            text = text.split("---", 2)[2]
        rules.append(f"\n\n<!-- rule: core/rules/{name} -->\n" + text.strip())
    rules_blob = "".join(rules)
    (WF / "prompts").mkdir(exist_ok=True)
    (WF / "system").mkdir(exist_ok=True)
    realms = realms_from_toml()
    for r in realms:
        d = ROOT / "realms" / r
        d.mkdir(parents=True, exist_ok=True)
        (d / "settings.json").write_text(fleet.replace("{{REALM}}", r))
        (WF / "prompts" / f"{r}-cycle.md").write_text(f"/cycle {r}\n")
        system = contract.replace("the realm name is in the prompt", f"the realm is {r}") + "\n\nKINGDOM RULES (authoritative; the same text lives in citadel/core/rules/):" + rules_blob + "\n"
        (WF / "system" / f"{r}-cycle.md").write_text(system)
        (d / "system.md").write_text(system)
    (WF / "prompts" / "citadel-cycle.md").write_text((ROOT / "workflows" / "citadel-cycle.prompt.md").read_text())
    print(f"rendered settings + prompts for {len(realms)} realms")


def remote_jobs():
    return {j["name"]: j for j in http("GET", "/jobs")["jobs"]}


def cmd_export():
    remote = sorted(remote_jobs().values(), key=lambda j: j["id"])
    (WF / "prompts").mkdir(exist_ok=True)
    (WF / "system").mkdir(exist_ok=True)
    for j in remote:
        (WF / "prompts" / f"{j['name']}.md").write_text(j["prompt"].rstrip("\n") + "\n")
        if j.get("appendSystemPrompt"):
            (WF / "system" / f"{j['name']}.md").write_text(j["appendSystemPrompt"].rstrip("\n") + "\n")
    (WF / "jobs.toml").write_text(toml_dump(remote))
    print(f"exported {len(remote)} jobs → {WF}")


def diff(local, remote):
    changes = {}
    for k in FIELDS + ["prompt", "appendSystemPrompt"]:
        lv, rv = local.get(k), (remote or {}).get(k)
        if lv is None and k not in local:
            continue
        if lv != rv:
            changes[k] = (rv, lv)
    return changes


def cmd_plan(apply=False, yes=False):
    local, remote = local_jobs(), remote_jobs()
    plan = []
    for name, j in local.items():
        r = remote.get(name)
        ch = diff(j, r)
        if r is None:
            plan.append(("create", name, j, None))
        elif ch:
            plan.append(("update", name, j, r))
        if r is not None and bool(r.get("scheduled")) != bool(j.get("enabled", True)):
            plan.append(("resume" if j.get("enabled", True) else "pause", name, j, r))
    for name in remote:
        if name not in local:
            print(f"  ! {name}: on server but not in workflows/ — `jobs.py prune` deletes it")
    if not plan:
        print("no changes")
        return
    for op, name, j, r in plan:
        print(f"  {'+' if op == 'create' else '*'} {op:6} {name}")
        if r and op == "update":
            for k, (old, new) in diff(j, r).items():
                short = lambda v: (str(v)[:60] + "…") if len(str(v)) > 60 else v
                print(f"        {k}: {short(old)!r} → {short(new)!r}")
    if not apply:
        return
    if not yes:
        ans = input(f"apply {len(plan)} change(s) to {SERVER}? [y/N] ")
        if ans.strip().lower() != "y":
            print("aborted")
            return
    for op, name, j, r in plan:
        body = {k: j[k] for k in FIELDS + ["prompt", "appendSystemPrompt"] if k in j}
        if op == "create":
            body["name"] = name
            res = http("POST", "/jobs", body)
            print(f"  created {name} → id {res.get('id', res.get('job', {}).get('id', '?'))}")
        elif op == "update":
            http("PATCH", f"/jobs/{r['id']}", body)
            print(f"  updated {name} (id {r['id']})")
        else:
            http("POST", f"/jobs/{r['id']}/{op}")
            print(f"  {op}d {name} (id {r['id']})")
    # newly created jobs that are meant to be disabled
    remote = remote_jobs()
    for name, j in local.items():
        if not j.get("enabled", True) and name in remote and remote[name].get("scheduled"):
            http("POST", f"/jobs/{remote[name]['id']}/pause"); print(f"  paused {name}")


def cmd_prune(yes=False):
    local, remote = local_jobs(), remote_jobs()
    extra = [n for n in remote if n not in local]
    if not extra:
        print("nothing to prune"); return
    print("server-only jobs:", ", ".join(extra))
    if not yes and input("delete them? [y/N] ").strip().lower() != "y":
        print("aborted"); return
    for n in extra:
        http("DELETE", f"/jobs/{remote[n]['id']}"); print(f"  deleted {n}")


def cmd_argv(realm):
    print("\n".join(expected_extra_args(realm)))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "plan"
    if cmd == "render":
        cmd_render()
    elif cmd == "export":
        cmd_export()
    elif cmd == "plan":
        cmd_plan()
    elif cmd == "apply":
        cmd_plan(apply=True, yes="--yes" in sys.argv)
    elif cmd == "prune":
        cmd_prune(yes="--yes" in sys.argv)
    elif cmd == "argv":
        cmd_argv(sys.argv[2])
    else:
        sys.exit(__doc__)
