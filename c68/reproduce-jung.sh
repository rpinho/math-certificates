#!/bin/sh
set -eu
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1
if [ -z "${PYTHON:-}" ]; then
 if [ -x ../../.venv/bin/python ]; then PYTHON=../../.venv/bin/python; else PYTHON=python3; fi
fi
nice -n 10 "$PYTHON" verify_jung_arb.py certificate-jung.json --out verification-jung-arb.json
nice -n 10 "$PYTHON" verify_jung_rational.py certificate-jung.json --out verification-jung-rational.json
