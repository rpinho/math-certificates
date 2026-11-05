# Clean-room replay: PASS

The independent checker proves

    B in [0.251996488988201164531880087886,
          0.251996488988201164532207712015].

The upper endpoint is less than the exact rational target 0.2519964890. The enclosure is strictly contained in the interval supplied in CLAIM.md. The mathematical reduction from C82 to B is reviewed in `../REFEREE.md`; this report explains the numerical proof.

## Reproduction

From the job directory, with the supplied shared virtual environment available:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 nice -n 10 \
  ~/dev/open-science/.venv/bin/python replay/check.py \
  --prec 256 --controls --output replay/result.json
```

The default certificate path is resolved relative to check.py. A separate explicit false-target run is:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 nice -n 10 \
  ~/dev/open-science/.venv/bin/python replay/check.py \
  --prec 256 --target 0.2519964889 --output replay/false-target.json
```

The latter must print FAIL and exit 1. PASS for the actual target exits 0. These commands make no network requests and do not read any other local source code. `check.py` imports only standard-library modules and python-flint. Python 3.12.13, python-flint 0.9.0, FLINT 3.6.0 were used. FLINT threads are explicitly set to one. The final successful run's main calculation took 39 seconds, before its small analytic controls; the first run took 54 seconds. Elapsed time is diagnostic, not part of the proof.

## Exact algebra and Mahler measure

The coefficient arrays are checked for actual integer entries, nonempty arrays, and nonzero leading coefficients. Every denominator must be nonconstant and monic, with positive integer multiplicity. Each active numerator exponent is parsed as an exact Fraction, checked nonnegative, and cleared by the exact lcm 1048576. Leading coefficients of numerators contribute log|lead| and are never silently normalized away. Search-time decimal metadata is parsed as strings and ignored.

All 120 active numerator/denominator gcds are computed in Z[X] by FLINT and have degree zero. The strict degree inequality is exact:

    D = 1000000000064
    a = 58700834920208207/65536
    D-a = 6835165083986097/65536 > 0.

Composition with T=z-z^2 is exact in Z[z]. FLINT's certified complex root enclosures, with multiplicities counted, cover all 2126 roots of the 23 composed factors. Before isolation, exact division extracts all copies of Phi_1=z-1, Phi_6=z^2-z+1, and Phi_10=z^4-z^3+z^2-z+1. These account for the seven roots whose modulus is exactly one. Every other root is required to satisfy a strict Arb comparison |r|<1 or |r|>1. In this certificate the denominator has no unit-circle roots.

For each composed denominator p, Jensen gives

    log M(p) = log|lead(p)| + sum_{|r|>1} multiplicity(r) log|r|.

This yields

    H in [0.251992523252609459669852920685,
          0.251992523252609459669852920686].

The root enclosure, root counts and unit-circle decisions rely on the certified FLINT/Arb backend. They are not informal floating-point root approximations.

## Rigorous treatment of signs and singularities

After composition, express g as

    g(t) = C + sum_r w_r log|exp(2*pi*i*t)-r|,

where C includes all weighted leading-coefficient logarithms. Numerator weights are positive q_i/D times root multiplicities; denominator weights are negative -m_j/D times root multiplicities. All are enclosed from exact rational values. Real coefficients give g(1-t)=g(t), so the checker tiles [0,1/2] with exact rational dyadic intervals.

For an entire panel, rectangular Acb evaluation encloses z=exp(2*pi*i*t). Root distances then enclose every logarithm. With positive weight, an upper bound on the distance gives an upper bound on its logarithmic contribution, even if the panel contains a zero. With negative weight, a strictly positive distance lower bound is required. This provides a valid upper bound on g even at numerator singularities, where the limiting value is -infinity.

On panels avoiding all roots, a second bound uses the midpoint value and the mean-value theorem:

    g'(t) = Re(2*pi*i*z * sum_r w_r/(z-r)).

All terms are evaluated on the whole panel in Arb/Acb. If h is the half-width, g(midpoint) +/- h sup|g'| encloses the full range. Taking the tighter of two proved bounds preserves rigor.

A panel with upper(g)<=0 contributes exactly zero to max(0,g). A panel with lower(g)>0 is accepted for integration. Otherwise it is subdivided, unless its full possible contribution is already small enough for the local stopping criterion. In that case the checker records the interval

    [0, 2*(right-left)*max(0, upper(g))].

The factor 2 accounts for the reflected half circle. The local tolerance is just a stopping heuristic: every actual error bound is summed into J. There is no assumption that the count of panels makes a tolerance automatically valid. No singular neighborhood or unresolved crossing is discarded.

The final partition has 1960 negative leaves, 958 positive leaves (joined into 29 arcs), and 58 unresolved leaves. It took 5951 range evaluations, with maximum depth 41. Their summed unresolved-integral upper bound is less than 3.277e-22. This is already included in B and is much smaller than the margin to the printed target.

## Integration by dilogarithm antiderivatives

This replay uses an analytic primitive instead of sampled quadrature. For a single root r, write theta=2*pi*t. For |r|<=1,

    log|exp(i*theta)-r| = log|1-r*exp(-i*theta)|,
    primitive in theta = Im Li_2(r*exp(-i*theta)).

For |r|>1,

    log|exp(i*theta)-r| = log|r| + log|1-exp(i*theta)/r|,
    primitive in theta = theta*log|r| - Im Li_2(exp(i*theta)/r).

Both follow by differentiating Li_2(w), whose derivative is -log(1-w)/w. The relevant arguments lie inside the unit disk, or on its boundary for exact cyclotomic roots. The principal dilogarithm is continuous at w=1; thus even a unit-circle logarithmic singularity has a continuous, integrable primitive. On open positive arcs none of those singularities occurs. For every formula the actual root is enclosed by its computed ball, and every endpoint operation is performed with Arb/Acb, including polylog(2).

The checker evaluates endpoint differences, divides by 2*pi, adds the constant term C times interval width, sums the weighted roots, and doubles for symmetry. It rejects any nonfinite special-function result. Arithmetic/endpoint/root errors are included by ball propagation. The explicit unresolved-panel interval is then added. This gives

    J in [0.000003965735591704862027167201,
          0.000003965735591704862354791329].

The displayed decimal endpoints of H, J and B are rounded outward using exact integer floor/ceiling at 30 decimal places. All comparisons with the target are made on the internal Arb enclosure, not rounded console strings.

## Required controls

1. A denominator leading coefficient changed from 1 to 2 is rejected before numerical work: denominator must be monic.
2. An exponent changed to -1 is rejected before numerical work: negative exponent.
3. The false target 0.2519964889 is below B's lower endpoint and is rejected. A separate CLI run records FAIL in `false-target.json` and exits 1.
4. Q=X-3, S=5, q=1 has H=log(3) and B=log(5), since |T-3|<=5 on the unit circle. The checker encloses log(5) and J=log(5/3), with B in [1.609437912434100374586491804342, 1.609437912434100374646115455456].
5. Q=X-3, S=X, q=1/2 tests a numerator singularity at z=1. For c=cos(theta), Re T=1+c-2c^2<=9/8, so |T-3|>=15/8>sqrt(2)>=sqrt(|T|). Thus g<0 away from its negative singularity, J=0 and B=log(3). The checker returns exactly J=0 and encloses log(3) in [1.098612288668109691395245236922, 1.098612288668109691395245236923].

Both synthetic certificates satisfy the strict degree condition. Their closed-form answers are independently derived here. The coefficient and exponent controls are rejection tests; no valid-perturbation sensitivity result is claimed.

An AST inspection of the final check.py found no math import, float call, or floating-point literal. Numeric computation is exact integer/rational or Arb/Acb. Time is recorded with integer monotonic nanoseconds.

## Clean-room and model attestation

The producer inputs are exactly the three files and hashes in REPLAY.json. They match the supplied manifest. The checker was written in this session from the proof/certificate, mathematical identities and the installed library interface. Neither producer nor third-party replay code was read, imported, or executed. Permitted public theorem/definition/PR text was read; linked packets were not. No neighboring job files or forbidden repositories were accessed.

The exact serving-model ID and producer/referee model difference cannot be established from exposed session metadata. REPLAY.json states this limitation in its model string. Its PASS status refers to the mathematical numerical replay, not a certification of different-model provenance. The referee verdict is HOLDS WITH CAVEATS for that reason. This is an AI review with the trust assumptions stated above.
