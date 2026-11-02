#!/bin/bash
set -eu
cd "$(dirname "$0")/.."
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
echo "SHELL_PID $$"
nice -n 10 python3 verify_caps.py cap_certificate.json > verification_caps.json
nice -n 10 python3 verify_spectral.py spectral_certificate_round3.json > verification_spectral.log 2>&1
nice -n 10 python3 verify_bound.py candidate.json > verification_row.log 2>&1
nice -n 10 python3 verify_column.py candidate.json > verification_column.log 2>&1
nice -n 10 python3 control_structure.py > control_structure.log 2>&1
nice -n 10 python3 control_rejections.py > control_rejections.log 2>&1
nice -n 10 python3 make_receipt.py > final_receipt.log 2>&1
date -u > reproduction.done
