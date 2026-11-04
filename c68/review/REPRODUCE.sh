#!/bin/sh
set -eu
review_python="${PY:-$HOME/dev/open-science/.venv/bin/python}"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
nice -n 10 "$review_python" -B audit_kernel.py
nice -n 10 "$review_python" -B check_moments.py
nice -n 10 "$review_python" -B check_scalar.py
nice -n 10 "$review_python" -B check_integrals.py
nice -n 10 "$review_python" -B check_retained.py
nice -n 10 "$review_python" -B attack_contacts.py
nice -n 10 "$review_python" -B attack_transfer.py
