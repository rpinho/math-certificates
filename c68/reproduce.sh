#!/bin/sh
set -eu
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1
if [ -z "${PYTHON:-}" ]; then
  if [ -x ../../.venv/bin/python ]; then PYTHON=../../.venv/bin/python; else PYTHON=python3; fi
fi
nice -n 10 "$PYTHON" verify_envelope_arb.py certificate-tight.json --out verification-tight-arb.json
nice -n 10 "$PYTHON" verify_envelope_rational.py certificate-tight.json --out verification-tight-rational.json
