# C38 finite-strip candidate certificate

Candidate and unrefereed. Verifier: separately written (same agent).
No novelty judgment or separate authorship is claimed.

This packet is positive only when packet.json, FULL_ACCEPTANCE.json and
REJECTION_CONTROLS.json have all been produced after the complete
fresh native replays. Spans1..17 use full-width upper potentials; span18
uses the finite-last-span proof in PROOF_LAST_FINITE.md and makes no
infinite-width tail claim. Partially populated input/replay directories are
work in progress and do not establish a bound.

The mathematical coefficients are exact counts of the finite bridge
family specified in PROOF_FINITE_STRIP.md, with each span's transverse
cap in packet.json. The expanded integer vector is not materialized.
The certificate proves the required polynomial inequality by exact
rational lower enclosures of that finite family's generating value.
It does not pass the rational value endpoints off as integer coefficients.
The main packet does not depend on Numaro's enumeration as a premise.

Read PROOF_FINITE_STRIP.md, STATE_PROOF_APPENDIX.md, ARITHMETIC_PROOF.md, CREDITS.md and
PRIOR_ART_PUBLIC.md, together with PROOF_LAST_FINITE.md. Plánočka's adapted search source and its MIT license
are credited explicitly. The native verifier uses separately written
component identities and local degree constraints.

CORE_MANIFEST.json freezes the native verifier source and mathematical
core. Every span_manifest records a producer input frozen before its
fresh native replay. The final INPUT_MANIFEST.json binds all these
unchanged files once span18 arrives. The per-span replay receipts retain
their original pre-replay hashes and time ordering. Earlier pilots are
excluded from acceptance. The final union manifest is not claimed to
predate the earlier per-span replays. A further complete standard-runtime
replay of all eighteen spans starts after the whole union is frozen and
is recorded in FULL_ACCEPTANCE.json and complete_union_replay/.

For a fast exact hash/receipt/renewal check on Python3.11 or later:

```sh
nice -n 10 python3 verify_packet.py packet.json --receipt checked.json
```

For a complete new native recomputation on Linux with GCC/OpenMP:

```sh
export OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 OMP_NUM_THREADS=14 OMP_DYNAMIC=FALSE
mkdir -p ../c38-reproduce
nice -n 10 g++ -O3 -march=native -std=c++17 -fopenmp verify_strip.cpp -o ../c38-reproduce/verify_strip
nice -n 10 g++ -O3 -march=native -std=c++17 -fopenmp verify_finite_strip.cpp -o ../c38-reproduce/verify_finite_strip
nice -n 10 python3 verify_packet.py packet.json --full --binary ../c38-reproduce/verify_strip --finite-binary ../c38-reproduce/verify_finite_strip --work ../c38-reproduce/fresh --receipt ../c38-reproduce/verified.json
nice -n 10 python3 test_point_packet_controls.py packet.json ../c38-reproduce/rejections.json --binary ../c38-reproduce/verify_strip --finite-binary ../c38-reproduce/verify_finite_strip --scratch ../c38-reproduce/tmp_controls
```

The work directory must not already exist. Full mode regenerates every
state and edge and every prescribed column, compares every exact finite
numerator, and validates the tail potential and exact renewal inequality.
It can take substantial CPU time and RAM; recorded job measurements
are in the accompanying research report. Threads alter scheduling,
not accepted integer arithmetic.

The auxiliary replay_public data evaluate the same frozen inputs at
51082227/2^27. verify_span17_stop.py combines their exact upper sums
with those at51081913/2^27 by convex interpolation at400/1051. A
passing stop certificate rules out the span<=17-only renewal method
for this target, including arbitrary lengths and transverse ranges.
It is not an upper bound on the connective constant.
