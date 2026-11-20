#!/bin/sh
# Run inside the job directory with src/offline and nice 10.
set -eu
py="${PYTHON:-python3}"
mkdir -p build/tmp data/face data/split23 data/split22
export PYTHONDONTWRITEBYTECODE=1
for script in planes three plane_sat; do
  "$py" "src/$script.py"
done
"$py" src/roots.py 23
"$py" src/roots.py 22
