#!/bin/bash
set -eu
# The comparator and exporter import Lean's standard library and each other only.
for target in @lean4export/+Export:o @lean4export/+Export.Parse:o @Comparator/+Comparator.Util:o @Comparator/+Comparator.Axioms:o @Comparator/+Comparator.Compare:o @Comparator/+Comparator:o; do
  lake build "$target"
done
lake build lean4export comparator
lake exe comparator ComparatorChallenges/LeanShadow.json
