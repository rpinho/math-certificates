# Independent replay method

This checker was written from the three supplied inputs, the live 82a definition, Doche's paper, and the permitted PR prose. No producer code or linked certificate packets were read or executed. Only the exact coefficient lists, multiplicities and rational-exponent strings affect the computation; other JSON numbers are parsed as inert strings.

## Exact algebra and normalization

Integer polynomial algebra checks every coefficient, denominator monicity, positive integer multiplicities, nonnegative rational exponents, every active numerator/denominator gcd, and the strict weighted-degree inequality. With T(z)=z(1-z), composition is exact. For each composed polynomial, FLINT isolates every complex root with its multiplicity; multiplicities must sum to the degree. Jensen's formula gives log M(f)=log|lc(f)|+sum log max(1,|r|), enclosed by Arb. The computation uses 384-bit precision, with one FLINT thread.

## Sign partition and integration

Write g(t)=c+sum_r w_r log|exp(2*pi*i*t)-r|, including signed normalized weights and multiplicities. Positive w come from numerators and negative w from denominators. All nonmonic numerator leading coefficients are included in c. Real coefficients give g(1-t)=g(t), so the checker integrates [0,1/2] and doubles.

For a dyadic panel centered at t0 of half-width h, set z0=exp(2*pi*i*t0), e=2*pi*h, d_r=|z0-r|. The chord distance from z0 is at most e. Thus d_r-e and d_r+e bound each root distance (using a lower bound only when positive). Summing weighted log upper bounds for numerator factors and log lower bounds for denominator factors gives a rigorous upper bound on g. This works even when a numerator root lies on the panel: its logarithm has a finite upper bound and its negative singularity cannot create missing positive area. No singular neighborhood is discarded by sampling.

If all root distances have positive lower bounds, the point value and first derivative are evaluated directly from the exact polynomials and their derivatives using Arb. The inequality

    |d²/dtheta² log|exp(i*theta)-r|| <= |r|/|exp(i*theta)-r|²

bounds the Taylor remainder. A panel range is obtained from g(t0), g'(t0), and half the weighted second-derivative bound times h². The checker either proves the panel nonpositive, proves it positive, or bisects it. Sign-uncertain panels are retained with an enclosure [0, width*max(0,upper(g))] only once upper(g)<eps. Their sum over the full circle is bounded by eps. No sign-change count or numerical zero finder is assumed.

Adjacent proven-positive panels are merged. Their integrals are evaluated using a rigorous dilogarithm primitive for each root. For |r|<1,

    integral_l^r log|exp(2*pi*i*t)-alpha| dt
      = Im[Li_2(alpha*exp(-2*pi*i*t))]_l^r/(2*pi).

For |alpha|>1, use log|alpha|*(r-l) minus Im[Li_2(exp(2*pi*i*t)/alpha)]_l^r/(2*pi). These arguments lie inside the unit disk, where no dilogarithm cut is crossed. Unit roots are certified by exact cyclotomic factors of the gcd of f with its reversal; each such enclosure must match exactly one isolated root. For a unit root the inside formula holds by continuity, including at its integrable singularity. The endpoint evaluation includes the uncertainty of the root enclosure. Any other modulus overlapping 1 is refused. Denominator roots overlapping the unit circle are conservatively refused; none occur in this certificate. This is a supported-domain restriction of the checker, not an additional hypothesis of the theorem.

All truncation/error sources are accounted for: root enclosures, Arb operations, interval sign bounds, uncertain panels and certified special-function evaluation. The tolerance is an explicit enclosure contribution, never a claim that an integrator's tolerance equals its error. Exact rational endpoints are saved in result.json; the final target comparison is made with exact rational input enclosed by Arb.

## Controls

The leading coefficient of one denominator is perturbed from 1 to 2 and rejected. One exponent is perturbed to -1 and rejected. Additional controls add a shared numerator/denominator factor and violate the degree inequality; both are rejected. The false target 0.2519696459 must lie strictly below the replay's lower endpoint.

The analytic certificate R=X-5, S=X-1, q=1/2 has |R(T)|>=3 and |S(T)|<=3, so J=0; both denominator roots have modulus sqrt(5), hence B=log(5). The checker verifies that value, and also compares the full-circle primitive with Jensen's formula, including its unit roots. A constant-positive integrand gives log(2) exactly up to the enclosing arithmetic.

## Reproduction

From the job directory:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 /usr/bin/time -l nice -n 10 ~/dev/open-science/.venv/bin/python replay/check.py
```

Requires standard-library Python and python-flint (tested version 0.9.0). No local helper imports, search libraries, binary floating-point literals, calls to float, or math imports occur in check.py. Logs and exact endpoint results are local artifacts. This is an AI-written numerical proof with FLINT/Arb and the cited theorem in its trust base, not a proof-assistant formalization.

## Final result

PASS. The rigorous enclosure is contained in

    [0.2519696459872490990419691935079545,
     0.2519696459872490990419691935079546].

It lies inside the supplied claim bracket and strictly below 0.2519696460.
The unrounded exact endpoint interval in result.json has width less than
9e-42; the displayed endpoints above are deliberately rounded outward.
The false target 0.2519696459 lies below the lower endpoint.

    H = 0.2519695552678072499354164706113521929338533...
    J = 0.00000009071944184910655272289660232626439...

All 4198 roots and 240 gcd pairs were checked. The sign partition used
14369 calls, 4161 nonpositive panels, 96 unresolved panels and 48 merged
positive intervals. The retained unresolved contribution is enclosed by
an Arb ball of radius less than 9e-42; it was not discarded.

The final checker run (PID 41126, time wrapper 41123) exited successfully:
143.00 seconds elapsed, 142.41 seconds user CPU, 0.27 seconds system CPU.
The /usr/bin/time peak RSS was 42,418,176 bytes, below the 1 GB cap;
result.json reports the slightly earlier in-process high-water mark
42,270,720 bytes. It used one numerical worker and one FLINT thread.
The earlier complete run agreed and took 136.57 seconds. The final run
added the analytic controls below without changing the integration code.
Final log: final-run.log. All started numerical workers have exited.

No exact serving-model identifier is exposed to this session. The receipt
truthfully records GPT-6 / Codex with that limitation; different-model
provenance is not certified. Producer code was neither read nor run.

Additional analytic controls exercise an inside root at 1/2 (its half-circle integral is zero by Jensen and conjugation symmetry) and the genuine certificate R=X-5, S=100, q=1. In the latter, |R(T)|<=7<100, so g is positive everywhere and B=log(100); this checks the nonconstant positive branch and the dilogarithm primitive together.
