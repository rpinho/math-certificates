#!/bin/sh
set -eu
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export OMP_THREAD_LIMIT=4 PYTHONDONTWRITEBYTECODE=1
PYTHON=${PYTHON:-python3}
mkdir -p logs work
case "${1:-controls}" in
  controls)
    nice -n 10 "$PYTHON" -B -u frozen_candidate_controls.py candidate_c91r6.json.gz verify_orbit8.py release --timeout 600 > logs/release_suite.log 2>&1
    nice -n 10 "$PYTHON" -B test_frozen_candidate_controls.py -v > logs/release_selftest.log 2>&1
    nice -n 10 "$PYTHON" -B rational_exponent.py candidate_c91r6.json.gz logs/release_rational_exponent.json > logs/release_rational_exponent.log 2>&1
    ;;
  producer)
    nice -n 10 "$PYTHON" -B -u verify_orbit8.py candidate_c91r6.json.gz
    ;;
  independent)
    nice -n 10 python3 verification/independent.py candidate_c91r6.json.gz
    ;;
  *) echo 'usage: reproduce.sh [controls|producer|independent]' >&2; exit 2 ;;
esac
