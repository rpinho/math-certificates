# Candidate C22b <= 7.087559024 — round 4

[C22b, Tao page 22b](https://teorth.github.io/optimizationproblems/constants/22b.html)
is the infimum of ropelength per crossing over alternating knots (and links).
Ropelength is the infimum of contour length divided by thickness over
embeddings; **thickness is a radius**, so unit thickness requires nonlocal
separation 2.

**Candidate bound: C22b <= 7.087559024**, below **Doldrums / SCiEL's
7.087662112*** ([PR #342](https://github.com/teorth/optimizationproblems/pull/342))
by **0.000103088**, under the same definition.

The producer's interval verifiers were separately written by the same AI
agent as the search. A clean-room AI referee, **GPT-6 Astra via Codex**,
did not read or run the producer's code, wrote its own checks, and found
**VERDICT: HOLDS**. This is an AI referee, not a human review.

**Verification level: L0** for the bound as a whole (definitions: https://github.com/rpinho/math-certificates/blob/59eeb7097f806da05187b5f234445be3589204d4/VERIFICATION_LEVELS.md)
The interval verifiers were separately written by the same AI agent, a clean-room AI referee on a different model wrote its own checks and found it holds, and the prose reductions still need mathematical review.

## Finite value and limit

For every integer n>=1 the specified closed curve has thickness at least 1,
knot type T(2,1324n+3) up to mirror, and contour length at most

    L_n <= 7.087559024*(1324n) + 150.

The directly checkable **finite n=1 bound** for T(2,1327) is

    Rop(T(2,1327))/1327 <= 148967627309/20734375000
                           = 7.18457283178296910324... < 7.184572832.

This uses the certified uniform cap allowance 150, rather than estimating
the finite value from a limiting coefficient. The **family limit bound** is

    C22b <= lim_{n -> infinity} (7.087559024*1324n+150)/(1324n+3)
          = 7.087559024 = 442972439/62500000.

The actual body coefficient is enclosed by the producer as
[7.087559023364 +/- 3.23e-13] and by the referee as
[7.08755902336373937805, 7.08755902336373937815]. Both are below the claimed
rational. The cap length is below 134.481173616861, hence below 150,
uniformly in n. These are upper bounds, not claims of optimal embeddings.

Doldrums / SCiEL / CPIL lab MBZUAI's even-radius modulation in #342 is the
starting idea. The four-strand superhelix, rational closure and caps come
from our #324, building on Huh–Kim–Oh and Youhua Li / Claude Opus 5.5.
See [CREDITS.md](CREDITS.md) for authors and classical theorem credits.

## Exact construction

All coefficients are exact rationals in
[CONSTRUCTION.json](candidate_high/CONSTRUCTION.json); the authoritative
tighter final bound is [BOUND.json](candidate_high/BOUND.json).
Construction SHA-256: `98ebe816e90e3898029e8019ef769518d003cedc98e0462f79d8659f0e0f160c`.
The auxiliary coefficient in CONSTRUCTION.json is a looser intermediate
claim; verify_result.py checks the tighter BOUND.json value separately.

Use N=331/6, R=2.932410534395, b=0.324186853064,
h=(N-1)b, s=sqrt(R^2+h^2), and lambda=1.000001. Every terminating
decimal below is exact. Define a(u)=sum a_k cos(ku),
i(u)=sum i_k cos(ku), and v(u)=u+sum p_k sin(ku).

| k | a_k | i_k |
| --- | --- | --- |
| 0 | 1.931566317919 | 0.078282208598 |
| 1 | 0.000856026859 | -0.000458314446 |
| 2 | 0.000001382955 | -0.000028104853 |
| 3 | -0.000008283669 | -0.000038357531 |
| 4 | -0.000006329464 | -0.000027421237 |
| 5 | 0.000001431805 | -0.000003084633 |
| 6 | -0.000000012009 | 0.000000203917 |

The phase coefficients are

    p_1 = -0.001210416525
    p_2 = 0.000035930304
    p_3 = 0.000071834467
    p_4 = 0.000244560086

For c in {-1,+1} and signed radius r=a or r=-i, set
A=R-r(u)cos(v(u)) and B=(h/s)r(u)sin(v(u)), then

    X=lambda*c*(A*cos(u/N)-B*sin(u/N)),
    Y=lambda*c*(A*sin(u/N)+B*cos(u/N)),
    Z=lambda*(h*u/N-(R/s)*r(u)*sin(v(u))).

The finite body is u in [0,2*pi*331*n]. All phases return after six
core turns per block. Use the inherited nested lower cap and swapped
upper cap with connector radii 15/2 and 63/2, vertical clearance 21/10,
and the actual endpoint unit tangents. Complete circle formulas, joins
and the all-n argument are in [PROOF.md](PROOF.md) and
[the round 1 proof](../round1/PROOF.md).

## Computation and proof scope

The release replay is in [release_validation](release_validation/), with
commands in [REPRODUCE.md](REPRODUCE.md). The source-time producer outputs
are preserved in [producer_logs](producer_logs/); their historical
“unrefereed” qualifications predate the clean-room AI referee.

- The producer checks all **22 geometry covers, 1006199 leaves** at 180-bit
  Arb precision, including body curvatures, outer self and outer/inner
  distances, all 16 cap/body interfaces and both lower-cap pair domains.
- Scalar checks certify positive height derivative, cross-bundle distance,
  short-arc bounds, tails, caps and joins. Actual-speed degree-six interval
  Taylor integration on 256 cells per radius includes all radius and phase
  derivatives, with remainder below 8.32e-14.
- The physical projection has **52668 leaves, 32229 inverse-height brackets,
  1088 events and 1868 crossings**. It gives body action
  `[[1,0],[1324,1]]` and identity material permutation.
- The supplementary actual-word Fox calculation gives determinants
  **1327, 2651, 3975** for n=1,2,3. Determinant agreement alone does not
  identify the knot. Finite alternating-diagram examples also pass.
- The **21 construction corruption controls** and **108 original controls**
  yield their specified rejections.
- The referee regenerates full-domain covers and uses projection X+Y/4,
  obtaining **1090 events, 1870 crossings**, the same body action and
  determinant 1327 at n=1. Different projections can have different raw
  crossing counts. The minimal crossing number comes from the knot-type
  argument, not those raw counts.

Computation certifies finite interval inequalities, full partition coverage,
Taylor remainders, physical block projections and exact algebra. The
[proof](PROOF.md), which depends on [round 1](../round1/PROOF.md), supplies
the exhaustive 210 piece-pair reductions, gluing and embeddedness,
application of the thickness theorem, all-n rational-tangle identification,
reduced alternating crossing minimality and passage to the limit.
The [AI referee report](referee/REFEREE.md) addresses these reductions;
passing programs alone does not establish them. Human mathematical review
of these prose steps remains needed.

BOUND.json is authoritative for the final coefficient and binds it to
construction SHA-256
`98ebe816e90e3898029e8019ef769518d003cedc98e0462f79d8659f0e0f160c`.
CONSTRUCTION.json preserves its earlier looser 7.087581 coefficient and
source-time status. The selected contact certifies a thickness upper
bound at specified points, not a global contact minimum. The referee
corrects an obsolete separation value from its instructions: the selected
scale is 1.000001 and the cross-bundle lower bound is
2.000001999997999998. Its proof uses Q=6; the linked published round 1
proof already incorporates the rational-height Q correction.

## Prior art and reproducible starting point

Round 3's 7.087580303 was replayed before the producer's search; its saved
result is [baseline_replay.json](producer_logs/baseline_replay.json).
Doldrums's exact certificate could not be retrieved by the producer:
the Zenodo record was restricted, with no downloadable construction.
Its 7.08766211189 certificate is therefore not represented as reproduced
or refuted. This access limitation occurred before any geometry replay.
[PRIOR_ART.md](PRIOR_ART.md) records inherited sources and this release's
refresh.

The exact construction, covers, projection and producer checkers are
unchanged. Only three referee input paths are remapped; formulas and saved
JSON are unchanged. Historical prose citations and model descriptions
are adapted to this release layout. The original-controls copy retains
its mathematical inputs and checkers, omits duplicated prose, and has
regenerated local indexes. See MANIFEST.json and SHA256SUMS for all members
except those two top-level indexes themselves.

This release adds no new search; it packages the producer's candidate and
the AI referee report. There is no optimality or exhaustive priority claim.
