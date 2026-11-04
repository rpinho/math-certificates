# Candidate, unrefereed C91 >= 0.265988

Round 6 records **265988/1000000 = 0.265988**, updating PR #306's previous
claim 0.263561. This remains candidate and unrefereed; no priority or
optimality claim is made.

The canonical-alignment first moment builds on **Leandre Jack's #273**:
https://github.com/teorth/optimizationproblems/pull/273. Earlier canonical
counting includes Ganguly–Mossel–Rácz and Bilardi–Schimd; Lueker and inherited
local rounds 2–5 are also credited. Round 6 adds **4,000 longer exact-DP-verified
forbidden words** and uses **eight even Walsh input-correlation statistics**
on round 5's W=3, B=2, S=0, T=2 gap-debt frontier with a bit-complement
quotient. The bank has 59,550 words of actual lengths 8–16; 21 is only its cap.
The feature family appeared in earlier local rounds; parameter retuning
also contributed, so no numerical gain is assigned solely to one component.

**Verification level: L0** for the whole bound: the universal bridges are
proved only in prose. **Finite component: L1**: an independently written
different-model checker rechecked the exact certificate in full. See
VERIFICATION_SCOPE.md and verification/PROVENANCE.md. This does not assert
external human refereeing or a formal proof.

The independent replay checked 121,332,798 complete representative rows,
499,034,690 edges with multiplicity and 32,774,059 potential classes.
Complement lifting covers 242,665,595 states. Every strict integer majorant
row inequality passed; minimum slack is 4736028943110 over denominator 2^42.
The rational exponent at 0.265988 is strictly positive. Rounding upward to
0.265989 is unsafe. The full independent run took 2141.69722533226 seconds;
it is preserved as hashed evidence, rather than rerun during packaging.

The frozen gzip certificate is **222,538 bytes** (SHA256
`e6bcacb08bb36ee21e93f90a05160b6240260692390630c03049ac0ccd39f767`),
well below 90 MB and GitHub's 100 MB file ceiling. The potential is a finite
128-step exact integer recipe, not an assumed convergence assertion.

From this directory, verify the release hashes before running:

```sh
shasum -a 256 -c SHA256SUMS
PYTHON=python3 ./reproduce.sh controls
./reproduce.sh independent
PYTHON=python3 ./reproduce.sh producer
```

Controls and the producer replay need Python with python-flint==0.9.0,
C++17/OpenMP and assertions enabled. On macOS the producer launcher uses
Homebrew libomp; on Linux it uses GNU g++. The independent checker needs
only Python's standard library and GNU g++/OpenMP on Linux. All independent
checker writes use a disposable TMPDIR. Set PYTHON to a suitable environment
for controls/producer. Full replays need at least 40 GB available RAM; run
them separately. The script caps OpenMP at four workers and BLAS at one.
The preserved independent receipt used its own authorized 16-worker host.

The frozen controls include a bounded positive replay through all 59,550
bank checks, intentionally stopped at the declared checkpoint, plus five
specific corruption rejections. That positive run is not a full-row replay.
Thirteen regression tests reject false passes, ordering errors and execution
failures. See REPORT_CONTROLS.md for the historical repair, RELEASE_NOTES.md
for relocation/redaction, and logs/release_* for the release-copy runs.

Proof dependencies are PROOF.md and sources/ROUND5_PROOF.md. Verification
contains the two complete independent checker sources, exact stdout,
normalized and original receipts, execution timing and model evidence.
SHA256SUMS covers all payload files; MANIFEST lists file sizes and hashes.
Review status: Astra ACCEPT; CS review pending (placeholder).
