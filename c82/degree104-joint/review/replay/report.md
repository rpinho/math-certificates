# Clean-room replay report: C82 certificate (round 12)

Replayer: Claude Opus 5.5 (claude-opus-5-5), job math_c82r12ref_1120. Only inputs/CLAIM.md, inputs/PROOF.md and inputs/certificates/certificate.json were used (sha256 3dce9f3e…, b4134725…, dc129b75…). No producer code was read or run.

## Method (replay/check.py, standard library + python-flint 0.9.0 only, no floating point)

- **Exact hypotheses.** All coefficients are Python ints. Denominators are monic, nonconstant and have positive integer multiplicities. Exponents are strict nonnegative `p/q` strings. Numerators are nonzero. a < D is checked in exact rationals, and gcd(S_i, R_j) = 1 is checked over Z[x] for every active pair.
- **H = (1/D) Σ m_j log M(R_j∘T).** R_j∘T is composed exactly in Z[x]. All 208 roots are isolated rigorously with FLINT (`fmpz_poly.complex_roots`, 256 bits). Then log M = log|lc| + Σ log max(1, |ρ|) is evaluated in Arb, and every |ρ| is decided to be above or below 1 (0 undecided). gcd(R_j∘T, reversed) = 1 confirms that Q∘T has no zero on |z| = 1.
- **J = 2∫_0^{1/2} max(0, g).** The factor 2 is exact because g(t) = g(1-t). The integral is computed with Arb's rigorous integrator (`acb.integral`, i.e. `acb_calc_integrate`) at 192 bits, with absolute tolerance 2^-60 and relative tolerance 2^-50. g is evaluated in root form over the 1863 isolated roots of the S_i and R_j in the w = T(z) plane:
  - Analytic flag set (ellipse bounds): the integrand returns the analytic continuation G = c + Σ (w_k/2) log((T(z) - s_k)(T(1/z) - conj s_k)) when Re G > 0 on the whole ball, returns 0 when Re G < 0 on the whole ball, and returns a non-finite ball otherwise (sign change, or a log touching its cut).
  - Analytic flag not set: the integrand returns a ball containing max(0, g) on the real points. A root touching the ball gives a one-sided bound: log of the upper bound of |w - s| for numerator roots, with the lower side set to -∞. Sign changes of g and the zeros of A∘T on the circle are therefore covered by Arb's own bisection and direct enclosures. No neighbourhood is excised.
- **B = H + J.** The exact dyadic endpoints are converted to Fractions and compared exactly with the target.

## Results

| run | B enclosure | target | result |
|---|---|---|---|
| main (`check.py certificate.json`, tol 2^-60) | [0.2519694758380326654679408, 0.2519694758382429035635232] | 0.2519694759 | **PASS** |
| false target (`--target 0.2519694758`, tol 2^-60) | [0.2519694758380326654679408, 0.2519694758382429035635232] (identical to main) | 0.2519694758 | FAIL, as required |
| coarse tolerance (`--tol 50`) | [0.2519694757893773091012337, 0.2519694759017172357419176] | 0.2519694759 | FAIL (resolution only, see below) |

Main run details:
- H ∈ [0.2519693873279416368328252, 0.2519693873279416368328253]
- J ∈ [0.0000000885100910286353274, 0.0000000885103012667304862]
- D = 740384615402384615382720 and a = 696806913114226553812602710857/1048576, so a/D ≈ 0.89754.
- 228 coprime pairs; 1,457,424 integrand evaluations.
- 1758 s on one core, nice 10, peak RSS 35.6 MB.

The producer's interval [0.2519694758381300638735, 0.2519694758381300658953] lies inside the main enclosure. The upper endpoint is 6.18·10⁻¹¹ below 0.2519694759, about 290 times the enclosure width of 2.1·10⁻¹³.

The run at tolerance 2^-50 has width 1.1·10⁻¹⁰, because Arb's absolute tolerance applies per subinterval. Its upper end exceeds the bar, so that tolerance cannot decide the claim. It is consistent with the main run and refutes nothing. A run at 2^-70 was stopped after about 40 minutes with no output, and its result is not used. The main run used an explicit `--tol 60`, which was then made the default in check.py; the computation is otherwise identical.

## Controls

- **Analytic controls** (`--control analytic`):
  - R = X-3 with no numerator: B = log 3.
  - R = X-3 with S = 7: g > 0 everywhere, B = log 7.
  - R = X-3 with S = 2: g changes sign at cos θ = 1/2 and 1/6, and B = log 3 + (1/π)∫_{π/3}^{acos(1/6)} (log 2 - ½ log(12cos²θ - 8cosθ + 5)) dθ, computed by a separate 1-D Arb integral.

  All three enclosures contain the known value with width < 10⁻¹⁵: OK.
- **Rejection controls** (`--control reject`): a non-monic denominator, a numerator equal to a denominator (gcd), the P1 exponent doubled (a ≥ D), a decimal exponent string, zero multiplicity and a non-integer coefficient are all rejected: OK.
- **Perturbed coefficient** (constant term of denominator 0 plus 1, `--control coeff --tol 50`): B ∈ [0.25683270814946, 0.25683270817347], disjoint from the original enclosure: OK.
- **Perturbed exponent** (q of N82r12_59d304ca3db3 doubled, `--control exponent --tol 50`): B ∈ [0.25199495456095, 0.25199495456771], disjoint from the original enclosure: OK.
- **Numerator zeros on the circle**, found by exact gcd with the reciprocal polynomial:
  - P1∘T has a zero at z = 1 (t = 0).
  - P2∘T has zeros at z² - z + 1 (t = 1/6, 5/6).
  - P4∘T has zeros at Φ10 (t = 1/10, 3/10, 7/10, 9/10).

  Each is a -∞ of g. The integrator handles them through one-sided bounds and they contribute 0 to J.

## Reproduce

    cd c82r12ref/replay
    ~/dev/open-science/.venv/bin/python -I check.py ../inputs/certificates/certificate.json                        # PASS (~30 min)
    ~/dev/open-science/.venv/bin/python -I check.py ../inputs/certificates/certificate.json --target 0.2519694758  # FAIL expected
    ~/dev/open-science/.venv/bin/python -I check.py ../inputs/certificates/certificate.json --control analytic
    ~/dev/open-science/.venv/bin/python -I check.py ../inputs/certificates/certificate.json --control reject
    ~/dev/open-science/.venv/bin/python -I check.py ../inputs/certificates/certificate.json --control coeff --tol 50 --ref-lo 0.2519694757893773091012337 --ref-hi 0.2519694759017172357419176
    ~/dev/open-science/.venv/bin/python -I check.py ../inputs/certificates/certificate.json --control exponent --tol 50 --ref-lo 0.2519694757893773091012337 --ref-hi 0.2519694759017172357419176

Raw outputs are in replay/*.out.

Trust base: FLINT's complex root isolation, Arb ball arithmetic and `acb_calc_integrate`, the python-flint bindings, and the correctness of check.py's integrand (in particular its analytic-flag logic, which the three analytic controls exercise).
