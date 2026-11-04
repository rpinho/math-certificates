# Independent C91 round-6 checker

Producer author: `gpt-6.1-sol`. Checker author: `gpt-6-astra`, resolved from the executor-selection evidence;
the original session self-label was `gpt-6` (see PROVENANCE.md). This checker extends the expressly authorized earlier independent `../l1chk_d/C91/independent.py` and `independent.cpp` (and their round-4 ancestry). It does not import, read, copy, or adapt producer checker/search implementation files. Its new mathematics comes from round-6 PROOF.md and VERIFICATION_SCOPE.md and its format from the certificate itself. The requested frozen/summary.json is absent. REPORT.md was read for the explicitly authorized size/resource information.

Certificate SHA256: `e6bcacb08bb36ee21e93f90a05160b6240260692390630c03049ac0ccd39f767`.

The finite scope is exact reconstruction and checking of the explicit forbidden-word bank, its run-aware matcher and complement involution, the complete reachable frontier/matcher/history complement quotient, its weighted partition, the deterministic integer potential recipe, every strict majorant row inequality with multiplicity, and positivity of the rational logarithm enclosure at `265988/1000000`. Universal canonical-survival, typicality, first-moment, and analytic-limit bridges remain prose. The whole bound stays L0.

Implementation details:

- Exact dynamic programming compares `(edit cost, gap count, operation tuple)` for every forbidden word, requiring strict nonminimality. Words are decoded as base-eight column strings, with the earlier column most significant. The allowed length cap is 21; the actual bank contains 59,550 words of lengths 8–16. Duplicate words and absent complements are rejected.
- The inherited five-rule run memory and trie/failure matcher are intersected and minimized while preserving literal run memory. A paired labeled traversal constructs and checks the root-fixing complement involution, all edge conjugacies, and its square.
- The unchanged W=3, B=2, S=0, T=2 absolute-cap frontier retains relative cost/gap/order witness triples. Direct breadth-first traversal combines it with the minimized matcher and valid input histories. Normalization uses the latest X bit, or the latest Y bit when X is empty. All eight labeled edge slots and their multiplicities remain present.
- Eight Walsh supports `[3,5,9,15,17,23,27,29]` contribute only when their newest input bit is consumed and the required previous bits exist. Four-bit histories suppress unavailable initial windows. An exact canonical-DP audit covers all 16,129 pairs whose two lengths are each 0 through 6. It checks acceptance, the complement lift, emitted-feature equality, and direct spin products computed separately from the original complete input strings.
- Weighted partition refinement sorts the eight `(monomial, destination class)` entries, retaining multiplicity, and numbers classes by first appearance. The potential recipe uses the first complete row of each class. The final strict tests cover every original complete representative row, so acceptance does not depend on an untested representative-row equivalence premise.
- Python unbounded integers construct the clearing denominator and all 1,171,875 formal edge coefficients for eight exponents in `[-2,2]` and three column kinds. For each coefficient `c/D`, integer division computes `u=ceil(2^b*c/D)` and checks `(u-1)D < 2^b*c <= uD`. No floating arithmetic is used.
- C++ reconstructs the finite recipe `V_next = 1 + floor((2^b V + sum u V_destination)/2^(b+1))` starting at M for the specified number of iterations, then checks `sum u V_destination < 2^b V_source` on every row. Coefficients are positive and less than 2^48, b is at most 48, and each vector entry is checked to fit a positive uint64. Thus each product is below 2^112, eight-edge sums below 2^115, and augmented sums below 2^116; unsigned 128-bit arithmetic is sufficient. Vector overflow is rejected before narrowing. A zero-step recipe can fail an exact necessary root-row test after bank/matcher audits.
- The exponent uses 120 terms of the rational atanh series and a rigorous signed geometric tail bound for each logarithm. Exact rational lower/upper endpoints are written to stdout. No Arb or floating logarithm is needed.

Reproduce from the round-6 release root on Linux with Python 3 and GNU g++ supporting C++17/OpenMP:

```sh
nice -n 10 python3 verification/independent.py candidate_c91r6.json.gz
```

The checker is read-only with respect to its certificate/source directory. All intermediate files and compilation go to a disposable subdirectory of TMPDIR. No NumPy, producer modules, generated graph inputs, network access, or precomputed potential is required. `independent.py` and `independent.cpp` are the complete implementation and both are hashed in the L1 receipt. The compiler and Python standard library are dependencies. The large-run receipt avoids short read-only automatic replays; actual replay requires a Linux/OpenMP build environment.

The original execution supervisor and harvest scripts are operational
infrastructure, not checker implementation or reproduction dependencies, and
are omitted. The historical run used at most 16 OpenMP workers and sampled
16.856 GB peak process-group RSS. Plan at least 40 GB available RAM for a
full replay. The release command caps OpenMP at four workers for this job's
default resource policy; expect a different runtime. The original full replay
was authorized separately with 16 workers. Compilation and all writes use TMPDIR.

verification/check.json has the exact L1 schema, with paths relative to the
round-6 root. verification/levels_update.json supplies its finite evidence.
The two implementation files and check.stdout are byte-identical to the
original packet. See PROVENANCE.md for metadata normalization and source hashes.
