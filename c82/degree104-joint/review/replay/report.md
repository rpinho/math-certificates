PASS: the independent 256-bit Arb replay proves C82 < 0.2519744488.

The rigorous outward decimal enclosure is

    0.25197444874089584903007645293157 <= B <= 0.25197444874089584903007646836791.

This interval lies strictly inside the interval in CLAIM.md. The exact dyadic endpoints, rather than rounded display values, are in result.json. The margin below the target is at least 0.00000000005910415096992353163209.

| Quantity | Rigorous lower endpoint | Rigorous upper endpoint |
| --- | --- | --- |
| H | 0.25197436708340060031800650705742 | 0.25197436708340060031800650705743 |
| J | 0.00000008165749524871206994587414 | 0.00000008165749524871206996131049 |
| B=H+J | 0.25197444874089584903007645293157 | 0.25197444874089584903007646836791 |

All 240 active gcds are 1. There are 5 denominators, 48 active numerators and 5,370 composed roots. D=1000000000064, a=233913093063931949/262144, D-a=28230906952845267/262144>0, and b=1048576. The task's smaller numerator/root counts are stale; the input hashes match its manifest.

The final partition has 7,595 leaves on [0,1/2]: 4,167 nonpositive by the series bound, 70 nonpositive by distance bounds, 3,254 positive integrations, and 104 sign-uncertain panels with bounded positive-part contributions. The deepest dyadic subdivision is 79. A total of 15,189 tree nodes were visited. These counts describe the enclosing partition, not a sampled sign-change count.

All controls passed:

- One denominator constant coefficient 1 -> 0: rejected by exact gcd.
- First numerator exponent increased by D, remaining positive: rejected by the strict degree inequality.
- False target 0.2519744487: proved below B's lower endpoint and rejected.
- Q(X)=X-3 with constant numerator 10: the enclosure contains B=log(10) and J=log(10/3).
- g(t)=log|exp(2*pi*i*t)-1|: the enclosure contains Im Li_2(exp(i*pi/3))/pi, testing both a circle singularity and a crossing.
- Six root-expression/direct-polynomial comparisons overlap. The static source check found zero math imports, float calls, or floating-point literals.

The final run used Python 3.12.13, python-flint 0.9.0 and FLINT 3.6.0, with ctx.prec=256 and ctx.threads=1. Series order K=16; moment truncation L=64; tolerance 1e-22. External /usr/bin/time measured 588.08 seconds wall time and 43,859,968 bytes peak RSS. The in-process RSS sample in result.json is slightly earlier. The initial complete integration and the final run briefly overlapped, with two single-threaded workers and about 80 MB combined observed RSS; the job stayed below 2 cores and 1 GB. Both workers exited. No remaining worker is permitted to outlive this session.

From the job directory, reproduce with:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
VECLIB_MAXIMUM_THREADS=1 /usr/bin/time -l nice -n 10 \
  "$HOME/dev/open-science/.venv/bin/python" replay/check.py \
  --prec 256 --tol 1e-22 --order 16 --target 0.2519744488 \
  --output replay/result.json > replay/final.log 2> replay/final.time
```

The checker reads only the supplied certificate as numerical input. No earlier results file or root cache is used. Its SHA-256 is `9faae75a638a6babd47a304e579824bbc9475b35de67fe13f9515f170aba65f4`. The raw final log is final.log; the resource measurements are final.time. All three input hashes and the canonical combined input hash are in REPLAY.json.

The exact serving-model ID is unavailable: the session identifies itself only as Codex based on GPT-6. REPLAY.json's PASS describes the completed interval replay; it does not attest a different-model relationship. REFEREE.md accordingly ends HOLDS WITH CAVEATS. No producer code was read or run.

The checker was written in this job from the allowed certificate and proof. It imports only the Python standard library and python-flint. No producer code, linked packet, prior local replay or forbidden repository was read or run. Public PR prose was read, including descriptions of other independent replays; those implementations were not accessed.

Exact arithmetic establishes canonical nonzero integer coefficient lists, monic nonconstant denominators, positive integer multiplicities, nonnegative rational exponents, the strict weighted degree inequality, and every active numerator–denominator gcd. Rational weights are parsed with Fraction, and the common denominator uses an integer gcd/lcm implementation. Search-time decimal fields are parsed as strings and ignored. Composition with T(z)=z-z^2 is performed with fmpz_poly. The checker never constructs the astronomical products Q or A.

For each composed integer polynomial, fmpz_poly.complex_roots supplies certified complex balls and multiplicities. Their multiplicities must sum to the exact degree. Jensen's formula evaluates log M as log of the absolute leading coefficient plus the sum of log(max(1,|r|)), including multiplicities. Every denominator root is proved off the unit circle. This implementation rejects a denominator whose root ball meets that circle; this numerical restriction is not an additional hypothesis of Doche's theorem. The supplied certificate passes it.

Let w_r be q_i/D for a numerator root, or -m_j/D for a denominator root, including root multiplicity. The integrand is evaluated as

    g(t) = c + sum_r w_r log|exp(2*pi*i*t)-r|,
    c = sum_f w_f log|leading_coefficient(f composed with T)|.

Thus nonmonic numerator factors contribute their leading coefficients; they are not silently normalized. The root expression is compared with direct evaluation of the exact composed polynomials at six rational points.

Integration uses an adaptive exact dyadic partition of [0,1/2], doubled by the real-coefficient identity g(1-t)=g(t). No sample is used to decide the sign on an interval. For a panel centered at t0, put z0=exp(2*pi*i*t0), h=pi*(right-left), p_r=z0/(z0-r), and u(delta)=exp(i*delta)-1. For |delta|<=h,

    log|z0 exp(i*delta)-r|
      = log|z0-r| + Re sum_{k=1}^K (-1)^(k+1) p_r^k u(delta)^k/k + E_r.

The series is used only if rho_r=|p_r| h < 3/4 for every root. Since |exp(i*delta)-1|<=|delta| for real delta, the rigorous uniform remainder is

    |E_r| <= rho_r^(K+1) / ((K+1)*(1-rho_r)).

The weighted errors are summed with absolute weights. All root uncertainty, coefficient formation, exponentials, logarithms, sums and remainders are enclosed by Arb. An interval evaluation of the summed polynomial in u, enlarged by the remainder, encloses g on the entire panel. A proved nonpositive panel contributes exactly zero to J. A proved positive panel contributes the enclosed integral of g. An unresolved panel contributes an enclosure from its positive-part range if small enough, otherwise it is bisected. These steps do not assume simple crossings or count crossings by sampling.

For positive panels the normalized moments of u(delta)^k are real. The identity

    sum_{j=0}^k (-1)^(k-j) binom(k,j) j^n = k! S(n,k)

with integer Stirling numbers gives the stable series

    mean(u(delta)^k) = sum_{even n>=k}
      (-1)^(n/2) h^n k! S(n,k) / (n!*(n+1)).

After n=L=2K+32, its absolute remainder is bounded by

    2^k exp(k*h) (k*h)^(L+1)/(L+1)!.

This follows by applying the exponential-series remainder to each term in the binomial expansion. The checker uses exact rational coefficients and adds this remainder before multiplying by the enclosed logarithm-series coefficient. The panel integral is its width times the average, including the logarithm remainder. All panel balls are added with outward rounding.

When the local log series cannot apply, the checker bounds every numerator log from above by log of an upper distance bound and every denominator log from below by log of a strictly positive lower distance bound. This yields an upper bound on g even if a numerator vanishes on the panel. A singular neighborhood is dropped only when that upper bound is nonpositive throughout. Otherwise it is subdivided. Hence log singularities are not omitted or replaced by point samples. The supplied numerator factors P1, P2 and P4 have possible unit-circle roots; all other root balls are separated from the circle.

The stopping tolerance controls panel error allocation, but acceptance of the advertised bound uses the actual final enclosure, not the tolerance setting. PASS requires that the exact dyadic upper endpoint be strictly less than the exact rational target. Reported decimal endpoints are rounded outward using integer arithmetic on the dyadic endpoints.

Controls include a one-coefficient perturbation that breaks coprimality, a positive exponent perturbation that breaks the degree condition, the false target 0.2519744487, and analytic examples. For Q(X)=X-3 and the constant numerator 10 with exponent 1, |Q(T(z))|<=5 on the unit circle, so B=log(10), H=log(3), J=log(10/3). For the root integrand g(t)=log|exp(2*pi*i*t)-1|, the singularity at t=0 and the crossing at t=1/6 are both present, and

    J = Im Li_2(exp(i*pi/3))/pi.

This follows from the Fourier expansion of log(2 sin(theta/2)), integrated over [pi/3,pi]. An independent Arb polylogarithm evaluation provides the comparison value.

Trusted components are Python exact integers/rationals, python-flint/FLINT's certified roots, and Arb's ball operations. This is a computer-assisted numerical proof with a prose mathematical reduction, not a proof-assistant formalization. Library documentation: https://python-flint.readthedocs.io/en/latest/fmpz_poly.html .
