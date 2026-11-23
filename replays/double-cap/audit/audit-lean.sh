#!/bin/bash
set -eu
job=$(cd ../.. && pwd)
export LEAN_PATH="$job:$LEAN_PATH"
cd "$job"
exec lean -j2 "$@"
