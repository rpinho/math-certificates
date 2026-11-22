#!/bin/sh
# Build the statement-audit files against this library. Run from c30/lean-m1 after `lake exe cache get && lake build`.
# usage: sh audit/build.sh            (builds Spec, Bridge, Mutants, Axioms in order)
set -e
mkdir -p audit/build
LP="$(lake env printenv LEAN_PATH):$(pwd)/audit/build"
for M in Spec Bridge Mutants Axioms; do
  lake env env LEAN_PATH="$LP" lean --root=audit -o "audit/build/$M.olean" "audit/$M.lean" > "audit/build/$M.log" 2>&1 || { echo "$M FAILED"; cat "audit/build/$M.log"; exit 1; }
  echo "$M ok"
done
grep -h "depends on axioms" audit/build/Axioms.log | sort | uniq -c
