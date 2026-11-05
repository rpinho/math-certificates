# Candidate C68 >= 447/1000 = 0.447 (rigorous, verify_measure.py)

**The frozen bar is met by a candidate, unrefereed analytic proof.** The exact
rational artifacts and all quantitative hypotheses pass verification. Both
methods were tried. Verification programs are **separately written (same agent)**;
there is no human mathematical endorsement or formalization, and no novelty
judgment is made.

The candidate is larger than the supplied 8937/20000 baseline by exactly
3/20000 = 0.00015. The written implication is: for every f,u in A²(D),
|f|<=|u| on 447/1000<|z|<1 implies ||f||₂<=||u||₂ (rigorous, verify_measure.py).

Credit first to **V. Patankar** (@vidigoat), [PR #274](https://github.com/teorth/optimizationproblems/pull/274),
for the retained flux and enclosing input; **Chunjie Wang** for the
[coefficient approach](https://doi.org/10.1090/proc/17112);
**Frank Wikström** for [moment integration](https://arxiv.org/abs/2607.17748);
and **Ricardo Pinho** for
the covering-strip, contact and signed outer-factor constructions. Schuster's
annular pseudodistance approach is an antecedent cited in the retained paper.

## What supports the candidate

[PROOF.md](PROOF.md) gives the norm implication, every moment reduction and
both tails. [INPUT_GREEN_FLUX.md](INPUT_GREEN_FLUX.md) and
[INPUT_ANGULAR.md](INPUT_ANGULAR.md) give the retained derivations with corrected
Patankar attribution. [CONTACT_ROW_LEMMA.md](CONTACT_ROW_LEMMA.md) gives the
changed analytic input and its positive moment/Schur-complement formulation.

At every balancing contact, the same hyperbolic cosine-rule average equals
h². Keeping the individual rows before averaging gives

    h² <= H²-D*max_i T(theta_i).

For a=|m1| and q0=E[cos²(theta-arg(m1))], the elementary support inequality
(X+1)(M-X)>=0 yields

    max_i T(theta_i) >= J=a(q0+a)/(1+a).

The weight becomes max(S,J,T), retaining the joint first/second contact
harmonics and their relative phase. Its verified linear-coefficient constant
is 23/200=.115, using the contact moment PSD constraint and the outer-factor
Schur complement (rigorous, verify_row.py). This corrects coefficient one only.

The frozen measure has eight positive rational atoms of mass 99/100 plus
Lebesgue measure on [99/100,1]. The main checker uses an explicit cubic lower
envelope for the continuous integral; the alternate implementation uses a
fresh 5000-cell interval envelope and exact integer ordinary moments.

| Verified condition | Primary receipt |
|---|---|
| Ordinary moments k=1,...,5999 | minimum relative margin >7.86562e-6, k=172  (rigorous, verify_measure.py) |
| Weighted moments k=1,...,1799 | minimum relative margin >7.68082e-6, k=648  (rigorous, verify_measure.py) |
| Ordinary infinite tail k>=6000 | exact last-atom gap 33/200000  (rigorous, verify_measure.py) |
| Weighted infinite tail k>=1800 | propagation gap >8.88107e-10  (rigorous, verify_measure.py) |
| Scalar parameter cover | 265 grid, 17 PSD, four constant and one small leaf |
| Scalar finite-leaf margin | >2.04388e-5  (rigorous, verify_row.py) |
| Small-parameter log margin | >0.01616841  (rigorous, verify_row.py) |
| Corrupted artifacts | all 35 exact expected rejection codes PASS |

The source job's 320-bit replay, controls and alternate arithmetic replays
passed. This release reruns the full replay, all 35 exact expected rejection
controls, retained counterexamples and exact contact/auxiliary checks on the
packaged files. Fresh receipts are in logs/verification-final.json,
logs/controls-results.json and logs/alternate-*.json; historical receipts are
explicitly separated under logs/source/. See REPRODUCE.md and
logs/release-checks.json for the fresh outcomes. The acceptance checker
recomputes the complete scalar cover; it does not trust a saved PASS.

Frozen artifact SHA-256:

* certificates/certificate-0447.json:
  `d9dd308f94efb019368682367609d9fa71c9982bb7195b27da22bb80d02f4afe`
* certificates/row-cover.json:
  `fda0aa1430313c3f896021073f3a44c3b1b920d2b07451d3b7d58d7d4d0bfc27`

FROZEN_MANIFEST.json covers the proof, acceptance code and exact artifacts.
The manifest records source hashes; documentation-only release edits are
listed in MANIFEST.json. Programs certify numerical hypotheses and exact
coverage; the complex analysis, contact geometry and outer-function argument
remain written, unrefereed mathematics. [PROOF_AUDIT.md](PROOF_AUDIT.md) records
the same-agent analytic audit and that verification boundary.

## Retained failures, and why this uses the row input

The old .105 counterexample is reproduced by exact-arc Arb integration:
its old-weight energy is 0.1044575940727006..., while its row-weight energy
is 0.6668411467973089... (estimate, verify_retained.py). Its moments are PSD; they were not discarded on
that basis. The naive third-diagonal extension still fails by exactly -1/100 (rigorous, verify_retained.py).
The exact balanced two-contact endpoint and a rational three-contact example
also pass; the latter has J>S while satisfying all geometric pair constraints.
Their scope is geometric, without a claimed annular interpolation.

[INEQUALITY_AUDIT.md](INEQUALITY_AUDIT.md) proves a useful same-measure comparison.
At c=.447 the full old .095 weighted k=1 margin, including an upper bound
for its continuous correction, is less than -0.00003324623828 (rigorous, verify_measure.py). The new
sufficient margin exceeds 0.000003854649777 (rigorous, verify_measure.py). Thus this frozen measure fails
the old criterion. The accepted result uses the row input; no optimality
limit for other old-criterion measures is asserted.

## The second method and the pilot

[TWO_RADII_LEMMA.md](TWO_RADII_LEMMA.md) derives the exact cross-contact Lorentz
identity, valid radial transport and a shared-center outer-factor Schur
complement before optimization. Paired LPs screened 5892 radius pairs and
251 sampled outer-factor cases; both selected zero unequal-radius mass.
The old-weight screen had negative margin. This transported family gave no
improvement; its sampled values are not certificates.

[CROSS_RADIUS_FLUX.md](CROSS_RADIUS_FLUX.md) extends Patankar's flux argument
to unequal radii and derives a sharper necessity for the two true contact
measures. Explicit algebra shows that this relaxation still admits the
retained bad relaxed moments at every pair of radii. This is a failure of
that proposed relaxation, not a barrier for every two-radius approach.

The unbundled historical pilot record reports PASS_CONTINUE before the six-hour deadline. Both retained
counterexamples and extremal contact configurations were checked within the
pilot. Sustained diagnostics then ran until 10:50 UTC: 149647446 total tests
across contact geometry, scalar minimization, polynomial Toeplitz minimizers
and annular-map families, with no recorded failure. These are diagnostics,
not proof or a measured probability of correctness. Failures and limitations
of every attempted method are recorded in [ATTEMPTS.md](ATTEMPTS.md).

## Release contents and reproduction

This README is adapted from the source job's unbundled report. Operational details,
private machine paths and unreleased diagnostic logs are excluded. Source
search and pilot results above are historical reports, not fresh searches
or new certificates produced by this packaging job. The pilot record and large
screening logs are omitted. No human mathematical endorsement is claimed.

The runtime acceptance core is verify_measure.py plus verify_row.py and the
two frozen certificate files. verify_alternate.py is a further arithmetic
implementation by the same AI agent. The rejection suite, retained-example
checker, auxiliary checker and contact-configuration checker are included.
certificates/moment-0115-float.json is historical search output, not an
acceptance certificate; no optimizer is required or imported.

[REPRODUCE.md](REPRODUCE.md) gives single-process, nice-10 commands and the
Python dependencies. [MANIFEST.json](MANIFEST.json) records source provenance
and transformations. SHA256SUMS covers the complete release including the
manifest. [PRIOR_ART_RELEASE.md](PRIOR_ART_RELEASE.md) records the live audit;
[PRIOR_ART.md](PRIOR_ART.md) is the source job's initial and final audit.
The frozen source manifests are historical provenance records and do not
serve as the release inventory (the historical source manifest is deliberately omitted).

Credit is V. Patankar (#274) first, then Wang, Wikström and the earlier
signed-contact step. The predecessor README's attribution of the flux input
to David Niedbala Giraudin was wrong: #274 and the source proof are V. Patankar's.
Older c68 folders keep that wrong name for checksum reasons; [../CREDIT_CORRECTION.md](../CREDIT_CORRECTION.md) overrides it. #274's own diff credits V. Patankar (table row and bibliography), and its commits are authored by Vidit Patankar.

**Verification level: L0** for the bound as a whole (definitions: https://github.com/rpinho/math-certificates/blob/59eeb7097f806da05187b5f234445be3589204d4/VERIFICATION_LEVELS.md)
The verifiers were separately written by the same AI agent; the new contact-row lemma is a prose argument needing mathematical review.

AI use and author review: Analysis and proof drafting by AI agents under my direction; I reviewed the results at summary level. AI agents also prepared the certificates, checkers and submission text. This does not claim a line-by-line human verification.
