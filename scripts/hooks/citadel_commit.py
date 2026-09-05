#!/usr/bin/env python3
"""Locked commit of one realm's memory into citadel: `citadel_commit.py <realm> <cycle-n>`.

Serializes concurrent realm cycles with an fcntl lock (macOS has no flock binary), stages only
that realm's directory, rebases with autostash, pushes, retries three times.
"""
import fcntl
import subprocess
import sys
import time

CITADEL = "/Users/fn/codespace/citadel"
realm, n = sys.argv[1], sys.argv[2]
paths = [f"realms/{realm}/memory", f"realms/{realm}/STATE.md", f"realms/{realm}/REALM.md"]

def git(*args, check=True):
    return subprocess.run(["git", "-C", CITADEL, *args], check=check, capture_output=True, text=True)

with open(f"{CITADEL}/.git/kingdom.lock", "w") as lock:
    deadline = time.time() + 180
    while True:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB); break
        except BlockingIOError:
            if time.time() > deadline: sys.exit("citadel lock busy for 180 s; retry next cycle")
            time.sleep(3)
    git("add", "--", *[p for p in paths if (subprocess.run(["test", "-e", f"{CITADEL}/{p}"]).returncode == 0)])
    if git("diff", "--cached", "--quiet", check=False).returncode == 0:
        print("nothing to commit"); sys.exit(0)
    git("commit", "-q", "-m", f"chore({realm}): cycle {n} memory\n\nCo-Authored-By: Claude <noreply@anthropic.com>")
    for attempt in range(3):
        r = git("pull", "-q", "--rebase", "--autostash", check=False)
        if r.returncode != 0:
            git("rebase", "--abort", check=False); time.sleep(5); continue
        if git("push", "-q", check=False).returncode == 0:
            print("pushed"); sys.exit(0)
        time.sleep(5)
    sys.exit("citadel push failed after 3 attempts; the commit is local and will go next cycle")
