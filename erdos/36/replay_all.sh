#!/bin/sh
# Replay everything in this packet. usage: sh replay_all.sh INPUTS_DIR [PYTHON] [OUT_DIR]
#   INPUTS_DIR  holds unktok/ and wetch/ fetched as in README.md section 4 (pinned commits)
#   PYTHON      interpreter with python-flint, numpy, scipy, mpmath (default: python3)
#   OUT_DIR     where logs and outputs go (default: replay_out); the packet itself is not modified
# Uses at most 4 worker processes, nice 10, about 5 minutes, about 250 MB per process.
set -e
IN=${1:?usage: sh replay_all.sh INPUTS_DIR [PYTHON] [OUT_DIR]}; PY=${2:-python3}; OUT=${3:-replay_out}
export E36_INPUTS="$IN" E36_CACHE="$OUT/cache" E36_VK="$OUT/vK_main.json"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
mkdir -p "$OUT/referee" "$OUT/ledger" "$OUT/cache"
CERT=certificates/certK_r105.json
$PY -c 'import sys,flint,numpy,scipy,mpmath;print(sys.version.split()[0],"python-flint",flint.__version__,"numpy",numpy.__version__,"scipy",scipy.__version__,"mpmath",mpmath.__version__)' | tee "$OUT/versions.txt"
$PY -I check_inputs.py "$IN" | tee "$OUT/check_inputs.log"
# 1. rigorous upper bound D_up on the integral of Phi_+ (writes producer/dint2/res_replay.json)
nice -n 10 $PY -I producer/dint2/dint2.py --out replay > "$OUT/dint2.log" 2>&1
mv producer/dint2/res_replay.json "$OUT/dint2_res.json"
# 2. producer's exact verifier, then its controls
V="nice -n 10 $PY -I producer/verify_K.py $CERT --dint2 $OUT/dint2_res.json"
$V --out "$OUT/vK_main.json" > "$OUT/vK_main.log" 2>&1
$V --raiseL 1e-6 --out "$OUT/ctrl_raiseL.json" > "$OUT/ctrl_raiseL.log" 2>&1
$V --flip 17 --out "$OUT/ctrl_flip.json" > "$OUT/ctrl_flip.log" 2>&1
$V --nocap 17 --out "$OUT/ctrl_nocap.json" > "$OUT/ctrl_nocap.log" 2>&1
$V --drop 17 --out "$OUT/ctrl_drop.json" > "$OUT/ctrl_drop.log" 2>&1
$V --N0shift=-1e-27 --out "$OUT/vK_N0shift.json" > "$OUT/vK_N0shift.log" 2>&1
# 3. referee's independent checker, controls and fixtures
nice -n 10 $PY -I referee/referee_check.py $CERT "$OUT/referee" > "$OUT/referee/replay.log" 2>&1
nice -n 10 $PY -I referee/referee_fixtures.py "$OUT/referee" > "$OUT/referee/fixtures.log" 2>&1
# 4. producer's N0 / C / paid-row / periodic-scatter ledger
for s in c_check n0_ledger assembly paid_rows ledger_arb scatter scatter_exact; do
  nice -n 10 $PY -I producer/ledger/$s.py > "$OUT/ledger/$s.log" 2>&1
done
# 5. search side (not needed to check): float caches, 16 step-function fixtures, and the search itself
nice -n 10 $PY -I producer/build_float_cache.py "$OUT/cache" > "$OUT/build_float_cache.log" 2>&1
nice -n 10 $PY -I producer/fixtures_K.py > "$OUT/fixtures_K.log" 2>&1
cp "$OUT/cache/fixtures_K.json" "$OUT/fixtures_K.json"
nice -n 10 $PY -I producer/make_K.py "$OUT/certK_search.json" 1.05 > "$OUT/make_K.log" 2>&1
# 6. compare with the shipped results
$PY -I compare_replay.py "$OUT" | tee "$OUT/compare_replay.log"
