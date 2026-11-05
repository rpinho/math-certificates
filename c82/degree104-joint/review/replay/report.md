# Independent replay of the supplied C82 certificate

**PASS.** The independently computed bound satisfies C82 <= B < 0.2519923410. The numerical replay passes; the exact serving-model ID remains unavailable, so different-model provenance cannot be attested.

## Inputs and independence

The mathematical inputs are only `inputs/CLAIM.md`, `inputs/PROOF.md`, and `inputs/certificates/certificate.json`. Their hashes were compared with `INPUTS_SHA256SUMS`. The old proof's certificate-specific values are not reused. Search-time JSON numbers are parsed as strings and ignored. No producer code or earlier checker was read, imported, or run. The allowed live 82a page, PR bodies/comments (#280, #301, #330), and Doche's paper supply definition, theorem, and comparison context; linked code/packets were not accessed.

Implementation uses Python's standard library and python-flint 0.9.0. Arb precision is 384 bits; FLINT and BLAS are restricted to one thread. The exact serving-model identifier is not exposed in this session; the honest model description is “GPT-6-based Codex (exact serving-model ID not exposed)”. This replay does not establish that the producer and referee used different model IDs.

## Exact certificate checks

Coefficients must be JSON integers (booleans excluded), with nonzero leading coefficient. Every denominator must have positive degree and leading coefficient exactly 1; multiplicities must be positive integers. Every numerator must be nonzero and its exponent an exact nonnegative rational string. Zero weights are discarded. All active numerator/denominator polynomial gcds have degree zero. The common exponent denominator is computed with integer Euclidean gcd/lcm.

For this certificate:

- Eight degree-104 monic denominators and eighteen active numerators.
- D = 999999999856.
- a = 939550863051360379/1048576.
- D-a = 109025136797644677/1048576 > 0.
- b = 1048576; deg(A) = 939550863051360379 < bD = 1048575999849005056.
- 144 active gcd pairs.
- 2224 roots counted with multiplicity after exact composition with T(z)=z-z².

In particular, the nonmonic numerators with leading coefficients 9 and 2 are retained without normalization. Their leading-coefficient logarithms contribute to g.

## Mahler measure

Each polynomial is composed with T in exact integer arithmetic. FLINT's certified complex root enclosures supply all roots and multiplicities, whose sum is checked against its degree. For a polynomial F with leading coefficient c,

    log M(F) = log|c| + sum_r multiplicity(r) * log(max(1, |r|)).

Arb's interval maximum is used even if a root's modulus enclosure meets 1. Hence no approximate inside/outside classification is needed. The denominator weights m/D give H.

## Rigorous integration, including sign changes

The real coefficients give g(1-t)=g(t). An adaptive exact dyadic partition covers [0,1/2]; its integral is doubled. The sum of accepted interval lengths is checked exactly to equal 1/2.

For a panel t=c+h*u, |u|<=1, set z0=exp(2πic). On the complex disk |u|<=4,

    |exp(2πi(c+h*u))-z0| <= delta = exp(8πh)-1.

For each composed factor F, certified roots give a positive lower bound d for min_r |z0-r|. If rho=delta/d<1, every root logarithm has an analytic branch relative to its value at the center. Factoring F shows that its log variation on this disk has modulus at most deg(F)*[-log(1-rho)]. Thus the weighted sum has a bound

    M = sum_F |weight(F)|*deg(F)*[-log(1-rho_F)].

Taking the real Taylor coefficients is legitimate: the holomorphic extension of the real part is the average of the analytic function and its coefficientwise conjugate. It has the same disk bound. The weights are -m/D for denominators and +q/D for numerators.

The coefficients through order K=40 are computed independently of the roots: form exp(2πi(c+h*u)), compose T, evaluate the original exact polynomial by series Horner, and take its logarithmic series in Arb/Acb. The principal logarithm's constant imaginary branch has no effect on the real coefficients or derivatives. All coefficient balls must be finite.

Cauchy's coefficient bound gives, uniformly for |u|<=1, the explicit omitted-tail bound

    E = M * 4^(-(K+1)) / (1-1/4).

A ball polynomial evaluation plus [-E,E] encloses g over the full real panel. A nonpositive panel contributes exactly zero. A strictly positive panel contributes the termwise polynomial integral plus [-2hE,2hE]; only even powers remain. If the sign is unresolved, the full range of max(0,g), multiplied by panel length, encloses its integral. Such a crossing panel is accepted only when this error is small enough; otherwise it is bisected. Therefore no assumption is made about how many zeros or sign changes occur. An accumulated final radius check includes all Taylor, root, quadrature, crossing, and rounding errors.

## Logarithmic singularities

An additional exact check computes gcd(F(z), z^deg(F) F(1/z)) for every real composed factor. A unit-circle root must occur in this gcd. All denominator gcds are 1. The only nonconstant numerator gcds are z-1 for P1, z²-z+1=Phi_6(z) for P2, and z⁴-z³+z²-z+1=Phi_10(z) for P4. These are cyclotomic, so the complete unit-circle singularity list on [0,1/2] is t=0, 1/10, 1/6, 3/10. All corresponding numerator exponents are positive. This classification is supplementary; the numerical algorithm below bounds every panel without assuming a preselected singularity list.

If the analytic disk test fails, the checker bounds each |F(z)|² as the leading coefficient squared times the product of squared distances to its certified roots. Arb evaluation over the entire real panel encloses this product. A numerator factor whose range contains zero still has a finite upper bound for log|F|, obtained from the product's positive upper endpoint. Its nonnegative weight preserves the bound. Denominator logs must have a strictly positive lower bound on that panel.

Only a proved negative upper bound for g permits such a panel to contribute zero; otherwise it is bisected. Thus a neighborhood of a numerator root on the unit circle is never silently omitted. At the singular point g tends to minus infinity and max(0,g)=0. The finite collection of such points also has measure zero. The checker deliberately fails if any other singularity cannot be handled within its recursion bound; it does not assume that singularities are harmless.

## Controls and implementation history

Requested controls perturb a denominator leading coefficient and a numerator exponent, requiring exact rejection. Additional controls violate the strict degree and gcd hypotheses. The false target 0.2519923409 must lie strictly below the computed lower endpoint. Two analytic certificates use Q(X)=X-3, with a constant numerator 1 or 16 of weight 1. On |z|=1,

    |z²-z+3|² = 5+12 cos²(theta)-8 cos(theta) >= 11/3 > 1,
    |z²-z+3| <= 5 < 16.

Both roots have modulus sqrt(3). Thus the first case has H=log(3), J=0, B=log(3); the second has H=log(3), J=log(16)-log(3), B=log(16). This checks a wholly negative integrand and positive analytic integration against known answers.

An initial indexing mistake covered only [0,1/4]. That run was terminated and the active implementation reverted before correction. It produced no accepted result. The corrected implementation starts at dyadic level zero and verifies exact covered length. No change of numerical method was required.

The next run finished integration but failed while parsing the decimal target with `fmpq`, which accepts integer/rational strings in this installation. That version was withdrawn before correction. The replacement uses `arb(target_string)` directly: a strict ball comparison proves that the entire B enclosure is below the exact target. The previously unreached controls were checked, then the complete computation was rerun. Neither failed run was counted as verification.

Backend contracts: [python-flint integer-polynomial API](https://python-flint.readthedocs.io/en/latest/fmpz_poly.html#flint.fmpz_poly.complex_roots) returns complex root balls with multiplicities; [FLINT's certified integer-polynomial roots](https://flintlib.org/doc/arb_fmpz_poly/index.html) describes disjoint certified root enclosures. This calculation trusts Python exact integers and the FLINT/Arb implementation; it is not a proof-assistant formalization.


## Completed result

The final command exited successfully. Its outward-rounded enclosures are:

| Quantity | Lower endpoint | Upper endpoint |
|---|---|---|
| H | 0.251990275374608412903614832015 | 0.251990275374608412903614832016 |
| J | 0.000002065597399978337287368115 | 0.000002065597399978337289388528 |
| B | 0.251992340972008391240902200131 | 0.251992340972008391240904220544 |

The B interval is 2.020413E-24 wide and lies entirely inside the supplied claimed interval [0.2519923409720083869767, 0.2519923409720083953971]. Its upper endpoint is below the exact target 0.2519923410 by 2.7991608759095779456E-11. These are two-sided rigorous enclosures, not quadrature estimates with only arithmetic radii.

The 7817 visited dyadic panels produced 3909 accepted panels: 2524 Taylor-negative, 1064 positive, 62 bounded sign-crossing panels, and 259 panels proved negative by root-product bounds. The deepest dyadic level was 45; accepted lengths sum exactly to 1/2. The final run took 478.658496375 seconds on one worker.

All controls passed:

| Control | Outcome |
|---|---|
| Perturbed denominator leading coefficient 1 -> 2 | Rejected: not monic |
| Perturbed numerator exponent -> -1 | Rejected: negative exponent |
| Exponent increased past degree allowance | Rejected: a >= D |
| Denominator added as active numerator | Rejected: nonconstant gcd |
| False target 0.2519923409 | Rejected: below rigorous lower endpoint of B |
| Analytic Q=X-3, numerator constant 1 | Contains log(3), J=0 |
| Analytic Q=X-3, numerator constant 16 | Contains log(16), J contains log(16/3) |

The final check.py passes an AST inspection for no floating-point literals, no math imports, and no float calls. It imports no other local file. No raw binary floating-point computation is used by the checker; Arb/Acb provide rigorous ball arithmetic.

## Reproduce

From this job directory, with the supplied inputs and python-flint installed:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
  nice -n 10 ~/dev/open-science/.venv/bin/python replay/check.py --controls
```

This writes replay/result.json and prints PASS only after the full interval computation and controls. The false-target control is included in that command. Output decimals are rounded outward from exact rational representations of Arb's dyadic endpoints. The final target comparison uses the conservative Arb enclosure of the decimal string.

## Comparison and conclusion

The candidate is below both live printed bounds on the same 82a definition. Comparing with the rigorous B upper endpoint, the decrease is:

- PR #280: 0.000015631427991608759095779456.
- PR #330: 0.000004148027991608759095779456.

The corresponding improvements of the printed target 0.2519923410 are 0.0000156314 against #280 and 0.0000041480 against #330. The prior packets were not replayed, and no global record claim is made. See PRIOR_ART.md for the scoped source check.

Did this referee discover something new? **No.** It independently reproduced the supplied candidate. That candidate does improve the compared printed bounds. The mathematical result holds, conditional on the usual trusted exact/ball-arithmetic backend. The referee verdict is HOLDS WITH CAVEATS solely because the exact model identity, and therefore different-model provenance, cannot be established within this session.
