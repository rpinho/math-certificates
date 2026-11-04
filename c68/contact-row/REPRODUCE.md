# Reproduce the contact-row release

Candidate, unrefereed C68 >= 447/1000 = 0.447. These commands replay the
quantitative hypotheses; the Green/flux, contact geometry, outer-function
and final norm arguments are prose requiring mathematical review.

Python 3.12, python-flint 0.9.0 and mpmath 1.3.0 were used for the release.
python-flint is needed by the acceptance and retained/contact checks;
mpmath is needed only for the additional alternate arithmetic replay.
Install dependencies in your own environment if needed:

```sh
python -m venv .venv
.venv/bin/python -m pip install python-flint==0.9.0 mpmath==1.3.0
```

From the math-certificates repository root, enter the packet. Use your
Python executable as PY. Verify frozen hashes before rerunning, because
commands overwrite receipts and their timing fields.

```sh
cd c68/contact-row
shasum -a 256 -c SHA256SUMS
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
PY=${PY:-python3}
nice -n 10 "$PY" -B verify_measure.py certificates/certificate-0447.json --bits 320 --output logs/verification-final.json > logs/release-full.log
nice -n 10 "$PY" -B verify_controls.py > logs/release-controls.log
nice -n 10 "$PY" -B verify_retained.py > logs/release-retained.log
nice -n 10 "$PY" -B verify_auxiliary.py > logs/release-auxiliary.log
nice -n 10 "$PY" -B verify_contact_configurations.py > logs/release-contacts.log
```

Run commands sequentially: each is a single process at nice 10, with library
thread limits set to one. No network, search or optimizer is used. The full
checker imports verify_row.py and recomputes the entire parameter cover;
a separate cover-only invocation is unnecessary. All five commands must
exit zero and the five JSON receipts must have status PASS. The rejection
suite must report exactly 35 controls with each actual rejection code equal
to the expected code; an arbitrary exception is not counted as a pass.
Generated mutations under controls/ must match the packaged frozen controls.

The full receipt must bind certificate SHA-256
`d9dd308f94efb019368682367609d9fa71c9982bb7195b27da22bb80d02f4afe`
and cover SHA-256
`fda0aa1430313c3f896021073f3a44c3b1b920d2b07451d3b7d58d7d4d0bfc27`.
It checks ordinary k=1,...,5999, weighted k=1,...,1799, and the analytic
infinite tails starting at 6000 and 1800. The tree has 265 grid, 17 PSD,
four constant and one small leaf. Timing and final displayed interval
digits may vary with environment; every accepted inequality must stay strict.

Additional arithmetic implementations, also separately written by the same
AI agent, use direct mpmath.iv trigonometric ranges and an integer/5000-cell
moment calculation instead of the acceptance checker's Arb/Taylor and cubic
integral envelopes. They are not independent-party verification.

```sh
nice -n 10 "$PY" -B verify_alternate.py scalar certificates/row-cover.json --output logs/alternate-scalar.json > logs/release-alternate-scalar.log
nice -n 10 "$PY" -B verify_alternate.py measure certificates/certificate-0447.json --output logs/alternate-measure.json > logs/release-alternate-measure.log
```

Fresh release outcomes and environment are summarized in logs/release-checks.json.
Historical source receipts are under logs/source/ and are clearly separated
from the new Mini replays. The retained examples cover the false old .105
coefficient, the naive third diagonal, the false J=|m1| floor and the false
.13 coefficient, plus exact two- and three-contact geometric configurations.
They do not establish holomorphic annular interpolation.

MANIFEST.json hashes every payload file except itself and SHA256SUMS;
SHA256SUMS hashes every other file including MANIFEST.json. The historical
FROZEN_MANIFEST.json and BUNDLE_MANIFEST.json document source provenance,
not the release inventory. No certificate data or acceptance program was
changed during packaging; documentation reference edits are listed in the
release manifest.

**Verification level: L0** for the bound as a whole (definitions: https://github.com/rpinho/math-certificates/blob/59eeb7097f806da05187b5f234445be3589204d4/VERIFICATION_LEVELS.md)
The verifiers were separately written by the same AI agent; the new contact-row lemma is a prose argument needing mathematical review.
