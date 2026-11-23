#!/bin/bash
set -eu
source "$(dirname "$0")/env.sh"
seconds=$1
shift
export LEAN_SYSROOT="${TC%/bin}"
exec nice -n 10 python3 "$JOB/bounded.py" "$seconds" /usr/bin/python3 -I "$HOME/.local/share/research-harness/tools/third_party.py" run --workdir "$JOB" --url https://github.com/allenibiapina/LeanShadow --commit 19deb3ed555cc8404958c1804f9b29898a918d10 --timeout "$seconds" -- "$@"
