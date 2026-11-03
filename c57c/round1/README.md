# Candidate, unrefereed C57c lower bound

This packet supports the candidate statement

    U >= 6123/10000 = 0.61230.

Complete verification is recorded in verification.json: complete
global coverage and every arithmetic range. A partial receipt proves no
constant bound. The gain over Wikström's arXiv lower bound 0.612242 is exactly
29/500000 = 0.000058 (+5.8e-5). The gain over our own earlier
0.612294 candidate, which was never filed, is 3/500000 = 0.000006
(+6e-6). Frank Wikström's normalization, bounded-image transform,
Grunsky framework, equation-(9) center and equation-(12) phase congruence are credited in the proof.
No novelty judgment or independent human review is claimed.

The center adds a localized sixth-coefficient term. Higher Grunsky forms,
the exterior area theorem and Bloch derivative disks eliminate four higher
complex coefficients through a quadratic contradiction. The exact dyadic
forest covers the remaining four real parameters. PROOF.md collects the
analytic reductions; the component proof files give the same arguments.
The classical area/Grunsky theorems and ordinary complex analysis are
explicit mathematical inputs, not formalized by the arithmetic checker.

The separately written (same agent) checker imports no discovery/SDP code. Its
formal-series construction, sparse quadratic assembly, core derivatives
and strict Arb positivity test differ from discovery. Both implementations
were written by the same agent; this is not independent authorship.
All arithmetic replay uses python-flint Arb at192 bits. A floating
Cholesky factor only proposes an exactly checked dyadic congruence.

C57_FOREST_V2.json and its12 gzip parts are the mathematical artifact.
RANGE_PLAN.json records the exact disjoint replay ranges used here;
cert_receipts/ contains their actual complete receipts. Final aggregation
rechecks every global coverage edge, matching code/data hashes and exact
range coverage. Historical receipts are evidence of completed runs, not
trusted inputs for a fresh reviewer's proof check.

Use Python3 with python-flint. Set single-thread BLAS and nice10. From this
packet directory, a full fresh replay on a machine authorized for a long
run is:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export PYTHONDONTWRITEBYTECODE=1
nice -n 10 python verify_c57c_forest.py C57_FOREST_V2.json \
  --receipt fresh_complete_verification.json
nice -n 10 python check_c57_forest_controls.py C57_FOREST_V2.json
```

The complete sequential replay may take hours. On the Mini, use bounded
ranges instead, with at most four mathematical workers and no run over
thirty minutes. Create an unused replay directory:

```sh
python prepare_fresh_c57_replay.py replay01
nice -n 10 python run_limited.py --seconds 1740 \
  --log replay01/controller1.log -- python run_c57_arithmetic_queue.py \
  --queue replay01/QUEUE.json --seconds 1600
```

Repeat the bounded controller command as needed; use distinct controller
log names. Up to four such controllers may share the same fresh queue.
They lock the queue and claim disjoint jobs, cap each child and record its
actual verdict. No historical receipt is copied into replay01. A capped
range remains pending/unverified and must be rerun with enough remaining
epoch time or split into exact smaller ranges. Once every fresh job says
done, run:

```sh
nice -n 10 python aggregate_fresh_c57_replay.py replay01
nice -n 10 python check_c57_forest_controls.py C57_FOREST_V2.json
```

The result must say VERIFIED_CANDIDATE_UNREFEREED, with all489994 leaves.
Structure-only, selected-leaf or incomplete-queue checks do not establish
the bound. See the proof's finite-union argument for bounded replay.

The nine actual-artifact rejection controls cover missing/duplicate parts,
corrupt hashes, false parameters, an identically positive false exclusion,
negative weights, unsupported phase, invalid transform t and false
coefficient caps. Broader mixed easy-radius and chain-rule/congruence
controls are retained separately. The literal input artifact and code
hashes, not an optimizer log, define the result.

Release qualification: written and checked by AI agents under Ricardo Pinho's
direction; the Arb checker was separately written by the same agent.
Two AI reviews (Claude Opus 5.5 via Claude Science and GPT-6 Astra) found
no false mathematical step. Both returned FLAG for the limitations recorded
in review/. No human referee has reviewed this candidate. The release reruns
controls, global aggregation and selected ranges; it is not a full fresh
arithmetic replay. Historical cert_receipts/ remain unchanged.
