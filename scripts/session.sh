#!/usr/bin/env bash
# Run one autonomous development cycle for a kingdom repo, exactly as the cron job would.
#   scripts/session.sh <job-name> [extra claude args...]
# Reads workflows/jobs.toml for cwd/model, workflows/prompts/<job>.md, workflows/system/<job>.md.
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
job="${1:?usage: session.sh <job-name>}"; shift || true
cwd=$(python3 - "$here" "$job" <<'PY'
import sys, pathlib; sys.path.insert(0, sys.argv[1] + "/scripts"); import jobs
j = jobs.toml_load((pathlib.Path(sys.argv[1]) / "workflows/jobs.toml").read_text())[sys.argv[2]]
print(j["cwd"]); print(j.get("model", "sonnet"))
PY
)
dir=$(echo "$cwd" | sed -n 1p); model=$(echo "$cwd" | sed -n 2p)
prompt="$here/workflows/prompts/$job.md"
sys="$here/workflows/system/$job.md"
args=(-p "$(cat "$prompt")" --model "$model" --permission-mode bypassPermissions)
[ -f "$sys" ] && args+=(--append-system-prompt "$(cat "$sys")")
echo ">> $job in $dir (model $model)"
cd "$dir" && exec claude "${args[@]}" "$@"
