#!/bin/sh
set -eu
cd "$(dirname "$0")"
PYTHON=${PYTHON:-python}
"$PYTHON" -B -c 'import sys; assert sys.version_info >= (3,12), "Use Python 3.12 or later"'
mkdir -p reproduction-output logs
"$PYTHON" -B verify_c44_exact.py certificates/c44_candidate.json > reproduction-output/c44_exact.log
cat reproduction-output/c44_exact.log
"$PYTHON" -B independent/verify_c44_fraction.py certificates/c44_candidate.json > reproduction-output/c44_fraction.log
cat reproduction-output/c44_fraction.log
"$PYTHON" -B reproduce_c44.py > reproduction-output/c44_baseline.log
cat reproduction-output/c44_baseline.log
