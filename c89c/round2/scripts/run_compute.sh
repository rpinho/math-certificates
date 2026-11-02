#!/bin/sh
set -eu
cd /root/os/math_c89cr2_1101
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 RAYON_NUM_THREADS=1
ulimit -v "${MATH_MEMORY_KB:-7500000}"
printf '%s %s\n' "$$" "$*" >> receipts/launched_pids.log
exec nice -n 10 "$@"
