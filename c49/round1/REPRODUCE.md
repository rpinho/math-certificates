# Reproduce the packet

Python's standard library suffices for the producer checker, controls and exact arithmetic. The referee finite checker needs a C++17 compiler. Search reconstruction uses our code only; OR-Tools is needed only to rerun optional optimization searches, not to verify this bound. All commands below run sequentially on one CPU. Start in the packet root.

Verify the sealed files first:

```sh
shasum -a 256 -c SHA256SUMS
```

Run the producer checker and its rejection controls. A scratch directory beside the packet keeps replay outputs outside the seal:

```sh
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
scratch="$(mktemp -d ../c49-replay.XXXXXX)"
scratch="$(cd "$scratch" && pwd)"
nice -n 10 python3 checker.py certificates/best_1.5678643845728069793620.json
nice -n 10 python3 controls.py certificates/best_1.5678643845728069793620.json --output "$scratch/controls.json"
```

Expected: ACCEPT, counts (33980,64728,64728,88867), exact comparison `above`; duplicate, Sperner, added-sunflower and raised-rate controls all reject, and 500 literal-definition comparisons match. The rounded-down claim is 1.5678643845.

Rebuild the baseline from Koshta's MIT data and mathematical description with our prepare.py. Apply the exact delta and compare every candidate mask. Then replay the referee's original parsing, data inspection, full-family checker and exact rates:

```sh
packet_root="$PWD"
mkdir -p "$scratch/certificates" "$scratch/sources" "$scratch/logs"
cp prepare.py "$scratch/"
cp sources/koshta_PROOF.md sources/two_pendant_extra_1.5678599.txt.xz "$scratch/sources/"
(cd "$scratch" && nice -n 10 python3 prepare.py)
nice -n 10 python3 checker.py "$scratch/certificates/baseline.json"
cp certificates/best_1.5678643845728069793620.json "$scratch/candidate.json"
cp certificates/best_delta.json "$scratch/claimed_delta.json"
cp sources/two_pendant_extra_1.5678599.txt.xz "$scratch/sources/baseline.txt.xz"
cp referee/*.py referee/*.cpp "$scratch/"
nice -n 10 clang++ -O3 -std=c++17 referee/independent.cpp -o "$scratch/independent"
(cd "$scratch" && nice -n 10 python3 prepare_data.py)
(cd "$scratch" && nice -n 10 python3 inspect_data.py)
nice -n 10 "$scratch/independent" "$scratch/baseline.masks" > "$scratch/logs/baseline_check.json"
nice -n 10 "$scratch/independent" "$scratch/candidate.masks" > "$scratch/logs/candidate_check.json"
(cd "$scratch" && nice -n 10 python3 exact_rates.py)
(cd "$scratch" && nice -n 10 python3 pendant_structure.py)
```

Expected: the baseline reconstructs exactly, including decompressed data digest `10ee18f93204468f3611d2c909a9eee443f3b4769cf7fddd964209edfebd4838`; both referee checks report `valid: true` and ordered containment and sunflower tuple counts equal to their member counts. Data inspection asserts the exact removed/added lists, both sixteen-member pendant additions and complete lifted fibers. Exact rates confirm the strict margin and safe printed lower bound. The staged candidate is the full supplied certificate; no optimizer is involved.

Optional historical referee controls and literal checks:

```sh
(cd "$scratch" && nice -n 10 python3 cross_checks.py)
nice -n 10 clang++ -O3 -std=c++17 referee/literal_region.cpp -o "$scratch/literal_region"
nice -n 10 "$scratch/independent" "$scratch/exceptions21.masks" literal
(cd "$scratch" && nice -n 10 ./literal_region baseline.masks exceptions21.masks)
```

The last command enumerates the original exceptional-region pivot triples and takes several minutes. Its original output is retained in referee/logs/. The fresh release replay reran the producer baseline/candidate checks and controls, the referee full baseline/candidate checker, exact rates and exact delta inspection; it did not rerun that optional historical literal scan.

The search sources and original logs document how the family was found. For optional optimizer reproduction use the producer report's commands from a working copy, set every `--threads` argument to `1`, and run only one solver process at once. Search outcomes may vary; only the supplied complete certificate fixes the claimed object. Optimization-exclusion claims in the historical reports are not part of the release's mathematical lower-bound claim.
