#!/usr/bin/env python3
"""Locked commit of one realm's memory onto citadel main: `citadel_commit.py <realm> <cycle-n>`.

The citadel checkout is shared by every realm session and by citadel's own cycles, so this helper
never commits in it, rebases it, stashes it, or switches its branch. Under an fcntl lock (macOS
has no flock binary) it takes the files under `realms/<realm>/{memory,STATE.md,REALM.md}` that
differ from the checkout's HEAD, lays them over a freshly fetched origin/main in a private index,
and pushes that commit to main — whatever branch the checkout is on and whatever other realms
left dirty or staged. Then it fast-forwards the checkout to origin/main if that cannot overwrite
anyone's edits, and says so when it cannot. A failed push leaves no local commit behind: the
edits stay in the working tree and the realm's next cycle carries them.
"""
import fcntl
import os
import re
import subprocess
import sys
import time

CITADEL = os.environ.get("KINGDOM_CITADEL", "/Users/fn/codespace/citadel")
REMOTE, MAIN = "origin", "main"
TRACKING = f"refs/remotes/{REMOTE}/{MAIN}"
PUSH_ATTEMPTS, RETRY_DELAY_S, LOCK_WAIT_S, LOCK_POLL_S = 3, 3, 180, 3
TRAILER = "Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
ENV = {k: v for k, v in os.environ.items() if k not in ("GIT_DIR", "GIT_WORK_TREE",
                                                          "GIT_INDEX_FILE")}


def git(*args, index=None, stdin=None, check=True):
    env = dict(ENV, GIT_INDEX_FILE=index) if index else ENV
    return subprocess.run(["git", "-C", CITADEL, *args], check=check, capture_output=True,
                          text=True, env=env, input=stdin)


def rev(name):
    """Object id of `name`, or None when it does not exist (e.g. a path absent from a tree)."""
    result = git("rev-parse", "-q", "--verify", name, check=False)
    return result.stdout.strip() or None


WARNED = set()


def warn(message):
    """Print each distinct warning once; /report relays them."""
    if message not in WARNED:
        WARNED.add(message)
        print(f"warning: {message}")


def parse_args(argv):
    usage = "usage: citadel_commit.py <realm> <cycle-n>"
    if len(argv) != 3:
        sys.exit(usage)
    realm, cycle = argv[1], argv[2]
    if not re.fullmatch(r"[a-z][a-z0-9_-]*", realm) or not re.fullmatch(r"[0-9]+", cycle):
        sys.exit(usage)
    if not os.path.isdir(os.path.join(CITADEL, "realms", realm)):
        sys.exit(f"unknown realm '{realm}': no citadel/realms/{realm}/")
    return realm, int(cycle)


def realm_changes(realm, base, index):
    """Paths under the realm's memory, STATE.md and REALM.md whose working-tree state differs
    from `base`: edited, added (unless ignored) and deleted files. Nothing else in the realm
    directory (settings.json, system.md are rendered) and nothing outside it is considered."""
    specs = [f"realms/{realm}/memory", f"realms/{realm}/STATE.md", f"realms/{realm}/REALM.md"]
    git("read-tree", base, index=index)
    listed = git("ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", *specs,
                 index=index).stdout
    if not listed:
        return []
    git("update-index", "--add", "--remove", "-z", "--stdin", index=index, stdin=listed)
    changed = git("diff", "--cached", "--name-only", "-z", "--no-renames", base, "--", *specs,
                  index=index).stdout.split("\0")
    changed = [path for path in changed if path]
    assert all(path.startswith(f"realms/{realm}/") for path in changed), changed
    return changed


def build_commit(changed, tip, message, index):
    """A commit whose parent is `tip` and whose tree is `tip` with `changed` taken from the
    working tree; None when that tree is `tip`'s own (the edits are already on main)."""
    assert changed, "build_commit needs at least one changed path"
    git("read-tree", tip, index=index)
    git("update-index", "--add", "--remove", "-z", "--stdin", index=index,
        stdin="\0".join(changed) + "\0")
    tree = git("write-tree", index=index).stdout.strip()
    if tree == rev(f"{tip}^{{tree}}"):
        return None
    commit = git("commit-tree", tree, "-p", tip, "-m", message).stdout.strip()
    assert rev(f"{commit}^") == tip, (commit, tip)
    return commit


def stage_paths_already_like(tip, head):
    """Stage every path main changed since `head` whose working-tree copy already equals `tip`'s
    (typically a realm's own memory this helper pushed), so the fast-forward keeps it."""
    paths = git("diff", "--name-only", "-z", "--no-renames", head, tip).stdout.split("\0")
    same = []
    for path in [p for p in paths if p]:
        on_disk = os.path.lexists(os.path.join(CITADEL, path))
        blob = git("hash-object", "--", path).stdout.strip() if on_disk else None
        if blob == rev(f"{tip}:{path}"):
            same.append(path)
    if same:
        git("update-index", "--add", "--remove", "-z", "--stdin", stdin="\0".join(same) + "\0")


def sync_checkout():
    """Fast-forward the shared checkout to origin/main when it is on main, strictly behind,
    and no local edit would be overwritten. Otherwise leave it exactly as it is and warn."""
    ref = git("symbolic-ref", "-q", "HEAD", check=False).stdout.strip()
    if ref != f"refs/heads/{MAIN}":
        where = ref.replace("refs/heads/", "branch ", 1) if ref else "a detached HEAD"
        warn(f"citadel checkout is on {where}, not main; memory goes to origin/main, "
             "checkout left alone")
        return
    head, tip = rev("HEAD"), rev(TRACKING)
    assert head and tip, (head, tip)
    if head == tip:
        return
    if git("merge-base", "--is-ancestor", head, tip, check=False).returncode != 0:
        warn("local main has commits that are not on origin/main; checkout left alone")
        return
    try:
        stage_paths_already_like(tip, head)
        merged = git("merge", "--ff-only", "-q", tip, check=False)
    except subprocess.CalledProcessError as error:
        warn(f"could not prepare the fast-forward: {error.stderr.strip()[:300]}")
        return
    if merged.returncode != 0:
        warn("fast-forward of the checkout refused (local edits to files main changed); "
             f"checkout left alone:\n{merged.stderr.strip()[:400]}")


def fetch():
    return git("fetch", "-q", REMOTE, MAIN, check=False).returncode == 0


def push(realm, cycle, index):
    """Returns the process exit status: 0 pushed or nothing to commit, 1 gave up."""
    message = f"chore({realm}): cycle {cycle} memory\n\n{TRAILER}\n"
    if not fetch():
        warn("fetch failed; building on the last known origin/main")
    sync_checkout()
    base = rev("HEAD")
    assert base, "citadel checkout has no HEAD"
    changed = realm_changes(realm, base, index)
    if not changed:
        print("nothing to commit")
        return 0
    error = ""
    for attempt in range(PUSH_ATTEMPTS):
        if attempt:
            time.sleep(RETRY_DELAY_S * attempt)
            fetch()
        tip = rev(TRACKING)
        assert tip, f"no {TRACKING}; fetch the citadel remote first"
        clobbered = [path for path in changed if rev(f"{base}:{path}") != rev(f"{tip}:{path}")]
        if clobbered:
            warn(f"main also changed {', '.join(clobbered)}; this cycle's copy replaces it")
        commit = build_commit(changed, tip, message, index)
        if commit is None:
            print("nothing to commit (already on main)")
            return 0
        pushed = git("push", "-q", REMOTE, f"{commit}:refs/heads/{MAIN}", check=False)
        if pushed.returncode == 0:
            fetch()
            sync_checkout()
            print(f"pushed {commit[:10]} to {REMOTE}/{MAIN}")
            return 0
        error = pushed.stderr.strip()[:300]
    print(f"citadel push failed after {PUSH_ATTEMPTS} attempts ({error}); nothing was "
          "committed locally, the edits stay in the working tree for the next cycle",
          file=sys.stderr)
    return 1


def acquire(lock):
    """Take the kingdom lock that serializes realm cycles, waiting at most LOCK_WAIT_S."""
    for _ in range(LOCK_WAIT_S // LOCK_POLL_S):
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return
        except BlockingIOError:
            time.sleep(LOCK_POLL_S)
    sys.exit(f"citadel lock busy for {LOCK_WAIT_S} s; retry next cycle")


def main():
    realm, cycle = parse_args(sys.argv)
    git_dir = git("rev-parse", "--absolute-git-dir").stdout.strip()
    index = os.path.join(git_dir, f"kingdom-{realm}.index")
    with open(os.path.join(git_dir, "kingdom.lock"), "w") as lock:
        acquire(lock)
        try:
            return push(realm, cycle, index)
        finally:
            if os.path.exists(index):
                os.remove(index)


if __name__ == "__main__":
    sys.exit(main())
