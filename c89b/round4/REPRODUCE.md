# Replay of the exact upper candidate

Candidate and unrefereed. Requirements: a C++17 compiler with unsigned __int128, GMP development headers/runtime, and Python >=3.10 standard library. Numerical search dependencies are not required for exact replay. Run from this package directory. Builds create local executables; executables are not shipped.

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
c++ -O3 -std=c++17 scripts/check_wide.cpp -lgmp -o check_wide
c++ -O3 -std=c++17 scripts/check_cayley_exact_r4.cpp -lgmp -o check_cayley_exact_r4
nice -n 10 python3 scripts/check_wide.py certificates/c5_cayley256_fine.json.gz 0.001648970526
nice -n 10 python3 scripts/check_cayley_matrix_r4.py certificates/c5_cayley256_fine.json.gz 0.001648970526
nice -n 10 python3 scripts/control_wide_cayley_r4.py
```

Both replays must return 15058298592194934908767847/9131939205947984819238469632. Their raw red/blue totals differ by exactly 256 because the second fixes the first part. The controls perform 36 literal comparisons and ten rejection checks. Both replay commands must fail if their final threshold is changed to .0016489.

The kernel can also be reconstructed without numerical search: expand the two disjoint masks H and F in PROOF.md, assign denominator-4041 numerators 4041,2648,0 respectively, and set every full-matrix entry to q[x XOR y]. The selected full matrix remains normative; exact replay does not import the numerical optimizer or its outputs. Acceptance receipts and hashes are under receipts/.

The optional exact density-polynomial replay is `nice -n 10 python3 scripts/cayley_probability_polynomial_r4.py`. It uses both compiled counters, seven probabilities and the explicit mask definition to reconstruct the formula in PROOF.md, and checks both retained upper fractions exactly.

On macOS with Homebrew GMP, add `-I/opt/homebrew/opt/gmp/include -L/opt/homebrew/opt/gmp/lib` to both compiler commands (adjust the prefix
for your installation). Both exact counters are separately written (same
agent), with no human referee. Python >= 3.10 is required.

Verify portable file integrity before building:

```sh
python3 scripts/check_manifest.py
shasum -a 256 -c SHA256SUMS
```

The exact rational comparison with `0.001648970526` is normative.
The historical `UNVERIFIED` generation label inside the byte-identical
certificate is superseded by the exact replay receipts. See CERTIFICATES.json.

The kernel JSON source_sha256 is historical generation metadata, not the
selected compressed-certificate hash. PROVENANCE.json and CERTIFICATES.json
identify the selected bytes; release_validation.json confirms that the kernel
and the two masks reconstruct every selected matrix entry exactly.
