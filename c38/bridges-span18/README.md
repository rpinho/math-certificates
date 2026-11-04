# C38: span-18 bridge candidate release

Based on the frozen research report dated 2026-11-04. See REPRODUCE.md for current commands and release validation.

Candidate and unrefereed:

\[
\mu(\mathbb Z^2)\ge \frac{8388608}{3192535}
=2.6275696272711184\ldots>\frac{1051}{400}=2.6275.
\]

The verifier is **separately written (same agent)**. No novelty judgment, separate authorship, refereeing, or formal proof-system acceptance is claimed.

The [best frozen certificate](frozen/c38_power_secant/VERIFIED.json), [written proof](frozen/c38_power_secant/input/PROOF_POWER_SECANT.md), and [22 actual corruption controls](frozen/c38_power_secant/REJECTION_CONTROLS.json) pass on the pod and the copied Mini artifact. The exact lower value at the reciprocal of this bound is approximately **1.0000001143720572**. Acceptance uses its exact rational numerator and denominator, with no decimal tolerance. The exact excess above the requested bound is 17783/255402800.

The best input-manifest SHA256 is

    9797a748df2e4f4e12bd56578e10d68ebdd8d350e8fd9180cfb8cc445d161281

**The full expanded integer coefficient vector is unmaterialized.** Its coefficients are specified exactly as counts of the finite family below, and its generating value is enclosed with exact rational arithmetic. Rational enclosure endpoints are not coefficient counts. An optional length-24 prefix was expanded and fully checked; it is not needed for the best bound.

## Finite family and proof

A strict bridge starts at (0,0), has every later first coordinate positive, and ends at its maximum first coordinate h. It is irreducible when every interior cut has at least three crossings. The certified family is the disjoint union of:

- All irreducible bridges of spans 1–18 with the span-specific transverse caps in the [main packet](frozen/c38_finite_strip/packet.json). At span h the range is at most w_h-1; at span 18, w_18=72.
- All irreducible bridges of spans 19–30, transverse range at most 22, and interior crossing count at most 5.

Translation fixes the start; no reflection quotient is taken. Each coefficient is a nonnegative integer count of actual irreducible bridges. The degree is at most 6817, from max(h*w_h) in the main family; the supplement has degree at most 690.

At b=M/2^27, M=51081913, the main computation gives exact lower values alpha_h for each finite span family. For h<=17 it also certifies full, all-range bridge and irreducible upper bounds by nonnegative integer upper potentials and exact renewal arithmetic. At span 18 only a finite sweep is used:

    alpha_18 = max(0, b_18 - sum_(j=1)^17 beta_j*U_(18-j)).

The subtracted reducible pairs have smaller spans and certified full upper values. No full span-18 upper sum is asserted. Its num_tail=0 is an unused marker, with infinite_tail_certified=false.

Let L17=sum_(h=1)^17 alpha_h and L18=alpha_18. A complete second-point replay supplies U, an upper bound for all irreducible bridges of spans<=17 at c=51082227/2^27. This also bounds the finite first-17 family there. For any nonnegative coefficient polynomial F and 0<a<b<c, the identity

    (b^n-a^n)/(b-a) = sum_(j=0)^(n-1) b^(n-1-j)*a^j

is at most the analogous sum with bases c,b. Summing coefficientwise and rearranging proves F(a)>=(1+t)F(b)-t*F(c), t=(b-a)/(c-b). At a=(M-k)/2^27, t=k/314. The finite span-18 polynomial obeys the explicitly proved Bernoulli lower bound (1-1296*k/M)*L18 when this multiplier is nonnegative.

For the higher-span supplement, let F22 count the completed width-22/cap-5 family of spans 18–30. Its span-18 part is contained in the completed width-23/cap-5 span-18 family H23. Thus the genuine nonnegative span-19–30 family E satisfies

    E(b) >= e = max(0, (lo22-hi23)/2^96)
               = 0.00005094176474102854... .

This subtraction bounds a value; it does not define coefficients by subtracting different range families. Since deg(E)<=690, E(a)>=(1-690*k/M)*e. The first exact comparison is

    (1+k/314)*L17 - (k/314)*U
      + (1-1296*k/M)*L18 + (1-690*k/M)*e >= 1,

at k=1352. Both linear multipliers are checked nonnegative, and every substitution has the required sign. The strongest refinement uses exact powers: put r=(M-k)/M. For each n<=N, r^n>=r^N because 0<r<1. Multiplying by the nonnegative coefficients gives G(a)>=r^1296*L18 and E(a)>=r^690*e. Therefore the sharper exact comparison is

    (1+k/314)*L17 - (k/314)*U + r^1296*L18 + r^690*e >= 1,

which passes at k=1353 and gives the headline fraction. The next point k=1354 fails this power-based sufficient inequality. Neither grid failure gives an upper bound on mu.

Concatenating these irreducible bridges gives a self-avoiding walk, and the singly crossed join cuts recover the factors uniquely. If P(a)>=1, the generating series for ordered factor sequences diverges at a. It is coefficientwise bounded by the SAW series. Submultiplicativity proves the connective-constant limit explicitly; if mu<1/a the SAW series would converge there, a contradiction. Therefore mu>=1/a. Nonnegative coefficients also give the originally requested P(400/1051)>=1.

Every underlying step is written in the frozen [finite-strip proof](frozen/c38_finite_strip/PROOF_FINITE_STRIP.md), [finite-last-span proof](frozen/c38_finite_strip/PROOF_LAST_FINITE.md), [state sufficiency appendix](frozen/c38_finite_strip/STATE_PROOF_APPENDIX.md), [arithmetic proof](frozen/c38_finite_strip/ARITHMETIC_PROOF.md), [secant proof](frozen/c38_secant_rescale/input/PROOF_SECANT_RESCALE.md), [disjoint-supplement proof](frozen/c38_disjoint_extension/input/PROOF_DISJOINT_EXTENSION.md), and [exact-power proof](frozen/c38_power_secant/input/PROOF_POWER_SECANT.md).

## Verification and reproduction

| Frozen computation | Completed check | Actual corruption cases |
|---|---|---:|
| Main spans 1–18 | Every separately written native span replay, then a further complete standard frozen-union replay | 35 |
| Full spans<=17 at two points | Complete native replays, then a further standard two-point aggregate replay | 11 |
| Range 22, spans 18–30, cap 5 | Complete fresh scalar native replay | 12 |
| Range 23, span 18, cap 5 | Complete fresh scalar native replay | 12 |
| Secant arithmetic extension | Exact three-term check | 22 |
| Disjoint supplement | Exact four-term check | 27 |
| Exact degree powers | Exact power/secant check | 22 |

Every recorded corruption produced its exact expected rejection. Main and two-point controls include rebound hashes followed by an actual fresh native run. The native verifier constructs transitions from explicit vertex degrees and component identities; production retains Plánočka's credited case-table construction. Both were written or adapted by this same agent.

Each producer input froze before its complete fresh native replay. The main union input SHA256 is c3b95cb5122603a8b09ae6b0001d90de5b45e9d32c82e86a351b6dd3f924cb88. Its packet SHA256 is 865241e4447884bb5354ba1799ab94baf4923bb4870e927a151cf14415d6faad. Its full standard replay finished 08:27:42 UTC in 4455.79 seconds. The complete two-point aggregate replay finished 09:48:18 in 4825.79 seconds. The rectangle replays took 11242.07 and 9406.44 seconds respectively; the last finished 10:32:03.


## Release validation and reading order

Start with [PROOF.md](PROOF.md), [REPRODUCE.md](REPRODUCE.md), [CREDIT.md](CREDIT.md), [exact enclosures](EXACT_ENCLOSURES.json), and [release validation](release_validation/summary.json). The candidate remains unrefereed, verification level L0 for the bound as a whole. The release freshly checks the frozen certificate and all 22 degree-power corruptions on the Mini; it does not repeat the large native enumeration. Native source, complete historical replay outputs and manifests are retained in frozen/. The full coefficient vector remains unmaterialized.

PROOF.md documents three scope/terminology cautions in the original prose. MANIFEST.json records release transformations; frozen mathematical inputs and certificates are unchanged. See [PRIOR_ART.md](PRIOR_ART.md) for the release source refresh.
