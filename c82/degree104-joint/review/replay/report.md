# Clean-room C82 replay

PASS. At 256-bit precision, with python-flint 0.9.0 and one FLINT thread, the independently written checker proves

    B in [0.2520179247552093517426, 0.2520179247552093517434]
    C82 <= B < 0.2520179248.

These displayed decimal endpoints are rounded outward from exact dyadic endpoints in `result.json`. The entire replay interval is inside the supplied interval [0.2520179247552093455135, 0.2520179247552093577392]. The margin below the requested target exceeds 4.4790648256e-11. The final run, including controls, took 77.04 seconds. Floating search fields were never used.

## Reproduction

Run from the job directory, with the shared environment on PATH or its Python selected as below:

```sh
nice -n 10 env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
  "$HOME/dev/open-science/.venv/bin/python" replay/check.py --controls
```

The checker is self-contained: only standard-library modules and python-flint are imported. The default certificate and output paths are resolved relative to the checker. `--bits` must be at least 192; default 256. `--target` is parsed as an exact rational. PASS is emitted only when the exact upper endpoint is strictly below that target. Exceptions fail closed. The result contains exact rational endpoints, all polynomial root counts and Mahler enclosures, exact hypotheses, and controls. No producer checker or source is imported or executed.

## Exact algebra

Coefficients are required to be genuine JSON integers (booleans are excluded), with nonzero leading coefficients. Denominators must be nonconstant and monic, their multiplicities positive integers. Numerator exponents must be nonnegative exact rational strings; zero exponents are discarded. FLINT integer-polynomial gcd checks cover every active numerator/denominator pair. The results are:

| Quantity | Exact result |
| --- | --- |
| Denominators / active numerators | 10 / 18 |
| Active gcd pairs, all constant | 180 |
| D | 999999999960 |
| a | 940866927165429405/1048576 |
| D-a | 107709072792627555/1048576 > 0 |
| Common exponent denominator b | 1048576 |
| deg A | 940866927165429405 |
| bD | 1048575999958056960 |
| Composed roots, with multiplicity | 2666 |

Composition with T(z)=z-z² is performed in exact integer polynomial arithmetic. Certified `fmpz_poly.complex_roots()` enclosures supply every root with multiplicity; their total is checked against each composed degree. No denominator root enclosure meets the unit circle. Nine numerator root enclosures meet it; no claim of exact unit modulus is needed for the numerical method. The numerator n121_1_12 has leading coefficient 2; its logarithmic leading-coefficient contribution is included.

## Why the enclosure is rigorous

Write each composed polynomial as c product(z-r), retaining multiplicities. Define signed weights w as q/D for numerator roots and -m/D for denominator roots. Then

    g(t) = C + sum_r w_r log|exp(2*pi*i*t)-r|,
    C = sum_f signed_weight_f log|leading_coefficient_f|.

Jensen's root formula gives H directly, using Arb's interval maximum for max(1,|r|). The computed value is

    H = 0.25201595834101400864803690432418192408422613437856...
    J in [0.0000019664141953430945990,
          0.0000019664141953430952898].

Both H and J, including all rounding and unresolved-cell errors, are enclosed in `result.json`.

For a dyadic t-interval with midpoint t0 and angular half-width h, put z0=exp(2*pi*i*t0). The chord bound |exp(i*s)-1|<=|s| bounds each root distance between max(0, |z0-r|-h, ||r|-1|) and |z0-r|+h. These give direct logarithmic upper and lower bounds with signs reversed for negative weights. A zero lower distance for a numerator contributes negative infinity to the lower bound, but a finite upper bound. Denominator distances stay positive by certified unit-circle separation. Thus neighborhoods containing numerator singularities can be proved nonpositive without omitting any neighborhood or integrating an undefined value.

On intervals whose root-distance lower bounds d_r are positive, a second, tighter enclosure uses the signed derivative sum at the midpoint:

    d/dtheta log|exp(i*theta)-r| = -Im(r/(exp(i*theta)-r)),
    |d²/dtheta² log|exp(i*theta)-r|| <= |r|/d_r².

Taylor's theorem bounds the change from the midpoint by

    |sum_r w_r f'_r(theta0)| h
      + (h²/2) sum_r |w_r| |r|/d_r².

All quantities are balls. Intersecting these one-sided bounds with the direct bounds preserves rigor. The second derivative estimate is valid throughout the real interval, not merely at sampled points.

The algorithm bisects [0,1/2]. Nonpositive intervals contribute zero; positive intervals are retained and adjacent ones merged. Any remaining interval contributes the enclosure [0, width*upper(g)] only after its upper contribution is below 1e-23. This tolerance is a subdivision criterion, not an asserted error estimate: the actual summed interval contributions enter the final ball. There were 5167 visited cells, 1461 negative leaves, 32 merged positive runs, 66 unresolved leaves, and maximum depth 41. The unresolved contribution after doubling is at most 6.91e-22. No completeness assumption about sign-change detection is used.

On positive intervals integration is by an analytic primitive, with no quadrature truncation error. For theta=2*pi*t:

    |r|<1: F_r(theta) = Im Li_2(r exp(-i*theta)),
    |r|>1: F_r(theta) = theta log|r| - Im Li_2(exp(i*theta)/r).

In each case F'_r(theta)=log|exp(i*theta)-r|. The interval integral is the endpoint difference divided by 2*pi. Strict modulus classification keeps the dilogarithm arguments inside the unit disk. For root balls whose modulus includes 1, the first formula is used only after an interval image of r*exp(-i*theta) is proved disjoint from the principal dilogarithm cut [1,infinity); otherwise that integral interval is bisected. This also covers possible roots just outside the circle. Arb encloses the dilogarithms and all endpoint arithmetic. Finally real coefficients imply g(1-t)=g(t), so the half-circle result is doubled.

The checker intentionally fails closed if a denominator cannot be separated from the unit circle. That limitation is irrelevant to this certificate; no general-purpose singular-denominator integration claim is made.

## Controls

All were executed in the final run:

- A denominator's leading coefficient changed from 1 to 2: rejected as nonmonic.
- An exponent changed to -1: rejected.
- A degree-violating exponent and an added shared numerator/denominator factor: rejected.
- A valid single-coefficient change P1=X to 2X: exact hypotheses still pass. The numerator log-Mahler mean alone is now greater than the original upper endpoint; since B is at least that mean, B provably changes. This specifically exercises numerator leading constants.
- A valid exponent change q(P1) to zero: exact hypotheses still pass. On [4/125,321/10000], an interval lower bound for g, together with H and symmetry, already exceeds the original upper endpoint. B provably changes; a full perturbed integral is unnecessary.
- False target 0.2520179247: below the certified lower endpoint, hence conclusively rejected.
- Full-pipeline analytic case Q(X)=X-3, A(X)=1: J=0 and B=log(3), reproduced at 256 bits. Indeed |3-z+z²|>=1 on the circle, and both roots have modulus sqrt(3).
- Singular/sign-changing analytic case g(t)=log|1-exp(2*pi*i*t)|: the computed integral of its positive part encloses Im Li_2(exp(i*pi/3))/pi = 0.3230659472194505140936365107..., with radius below 4e-24. Its positive support is (1/6,5/6).

The valid mutations are evaluated through the same exact hypotheses and root methods. Their separation witnesses and exact endpoints are in `result.json`.

## Provenance and limits

Only the supplied CLAIM.md, PROOF.md, and certificate.json were used as producer inputs. Their hashes match INPUTS_SHA256SUMS. Public reference reading was limited to the allowed live 82a page, PR text, and Doche's paper. The checker and root probe were written during this session. No linked producer packet or repository code was read, imported, or run. The replay does not numerically reproduce the older PR certificates.

This is a mathematical and interval-arithmetic AI review, not a proof-assistant formalization or a human review. Its arithmetic trust is Python exact integers/Fraction, python-flint, and FLINT/Arb's certified polynomial roots and special functions. The session identifies itself as GPT-6-based Codex but does not expose the exact serving-model ID. The receipt therefore cannot authenticate a different-model claim; that would require the launcher's separate evidence.
