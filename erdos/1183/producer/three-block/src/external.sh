#!/bin/sh
set -eu
lean_bin="${LEAN:-lean}"
"$lean_bin" --version
for category in face split23 split22; do
  start=$(date +%s)
  for f in data/"$category"/*.cnf; do
    echo "$f"
    "$lean_bin" --run src/CheckLRAT.lean "$f" "${f%.cnf}.lrat"
  done
  end=$(date +%s)
  echo "Elapsed seconds for $category: $((end-start))"
done
