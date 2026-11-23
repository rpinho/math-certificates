#!/bin/bash
# Invoked inside the pinned Lake environment. Rebuild all audit imports from source.
set -eu
job=$(cd ../.. && pwd)
cd "$job"
out="$job/tmp/final-audit"
mkdir -p "$out"
export LEAN_PATH="$out:$LEAN_PATH"
for module in Spec NonVacuity BridgeChallenge Bridge Axioms Mutants; do
  echo "elaborating $module.lean"
  lean -j2 -o "$out/$module.olean" "$module.lean"
done
