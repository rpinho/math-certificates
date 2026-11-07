# bento J012 — candidate restricted-weight path theorem

State requested: claimed, for a separate referee and taste step. No novelty or author-interest verdict is made by this worker.

## Published number and location

Bento, Furmaniak and Ray, *On the Complexity of the Weighted Fused Lasso*, IEEE Signal Processing Letters (2018), https://arxiv.org/abs/1801.04987v3 , Eq.(2), Thms2–4 and §IV. With n observations, the unrestricted positive-weight path has tight Θ(n²) affine pieces; equal weights have T≤n. §IV asks for weight/input conditions giving O(n). Identity checked on the primary paper: Bento's bc.edu affiliation and coauthors match the author page.

The stronger trivial prior-art control is Tibshirani–Taylor (2011), https://stat.cmu.edu/~ryantibs/papers/genlasso.pdf , §6 Eq.(23): diagonal dominance gives T≤n for all zero-padded concave weight profiles. This killed attempt 1 and is explicitly credited.

Reproduced first: the 2018 paper's Fig.1 instance y=(0,−1/2,1/2,1/2), α=(1/50,1/2,1/2). Exact T=5 and knots 25/27,25/23,100/73,25/4; the printed edge-1 fusion/unfusion values match. Same y with equal weights: T=3, zero unfusions. Small n=3,...,10 instances of the printed Thm4 construction were also certified, without claiming those finite values establish its asymptotic lower bound.

## Proposed number / theorem

Pad the positive weights with a_0=a_n=0. Let H be their least concave majorant, k the number of strict deficits a_i<H(i), and g=n+1−k. For every real input y, claim

    T ≤ min{3^k(g−1), 1+8[2g−3+gk+k(k−1)/2]} = O(n(k+1)).

Thus bounded k gives O(n) while allowing unfusions. For k=1, T≤3(n−1). A simple family consists of any positive padded concave weight profile with at most k entries decreased, preserving positivity. This refines the general quadratic guarantee on a nonconcave family; it does not lower the observed five-piece baseline or change the unrestricted quadratic order. It is a sufficient condition, not a complete classification or a runtime/sharp-constant claim.

PROOF.md supplies the all-n argument: envelope-contact coordinates never re-enter the taut-string contact set; their adjacency pairs only accumulate linearly, while exceptional endpoints contribute O(nk+k²) pairs. The source paper's at-most-eight-events-per-pair argument then applies. A separate signed-face count gives 3^k(g−1), directly with degeneracies; the polynomial proof includes a perturbation/limit argument preserving all good indices.

## Code and data on the Mini

Root: friends_pf_bento/J012_worker/

- PROOF.md — full theorem, assumptions and proof.
- exact_faces.py — rational taut-string face enumeration search.
- verify_paths.py — independently written primal subgradient KKT verifier; no imports from search.
- verify_panel.py — complete-path and all-chord checks on diagnostics.
- verify_theorem.py — exact symbolic identities and finite combinatorial checks.
- run_panel.py and pod_baseline.sh / pod_panel.sh / pod_poll.sh / pod_theorem.sh — reproduction commands, also listed in REPORT.md.
- pod_results/baseline_paths.json and baseline_verification.json.
- pod_results/panel/ — 73 small complete rational path certificates; panel_manifest.json fixes their input vectors; panel_verification.json and EXACT_TABLE.md give results.
- pod_results/theorem_verification.json and zero_cut_control.json.
- PRIOR_ART.md, SWEEP.md, pod_results/sweep_api.json and final_source_check.json — source checks and limitations.
- ATTEMPT1.md, ATTEMPT2.md, config_A1.json, config_A2.json — two distinct immutable attempt records. A2 changes the formulation from forbidding unfusions to controlling exceptional indices; it is not a retune.
- results_backup.tar.gz and BACKUP_RECEIPT.json — base64 transport archive with matching pod/local SHA-256. Protected pod source: /workspace/bento/RESULTS/J012.

All computation was on bio2, at most eight single-threaded workers with nice 10. The Mini only edited and transported small files. No hold-out was needed/opened for this all-data mathematical statement. No person was contacted and nothing was posted/published.

## Verification and controls

All 73 complete diagnostic paths passed independent rational primal KKT, including the λ=∞ tail, interval coverage, continuity and actual slope changes. Twenty-seven exhibit unfusions. Examples beyond diagonal dominance: k=1,n=10,T=12 with one unfusion; k=2,n=4,T=6 with one unfusion; a concave-parabola profile with one dip has k=1,n=6,T=8 and one unfusion. The known no-unfusion control fails on these weights. Replacing the positive low edge by zero (independent-component control) yields a path rejected under the original positive-weight objective. Three deliberately corrupted baseline certificates were rejected.

Separate checks passed 12 symbolic identities, eight universal signed derivative decompositions, and 46,234 finite monotone-deletion schedules. The universal mathematical conclusion is the written proof, not an extrapolation of the finite panel. The analytic steps are not formalized in a proof assistant.

## Prior-art recheck and concerns

Final primary/code API recheck at 2026-11-03 02:14 UTC: source remains arXiv v3; author code commit a2c2dd005d6fbaf1e8d6a04438cc2c08f7907ec3 has no open issues or PRs. Updated public repository searches, recent papers including 2025 ADMM and 2602.02406 v2, and indexed AI-lab/community/X searches located no matching envelope-defect bound. GitHub authenticated code search returned HTTP401; indexed X search is incomplete. These gaps and whether the deduction is already known belong in the referee's assessment.

Main review risks: validity of the endpoint-pair amortization and generic-to-degenerate limit in PROOF.md; whether this restricted family is sufficiently substantial; and whether unindexed literature already states this corollary. Concavity alone is already public prior art. The requested _codex/friends_pf_bento.md was missing; the worker read RULES.md and the active friends_board_bento_1103.md plus the user's explicit instructions. No referee or taste verdict is supplied here.
