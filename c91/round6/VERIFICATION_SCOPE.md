# Release verification scope

**Whole bound: L0; finite component: L1.** Canonical survival, the universal
frontier invariant, typicality, complement lifting, first moment and limit
arguments are proved only in prose in PROOF.md and sources/ROUND5_PROOF.md.
The finite packet checks the 59,550-word bank, the complete 121,332,798-row
representative graph with 499,034,690 edges, 32,774,059 potential classes,
the exact integer recipe and every strict dyadic-majorant row inequality,
plus the positive rational exponent at 265988/1000000. The 242,665,595-state
lift uses checked complement symmetry rather than separate enumeration.

Producer: `gpt-6.1-sol`; independently written checker: `gpt-6-astra`.
See verification/PROVENANCE.md for model-selection evidence, original
generic author label and explicitly normalized receipts. An AI review
and a producer replay are distinct from this different-model implementation.

The following is the original producer-only implementation scope. Its
same-agent wording describes the producer verifier, not the independent
implementation in verification/.

---

# Verification scope and provenance

All results are candidate and unrefereed. No novelty judgment is made.
The verifier is separately written (same agent). This describes separation
from the numerical search, without claiming separate-party authorship.

Inherited without mathematical changes from round 5: the eight-feature
C++ exact arithmetic, forward whole-operation canonical-key DP, explicit
suffix matcher reconstruction, run-memory encoding, completed-score
frontier reconstruction, bit-complement involution, deterministic partition
reconstruction and exhaustive strict integer row tests. These are different
implementations from the search's backward scalar DP, Aho–Corasick matcher,
relative-score frontier, hash-based minimizer and floating numerical kernel.
The eight-feature family and its general typicality argument also appeared
in rounds 3/5 and are credited as inherited.

Round-6 verifier changes: enforce the .2645 frozen bar and lifted-state cap;
replace the explicit floating-vector codec with a finite exact integer
iteration recipe; add the exact necessary root-row test already present in round
5's four-feature checker. The root test for zero-step (constant) recipes runs only after every explicit
forbidden word passes exact DP. It rejects some corrupt positive potentials
early; successful certification still requires reconstruction and EVERY row.
No search graph, numerical matrix, generated state map or optimizer output
is an input to frozen verification.

Round-5's frozen artifact and its four-feature verifier are unchanged.
All 38 entries in its retained SHA256SUMS match, including the artifact,
checker, proof and completed replay/control receipts. As instructed, this
job does not repeat its complete exact replay. New round-6 artifacts must
pass their own complete replay and actual-artifact rejection controls.

Search-side probes, ARPACK output, potential quantization and bit clearing
are floating proposals only. Exact DP bank audits and small-pair survival
checks support the universal written invariant but do not replace its proof.
The frozen integer rows and exact/Arb logarithm enclosures are what establish
any final rational candidate bound.

The compact integer-iteration path additionally uses a new potential recipe
and exact dyadic majorants (coefficient ceilings found by bounded integer binary search). The search-side `power_search.cpp` reads the
numerical quotient and proposes a finite iteration count. The frozen C++
checker has a separately written reconstruction: it rebuilds the entire
model and its partitions, computes the coefficient ceilings from exact
rational parameters, reconstructs the integer vector, and checks every full
row against the majorant. It imports no search implementation. The proof
of one-sided rounding and all uint128 capacity limits are in PROOF.md.
This is still separately written (same agent), with the inherited parts
identified above; it is not a separate-party or formal referee report.
