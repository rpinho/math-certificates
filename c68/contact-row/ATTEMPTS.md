# Attempts — math_c68_1104

All searches are diagnostic until exact/Arb certification and a full written
proof pass. Acceptance verifiers are separately written (same agent).

No research search before PRIOR_ART.md and BAR.json. Baseline replay pending.

Retained rejected proposals to replay: relaxed one-coefficient constant 0.105
(degree-128 rational polynomial, m1=1/50,m2=1); naive three-diagonal constant
7/100 (degree-eight rational polynomial, m1=0,m2=1, exact gap -1/100).
Neither failure refutes the baseline 0.095 or the Bergman candidate.

01:32 UTC. Baseline 0.44685 replay PASS at 320-bit Arb; frozen hashes match.
All 5999 ordinary and 1799 weighted moments, scalar cover, and both tails
pass in 46.64 seconds. This is a supplied baseline checker, not a newly
written acceptance verifier.

Method 1 proposal A: CONTACT_ROW_LEMMA.md derives a stronger constant floor
from each contact row before averaging. Its moment positivity constraint
alone does not remove the 0.105 counterexample; the new row bound changes
that example's floor from 0.0004 to 0.02. Uniform PSD-domain minimization,
actual probability-moment sampling, and the two retained polynomials are
running on the pod. A separate floating moment LP tests 0.447 at zeta=0.115.
Neither is an accepted bound.

01:39 UTC. Method 1 proposal A passes its new Arb verifier at 256 bits on
the frozen 287-leaf cover, and the full radius-0.447 measure verifier at
320 bits. Uniform zeta=23/200=.115; all ordinary indices 1..5999 and
weighted indices 1..1799 pass, and both infinite tails close. The old .095
criterion on the same measure has a negative full k=1 upper margin, below
-0.0000332462. This is a candidate, unrefereed result, pending the remaining
controls, adversarial tests and full resource/deadline closeout.

01:45 UTC. Both retained counterexamples reproduced exactly/with exact-arc
Arb integration: old .105 energy .1044575940727..., row-weight energy
.6668411467973...; the third-diagonal failure is still exactly -1/100.
All 34 corruption controls return their prescribed exact rejection codes.

Method 2: TWO_RADII_LEMMA.md derives the exact cross-contact Lorentz identity,
a valid unequal-radius strip necessity, shared-center radial transport, and
the two-radius outer-factor Schur complement before optimization. A positive
mixture with no genuine coupling is only a measure reparameterization.
Paired LPs with 450 base nodes, seven separations in both directions and
sampled outer-factor banks have finished. Both assign zero weight to all
off-diagonal pairs. Failure reason: in this sampled transported family the
shared-center transport cost outweighs the variance term; it supplies no
gain over single-radius atoms. This is a numerical negative for this family,
not a theorem excluding all coupled-radii arguments. The row-based paired
screen remains feasible, while the old-weight paired screen does not support
the required 0.447. Full numbers are retained in logs/two-radii-*.json.

01:49 UTC. Alternate checker implementation failure: mpmath.iv has no cosh,
sinh or tanh methods in this environment. The exact integer ordinary-moment
part had already passed. Replaced those functions by their exponential
identities and restarted the alternate measure check. This is a software
API failure, not a failure of the candidate inequalities. The original log
is retained as logs/alternate-measure.log.

01:53 UTC. Arithmetic audit made the directional max/min rounding helpers
explicit in verify_row.py, avoiding reliance on exact endpoint balls when
using a helper with the opposite rounding direction. Mathematical formulas
and frozen artifacts are unchanged; a full replay is running on this code.
This conservative implementation cleanup was identified during review; no
failed bound or failed artifact was found in the preceding receipts.

02:00 UTC. The alternate interval measure replay passes. It uses exact
integer ordinary moments and a fresh uniform 5000-cell lower envelope for
weighted moments, rather than the main checker's cubic. The two implementations
are separately written (same agent); no second party is claimed. The alternate
scalar implementation uses mpmath.iv and direct trigonometric cell ranges.

02:28 UTC. Added a corruption that merges a broad positive-floor parameter
branch into one grid leaf. Its required rejection is GRID_SCALAR_MARGIN,
so the controls now exercise a numerical scalar failure as well as malformed
schemas, false PSD exclusions, false constant/small leaves, moment failures
and both tail mechanisms. The augmented controls are running on the pod.

Method 2 refinement B: CROSS_RADIUS_FLUX.md extends Patankar's period argument
to unequal radii, proves Phi_e<=Phi_0+e/2 by differentiation, and derives
a sharper necessary constraint on the TWO true contact measures. Failure
reason is explicit algebra: that cross-moment relaxation still admits
m1=a,m2=1 at every radius with the old scalar floors. The squared feasibility
gap is K[2e-(sin u-sin v)^2]+2e sin u sin v+e^2>=0. Thus this relaxation
alone does not remove the retained .105 obstruction. This is a specific
negative for the proposed relaxation, not a global two-radius barrier.
The successful candidate continues to rely on method 1's contact rows.

02:28 UTC. The augmented 35-control suite PASS: the merged broad leaf gives
exactly GRID_SCALAR_MARGIN, as prescribed. The revised directional-rounding
acceptance implementation also passes its full 320-bit replay. All frozen
measure and cover hashes remain unchanged.

Auxiliary false proposals (exactly rejected): replacing the projected floor
by |m1| fails on a rational balanced two-contact geometric relaxation;
its precise scope and certificate are in AUXILIARY_FAILURES.md. Raising the
one-coefficient constant to 13/100 fails on a rational odd polynomial with
energy 42/325 and exact gap -1/1300. Both prescribed rejection labels pass
verify_auxiliary.py. Neither is a counterexample to the accepted .115 row lemma.

Other failed operations, preserved as limitations: the first PSD differential-
evolution run reached its iteration limit, so its approximate minimum was
never used as proof; the frozen cover supplied the acceptance instead. An
initial gh repository search used unsupported JSON field nameWithOwner and
was rerun with fullName. The guessed 2024 AMS PDF path returned 404; the
correct 2025 PDF/viewer and alternative path returned 403. Full original
Wang access is unavailable, as recorded in PRIOR_ART.md.

04:27 UTC. Exact geometric controls PASS. The balanced two-contact limit
has m1=0,m2=1 and normalized radius exactly one, saturating the old enclosing
bound; the three-contact rational example has S=666329/10291264 and
J=0.24821680556056..., a strict strengthening, while every Fourier pair
constraint and each balancing row identity holds exactly. These are geometric
controls, not claimed holomorphic annular interpolants.

Six-hour pilot: PASS_CONTINUE, frozen in PILOT.json. The row correction has a passing exact/Arb certificate and separately written (same agent) acceptance checks. Both retained false statements remain refuted. The proposed two-radius relaxations gave no gain, for the recorded numerical and algebraic reasons. An operational patch at 06:25 first failed a context match without changing files; the files were reread and the corrected patch applied. No mathematical artifact changed.

09:04 UTC onward: direct SSH transport times out. Multiple ten-second retries failed, with no authentication or remote-command execution. Successful math artifacts and receipts were already pulled locally; the 09:03 monitoring snapshot is additionally preserved. This is an operational connectivity failure, not a mathematical rejection. Recovery attempts remain read-only and do not change pod lifecycle or other jobs.

Transport recovery: direct endpoint timed out from about 09:04. The registered provider SSH proxy reached the exact same pod and BAR hash. Emergency tar checkpoint completed 09:13:06 UTC; actual rsync over a framed SSH bridge then succeeded around 09:17. An initial unframed binary-over-PTY bridge failed signature verification because the PTY altered bytes; the host key was separately checked against the pod public host key and matched. ASCII framing restored byte-exact SSH/rsync. No mathematical artifact changed. One successful checkpoint gap exceeded 30 minutes because of the outage; final deadline remains achievable.

Final replays: the full 320-bit acceptance checker and all 35 exact artifact-corruption controls passed again by 10:52:41 UTC, together with retained, auxiliary and exact-contact controls. The first process-audit filter falsely matched the parent orchestration shell because its command line mentioned verifier filenames; it was restricted to actual Python numerical processes and rerun. This was an audit-filter failure, not a mathematical rejection.

Closeout synchronization audit found two automatic successful-pull gaps above 30 minutes: 2119.466514 seconds and 1874.405039 seconds. They correspond to direct SSH outage and a later proxy heartbeat timeout. All math artifacts were preserved and all later results recovered. Initial documentation mentioning one gap described the earlier recovery point; the final report and audit record both.

2026-11-04T11:10:57.550711+00:00 — Minimal bundle replay PASS (56.49 s), with search programs absent and environment/user-site imports disabled. Frozen hashes unchanged. A local archive process filter initially matched another job's SSH client solely because it used the shared pod alias; restricting the filter to this job's exact directory fixed the false positive. No other-job process was touched. The corrected archive integrity audit passes.

2026-11-04T11:11:44.681053+00:00 — Final prose review clarified PROOF_AUDIT.md: the selected zero's unremoved strip lifts belong to the Green-comparison remainder, while other annular zeros and the harmonic term supply the flux remainder. The full frozen derivation already distinguishes these; no proof, acceptance code or numerical certificate changed.

2026-11-04T11:17:21.011672+00:00 — Final resource-audit invocation first omitted its required --output argument and exited 2 before performing the audit. Rerun with --output logs/resource-final.json; the following process audit remains required. This was an orchestration argument error, not a mathematical failure.

2026-11-04T11:20:41.193217+00:00 — The broader process audit found 26 orphaned framed SSH forwarding helpers from recovery. These were transport processes, not numerical workers. cleanup_forwarders.py identified them by exact forwarding code and this job's exact cwd and sent SIGTERM only to those PIDs. The 11:19:06 audit passes; the current transport has an absolute 60-second lifetime. All final framed transfers also use that limit. A plain-provider final read will confirm that the bounded helpers have exited without creating another forwarder.

2026-11-04T11:21:41.750821+00:00 — Final plain-provider audit PASS at 11:21:07 UTC: no owned Python numerical workers or forwarding helpers remained. The provider shell exited normally, SSH exit 0; no new framed helper was created. Final actual rsync passed at 11:19:40 UTC. All mathematical artifacts, both methods and retained failures are preserved locally. Final local archive audit and manifest follow.

2026-11-04T11:24:06.829267+00:00 — Run complete: candidate/unrefereed .447 accepted by frozen exact/Arb checks, with both infinite tails and 35 exact rejections. The first method supplies the contact-row correction; the second method failed to improve the examined coupled relaxations/families. Final metadata and full archive hashes retained.
