# Clean-room replay of the supplied C82 certificate

**PASS — independently enclosed at 384 bits.** Completed 2026-11-04T23:37:36.587648+00:00.

    H = [0.252403463228463620015602513255947419238611832477773973947245156807963034311220407443823972998969083150676573621947 +/- 8.10e-115]
    J = [1.342726590035218036e-6 +/- 2.32e-25]
    B in [0.2524048059550536552336383477,
          0.2524048059550536552336387448]

The displayed endpoints are rounded outward from exact rational endpoints of the Arb ball. In particular, B < 0.252404806, so the mathematical reduction proves **C82 < 0.252404806**. This enclosure is strictly inside the producer's stated interval [0.2524048059550536501, 0.2524048059550536604]. The margin below the requested target is approximately 4.4946344766361e-11.

The certificate has D=999999999856 and weighted numerator degree 952533595715278899/1048576. All 78 numerator/denominator gcds and 15 denominator pairs passed. All 19 supplied factors were found irreducible over Q (irreducibility is extra information, not a required hypothesis). Certified roots account for 1644 composed roots with multiplicities, including exactly seven numerator circle roots and no denominator circle roots.

The half-domain tiling visited 11772 cells: 4667 geometric bisections, 1217 sign bisections, 748 accepted positive cells, 5098 accepted negative cells, and 42 unresolved crossing boxes with fully included integral error. The bound for the sum of those crossing contributions on the half-domain is [1.92836909499839011532194646404619857854815176544154895040280401996804370777261856281667166971441204310929030021046e-25 +/- 5.27e-139]. Every removed singular neighborhood had a strictly negative certified upper bound for g (approximately -4.7111, -0.4853, -4.1700, -0.5146 in increasing t order).

## Controls

| Control | Result |
|---|---|
| First denominator's constant coefficient changed from 1 to 0 | Rejected: common numerator/denominator factor |
| First denominator's leading coefficient changed from 1 to 2 | Rejected: nonmonic denominator |
| First numerator's exponent changed to D/1 | Rejected: degree condition |
| First numerator's exponent changed to -1/1 | Rejected: negative exponent |
| First denominator multiplicity changed to 0 | Rejected: nonpositive multiplicity |
| False target 0.25240480595 | Rejected: it is strictly below the certified lower endpoint of B |
| Root-factored g against exact-polynomial evaluation at three rational t values | Passed; intervals overlap and differences are bounded below 1e-25 |
| R=X+1, no numerator: B=log((1+sqrt(5))/2), J=0 | Passed |
| R=X+1, constant numerator 10, exponent 1: B=log(10), J>0 | Passed |
| R=X+10, numerator X, exponent 1/2: B=log(10), J=0 with a numerator log singularity | Passed |

Full numerical evidence and analytic-case enclosures are in `result.json`. The earlier full Taylor run also passed at 384 bits (`taylor-first.json`); the accepted run includes the final root diagnostics and all controls. No additional method search was performed.

## Reproduce

From the job directory, with python-flint installed in the shared environment:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
  nice -n 10 "$HOME/dev/open-science/.venv/bin/python" -u replay/check.py \
  --precision 384 --tol 1e-20 --controls --output replay/result.json
```

The checker uses one FLINT thread and makes no network calls. The accepted run took 452.66 seconds. A second single-threaded first-replay worker overlapped temporarily, staying within the two-core budget. The only dependencies are Python's standard library and python-flint 0.9.0.

## Comparison and provenance

The live [PR #280](https://github.com/teorth/optimizationproblems/pull/280) prints 0.2524177045*. The newly verified candidate B is lower by approximately **0.000012898544946344766361**. The earlier independently replayed value quoted in that PR, [0.2524177044473123, 0.2524177044473124], is also above this candidate. The #280 certificate was not an allowed input and was not locally reverified. See `../PRIOR_ART.md` and the local public-source snapshots for the live comparison.

The assistant's session instructions identify Codex based on GPT-6 but do not expose the exact serving-model identifier. `REPLAY.json` records that limitation rather than inventing an identifier. Different-model provenance relative to the producer cannot be independently established from the two supplied construction inputs. The clean-room attestations concern source access and code execution and are affirmative: no producer code was read or run.

The referee verdict is **HOLDS WITH CAVEATS**: the mathematical bound is verified; the caveats are the incorrect bibliographic title in the supplied proof and the limited model-identity provenance. The omitted extraction argument has been supplied in `../REFEREE.md`.


## Construction inputs and scope

The only construction inputs were `inputs/PROOF.md` and `inputs/certificates/certificate.json`, with SHA-256 hashes checked against `INPUTS_SHA256SUMS`. The proof and certificate are preserved unchanged. Public sources read were the live teorth 82a definition, #280/#301 bodies and comments through the specified gh client, the open-PR title index, Doche's published Bordeaux paper, and recent public literature. Sources outside the clean-room allowlist and linked producer/replayer code were not read or run. `N` and `numeric_unverified` are ignored.

`check.py` is independently written, self-contained Python, importing only the standard library and python-flint. It makes no network calls and imports no other local source. The first unsuccessful implementation is retained as `standard_first.py`; it too was independently written here. It is not the accepted checker.

## Exact algebra and certified roots

JSON coefficients must be integers (booleans are rejected). Denominator leading coefficients must equal 1, multiplicities must be strictly positive integers, and numerator exponents must be nonnegative exact rational strings. Weighted degrees use `fractions.Fraction`, never floats. All 78 numerator/denominator gcds and 15 denominator/denominator gcds are computed in Z[X]. FLINT factorization results are multiplied back exactly, with contents and multiplicities reported.

For each polynomial P the checker forms P(z(1-z)) exactly. The known cyclotomic factors Phi_1, Phi_6 and Phi_10 are divided out exactly from numerators, recording their roots at exact rational angles; these account for all unit-circle roots in this certificate. Every residual root is enclosed with FLINT's certified integer-polynomial complex-root routine, with multiplicities. The counts must equal the exact degree; isolating rectangles must be pairwise disjoint; every residual root's modulus must be strictly separated from 1. Any unhandled circle root or inadequate separation causes rejection. This is a checker for the present supported inputs, not a universal treatment of denominator circle roots.

Jensen's formula gives log M(P)=log|leading coefficient|+sum multiplicity*log(max(1,|root|)). Every operation is Arb ball arithmetic. All six composed denominators have no circle roots. Numerator leading coefficients, including the nonmonic factor with leading coefficient 2, are retained when computing g.

## Singularities and sign changes

Real coefficients imply g(1-t)=g(t), so the checker integrates on [0,1/2] and doubles the result. The numerator circle roots on that half interval occur at t=0, 1/10, 1/6, 3/10. Around each, a rational neighborhood of radius 2^-40 (clipped to the half interval) is considered. For z=e^(2 pi i t), interval distances to all roots give a one-sided upper bound for g: use upper distances for positive numerator weights and lower distances for negative denominator weights. Numerator logarithms are bounded above even when an interval contains their zero. Denominator lower distances must be positive. Every such neighborhood is discarded only after proving g<0 throughout it; its positive-part integral is therefore exactly zero. This handles the logarithmic singularities, rather than sampling past them.

Direct adaptive `acb.integral` applied to the positive part was tried first, with the analytic flag forwarded through logarithms and `real_max`. It exhausted its 100000-evaluation budget on the first interval and returned a nonfinite ball. This was rejected, with the failure recorded in STATUS.md before changing method. See `standard-first.log` and the archived first source.

The accepted method uses rigorous local Taylor models. On each rational cell [a,b], put m=(a+b)/2, h=(b-a)/2, x=(t-m)/h. At 384 bits, Arb formal series compute the first 40 coefficients of

    sum_P w_P Re log P(T(exp(2 pi i (m+h*x)))),

where w_P=q_i/D for numerators and -m_j/D for denominators. Evaluating P after T avoids the large coefficient growth of an expanded composed polynomial, without changing the function.

Here is the truncation proof. Set R=4h, z0=exp(2 pi i m), and let d>0 be a certified lower bound for the distance from z0 to every composed root. On the complex disk |t-m|<=R,

    |exp(2 pi i t)-z0| <= exp(2 pi R)-1 = delta.

Require delta<d/2. Then each root term admits a holomorphic logarithm of its ratio to its center value, and its modulus is at most -log(1-delta/d). If W=sum_P |w_P| deg(P∘T), the absolute value of the combined logarithmic variation is at most M=-W log(1-delta/d). Taking the holomorphic extension with real Taylor coefficients preserves this bound: average the analytic function and its conjugate-reflected function. Cauchy's coefficient estimate bounds the entire omitted degree >=40 tail on |x|<=1 by

    E = M*4^(-40)/(1-1/4).

All quantities in this inequality are themselves interval-enclosed. Cells failing the disk condition are bisected. Interval Horner evaluation on x in [-1,1], enlarged by [-E,E], encloses g on the whole cell. A strictly negative enclosure contributes zero. A strictly positive enclosure permits exact integration of the polynomial terms, plus a rigorous error [-2hE,2hE]. If the enclosure crosses zero, the cell is bisected or its complete positive-part integral is bounded by [0,(b-a)*max(0,g_upper)]. Thus no unobserved sign change can be dropped. The unresolved crossing contributions and Taylor remainders are included in the final interval; there is no empirical quadrature error estimate. The final interval width must also meet the requested tolerance.

## Interpretation

The exact reduction to the live essential minimum, including the infinitely-many-distinct-algebraic-numbers argument, is in REFEREE.md. The interval computation certifies B; it does not determine C82 or establish optimality. A failure to prove a numerical inequality is distinct from disproving the mathematical claim. The full trusted base is Python's integer/rational operations, python-flint 0.9.0 and its FLINT/Arb arithmetic and certified roots, plus the stated mathematical argument. This is not a proof-assistant formalization.

Did this replay find something new? No. It reproduces a supplied candidate. The live #280 comparison is a public printed bound, not a predictive score or a separately replayed local certificate. SBS is inapplicable.
