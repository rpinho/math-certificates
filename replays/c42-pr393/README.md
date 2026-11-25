# C42 PR #393 clean-room audit and replay

I audited Jinhao Huang’s Turán pure power-sum claims for Optimization Constants entry 42a. [teorth/optimizationproblems#393](https://github.com/teorth/optimizationproblems/pull/393), [doi:10.5281/zenodo.24502737](https://doi.org/10.5281/zenodo.24502737).

- **Theorem 1 — HOLDS.** The rigorous replay of Huang’s $R_n > 501/1000$ for all $n \ge 1$ uses `replay/verifier_a.py` and `replay/verifier_b.py`. The rigorous one-box hand proof of $R_n > 5001/10000$ also holds, with exact checks in `replay/check_hand_proof.py` and a separate one-box calculation in `replay/verifier_a.py`.
- **Theorem 2 (PDF Theorem 4) — hypotheses checked, $F<T$ not replayed.** Huang claims $C_{42} \le 0.6863607438$. The T2-lite check covers input provenance and the hypotheses detailed below. [Huang’s manuscript](https://doi.org/10.5281/zenodo.24502737).

This is AI work. Gemini 4 Neon High carried out my clean-room audit from the mathematical text and data. The claimant’s verification archive was neither read nor run. GPT-6.2 Sol packaged this folder. [C42-verification.zip archive record](https://doi.org/10.5281/zenodo.24502737). Verifiers A and B are two separate implementations by one agent and do not constitute independent review. No human has checked it. I claim no new bound. This replay alone does not remove an asterisk.

**Conflict of interest.** Huang’s Theorem 1 supersedes my $1/2 + 2^{-4096}$ lower bound from the earlier PR. Huang’s Theorem 2 cites my arbitrary-knot form of Bakeas’s Theorem A. [Earlier lower bound](https://github.com/teorth/optimizationproblems/pull/310), [Bakeas’s paper and appendix](https://hexagonmath.org/2611.00069v1).

## Lemmas and hand proof

I checked the normalization, both Newton identities, the first escape from the sector, the index and sector-induction preconditions, and the covariance transfer and separation steps. At $r=1/\sqrt{2}$ and $q<r$, the first Newton inequality at $l=1$ excludes $k=1$. Thus the escape index $k$ is at least two. The case $n=2$ is ruled out, since escape would require $k\le n-1$. The audit handles the acute and obtuse cases of sector induction and checks summation by parts and the complex conjugations in Lemma 2. [Lemma audit](replay/LEMMAS.md).

The proof minimizes $A_1-A_2$ over $(h,R)$ at $(h_-,R_+)$ after testing the derivative conditions. At that corner I checked that both radicands have strictly positive minima and that the maximum of $A_1$ lies below twice the minimum of $A_2$. This makes the $x'$ derivative of $A_1-A_2$ strictly negative on the full $(x',a)$ rectangle, including its algebraic corners with $a<(x')^2$. The rigorous `replay/check_hand_proof.py` passed all 41 of 41 checks in exact `fractions.Fraction` arithmetic. [Lemma audit](replay/LEMMAS.md), [hand-proof results](replay/hand_proof_audit.json).

I used `replay/stress_test.py` on 143 tuples, including 57 at $n=2$. The 74 Biró–Harcos cases that passed the sector threshold included eight 256-bit Arb root-tuple runs. These cases satisfy $q_{\mathrm{eff}}<1/\sqrt{2}$. The smallest observed $q_{\mathrm{eff}}$ was about 0.6900. The largest observed lemma residual was about $1.97\times 10^{-14}$. These are numerical stress diagnostics. The tuples exercise the AM–GM step and the forms with exact $k^{-1}$, and fall outside the small-$q$ precondition for the full index bound. [Stress results](replay/stress_test_results.json).

## Lower-bound verifiers

- **Verifier A.** In the rigorous run, `replay/verifier_a.py` used outward-rounded stdlib integers scaled by $10^{24}$ and a monotonicity reduction. It visited 6,922 boxes with 4,229 leaves. Its minimum leaf margin in $A_1-A_2-U_*$ was about 1.857e-7, and its diagnostic $q_{\max}$ was about 0.501034. The one-box run closed at depth zero. All 12,000 primitive trials against 100-digit `mpmath.iv` passed. [Verifier A results](replay/verifier_a_results.json).
- **Verifier B.** In the rigorous run, `replay/verifier_b.py` used 160-bit Arb, a factored squared inequality and splitting in $(h,R,x')$. It visited 92,146 boxes with 47,609 leaves. Its minimum leaf margin in $A_1^2-A_2^2-U_*(2A_2+U_*)$ was about 2.397e-7, and its diagnostic $q_{\max}$ was about 0.501014. Its NaN, infinity, overlapping-ball and negative-square-root tests passed. [Verifier B results](replay/verifier_b_results.json).

Both verifiers closed the boundary strips at $t=0$, $t=t_{\max}$, $z=0$ and $z=1$. The two margins are on different expressions. The bisections describe the observed limits of the verifier configurations.

| Control | Outcome in A and B |
| --- | --- |
| $q=0.5016$, $c=0.9657$ | `PRECONDITION_FAILED` on the sector condition |
| $q=0.5019$, $c=0.9657$ | `PRECONDITION_FAILED` on both sector and index conditions |
| $q=0.5019$, $c=0.96$ | `PRECONDITION_FAILED` on the index condition alone |
| $c=0.99$, $q=0.501$ | `PRECONDITION_FAILED` on the sector condition. With the precondition deliberately bypassed, separation succeeds in 1,536 and 3,072 leaves, respectively |
| $q=0.5012$, $c=0.9657$ | Preconditions pass. Separation is `INCONCLUSIVE` after 1,814 and 26,474 visits |
| $c=0.95$, $q=0.501$ | Preconditions pass. Separation is `INCONCLUSIVE` after 13 and 18 visits |
| Set $m_0=0$ at $q=0.501$ | `INCONCLUSIVE` after 530 and 11,967 visits |
| Drop $v_-^2 D_0^2$ at $q=0.501$ | Positive control passes after 8,666 and 113,836 visits |

The source audit’s first expanded squared expression caused the positive control to hit Verifier B’s depth limit. Algebraic factoring reduced interval dependency and the final run passed. The source audit also recorded float cancellation during polynomial reconstruction and a binary-division artifact in the primitive tests. It used Arb polynomial multiplication and exact integer checks with high-precision interval comparisons to address them. [Ledger verdict](replay/VERDICT_for_ledger.txt).

## Theorem 2 T2-lite

With `replay/t2_lite.py` I matched the claimant JSON to the manuscript SHA-256, matched the 100 strictly increasing rational knots to the stated knot set, and confirmed that $T$ and $C$ both equal $3431803719/5000000000$. All 100 knots and phase strings agree with Vatopoulos’s pinned file. Huang used a height of 0.6863607438. Vatopoulos’s earlier search used 0.68636074. [Pinned phase input](https://github.com/NikosVat/turan-c42/blob/72703467aaac1082a123966b75f654a292c1e5f7/results/A_D96_4.json), [T2-lite results](replay/t2_lite_results.json).

The rigorous 256-bit Arb checks in `replay/t2_lite.py` give $\operatorname{Re}\gamma>0.09318$ and $\sup_{0<v\le 1/2}|d_0(v)|<0.587$ across all 99 segments. On the second half the rigorous check in `replay/t2_lite.py` gives $|d_0(v)|=T<1$. The rotation of the initial phase by minus half a radian failed the real-part test (approximately -0.244238). For the second red control I set the final phase to the initial phase plus two radians. The test rejected the resulting last-segment enclosure, whose upper endpoint was approximately 1.155105. [T2-lite results](replay/t2_lite_results.json).

The printed numerator and denominator are 0.197467474154 and 0.287702168300. Their quotient is approximately 0.686360743545359, about 3.2e-12 above the manuscript’s printed 0.686360743542159 and about 2.546e-10 below the stated height. The source audit attributes the discrepancy to outward rounding of the printed endpoints. The Volterra integral inequality $F<T$ remains unreplayed. [Manuscript](https://doi.org/10.5281/zenodo.24502737), [T2-lite results](replay/t2_lite_results.json).

## Replay

The core lower-bound checks use only the scripts and Python dependencies below. For the stress test and T2-lite, obtain the exact JSON inputs from the public sources in the [input manifest](replay/INPUTS.sha256). The manifest also records the PDF and TeX inputs for manual review. The scripts write their JSON outputs to the working directory, so run them in a separate directory to preserve the packaged results.

In a Python environment with NumPy, mpmath and python-flint (Verifier B used python-flint 0.9.0), run from this packet’s root:

```sh
shasum -a 256 -c SHA256SUMS
work="$(mktemp -d)"
mkdir -p "$work/inputs"
cp replay/*.py replay/INPUTS.sha256 "$work/"
cd "$work"
python3 check_hand_proof.py
python3 verifier_a.py
python3 verifier_b.py
```

Place Huang’s data at [inputs/upper99-tight.json](https://doi.org/10.5281/zenodo.24502737) and Vatopoulos’s data at [vatopoulos_A_D96_4.json](https://github.com/NikosVat/turan-c42/blob/72703467aaac1082a123966b75f654a292c1e5f7/results/A_D96_4.json) in that working directory using the [input manifest](replay/INPUTS.sha256). Then run:

```sh
awk '$2 ~ /[.]json$/' INPUTS.sha256 | shasum -a 256 -c -
python3 stress_test.py
python3 t2_lite.py
```

Allow runtime fields to vary. Compare the outcomes and counts to the captured JSON files. The exact lower-bound check excludes every box of the stated domain. There is no statistical holdout.

## Credits

Jinhao Huang, with OpenAI Codex, derived and reported the claims. I credit A. Biró for the Newton-identity method, Biró and G. Harcos for the upper-bound construction used in the stress tests, V. Bakeas for Theorem A, N. Vatopoulos for the phase data, and A. Canli for earlier replays of Theorem A certificates. [Credits and sources](CREDITS.md), [prior art](replay/PRIOR_ART.md), [packaging and provenance](PACKAGING.md).
