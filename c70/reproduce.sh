#!/bin/sh
set -eu
cd "$(dirname "$0")"
UV=${UV:-uv}
mkdir -p reproduction-output
"$UV" run -q --python 3.12 --with python-flint==0.9.0 --with mpmath==1.3.0 python -B verify_c70_arb.py certificates/c70_candidate.json > reproduction-output/c70_arb.log
cat reproduction-output/c70_arb.log
"$UV" run -q --python 3.12 --with python-flint==0.9.0 --with mpmath==1.3.0 python -B independent/verify_c70_rational.py certificates/c70_candidate.json > reproduction-output/c70_rational.log
cat reproduction-output/c70_rational.log
"$UV" run -q --python 3.12 --with python-flint==0.9.0 --with mpmath==1.3.0 python -B verify_c70_arb.py --baseline > reproduction-output/c70_arb_baseline.log
cat reproduction-output/c70_arb_baseline.log
