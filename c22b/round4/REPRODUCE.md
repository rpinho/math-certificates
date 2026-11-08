# Reproduce round 4

Install this directory as c22b/round4/ alongside the existing c22b/round1/
in [math-certificates](https://github.com/rpinho/math-certificates).
The proof intentionally uses ../round1/PROOF.md; no unpublished round 3
file is required. Use a working copy: referee commands regenerate JSON
in their current directory, and indexes describe the archived outputs.

Python 3.12 with python-flint 0.9.0, numpy 2.5.4, scipy 1.18.1 and sympy
1.14.0 was used. For example, install those versions in a virtual environment
with `python -m pip install python-flint==0.9.0 numpy==2.5.4 scipy==1.18.1 sympy==1.14.0`.
The commands below use the activated environment's `python`.

From round4/:

```sh
export PYTHONDONTWRITEBYTECODE=1
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
shasum -a 256 -c SHA256SUMS
nice -n 10 python verify_result.py candidate_high
nice -n 10 python controls.py candidate_high
nice -n 10 python original/run_controls.py original
nice -n 10 python check_contact.py candidate_high
nice -n 10 python check_determinant.py candidate_high
```

Expected: CERTIFIED_CANDIDATE_C22B_UPPER_BOUND at 7.087559024; 21 specified
construction rejections; 108 original rejections; selected tangent-point
radius below 1.000001000; determinants 1327,2651,3975. Result verification
recomputes all 1006199 geometry leaves and the full physical projection.

From round4/referee/:

```sh
nice -n 10 python scalar.py
nice -n 10 python covers.py curvature
nice -n 10 python covers.py body
nice -n 10 python covers.py interfaces
nice -n 10 python covers.py lower
nice -n 10 python caps_contact.py
nice -n 10 python topology.py
```

Run scalar.py before interfaces; it supplies the speed bounds in scalar.json.
Expected: strictly positive complete-domain inequalities, body coefficient
below 7.087559024, cap length below 150, and body action [[1,0],[1324,1]]
with identity permutation and n=1 determinant 1327. All seven commands
use the referee's own formulas, not the producer's partitions.

The release helper outside this package ran up to four single-threaded
processes, effective nice 10. Logs, exit codes, elapsed times and versions
are in release_validation/summary.json. It saved fresh referee JSON in
release_validation/referee_outputs/ and restored source JSON afterward.
The source-time producer outputs in producer_logs/ are preserved.
These computations check finite statements; consult PROOF.md and
referee/REFEREE.md for the prose reductions to the all-n bound.
