#!/usr/bin/env bash
# All arithmetic and finite controls; no network, remote compute, or search.
set -euo pipefail
cd -- "$(dirname -- "$0")"
TASK_PYTHON="${TASK_PYTHON:-python3}"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export PYTHONDONTWRITEBYTECODE=1
"$TASK_PYTHON" -B check_manifest.py
shasum -a 256 -c SHA256SUMS
bash replay.sh
nice -n 10 "$TASK_PYTHON" -B check_value_word.py --max-n 9 --output artifacts/value_word_rerun.json
nice -n 10 "$TASK_PYTHON" -B check_profile_envelope.py
nice -n 10 "$TASK_PYTHON" -B evidence/reviews/astra/independent_exact_checks.py evidence/reviews/astra/brute14.jsonl
nice -n 10 "$TASK_PYTHON" -B evidence/reviews/astra/independent_algebra_checks.py
nice -n 10 "$TASK_PYTHON" -B evidence/reviews/astra/independent_pairing_check.py
nice -n 10 "$TASK_PYTHON" -B check_manifest.py
shasum -a 256 -c SHA256SUMS
