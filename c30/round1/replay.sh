#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
TASK_PYTHON="${TASK_PYTHON:-python3}"
export PYTHONDONTWRITEBYTECODE=1
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
nice -n 10 "$TASK_PYTHON" -B verify_baseline.py artifacts/baseline_certificate.json
nice -n 10 "$TASK_PYTHON" -B rejection_controls.py
nice -n 10 "$TASK_PYTHON" -B verify_ordering.py
nice -n 10 "$TASK_PYTHON" -B verify_v2_scaling.py
nice -n 10 "$TASK_PYTHON" -B verify_reduced_obstruction.py
nice -n 10 "$TASK_PYTHON" -B check_tower_counts.py evidence/reviews/astra/brute14.jsonl
nice -n 10 "$TASK_PYTHON" -B verify_mean_two_leaf.py
nice -n 10 "$TASK_PYTHON" -B verify_candidate.py artifacts/candidate_certificate.json
nice -n 10 "$TASK_PYTHON" -B candidate_rejection_controls.py
