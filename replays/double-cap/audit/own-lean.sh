#!/bin/bash
set -eu
source "$(dirname "$0")/env.sh"
cd "$M"
export LEAN_PATH="$JOB:$(lake env printenv LEAN_PATH)"
cd "$JOB"
exec nice -n 10 "$TC/lean" -j2 "$@"
