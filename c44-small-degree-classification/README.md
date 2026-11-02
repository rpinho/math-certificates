# C44 < 2.0417086280: R4 = 22 and classification at small degree

Unrefereed. This certifies an upper bound on C44, the constant in r(f) <= C 2^deg(f), Tao table [44a](https://teorth.github.io/optimizationproblems/constants/44a.html), and the exact value R4 = 22 for the maximum number of relevant variables at degree 4. No human expert has reviewed it line by line. Please read it with suspicion.

    R4 = 22,  46 <= R5 <= 50,  94 <= R6 <= 109
    3/2 <= C44 <= 80880411492166173705437336107 / 39614081257132168796771975168 < 2.0417086280

It improves the 2.1974348818 in [c44-certificate/reed-muller-caps](https://github.com/rpinho/c44-certificate/tree/e44b9b0cc91c656a680854ce341927c5a7b337c4/reed-muller-caps), and rests on that argument, including its inequality (3).

## What's here

- `r4-exact/`: proof of R4 = 22 and R5 <= 53, using the published cubic classification.
- `round7/`: R5 <= 51, R6 <= 110, C44 < 2.0808959614, by a 52-case classification.
- `round8/`: R5 <= 50, R6 <= 109, C44 < 2.0417086280, by Boolean completion compatibility. `round8/PROOF.md` is the place to start. `INPUT_ERRATA.md` records a wording fix in round 7.
- `review/`: separate AI reviews of each step, and a blind review of the earlier argument.

Each folder is frozen with a manifest of hashes, and `inputs/` holds the exact earlier artifacts it uses. Compiled binaries are left out, so build the C++ sources first. Paths in old logs are from the rented machines.

## Reproduce

From `round8/`, run `verify_completion_a.py` and `verify_completion_b.py`, then the composition verifiers. They need only Python's standard library and a C++17 compiler.

## What this doesn't show

Every review here is AI. They reproduced the final rational with their own code and checked all 52 cases, and SAT attempts at counterexamples were inconclusive. Blind reviews of the earlier argument found no false step, with one putting it at about 0.8. None is a second party.

R3 = 10 and the Reed-Muller weight and lattice results are cited, not reproved. It may already be known. The lower bound stays at 3/2, since no 47-variable degree-5 function was found. No priority or optimality is claimed.

## Credit

Chiarelli, Hatami and Saks, Wellens, Kasami, Tokura and Azumi, Tarannikov and Kirienko, and Valyuzhenich. Details are in each `PRIOR_ART.md`.

## AI use

Analysis and proof drafting by AI agents under my direction; I reviewed the results at summary level. AI agents also prepared the certificates, verifiers and this text. This does not claim a line-by-line human verification.
