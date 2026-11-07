# Bento J011 — exact finite-kappa Nesterov certificate

State requested: claimed for separate referee and taste review. This worker supplies a proposed theorem and an independently checked exact certificate, without judging novelty or author interest.

## Published number and reproduced baseline

Safavi, Joshi, França and Bento, *An Explicit Convergence Rate for Nesterov's Method from SDP* (2018), Thm5/Eq26: https://arxiv.org/abs/1801.04492 and https://www.jbento.info/papers/nesterov_sdp.pdf . Bento's identity was checked from the primary paper's Boston College author/email block. For mu-strongly convex L-smooth objectives, kappa=L/mu, alpha1/L and the paper's tuned beta, the distance factor is sqrt(1-sqrt(2kappa-1)/kappa). At kappa25 this is beta21/32 and q_old=tau_old²=18/25, tau_old0.848528137423857.

Reproduced first: exact source P and all required LMI principal minors at kappa5,13,25,41, recorded in baseline_exact.json. The public Taylor–VanScoy–Lessard2018 N1 interpolation SDP (https://github.com/QCGroup/quad-lyap-first-order ; https://proceedings.mlr.press/v80/taylor18a.html) was ported and reproduced: README standard-k10 tau0.7518; source-tuned k25 numerical tau bracket[0.8485251525,0.8485327818], consistent with the source bound. All eight free-rho and eight fixed-rho A1 controls landed on existing boundaries without a verified gain.

Current literature was checked before search and again at the end. Pokutta–Stellato2026-10-10 (https://arxiv.org/abs/2610.15125) already gives exact optimal STANDARD-beta squared factors q10=0.5644232779728935... and q100=0.859899778052548..., and its public integer-dyadic checker was replayed successfully. Those are credited and are not claimed to be beaten. At k25 its standard beta2/3 differs from the source-tuned21/32 fixed here. The best *reported matched tuned-beta25 bound found in readable sources* remained q18/25. PRIOR_ART.md and SWEEP.md describe broader automated methods and coverage gaps; a public framework may already compute a stronger number.

## Proposed number and theorem

For every finite dimension, every (L/25)-strongly convex L-smooth differentiable objective and all initial points, run exactly

    y_t=(1+21/32)x_t-(21/32)x_{t-1},
    x_{t+1}=y_t-(1/L)grad f(y_t).

There is a finite uniform constant K such that

    ||x_t-x*||² ≤ K (3599/5000)^t
                     (||x_{-1}-x*||²+||x_0-x*||²),  t≥0.

Thus q_new=3599/5000=0.7198<0.72, an exact improvement1/5000, and tau_new0.8484102781084161. The new tau is below the entire reproduced public N1 numerical bracket. The certificate uses the existing public finite-history interpolation method with N32; this is an exact finite-parameter extension, not a new method or a standard-beta optimal-rate claim. The deliberately loose prefactor is about3.67545e44, so no useful finite-time improvement or sharp constant is asserted.

PROOF.md gives the complete argument. A35-dimensional quadratic-plus-function-value potential uses a finite look-ahead window of gradients; its decrease is a36-dimensional matrix inequality. Exact coercivity and an explicit uniform initial-potential bound turn it into the stated distance rate for all objectives, rather than a numerical trajectory claim.

## Exact certificate and controls

Root on the Mini: friends_pf_bento/J011_worker/ . Protected pod root: /workspace/bento/RESULTS/J011 . All small artifacts are copied back under pod_results/ with a SHA256-verified archive receipt.

- PROOF.md and REPORT.md: theorem, complete matrix conventions, proof, limitations and exact reproduction commands.
- pod_results/A2_strict_N32_candidate_rational.json: rational P,p,lambda,eta; SHA256651ce2bf58ca9cfdf1732aa357f335709de93928ce8fb035aaef69e747df3f6f.
- verify_A2.py and pod_results/A2_strict_N32_candidate_rational_VERIFIED.json: separately written checker, no imports from search/reconstruction; exact nonnegative multipliers, function equalities, positivity and decrease. Floating arithmetic chooses a rational congruence only; acceptance is exact strict diagonal dominance on the reconstructed rational matrices. Both positivity checks pass.
- pod_results/CONTROLS.json: negative-multiplier, broken-equality and noncoercive-storage corruptions all rejected. The exact scalar quadratic f(x)=mu x²/2 has characteristic roots21/25 and3/4, giving necessary squared lower bound441/625=0.7056, respected by the new universal bound. Quadratic-only analysis cannot certify this nonquadratic class. The familiar classical standard-beta q4/5 is a different-parameter reference, not the matched bar.
- pod_results/baseline_exact.json, public_baseline_25_tuned.json and latest_exact_dyadic.log: source, public N1 and recent exact standard-beta reproductions.
- ATTEMPT1.md/config_A1.json and ATTEMPT2.md/config_A2.json: distinct immutable attempt records. config_A2_extension.json predeclared the longer-history expansion. SWEEP.md was written after A1 failed and before A2. Numerical search traces remain diagnostic, not proof.
- pod_results/FINAL_SOURCE_CHECK.json: public-source hashes, dependency versions and access failures; pod_results/FINAL_PROCESS_CHECK.json: own research workers finished; BACKUP_RECEIPT.txt and pod_backup.tar.gz: verified transport.

No dataset or hold-out is used for this all-function theorem; no sealed evaluation data was opened. No biology, person contact, post, external publication or account creation occurred. Only J011 is changed. The Mini did editing and small transport; research computation ran on mscr with nice10. Preliminary CLARABEL long-history runs exposed solver-native threading despite BLAS caps; affected own workers were stopped and the accepted candidate/verification used explicit one-thread solver settings. The earlier aggregate peak was not fully measured, so full-session eight-core compliance is not asserted. No extra compute is requested.

## Review scope and remaining uncertainty

The requested _codex/friends_pf_bento.md was absent; RULES.md and the available friends_board_bento_1103.md were read, with the user's row-specific instructions controlling. That available driver has no exact CLAIM.md template; this packet follows the existing queue claim's problem/baseline/theorem/evidence/review structure.

Final source recheck was2026-11-03 13:58 UTC. GitHub issue/PR APIs returned403 and web cache misses; code-search and indexed X/community coverage are incomplete. No sharper reported matched number was located in readable sources, which is not proof of novelty. The strongest review questions are whether the exact finite-kappa extension is already implicit or reported elsewhere, whether such a small gain from an existing method is substantial, and whether the look-ahead potential argument and coefficient conventions withstand independent verification. Those judgments belong to the separate referee and taste process. Nothing is sent to an author by this worker.
