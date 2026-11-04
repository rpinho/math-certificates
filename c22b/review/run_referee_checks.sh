#!/bin/sh
set -eu
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export PYTHONDONTWRITEBYTECODE=1
referee_python="${REFEREE_PYTHON:-$HOME/dev/open-science/.venv/bin/python}"
nice -n 10 "$referee_python" independent_geometry.py all > geometry_all.log
nice -n 10 "$referee_python" independent_topology.py > topology.log
nice -n 10 "$referee_python" independent_alexander.py > alexander.log
nice -n 10 "$referee_python" independent_audit.py > audit.log
nice -n 10 "$referee_python" independent_baseline.py > baseline.log
printf '%s\n' 'ALL_INDEPENDENT_REFEREE_CHECKS_PASS'
